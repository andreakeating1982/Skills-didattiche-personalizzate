#!/usr/bin/env python3
"""Verifica gli asset delle mappe finali e segnala riusi da valutare editorialmente.

Non legge una rete e non giudica significato, somiglianza grafica o stile clay.
I duplicati sono avvisi, non errori, salvo --require-distinct su richiesta esplicita.
"""
from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote, unquote_to_bytes, urlsplit

from bs4 import BeautifulSoup


def asset_bytes(src: str, base: Path):
    """Ritorna (bytes, descrizione, avviso) senza effettuare richieste di rete."""
    if src.startswith('data:'):
        try:
            header, body = src.split(',', 1)
            raw = base64.b64decode(body, validate=True) if ';base64' in header.lower() else unquote_to_bytes(body)
            if not raw:
                raise ValueError('contenuto vuoto')
            return raw, 'data-uri', None
        except (ValueError, binascii.Error):
            return None, 'data-uri', 'data_uri_non_valida'
    parts = urlsplit(src)
    if parts.scheme in ('http', 'https'):
        return None, src, 'immagine_remota_non_scaricata'
    if parts.scheme and parts.scheme != 'file':
        return None, src, 'schema_non_supportato'
    if parts.scheme == 'file' and parts.netloc not in ('', 'localhost'):
        return None, src, 'file_host_non_supportato'
    path = Path(unquote(parts.path))
    if not path.is_absolute():
        path = base / path
    path = path.resolve()
    if not path.is_file():
        return None, str(path), 'file_immagine_mancante'
    try:
        return path.read_bytes(), str(path), None
    except OSError:
        return None, str(path), 'file_immagine_non_leggibile'


def check(html, map_id=None, require_distinct=False):
    path = Path(html).resolve()
    soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
    if map_id:
        elem = soup.find(id=map_id)
        maps = [elem] if elem is not None and 'lf-simple-map' in elem.get('class', []) else []
    else:
        maps = soup.select('.lf-simple-map')
    errors, warnings, records = [], [], []
    if not maps:
        errors.append({'issue': 'mappa_finale_non_trovata', 'map_id': map_id})
    for imap, mapping in enumerate(maps, 1):
        mid = mapping.get('id') or f'map-{imap}'
        cards = mapping.select('.lf-map-card')
        if not cards:
            errors.append({'issue': 'mappa_senza_nodi', 'map_id': mid})
        for index, card in enumerate(cards, 1):
            cid = card.get('id') or f'{mid}-node-{index}'
            title = card.find(['h3', 'h4', 'h5'])
            title = title.get_text(' ', strip=True) if title else ''
            imgs = card.select('img')
            if len(imgs) != 1:
                errors.append({'issue': 'numero_immagini_nodo_non_valido', 'id': cid, 'count': len(imgs)})
                continue
            img = imgs[0]
            src, alt = img.get('src', '').strip(), img.get('alt', '').strip()
            if not alt:
                errors.append({'issue': 'alt_mancante', 'id': cid})
            if not src:
                errors.append({'issue': 'src_mancante', 'id': cid})
                continue
            raw, location, status = asset_bytes(src, path.parent)
            row = {'map_id': mid, 'id': cid, 'titolo': title, 'src': src, 'alt': alt,
                   'sha256': hashlib.sha256(raw).hexdigest() if raw is not None else None}
            records.append(row)
            if status == 'immagine_remota_non_scaricata':
                warnings.append({'issue': status, 'id': cid, 'src': src})
            elif status:
                errors.append({'issue': status, 'id': cid, 'src': src})
    by_hash = defaultdict(list)
    for row in records:
        if row['sha256']:
            by_hash[(row['map_id'], row['sha256'])].append(row)
    duplicates = []
    for (mid, digest), rows in sorted(by_hash.items()):
        if len(rows) <= 1:
            continue
        group = {'map_id': mid, 'sha256': digest, 'nodes': [r['id'] for r in rows],
                 'titles': [r['titolo'] for r in rows], 'sources': [r['src'] for r in rows]}
        duplicates.append(group)
        item = {'issue': 'immagine_ripetuta_valutare_pertinenza', **group}
        (errors if require_distinct else warnings).append(item)
    if require_distinct and any(x['issue'] == 'immagine_remota_non_scaricata' for x in warnings):
        errors.append({'issue': 'unicita_non_verificabile_immagini_remote'})
    return {
        'passed': not errors,
        'maps': len(maps),
        'nodes_with_images': len(records),
        'local_or_data_images_verified': sum(r['sha256'] is not None for r in records),
        'unique_local_or_data_images': len({r['sha256'] for r in records if r['sha256']}),
        'duplicates': duplicates,
        'nodes': records,
        'warnings': warnings,
        'errors': errors,
        'limits': ('I file uguali possono essere appropriati per lo stesso concetto o due lingue; '
                   'file diversi possono mostrare la stessa scena. L’hash non valuta pertinenza, '
                   'stile clay, somiglianza grafica, licenza o leggibilità. Controllo visivo necessario.'),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('html', help='HTML da verificare')
    parser.add_argument('--map-id', help='Limita al singolo id della mappa finale')
    parser.add_argument('--require-distinct', action='store_true',
                        help='Tratta i duplicati come errore solo se la richiesta impone tutte immagini distinte')
    parser.add_argument('--report', help='Salva il rapporto JSON')
    args = parser.parse_args()
    result = check(args.html, args.map_id, args.require_distinct)
    text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.report:
        Path(args.report).write_text(text, encoding='utf-8')
    print(text, end='')
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())

