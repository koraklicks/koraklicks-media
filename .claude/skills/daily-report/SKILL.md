---
name: daily-report
description: >
  This skill should be used when the owner asks how the newsroom did: "daily report",
  "تقرير اليوم", "what did we publish today", "what's waiting for me", "performance today".
  BOSS compiles what was published per platform, what is waiting for owner approval, what was
  rejected, corrections, and tomorrow's plan.
metadata:
  version: "0.1.0"
---

# Daily newsroom report

Ask the **boss** agent to compile, from the newsroom log of the day, a one-page Arabic report:

0. **Silent runs:** `python3 scripts/missing_runs.py logs/<day>.md`; list every MISSING and STUCK cycle in the report (review 19 Oct; STUCK added 20 Oct).
1. **ملخص**: total stories found / published / waiting / rejected.
2. **⏳ مستني موافقتك**: every unconfirmed story still in the queue (approval-queue format). Put this first if not empty.
3. **✅ اللي اتنشر**: a table per platform (Facebook, Instagram, X, TikTok): ID, headline, time, link.
4. **🔁 تصحيحات**: any corrections and why.
5. **📈 الأداء**: top 3 posts by engagement, if a platform analytics connection is available; otherwise skip this section silently.
6. **📅 بكرة**: tomorrow's big matches (Cairo time) and planned coverage.

Keep it short and scannable. Deliver it in the conversation.
