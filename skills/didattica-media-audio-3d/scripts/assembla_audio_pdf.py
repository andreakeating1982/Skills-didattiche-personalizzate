#!/usr/bin/env python3
"""Montare clip TTS gia prodotte: nessuna generazione o rigenerazione di voci.
Dipendenze: ffmpeg/ffprobe, requests (solo download). --offline non usa la rete.
"""
import argparse, hashlib, json, re, subprocess, wave
from pathlib import Path


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def run(args):
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(' '.join(map(str, args))+'\n'+result.stderr[-2000:])
    return result


def probe(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(path)]).stdout)


def measure(path):
    result = run(['ffmpeg','-hide_banner','-nostdin','-i',str(path),'-af',
                  'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'])
    return json.loads(re.findall(r'\{[^{}]+\}', result.stderr, re.S)[-1])


def stamp(seconds):
    n=round(seconds)
    return f'{n//60:02}:{n%60:02}'


def quote(path):
    return "file '"+str(path).replace("'", "'\\''")+"'"


def resolve(base, value):
    path=Path(value)
    return path.resolve() if path.is_absolute() else (base/path).resolve()


def validate(manifest, base):
    if not manifest.get('title') or not manifest.get('parts'):
        raise ValueError('Titolo e parti obbligatori')
    if float(manifest.get('speed',0)) != 1.12:
        raise ValueError('Lo standard approvato richiede speed=1.12')
    source=resolve(base, manifest['source_pdf'])
    if not source.is_file() or sha(source) != manifest['source_sha256']:
        raise ValueError('Fonte mancante o SHA-256 diverso dal manifest: blocco antiversione errata')
    names=set(); closed=set(); current=None; gender=None
    for part in manifest['parts']:
        if not re.fullmatch(r'[A-Za-z0-9_-]+',part['name']) or part['name'] in names:
            raise ValueError('Nome clip non valido o duplicato')
        names.add(part['name'])
        if not 0 < len(part['text'].strip()) < 5000:
            raise ValueError('Testo vuoto o >=5000 caratteri')
        if float(part.get('speed',manifest['speed'])) != manifest['speed']:
            raise ValueError('Velocita incoerente')
        if part['gender'] not in ('female','male') or not part.get('title'):
            raise ValueError('Voce o titolo mancanti')
        pages=part['pages']
        if len(pages)!=2 or not 1 <= pages[0] <= pages[1] <= manifest['pages']:
            raise ValueError('Intervallo pagine non valido')
        chapter=part['chapter']
        if chapter == current:
            if part['gender'] != gender: raise ValueError('Cambio voce dentro lo stesso capitolo')
        else:
            if chapter in closed: raise ValueError('Capitolo fuori ordine o non contiguo')
            if current is not None:
                closed.add(current)
                if part['gender'] == gender: raise ValueError('Capitoli consecutivi senza alternanza delle voci')
            current,gender=chapter,part['gender']
    return source


def assemble(manifest_path, output, offline=False, validate_only=False):
    manifest_path=Path(manifest_path).resolve(); base=manifest_path.parent
    m=json.loads(manifest_path.read_text(encoding='utf-8')); source=validate(m,base)
    if validate_only:
        print(f"MANIFEST VALIDO: {len(m['parts'])} parti, fonte {source.name}"); return
    output=Path(output).resolve()
    clips=output/'clip'; cache=output/'cache'; qa=output/'verifica'; delivery=output/'consegna'
    for directory in (clips,cache,qa,delivery): directory.mkdir(parents=True,exist_ok=True)
    parts=m['parts']; concat=[]; chapters=[]; offset=0
    silence=cache/'pausa.wav'
    run(['ffmpeg','-v','error','-nostdin','-y','-f','lavfi','-i','anullsrc=r=44100:cl=mono',
         '-t','0.3','-c:a','pcm_s16le',str(silence)])
    previous=None
    for index,p in enumerate(parts):
        src=resolve(base,p['clip_path']) if p.get('clip_path') else clips/(p['name']+'.mp3')
        if not src.is_file():
            if offline or not p.get('source_url') or p.get('clip_path'):
                raise FileNotFoundError(f'Clip non disponibile: {src}; non generare una nuova voce automaticamente')
            if not p['source_url'].startswith('https://media.easy-peasy.ai/'):
                raise ValueError('URL non appartenente ai risultati media; scaricare separatamente e usare clip_path')
            import requests
            res=requests.get(p['source_url'],timeout=150); res.raise_for_status(); src.write_bytes(res.content)
        p['clip_sha256']=sha(src)
        if p.get('expected_clip_sha256') and p['expected_clip_sha256']!=p['clip_sha256']:
            raise ValueError('Clip diversa da quella registrata')
        p['raw_duration']=float(probe(src)['format']['duration'])
        signature=hashlib.sha256((p['clip_sha256']+'|r128:-16:-1.5:11|44100|mono|pcm_s16le|v1').encode()).hexdigest()[:18]
        wav=cache/(p['name']+'_'+signature+'.wav'); stats=wav.with_suffix('.json')
        if not wav.exists() or not stats.exists():
            loud=measure(src)
            filt=('loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={input_i}:measured_TP={input_tp}:'
                  'measured_LRA={input_lra}:measured_thresh={input_thresh}:offset={target_offset}:linear=true').format(**loud)
            run(['ffmpeg','-v','error','-nostdin','-y','-i',str(src),'-af',filt,
                 '-ar','44100','-ac','1','-c:a','pcm_s16le',str(wav)])
            save(stats,loud)
        with wave.open(str(wav),'rb') as audio:
            duration=audio.getnframes()/audio.getframerate()
        if duration<=0: raise ValueError('Clip vuota')
        p.update(seconds=duration,start_seconds=offset,normalized_path=str(wav))
        if previous != p['chapter']:
            chapters.append(dict(title=p['title'],start=offset,pdf_page=p['pages'][0],gender=p['gender']))
        previous=p['chapter'];concat.append(quote(wav));offset+=duration
        if index<len(parts)-1:concat.append(quote(silence));offset+=0.3
        print(p['name'],stamp(duration),flush=True)
    concat_path=cache/'concat.txt';concat_path.write_text('\n'.join(concat)+'\n')
    slug=re.sub(r'[^A-Z0-9_]+','_',m.get('slug',m['title']).upper()).strip('_')
    final=delivery/(slug+'_AUDIO_INTEGRALE_DUE_VOCI_1_12x.mp3')
    meta=[';FFMETADATA1','title='+m['title'].replace('\n',' ').replace('=','\\=')]
    for i,c in enumerate(chapters):
        end=chapters[i+1]['start'] if i+1<len(chapters) else offset
        meta+=['[CHAPTER]','TIMEBASE=1/1000',f"START={round(c['start']*1000)}",f"END={round(end*1000)}",
               'title='+c['title'].replace('\n',' ').replace('=','\\=')]
    metadata=cache/'capitoli.ffmeta';metadata.write_text('\n'.join(meta)+'\n')
    run(['ffmpeg','-v','error','-nostdin','-y','-f','concat','-safe','0','-i',str(concat_path),'-i',str(metadata),
         '-map_metadata','1','-map_chapters','1','-ar','44100','-ac','1','-c:a','libmp3lame','-b:a','128k',
         '-id3v2_version','3',str(final)])
    final_seconds=float(probe(final)['format']['duration'])
    if abs(final_seconds-offset)>0.2:raise ValueError('Durata finale non corrisponde alle clip e alle pause')
    run(['ffmpeg','-v','error','-nostdin','-i',str(final),'-f','null','-'])
    loud=measure(final); samples=[];schedule=[]; sample_time=0
    for p in parts:
        for label,start,length in [('INIZIO',0,min(8,p['seconds'])),('FINE',max(0,p['seconds']-10),min(10,p['seconds']))]:
            excerpt=qa/(p['name']+'_'+label+'.wav')
            run(['ffmpeg','-v','error','-nostdin','-y','-ss',str(start),'-i',p['normalized_path'],
                 '-t',str(length),'-c:a','pcm_s16le',str(excerpt)])
            samples += [quote(excerpt),quote(silence)]
            schedule.append(dict(time=stamp(sample_time),part=p['name'],sample=label,
                                 expected=p['text'][:220] if label=='INIZIO' else p['text'][-280:]))
            sample_time+=length+0.3
    qa_list=qa/'concat_campioni.txt';qa_list.write_text('\n'.join(samples)+'\n')
    run(['ffmpeg','-v','error','-nostdin','-y','-f','concat','-safe','0','-i',str(qa_list),
         '-c:a','libmp3lame','-b:a','128k',str(qa/'QA_CAMPIONI.mp3')])
    save(qa/'QA_CAMPIONI.json',schedule)
    md=['# '+m['title'],'','## LETTURA INTEGRALE A DUE VOCI — 1,12×','',
        '**Durata:** '+stamp(final_seconds)+'. **Fonte:** '+source.name+'.',
        '**Voci:** italiana femminile e maschile alternate. Nessuna musica e nessun riassunto.',
        'Il copione e le esclusioni devono essere verificati contro il PDF prima della consegna.','',
        '## INDICE TEMPORALE','','| INIZIO | CAPITOLO | PAGINA PDF |','|---|---|---|']
    md += [f"| {stamp(c['start'])} | {c['title'].replace('|','/')} | {c['pdf_page']} |" for c in chapters]
    md+=['','## TESTO DELLA LETTURA','']
    for p in parts:md+=['### '+p['title'].upper(),'',p['text'],'']
    index_file=delivery/(slug+'_TESTO_AUDIO_E_INDICE_TEMPORALE.md');index_file.write_text('\n'.join(md),encoding='utf-8')
    report=dict(technical_passed=True,audition_pending=True,source_coverage_review_pending=True,
                source_pdf=str(source),source_sha256=m['source_sha256'],speed=1.12,parts_count=len(parts),
                duration_seconds=final_seconds,duration=stamp(final_seconds),duration_difference_seconds=final_seconds-offset,
                measured_final_loudness=loud,decode_errors=False,final_sha256=sha(final),
                limits='Verifica tecnica, non certificazione della fedelta del parlato: completare copertura testo e ascolto campioni.')
    save(qa/'VERIFICA_AUDIO.json',report); save(output/'manifest_con_durate.json',m)
    save(output/'consegna.json',dict(audio=str(final),index=str(index_file),duration=stamp(final_seconds)))
    print('TECNICA SUPERATA; ASCOLTO E COPERTURA DA COMPLETARE:',stamp(final_seconds),final)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest',type=Path)
    parser.add_argument('--out',type=Path,default=Path('montaggio_audio'))
    parser.add_argument('--offline',action='store_true')
    parser.add_argument('--validate-only',action='store_true')
    args=parser.parse_args()
    assemble(args.manifest,args.out,args.offline,args.validate_only)

