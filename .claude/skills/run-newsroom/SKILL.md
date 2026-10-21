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
2b. **Live-coverage plan check (firm rule, review 18 Oct: no plan on 16, 17 and 18 Oct, REPEATED from 12–13 Oct).**
   Any scheduled cycle from 09:00 on: `grep -c "PLAN" logs/<today>.md`. If 0, the 08:47 planner failed: build the plan NOW
   (same steps as the planner; `list_triggers` recurring false first), before news. «Only evening matches left» is never a
   reason to skip: every remaining big match still gets line-ups / FT tasks and every other Tier A slot a FT round-up task.
   Every cycle FIRST appends `HH:MM · — · STARTED · cycle` and pushes it (silent cycles 13, 16, 17, 18 Oct), then ends with one result line, even «NO NEW».
   **The plan covers the FULL slate (review 19 Oct, REPEATED 17 Oct):** on 18 Oct the plan (built ~14:30, no log line) had only
   Forest×Arsenal + Real×Sevilla; Juventus×Lazio, Brighton×Palace, Bournemouth×Sunderland and 5 La Liga/Serie A matches got nothing.
   Take the day's list from a full schedule page (FilGoal/Yallakora match centre, or livesoccertv.com/schedules/<YYYY-MM-DD>/ —
   its times are US Eastern: Cairo = ET + 7 h in Oct) and write it into the log as ONE line
   `PLAN · <home×away HH:MM> | … · tasks: <list>` before creating tasks. The noon story and the night results task read that line.
   Log times are Cairo (`TZ=Africa/Cairo date +%H:%M`), never UTC.
   **No excuses (review 20 Oct, REPEATED 6th time):** on 19 Oct the 09:20/11:12 cycles skipped the plan because «the 08:47 planner
   is still running», 13:15 skipped it because «noon ran», and 19:12/21:09 started building it and died with no line.
   A planner «still running» is not a PLAN line: only `grep -c "PLAN"` > 0 counts. Build it in two pushes:
   (1) one schedule search → append + push the `PLAN · …` slate line at once (before any task is created, so a run that dies
   still leaves the slate for the next one); (2) then create the tasks and append `PLAN-TASKS · …`.
   The slate always includes the matches of the Arab stars' clubs (`coverage.md` «Arab stars' clubs»), e.g. Trabzonspor (Salah).
   **Tasks must exist, not just be written (review 21 Oct):** on 20 Oct the PLAN line said «tasks: SPL FT round-up 00:30» but no
   such task was ever created, and the 10:51 UCL desk died (run PENDING, no line, no task) so UCL MD3 night (PSG×Barça,
   Liverpool×Villarreal, City×AEK…) got no XI, no FT, no «ليلة الأبطال»; 19:15/21:15/23:10 cycles all wrote «left to live/FT tasks».
   Every cycle from 11:07: `python3 scripts/missing_runs.py logs/<today>.md` and `list_triggers` (recurring false, enabled) — a
   PLAN/UCL task named in the log that is not in the list → create it now. On a UCL matchday (`ucl.md` calendar) with no
   `UCL plan` line by the 11:07 cycle, the desk failed: create its one-off tasks yourself (ucl.md package, times from its table)
   and log `UCL plan · …`. «Left to the FT task» is only valid after you have seen that task in `list_triggers`.
3. **No duplicates (firm rule, after 11 Oct: Como–Roma and Palace–Forest each went out twice).** Before writing any result or story:
   - run `bash .claude/skills/newsroom-rules/scripts/already_posted.sh <team names in Arabic and English>` (today's + yesterday's log);
   - check `getScheduledPosts` from **00:00 Cairo today** (not just the last few hours), searching the text for the team names;
   - never trust a "not yet posted" note from an earlier run: the log entries with a plannerUrl are the truth.
   If it was posted, only a missing network or a new stage (HT → FT) may go out.
   Also check the growth plan for the next 4 h: a big match without its «توقعوا النتيجة» post → make it now (live-match step 8).
3b. **Morning round-up (09:07 cycle only, owner ✅ 21 Oct):** for each league whose round finished yesterday and has no
   «أهم نتايج الجولة» post yet (already_posted.sh), make one round-up Short (`motion_short.py`, all results, top scorer/star)
   scheduled for **10:00** → YouTube Short + IG Reel (+ end card), and the same results as a TikTok PHOTO post (growth-playbook §0.7).
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
