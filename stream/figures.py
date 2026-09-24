#!/usr/bin/env python3
"""Visuals for a stream: arXiv figures, project-page / launch-post media, crop QA.

  stream/py figures.py pull  <stream-dir> 2609.14858 2506.13131 ...      # every figure + caption
  stream/py figures.py pull  <stream-dir> --only 2609.14858:F3,F4        # specific figure numbers
  stream/py figures.py crop  <stream-dir> 2609.14858:S5-F6:11:298,208,536,674   # manual PDF crop (page, PDF pts)
  stream/py figures.py page  <stream-dir> https://project.page/          # list media on a page (no download)
  stream/py figures.py get   <stream-dir> <media-url> <stem> [--caption "..."] [--from <page-url>]
  stream/py figures.py qa    <stream-dir> [stems...]                     # flag crops worth a second look
  stream/py figures.py restore <stream-dir> [stems...]                   # rebuild missing files from captions.json

Files land in <stream>/figures/ (gitignored). arXiv figures are named <id>_S<sec>-F<n>.jpg (same as past
streams); web media are named web_<stem>.<ext>. Captions + provenance go to figures/captions.json.
Sources for arXiv, in order: arxiv.org/html, ar5iv, then a PDF crop (PyMuPDF).
Every image is whitespace-trimmed and capped at 1800px wide. Videos/GIFs are kept as-is (<= 25 MB).
"""
import io, json, re, sys, time
from pathlib import Path
from urllib.parse import urljoin, urlparse
import pymupdf as fitz
from bs4 import BeautifulSoup
from PIL import Image, ImageChops
from common import get, stream_dir

MAXW = 1800
VIDEO = (".mp4", ".webm", ".mov")
FIG = CAP = None


def setup(d):
    global FIG, CAP
    FIG = d / "figures"; FIG.mkdir(exist_ok=True); CAP = FIG / "captions.json"


def load_caps(): return json.loads(CAP.read_text()) if CAP.exists() else {}
def save_caps(c): CAP.write_text(json.dumps(c, indent=1, ensure_ascii=False))


def trim(im, pad=12):
    """Cut uniform white margins (PDF crops and HTML bitmaps often carry a lot)."""
    bg = Image.new("RGB", im.size, (255, 255, 255))
    box = ImageChops.difference(im, bg).convert("L").point(lambda v: 255 if v > 18 else 0).getbbox()
    if not box: return im
    x0, y0, x1, y1 = box
    return im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad)))


def save_img(data, stem):
    im = Image.open(io.BytesIO(data))
    if im.mode in ("RGBA", "LA", "P"):
        rgba = im.convert("RGBA"); bg = Image.new("RGB", im.size, "white"); bg.paste(rgba, mask=rgba.split()[-1]); im = bg
    else:
        im = im.convert("RGB")
    im = trim(im)
    if im.width > MAXW:
        im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
    out = FIG / f"{stem}.jpg"
    im.save(out, "JPEG", quality=88, optimize=True)
    return out.name


# ---------- arXiv ----------

def html_figs(aid):
    """-> (base_url, [(figid like S1.F1, [img srcs], caption)]) or None"""
    for base in (f"https://arxiv.org/html/{aid}", f"https://ar5iv.labs.arxiv.org/html/{aid}"):
        r = get(base)
        if not r or "figure" not in r.text: continue
        s = BeautifulSoup(r.text, "lxml")
        out = []
        for f in s.find_all("figure"):
            fid = f.get("id") or ""
            if not re.search(r"\.F\d+$", fid) and not re.match(r"^F\d+$", fid): continue
            if f.find_parent("figure"): continue   # subfigures handled via parent
            imgs = [i.get("src") for i in f.find_all("img") if i.get("src")]
            c = f.find("figcaption")
            cap = " ".join(c.get_text(" ", strip=True).split()) if c else ""
            out.append((fid, imgs, cap))
        if out: return r.url, out
    return None


def pdf_doc(aid):
    p = FIG / f".{aid.replace('/', '')}.pdf"
    if not p.exists():
        r = get(f"https://arxiv.org/pdf/{aid}")
        if not r: return None
        p.write_bytes(r.content)
    return fitz.open(p)


def pdf_crop(doc, n):
    """Crop Figure n from the PDF: region of drawings/images sitting above the caption."""
    pat = re.compile(rf"^\s*(Figure|Fig\.)\s*{n}\s*[|:.]", re.I)
    for page in doc:
        blocks = page.get_text("blocks")
        caps = [b for b in blocks if pat.match(b[4])]
        if not caps: continue
        cx0, cy0, cx1, cy1 = caps[0][:4]
        pw = page.rect.width
        hdr = 0.075 * page.rect.height   # running header band (title line + rule) is never part of a figure
        rects = [fitz.Rect(d["rect"]) for d in page.get_drawings()]
        rects += [page.get_image_bbox(i) for i in page.get_images(full=True)]
        cand = [r for r in rects if r.y1 <= cy0 + 2 and r.y0 >= cy0 - 520 and r.width > 8 and r.height > 3 and r.y0 > hdr
                and (r.x1 > cx0 - 20 and r.x0 < cx1 + 20)]
        if cand:
            u = cand[0]
            for r in cand[1:]: u |= r
            # body-text paragraphs above the figure bound it from the top
            body = [b for b in blocks if not pat.match(b[4]) and b[3] <= u.y0 + 4 and b[1] >= u.y0 - 200
                    and len(b[4].strip()) > 120 and (b[3] - b[1]) > 28 and (b[2] > u.x0 and b[0] < u.x1)]
            if body: u.y0 = max(u.y0, max(b[3] for b in body) + 2)
            # pull in short labels (axis ticks, titles, legends) that sit on or beside the drawing
            for _ in range(2):
                grown = fitz.Rect(u.x0 - 28, u.y0 - 22, u.x1 + 28, u.y1 + 22)
                for b in blocks:
                    t = b[4].strip()
                    if pat.match(t) or len(t) > 120: continue
                    rb = fitz.Rect(b[:4])
                    if rb.intersects(grown) and rb.y1 <= cy0 + 2 and rb.y0 >= max(hdr, cy0 - 560): u |= rb
            clip = fitz.Rect(max(0, u.x0 - 6), max(0, u.y0 - 6), min(pw, u.x1 + 6), min(cy0, u.y1 + 6))
        else:
            clip = fitz.Rect(cx0 - 10, max(0, cy0 - 320), cx1 + 10, cy0)
        pix = page.get_pixmap(matrix=fitz.Matrix(4, 4), clip=clip, alpha=False)
        return pix.tobytes("png"), page.number + 1
    return None, None


def pull(aid, only=None):
    caps = load_caps()
    fsid = aid.replace("/", "")
    got, doc = [], None
    hf = html_figs(aid)
    if hf:
        base, figs = hf
        for fid, imgs, cap in figs:
            m = re.search(r"(?:^|\.)?([A-Za-z]*\d*)\.?F(\d+)$", fid)
            sec = (m.group(1) or "S0").replace("Ax", "A"); n = int(m.group(2))
            if only and n not in only: continue
            stem = f"{fsid}_{sec}-F{n}"
            if any(FIG.glob(stem + ".*")): got.append(stem); continue
            name = None
            for src in imgs[:1]:   # first bitmap; subfigure composites usually share one
                url = urljoin(base, src)
                if url.endswith(".svg"): continue
                r = get(url)
                if r:
                    try: name = save_img(r.content, stem); break
                    except Exception as e: print("  img fail", url, e)
            src_kind = "html"
            if not name:
                doc = doc or pdf_doc(aid)
                if doc:
                    png, pg = pdf_crop(doc, n)
                    if png: name = save_img(png, stem); src_kind = f"pdf p{pg}"; cap = cap or f"Figure {n}"
            if name:
                caps[stem] = {"caption": cap, "src": src_kind, "n_subimages": len(imgs)}
                got.append(stem)
    else:
        doc = pdf_doc(aid)
        if not doc: print(f"{aid}: nothing"); return got
        txt = "".join(p.get_text() for p in doc)
        for n in (only or range(1, 13)):
            stem = f"{fsid}_S0-F{n}"
            if any(FIG.glob(stem + ".*")): got.append(stem); continue
            png, pg = pdf_crop(doc, n)
            if not png:
                if not only: break
                continue
            save_img(png, stem)
            m = re.search(rf"(Figure|Fig\.)\s*{n}\s*[|:.]\s*(.{{0,400}}?)(?:\n\s*\n|(?=\n\s*(Figure|Fig\.)\s*\d))", txt, re.S)
            caps[stem] = {"caption": " ".join(m.group(2).split()) if m else f"Figure {n}", "src": f"pdf p{pg}"}
            got.append(stem)
    save_caps(caps)
    print(f"{aid}: {len(got)} figs -> {', '.join(got)}")
    return got


def manual_crop(aid, stem, page, box):
    doc = pdf_doc(aid); pg = doc[page - 1]
    pix = pg.get_pixmap(matrix=fitz.Matrix(4, 4), clip=fitz.Rect(*box), alpha=False)
    key = f"{aid.replace('/', '')}_{stem}"
    for old in FIG.glob(f"{key}.*"): old.unlink()
    save_img(pix.tobytes("png"), key)
    caps = load_caps(); e = caps.get(key, {}); e["src"] = f"pdf p{page} manual {box}"; caps[key] = e; save_caps(caps)
    print(f"  {key}: manual crop p{page}")


# ---------- web media (project pages, launch posts, GitHub READMEs) ----------

def page_media(url):
    """List candidate media on a page: [(kind, abs_url, hint)]."""
    r = get(url)
    if not r: print(f"{url}: unreachable"); return []
    s = BeautifulSoup(r.text, "lxml"); out = []
    for m in s.find_all("meta", attrs={"property": "og:image"}):
        if m.get("content"): out.append(("og:image", urljoin(r.url, m["content"]), "social card"))
    for v in s.find_all("video"):
        srcs = [v.get("src")] + [x.get("src") for x in v.find_all("source")]
        for x in filter(None, srcs):
            out.append(("video", urljoin(r.url, x), (v.get("poster") or "")[:80]))
    for i in s.find_all("img"):
        x = i.get("data-src") or i.get("src")
        if not x or x.startswith("data:") or re.search(r"(logo|icon|avatar|badge|shields\.io)", x, re.I): continue
        cap = i.find_parent("figure").find("figcaption").get_text(" ", strip=True)[:120] if i.find_parent("figure") and i.find_parent("figure").find("figcaption") else (i.get("alt") or "")[:120]
        out.append(("gif" if x.lower().split("?")[0].endswith(".gif") else "img", urljoin(r.url, x), cap))
    seen, uniq = set(), []
    for k, u, h in out:
        if u not in seen: seen.add(u); uniq.append((k, u, h))
    return uniq


def get_media(url, stem, caption="", page=""):
    stem = "web_" + re.sub(r"[^A-Za-z0-9_.-]+", "-", stem).strip("-")
    r = get(url)
    if not r: print(f"{url}: download failed"); return None
    ext = Path(urlparse(url).path).suffix.lower()
    ctype = r.headers.get("content-type", "")
    if ext in VIDEO or ctype.startswith("video/") or ext == ".gif" or "gif" in ctype:
        if len(r.content) > 25e6: print(f"{url}: {len(r.content)/1e6:.0f} MB, too big -- pick a smaller asset"); return None
        ext = ext if ext in VIDEO + (".gif",) else (".gif" if "gif" in ctype else ".mp4")
        for old in FIG.glob(f"{stem}.*"): old.unlink()
        (FIG / f"{stem}{ext}").write_bytes(r.content); name = f"{stem}{ext}"
    else:
        name = save_img(r.content, stem)
    caps = load_caps(); caps[stem] = {"caption": caption, "src": url, "page": page}; save_caps(caps)
    print(f"  {name}  <- {url}")
    return name


# ---------- restore (figures/ is never committed; captions.json records how to rebuild each file) ----------

def restore(stems=None):
    """Re-create missing figure files from their recorded provenance (HTML/PDF pull, manual crop box, web URL).
    Default: every stem used by analysis.json and deck.json."""
    caps = load_caps(); d = FIG.parent
    if not stems:
        stems = set()
        if (d / "analysis.json").exists():
            a = json.loads((d / "analysis.json").read_text())
            stems |= {s for t in a.get("themes", []) for p in t.get("papers", []) for s in p.get("figs", []) + p.get("media", [])}
        if (d / "deck.json").exists():
            stems |= {s["fig"] for sec in json.loads((d / "deck.json").read_text())["sections"] for s in sec["slides"]}
    missing = sorted(s for s in stems if not any(FIG.glob(s + ".*")))
    print(f"restore: {len(stems)} stems, {len(missing)} missing")
    failed = []
    for s in missing:
        src = str(caps.get(s, {}).get("src", ""))
        m = re.match(r"pdf p(\d+) manual \[([^\]]+)\]", src)
        try:
            if s.startswith("web_"):
                get_media(src, s[4:], caps[s].get("caption", ""), caps[s].get("page", ""))
            elif m:
                aid, stem = s.split("_", 1)
                manual_crop(aid, stem, int(m[1]), [float(v) for v in m[2].split(",")])
            else:
                aid, loc = s.split("_", 1)
                pull(aid, {int(re.search(r"F(\d+)", loc)[1])})
        except Exception as e:
            print(f"  {s}: {e}")
        if not any(FIG.glob(s + ".*")): failed.append(s)
    save_caps({**caps, **load_caps()})
    print(f"restore: {len(missing) - len(failed)} rebuilt, {len(failed)} failed" + (": " + " ".join(failed) if failed else ""))
    return failed


# ---------- QA ----------

def qa(stems=None):
    """Flag crops that usually look bad on a 1920x1080 slide. Heuristics only -- always look at the image."""
    caps = load_caps(); flagged = 0
    files = sorted(p for p in FIG.iterdir() if p.suffix in (".jpg", ".png") and not p.name.startswith("."))
    for p in files:
        if stems and p.stem not in stems: continue
        im = Image.open(p); w, h = im.size; notes = []
        if w < 600: notes.append(f"small ({w}px wide)")
        if h > 1.6 * w: notes.append(f"portrait {w}x{h} -- tiny on a 16:9 slide")
        if w > 4.5 * h: notes.append(f"strip {w}x{h} -- too wide to read")
        g = im.convert("L").resize((min(400, w), max(1, round(min(400, w) * h / w))))
        dark = sum(g.histogram()[:110]) / (g.width * g.height)
        if dark > 0.55: notes.append("mostly dark -- white frame will look odd")
        c = caps.get(p.stem, {})
        if not c.get("caption"): notes.append("no caption")
        if "pdf" in str(c.get("src", "")) and "manual" not in str(c.get("src", "")): notes.append("auto PDF crop -- check for body text / cut labels")
        if c.get("n_subimages", 0) > 3: notes.append(f"{c['n_subimages']} sub-images in HTML, only the first was saved -- may be partial")
        if notes: flagged += 1; print(f"{p.name}: " + "; ".join(notes))
    print(f"qa: {flagged} flagged of {len(files)}")


if __name__ == "__main__":
    if len(sys.argv) < 3: raise SystemExit(__doc__)
    cmd, d, args = sys.argv[1], stream_dir(sys.argv[2]), sys.argv[3:]
    setup(d)
    if cmd == "pull":
        only = {}
        if args and args[0] == "--only":
            for spec in args[1:]:
                a, fs = spec.split(":"); only[a] = {int(x.strip("F")) for x in fs.split(",")}
            args = list(only)
        for a in args:
            try: pull(a, only.get(a))
            except Exception as e: print(f"{a}: ERROR {e}")
            time.sleep(2)
    elif cmd == "crop":
        for spec in args:
            aid, stem, page, box = spec.split(":")
            manual_crop(aid, stem, int(page), [float(v) for v in box.split(",")])
    elif cmd == "page":
        for u in args:
            for k, url, h in page_media(u): print(f"{k:8} {url}  {h}")
    elif cmd == "get":
        cap = page = ""
        if "--caption" in args: i = args.index("--caption"); cap = args[i + 1]; del args[i:i + 2]
        if "--from" in args: i = args.index("--from"); page = args[i + 1]; del args[i:i + 2]
        get_media(args[0], args[1], cap, page)
    elif cmd == "restore":
        sys.exit(1 if restore(set(args) or None) else 0)
    elif cmd == "qa":
        qa(set(args) or None)
    else:
        raise SystemExit(__doc__)
