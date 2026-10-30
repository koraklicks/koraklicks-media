# Kora Klicks growth playbook

The goal is **reach first, then revenue**, without breaking the verification rule or the calm voice.
Every agent reads this before working. The **growth-analyst** updates the "What we learned" section
weekly from real numbers. Never invent metrics; when data is missing, say so.

## 0. Growth plan (owner-approved 12 Oct 2026) — do these every day
1. **Short video is the main discovery door.** 3–4 vertical videos a day on Instagram Reels, Facebook Reels, TikTok and YouTube Shorts, all made with `story_short.py`:
   noon «ماتشات النهارده», a short right after every big match's full time, «رقم/خبر اليوم» (afternoon), night «نتايج النهارده». Answer in the first 2 seconds (score, number or question on screen).
2. **Egypt and Arabs abroad first.** Al Ahly, Zamalek, Pyramids and the Egyptian league get the deepest coverage (line-ups, HT, FT, a short). Every match night: «ليلة العرب» (Salah, Marmoush and the Arab players abroad: goals, assists, minutes, ratings from two live-score sources). Start with the clubs in `coverage.md` «Arab stars' clubs» (Salah → Trabzonspor); «no Arab player found» is only valid after checking every club on that list.
3. **Engagement formats** (they push reach): before every big match a «توقعوا النتيجة» post (X + Instagram + Facebook Story) about 3 h before kick-off; «مين أحسن؟» / «مين نجم الماتش؟» after big matches; a simple quiz card once a day when there is a quiet slot.
   Every feed post gets a short engaging question as `firstCommentText` (e.g. «مين كان نجم الماتش في رأيكم؟ 👇»).
4. **Comments:** Metricool can't read or answer comments. Each evening the community-manager drafts 5–10 ready replies (calm Egyptian dialect) for the most likely comments on the day's biggest posts and includes them in the owner's daily report, for him to paste.
5. **YouTube search titles (owner ✅ 18 Oct, from YouTube Analytics 11–18 Oct: Shorts feed 88.9% of views, search 6.5%, suggested = longest watch):**
   - Start with the two team names exactly as Egyptians search them («طرابزون وكوبس», «النصر و نيفتشي», «بيراميدز …»), then «نتيجة», the score and the scorer/star names; competition name next («دوري أبطال أوروبا»). Then #Shorts for Shorts.
   - Same words in the first line of the description and 5–8 tags (both team names, competition, star players, «نتيجة ماتش …»).
   - «ملخص الجولة» is fine for our round-ups (they summarise results). **Never «أهداف …» / «ملخص المباراة» / «شاهد الأهداف» on a graphics-only video**: viewers expect footage, swipe away and YouTube treats it as misleading metadata (platform-rules §3). Use «مين سجّل في …؟» or «نتيجة وأهداف … بالأرقام» only when the video really lists every scorer.
   - Every Short: the fact on screen in the first 2 s (score/number/name), no slow intro; the like + subscribe end card (`endcard.py`).
   - Feed «Suggested»: keep one long video per round (Europe, UCL, Egypt+Saudi); the owner links each Short to the related long video in YouTube Studio (Shorts «Related video») and adds playlists per competition.
7. **Viral rules (owner ✅ 21 Oct 2026, from the 9–20 Oct numbers):**
   - **TikTok = PHOTO posts** for results and news (photos averaged 127 views vs 15 for videos; top TikToks: «ليفربول 0-3 مانشستر سيتي» 298, «الزمالك 0-2 الأهلي» 229). 3–5 JPGs 1080×1920 in one post: cover with the hook (score/number/name) + one slide per result/fact (`story_short.py` cards). TikTok video only for the morning round-up and memes.
   - **Morning round-up Short at 10:00** for every league whose round finished the day before («أهم نتايج الجولة …», our top YouTube post: 390 views). Made by the 09:07 newsroom cycle (run-newsroom step 3b), YouTube Short + IG Reel; TikTok as photos. Night-of result Shorts stay only for BIG matches.
   - **Egyptian / Arab angle first** in every caption and hook: Salah, Marmoush, Ahly, Zamalek, Pyramids, Arab players before anything else.
   - **Comment bait on everything:** each post ends with one question («مين أحسن؟» / «توقعوا» / «اختار تشكيلتك» / «مين نجم الماتش؟») and the same question as `firstCommentText`.
   - **First 2 seconds = the fact** (score, number, name or question on screen); no logo intro, no slow build-up.
8. **Content plan (owner ✅ 26 Oct 2026, from the 9–25 Oct numbers: TikTok photo avg 534 vs video 4.8; top post «الأهلي 3-3 القناة» photos 947):**
   - **Instagram carousel = the TikTok photo slides.** Every results/news photo post on TikTok also goes to Instagram as a carousel POST (same 3–5 JPG slides, `instagramData.type` POST with several media). Single images only when there is one fact.
   - **Egyptian big-match package** (any Al Ahly / Zamalek / Pyramids match): predictions KO−3 h, line-ups, FT within 15 min (X + IG story + TikTok photos + IG carousel + Reel/Short), and «رقم الماتش» the next morning at 10:00 (one confirmed number from the match).
   - **Weekly series, made by the 16:47 «رقم/خبر اليوم» task (it follows this calendar first; plain «رقم اليوم» on the other days or when the series item has no confirmed data):**
     - Monday: «صلاح الأسبوع ده» — Salah's confirmed numbers this week (matches, goals, assists) as photo slides + short.
     - Tuesday: «تشكيلة الجولة» — 11 best players of the weekend round in the big leagues + Egypt (from a source's published team of the week, e.g. WhoScored/Sofascore/league official; credit it; never our own invented ratings), carousel + TikTok photos.
     - Wednesday: «مين أحسن؟» — two players or two teams side by side with confirmed season numbers, question in the caption.
     - Thursday: «الترتيب بعد الجولة» — table card for the league with the most interesting race (official league site).
     - UCL weeks: «ليلة الأبطال» and «رقم الجولة» stay as in ucl.md.
   - **Comment questions:** «مين أحسن؟» / «توقّع النتيجة» / «سؤال الجولة» (text quiz, no player photos) at the end of every post and as firstCommentText. (Metricool cannot read comments, so we don't announce winners.)
   - **Timing:** non-live posts at 10:00 or 18:00; results as soon as confirmed.
6. **Measure every week:** the Friday growth review compares followers and reach by format (reel vs card vs story), topic and hour, and moves the content mix toward what brings followers.
Not automated (owner does by hand): WhatsApp channel, sharing in Facebook groups, Instagram Collabs with other pages, paid boosts.

## 1. Speed standards (news is a race)

| Event | Target from confirmation to post |
|---|---|
| Live goal / red card | X ≤ 2 min, Instagram Story ≤ 4 min |
| Full-time result | X ≤ 3 min, Facebook + Instagram ≤ 10 min |
| Breaking confirmed news (transfer, coach sacked) | X ≤ 5 min, all other platforms ≤ 15 min |
| TikTok / Reels round-up | same evening, after the last big match |
| YouTube round-up | within 24 h of the round ending |

Speed never overrides verification: an unconfirmed story still waits for the owner.

## 2. Hooks (first line / first 2 seconds)

- Lead with the most surprising **true** fact, not the club name: «أسرع هدف في الجولة: دقيقتين بس».
- Numbers beat adjectives: «5 أهداف في شوط واحد» > «ماتش مجنون».
- Questions and choices drive comments: «مين نجم الماتش؟ 👇», «تتوقعوا مين يكسب؟».
- Arab players and Egyptian and Saudi clubs are the strongest hooks for our audience. Mention them first when relevant.
- Never clickbait: the hook must be true and answered in the post.

## 3. Content mix per day (starting point, to be tuned by data)

| Type | Share | Why |
|---|---|---|
| Results and live | 40% | habit and daily returns |
| Confirmed news (transfers, injuries, coaches) | 30% | shares and saves |
| Engagement (polls, predictions, «اختار تشكيلتك») | 15% | comments boost reach |
| Stats and lists («أكتر 5…», records) | 15% | saves, carousels, evergreen |

## 4. Platform growth levers

- **Facebook:** Reels plus native videos, and one match post updated live. Ask a question in every post and pin the best comment.
- **Instagram:** carousels (saves), Reels 7–20 s with a loopable ending, Stories with polls and quizzes every match day.
- **X:** one live thread per big match; reply fast to trending match conversations from our account; 1–2 relevant hashtags.
- **TikTok:** 1–3 videos a day, hook in 1–2 s, on-screen text, original music. Test both short (<20 s) and longer (60 s+) explainers, because longer videos may be needed for creator monetization.
- **YouTube:** weekly round-ups (long), plus **Shorts** cut from every round-up; searchable Arabic titles; chapters; custom thumbnail with ≤ 4 words.
- **All:** consistent handle and logo (KK), post at the audience's peak times (see section 6), and cross-promote the YouTube video and website.

## 5. Arabic search (SEO) keywords to use naturally

Titles, descriptions and hashtags should contain what people actually type:
«ملخص»، «نتيجة مباراة»، «أهداف»، «ترتيب الدوري»، «موعد مباراة»، «تشكيل»، plus team names in Arabic
and the common English spelling (Al Ahly, Al Hilal). Example YouTube title:
«ملخص ونتيجة مباراة برشلونة وخيتافي 3-0 | الجولة 8 من الدوري الإسباني».

## 6. Posting times (Cairo) — measured, growth review 23 Oct 2026

Metricool best-time scores for 16–22 Oct (Metricool's model; our audience is still tiny, re-check weekly):
- **Instagram:** peak 10:00 every day; second peak 18:00 (weekdays), 18:00–19:00 at weekends. Weakest 02:00–05:00.
- **TikTok:** peaks 10:00, 12:00 and 18:00 (unchanged from 9–15 Oct).
- **YouTube:** peak 16:00 every day (weekdays 14:00–16:00 also strong; 10:00 is a second peak). Weakest 01:00–03:00.
- **X:** not available (best-times 403, impressions empty — same as 16 Oct).
Our own posts: the TikTok photo posts that broke 300 views went out 14:12–23:20, so the format matters more than the hour at our size.
Re-checked 30 Oct (23–29 Oct scores): unchanged — IG 10:00 (2nd 18:00), TikTok 10:00/12:00/18:00, YouTube 16:00 (10:00 second).
Rule from now on: non-live content (رقم اليوم، ماتشات النهارده، round-ups) aims at 10:00 (IG/TikTok) and 16:00 for YouTube-only uploads; live/FT posts keep going out at once.

## 7. Experiments (always run one, one variable at a time)

Each week test **one** thing per platform (hook style, post length, carousel vs single, posting hour,
video length) on at least 5 posts against a comparable control, then keep the winner here.

**Week 17–23 Oct 2026 — result (23 Oct review):**
- TikTok photos: run on 21 Oct only (4 posts) → avg 534 views vs 4.8 for the 16 videos of 16–22 Oct. **Winner: photo.** But 22 Oct results went out as a TikTok VIDEO again (8 views).
- Instagram carousel vs single: NOT RUN (0 carousels posted). Carried over.
- YouTube morning round-up Short: NOT RUN (no «أهم نتايج الجولة» post this week; the 09:07 cycles had no 2-source FTs). Carried over.

**Week 24–30 Oct 2026** (judge on 48 h views in the 30 Oct review):
- TikTok: EVERY TikTok post as a PHOTO post (fixtures, رقم اليوم, results, news; 3–5 JPG slides), no TikTok videos except the morning round-up. Target ≥ 5 photo posts; compare with 534 (photo) vs 4.8 (video).
- Instagram: night results as a 2–4 slide carousel (5 posts) vs single image (5 posts); the Reel still goes out as usual.
- YouTube: one «أهم نتايج الجولة …» round-up Short per league round at 10:00 the morning after (EGY, SPL, PL, LaLiga, Serie A), vs the night-of result Shorts (16–20 Oct: 4 Shorts, 7–212 views, avg 94).
- X: no experiment (not measurable).

**Week 24–30 Oct 2026 — result (30 Oct review):**
- TikTok: 12 photo posts (✅ target) avg 310 views (412 without the <24 h 29 Oct posts) vs 8 fixture VIDEOS avg 172. **Photo wins again**, but the 10:00 «ماتشات النهارده» kept going to TikTok as video.
- Instagram carousel vs single: 6 carousels avg 9.8 views vs 1 single 11 → **no difference**; feed posts ≈ 1/8 of a Reel (avg 78). Owner asked whether to keep carousels (plan §0.8).
- YouTube 10:00 round-up Short: ran once (25 Oct 08:24 PL round 8: 95) vs night-of results Shorts avg 50 → promising, carried over.

**Week 31 Oct–6 Nov 2026** (judge on 48 h views in the 6 Nov review):
- TikTok: «ماتشات النهارده» at 10:00 as a PHOTO post (cover + one slide per match), ≥ 5 posts, vs the 8 fixture videos of 23–29 Oct (avg 172).
- Instagram: one match per Reel for BIG/Egyptian results (≥ 5) vs the multi-result night Reel (≥ 5); same 18:00/at-once timing.
- YouTube: «أهم نتايج الجولة …» round-up Short at 10:00 the morning after each finished round (PL, LaLiga, Serie A, SPL, EGY; target ≥ 3) vs night-of results Shorts (avg 50).
- X: no experiment (not measurable).

## 8. What we learned (updated weekly by the growth-analyst)

### Week 23–29 Oct 2026 (vs 16–22 Oct)
- **TikTok carried the brand:** 5,097 views on the week's posts (×2.2 vs 2,283), followers 4 → 6, interactions 34 vs 19. 12 photo posts avg 310; even fixture videos rose to avg 172 (from 4.8), so the account is now being pushed — keep daily output.
- **Egyptian/Arab + big-match angle won:** top 3 = ليلة العرب (ربيعة/النصيري) 448, الأهلي 4-0 كيتارا 445, فيلا 2-1 سيتي 423; Clasico 417 (TikTok), 163 (IG, top Reel), 167 (YT, top Short with team names + score in the title).
- **Instagram flat:** reach 1,530 vs 1,342 (+14%), Reels avg 78 vs 87, followers 18 → 18. Feed carousels 6–15 views each; fixture Reels 6–38 views (except Clasico day 109).
- **YouTube:** subs 9 → 11; 15 Shorts 23–27 Oct avg 78 (night results Shorts the weakest, 25–40). 28–29 Oct not synced. Revenue 0. Long videos still paused.
- **X:** 6 posts (19 before), impressions 0 → third week unmeasurable.

### Week 16–22 Oct 2026 (vs 9–15 Oct)
- **TikTok photos confirmed (≈ ×110 per post):** 4 photo posts on 21 Oct = 2,134 views (الأهلي 3-3 القناة 947, كومو 4-1 يونايتد + ليل×جالاتاسراي 439, بايرن 2-2 أرسنال 413, رقم اليوم 40 هدف 335); 16 videos = 77 views total. TikTok followers 3 → 4.
- **Egyptian angle won this week:** the top post of the week on any network was الأهلي 3-3 القناة (TikTok photo, 947). On IG the Salah posts were top-3 (صلاح وكوبس 147, صلاح 8 أهداف 126).
- **Instagram did more with less:** 26 posts (20 Reels + 6 images) vs 77 (23 Reels + 54 images); reach 1,274 vs 1,318 (≈ flat), Reels avg 80 views vs 76. Single images still ≈ 9 views each → drop them except match-day predictions. Number hooks («رقم اليوم») again top Reels (164, 140). Followers 14 → 18.
- **YouTube:** subscribers 5 → 9 (16→22 Oct). Shorts published 16–20 Oct: 12, 998 views; best = night results «الأهلي وليفربول وإنتر وبرشلونة» 212 and «صلاح يقود طرابزون» 208 (morning after, 07:31). 21–22 Oct views not synced yet. Revenue 0.
- **Output fell:** X 59 → 19 posts, IG 77 → 26, TikTok 33 → 20; several FTs stayed HOLD (no 2 approved sources). Empty days (19, 22–23 Oct) = near-zero reach.
- **X:** still unmeasurable (followers 4, impressions empty).

### Week 9–15 Oct 2026 (first measured week; Metricool connected 11 Oct, so no week-before comparison)
- **TikTok: photo posts beat videos 8×.** 7 PHOTO posts (11 Oct) averaged 127 views; 26 VIDEO posts averaged 15 (most 0–5). Only two videos broke 100 (أتلتيكو 2-0 يونايتد 172, ليلة الأبطال 136).
- **Instagram: Reels carry the account.** 23 Reels averaged 73 views; 54 single-image feed posts averaged 11. Best Reels: «رقم اليوم» (1953 = 158, 7 أهداف بروج-إنتر = 139). Number hooks win.
- **YouTube: morning-after league round-up Shorts with search titles win** («أهم نتايج الجولة 8 من الليجا» 390, الكالتشيو 122, الإنجليزي 90) and the noon «ماتشات النهارده» (206). Night-of result Shorts: 1–10 views. Long video: 13 views, avg view ≈ 58 s.
- **Topics:** Egypt/Arab stories did not out-perform big European clubs this week (except الزمالك 0-2 الأهلي on TikTok, 229). Keep Egypt first for loyalty, but lead hooks with the biggest number.
- **X:** cannot be measured (no impressions in Metricool).

- **Video style (owner ✅ 13 Oct 2026):** all Reels/Shorts/TikToks are made with `motion_short.py` (motion graphics + original music + beat-synced effects), memes included (one a day max, friendly humour). Alternate the dark and light looks.

- **Music (owner ✅ 18 Oct 2026):** one house track («Match Result Reveal», `.claude/assets/music/house.mp3`) on every video; the TREND-SOUND no-music flow and the phonk/fun/drive rotation are retired. Planners no longer write `TREND-SOUND:`.
