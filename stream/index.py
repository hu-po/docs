#!/usr/bin/env python3
"""Cross-week memory: index every stream folder in the repo.   stream/py index.py

Writes stream/index.jsonl, one row per stream: folder, date, title, youtube, x, and the arXiv ids the
stream covered (README references, plus deck.json slides when present). sweep.py uses it to mark
candidates that were already covered and the analysis phase uses it for callbacks.
"""
import json, re
from common import REPO, TOOLS, ARXIV_ID, write_jsonl

FOLDER = re.compile(r"^(\d{4})\.(\d{2})\.(\d{2})\.(.+)$")


def index():
    rows = []
    for d in sorted(REPO.iterdir()):
        m = FOLDER.match(d.name)
        if not d.is_dir() or not m or m[4] == "untitled": continue   # a stream still in prep
        rd = d / "README.md"
        t = rd.read_text(errors="ignore") if rd.exists() else ""
        title = (re.search(r"^# (.+)$", t, re.M) or [None, d.name])[1].strip()
        yt = re.search(r"https?://(?:www\.)?youtu[^\s)]+", t)
        x = re.search(r"https?://(?:x|twitter)\.com/[^\s)]+", t)
        ids = ARXIV_ID.findall(t)
        deck = d / "deck.json"
        if deck.exists():
            for s in (sl for sec in json.loads(deck.read_text()).get("sections", []) for sl in sec["slides"]):
                if s.get("paper"): ids.append(s["paper"])
        rows.append(dict(folder=d.name, date=f"{m[1]}-{m[2]}-{m[3]}", title=title,
                         youtube=yt.group(0) if yt else "", x=x.group(0) if x else "",
                         arxiv=list(dict.fromkeys(ids))))
    write_jsonl(TOOLS / "index.jsonl", rows)
    print(f"index.jsonl: {len(rows)} streams, {sum(len(r['arxiv']) for r in rows)} arXiv refs")


def covered():
    """{arxiv id: [folder, ...]} from index.jsonl."""
    from common import read_jsonl
    out = {}
    for r in read_jsonl(TOOLS / "index.jsonl"):
        for a in r["arxiv"]: out.setdefault(a, []).append(r["folder"])
    return out


if __name__ == "__main__":
    index()
