# austinvanloon.com

Personal website of Austin van Loon, served by GitHub Pages at <https://austinvanloon.com>.

The site was built with [Lovable](https://lovable.dev) and exported as a static build: pre-rendered HTML for each page plus a small React / TanStack Router bundle that takes over after load. There is no build step in this repository. Whatever is committed to `main` is exactly what gets served.

## What is in here

| Path | Purpose |
| --- | --- |
| `index.html`, `research/`, `software-teaching/`, `cv/` | The four pages, pre-rendered |
| `research.html`, `software-teaching.html`, `cv.html` | Identical copies so that `/research` etc. resolve directly instead of redirecting to `/research/` |
| `assets/` | Compiled JavaScript and CSS (file names contain content hashes) |
| `__l5e/assets-v1/` | Images (Lovable's asset folder) |
| `cv.pdf` | The downloadable CV linked from the CV page |
| `404.html` | Custom "page not found" page served by GitHub Pages |
| `.nojekyll` | Tells GitHub Pages not to run Jekyll. Required: Jekyll silently drops folders whose names start with `_`, which would remove every image |
| `CNAME` | The custom domain (`austinvanloon.com`) |
| `robots.txt`, `sitemap.xml` | Search-engine hints |

## Updating the site

**CV only:** replace `cv.pdf`, commit, push.

**Everything else** (after editing in Lovable and exporting a new build):

1. Delete the old `assets/` folder, then copy in the new `index.html`, the three page folders, `assets/`, `__l5e/`, and `cv.pdf` from the export.
2. Re-create the extensionless copies: `research.html` from `research/index.html`, `cv.html` from `cv/index.html`, `software-teaching.html` from `software-teaching/index.html`.
3. Keep `CNAME`, `.nojekyll`, `404.html`, `robots.txt`, `sitemap.xml`, and this README. If the CSS file name in `assets/` changed, update the stylesheet link near the top of `404.html`.
4. Commit and push to `main`. GitHub Pages redeploys within a minute or two.

Three changes were applied by hand to the exported build and will need re-applying after a fresh export (or, better, made in Lovable so they come out of the export): (1) in the HTML files and `assets/index-*.js`, the canonical and `og:url` tags were made absolute (`https://austinvanloon.com/...`), a social-preview image (`og:image`, the square headshot) was added, and the Twitter card type was changed to `summary`; (2) in `assets/styles-*.css`, `scroll-behavior: smooth` was removed from the `html` rule, because with smooth scrolling the router's scroll restoration interrupted the jump to `#disagreement` / `#ai-methods` from the home page's "Explore this agenda" links; (3) a clearly marked block at the very end of `assets/styles-*.css` adds the home-page entrance animation and hover micro-interactions (cards, buttons, links), with a `prefers-reduced-motion` guard. After a re-export, re-append that block.

## Hosting setup

- **Repository:** `AustinVL/austinvl.github.io`, publishing from the `main` branch, root folder (repository Settings → Pages).
- **Custom domain:** `austinvanloon.com`, entered under Settings → Pages → Custom domain. Turn on "Enforce HTTPS" once GitHub has issued the certificate.
- **DNS** (managed at the registrar, Squarespace Domains):
  - `A` records for the apex domain (`@`): `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
  - `AAAA` records for the apex domain (`@`): `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`
  - `CNAME` record: `www` → `austinvl.github.io`

GitHub redirects `www.austinvanloon.com` to `austinvanloon.com` automatically once both records are in place.
