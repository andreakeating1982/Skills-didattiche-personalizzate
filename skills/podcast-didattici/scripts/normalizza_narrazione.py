#!/usr/bin/env python3
"""Normalizza un'unica narrazione pulita, senza musica, tagli o cambi di velocità."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import wave


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--audio',required=True,type=Path)
    parser.add_argument('--out',required=True,type=Path)
    parser.add_argument('--lufs',type=float,default=-16.0)
    parser.add_argument('--true-peak',type=float,default=-2.5)
    parser.add_argument('--overwrite',action='store_true')
    args=parser.parse_args()
    for tool in ('ffmpeg','ffprobe'):
        if not shutil.which(tool):
            parser.error(f'Manca {tool}')
    if not args.audio.is_file():
        parser.error('Sorgente audio mancante')
    if args.out.suffix.lower()!='.wav':
        parser.error('Il master deve essere WAV; codificare poi l’AAC per il video')
    if args.audio.resolve()==args.out.resolve():
        parser.error('Non sovrascrivere la sorgente')
    if args.out.exists() and not args.overwrite:
        parser.error('Output già esistente: cambiare nome o usare --overwrite')
    args.out.parent.mkdir(parents=True,exist_ok=True)
    log=args.out.with_suffix('.normalizzazione.log')
    commands=[]

    def run(command):
        command=list(map(str,command))
        commands.append(command)
        result=subprocess.run(command,capture_output=True,text=True)
        with log.open('a',encoding='utf-8') as stream:
            stream.write('\nCOMMAND: '+' '.join(command)+'\n'+result.stderr)
        if result.returncode:
            raise RuntimeError(result.stderr[-3000:])
        return result

    def measurement(path):
        result=run(['ffmpeg','-hide_banner','-nostdin','-threads','2','-i',path,'-map','0:a:0','-vn',
                    '-af',f'loudnorm=I={args.lufs}:TP={args.true_peak}:LRA=11:print_format=json',
                    '-f','null','-'])
        candidates=re.findall(r'\{\s*"input_i".*?\}',result.stderr,re.S)
        if not candidates:
            raise RuntimeError('Misura loudness non disponibile')
        value=json.loads(candidates[-1])
        if not all(math.isfinite(float(value[k])) for k in ('input_i','input_tp','input_lra','input_thresh')):
            raise ValueError('Sorgente silenziosa o misura non finita')
        return value

    log.write_text('Solo parlato: una sorgente audio; nessuna musica, taglio o variazione di velocità.\n',encoding='utf-8')
    before=measurement(args.audio)
    filt=(f'loudnorm=I={args.lufs}:TP={args.true_peak}:LRA=11:'
          f'measured_I={before["input_i"]}:measured_TP={before["input_tp"]}:'
          f'measured_LRA={before["input_lra"]}:measured_thresh={before["input_thresh"]}:'
          f'offset={before["target_offset"]}:linear=true:print_format=json')
    run(['ffmpeg','-hide_banner','-nostdin','-y','-threads','2','-i',args.audio,'-map','0:a:0',
         '-vn','-af',filt,'-ar','48000','-ac','2','-c:a','pcm_s16le','-map_metadata','-1',args.out])
    after=measurement(args.out)
    probe=json.loads(run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',args.audio]).stdout)
    source_duration=float(probe['format']['duration'])
    with wave.open(str(args.out),'rb') as source:
        duration=source.getnframes()/source.getframerate()
        channels=source.getnchannels()
        rate=source.getframerate()
    run(['ffmpeg','-hide_banner','-nostdin','-v','error','-xerror','-i',args.out,'-f','null','-'])
    passed=(abs(duration-source_duration)<.15 and abs(float(after['input_i'])-args.lufs)<=1
            and float(after['input_tp'])<=-1 and rate==48000 and channels==2)
    report={'technical_pass':passed,'file':str(args.out),'audio_source':str(args.audio),
            'source_sha256':hashlib.sha256(args.audio.read_bytes()).hexdigest(),
            'output_sha256':hashlib.sha256(args.out.read_bytes()).hexdigest(),
            'single_audio_source':True,'music_inputs':[], 'background_music_added':False,
            'source_must_be_verified_clean_speech':True,'speed_change_applied':False,'audio_cuts':[],
            'source_duration_seconds':source_duration,'output_duration_seconds':duration,
            'sample_rate':rate,'channels':channels,'target_LUFS':args.lufs,
            'output_LUFS':float(after['input_i']),'output_true_peak_dBTP':float(after['input_tp']),
            'full_decode_test':'PASS','commands':commands}
    args.out.with_suffix('.qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='commands'},ensure_ascii=False,indent=2))
    return 0 if passed else 2


if __name__=='__main__':
    raise SystemExit(main())

