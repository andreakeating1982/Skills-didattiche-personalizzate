#!/usr/bin/env python3
"""Validate a Latino Facile export against its committed repository.
Usage: python3 verify_export.py REPO ZIP [REPORT_JSON]
No network calls, no keys or databases are accessed.
"""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import zipfile


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])


def validate(repo, archive):
    if git(repo, 'status', '--porcelain', '--untracked-files=normal').strip():
        raise ValueError('Repository non pulita: non confrontare un export con file non committati.')
    commit = git(repo, 'rev-parse', 'HEAD').decode().strip()
    tracked = set(git(repo, 'ls-tree', '-r', '--name-only', 'HEAD').decode().splitlines())
    prefix = repo.name + '/'
    required = {
        'README.md', 'AGENTS.md', 'REBUILD.md', 'ADATTARE.md', 'RENDER.md',
        'ACCESSIBILITA.md', 'OCR-FOTO.md', 'SCROLLING-MOBILE.md', 'manifest.json',
        'RILASCIO-MOBILE-2026-10-28.md', '.env.example', 'render.yaml',
        '.github/workflows/ci.yml', 'Dockerfile', 'package.json', 'pnpm-lock.yaml',
        'patches/wouter@3.7.1.patch', 'client/src/components/CropDialog.tsx',
        'client/src/hooks/useCropDialogViewport.ts', 'client/src/lib/heightSync.ts',
        'client/src/lib/cropBox.ts', 'client/src/index.css', 'tests/crop-mobile.e2e.mjs',
        'tests/crop-drag.e2e.mjs', 'tests/legend-colors.e2e.ts',
        'PHOTO-CROP-CLONABILE.md', 'docs/photo-crop-mobile.png',
        'server/analyzer/moodColors.test.ts',
        'client/public/fonts/OpenDyslexic-Regular.ttf',
        'client/public/fonts/OpenDyslexic-Bold.ttf',
        'client/public/tessdata/lat.traineddata.gz',
        'cornice-dinamica/README.md', 'cornice-dinamica/embed-latino-facile-dedicata.html',
    }
    secret_pattern = re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\bsk-[A-Za-z0-9]{32,}\b|\bAIza[A-Za-z0-9_-]{35}\b')
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None:
            raise ValueError('Controllo CRC ZIP fallito.')
        if z.comment.decode().strip() != commit:
            raise ValueError('Il commit nel commento ZIP non corrisponde a HEAD.')
        archived = set()
        directories = 0
        total_bytes = 0
        font_files = 0
        pdf_files = 0
        for entry in z.infolist():
            path = PurePosixPath(entry.filename)
            if path.is_absolute() or '..' in path.parts or not entry.filename.startswith(prefix):
                raise ValueError('Percorso ZIP non sicuro o prefisso inatteso.')
            if entry.is_dir():
                directories += 1
                continue
            relative = entry.filename[len(prefix):]
            if relative in archived:
                raise ValueError('Percorso duplicato nell’archivio: ' + relative)
            parts = PurePosixPath(relative).parts
            if set(parts) & {'.git', 'node_modules', 'dist', '.cache', '__pycache__'}:
                raise ValueError('Cartella temporanea/non esportabile: ' + relative)
            name = parts[-1]
            if (name.startswith('.env') and name != '.env.example') or name.endswith(('.log', '.sqlite', '.sqlite3', '.db', '.pem', '.key')):
                raise ValueError('File privato o runtime nell’archivio: ' + relative)
            body = z.read(entry)
            expected = git(repo, 'show', 'HEAD:' + relative)
            if hashlib.sha256(body).digest() != hashlib.sha256(expected).digest():
                raise ValueError('Contenuto diverso dalla repository: ' + relative)
            if secret_pattern.search(body):
                raise ValueError('Possibile credenziale incorporata in: ' + relative)
            total_bytes += len(body)
            font_files += name.endswith(('.ttf', '.otf', '.woff', '.woff2'))
            pdf_files += name.endswith('.pdf')
            archived.add(relative)
        if tracked != archived:
            raise ValueError('Insieme file ZIP diverso dal commit: ' + repr(sorted(tracked ^ archived)))
        if required - archived:
            raise ValueError('File indispensabili mancanti: ' + repr(sorted(required - archived)))
        manifest = json.loads(z.read(prefix + 'manifest.json'))
        package = json.loads(z.read(prefix + 'package.json'))
        if manifest.get('scripts') != package.get('scripts'):
            raise ValueError('Script del manifest non allineati a package.json.')
        deployment = manifest.get('release', {}).get('deploymentId')
        if not isinstance(deployment, int) or deployment < 8731:
            raise ValueError('Manifest non aggiornato al rilascio crop diretto 8731 o successivo.')
        crop = z.read(prefix + 'client/src/components/CropDialog.tsx').decode()
        hook = z.read(prefix + 'client/src/hooks/useCropDialogViewport.ts').decode()
        sync = z.read(prefix + 'client/src/lib/heightSync.ts').decode()
        assert 'modal={true}' in crop and 'data-crop-scroll' in crop and 'data-crop-footer' in crop
        assert 'data-crop-controls' in crop and 'data-crop-selection' in crop
        assert 'Ritaglia la foto' in crop and '<Move' not in crop
        assert 'setPointerCapture' in crop and 'pointerId' in crop
        css = z.read(prefix + 'client/src/index.css').decode()
        assert re.search(r'\.lf-crop-move\s*\{[^}]*pointer-events:\s*auto;[^}]*touch-action:\s*none;', css)
        assert 'OTHER_MOODS_COLOR = "#795548"' in z.read(prefix + 'shared/types.ts').decode()
        assert 'IntersectionObserver' in hook and 'intersectionRect' in hook
        assert 'data-lf-crop-open' in sync and 'lf:crop-closed' in sync
        guide = z.read(prefix + 'PHOTO-CROP-CLONABILE.md').decode()
        embedded = dict(re.findall(r'^### FILE: ([^\n]+)\n\n````[^\n]*\n(.*?)^````\n', guide, re.M | re.S))
        hash_block = guide.split('## HASH SHA-256 DEI FILE TESTUALI', 1)[1]
        crop_manifest = json.loads(re.search(r'```json\n(.*?)\n```', hash_block, re.S).group(1))
        if crop_manifest['production_baseline_deployment'] != deployment:
            raise ValueError('Foglio cropper e manifest app hanno deploy diversi.')
        if set(embedded) != set(crop_manifest['file_sha256']):
            raise ValueError('Sorgenti nel foglio clonabile incomplete.')
        for name, body in embedded.items():
            if hashlib.sha256(body.encode()).hexdigest() != crop_manifest['file_sha256'][name]:
                raise ValueError('SHA-256 del sorgente incorporato non valido: ' + name)
            if name in archived and z.read(prefix + name) != body.encode():
                raise ValueError('Foglio clonabile non allineato ai sorgenti: ' + name)
        baseline = manifest['release']['codeCommit']
        changed_runtime = git(repo, 'diff', '--name-only', baseline, 'HEAD', '--', 'client', 'server', 'shared', 'tests', 'package.json', 'pnpm-lock.yaml', 'patches', 'Dockerfile').decode().splitlines()
        if changed_runtime:
            raise ValueError('Il runtime differisce dal codice pubblicato: ' + repr(changed_runtime))
    return {
        'archive': archive.name,
        'archive_commit': commit,
        'production_deployment_id': deployment,
        'production_code_commit': manifest['release']['codeCommit'],
        'runtime_identical_to_production_commit': True,
        'portable_crop_guide_embedded_sources_verified': len(embedded),
        'portable_crop_guide_matches_repository': True,
        'zip_crc_ok': True,
        'all_tracked_files_present_and_sha256_identical': True,
        'required_files_present': len(required),
        'files': len(archived),
        'directory_entries': directories,
        'compressed_bytes': archive.stat().st_size,
        'uncompressed_file_bytes': total_bytes,
        'font_files': font_files,
        'pdf_files': pdf_files,
        'no_private_or_runtime_files': True,
        'credential_pattern_scan': 'No matches; not a comprehensive security audit',
        'sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
    }


if __name__ == '__main__':
    if len(sys.argv) not in (3, 4):
        raise SystemExit('Uso: verify_export.py REPO ZIP [REPORT_JSON]')
    result = validate(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())
    text = json.dumps(result, indent=2, ensure_ascii=False) + '\n'
    if len(sys.argv) == 4:
        Path(sys.argv[3]).write_text(text, encoding='utf-8')
    print(text, end='')

