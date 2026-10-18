#!/usr/bin/env python3
"""Kora Klicks original music bed: an energetic electronic sports track composed in code
(no samples, no third-party audio, so no copyright claims), locked to the video's scenes.

  python3 music.py storyboard.json OUT_DIR [--bpm 120] [--mood drive|dark|anthem] [--seed 1]

- Snaps every scene to whole bars (default 2-bar grid) so cuts land on the beat.
- Arrangement: filtered build-up during the intro, the drop on the first cut, an impact
  plus a short riser on every scene change, and a clean ending on the outro.
- Writes <slug>-music.wav and <slug>-timed.json (with "audio" set), ready for render.py.
"""
import argparse, json, subprocess
from pathlib import Path
import numpy as np
from scipy.signal import butter, sosfilt

SR = 44100
rng = np.random.default_rng(1)

MOODS = {  # chord roots (semitones from A2 = 110 Hz) and chord quality, one chord per bar
    "drive":  [(0, "m"), (-4, "M"), (3, "M"), (-2, "M")],   # Am F C G
    "dark":   [(0, "m"), (-4, "M"), (-2, "M"), (-5, "m")],   # Am F G Em
    "anthem": [(-4, "M"), (3, "M"), (-2, "M"), (0, "m")],    # F C G Am
    "fun":    [(3, "M"), (-2, "M"), (0, "m"), (-4, "M")],    # C G Am F, bouncy pluck lead (memes, light shorts)
    "phonk":  [(0, "m"), (0, "m"), (-4, "M"), (-5, "m")],    # drift-phonk style (cowbell + 808), use --bpm 140
}


def hz(semi, base=110.0):
    return base * 2 ** (semi / 12)


def env(n, a=0.002, d=0.2, sustain=0.0):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * (sustain + (1 - sustain) * np.exp(-t / d))
    return e


def lp(x, f, order=2):
    return sosfilt(butter(order, min(f, SR / 2 - 100), "low", fs=SR, output="sos"), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, "high", fs=SR, output="sos"), x)


def saw(freq, n, detune=0.0):
    t = np.arange(n) / SR
    out = np.zeros(n)
    for d in (-detune, 0, detune):
        ph = (t * freq * (1 + d)) % 1.0
        out += 2 * ph - 1
    return out / 3


def kick(n=int(0.45 * SR)):
    t = np.arange(n) / SR
    f = 48 + 110 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t * 7)
    click = hp(rng.standard_normal(n) * np.exp(-t * 400), 2000) * 0.25
    return np.tanh(1.8 * (body + click))


def clap(n=int(0.3 * SR)):
    t = np.arange(n) / SR
    noise = rng.standard_normal(n)
    e = np.zeros(n)
    for off in (0, 0.011, 0.022):
        k = int(off * SR)
        e[k:] += np.exp(-(t[: n - k]) * 60)
    e += np.exp(-t * 14) * 0.5
    x = sosfilt(butter(2, [900, 4000], "band", fs=SR, output="sos"), noise * e)
    return x / (np.abs(x).max() + 1e-9)


def hat(open_=False):
    n = int((0.22 if open_ else 0.06) * SR)
    t = np.arange(n) / SR
    x = hp(rng.standard_normal(n), 7000) * np.exp(-t * (14 if open_ else 70))
    return x / (np.abs(x).max() + 1e-9)


def impact(n=int(2.2 * SR)):
    t = np.arange(n) / SR
    f = 30 + 60 * np.exp(-t * 6)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.2)
    crash = hp(rng.standard_normal(n), 3000) * np.exp(-t * 3.5) * 0.35
    return np.tanh(1.5 * (boom + crash))


def riser(n):
    t = np.arange(n) / SR
    noise = rng.standard_normal(n)
    out = np.zeros(n)
    # sweep a band-pass upward in chunks
    chunks = 24
    for i in range(chunks):
        a, b = i * n // chunks, (i + 1) * n // chunks
        fc = 400 * (12 ** (i / chunks))
        seg = sosfilt(butter(2, [fc * 0.7, min(fc * 1.4, 18000)], "band", fs=SR, output="sos"), noise[a:b])
        out[a:b] = seg
    return out * (t / t[-1]) ** 2


def pop(n=int(0.12 * SR)):
    """short bubbly 'pop' for meme captions / chat bubbles"""
    t = np.arange(n) / SR
    f = 900 + 1400 * np.exp(-t * 60)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 38)


def whoosh(n=int(0.45 * SR)):
    t = np.arange(n) / SR
    x = riser(n) * np.sin(np.pi * t / t[-1])
    return x / (np.abs(x).max() + 1e-9)


def pluck(freq, n):
    t = np.arange(n) / SR
    x = (np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(4 * np.pi * freq * t) + 0.15 * np.sin(6 * np.pi * freq * t))
    return x * np.exp(-t * 9) * np.minimum(1, t / 0.003)


def square(freq, n):
    t = np.arange(n) / SR
    return np.sign(np.sin(2 * np.pi * freq * t))


def cowbell(semi, n=int(0.22 * SR)):
    """phonk cowbell: two detuned squares, band-passed, fast decay; semi = semitones from A4"""
    k = 2 ** (semi / 12)
    t = np.arange(n) / SR
    x = (square(587 * k, n) + square(845 * k, n)) * 0.5
    x = sosfilt(butter(2, [500, 4500], "band", fs=SR, output="sos"), x)
    return x * np.exp(-t * 16) * np.minimum(1, t / 0.002)


def bass808(semi, n):
    """808 with a short pitch drop and saturation; semi from A1 (55 Hz)"""
    t = np.arange(n) / SR
    f = 55 * 2 ** (semi / 12) * (1 + 1.0 * np.exp(-t * 40))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.6) * np.minimum(1, t / 0.003)
    return np.tanh(2.6 * x)


def phonk_parts(total, intro_end, outro_start, beat, bar, chords):
    n = int((total + 0.05) * SR)
    drums, bass, lead = np.zeros(n), np.zeros(n), np.zeros(n)
    K, C, H = kick(), clap(), hat()
    st = beat / 4                                   # 16th note
    melody = {0: 0, 3: 3, 6: 7, 8: 5, 10: 3, 12: 0, 14: -2}
    for k in range(int(total / bar) + 1):
        tb = k * bar
        root = chords[k % len(chords)][0]
        in_intro, in_end = tb < intro_end, tb >= outro_start + bar
        for step, semi in melody.items():
            ts = tb + step * st
            if ts < total:
                add(lead, cowbell(semi + root), ts, 0.35 if in_intro else 0.5)
        if in_intro or in_end:
            continue
        for step in (0, 6, 10):                     # kick + 808 pattern
            ts = tb + step * st
            add(drums, K, ts, 0.8)
            add(bass, bass808(root, int(min(4 * st if step else 6 * st, 0.9) * SR)), ts, 0.75)
        add(drums, C, tb + 8 * st, 0.75)            # half-time clap on beat 3
        for step in range(16):                      # hats, with a 32nd roll at the end of every 2nd bar
            add(drums, H, tb + step * st, 0.16 if step % 2 == 0 else 0.09)
            if k % 2 == 1 and step >= 13:
                add(drums, H, tb + step * st + st / 2, 0.08)
    return drums, bass, lead


def add(buf, x, at, gain=1.0):
    i = int(at * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(x))
    buf[i:j] += x[: j - i] * gain


HOUSE_DIR = Path(__file__).resolve().parents[3] / "assets" / "music"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("storyboard"); ap.add_argument("out_dir")
    ap.add_argument("--bpm", type=float, default=120)
    ap.add_argument("--mood", choices=list(MOODS), default="drive")
    ap.add_argument("--grid", type=int, default=2, help="snap scenes to multiples of this many bars")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--track", help="owner track (mp3/wav) to use instead of the generated music; default: "
                    ".claude/assets/music/house.* if it exists")
    ap.add_argument("--generated", action="store_true", help="ignore the house track, use the code-made music")
    a = ap.parse_args()
    global rng
    rng = np.random.default_rng(a.seed)

    sb = json.loads(Path(a.storyboard).read_text(encoding="utf-8"))
    out = Path(a.out_dir).resolve(); out.mkdir(parents=True, exist_ok=True)
    slug = sb.get("slug", "kora-klicks-video")
    beat = 60.0 / a.bpm; bar = 4 * beat
    # snap scenes to the bar grid (never shorter than the original duration minus half a bar)
    starts, t = [], 0.0
    for s in sb["scenes"]:
        d = float(s["duration"])
        bars = max(a.grid, int(round(d / bar / a.grid)) * a.grid)
        if bars * bar < d - bar / 2:
            bars += a.grid
        s["duration"] = round(bars * bar, 3)
        starts.append(t); t += s["duration"]
    total = t
    n = int((total + 0.05) * SR)
    drums, bass, synth, fx = (np.zeros(n) for _ in range(4))

    intro_end = starts[1] if len(starts) > 1 else bar * 2
    outro_start = starts[-1]
    K, C, H, HO = kick(), clap(), hat(), hat(True)
    chords = MOODS[a.mood]
    nb = int(total / beat) + 1
    pump = np.ones(n)  # sidechain envelope driven by kicks
    for b in range(nb):
        tb = b * beat
        in_intro = tb < intro_end
        in_end = tb >= outro_start + bar  # last part of outro: drums out
        if not in_intro and not in_end:
            add(drums, K, tb, 0.95)
            i = int(tb * SR); j = min(n, i + int(0.28 * SR))
            pump[i:j] = np.minimum(pump[i:j], 0.35 + 0.65 * (np.arange(j - i) / (j - i)) ** 0.6)
            if b % 4 in (1, 3):
                add(drums, C, tb, 0.55)
            add(drums, H, tb + beat / 2, 0.22)
            if b % 2 == 1:
                add(drums, HO, tb + beat / 2, 0.12)
            add(drums, H, tb + beat / 4, 0.08); add(drums, H, tb + 3 * beat / 4, 0.08)
        elif in_intro:
            add(drums, H, tb + beat / 2, 0.10 + 0.15 * tb / max(intro_end, 1e-3))

    # bass + chord stabs, one chord per bar
    for k in range(int(total / bar) + 1):
        tb = k * bar
        root, q = chords[k % len(chords)]
        third = 3 if q == "m" else 4
        in_intro = tb < intro_end
        for step in range(8):  # 8th-note bass
            ts = tb + step * beat / 2
            if ts >= total or ts >= outro_start + bar:
                break
            nn = int(beat / 2 * SR * 0.9)
            f = hz(root - 12 if step % 2 == 0 else root)
            note = (np.sin(2 * np.pi * f * np.arange(nn) / SR) * 0.7 + lp(saw(f, nn, 0.004), 900) * 0.5) * env(nn, 0.004, 0.18, 0.4)
            add(bass, note, ts, 0.0 if in_intro else 0.55)
        # off-beat stabs (minor/major triad, an octave up)
        for step in (1, 3, 5, 7):
            ts = tb + step * beat / 2
            if ts >= total or ts >= outro_start + bar:
                break
            nn = int(0.22 * SR)
            ch = sum(saw(hz(root + iv + 12), nn, 0.006) for iv in (0, third, 7)) / 3
            cut = 1200 + 3800 * min(1.0, tb / max(intro_end, 1e-3)) if in_intro else 4500
            add(synth, lp(ch, cut) * env(nn, 0.003, 0.09), ts, 0.30 if not in_intro else 0.22)
        # pad
        nn = int(bar * SR)
        pad = sum(saw(hz(root + iv + 12), nn, 0.01) for iv in (0, third, 7, 12)) / 4
        add(synth, lp(pad, 700 if in_intro else 1400) * env(nn, 0.25, 9, 0.8), tb, 0.10)
        if a.mood == "fun":  # 16th-note pluck arpeggio, two octaves up
            arp = (0, third, 7, 12, 7, third, 0, 7)
            for step in range(16):
                ts = tb + step * beat / 4
                if ts >= total or ts >= outro_start + bar or (in_intro and step % 2):
                    continue
                add(synth, pluck(hz(root + 24 + arp[step % 8]), int(0.25 * SR)), ts, 0.16)

    if a.mood == "phonk":  # replace the house arrangement with the phonk one
        drums, bass, synth = phonk_parts(total, intro_end, outro_start, beat, bar, chords)
        pump = np.ones(n)

    # fx: intro riser into the first cut, impacts + short risers on every scene change, final hit
    if len(starts) > 1:
        add(fx, riser(int(intro_end * SR)), 0, 0.35)
    P, WH = pop(), whoosh()
    for k, st in enumerate(starts):
        sc = sb["scenes"][k]
        kind = sc.get("sfx", "impact")
        if k > 0:
            if kind == "impact":
                add(fx, impact(), st, 0.7)
                rl = min(beat * 2, 1.2)
                add(fx, riser(int(rl * SR)), max(0, st - rl), 0.22)
            elif kind == "whoosh":
                add(fx, WH, max(0, st - 0.3), 0.45)
            elif kind == "pop":
                add(fx, P, st, 0.5)
        for pt in sc.get("pops", []):  # extra pops inside the scene (seconds from scene start)
            add(fx, P, st + float(pt), 0.45)
    add(fx, impact(), outro_start + bar, 0.8)

    music = drums * 0.9 + (bass + synth) * pump + fx
    fade = int(min(2.5, total / 4) * SR)
    music[-fade:] *= np.linspace(1, 0, fade)
    music = np.tanh(1.2 * music / (np.abs(music).max() + 1e-9)) * 0.9
    stereo = np.stack([music, np.roll(music, int(0.008 * SR))], axis=1)  # small Haas width
    import soundfile as sf
    raw = out / f"{slug}-music-raw.wav"
    sf.write(str(raw), stereo, SR)
    final = out / f"{slug}-music.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-af",
                    f"loudnorm=I=-14:TP=-1.5:LRA=9,aresample={SR},atrim=0:{total:.3f}", str(final)], check=True)
    raw.unlink()
    track = None if a.generated else (Path(a.track) if a.track else next(iter(sorted(HOUSE_DIR.glob("house.*"))), None))
    if track:  # owner's track (18 Oct 2026): loop/trim to the video length, short fade in, fade out at the end
        fo = min(2.5, total / 4)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-stream_loop", "-1", "-i", str(track), "-af",
                        f"atrim=0:{total:.3f},afade=t=in:d=0.15,afade=t=out:st={total - fo:.3f}:d={fo:.3f},"
                        f"loudnorm=I=-14:TP=-1.5:LRA=9,aresample={SR}", "-ac", "2", str(final)], check=True)
    sb["audio"] = final.name
    timed = out / f"{slug}-timed.json"
    timed.write_text(json.dumps(sb, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"music": str(final), "track": str(track) if track else "generated",
                      "timed_storyboard": str(timed), "bpm": a.bpm, "mood": a.mood,
                      "duration_s": round(total, 2), "scene_durations": [s["duration"] for s in sb["scenes"]]},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
