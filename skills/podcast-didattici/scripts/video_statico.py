#!/usr/bin/env python3
"""MP4 leggero da audio integrale e copertina esistenti; nessuna generazione AI."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import wave


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--audio', type=Path, required=True)
    parser.add_argument('--cover', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--title', default='PODCAST INTEGRALE')
    parser.add_argument('--audio-bitrate', default='128k')
    parser.add_argument('--max-mb', type=float, default=100.0)
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    for binary in ('ffmpeg', 'ffprobe'):
        if not shutil.which(binary):
            parser.error(f'Manca {binary}.')
    for path in (args.audio, args.cover):
        if not path.is_file():
            parser.error(f'File mancante: {path}')
        if path.resolve() == args.out.resolve():
            parser.error('Non sovrascrivere le risorse sorgenti.')
    if args.out.suffix.lower() != '.mp4':
        parser.error('Usare un output .mp4.')
    if args.out.exists() and not args.overwrite:
        parser.error('Output gia presente: scegliere un altro nome o --overwrite.')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    work = args.out.parent / (args.out.stem + '_lavoro')
    work.mkdir(exist_ok=True)
    log = work / 'montaggio.log'
    log.write_text('Audio integrale e immagine fissa; nessun taglio o cambio di velocita.\n')

    def run(command):
        command = list(map(str, command))
        result = subprocess.run(command, capture_output=True, text=True)
        with log.open('a') as stream:
            stream.write('\nCOMMAND: ' + ' '.join(command) + '\n' + result.stderr + '\n')
        if result.returncode:
            raise RuntimeError(result.stderr[-3000:])
        return result.stdout

    def probe(path):
        return json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', path]))

    report = {'file': str(args.out), 'technical_pass': False, 'visual_and_ending_check_required': True}
    report_path = args.out.with_suffix('.qa.json')
    try:
        decoded = work / 'audio_integrale.wav'
        run(['ffmpeg', '-hide_banner', '-nostdin', '-y', '-threads', '2', '-i', args.audio,
             '-map', '0:a:0', '-vn', '-ar', '48000', '-ac', '2', '-c:a', 'pcm_s16le', decoded])
        with wave.open(str(decoded), 'rb') as stream:
            duration = stream.getnframes() / stream.getframerate()
        if duration <= 1:
            raise ValueError('Audio troppo breve o non valido.')
        segment = work / 'copertina_segmento.mp4'
        run(['ffmpeg', '-hide_banner', '-nostdin', '-y', '-loop', '1', '-framerate', '2', '-i', args.cover,
             '-t', f'{min(120, duration):.9f}', '-vf',
             'scale=1280:720:force_original_aspect_ratio=decrease:flags=lanczos,'
             'pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=0x23392b,setsar=1,format=yuv420p',
             '-c:v', 'libx264', '-threads', '2', '-preset', 'medium', '-tune', 'stillimage',
             '-crf', '24', '-r', '2', '-g', '240', '-keyint_min', '240', '-sc_threshold', '0',
             '-bf', '0', '-an', '-map_metadata', '-1', segment])
        run(['ffmpeg', '-hide_banner', '-nostdin', '-y', '-stream_loop', '-1', '-i', segment,
             '-i', decoded, '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy', '-c:a', 'aac',
             '-b:a', args.audio_bitrate, '-ac', '2', '-ar', '48000', '-threads', '2',
             '-t', f'{duration:.9f}', '-shortest', '-map_metadata', '-1',
             '-metadata', f'title={args.title}', '-movflags', '+faststart', args.out])
        run(['ffmpeg', '-hide_banner', '-nostdin', '-v', 'error', '-xerror', '-i', args.out, '-f', 'null', '-'])
        info = probe(args.out)
        video = next(s for s in info['streams'] if s['codec_type'] == 'video')
        audio = next(s for s in info['streams'] if s['codec_type'] == 'audio')
        audio_duration = float(audio['duration'])
        duration_ok = abs(audio_duration - duration) < 0.15
        size_ok = args.out.stat().st_size < args.max_mb * 1000000
        video_ok = video['codec_name'] == 'h264' and video['width'] == 1280 and video['height'] == 720
        for label, timestamp in [('inizio', min(0.5, duration/4)), ('meta', duration/2), ('fine', max(0, duration-0.6))]:
            run(['ffmpeg', '-hide_banner', '-nostdin', '-y', '-ss', f'{timestamp:.6f}', '-i', args.out,
                 '-frames:v', '1', '-update', '1', work / f'fotogramma_{label}.jpg'])
        run(['ffmpeg', '-hide_banner', '-nostdin', '-y', '-ss', f'{max(0,duration-30):.6f}', '-i', args.out,
             '-map', '0:a:0', '-vn', '-c:a', 'libmp3lame', '-b:a', '128k', work / 'finale_video.mp3'])
        report.update({'technical_pass': duration_ok and size_ok and video_ok,
                       'audio_source': str(args.audio), 'cover_source': str(args.cover),
                       'audio_source_sha256': hashlib.sha256(args.audio.read_bytes()).hexdigest(),
                       'source_duration_seconds': duration, 'output_audio_duration_seconds': audio_duration,
                       'output_video_duration_seconds': float(info['format']['duration']),
                       'size_bytes': args.out.stat().st_size, 'size_limit_MB': args.max_mb,
                       'under_size_limit': size_ok, 'resolution': '1280x720', 'fps': '2',
                       'video_codec': video['codec_name'], 'audio_codec': audio['codec_name'],
                       'decode_test': 'PASS', 'audio_cuts': [], 'speed_change_applied': False,
                       'work_directory': str(work)})
    except Exception as error:
        report['error'] = str(error)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        raise
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['technical_pass'] else 2


if __name__ == '__main__':
    sys.exit(main())

