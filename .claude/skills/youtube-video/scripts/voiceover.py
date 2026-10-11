#!/usr/bin/env python3
"""Kora Klicks voice-over builder (Egyptian Arabic).

Reads a storyboard whose scenes carry a `narration` line, produces one voice clip per
scene, re-times every scene to its clip, mixes one voice-over track (with optional
background music under it), and writes a timed storyboard ready for render.py.

Usage:
  python3 voiceover.py storyboard.json OUT_DIR --engine edge|elevenlabs|files
         [--voice ar-EG-ShakirNeural] [--rate +0%] [--recordings DIR]
         [--music music.mp3] [--music-volume 0.12] [--lexicon pronunciation.json]

Engines:
  edge        Microsoft neural voices (free, needs internet access to Microsoft).
              Egyptian voices: ar-EG-ShakirNeural (male), ar-EG-SalmaNeural (female).
              pip install edge-tts
  elevenlabs  ElevenLabs API. Needs env ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID
              (an Arabic voice; optional ELEVENLABS_MODEL, default eleven_multilingual_v2).
  offline     Free offline Arabic voice "Kareem" (Piper VITS via sherpa-onnx), runs anywhere, no API.
              pip install sherpa-onnx soundfile; download vits-piper-ar_JO-kareem-medium.tar.bz2 from
              github.com/k2-fsa/sherpa-onnx/releases/tag/tts-models and pass --model-dir. Accent is
              Levantine/MSA, not Egyptian. Write narration WITH tashkeel for good pronunciation.
  files       Human recordings: DIR/scene-01.mp3, scene-02.mp3 … (number = scene position,
              starting at 1). Scenes without a file stay silent (music only).

Then:  python3 render.py OUT_DIR/<slug>-timed.json OUT_DIR
"""
import argparse, asyncio, json, os, subprocess, sys, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAD = 0.35   # seconds of silence before the voice starts in each scene
TAIL = 0.65   # seconds after the voice ends before the next scene


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def apply_lexicon(text, lex):
    for written, spoken in sorted(lex.items(), key=lambda kv: -len(kv[0])):
        text = text.replace(written, spoken)
    return text


def tts_edge(text, path, voice, rate):
    import edge_tts
    async def go():
        await edge_tts.Communicate(text, voice, rate=rate).save(str(path))
    asyncio.run(go())


def tts_elevenlabs(text, path):
    key, voice = os.environ.get("ELEVENLABS_API_KEY"), os.environ.get("ELEVENLABS_VOICE_ID")
    if not key or not voice:
        sys.exit("Set ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID")
    body = json.dumps({"text": text, "model_id": os.environ.get("ELEVENLABS_MODEL", "eleven_multilingual_v2"),
                       "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.35}}).encode()
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_128",
                                 data=body, headers={"xi-api-key": key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        Path(path).write_bytes(r.read())


_OFFLINE = None
def tts_offline(text, path, model_dir, speed):
    global _OFFLINE
    import sherpa_onnx, soundfile as sf
    d = Path(model_dir)
    if _OFFLINE is None:
        onnx = next(d.glob("*.onnx"))
        _OFFLINE = sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
            vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=str(onnx), tokens=str(d / "tokens.txt"),
                                                       data_dir=str(d / "espeak-ng-data")), num_threads=4)))
    au = _OFFLINE.generate(text, sid=0, speed=speed)
    wav = Path(path).with_suffix(".wav")
    sf.write(str(wav), au.samples, au.sample_rate)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-af",
                    "highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=80", "-b:a", "192k", str(path)], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("storyboard"); ap.add_argument("out_dir")
    ap.add_argument("--engine", choices=["edge", "elevenlabs", "offline", "files"], required=True)
    ap.add_argument("--voice", default="ar-EG-ShakirNeural")
    ap.add_argument("--rate", default="+0%")
    ap.add_argument("--recordings")
    ap.add_argument("--model-dir", help="offline engine: folder of the sherpa-onnx Piper voice")
    ap.add_argument("--speed", type=float, default=0.95, help="offline engine speed")
    ap.add_argument("--music"); ap.add_argument("--music-volume", type=float, default=0.12)
    ap.add_argument("--lexicon", default=str(HERE.parent / "assets" / "pronunciation.json"))
    a = ap.parse_args()

    sb_path = Path(a.storyboard).resolve()
    sb = json.loads(sb_path.read_text(encoding="utf-8"))
    out = Path(a.out_dir).resolve(); out.mkdir(parents=True, exist_ok=True)
    clips_dir = out / "vo-clips"; clips_dir.mkdir(exist_ok=True)
    lex = json.loads(Path(a.lexicon).read_text(encoding="utf-8")) if a.lexicon and Path(a.lexicon).exists() else {}
    lex = {k: v for k, v in lex.items() if not k.startswith("_")}
    slug = sb.get("slug", "kora-klicks-video")

    t, placements, report = 0.0, [], []
    for i, s in enumerate(sb["scenes"], start=1):
        text = (s.get("narration") or "").strip()
        clip = None
        if a.engine == "files":
            rec = Path(a.recordings or ".").resolve() / f"scene-{i:02d}.mp3"
            if rec.exists():
                clip = rec
        elif text:
            clip = clips_dir / f"scene-{i:02d}.mp3"
            spoken = apply_lexicon(text, lex)
            if a.engine == "edge":
                tts_edge(spoken, clip, a.voice, a.rate)
            elif a.engine == "offline":
                tts_offline(s.get("narration_tashkeel") or spoken, clip, a.model_dir, a.speed)
            else:
                tts_elevenlabs(spoken, clip)
        if clip:
            d = probe(clip)
            s["duration"] = round(max(float(s.get("min_duration", 3)), LEAD + d + TAIL), 2)
            placements.append((clip, t + LEAD))
            report.append({"scene": i, "type": s["type"], "voice_s": round(d, 2), "scene_s": s["duration"]})
        else:
            report.append({"scene": i, "type": s["type"], "voice_s": 0, "scene_s": float(s["duration"])})
        t += float(s["duration"])
    total = t

    if not placements:
        sys.exit("No narration produced: add `narration` to scenes (or recordings for --engine files).")

    # one voice track: every clip delayed to its scene start, then mixed and loudness-normalised
    inputs, filters = [], []
    for k, (clip, start) in enumerate(placements):
        inputs += ["-i", str(clip)]
        ms = int(start * 1000)
        filters.append(f"[{k}:a]aresample=44100,aformat=channel_layouts=mono,adelay={ms}|{ms}[v{k}]")
    n = len(placements)
    mix = "".join(f"[v{k}]" for k in range(n)) + f"amix=inputs={n}:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=44100,apad,atrim=0:{total:.3f}[voice]"
    filters.append(mix)
    final_label = "[voice]"
    if a.music:
        inputs += ["-stream_loop", "-1", "-i", str(Path(a.music).resolve())]
        m = n
        filters.append(f"[{m}:a]aresample=44100,volume={a.music_volume},atrim=0:{total:.3f},afade=t=out:st={max(0, total - 3):.3f}:d=3[music]")
        filters.append("[voice]asplit=2[vmain][vkey]")
        filters.append("[music][vkey]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[ducked]")
        filters.append("[vmain][ducked]amix=inputs=2:normalize=0[mixout]")
        final_label = "[mixout]"
    track = out / f"{slug}-voiceover.m4a"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filters),
                    "-map", final_label, "-c:a", "aac", "-b:a", "192k", "-ar", "44100", str(track)], check=True)

    sb["audio"] = track.name
    timed = out / f"{slug}-timed.json"
    timed.write_text(json.dumps(sb, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"timed_storyboard": str(timed), "voiceover": str(track), "duration_s": round(total, 1),
                      "scenes": report}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
