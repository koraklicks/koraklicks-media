# Voice-over (عامية مصرية)

## In the storyboard

Every scene can carry a `narration` line (Egyptian dialect, what the voice says) and an optional
`min_duration` (seconds the scene must stay on screen even if the line is short; default 3).
`voiceover.py` sets each scene's `duration` = 0.35 s lead + voice length + 0.65 s tail
(never below `min_duration`), places every clip at its scene start, normalises loudness, mixes
optional music under the voice with automatic ducking, and writes a timed storyboard for `render.py`.

## Engines

| Engine | Quality of Egyptian accent | Cost | Needs |
|---|---|---|---|
| `files` (owner recordings) | Best: a real Egyptian voice | Free | Owner records `scene-01.mp3`, `scene-02.mp3` … |
| `files` (clips from a connected voice tool, e.g. ElevenLabs via a connected service) | Good: clear Arabic, accent depends on the voice chosen | Credits per line | Owner OK on cost |
| `elevenlabs` | Good | ElevenLabs plan (has a free monthly allowance) | `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID` (an Arabic or multilingual voice), internet access to api.elevenlabs.io |
| `offline` (Kareem, Piper via sherpa-onnx), **owner rejected it, only on explicit request** | Robotic, Levantine/MSA accent, not Egyptian | Free, runs anywhere, no API | `pip install sherpa-onnx soundfile` + the voice from GitHub (`vits-piper-ar_JO-kareem-medium`), `--model-dir` |
| `edge` | Real Egyptian neural voices: `ar-EG-ShakirNeural` (male), `ar-EG-SalmaNeural` (female) | Free | `pip install edge-tts`, internet access to Microsoft's speech service |

Some sandboxed environments block these voice services. If so, generate clips where the
service is reachable (e.g. on the owner's computer, or through a connected voice tool) and use `--engine files`.

## Offline voice tips (Kareem)

- Put a fully diacritized copy of each line in `narration_tashkeel` (the on-screen `narration` stays plain). Without tashkeel it mispronounces common words.
- Avoid a sukun on the first letter (write «نِرُوح», not «نْرُوح») and keep «إيه؟» questions simple.
- Check intelligibility by transcribing the clips back with a speech recogniser (e.g. sherpa-onnx Whisper small, also on GitHub releases) and fix any line that comes back garbled.

## Recording guide for the owner

- One file per scene, named `scene-NN.mp3` by scene number (01, 02, …). Scenes without a file stay music-only.
- Quiet room, phone 20 cm from the mouth, read the line once with energy, leave half a second of silence at both ends.
- Re-record any single scene without redoing the rest.

## Writing for the ear

- One idea per line, 12–25 words. Read it aloud: if you run out of breath, split it.
- Numbers as spoken words: «تلاتة صفر», «الدقيقة تلاتة وسبعين».
- No symbols: «الفار», «ضد», «نهاية الماتش».
- Open with a hook, close with a question for the comments and «اشتركوا في كورة كليكس».
