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
- No voice-over on videos unless the owner asks; use the original music from `music.py`.

## Publishing
- Through the Metricool connector, brand `7358209`, timezone Africa/Cairo. Details: `.claude/skills/newsroom-rules/references/metricool.md`.
- Images/videos get public links with `bash .claude/skills/newsroom-rules/scripts/host_media.sh FILE...` (branch `media`).
- Before posting, check `getScheduledPosts` and `logs/` so nothing is posted twice.

## Memory between runs
Every scheduled run is a fresh session. Keep the newsroom log in `logs/YYYY-MM-DD.md` (Cairo date):
one line per story handled (time · story ID · status · networks · Metricool plannerUrl or "waiting for owner").
Read today's log first, append at the end of the run, then commit and push to `main`
(`git pull --rebase` first; commit as "Kora Klicks Newsroom" <noreply@anthropic.com>).

## Reporting to the owner
End every run with a short Arabic summary: what was published, what waits for the owner's approval (with the exact text), and any problem.
If nothing new happened, say so in one line.
