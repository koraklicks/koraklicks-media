---
name: newsroom-rules
description: >
  This skill should be used whenever any Kora Klicks (كورة كليكس) newsroom work happens:
  finding, verifying, writing, editing, designing or publishing football news, live scores
  or results for the Premier League, La Liga, Serie A, Saudi Pro League, Egyptian Premier
  League, continental club competitions (UEFA, CAF, AFC, Arab), or national teams. It holds the house rules every newsroom agent must follow: the verification gate,
  source crediting, the Egyptian-dialect voice, the brand look and the platform specs.
  Trigger on "Kora Klicks rules", "newsroom rules", "is this confirmed", "can we publish this",
  "house style", or before any agent drafts or publishes content.
metadata:
  version: "0.1.0"
---

# Kora Klicks Newsroom Rules

Apply these rules in every newsroom task. They override any agent's own habits.

## 0. What we cover

- **Tier A (daily, full):** Premier League, La Liga, Serie A, Saudi Pro League, Egyptian Premier League.
- **Tier B (important matches only):** Champions League / Europa / Conference, CAF and AFC club competitions, Arab Club Champions Cup, Club World Cup, domestic cups; Arab national teams (all official matches), European national teams (big matches), Brazil and Argentina; World Cup, AFCON, Asian Cup, Arab Cup, Euro, Nations League, Copa América.
- What makes a Tier B match "important" and the priority order: `references/coverage.md`.

## 1. The verification gate (the most important rule)

Classify every story before anything is written. Use the source tiers in
`references/trusted-sources.md`.

| Status | Meaning | What happens |
|---|---|---|
| **مؤكد (CONFIRMED)** | Announced by an official source (club, league, federation, competition organiser, player's own verified account), OR reported independently by at least two Tier-1 sources | Publish without waiting. Always credit the source on the post. |
| **غير مؤكد (UNCONFIRMED)** | Rumour, single Tier-2 report, "sources say", transfer gossip, agent claims, social posts from unverified accounts | **Never publish.** Put it in the owner's approval queue and wait for an explicit "yes" from the owner. |
| **مرفوض (REJECTED)** | Fake, satire, unsourced, or contradicted by an official source | Drop it. Log the reason. |

Additional hard rules:
- Live match events (goals, cards, final score) count as CONFIRMED only when they appear in an
  official match centre or at least two Tier-1 live-score sources.
- Injuries, deaths, legal cases, arrests, and anything about a person's private life are
  CONFIRMED only from an official statement. Otherwise treat as UNCONFIRMED.
- When a confirmed story later changes, publish a correction labelled "تصحيح" on every platform
  that carried it. Never silently delete.
- Never invent quotes, numbers, or minutes. If a fact is missing, leave it out.

## 2. Source credit format

Every published news post ends with a source line:

`📌 المصدر: [source name]` (e.g. `📌 المصدر: الموقع الرسمي لنادي الأهلي`)

For live scores and results: `📌 المصدر: [league or match-centre name]`.
Credit by name; add the link in the first comment (Facebook, Instagram) or in the reply (X) when a link exists.

## 3. Voice: Egyptian dialect, fan-to-fan

- Write mostly in **Egyptian colloquial Arabic (عامية مصرية)**: lively, warm, short sentences, like a well-informed friend.
  Example: «رسمياً.. صلاح جدد مع ليفربول لحد 2027 🔴»
- Keep **names, numbers, dates, scores and quotes exact**. Quotes stay in the speaker's original wording (translated faithfully if foreign).
- Neutral between clubs. Calm, warm enthusiasm; no harsh verbs (فرم، سحق، اكتسح، ما رحمش…) and no insults or mocking of any club, fans, nationality or referee. Full list: `references/voice-guide.md`.
- Avoid clickbait that the story doesn't support. A headline must be true on its own.
- Dialect and phrasing details: `references/voice-guide.md`.

## 4. Brand look (for the creative agent)

- Colours: pitch green `#00C853`, deep navy `#0A1F44`, white, accent yellow `#FFD600` (live/goal moments only).
- Fonts: Cairo (Arabic), Outfit (English labels).
- **Logo (new, 11 Oct 2026):** wordmark «KORA KLICKS» in extra-bold condensed letters (Anton, thickened, stretched 1.22×) in ice-white #E3F4FF on black, with no symbols. Profile picture / mark: «KK» only, ice-white on black. Final files (SVG + PNG, outlined): `.claude/assets/logo/`. The old ball-and-cursor logo is retired.
- Template families: **News** (navy + yellow «خبر عاجل» tag), **Live** (navy + yellow «مباشر LIVE» pill, optional «هدف! GOAL» banner), **Result** (green + navy «النتيجة النهائية FT»).
- No real club crests unless the owner supplied licensed files. Use team names, or placeholders.

### Cinematic style (default for new work)

Inspired by high-end sports studios: pure black `#050608`, ice-white text `#E3F4FF`, Kora green
`#00C853` as the single accent (yellow `#FFD600` still only for LIVE/goal), giant condensed
display type (Lalezar for Arabic, Anton for numbers/Latin), small mono labels (Space Mono:
`#01`, `01 / 09`, `FULL TIME`), thin `#22272E` divider lines instead of boxes, a huge faint
background word (`FT`, `LIVE`, `BREAKING`), and moody full-bleed photography with a dark grade
when a licensed photo exists. Cinematic templates: `Major-News-Post`, `Major-Live-Post`,
`Major-Result-Post` on the templates canvas; videos use theme `major`.

## 5. Platform specs

Details per platform: `references/platform-specs.md`. Summary:
Publishing tools, brand id, handles and posting rules: `references/metricool.md`.

| Platform | Format | Caption length | Hashtags |
|---|---|---|---|
| Facebook | 1080×1350 or 1600×900 | 1–4 short lines + source | 0–2 |
| Instagram | 1080×1350 post, 1080×1920 story/reel | hook line + 2–3 lines + source | 3–6 |
| X | 1600×900 image, text ≤ 280 chars | one punchy line + source | 1–2 |
| TikTok | 1080×1920 vertical video/slides, 7–30 s | on-screen hook in first 2 s, caption 1 line | 3–5 |

## 6. Handoff format between agents

Every agent passes work on as a **story card**:

```
ID: KK-[YYYYMMDD]-[nn]
Type: news | live | result | feature
Competition: EPL | LALIGA | SERIEA | SPL | EGY | UCL | UEL | UECL | CAFCL | CAFCC | ACLE | ARABCC | CWC | CUP | NT-[team] | WC | AFCON | ASIAN | ARABCUP | EURO | UNL | COPA
Status: CONFIRMED | UNCONFIRMED | REJECTED
Source(s): [name + link] (Tier 1/2/Official)
Priority: 🔴 breaking | 🟡 normal | ⚪ filler
Facts: [bullet list, exact]
Draft: [Arabic text, once written]
Visual: [template + filled fields, once designed]
Approvals: editor ✔/✘ · boss ✔/✘ · owner (UNCONFIRMED only) ✔/✘
```


## Speed over perfection for match data (owner decision, 11 Oct 2026)
- Match facts (scores, scorers, cards, line-ups, kick-off times) are confirmed by **two of Sofascore, 365Scores, FilGoal, Yallakora** (see trusted-sources). Do not hold a result waiting for BBC/Sky/official pages.
- Publish a big-match result within ~10 minutes of full time, and the half-time score at half-time. Don't hold big results for a round-up; round-ups are only for smaller matches.
- Line-ups come out about 60 minutes before kick-off: post them as soon as two live-score sources (or the club) show them.
- If a fetch is blocked, move on to the next source instead of waiting; never skip a big match because one site timed out.
