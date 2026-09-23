#!/usr/bin/env python3
"""Check a stream folder before it is published, optionally filling the YouTube link first.

  stream/py finalize.py <stream-dir> [--fill-youtube] [--require-youtube]

--fill-youtube     if the README's YouTube line is empty, look the video up in the channel's public feed
                   (a video whose title matches the README title, published within 2 days of the stream date)
--require-youtube  fail unless the YouTube line is filled and the video is public

Checks: the folder is titled (not *.untitled), the README has a real title, thumbnail.jpg and slides.html exist,
deck.json builds with every figure present, and every link in the README resolves (http links return < 400,
relative links exist). Rebuilds slides.html + README references from deck.json first. Exit 0 = ready, 1 = not.
"""
import datetime as dt, re, subprocess, sys, time
import xml.etree.ElementTree as ET
from common import TOOLS, get, stream_dir
import requests

CHANNEL = "UCI5dM9hNYAXwuvhQRXwzzww"   # youtube.com/@hu-po


def norm(s): return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def find_youtube(title, day):
    r = get(f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL}")
    if not r: return None
    ns = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}
    want, tail = norm(title), norm(title.split(":")[-1])
    hits = []
    for e in ET.fromstring(r.content).findall("a:entry", ns):
        t = norm(e.findtext("a:title", "", ns)); pub = dt.date.fromisoformat(e.findtext("a:published", "", ns)[:10])
        if abs((pub - day).days) <= 2 and (t == want or t == tail or (tail and tail in t)):
            hits.append((pub, e.findtext("yt:videoId", "", ns)))
    return f"https://youtube.com/live/{sorted(hits)[0][1]}" if hits else None


def link_ok(url):
    if re.search(r"youtu\.?be", url):   # the watch page is always 200; oEmbed 404s for private/deleted videos
        url = "https://www.youtube.com/oembed?format=json&url=" + requests.utils.quote(url, safe="")
    for i in range(3):
        try:
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (hu-po stream link check)"}, timeout=30, allow_redirects=True)
            if r.status_code < 400: return True, r.status_code
            if r.status_code in (404, 410): return False, r.status_code
        except requests.RequestException as e:
            err = str(e)[:60]
        time.sleep(3 * (i + 1))
    return False, locals().get("r") and r.status_code or err


def main():
    d = stream_dir(sys.argv[1]); fill, need = "--fill-youtube" in sys.argv, "--require-youtube" in sys.argv
    problems, rd = [], d / "README.md"
    t = rd.read_text()
    title = (re.search(r"^# (.+)$", t, re.M) or [None, ""])[1].strip()
    if d.name.endswith(".untitled") or title in ("", "Title", "Untitled"): problems.append(f"untitled: folder {d.name}, README '# {title}'")
    day = dt.date(*map(int, d.name[:10].split(".")))
    yt = re.search(r"^\*\*YouTube:\*\*[ \t]*(\S*)", t, re.M)
    if fill and yt and not yt.group(1):
        url = find_youtube(title, day)
        if url:
            t = re.sub(r"^\*\*YouTube:\*\*.*$", f"**YouTube:** {url}", t, count=1, flags=re.M); rd.write_text(t)
            print(f"YouTube: {url}")
        else: print(f"YouTube: no video titled like '{title}' within 2 days of {day} in the channel feed yet")
    if (d / "deck.json").exists():
        r = subprocess.run([sys.executable, str(TOOLS / "deck.py"), str(d)], capture_output=True, text=True)
        print(r.stdout.strip())
        if r.returncode: problems.append("deck.py: " + (r.stdout + r.stderr).strip()[-300:])
    else: problems.append("no deck.json")
    for f in ("thumbnail.jpg", "slides.html"):
        if not (d / f).exists(): problems.append(f"missing {f}")
    t = rd.read_text()
    yt = re.search(r"^\*\*YouTube:\*\*[ \t]*(\S*)", t, re.M)
    if need and not (yt and yt.group(1)): problems.append("YouTube link not filled")
    links = re.findall(r"\]\(([^)\s]+)\)|(https?://[^\s)>\]]+)", t)
    urls = list(dict.fromkeys(a or b for a, b in links))
    bad = 0
    for u in urls:
        if u.startswith("http"):
            ok, code = link_ok(u)
        else:
            ok, code = (d / u).exists(), "missing file"
        if not ok: bad += 1; problems.append(f"link {u}: {code}")
        time.sleep(0.5 if "arxiv.org" in u else 0)
    print(f"links: {len(urls) - bad}/{len(urls)} ok")
    if problems:
        print("NOT READY:\n  " + "\n  ".join(problems)); sys.exit(1)
    print("READY")


if __name__ == "__main__":
    main()
