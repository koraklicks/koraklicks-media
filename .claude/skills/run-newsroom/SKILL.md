---
name: run-newsroom
description: >
  This skill should be used when the owner wants the Kora Klicks newsroom to run a cycle:
  "run the newsroom", "شغّل الديسك", "ابدأ الشغل", "what's new today", "cover today's news",
  "handle this story", or when a scheduled newsroom run fires. It starts the BOSS agent, which
  drives news-desk, live-score-desk, writer, editor, creative and the four platform publishers.
  Accepts an optional argument: a single story/link to handle, or a league to focus on.
metadata:
  version: "0.1.0"
---

# Run the Kora Klicks newsroom

1. Load the `newsroom-rules` skill.
2. Hand control to the **boss** agent with this brief:
   - Scope: the argument if given (one story, link, league, competition or national team); otherwise a full cycle for the whole coverage map (`newsroom-rules` → `references/coverage.md`): Tier A leagues, plus important Tier B club and national-team matches, covering the last few hours.
   - Steps: news-desk (find + verify) and live-score-desk (today's fixtures/results) in parallel → BOSS decides priority and platforms → writer → editor → creative → platform publishers.
3. **No duplicates (firm rule, after 11 Oct: Como–Roma and Palace–Forest each went out twice).** Before writing any result or story:
   - run `bash .claude/skills/newsroom-rules/scripts/already_posted.sh <team names in Arabic and English>` (today's + yesterday's log);
   - check `getScheduledPosts` from **00:00 Cairo today** (not just the last few hours), searching the text for the team names;
   - never trust a "not yet posted" note from an earlier run: the log entries with a plannerUrl are the truth.
   If it was posted, only a missing network or a new stage (HT → FT) may go out.
4. Enforce the gate on every story:
   - CONFIRMED (official source or two Tier-1 sources) + editor pass → publish now, with `📌 المصدر:`.
   - UNCONFIRMED → owner approval queue only. Never publish without the owner's ✅.
   - REJECTED → drop and log.
5. Run independent agents in parallel (e.g. the four publishers for the same story).
6. Finish with BOSS's report to the owner, in Arabic, in this order:
   1. ⏳ **محتاج موافقتك**: each unconfirmed story in the approval-queue format.
   2. ✅ **اتنشر**: per platform, ID + one line + link (or "package ready" when no publishing connection exists).
   3. ❌ **اترفض**: one line each with the reason.
   4. 📅 **جاي**: next big matches with Cairo time.
7. When the owner replies to the queue (✅ / ✏️ / ❌), route the decision back to BOSS and continue.

Publishers post through Metricool (`newsroom-rules` → `references/metricool.md`). If Metricool is unavailable or a visual has no public URL, deliver ready-to-post packages (final captions + visuals) instead of failing, and mention once which connection would let the publishers post directly.
