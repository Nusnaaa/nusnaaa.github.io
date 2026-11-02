# Portfolio refinement verification — 30 October 2026

Implementation branch: `improve/employer-ready-portfolio-oct-2026`.
Compared with `main` at `064660d10573774fa064ffc2d4f5b3d68d5534f1`; main is unchanged. GitHub Pages configuration was read, not modified: legacy publishing from `main:/`, no custom domain and no custom deployment workflow. Review-branch changes are not a live release.

## Content and document results

| Check | Result |
| --- | --- |
| Four-section homepage, approved positioning and public email | PASS |
| Six-section CV in approved order, distinct Unite Students roles | PASS |
| Project ordering and overview/report reciprocal routes | PASS |
| Overview prose length and figures | PASS — 367/377 words, two existing images each |
| Full report evidence, figures, prose and existing IDs retained | PASS — compared section/aside text, media references and IDs with main |
| Rocket model source preserved | PASS — byte comparison with main |
| UAS page unchanged | PASS — Git blob `8bc70dd14e66c34681a6db7aea5361f7e30175de` |
| Aircraft page deleted and no internal links remain | PASS — old external links intentionally become 404 |
| Engineering PDF | PASS — rebuilt, readable two-page tagged PDF; original URL preserved |
| Procurement PDF | PASS — readable one-page tagged PDF at its new URL |
| PDF claims and contact routes | PASS — text extraction, rendered-page review, conservative source reconciliation |
| Both private handover inputs ignored/untracked | PASS — ignore checks and tracked-path scan |
| Static HTML/assets/fragments | PASS — eight nonempty pages, 162 local references; empty unlinked about.html preserved |
| CSS/JS | PASS — CSS parsed with tinycss2; browser loaded all page scripts without new errors |
| Browser layout/keyboard checks | PASS — 40 page/viewport combinations, including UAS |
| Video playback | PASS — all five clips decoded and playback time advanced locally |
| No-JavaScript fallback | PASS — content and fallback navigation on seven modified pages |
| Physical devices, Safari/Firefox, screen reader and field INP | NOT RUN |
| LinkedIn signed-in destination | NOT VERIFIED — automated access blocked; existing owner-supplied URL retained |
| Deployment smoke test | NOT RUN — deployment not authorised |

The engineering PDF corrects 500 N to a **600 N design target**, identifies the final two-ring impinging injector, and records ignition without sustained combustion. The CFD power-coefficient shortfall (approximately 0.13 versus reference 0.27) and uncertain acoustic fidelity appear alongside the result. Both PDFs use the approved email and consistent dates/qualification. Unsupported supplier counts, contract counts, delivery timing, team co-leadership and savings assertions were not carried into the rebuilt PDFs. No confidential supplier or tender information was added. Named procurement exercises were omitted where supporting detail was unavailable.

## Browser context

Playwright Python 1.64.1; Chromium 156.0.8078.4 on Linux, headless. Local static HTTP server, normal network for functional tests; emulated widths 320, 375, 390, 768 and 1440 px, height 900. All eight pages tested. Emulation is not physical-device testing.

Verified keyboard skip links and main focus, visible focus outlines, all five shared navigation links at small widths, Contact routing from root/nested pages, generated anchor destinations, report/UAS TOC Enter/Escape behaviour and heading focus after activation. Verified no TOC on compact overviews, rocket-model arrow input and Enter reset, no horizontal page overflow, no new JavaScript errors or failed page resource responses. Video playback and no-JavaScript fallback were checked separately. Screen captures and raw measurements are retained locally, outside tracked paths.

## Performance observations

Measured on 30 October 2026 with the same Playwright/Chromium versions. Frozen `main` served at `http://127.0.0.1:8766/before/`; proposed branch at `http://127.0.0.1:8766/after/`; separate live baseline at `https://nusnaaa.github.io/`. Viewport 390×844 CSS px, DPR 1, mobile/touch emulation, CPU slowdown 4×. CDP requested 80 ms latency, 4 Mbit/s download and 1 Mbit/s upload. **These are lab settings, not a measured real mobile connection. Media traffic can bypass portions of CDP emulation; the live media byte volume demonstrates that the nominal bandwidth must not be treated as a universal cap.**

One cold-cache and one repeat warm-cache navigation per page and origin. Ten-second observation window after DOMContentLoaded, no scrolling or input. Bytes include completed encoded transfers and observed partial transfers; request counts include pending responses. No field percentile, full-page-download completion or interaction latency is inferred. Local Python server sends uncompressed resources; GitHub Pages serves compressed text and supports different caching/range behaviour, so cross-origin byte totals are not direct hosting comparisons.

Cold-cache local observations (milliseconds and decimal kB):

| Page | TTFB before → after | FCP before → after | LCP before → after | Initial kB before → after | Requests before → after |
| --- | ---: | ---: | ---: | ---: | ---: |
| Homepage | 3 → 3 | 444 → 404 | 444 → 404 | 47.9 → 27.3 | 4 → 4 |
| Projects | 3 → 2 | 312 → 320 | 312 → 320 | 20.1 → 22.7 | 3 → 3 |
| CV | 3 → 2 | 468 → 372 | 468 → 372 | 77.9 → 32.7 | 4 → 4 |
| Full aeroacoustics | 2 → 2 | 560 → 568 | 560 → 568 | 135.6 → 139.7 | 7 → 6 |
| Full rocket | 3 → 2 | 1056 → 812 | 1056 → 812 | 4398.2 → 732.1 | 17 → 12 |
| New aeroacoustics overview | — → 3 | — → 384 | — → 416 | — → 89.4 | — → 5 |
| New rocket overview | — → 2 | — → 416 | — → 416 | — → 588.5 | — → 5 |

All measured initial layout-shift sums were zero in this observation window (not a full field CLS assessment). LCP was predominantly text at this mobile viewport; images can finish later. Six transfers were pending at baseline rocket observation end, versus none after. The original aeroacoustics iframe also initiated a below-fold document request; adding lazy loading avoids that request during initial observation. The after overview routes did not exist in the baseline.

Local warm LCP before → after: homepage 88 → 96 ms; projects 64 → 152 ms; CV 144 → 104 ms; full aeroacoustics 124 → 116 ms; full rocket 168 → 140 ms. New overviews: 100/180 ms. Small timing differences in individual runs are noise, not evidence of a reliable speedup or regression. Warm-cache transferred bytes were zero except a small 104-byte after listing revalidation and approximately 4.13 MB of baseline rocket media. The after pages are within the 2.5 s lab LCP aim, but this does not promise a PageSpeed score or a field result.

Live cold baseline TTFB/FCP/LCP: homepage 260/660/660 ms; projects 161/400/400 ms; CV 220/624/624 ms; full aeroacoustics 242/832/832 ms; full rocket 160/720/720 ms. Live homepage initial transfer was approximately 10.1 kB; live rocket initial transfer approximately 31.46 MB including partial video downloads. Live warm LCP was 84/68/112/120/152 ms respectively. The reported ten-second homepage delay was **not reproduced** in these runs. No conclusion is drawn that GitHub Pages or DNS is its cause; test the affected device/network if it recurs.

Changes with directly observed effects: homepage/CV text and CSS payload reduced; metadata/fallback routes add a small amount to the listing and full aeroacoustics page; videos changed from metadata preload to on-demand; three original rocket photos total 24,110,378 → 2,002,862 bytes (91.7% file reduction), visually reviewed with orientation preserved; image dimensions reserve space; report iframe lazy-loaded. Initial rocket transfer in the local window fell approximately 83%, with no video prefetch after. No claim equates the 91.7% photo reduction to homepage speed, because the homepage embeds no images/videos.

## Reproduction and remaining scope

See `tools/README.md`. PDF generation requires optional development-time Playwright; the website adds no runtime framework or dependency. Original full-resolution photographs remain recoverable from main history. Keep validation runs separate from content editing for stable comparisons.

Owner-authored UAS content, manual LinkedIn checking, physical/cross-browser and assistive-technology checks remain outside the executed validation. No material factual/PDF blocker remains. The branch is ready for owner review and release approval; the existing live site still has the older positioning, aircraft placeholder link and older PDF, so prefer reviewing/releasing the refined branch before sending it as the final application portfolio. **NOT MERGED / NOT DEPLOYED.**
