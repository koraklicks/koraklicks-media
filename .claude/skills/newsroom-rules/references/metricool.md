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
| Check what is already queued (avoid duplicates) | `getScheduledPosts` |
| Fix a queued post | `updateScheduledPost` |
| Performance data | `getAnalyticsAvailableMetrics`, then `getAnalyticsDataByMetrics` |

## Network rules (from Metricool)

- `providers` network names: `facebook`, `instagram`, `twitter` (X), `tiktok`, `youtube`.
- Always include the `<network>Data` object for each provider (empty `{}` if nothing to set).
- **X:** one single post, never a thread. Don't cut the text yourself; if Metricool returns a length error, send it back to the writer.
- **Instagram:** needs at least one image (POST/carousel) or a video (REEL). Set `isAiGenerated: true` for AI-made images.
- **TikTok:** needs an image or video. `isAigc: true` for AI-edited videos.
- **Facebook:** text-only POST is allowed; REEL needs a video.
- **YouTube:** video + `title` + `madeForKids: false` + `category: "SPORTS"`. **Only after the owner approved this exact video.**
- `media` must be **public URLs**. Get them by uploading the finished files to the brand media repo
  (github.com/Mohamed-koraklikcs/koraklicks-media):
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
