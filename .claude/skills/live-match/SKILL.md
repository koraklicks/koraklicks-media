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
   Timing (firm): line-ups task at kick-off − 70 min (UCL: see ucl.md; no official/approved XI by KO − 25 → drafts to the owner, never from outlets); if a run starts later, post the line-ups as text on X first, then the card.
   Half-time (firm, missed or late on 11, 12 AND 13 Oct): the HT task fires at kick-off + 40 min (not later) and searches from then, using the
   HT/FT playbook in `references/trusted-sources.md` (per competition). Post as soon as two approved sources agree; if after
   HT + 10 min only one source has it, skip HT and put the effort into FT. Full time: within 10 min.
   Kick-off check: HT/FT tasks first confirm the match kicked off on time (search teams + "delayed"/«تأجيل»); if not, re-arm
   themselves (send_later) for the new time.
   Egyptian league + ACLE (owner, 13 Oct 19:30): results ONCE per competition after its last match (one X post + one IG story); no HT, line-ups or per-match posts for them.
   No repeated scores on X (firm, 13 Oct): before any FT post, check whether a round-up already carried that score
   (getScheduledPosts + log). If yes, the late per-match result goes to an IG story only, not to X again.
   Every post gets a question (line-ups: «توقعكم للنتيجة؟ 👇», HT: «الشوط التاني هيجيب إيه؟ 👇»), on X in the text, elsewhere as `firstCommentText`.
4. For each covered match, run this loop until full time:
   - Line-ups (≈60 min before): writer + creative (News template, «التشكيل الرسمي») → X, IG Story, FB.
   - KICKOFF / GOAL / RED CARD / HT: live card (two-source rule) → writer (one line) → creative (Live template; «هدف! GOAL» banner for goals) → **X thread first**, then IG Story, then update the single FB match post.
   - FT: result card → creative (Result template, all three sizes) → X, IG feed, FB, and a TikTok result video for big matches.
5. Live events and results confirmed by the official match centre or two sources are CONFIRMED: publish without asking. Anything uncertain (a disputed goal, unclear scorer) waits until sources agree.
6. VAR changes: publish a «تصحيح» immediately on every platform that carried the event.
7. After the last match: an evening round-up per league (carousel on IG, one post on FB, one tweet on X).

For coverage that must keep running while the owner is away, set this skill up as a scheduled task during match windows (e.g. every 10–15 minutes from kickoff to full time) using the session's scheduling tools.

8. **Growth add-ons for BIG matches** (see `newsroom-rules` → `references/growth-playbook.md` §0):
   - Pre-match (≈ 3 h before kick-off, or at line-ups time if later): a separate «توقعوا النتيجة» post on X + Instagram and a Facebook Story.
     Not made on 12 Oct for Pyramids, Al Nassr or Al Ahli Saudi (only the noon fixtures card asked «توقعاتكم إيه؟»). So: any newsroom
     run that sees a big match kicking off within 1–4 h and no «توقعوا» post for it in the log/getScheduledPosts makes it right away.
   - Full time: within 15 min also make a result short with `story_short.py` (kind "results", one match) and publish it as Instagram Reel, Facebook Reel, TikTok and YouTube Short (#Shorts in the title), plus a «مين نجم الماتش؟» question as the first comment.
   - Egyptian clubs (Al Ahly, Zamalek, Pyramids) always count as big matches.
   - Music: the owner's house track on every FT short (automatic in `music.py`, owner 18 Oct 2026); no TREND-SOUND no-music version, no phonk.
