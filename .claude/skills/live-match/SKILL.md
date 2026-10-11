---
name: live-match
description: >
  This skill should be used when the owner wants live coverage of a match or of today's matches:
  "cover the match live", "غطّي الماتش", "لايف سكور", "start live coverage", "Al Ahly vs Zamalek live",
  "today's results". It runs the live-score-desk with the creative and publishers for live goal,
  half-time and full-time posts. Accepts an optional match name or league.
metadata:
  version: "0.1.0"
---

# Live match coverage

1. Load the `newsroom-rules` skill.
2. Ask the **live-score-desk** agent for the fixture list (or the named match) with Cairo-time kickoffs and which matches get full live coverage.
3. Before posting anything for a match, run `bash .claude/skills/newsroom-rules/scripts/already_posted.sh <teams>` and check
   `getScheduledPosts` from 00:00 today: if this stage (line-ups / HT / FT) is already out — by another task or by the owner — don't post it again
   (on 11 Oct the Zamalek–Ahly line-ups went out twice on X). Log every post you make with its plannerUrl, line-ups included.
   Timing (firm): line-ups task at kick-off − 45 min; if a run starts later, post the line-ups as text on X first, then the card.
   Half-time: post within 5 min of the HT whistle; if the live pages are cached, use a search for a HT report (Al-Ahram gate for Egypt,
   Sky Sports/BBC report pages for England) instead of waiting. Full time: within 10 min.
4. For each covered match, run this loop until full time:
   - Line-ups (≈60 min before): writer + creative (News template, «التشكيل الرسمي») → X, IG Story, FB.
   - KICKOFF / GOAL / RED CARD / HT: live card (two-source rule) → writer (one line) → creative (Live template; «هدف! GOAL» banner for goals) → **X thread first**, then IG Story, then update the single FB match post.
   - FT: result card → creative (Result template, all three sizes) → X, IG feed, FB, and a TikTok result video for big matches.
5. Live events and results confirmed by the official match centre or two sources are CONFIRMED: publish without asking. Anything uncertain (a disputed goal, unclear scorer) waits until sources agree.
6. VAR changes: publish a «تصحيح» immediately on every platform that carried the event.
7. After the last match: an evening round-up per league (carousel on IG, one post on FB, one tweet on X).

For coverage that must keep running while the owner is away, set this skill up as a scheduled task during match windows (e.g. every 10–15 minutes from kickoff to full time) using the session's scheduling tools.
