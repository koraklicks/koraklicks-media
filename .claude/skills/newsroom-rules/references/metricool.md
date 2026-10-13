# Publishing and analytics through Metricool

All publishing and analytics for Kora Klicks go through the connected **Metricool** connector.

## Brand

| Field | Value |
|---|---|
| Brand (blogId) | `7358209` (label «Kora Klicks كورة كليكس») |
| Timezone | `Africa/Cairo` (always use it in `publicationDate`) |
| Facebook page | id `1394713893718953` |
| Instagram | @koraklicks |
| X | @Koraklicks |
| TikTok | @koraklicks |
| YouTube | channel `UCJqeR4W_KYcAqaKo_zslkjA` |

Handles for end-cards and outros: `@koraklicks` (all platforms).
If a value here stops working, call `getBrandSettings` and use what it returns.

## Tools

| Need | Tool |
|---|---|
| Publish now / at a time | `createScheduledPost` (date ≥ now + 2 min for "now") |
| Best slot when no urgency | `getBestTimeToPostByNetwork` |
| Check what is already queued or posted (avoid duplicates) | `getScheduledPosts` from **00:00 Cairo today** to now+3 h, in chunks of ~6 h (a whole day is too big for one call). Also run `scripts/already_posted.sh TEAM...` |
| Fix a queued post | `updateScheduledPost` |
| Performance data | `getAnalyticsAvailableMetrics`, then `getAnalyticsDataByMetrics` |

## Network rules (from Metricool)

- `providers` network names: `facebook`, `instagram`, `twitter` (X), `tiktok`, `youtube`.
- Always include the `<network>Data` object for each provider (empty `{}` if nothing to set).
- **X:** one single post, never a thread. Check the length with `scripts/x_len.py` (≤ 250) before sending; if it is over, the writer shortens it (names go on the card).
- **Instagram:** needs at least one image (POST/carousel) or a video (REEL). Set `isAiGenerated: true` for AI-made images.
- **TikTok:** needs an image or video. `isAigc: true` for AI-edited videos.
- **FACEBOOK PAUSED (13 Oct 2026): no Facebook posts of any kind (feed, reel, story) until the owner lifts the pause. See LESSONS.md.**
- **Facebook:** text-only POST is allowed; REEL needs a video.
  The page is new: Facebook rate-limits frequent posting (error 400 "We limit how often you can post").
  **What happened on 11 Oct:** 5 feed posts in 88 min (14:03–15:31) went through, then every feed post and reel failed for the rest
  of the day (15:51, 16:21, 20:02, 20:21, 22:22, 23:59), even 2–4 h apart. **Facebook Stories never failed.**
  Firm rules:
  - Before any Facebook FEED post, read the last Facebook feed post time from `getScheduledPosts`: never two feed posts less than **60 min** apart,
    and never more than **2 in any 3 h**. Morning catch-up results go to X/Instagram and a Facebook Story, not a burst of feed posts.
  - **Daily budget (owner decision 12 Oct 2026): max 4–5 Facebook FEED posts a day, only for big matches/stories.** Everything else goes to Facebook as a Story. Count today's Facebook feed posts in `getScheduledPosts` before posting.
  - Big results (derbies, top-league clashes) always go to Facebook: as a **Story right away** (works during a block) and as the feed post when the cadence allows.
  - **12 Oct:** after ~20 h of no feed tries (Stories only), the 22:06 feed post (Pyramids 4-1) and the 23:27 one (Al Ain 1-4) both went
    through, and Reels were queued at 01:10 and 02:30 under the 2-per-3 h rule. So the cadence works: keep it, don't burst.
  - After a rate-limit error, the next Facebook feed try is ≥ 2 h later and only for a big result; don't stop Facebook for the day.
- **YouTube:** video + `title` + `madeForKids: false` + `category: "SPORTS"`. **Long videos: only after the owner approved this exact video.** Daily story Shorts (noon fixtures, night results) go out automatically (`type: "short"`).
  YouTube channel is phone-verified (13 Oct 2026): **always send a custom thumbnail** (`videoThumbnailUrl`, a 1280×720 JPG in the brand look with the main result/headline) on long videos; for Shorts use `videoCoverMilliseconds` at the frame that shows the key fact.
- `media` must be **public URLs**. Get them by uploading the finished files to the brand media repo
  (github.com/koraklicks/koraklicks-media):
  `bash .claude/skills/newsroom-rules/scripts/host_media.sh card.jpg reel.mp4`
  It prints one `https://raw.githubusercontent.com/.../media/...` URL per file (branch `media`, kept 14 days); pass those in `media`
  (and a cover image URL in `videoThumbnailUrl` when useful). Metricool copies the file to its own storage.
  Use JPG for images (smaller, TikTok rejects PNG), MP4/H.264 for video, max 95 MB per file.
  Tested 11 Oct 2026: Metricool accepted a raw.githubusercontent.com image.
- If the upload fails (GitHub not reachable in this session), publish text-only where the network allows it (Facebook, X), otherwise deliver a ready-to-post package.

## Delivery mode

- `autoPublish: true` → Metricool publishes on its own. Use for **CONFIRMED + editor ✔ + boss ✔** stories.
- `autoPublish: false` → the owner gets a push in the Metricool app and posts by hand. Use when in doubt.
- **UNCONFIRMED** stories are never sent to Metricool before the owner's ✅.

## After posting

Log `plannerUrl`, network, time, format and story ID in the daily log so the growth-analyst can measure it.
