#!/usr/bin/env python3
"""The review gate: a local page where Hugo stars / vetoes before any deck is built.

  stream/py review.py build <stream-dir>              # writes <stream>/review.html (gitignored)
  stream/py review.py serve <stream-dir> [--port 8767] # serves the folder on 127.0.0.1, saves picks.json

Reads ledger.jsonl + analysis.json + figures/captions.json (+ picks.json to restore earlier choices).
The Save button POSTs to /picks, which writes <stream>/picks.json (gitignored); "Save & start deck" also starts
the deck rounds and thumbnail prompts. Bound to 127.0.0.1 only; never published.
"""
import datetime as dt, html, json, sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from common import TOOLS, read_jsonl, stream_dir

PAGE = r"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Review · __TITLE__</title>
<style>
:root{--bg:#0B0E0F;--panel:#141A1B;--panel2:#1A2223;--ink:#E9EFED;--muted:#93A29E;--faint:#63736F;--rule:#243030;
--live:#56E0BE;--star:#F2C14E;--veto:#E5646E;--mono:ui-monospace,"SF Mono","DejaVu Sans Mono",Menlo,monospace;
--sans:"Helvetica Neue",Helvetica,Arial,system-ui,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.45 var(--sans)}
a{color:var(--live)}header{position:sticky;top:0;z-index:5;background:rgba(11,14,15,.96);border-bottom:1px solid var(--rule);
padding:12px 20px;display:flex;gap:16px;align-items:center;flex-wrap:wrap}
header h1{font-size:17px;margin:0;font-weight:600}header .meta{font:12px var(--mono);color:var(--faint)}
header .grow{flex:1}#status{font:12px var(--mono);color:var(--muted)}
button{font:inherit;cursor:pointer}.save.alt{background:var(--panel2);color:var(--ink);border:1px solid var(--rule)}.save{background:var(--live);color:#062019;border:0;padding:7px 16px;font-weight:700;border-radius:3px}
main{max-width:1280px;margin:0 auto;padding:20px}
.block{background:var(--panel);border:1px solid var(--rule);border-radius:4px;padding:16px 18px;margin:0 0 18px}
h2{font-size:22px;margin:0 0 6px}h3{font:12px var(--mono);letter-spacing:.14em;color:var(--live);margin:0 0 10px;text-transform:uppercase}
.why{color:var(--muted);margin:0 0 12px;max-width:900px}
.titles label{display:block;padding:5px 0}.titles small{color:var(--faint);margin-left:8px}
.titles input[type=text]{background:var(--panel2);border:1px solid var(--rule);color:var(--ink);padding:5px 8px;width:420px;max-width:100%}
.theme{border-left:3px solid var(--rule)}.theme.v1{border-left-color:var(--star)}.theme.v-1{border-left-color:var(--veto);opacity:.55}
.thead{display:flex;gap:12px;align-items:flex-start;justify-content:space-between;flex-wrap:wrap}
.vote{display:inline-flex;gap:4px}.vote button{background:var(--panel2);border:1px solid var(--rule);color:var(--muted);
padding:3px 10px;border-radius:3px}.vote button.on.s{background:var(--star);color:#241a00;border-color:var(--star)}
.vote button.on.x{background:var(--veto);color:#2a0508;border-color:var(--veto)}
.paper{display:grid;grid-template-columns:1fr;gap:6px;padding:12px 0;border-top:1px solid var(--rule)}
.paper.v-1{opacity:.4}.paper.v1 .ptitle{color:var(--star)}
.prow{display:flex;gap:12px;justify-content:space-between;align-items:flex-start;flex-wrap:wrap}
.ptitle{font-weight:600;font-size:16px}.pmeta{font:12px var(--mono);color:var(--faint)}
.badges{display:flex;gap:6px;flex-wrap:wrap}.b{font:11px var(--mono);padding:1px 6px;border:1px solid var(--rule);border-radius:10px;color:var(--muted)}
.b.hot{color:var(--star);border-color:#5a4a1e}.b.cov{color:var(--veto);border-color:#5a2a2e}.b.anc{color:#9fb7ff;border-color:#2e3a5a}
.pwhy{color:var(--ink)}.figs{display:flex;gap:8px;overflow-x:auto;padding:4px 0}
.figs figure{margin:0;flex:0 0 auto;width:220px;cursor:pointer;border:2px solid transparent;border-radius:3px;background:#fff}
.figs figure.pick{border-color:var(--live)}.figs img,.figs video{width:100%;height:140px;object-fit:contain;display:block}
.figs figcaption{font:10px var(--mono);color:#555;padding:2px 4px;background:#eee}
details{color:var(--muted)}summary{cursor:pointer;font-size:13px}textarea,.note{width:100%;background:var(--panel2);border:1px solid var(--rule);
color:var(--ink);padding:6px 8px;font:13px var(--sans);border-radius:3px}
.note{height:30px}#lb{position:fixed;inset:0;background:rgba(0,0,0,.92);display:none;z-index:9;align-items:center;justify-content:center;padding:30px}
#lb.on{display:flex}#lb img,#lb video{max-width:100%;max-height:82vh;background:#fff}#lb p{position:fixed;bottom:12px;left:20px;right:20px;color:var(--ink);font-size:14px}
table{width:100%;border-collapse:collapse;font-size:13px}td{padding:5px 6px;border-top:1px solid var(--rule);vertical-align:top}
td.n{font:12px var(--mono);color:var(--faint);white-space:nowrap}
@media (max-width:700px){main{padding:12px}.figs figure{width:160px}}
</style></head><body>
<header><h1>__TITLE__</h1><span class="meta">__META__</span><span class="grow"></span><span id="status"></span>
<button class="save alt" id="save">Save picks</button><button class="save" id="go" title="save, then run the deck rounds and thumbnail prompts unattended">Save &amp; start deck</button></header>
<main id="app"></main><div id="lb"></div>
<script>
const D=__DATA__;
const P=Object.assign({title:"",themes:{},papers:{},notes:""},D.picks||{});
const L=Object.fromEntries(D.ledger.map(r=>[r.id,r]));
const $=(t,a={},...c)=>{const e=document.createElement(t);for(const[k,v]of Object.entries(a)){if(k==="on")for(const[ev,f]of Object.entries(v))e.addEventListener(ev,f);else if(k==="html")e.innerHTML=v;else e.setAttribute(k,v);}for(const x of c.flat())if(x!=null)e.append(x.nodeType?x:document.createTextNode(x));return e;};
let dirty=false;const mark=()=>{dirty=true;st("unsaved changes");};const st=t=>document.getElementById("status").textContent=t;
function vote(obj,key,el){const cur=(obj[key]||{}).vote||0;const w=$("span",{class:"vote"});
 const mk=(v,cls,label)=>$("button",{class:cls+(cur===v?" on":""),title:v>0?"star":"veto",on:{click:()=>{obj[key]=obj[key]||{};obj[key].vote=obj[key].vote===v?0:v;mark();render();}}},label);
 w.append(mk(1,"s","★"),mk(-1,"x","✕"));return w;}
function fig(stem){const c=D.captions[stem]||{};return c;}
function media(stem,big){const f=D.files[stem];if(!f)return $("div",{class:"pmeta"},"missing "+stem);
 if(!/\.(mp4|webm|mov)$/.test(f))return $("img",{src:"figures/"+f,loading:"lazy",alt:stem});
 // the muted attribute does not mute a script-created video; only the property does
 const v=$("video",{src:"figures/"+f,loop:"",autoplay:"",playsinline:"",preload:"metadata"});v.muted=true;if(big)v.controls=true;return v;}
function lightbox(stem){const lb=document.getElementById("lb");lb.innerHTML="";lb.append(media(stem,true),$("p",{},stem+" — "+(fig(stem).caption||"")));lb.classList.add("on");}
document.getElementById("lb").onclick=e=>{if(e.target.tagName==="VIDEO")return;const lb=e.currentTarget;lb.classList.remove("on");lb.innerHTML="";};
function badges(r){const s=r.signals||{},b=[];
 if(s.hf_upvotes)b.push($("span",{class:"b"+(s.hf_upvotes>=100?" hot":"")},"HF ▲"+s.hf_upvotes));
 if(s.dair)b.push($("span",{class:"b hot"},"dair "+s.dair.split(" ").slice(0,3).join(" ")));
 if(s.emergentmind)b.push($("span",{class:"b"},"EmergentMind"));if(s.alphaxiv)b.push($("span",{class:"b"},"alphaXiv"));
 if(s.inbox)b.push($("span",{class:"b hot"},"inbox"));if(r.role==="ancestor")b.push($("span",{class:"b anc"},"ancestor · cited by "+(s.cited_by_week||[]).length+" this week"));
 if(r.role==="recent")b.push($("span",{class:"b"},"recent"));
 for(const c of r.covered_in||[])b.push($("span",{class:"b cov"},"covered "+c.slice(0,10)));
 if(r.org)b.push($("span",{class:"b"},r.org));return $("div",{class:"badges"},b);}
function paper(p){const r=L[p.id]||{id:p.id,title:p.id,signals:{}};const pk=P.papers[p.id]||{};const v=pk.vote||0;
 const figs=[...(p.figs||[]),...(p.media||[])];
 const row=$("div",{class:"paper v"+v},
  $("div",{class:"prow"},$("div",{},$("div",{class:"ptitle"},r.title),
    $("div",{class:"pmeta"},`${p.id} · ${r.first_author||""}${r.n_authors>1?" et al.":""} · ${r.published||""} · score ${r.score??""}`)),vote(P.papers,p.id)),
  badges(r),p.why?$("div",{class:"pwhy"},p.why):null,
  figs.length?$("div",{class:"figs"},figs.map(st=>{const f=$("figure",{class:(pk.figs||[]).includes(st)?"pick":""},media(st),$("figcaption",{},st.replace(p.id+"_","")+"  ⤢"));
    f.onclick=e=>{if(e.target.tagName==="FIGCAPTION"){lightbox(st);return;}P.papers[p.id]=P.papers[p.id]||{};const a=P.papers[p.id].figs=P.papers[p.id].figs||[];
     const i=a.indexOf(st);i<0?a.push(st):a.splice(i,1);mark();render();};return f;})):null,
  $("details",{},$("summary",{},"abstract · links"),$("p",{},r.abstract||""),$("p",{},...Object.entries(r.links||{}).map(([k,u])=>[$("a",{href:u,target:"_blank"},k)," "]))),
  (()=>{const n=$("input",{class:"note",placeholder:"note (optional)",value:pk.note||""});n.oninput=()=>{P.papers[p.id]=P.papers[p.id]||{};P.papers[p.id].note=n.value;mark();};return n;})());
 return row;}
function render(){const app=document.getElementById("app");const y=scrollY;app.innerHTML="";const A=D.analysis;
 app.append($("div",{class:"block"},$("h3",{},"The week"),$("p",{class:"why",html:(A.summary||"").replace(/\n/g,"<br>")}),
  A.news&&A.news.length?$("div",{},$("h3",{},"News / launches (live segment, not slides)"),$("ul",{},A.news.map(n=>$("li",{},n.url?$("a",{href:n.url,target:"_blank"},n.what):n.what)))):null));
 const tc=$("div",{class:"block titles"},$("h3",{},"Title"));
 for(const t of A.title_candidates||[]){const i=$("input",{type:"radio",name:"t"});i.checked=P.title===t.title;i.onchange=()=>{P.title=t.title;mark();render();};
  tc.append($("label",{},i," "+t.title,$("small",{},t.why||"")));}
 const own=$("input",{type:"text",placeholder:"or write your own",value:(A.title_candidates||[]).some(t=>t.title===P.title)?"":P.title});
 own.oninput=()=>{P.title=own.value;mark();};tc.append($("label",{},"✎ ",own));app.append(tc);
 for(const t of A.themes||[]){const tv=(P.themes[t.id]||{}).vote||0;
  const b=$("div",{class:"block theme v"+tv},$("div",{class:"thead"},$("div",{},$("h2",{},t.name),$("p",{class:"why"},t.why||"")),vote(P.themes,t.id)));
  const extra=[...(t.ancestors||[]).map(a=>(L[a]?`${L[a].title} (${L[a].published.slice(0,4)})`:a)),...(t.callbacks||[]).map(c=>"callback: "+c)];
  if(extra.length)b.append($("p",{class:"pmeta"},"threads: "+extra.join(" · ")));
  const tn=$("input",{class:"note",placeholder:"theme note (optional)",value:(P.themes[t.id]||{}).note||""});tn.oninput=()=>{P.themes[t.id]=P.themes[t.id]||{};P.themes[t.id].note=tn.value;mark();};b.append(tn);
  for(const p of t.papers||[])b.append(paper(p));app.append(b);}
 const themed=new Set((A.themes||[]).flatMap(t=>(t.papers||[]).map(p=>p.id)));
 const rest=D.ledger.filter(r=>!themed.has(r.id)&&r.role!=="ancestor").slice(0,15);
 const tb=$("table",{},rest.map(r=>{const v=(P.papers[r.id]||{}).vote||0;return $("tr",{style:v<0?"opacity:.4":""},$("td",{class:"n"},r.score),$("td",{},$("a",{href:r.links.abs,target:"_blank"},r.title),$("div",{},badges(r))),$("td",{},vote(P.papers,r.id)));}));
 app.append($("div",{class:"block"},$("details",{},$("summary",{},"Not in a theme — top "+rest.length+" of the ledger (star to pull one in)"),tb)));
 const anc=D.ledger.filter(r=>r.role==="ancestor");
 if(anc.length)app.append($("div",{class:"block"},$("details",{},$("summary",{},anc.length+" ancestors — older papers this week keeps citing"),$("table",{},anc.map(r=>$("tr",{},$("td",{class:"n"},(r.signals.cited_by_week||[]).length+"×"),$("td",{},$("a",{href:r.links.abs,target:"_blank"},r.title),$("span",{class:"pmeta"}," "+r.published.slice(0,4))),$("td",{},vote(P.papers,r.id))))))));
 const nt=$("textarea",{rows:5,placeholder:"anything else for the deck agent: order, what to lead with, what to cut, a paper that's missing…"});nt.value=P.notes||"";nt.oninput=()=>{P.notes=nt.value;mark();};
 app.append($("div",{class:"block"},$("h3",{},"Notes"),nt));scrollTo(0,y);}
async function save(go){P.saved=new Date().toISOString();
 try{const r=await fetch("/picks"+(go?"?deck=1":""),{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(P,null,1)});
  if(!r.ok)throw new Error(r.status);dirty=false;st((go?(await r.text())+" · ":"")+"saved "+new Date().toLocaleTimeString());}
 catch(e){st("save failed ("+e.message+") — is review.py serve running?");}}
document.getElementById("save").onclick=()=>save(false);
document.getElementById("go").onclick=()=>{if(!P.title){st("pick a title first");return;}save(true);};
addEventListener("beforeunload",e=>{if(dirty){e.preventDefault();e.returnValue="";}});
render();st(D.picks?"loaded picks from "+(D.picks.saved||"picks.json"):"no picks yet");
</script></body></html>"""


def build(d):
    ledger = read_jsonl(d / "ledger.jsonl")
    ap = d / "analysis.json"
    if not ap.exists(): raise SystemExit("no analysis.json yet -- run the analyze phase first")
    analysis = json.loads(ap.read_text())
    caps = json.loads((d / "figures/captions.json").read_text()) if (d / "figures/captions.json").exists() else {}
    files = {p.stem: p.name for p in (d / "figures").glob("*") if not p.name.startswith(".") and p.suffix != ".json"} if (d / "figures").exists() else {}
    picks = json.loads((d / "picks.json").read_text()) if (d / "picks.json").exists() else None
    sweep = json.loads((d / "sweep.json").read_text()) if (d / "sweep.json").exists() else {}
    keep = {"id", "role", "score", "title", "first_author", "n_authors", "published", "signals", "links", "covered_in", "abstract", "org"}
    data = dict(ledger=[{k: v for k, v in r.items() if k in keep} for r in ledger], analysis=analysis,
                captions={k: {"caption": v.get("caption", "")} for k, v in caps.items()}, files=files, picks=picks)
    meta = f"window {sweep.get('start', '?')} → {sweep.get('end', '?')} · {len(ledger)} papers · {len(analysis.get('themes', []))} themes"
    out = (PAGE.replace("__TITLE__", html.escape(d.name)).replace("__META__", html.escape(meta))
           .replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/")))
    (d / "review.html").write_text(out)
    print(f"review.html: {len(analysis.get('themes', []))} themes, {sum(len(t.get('papers', [])) for t in analysis.get('themes', []))} themed papers")


def live(d):
    """The stream folder now. Deck round 1 renames <date>.untitled to <date>.<title> under a running server."""
    if d.is_dir(): return d
    return next((p for p in sorted(d.parent.glob(d.name[:10] + ".*")) if p.is_dir()), d)


def start_deck(d):
    """Kick off the deck rounds, then the thumbnail prompts, detached (stream/run.sh)."""
    import subprocess
    date = d.name.split(".untitled")[0][:10]
    lock = d / ".deck-running"
    if lock.exists(): return b"deck already running"
    lock.touch()
    log = open(d / "run.log", "a")
    subprocess.Popen(["bash", "-c", f'"$0" deck {date}; "$0" thumbnail {date}; rm -f "{d.parent}"/{date}.*/.deck-running', str(TOOLS / "run.sh")],
                     stdout=log, stderr=log, start_new_session=True, cwd=str(d.parent))
    print(f"[{dt.datetime.now():%H:%M:%S}] deck rounds started")
    return b"deck rounds started"


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, request, client, server):
        super().__init__(request, client, server, directory=str(live(server.stream)))

    def do_POST(self):
        if self.path.split("?")[0] != "/picks": self.send_error(404); return
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        try: picks = json.loads(body)
        except ValueError: self.send_error(400); return
        (live(self.server.stream) / "picks.json").write_text(json.dumps(picks, indent=1, ensure_ascii=False))
        print(f"[{dt.datetime.now():%H:%M:%S}] picks.json saved ({sum(1 for v in picks.get('papers', {}).values() if v.get('vote') == 1)} starred)")
        msg = b"ok"
        if "deck=1" in self.path:
            msg = start_deck(live(self.server.stream))
        self.send_response(200); self.end_headers(); self.wfile.write(msg)

    def log_message(self, *a): pass


if __name__ == "__main__":
    if len(sys.argv) < 3: raise SystemExit(__doc__)
    cmd, d = sys.argv[1], stream_dir(sys.argv[2])
    if cmd == "build": build(d)
    elif cmd == "serve":
        port = int(sys.argv[sys.argv.index("--port") + 1]) if "--port" in sys.argv else 8767
        build(d)
        srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
        srv.stream = d
        print(f"review: http://localhost:{port}/review.html")
        srv.serve_forever()
    else: raise SystemExit(__doc__)
