#!/usr/bin/env python3
"""Estrarre senza omissioni testo e coordinate; NON decide ordine di lettura o pronuncia."""
import argparse, hashlib, json
from pathlib import Path
import pymupdf


def extract(source, output):
    source, output = Path(source).resolve(), Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    pages, plain = [], []
    with pymupdf.open(source) as doc:
        for page in doc:
            blocks = [dict(id=f'p{page.number+1:03d}_b{i:03d}', bbox=list(b[:4]), text=b[4])
                      for i, b in enumerate(page.get_text('blocks', sort=True)) if b[6] == 0]
            pages.append(dict(page=page.number+1, width=page.rect.width, height=page.rect.height,
                              needs_visual_or_ocr_review=not any(b['text'].strip() for b in blocks), blocks=blocks))
            plain.append(f'--- PAGINA {page.number+1} ---\n'+ '\n'.join(b['text'] for b in blocks))
    data = dict(source_pdf=str(source), source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                pages=len(pages), extraction_only=True, editorial_review_pending=True, page_blocks=pages)
    (output/'fonte_blocchi.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    (output/'estratto_integrale.txt').write_text('\n\n'.join(plain), encoding='utf-8')
    print(json.dumps(dict(pages=len(pages), source_sha256=data['source_sha256'],
                         pages_without_text=[p['page'] for p in pages if p['needs_visual_or_ocr_review']],
                         output=str(output)), ensure_ascii=False, indent=2))
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    extract(args.pdf, args.out)

