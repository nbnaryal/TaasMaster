# TaasMaster — Call Break, Marriage & Teen Patti score trackers

A static, installable (PWA) website. There is no server code. Upload the `dist/` folder to any static host.

## Pages
| English | Nepali |
|---|---|
| `/` | `/ne/` |
| `/call-break-score/` (tracker) | `/ne/call-break-score/` |
| `/marriage-calculator/` (tracker) | `/ne/marriage-calculator/` |
| `/teen-patti-tracker/` (tracker) | `/ne/teen-patti-tracker/` |
| `/call-break-rules/` | `/ne/call-break-rules/` |
| `/marriage-rules/` | `/ne/marriage-rules/` |
| `/teen-patti-rules/` | `/ne/teen-patti-rules/` |
| `/faq/` | `/ne/faq/` |

## Publishing (automatic)
Every push to `main` triggers `.github/workflows/deploy.yml`, which builds the site and publishes it to GitHub Pages at
https://nbnaryal.github.io/TaasMaster/ . To use your own domain later, add a repository variable `SITE_URL`
(Settings → Secrets and variables → Actions → Variables), e.g. `https://taasmaster.com`, and set the custom domain under Settings → Pages.
Note: Google only reads `robots.txt` at the root of a domain, so use a custom domain before relying on it for SEO.

## 1. Build locally (optional)
```
python3 build.py --base https://your-domain.com
```
This regenerates `dist/` with your domain in the canonical tags, hreflang tags, sitemap, robots.txt and Open Graph tags. It needs Python 3 and Pillow (`pip install pillow`) for the icons.

## 2. Deploy
Upload the **contents** of `dist/` to the root of your domain. The site must sit at the root, not in a subfolder. Free hosts that work well are Cloudflare Pages, Netlify and GitHub Pages. Cloudflare Pages and Netlify also apply the `_headers` file for caching.

## 3. Google Search Console
1. Add your domain as a property at https://search.google.com/search-console and verify it, either with a DNS record or with an HTML file in `dist/`.
2. Go to **Sitemaps** and submit `https://your-domain.com/sitemap.xml`.
3. Use **URL Inspection → Request indexing** for the three tracker pages and the home page.
4. Check **Enhancements** for FAQ and Software App structured data. You can also test any URL at https://search.google.com/test/rich-results.

## Editing content
- Page text: `content_en.py` and `content_ne.py`. Each rules page's `faq` list feeds both the visible FAQ and the `FAQPage` schema.
- Tracker logic and strings: `src/assets/app.js`. Styles: `src/assets/style.css`.
- Run `build.py` again after any change. The service-worker cache version updates automatically, so installed users get the new version.

## How it works
- **Offline:** `sw.js` precaches every page on the first visit and serves pages from the cache first, updating them in the background.
- **Saving:** each game saves to `localStorage` (`taasmaster:<game>:v1`) after every change. A game is only cleared when someone taps "New game".
- **Scoring:**
  - Call Break: a made call scores call + 0.1 for each extra trick; a missed call scores −call.
  - Marriage: each player gets maal × players − total maal. Unseen players count 0 maal. Each loser also pays the winner a fee (seen 3, unseen 10, both editable), plus an optional dublee bonus.
  - Teen Patti: the winner takes the pot.
