"""Screenshot the local preview (and optionally the live site) with headless Edge, for before/after comparison.

Usage:  python -m http.server 8787        (in another terminal, from the repo root)
        python tools/shots.py [out_dir] [--live]

Writes local-<page>-desk.png and local-<page>-mob.png per page. With --live it also captures the live
site and reports whether each pair is pixel-identical. Note: headless Edge will not render narrower
than about 490px, so the "mob" shots approximate a large phone, not a small one.
"""
import pathlib
import subprocess
import sys

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PAGES = {"home": "/", "research": "/research/", "software": "/software-teaching/", "cv": "/cv/"}
SIZES = {"desk": "1280,2600", "mob": "500,1800"}

args = [a for a in sys.argv[1:] if not a.startswith("--")]
out = pathlib.Path(args[0] if args else "shots")
out.mkdir(exist_ok=True)
live = "--live" in sys.argv


def shot(name, size, url):
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                    "--virtual-time-budget=6000", f"--window-size={size}", f"--screenshot={out / name}.png", url],
                   capture_output=True)


for n, path in PAGES.items():
    for v, size in SIZES.items():
        shot(f"local-{n}-{v}", size, "http://127.0.0.1:8787" + path)
        if live:
            shot(f"live-{n}-{v}", size, "https://austinvanloon.com" + path)

if live:
    from PIL import Image, ImageChops
    for n in PAGES:
        for v in SIZES:
            a = Image.open(out / f"local-{n}-{v}.png").convert("RGB")
            b = Image.open(out / f"live-{n}-{v}.png").convert("RGB")
            box = ImageChops.difference(a, b).convert("L").getbbox() if a.size == b.size else "size differs"
            print(f"{n:9s}{v:5s} {'identical' if box is None else f'differs: {box}'}")
print("screenshots in", out.resolve())
