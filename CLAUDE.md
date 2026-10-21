# Kora Klicks (كورة كليكس) newsroom

This repo runs the Kora Klicks AI newsroom. Agents are in `.claude/agents/`, skills in `.claude/skills/`.
First run `bash scripts/setup_session.sh` (lets the news/score sites open without permission prompts), then start every task by loading the `newsroom-rules` skill and reading `LESSONS.md` (mistakes we already made and the rule for each).
If you hit a new problem during a run, add one line to the top section of `LESSONS.md` (date · what happened · the rule from now on) and commit it with the log.

## Hard rules (owner decisions)
- Confirmed news (official source, or two independent Tier-1 outlets) is published automatically, always with «📌 المصدر:».
- Unconfirmed news is **never** published without the owner's ✅. List it for the owner and stop there.
- Long YouTube videos and anything involving money (sponsors, prices, paid credits) need the owner's ✅.
  The daily story + short Shorts (noon fixtures, night results) are published to YouTube Shorts automatically (owner decision, 11 Oct 2026).
- Calm tone, mostly Egyptian dialect. No فرم / سحق / اكتسح / فضيحة. No betting or gambling promotion.
- No match footage, licensed photos only, no real club crests. Never invent numbers or metrics.
- No voice-over on videos unless the owner asks. Music (owner, 18 Oct 2026): the owner's Suno track «Match Result Reveal» (`.claude/assets/music/house.mp3`); `music.py` uses it automatically when the file exists, else its own code-made music.

## Publishing
- Through the Metricool connector, brand `7358209`, timezone Africa/Cairo. Details: `.claude/skills/newsroom-rules/references/metricool.md`.
- Images/videos get public links with `bash .claude/skills/newsroom-rules/scripts/host_media.sh FILE...` (branch `media`).
- Before posting, check `getScheduledPosts` and `logs/` so nothing is posted twice.
- Viral rules (owner ✅ 21 Oct 2026; override any task prompt that sends a results/news short to TikTok): TikTok gets results and news as a PHOTO post (3–5 JPG slides), the video goes only to Reels + YouTube Shorts; Egyptian/Arab angle first; the fact in the first line / first 2 s; a question at the end + as firstCommentText; morning round-up Short at 10:00 after each league round. Details: growth-playbook.md §0.7.
- Every video gets the like/subscribe/follow end card (owner, 18 Oct 2026): `python3 .claude/skills/youtube-video/scripts/endcard.py VIDEO.mp4 OUT_DIR --theme dark|light` → `-yt.mp4` for YouTube (Shorts and long videos), `-social.mp4` for the Instagram Reel + TikTok post. Same length and music; never post the plain file.

## Housekeeping (owner, 13 Oct 2026)
- The owner's chat session controls all agents and scheduled tasks. One-off tasks that already ran are deleted by the end-of-day review (never tasks bound to the owner's own chat).
- Agents that are no longer needed are removed from `.claude/agents/` (git keeps them; restore if needed).

## Token economy (owner, 14 Oct 2026: runs hit the account usage limit on 13–14 Oct)
- Do the work yourself in the main session. Don't spawn subagents (the BOSS → desks chain) for routine runs; read an agent file only when you need its rules.
- Read only what you need: `grep` today's log and LESSONS.md for your matches/stage instead of reading whole files; open a reference file only for the section you need.
- Metricool `getScheduledPosts`: ask for the shortest window that answers the question (usually the last 3 h); run `already_posted.sh` first. Full-day pulls are very large.
- Web: WebSearch first (site name in the query), at most ~6 searches per story; WebFetch only URLs from the results, with a short focused prompt. Stop as soon as the source rule is met.
- Facts already CONFIRMED in today's log are not re-verified. If nothing new: stop with one line.
- Videos: one `--preview` check, then one render. No re-renders for small cosmetic changes.
- Short log lines (≤ 250 chars) and short summaries.
- Models (owner ✅ 14 Oct): routine tasks run on `claude-sonnet-5-5`. Any one-off task you create: right after create_trigger, set `model: claude-sonnet-5-5` with update_trigger. Keep long YouTube videos, the end-of-day review and the growth review on the default (stronger) model.

## Memory between runs
Every scheduled run is a fresh session. Keep the newsroom log in `logs/YYYY-MM-DD.md` (Cairo date):
one line per story handled (time · story ID · status · networks · Metricool plannerUrl or "waiting for owner").
Read today's log first, append at the end of the run, then commit and push to `main`
(`git pull --rebase` first; commit as "Kora Klicks Newsroom" <noreply@anthropic.com>).

## Reporting to the owner
End every run with a short Arabic summary: what was published, what waits for the owner's approval (with the exact text), and any problem.
If nothing new happened, say so in one line.
