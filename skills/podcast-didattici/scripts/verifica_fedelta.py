#!/usr/bin/env python3
"""Controllare copertura della fonte e verbale QA, senza fingere di ascoltare l'audio.

Usare pagine canoniche estratte e verificate visivamente. Vedere
references/fedelta-pdf-e-revisioni.md e templates/SCHEMA_AUDIT_FEDELTA.json.
Nessuna rete, TTS, generazione o modifica dei file multimediali.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


class AuditError(ValueError):
    pass


def require(ok, message):
    if not ok:
        raise AuditError(message)


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def read_json(path):
    with Path(path).open(encoding='utf-8') as f:
        value = json.load(f)
    require(isinstance(value, dict), f'{path}: atteso oggetto JSON')
    return value


def text(value, label):
    require(isinstance(value, str) and value.strip(), f'{label}: testo mancante')
    return value


def norm(value):
    # Non cancellare accenti, punteggiatura, cifre, citazioni o parole ripetute.
    return re.sub(r'\s+', ' ', value).strip()


def resolve(value, parent):
    p = Path(text(value, 'percorso'))
    return p if p.is_absolute() else parent / p


def same_text(expected, actual, label):
    require(norm(expected) == norm(actual), f'{label}: testo o ordine diverso dalla fonte')


def audit(pages_file, manifest_file, mp4_file=None, review_file=None):
    pages_file, manifest_file = Path(pages_file), Path(manifest_file)
    pages, manifest = read_json(pages_file), read_json(manifest_file)
    pdf = resolve(pages.get('pdf_path'), pages_file.parent)
    source_hash = text(pages.get('pdf_sha256'), 'pdf_sha256')
    require(sha256(pdf) == source_hash, 'Il PDF corrente non corrisponde allo SHA-256 delle pagine canoniche')
    require(manifest.get('pdf_sha256') == source_hash, 'Manifest riferito a una diversa versione del PDF')
    require(manifest.get('mode') == 'integral_from_current_pdf', 'Questo audit integrale non certifica una riparazione selettiva')
    result = subprocess.run(['pdfinfo', str(pdf)], capture_output=True, text=True, timeout=30)
    require(result.returncode == 0, 'Impossibile verificare il numero di pagine del PDF')
    match = re.search(r'^Pages:\s+(\d+)', result.stdout, re.M)
    require(match is not None, 'Numero di pagine non ricavabile da pdfinfo')
    count = int(match.group(1))
    canonical = pages.get('canonical_pages')
    require(isinstance(canonical, list) and len(canonical) == count, 'Pagine canoniche incomplete o eccedenti')
    require([p.get('page') for p in canonical if isinstance(p, dict)] == list(range(1, count + 1)), 'Pagine canoniche duplicate o fuori ordine')
    for page in canonical:
        text(page.get('text'), f'Pagina {page["page"]}')
        require(page.get('visually_checked') is True, f'Pagina {page["page"]}: confronto visivo non registrato')
    omissions = pages.get('excluded_service_elements', [])
    require(isinstance(omissions, list), 'excluded_service_elements deve essere una lista')
    for omission in omissions:
        require(isinstance(omission, dict) and omission.get('page') in range(1, count + 1), 'Esclusione senza pagina valida')
        text(omission.get('text'), 'Testo escluso')
        text(omission.get('reason'), 'Motivazione esclusione')
    sections = manifest.get('sections')
    require(isinstance(sections, list) and sections, 'Manifest privo di sezioni')
    ids, page_texts, sequence, reuse_ids = [], {p: [] for p in range(1, count + 1)}, [], []
    for s in sections:
        require(isinstance(s, dict), 'Sezione non valida')
        sid = text(s.get('id'), 'ID sezione')
        require(sid not in ids, f'ID duplicato: {sid}')
        ids.append(sid)
        source = text(s.get('source_text'), f'{sid}.source_text')
        speech = text(s.get('speech_text'), f'{sid}.speech_text')
        action = text(s.get('action'), f'{sid}.action')
        require(action.startswith(('generate', 'reuse')), f'{sid}: action sconosciuta')
        units = s.get('source_units')
        if units is None:
            pp = s.get('pdf_pages')
            require(isinstance(pp, list) and len(pp) == 1, f'{sid}: per piu pagine specificare source_units')
            units = [{'page': pp[0], 'text': source}]
        require(isinstance(units, list) and units, f'{sid}: source_units mancanti')
        parts = []
        for u in units:
            require(isinstance(u, dict), f'{sid}: unita fonte non valida')
            pp = u.get('page')
            require(type(pp) is int and pp in page_texts, f'{sid}: pagina non presente nel PDF')
            part = text(u.get('text'), f'{sid}: testo unita')
            sequence.append(pp)
            page_texts[pp].append(part)
            parts.append(part)
        same_text(source, '\n'.join(parts), f'{sid}: source_text rispetto alle unita')
        if action.startswith('reuse'):
            evidence = s.get('reuse_evidence')
            require(isinstance(evidence, dict), f'{sid}: riuso senza evidenza')
            require(evidence.get('checked_against_current_pdf') is True, f'{sid}: stem non verificato sulla fonte attuale')
            same_text(source, text(evidence.get('source_text'), f'{sid}: vecchia fonte'), f'{sid}: fonte dello stem riusato')
            same_text(speech, text(evidence.get('speech_text'), f'{sid}: vecchio copione'), f'{sid}: copione dello stem riusato')
            audio = resolve(evidence.get('audio_path'), manifest_file.parent)
            require(sha256(audio) == evidence.get('audio_sha256'), f'{sid}: hash dello stem cambiato')
            reuse_ids.append(sid)
    require(sequence == sorted(sequence), 'Ordine delle sezioni diverso dall ordine delle pagine')
    coverage = []
    for page in canonical:
        n = page['page']
        require(page_texts[n], f'Pagina {n} omessa')
        same_text(page['text'], '\n'.join(page_texts[n]), f'Copertura pagina {n}')
        coverage.append({'page': n, 'exact_source_coverage': True})
    report = {
        'source_coverage_pass': True,
        'pdf_sha256': source_hash,
        'manifest_sha256': sha256(manifest_file),
        'pdf_pages': count,
        'section_ids': ids,
        'reused_sections_checked': reuse_ids,
        'coverage': coverage,
        'final_review_record_pass': False,
        'ready_for_delivery': False,
        'scope': 'Solo copertura testuale: nessun ascolto automatico o certificazione semantica.',
    }
    require((mp4_file is None) == (review_file is None), 'Specificare insieme --mp4 e --review')
    if review_file is not None:
        review = read_json(review_file)
        require(review.get('pdf_sha256') == source_hash, 'Verbale riferito a un altro PDF')
        require(review.get('manifest_sha256') == report['manifest_sha256'], 'Manifest cambiato dopo la revisione')
        mp4_hash = sha256(mp4_file)
        require(review.get('mp4_sha256') == mp4_hash, 'MP4 cambiato dopo la revisione')
        reviewed = review.get('sections')
        require(isinstance(reviewed, dict) and set(reviewed) == set(ids), 'Revisione AAC non registrata per tutte le sezioni correnti')
        for sid in ids:
            checks = reviewed[sid]
            require(isinstance(checks, dict), f'{sid}: verbale non valido')
            for flag in ['script_vs_pdf_checked', 'aac_transcript_compared', 'aac_listened']:
                require(checks.get(flag) is True, f'{sid}: controllo mancante: {flag}')
            require(checks.get('unresolved_differences') == [], f'{sid}: differenze mancanti o non risolte')
        checks = review.get('checks', {})
        require(isinstance(checks, dict), 'Controlli finali non validi')
        for flag in ['joins_listened', 'cover_start_mid_end_checked', 'final_sentence_checked', 'no_music_checked', 'speed_and_voices_checked', 'full_decode_passed', 'aac_peaks_measured']:
            require(checks.get(flag) is True, f'Controllo finale non completato: {flag}')
        text(review.get('last_sentence_heard'), 'Ultima frase realmente ascoltata')
        require(review.get('unresolved_issues') == [], 'Questioni finali mancanti o non risolte')
        require(review.get('technical_pass') is True, 'Verifica tecnica non superata')
        report.update(final_review_record_pass=True, ready_for_delivery=True, mp4_sha256=mp4_hash,
                      scope='Copertura e completezza/hash del verbale controllati; ascolto e revisione semantica restano responsabilita del revisore.')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pages', required=True, type=Path)
    parser.add_argument('--manifest', required=True, type=Path)
    parser.add_argument('--mp4', type=Path)
    parser.add_argument('--review', type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    try:
        report = audit(args.pages, args.manifest, args.mp4, args.review)
        status = 0
    except (AuditError, OSError, KeyError, TypeError, ValueError, subprocess.SubprocessError) as exc:
        report = {'source_coverage_pass': False, 'final_review_record_pass': False, 'ready_for_delivery': False, 'error': str(exc)}
        status = 1
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k not in ['coverage', 'section_ids']}, ensure_ascii=False, indent=2))
    return status


if __name__ == '__main__':
    sys.exit(main())

