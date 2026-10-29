# austinvanloon.com

Personal website of Austin van Loon, served by GitHub Pages at <https://austinvanloon.com>.

The site is plain static HTML + CSS with one small JavaScript file. There is no framework and no build
step: whatever is committed to `main` is exactly what gets served. (It was originally designed in Lovable
and exported as a React build; in October 2026 the React layer was removed so the pages can be edited
directly, with no dependency on Lovable.)

## What is in here

| Path | Purpose |
| --- | --- |
| `index.html`, `research/index.html`, `software-teaching/index.html`, `cv/index.html` | The four pages. **Edit these.** |
| `research.html`, `cv.html`, `software-teaching.html` | Generated copies of the folder pages so `/research` resolves without a redirect. Never edit by hand; `tools/check.py` regenerates them. |
| `assets/styles.css` | Frozen stylesheet compiled from the original export: design tokens on `:root` plus the Tailwind utility classes the pages use. Do not edit. |
| `assets/site.css` | **Hand-written styles.** Mobile nav panel, home-page animation, and every new or overriding rule. |
| `assets/site.js` | The only JavaScript: toggles the mobile navigation panel. |
| `__l5e/assets-v1/` | Images (folder name inherited from the Lovable export; new images can go anywhere, e.g. `images/`). |
| `cv.pdf` | The downloadable CV linked from the CV page. |
| `404.html` | Custom "page not found" page served by GitHub Pages. |
| `.nojekyll` | Tells GitHub Pages not to run Jekyll. Required: Jekyll silently drops folders whose names start with `_`. |
| `CNAME` | The custom domain (`austinvanloon.com`). |
| `robots.txt`, `sitemap.xml` | Search-engine hints. Add new pages to the sitemap. |
| `tools/check.py` | Pre-push checks: regenerates the copies, validates links, chrome consistency, leftovers. |
| `tools/shots.py` | Headless-Edge screenshots of the local preview, optionally diffed against the live site. |

## Editing workflow

1. Edit the page(s) listed above. The markup uses Tailwind-style utility classes (`mt-20`, `grid`,
   `md:grid-cols-2`, `text-muted-foreground`, ...). Reusing a class that already appears somewhere in the
   pages always works. A utility class that appears nowhere in the site does **not** exist in
   `styles.css`, so for anything new write an ordinary rule in `assets/site.css`, using the tokens
   `var(--primary)`, `var(--foreground)`, `var(--muted-foreground)`, `var(--rule)`, `var(--background)`,
   `var(--card)`, `var(--radius)`.
2. The header (site title, desktop nav, mobile nav) and the footer are repeated verbatim in all four
   pages. Change them in every page; `tools/check.py` fails if they drift apart.
3. Preview locally: `python -m http.server 8787` from the repo root, then open <http://localhost:8787>.
   The pages use absolute paths (`/assets/...`), so they must be served, not opened as files.
4. Run `python tools/check.py`. It regenerates `research.html` etc. and validates everything.
5. Commit and push to `main`. GitHub Pages redeploys within a minute or two.

**CV only:** replace `cv.pdf`, commit, push.

**New page:** copy `software-teaching/index.html` to `newpage/index.html`; replace the `<title>`, the
meta description, the canonical and `og:` tags, the JSON-LD block, and the `<main>` content; add a nav
link in every page's `<nav aria-label="Primary">` and `<nav id="mobile-nav">`; add the URL to
`sitemap.xml`; run the checks. If the page should also resolve at `/newpage` without a redirect, add it
to `COPIES` in `tools/check.py`.

## Hosting setup

- **Repository:** `AustinVL/austinvl.github.io`, publishing from the `main` branch, root folder
  (repository Settings → Pages).
- **Custom domain:** `austinvanloon.com`, entered under Settings → Pages → Custom domain, with
  "Enforce HTTPS" on.
- **DNS** (managed at the registrar, Squarespace Domains):
  - `A` records for the apex domain (`@`): `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
  - `AAAA` records for the apex domain (`@`): `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`
  - `CNAME` record: `www` → `austinvl.github.io`

GitHub redirects `www.austinvanloon.com` to `austinvanloon.com` automatically once both records are in place.
