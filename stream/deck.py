#!/usr/bin/env python3
"""Build <stream>/slides.html from <stream>/deck.json.   stream/py deck.py <stream-dir> [--check]

deck.json:
{
  "title": "Figure Review 002", "date": "2026.10.02",
  "names": {"2609.24972": "RRSI"},                  # optional short names (else: title before ':')
  "sections": [
    {"title": "...", "blurb": "one or two sentences",
     "slides": [
       {"fig": "2609.24972_S1-F1", "ctx": "one factual line from the authors' caption"},
       {"fig": "web_rrsi-demo", "ctx": "...", "cite": "Google Research · RRSI project page",
        "url": "https://regularized-rsi.com/", "paper": "2609.24972"}      # web media; paper optional
     ]}
  ]
}
The cite line of an arXiv figure is derived from ledger.jsonl (verified by sweep.py against the arXiv
API). An id used in the deck but missing from the ledger is resolved against the arXiv API now and
appended to the ledger with role "added" -- never typed in by hand. The references slide and the README
References list are regenerated from the slides actually in the deck.
"""
import html, json, re, sys
from pathlib import Path
from chrome import HEAD, TAIL_PRE, TAIL_POST
from common import ARXIV_ID, arxiv_meta, read_jsonl, write_jsonl, stream_dir

VIDEO = (".mp4", ".webm", ".mov")
# Play only the video on the visible slide (the frozen chrome toggles .on).
VIDEO_JS = """<script>(function(){var v=[].slice.call(document.querySelectorAll('.slide video'));if(!v.length)return;
function sync(){v.forEach(function(x){var on=x.closest('.slide').classList.contains('on');if(on&&x.paused){x.currentTime=0;x.play().catch(function(){});}if(!on&&!x.paused)x.pause();});}
new MutationObserver(sync).observe(document.getElementById('deck'),{attributes:true,subtree:true,attributeFilter:['class']});sync();})();</script>
"""


def esc(s): return html.escape(s, quote=False)


def main():
    d = stream_dir(sys.argv[1]); check = "--check" in sys.argv
    spec = json.loads((d / "deck.json").read_text())
    ledger = read_jsonl(d / "ledger.jsonl"); meta = {r["id"]: r for r in ledger}
    names = spec.get("names", {})
    errors = []

    def fig_file(stem):
        m = sorted(p for p in (d / "figures").glob(f"{stem}.*"))
        if not m: errors.append(f"missing figure: {stem}"); return None
        return f"figures/{m[0].name}"

    # resolve every arXiv id the deck touches
    ids = []
    for sec in spec["sections"]:
        for s in sec["slides"]:
            aid = s.get("paper") or (s["fig"].split("_")[0] if ARXIV_ID.fullmatch(s["fig"].split("_")[0]) else None)
            s["_paper"] = aid
            if aid and aid not in ids: ids.append(aid)
    new = [a for a in ids if a not in meta]
    if new:
        got = arxiv_meta(new)
        for a in new:
            if a not in got: errors.append(f"arXiv does not resolve {a}"); continue
            m = got[a]
            row = dict(id=a, role="added", score=0, title=m["title"], first_author=m["first_author"], n_authors=len(m["authors"]),
                       authors=m["authors"][:8], published=m["published"], categories=m["categories"][:4], signals={},
                       links=dict(abs=f"https://arxiv.org/abs/{a}"), covered_in=[], abstract=m["abstract"])
            ledger.append(row); meta[a] = row; print(f"  added to ledger from arXiv API: {a} {m['title'][:60]}")
        write_jsonl(d / "ledger.jsonl", ledger)

    def short(aid):
        if aid in names: return names[aid]
        t = meta[aid]["title"]
        return t.split(":")[0] if ":" in t and len(t.split(":")[0]) <= 32 else t[:48]

    title, date = spec["title"], spec["date"]
    slides, ov, used, web = [], [], [], []
    if (d / "thumbnail.jpg").exists():
        slides.append(f'<section class="slide title"><img src="thumbnail.jpg" alt="{esc(title)}"></section>')
        ov.append(('<img src="thumbnail.jpg" alt="" loading="lazy">', "Title"))
    else:
        slides.append(f'<section class="slide sec"><div class="secbody"><p class="num">hu-po &middot; {date}</p><h2>{esc(title)}</h2></div></section>')
        ov.append(('<span class="ovcard"></span>', "Title"))
    n = len(spec["sections"])
    for k, sec in enumerate(spec["sections"], 1):
        slides.append(f'<section class="slide sec"><div class="secbody"><p class="num">{k:02d} / {n:02d}</p>'
                      f'<h2>{esc(sec["title"])}</h2><p class="blurb">{esc(sec.get("blurb", ""))}</p></div></section>')
        ov.append(('<span class="ovcard"></span>', sec["title"]))
        for s in sec["slides"]:
            src = fig_file(s["fig"]); aid = s["_paper"]
            if not src: continue
            if not s.get("ctx"): errors.append(f"no ctx line: {s['fig']}")
            if s["fig"].startswith("web_"):
                if not s.get("cite"): errors.append(f"web figure needs a cite: {s['fig']}")
                cite = esc(s.get("cite", "")); label = s.get("cite", s["fig"]).split("·")[0].strip()
                if s.get("url") and s["url"] not in [w[0] for w in web]: web.append((s["url"], s.get("cite", "")))
            else:
                if aid not in meta: continue
                loc = s["fig"].split("_", 1)[1]; fn = re.search(r"F(\d+)", loc).group(1)
                kind = "Table" if loc.startswith("T") else "Fig."
                cite = f"{esc(meta[aid]['first_author'])} et al. &middot; {esc(short(aid))} &middot; {kind} {fn} &middot; arXiv:{aid}"
                label = f"{short(aid)} F{fn}"
            if aid and aid not in used: used.append(aid)
            dark = " dark" if s.get("dark") else ""
            if src.endswith(VIDEO):
                media = f'<video src="{src}" muted loop playsinline preload="metadata"></video>'
                thumb = '<span class="ovcard"></span>'
            else:
                media = f'<img src="{src}" alt="{esc(label)}">'
                thumb = f'<img src="{src}" alt="" loading="lazy">'
            slides.append(f'<section class="slide fig"><div class="frame{dark}">{media}</div>'
                          f'<p class="ctx">{s.get("ctx", "")}</p><p class="cite">{cite}</p></section>')
            ov.append((thumb, label))
    refs = [f'<div class="ref"><code>{a}</code><div class="t"><b>{esc(short(a))}</b>'
            f'<span>{esc(meta[a]["first_author"])} et al. &middot; {meta[a]["published"]}</span></div></div>' for a in used if a in meta]
    refs += [f'<div class="ref"><code>web</code><div class="t"><b>{esc(c.split("·")[0].strip() or u)}</b>'
             f'<span>{esc(re.sub(r"^https?://", "", u)[:48])}</span></div></div>' for u, c in web]
    for i in range(0, len(refs), 45):
        slides.append('<section class="slide refs"><div class="reflist">' + "".join(refs[i:i + 45]) + '</div></section>')
        ov.append(('<span class="ovcard"></span>', "References"))
    if errors:
        print("\n".join(errors)); raise SystemExit(f"deck.json has {len(errors)} problem(s); slides.html not written")
    nfig = sum(len(s["slides"]) for s in spec["sections"])
    print(f"slides: {len(slides)} total ({n} sections, {nfig} figure slides, {len(used)} papers, {len(web)} web sources)")
    if check: return
    ovh = '<div id="overview"><div class="ovgrid">' + "".join(
        f'<button class="ov" data-i="{i}">{img}<em>{i + 1}. {esc(lab)}</em></button>' for i, (img, lab) in enumerate(ov)) + '</div>'
    out = HEAD.replace("{TITLE}", esc(title)).replace("{DATE}", date) + "".join(slides) + TAIL_PRE + ovh + TAIL_POST
    (d / "slides.html").write_text(out.replace("</body>", VIDEO_JS + "</body>"))
    # README: title + references in sync with the deck
    rd = d / "README.md"
    if rd.exists():
        t = rd.read_text()
        t = re.sub(r"^# .*$", f"# {title}", t, count=1, flags=re.M)
        links = "\n".join([f"- https://arxiv.org/abs/{a}" for a in used] + [f"- {u}" for u, _ in web])
        t = re.sub(r"(### References\n)[\s\S]*$", lambda m: m.group(1) + "\n" + links + "\n", t)
        rd.write_text(t)


if __name__ == "__main__":
    main()
