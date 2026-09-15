#!/usr/bin/env python3
"""Pull figures (+captions) for arXiv papers into figures/.

  python3 pull_figures.py 2609.14858 2506.13131 ...
  python3 pull_figures.py --only 2609.14858:F3,F4   # specific figure numbers
  python3 pull_figures.py --crop 2609.14858:S5-F6:11:298,208,536,674   # manual PDF crop (page, pts)

Files are named <id>_S<sec>-F<n>.<ext> (matches previous streams). Captions and
provenance go to figures/captions.json. Sources, in order: arxiv.org/html,
ar5iv, then a PDF crop (PyMuPDF) for figures the HTML has no bitmap for.
"""
import io, json, re, sys, time
from urllib.parse import urljoin
from pathlib import Path
import requests, fitz
from bs4 import BeautifulSoup
from PIL import Image

HERE = Path(__file__).resolve().parent
FIG = HERE / "figures"; FIG.mkdir(exist_ok=True)
CAP = FIG / "captions.json"
UA = {"User-Agent": "Mozilla/5.0 (hu-po stream deck; figure pull)"}
MAXW = 1800

def load_caps():
    return json.loads(CAP.read_text()) if CAP.exists() else {}

def save_caps(c):
    CAP.write_text(json.dumps(c, indent=1, ensure_ascii=False))

def get(url, **kw):
    for i in range(3):
        r = requests.get(url, headers=UA, timeout=60, **kw)
        if r.status_code == 200: return r
        if r.status_code == 404: return None
        time.sleep(3 * (i + 1))
    return None

def save_img(data, stem):
    im = Image.open(io.BytesIO(data))
    if im.mode in ("RGBA", "LA", "P"):
        bg = Image.new("RGB", im.size, "white"); bg.paste(im.convert("RGBA"), mask=im.convert("RGBA").split()[-1]); im = bg
    else:
        im = im.convert("RGB")
    if im.width > MAXW:
        im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
    out = FIG / f"{stem}.jpg"
    im.save(out, "JPEG", quality=88, optimize=True)
    return out.name

def html_figs(aid):
    """-> (base_url, [ (figid like S1.F1, img_src or None, caption) ]) or None"""
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
        rects = [fitz.Rect(d["rect"]) for d in page.get_drawings()]
        rects += [page.get_image_bbox(i) for i in page.get_images(full=True)]
        # things above the caption, roughly in the same column (or full width)
        cand = [r for r in rects if r.y1 <= cy0 + 2 and r.y0 >= cy0 - 520 and r.width > 8 and r.height > 3
                and (r.x1 > cx0 - 20 and r.x0 < cx1 + 20)]
        if cand:
            u = cand[0]
            for r in cand[1:]: u |= r
            # body-text paragraphs above the figure bound it from the top
            body = [b for b in blocks if not pat.match(b[4]) and b[3] <= u.y0 + 4 and b[1] >= u.y0 - 200
                    and len(b[4].strip()) > 120 and (b[3] - b[1]) > 28 and (b[2] > u.x0 and b[0] < u.x1)]
            if body:
                u.y0 = max(u.y0, max(b[3] for b in body) + 2)
            # pull in short labels (axis ticks, titles, legends) that sit on or beside the drawing
            for _ in range(2):
                grown = fitz.Rect(u.x0 - 28, u.y0 - 22, u.x1 + 28, u.y1 + 22)
                for b in blocks:
                    t = b[4].strip()
                    if pat.match(t) or len(t) > 120: continue
                    rb = fitz.Rect(b[:4])
                    if rb.intersects(grown) and rb.y1 <= cy0 + 2 and rb.y0 >= cy0 - 560:
                        u |= rb
            clip = fitz.Rect(max(0, u.x0 - 6), max(0, u.y0 - 6), min(pw, u.x1 + 6), min(cy0, u.y1 + 6))
        else:
            clip = fitz.Rect(cx0 - 10, max(0, cy0 - 320), cx1 + 10, cy0)
        pix = page.get_pixmap(matrix=fitz.Matrix(3, 3), clip=clip, alpha=False)
        return pix.tobytes("png"), page.number + 1
    return None, None

def pull(aid, only=None):
    caps = load_caps()
    fsid = aid.replace("/", "")   # old-style ids like cs/0309048
    got = []
    hf = html_figs(aid)
    doc = None
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
            if not name:
                doc = doc or pdf_doc(aid)
                if doc:
                    png, pg = pdf_crop(doc, n)
                    if png: name = save_img(png, stem); cap = cap or f"Figure {n}"; print(f"  {stem}: pdf crop p{pg}")
            if name:
                caps[stem] = {"caption": cap, "src": "html" if imgs else "pdf"}
                got.append(stem)
    else:
        doc = pdf_doc(aid)
        if not doc: print(f"{aid}: nothing"); return got
        for n in (only or range(1, 13)):
            stem = f"{fsid}_S0-F{n}"
            if any(FIG.glob(stem + ".*")): got.append(stem); continue
            png, pg = pdf_crop(doc, n)
            if not png:
                if not only: break
                continue
            name = save_img(png, stem)
            txt = "".join(p.get_text() for p in doc)
            m = re.search(rf"(Figure|Fig\.)\s*{n}\s*[|:.]\s*(.{{0,400}}?)(?:\n\s*\n|(?=\n\s*(Figure|Fig\.)\s*\d))", txt, re.S)
            caps[stem] = {"caption": " ".join(m.group(2).split()) if m else f"Figure {n}", "src": f"pdf p{pg}"}
            got.append(stem); print(f"  {stem}: pdf crop p{pg}")
    save_caps(caps)
    print(f"{aid}: {len(got)} figs -> {', '.join(got)}")
    return got

def manual_crop(aid, stem, page, box):
    doc = pdf_doc(aid); pg = doc[page - 1]
    pix = pg.get_pixmap(matrix=fitz.Matrix(3, 3), clip=fitz.Rect(*box), alpha=False)
    for old in FIG.glob(f"{aid}_{stem}.*"): old.unlink()
    name = save_img(pix.tobytes("png"), f"{aid}_{stem}")
    caps = load_caps(); e = caps.get(f"{aid}_{stem}", {}); e["src"] = f"pdf p{page} manual"; caps[f"{aid}_{stem}"] = e; save_caps(caps)
    print(f"  {aid}_{stem}: manual crop p{page} -> {name}")

if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--crop":
        for spec in args[1:]:
            aid, stem, page, box = spec.split(":")
            manual_crop(aid, stem, int(page), [float(v) for v in box.split(",")])
        sys.exit()
    only = {}
    if args and args[0] == "--only":
        for spec in args[1:]:
            a, fs = spec.split(":")
            only[a] = {int(x.strip("F")) for x in fs.split(",")}
        args = list(only)
    for a in args:
        try: pull(a, only.get(a))
        except Exception as e: print(f"{a}: ERROR {e}")
        time.sleep(2)
