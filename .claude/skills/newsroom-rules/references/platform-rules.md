# Platform safety rules (Instagram, TikTok, YouTube, X)

Written 13 Oct 2026 after Meta permanently disabled the admin profile and the Facebook page was lost
(bursts of posts, rate-limit errors, and fast settings changes made with browser automation). Every run follows these rules;
they win over growth targets. Sources were checked on 13 Oct 2026 (list at the end). Re-check them every quarter.

## 1. Never again (firm)

- **No browser automation on any of our accounts.** Agents never log in, follow, like, comment by hand, or change names,
  bios, categories or settings on any platform. Publishing goes ONLY through Metricool (official APIs).
  X says scripting its website can mean permanent suspension; Meta treated our pattern as suspicious.
- Settings, usernames, bios, security: **the owner changes them by hand, one change at a time**, never during a heavy posting day.
- **On any rate-limit / spam / permission error** (e.g. Instagram "limit how often", TikTok `spam_risk_too_many_posts` or
  `spam_risk_user_banned_from_posting`, HTTP 429): stop that network for **24 h**, log it, tell the owner in the run summary.
  Never retry in a loop, never "test" the network again the same day.

## 2. Daily budgets and spacing (Cairo day, count with getScheduledPosts from 00:00 before every post)

| Network | Max per day | Spacing | Hashtags |
|---|---|---|---|
| Instagram | **25 items in total** (feed + reels + stories; API cap is 50/24 h incl. stories, we stay at half). Within that: ≤ 8 feed posts, ≤ 5 reels | ≥ 30 min between feed posts/reels; ≤ 3 stories per hour | **max 5** (Instagram limit since Dec 2025), rotate sets |
| TikTok | **6 videos** (API cap ~15) | ≥ 60 min apart | 3–5, rotate |
| YouTube | **5 Shorts** + long videos only with owner ✅ | ≥ 60 min apart | 3–5; never more than 15 tags/hashtags |
| X | **25 posts** | ≥ 10 min apart; live matches max 6 per hour | **max 2** |

**Check before every post (firm, 13 Oct review):** save the getScheduledPosts JSON (00:00 of the Cairo day → 06:00 next day) to a file
and run `python3 scripts/budget_check.py FILE YYYY-MM-DD --add instagram:REEL@YYYY-MM-DDTHH:MM` (network:type@time of the post you plan).
If it prints SPACING / STORIES / OVER, move the post later. On 13 Oct the feed→reel gaps were 25, 14 and 28 min and 5 IG stories went out in 47 min
(23:54–00:41) because parallel tasks did not see each other's slots; midnight does not reset spacing.

When the budget is tight, keep (in order): Egyptian clubs/players → UCL big matches → Saudi big four → other Tier A →
everything else goes to a round-up or a Story. A round-up beats five separate posts.
12 Oct had 37 Instagram items in one day and 9 TikToks: that is above these budgets. Don't repeat it.

## 3. Content rules that protect reach and the account

- **Original only.** Our own design, text and angle on every card and short. Never repost other accounts' clips, memes or
  screenshots, even with credit (Instagram stops recommending accounts that "regularly repost content they didn't create";
  TikTok and YouTube treat it as unoriginal/reused).
- **No mass-produced look (YouTube "inauthentic content", July 2025).** Each Short has its own facts and angle; rotate
  scene types, themes (dark/light) and music moods; never two near-identical Shorts the same day; no image slideshows with no value.
- **No duplicate posts on X.** Write each X post fresh (not the Instagram caption), never the same score twice,
  never auto-post on trending hashtags, no automated replies or mentions.
- **Engagement questions must be open** («توقعك إيه؟», «مين نجم الماتش؟»). Never «اكتب ١ لو…», «منشن صاحبك», «اكتب كلمة…»,
  «لايك لو…» (engagement bait). Vary the wording; don't reuse the same first comment on every post.
- **Titles and thumbnails match the video.** Never «ملخص كامل / أهداف المباراة / بث مباشر» on graphics-only videos.
  No keyword stuffing in titles, descriptions or tags.
- **IP:** no match footage, no club crests or kits as logos, licensed photos only (keep the licence/source in the log),
  our own code-made music only (no trending sounds). Never dispute a claim without proof.
- **AI label:** not needed for our code-made motion graphics and text cards. If we ever use a realistic AI image, video or
  voice, tick the platform's AI / altered-content label.
- **Gambling:** no odds, tips, links, logos or names of betting sites, ever (TikTok bans marketing gambling; YouTube bans
  uncertified gambling links; X bans gambling ads in Egypt).
- **News:** only CONFIRMED stories (verification gate). TikTok holds back unverified claims about unfolding events.
- **Impersonation:** never present a post as coming from a club, league or player; our name and avatar stay ours.

## 4. Account security (owner checklist, by hand)

- Authenticator-app 2FA on every account; backup codes stored offline; recovery email and phone up to date.
- A second trusted person with access, without sharing passwords:
  YouTube → Settings → Permissions (Manager); TikTok → Business Center with 2 admins; X → Delegate;
  Instagram → Accounts Center / professional tools if available without the lost Facebook profile.
- Log in from one or two known devices; no shared passwords, no unknown "growth" apps connected.
- YouTube: a terminated channel can't be replaced by a new one, and a second copyright or Community Guidelines strike
  stops uploads. Treat every warning as an emergency and tell the owner.

## Sources (checked 13 Oct 2026)

- Instagram hashtag limit (5): socialmediatoday.com/news/instagram-implements-new-limits-on-hashtag-use/808309/ (18 Dec 2025, press)
- Instagram reposts not recommended: techcrunch.com/2026/04/30/instagram-restricts-reach-of-content-aggregators-in-new-crackdown/ (press)
- Instagram API publishing limit: developers.facebook.com/documentation/instagram-platform/content-publishing; Metricool: help.metricool.com/instagram-posting-errors-troubleshooting-fkhpc
- TikTok API ~15 posts/day, spam_risk errors: developers.tiktok.com/doc/content-sharing-guidelines, developers.tiktok.com/docs/en/content-posting-api-reference-direct-post
- TikTok originality / FYF: tiktok.com/community-guidelines/en/fyf-standards; integrity: tiktok.com/community-guidelines/en/integrity-authenticity; gambling: tiktok.com/community-guidelines/en/regulated-commercial-activities
- TikTok Business Center security: ads.tiktok.com/help/article/best-practices-for-securing-your-business-center
- YouTube inauthentic/reused content: support.google.com/youtube/answer/1311392; spam & deceptive practices: support.google.com/youtube/answer/2801973; tags/hashtags: support.google.com/youtube/answer/6390658; AI disclosure: support.google.com/youtube/answer/14328491; strikes: support.google.com/youtube/answer/2802032, support.google.com/youtube/answer/2814000; gambling: support.google.com/youtube/answer/9229611; permissions: support.google.com/youtube/answer/9481328
- X automation: help.x.com/en/rules-and-policies/x-automation; authenticity/spam: help.x.com/en/rules-and-policies/authenticity; limits: help.x.com/en/rules-and-policies/x-limits; hashtags: help.x.com/en/using-x/how-to-use-hashtags; delegate: help.x.com/en/managing-your-account/how-to-use-the-delegate-feature
