#!/usr/bin/env python3
"""Confronto pixel di pagine dichiarate invariate, NON selezione automatica della base approvata.
Richiede l'hash atteso della baseline gia identificata. Non certifica PDF/UA o merito dei contenuti.
"""
import argparse, hashlib, json
from pathlib import Path
import pymupdf


def compare(baseline, revision, expected_sha, pages, output):
    baseline,revision=Path(baseline),Path(revision)
    actual=hashlib.sha256(baseline.read_bytes()).hexdigest()
    if actual != expected_sha:raise ValueError('SHA-256 della baseline diverso da quello atteso: interrompere')
    wanted=[]
    for token in pages.split(','):
        ends=list(map(int,token.strip().split('-')))
        wanted.extend(range(ends[0],ends[-1]+1))
    wanted=sorted(set(wanted));identical=[];changed=[]
    with pymupdf.open(baseline) as before,pymupdf.open(revision) as after:
        for number in wanted:
            if not 1<=number<=min(len(before),len(after)):raise ValueError('Pagina fuori intervallo')
            a,b=before[number-1].get_pixmap(alpha=False),after[number-1].get_pixmap(alpha=False)
            match=(a.width,a.height,a.n,a.samples)==(b.width,b.height,b.n,b.samples)
            (identical if match else changed).append(number)
        result=dict(baseline=str(baseline.resolve()),baseline_sha256=actual,revision=str(revision.resolve()),
                    revision_sha256=hashlib.sha256(revision.read_bytes()).hexdigest(),
                    baseline_pages=len(before),revision_pages=len(after),identical_pages=identical,changed_pages=changed,
                    passed=not changed,limits='Solo pagine selezionate, render stesso ambiente; scegliere e documentare prima la base corretta.')
    if output:Path(output).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2));return not changed


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('baseline',type=Path);p.add_argument('revision',type=Path)
    p.add_argument('--baseline-sha256',required=True)
    p.add_argument('--pages',required=True,help='Pagine invariate, esempio 2-32 oppure 2,4-6')
    p.add_argument('--report',type=Path)
    a=p.parse_args()
    raise SystemExit(0 if compare(a.baseline,a.revision,a.baseline_sha256,a.pages,a.report) else 1)

