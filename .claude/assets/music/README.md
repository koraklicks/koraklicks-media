# House music

`house.mp3` = the owner's track «Match Day Power» (uploaded 22 Oct 2026; replaced «Match Result Reveal»).
Owner 22 Oct: use this track in ALL our videos. `music.py` picks `house.*` automatically (never the .json/.md).
`house.json`: drop at 22.05 s, 131 BPM. Shorts start on the drop so frame 0 already has full energy; long videos start at 0.
`motion_short.py` takes its default `--bpm` from `house.json` so cuts and punches land on the beat.
