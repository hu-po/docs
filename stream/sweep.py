#!/usr/bin/env python3
"""Data phase: sweep open sources into <stream>/ledger.jsonl.

  stream/py sweep.py <stream-dir> [--end 2026-09-24] [--days 7] [--lookback 21] [--ancestors 60]

Tiers (the `role` field):
  week      in the main window (last --days days of HF daily papers, dair-ai weeks overlapping it,
            EmergentMind / alphaXiv trending right now, plus anything in <stream>/inbox.md)
  recent    top-upvoted HF papers from the --lookback days before the window (context, follow-ups)
  ancestor  older papers cited by several of this week's top papers (Semantic Scholar references) --
            the historical threads that tie the week into larger themes
Every row is resolved against the arXiv API; ids arXiv doesn't know are dropped and logged.
Reddit and X are not swept (blocked / login-walled); Hugo drops links from there into inbox.md.
"""
import argparse, datetime as dt, json, math, re, sys, time
from collections import Counter, defaultdict
import requests
from common import UA, ARXIV_ID, get, arxiv_meta, read_jsonl, write_jsonl, stream_dir
from index import covered, index as rebuild_index

MONTHS = {m: i for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August",
                                      "September", "October", "November", "December"], 1)}


def hf_day(day):
    r = get(f"https://huggingface.co/api/daily_papers?date={day.isoformat()}")
    out = []
    for it in (r.json() if r else []):
        p = it.get("paper", {})
        if not p.get("id"): continue
        out.append(dict(id=p["id"], hf_upvotes=p.get("upvotes", 0), hf_comments=it.get("numComments", 0),
                        hf_date=day.isoformat(), github=p.get("githubRepo") or "", project=p.get("projectPage") or "",
                        github_stars=p.get("githubStars"), hf_summary=p.get("ai_summary") or "",
                        org=(it.get("organization") or {}).get("fullname", "")))
    return out


def dair(start, end):
    """dair-ai weekly picks whose week overlaps [start, end] -> {id: 'Sep 14-20 #2 Name'}"""
    r = get("https://raw.githubusercontent.com/dair-ai/ML-Papers-of-the-Week/main/years/%d.md" % end.year)
    out = {}
    if not r: return out
    for sec in re.split(r"^## ", r.text, flags=re.M)[1:]:
        m = re.match(r"Top AI Papers of the Week \((\w+) (\d+) - (\w+) (\d+)\)", sec)
        if not m or m[1] not in MONTHS or m[3] not in MONTHS: continue
        a = dt.date(end.year, MONTHS[m[1]], int(m[2])); b = dt.date(end.year, MONTHS[m[3]], int(m[4]))
        if b < start or a > end: continue
        for row in sec.splitlines():
            rm = re.match(r"\|\s*(\d+)\)\s*\*\*(.+?)\*\*", row)
            if not rm: continue
            for aid in dict.fromkeys(ARXIV_ID.findall(row)):
                out.setdefault(aid, f"{m[1][:3]} {m[2]}-{m[4]} #{rm[1]} {rm[2]}")
    return out


def page_ids(url, pat=r"/(?:papers|abs)/(\d{4}\.\d{4,5})"):
    r = get(url)
    return list(dict.fromkeys(re.findall(pat, r.text))) if r else []


def inbox(d):
    p = d / "inbox.md"
    return list(dict.fromkeys(ARXIV_ID.findall(p.read_text()))) if p.exists() else []


def s2_refs(ids):
    """Semantic Scholar batch -> {id: [(ref arxiv id, title, year, citationCount)]}. Unauthenticated, rate limited."""
    out = {}
    for i in range(0, len(ids), 100):
        chunk = ids[i:i + 100]
        for t in range(5):
            try:
                r = requests.post("https://api.semanticscholar.org/graph/v1/paper/batch",
                                  params={"fields": "references.externalIds,references.title,references.year,references.citationCount"},
                                  json={"ids": [f"arXiv:{a}" for a in chunk]}, headers=UA, timeout=90)
            except requests.RequestException: r = None
            if r is not None and r.status_code == 200: break
            time.sleep(8 * (t + 1))
        else:
            print("  ! semantic scholar unavailable; no ancestors", file=sys.stderr); return out
        for aid, p in zip(chunk, r.json()):
            refs = []
            for ref in (p or {}).get("references") or []:
                ra = (ref.get("externalIds") or {}).get("ArXiv")
                if ra: refs.append((ra, ref.get("title"), ref.get("year"), ref.get("citationCount")))
            out[aid] = refs
        time.sleep(3)
    return out


def score(sig):
    s = 10 * math.log10(1 + (sig.get("hf_upvotes") or 0)) + 2 * math.log10(1 + (sig.get("hf_comments") or 0))
    s += 8 * bool(sig.get("dair")) + 5 * bool(sig.get("emergentmind")) + 5 * bool(sig.get("alphaxiv"))
    s += 25 * bool(sig.get("inbox")) + 3 * len(sig.get("cited_by_week", []))
    return round(s, 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir"); ap.add_argument("--end", default=dt.date.today().isoformat())
    ap.add_argument("--days", type=int, default=7); ap.add_argument("--lookback", type=int, default=21)
    ap.add_argument("--ancestors", type=int, default=60, help="how many top week papers to mine references from (0 = skip)")
    ap.add_argument("--min-cited", type=int, default=3)
    a = ap.parse_args()
    d = stream_dir(a.dir)
    end = dt.date.fromisoformat(a.end); start = end - dt.timedelta(days=a.days - 1)
    old_start = start - dt.timedelta(days=a.lookback)
    print(f"window {start} .. {end}   lookback from {old_start}")

    sig = defaultdict(dict); role = {}; links = defaultdict(dict); extra = defaultdict(dict)

    def hf_row(x, r):
        s = sig[x["id"]]
        s["hf_upvotes"] = max(s.get("hf_upvotes", 0), x["hf_upvotes"]); s["hf_comments"] = x["hf_comments"]
        s["hf_date"] = x["hf_date"]; role.setdefault(x["id"], r)
        links[x["id"]].update({k: x[k] for k in ("github", "project") if x[k]})
        extra[x["id"]].update({k: x[k] for k in ("hf_summary", "org", "github_stars") if x[k]})

    day = start
    while day <= end:
        rows = hf_day(day); print(f"  hf {day}: {len(rows)}")
        for x in rows: hf_row(x, "week")
        day += dt.timedelta(days=1)
    day = old_start
    while day < start:
        rows = sorted(hf_day(day), key=lambda x: -x["hf_upvotes"])[:5]   # only the day's head
        for x in rows: hf_row(x, "recent")
        day += dt.timedelta(days=1)
    for aid, v in dair(start - dt.timedelta(days=6), end).items(): sig[aid]["dair"] = v; role.setdefault(aid, "week")
    for aid in page_ids("https://www.emergentmind.com/"): sig[aid]["emergentmind"] = True; role.setdefault(aid, "week")
    for aid in page_ids("https://www.alphaxiv.org/", r"(?<![\d.])([0-2]\d(?:0[1-9]|1[0-2])\.\d{5})(?![\d])")[:60]: sig[aid]["alphaxiv"] = True; role.setdefault(aid, "week")
    for aid in inbox(d): sig[aid]["inbox"] = True; role[aid] = "week"
    print(f"  dair {sum('dair' in s for s in sig.values())}  emergentmind {sum('emergentmind' in s for s in sig.values())}  "
          f"alphaxiv {sum('alphaxiv' in s for s in sig.values())}  inbox {sum('inbox' in s for s in sig.values())}")

    # ancestors: older arXiv papers the week's top papers keep citing
    week = sorted((x for x in role if role[x] == "week"), key=lambda x: -score(sig[x]))
    if a.ancestors:
        refs = s2_refs(week[:a.ancestors])
        cnt, info = Counter(), {}
        for src, rs in refs.items():
            for ra, t, y, c in rs:
                if ra in role: continue
                cnt[ra] += 1; info[ra] = (t, y, c); sig[ra].setdefault("cited_by_week", []).append(src)
        anc = [x for x, n in cnt.most_common(40) if n >= a.min_cited]
        for x in anc: role[x] = "ancestor"; sig[x]["s2_citations"] = info[x][2]
        for x in list(sig):
            if x not in role: del sig[x]
        print(f"  ancestors: {len(anc)} cited by >= {a.min_cited} of the top {len(refs)}")

    meta = arxiv_meta(list(role))
    missing = [x for x in role if x not in meta]
    if missing: print(f"  ! arXiv API did not resolve {len(missing)}: {' '.join(missing[:20])}")
    rebuild_index(); cov = covered()
    rows = []
    for x in role:
        if x not in meta: continue
        m = meta[x]
        rows.append(dict(id=x, role=role[x], score=score(sig[x]), title=m["title"], first_author=m["first_author"],
                         n_authors=len(m["authors"]), authors=m["authors"][:8], published=m["published"],
                         categories=m["categories"][:4], signals=sig[x],
                         links=dict(abs=f"https://arxiv.org/abs/{x}", hf=f"https://huggingface.co/papers/{x}", **links[x]),
                         covered_in=[f for f in cov.get(x, []) if f != d.name], abstract=m["abstract"], **extra[x]))
    have = {r["id"] for r in rows}   # keep rows deck.py added, and ancestors an earlier sweep found (S2 is flaky)
    rows += [r for r in read_jsonl(d / "ledger.jsonl") if r.get("role") in ("added", "ancestor") and r["id"] not in have]
    order = {"week": 0, "recent": 1, "ancestor": 2, "added": 3}
    rows.sort(key=lambda r: (order[r["role"]], -r["score"]))
    write_jsonl(d / "ledger.jsonl", rows)
    (d / "sweep.json").write_text(json.dumps(dict(run=dt.datetime.now().isoformat(timespec="minutes"), start=str(start),
        end=str(end), lookback_from=str(old_start), counts=Counter(r["role"] for r in rows), unresolved=missing), indent=1))
    c = Counter(r["role"] for r in rows)
    print(f"ledger.jsonl: {len(rows)} rows  week {c['week']} · recent {c['recent']} · ancestor {c['ancestor']}  "
          f"({sum(bool(r['covered_in']) for r in rows)} already covered on a past stream)")


if __name__ == "__main__":
    main()
