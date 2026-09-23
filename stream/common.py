"""Shared helpers for the stream tools: HTTP, arXiv metadata, ledger I/O."""
import json, re, sys, time
import xml.etree.ElementTree as ET
from pathlib import Path
import requests

TOOLS = Path(__file__).resolve().parent          # <repo>/stream
REPO = TOOLS.parent
UA = {"User-Agent": "Mozilla/5.0 (hu-po stream research; github.com/hu-po/docs)"}
ARXIV_ID = re.compile(r"(?<![\d.])(\d{4}\.\d{4,5})(?:v\d+)?(?![\d])")


def get(url, tries=3, **kw):
    """GET with retries; returns Response or None (404 / persistent failure)."""
    for i in range(tries):
        try:
            r = requests.get(url, headers=UA, timeout=60, **kw)
        except requests.RequestException as e:
            print(f"  ! {url}: {e}", file=sys.stderr); time.sleep(3 * (i + 1)); continue
        if r.status_code == 200: return r
        if r.status_code == 404: return None
        time.sleep(4 * (i + 1))
    print(f"  ! {url}: gave up", file=sys.stderr)
    return None


def arxiv_meta(ids):
    """Resolve arXiv ids against the arXiv API. -> {id: {title, authors, first_author, published, updated,
    categories, abstract}}. Ids the API does not know are absent from the result."""
    out, ids = {}, list(dict.fromkeys(ids))
    ns = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
    for i in range(0, len(ids), 50):
        chunk = ids[i:i + 50]
        r = get("https://export.arxiv.org/api/query", params={"id_list": ",".join(chunk), "max_results": len(chunk)})
        if not r: continue
        for e in ET.fromstring(r.content).findall("a:entry", ns):
            m = ARXIV_ID.search(e.findtext("a:id", "", ns)) or re.search(r"abs/(.+?)(v\d+)?$", e.findtext("a:id", "", ns))
            if not m or not e.findtext("a:title", "", ns).strip(): continue
            aid = m.group(1)
            authors = [a.findtext("a:name", "", ns) for a in e.findall("a:author", ns)]
            out[aid] = dict(
                title=" ".join(e.findtext("a:title", "", ns).split()),
                authors=authors,
                first_author=authors[0].split()[-1] if authors else "",
                published=e.findtext("a:published", "", ns)[:10],
                updated=e.findtext("a:updated", "", ns)[:10],
                categories=[c.get("term") for c in e.findall("a:category", ns)],
                abstract=" ".join(e.findtext("a:summary", "", ns).split()),
            )
        time.sleep(3)   # arXiv API etiquette
    return out


def read_jsonl(p):
    p = Path(p)
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def write_jsonl(p, rows):
    Path(p).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))


def stream_dir(arg):
    d = Path(arg).resolve()
    if not d.is_dir(): raise SystemExit(f"not a directory: {d}")
    return d
