"""Pre-push checks for austinvanloon.com. Run from the repo root:  python tools/check.py

1. Regenerates the extensionless page copies (research.html, cv.html, software-teaching.html)
   from the folder versions (research/index.html, ...), which are the source of truth.
2. Verifies every page: no stray React/Lovable leftovers, no NUL bytes, stylesheet + site.js wired in,
   mobile-nav panel present, and the header nav + mobile nav + footer identical across pages.
3. Verifies every local href/src resolves to a file in the repo, and that sitemap.xml lists every page.
Exits non-zero on any problem.
"""
import re
import shutil
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ["index.html", "research/index.html", "software-teaching/index.html", "cv/index.html"]
COPIES = {
    "research/index.html": "research.html",
    "cv/index.html": "cv.html",
    "software-teaching/index.html": "software-teaching.html",
}
problems = []

for src, dst in COPIES.items():
    shutil.copyfile(ROOT / src, ROOT / dst)


def segment(html, tag):
    m = re.search(rf"<{tag}\b.*?</{tag}>", html, re.S)
    return m.group(0) if m else ""


def normalize_chrome(s):
    """Canonical form of a header/footer so pages compare equal despite the current-page link styling.

    The active nav link carries aria-current="page" and extra classes (active, text-primary), and its
    attributes come in a different order. Drop those, de-duplicate class tokens, sort attributes.
    """
    def fix_tag(m):
        name, attrs = m.group(1), m.group(2)
        pairs = re.findall(r'([\w:-]+)(?:="([^"]*)")?', attrs)
        out = []
        for key, val in pairs:
            if key == "aria-current":
                continue
            if key == "class":
                seen = []
                for tok in val.split():
                    if tok in ("active", "text-primary") or tok in seen:
                        continue
                    seen.append(tok)
                val = " ".join(seen)
            out.append(f'{key}="{val}"' if val or key == "class" else key)
        return f"<{name}" + ("".join(" " + a for a in sorted(out))) + ">"
    return re.sub(r"<(\w[\w-]*)((?:\s+[^<>]*?)?)>", fix_tag, s)


reference = {}
for p in PAGES:
    html = (ROOT / p).read_bytes().decode("utf-8")
    if "\x00" in html:
        problems.append(f"{p}: NUL bytes")
    for bad in ["modulepreload", "$tsr", "__TSR", 'type="module"']:
        if bad in html:
            problems.append(f"{p}: leftover '{bad}'")
    for need in ['href="/assets/styles.css"', 'href="/assets/site.css"', 'src="/assets/site.js"',
                 'id="mobile-nav"', "data-menu-toggle"]:
        if need not in html:
            problems.append(f"{p}: missing {need}")
    for tag in ["header", "footer"]:
        s = normalize_chrome(segment(html, tag))
        reference.setdefault(tag, (p, s))
        if s != reference[tag][1]:
            problems.append(f"{p}: <{tag}> differs from {reference[tag][0]} (the shared chrome must be edited in every page)")
    for r in set(re.findall(r'(?:href|src)="(/[^"#]+)', html)):
        target = ROOT / r.lstrip("/")
        if not (target.is_file() or (target / "index.html").is_file() or target.with_suffix(".html").is_file()):
            problems.append(f"{p}: broken local link {r}")

sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
for p in PAGES:
    url = "https://austinvanloon.com/" + ("" if p == "index.html" else p.rsplit("/", 1)[0] + "/")
    if url not in sitemap and url.rstrip("/") not in sitemap:
        problems.append(f"sitemap.xml: missing {url}")

if problems:
    print("PROBLEMS:\n  " + "\n  ".join(problems))
    sys.exit(1)
print(f"OK: {len(PAGES)} pages checked, extensionless copies refreshed.")
