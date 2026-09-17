# autoresearch — Recursive Self-Improvement stream deck

You are running one **round** of an autonomous research-and-edit loop on a slide deck for a live
YouTube stream. The stream is **Friday 2026-09-18, 9am CDT**. Hugo (hu-po) talks over the slides live
with a voice agent; the deck is figures from papers, not a script. You run unattended. Do the round,
log it, commit, exit. The next invocation reads your log and continues.

## Where things are

Working directory: `/home/ook/docs-2026.09.18.recursive_self_improvement/2026.09.18.recursive_self_improvement/`
(a git worktree on branch `2026.09.18.recursive_self_improvement`; never push, never touch `~/docs`).

| file | role |
|---|---|
| `iterations.md` | **Read first.** Round log + "Story status". Tells you which round you are and what's been tried. |
| `research.md` | The original arc and ranked candidate-paper list. A menu, not a mandate. |
| `deck.py` | `PAPERS` + `SECTIONS` lists drive everything. `python3 deck.py` rebuilds `slides.html` and the README refs. Do not edit the chrome (HEAD/TAIL strings). |
| `pull_figures.py` | `.venv/bin/python pull_figures.py <arxiv-id> …` → `figures/<id>_S<sec>-F<n>.jpg` + `figures/captions.json`. `--only id:F3,F4` for specific figures. `--crop id:S5-F6:<page>:<x0,y0,x1,y1>` (PDF points) when a PDF crop grabbed stray text. |
| `figures/` | 370+ figures already pulled (gitignored). Check `captions.json` before pulling again. |
| `slides.html` | The deliverable. Served on `localhost:8765`; Hugo may be looking at it — never leave it broken. |
| `thumbnail.jpg` | Title slide. Made by Hugo. Don't regenerate. |

## The deck's rules (Hugo's, from last week — non-negotiable)

- **Figures, not text.** A slide is one figure in a white frame, one factual context line, one cite line.
- **No commentary.** The context line says what is shown and what the axes/parts mean, derived from the
  authors' own caption. No "notice that", no opinions, no takeaways, no timecodes. Hugo supplies the
  understanding live; he wants to learn alongside the audience, not read a speech.
- **Every figure must be legible on its own.** If it needs the paper to make sense, it goes.
- **Story order, not paper order.** Sections are themes. A paper can appear in three sections or once.
- **Size:** 50–60 slides at the end, 66 absolute max. 7–9 sections.
- **Verify everything.** Fetch the arXiv abs page for every id before citing it. Never cite from memory.
  Dates and first authors in `PAPERS` come from the abs page.

## The story (current; you may improve it)

Dream-RSI (arXiv:2609.14858, Google, Sept 14) is the anchor. Hinge: it is Dreamer where the
environment is the discovery tree — last week's stream was world models, so section 05 is a callback.
Close on the tension: only the exploration *scheduler* learns (weights, evaluator, agent frozen);
replay is offline evaluation on logged trees and can't credit branches nobody opened; NeoHorse-1
(same week, "RSI" via post-training) is the foil. See `iterations.md` → Story status for open questions.

## One round

1. **Orient.** Read `iterations.md` fully. Note round number N (= last round + 1), slide count, what
   previous rounds added/removed/rejected, and open story questions. Run `python3 deck.py` once to
   confirm the build is green before you touch anything.
2. **Research.** Find 3–6 candidate papers/figures *not already in `deck.py`* that would strengthen a
   specific section or answer an open story question. Sources: arXiv search/listing, HF daily papers,
   Semantic Scholar, the bibliographies of papers already in the deck (Dream-RSI's related-work section
   is dense). Topics: recursive self-improvement, LLM discovery loops (AlphaEvolve lineage), exploration
   / search-policy optimization, world models of search, off-policy / offline evaluation, self-play
   from zero data, harness/skill/environment evolution. Also re-check `github.com/zhengkid/Dream-RSI`
   and `dream-rsi.com` — if code or new figures landed, that's the priority add.
   Prefer: Figure 1 / overview figures, result curves with clear axes, and figures that visually
   contrast with a neighbor slide. Avoid: tables of numbers, dense ablation grids, anything needing
   >2 sentences to decode.
3. **Pull and inspect.** `pull_figures.py` the chosen ids, then actually look at each crop (open the
   jpg). PDF-derived crops sometimes include body text or cut axis labels — fix with `--crop` or pick
   a different figure. Don't add a figure you haven't looked at.
4. **Edit `deck.py`.** Add 2–3 figure slides. Optionally remove 1 that fails the legibility rule.
   Write the context line from the caption (1–2 sentences, plain, factual). Add the paper to `PAPERS`
   with verified short name / first author / date / title.
5. **Let the story breathe.** If the research suggests a better arc — a section that should split,
   two that should merge, a stronger opener or closer, a better blurb — make the change and write
   *why* under Story status. Don't churn: no structural change without a reason you can state in one
   sentence. Keep the callback to world models and the NeoHorse-1 foil unless you find something
   better and say so.
6. **Build and check.** `python3 deck.py`. Confirm the printed slide count, that every referenced
   figure exists (`deck.py` exits with "missing figure" otherwise), and `grep -c '<section' slides.html`
   matches. Eyeball one new slide's HTML.
7. **Log.** Append to `iterations.md`:
   ```
   ## Round N — <date time>
   + <id> F<n> (<section>): <why>
   − <id> F<n>: <why>            (if any)
   Story: <changes, or "unchanged">
   Rejected: <candidates you looked at and didn't use, one line each — saves the next round time>
   Seed question: <1 question for the voice-agent back-and-forth, if the new material suggests one>
   Slides: <total> · Sections: <n> · Papers: <n>
   ```
   Update the Story status block (don't just append to it — keep it current).
8. **Commit.** `git add README.md slides.html deck.py pull_figures.py research.md iterations.md thumbnail.jpg`
   then `git commit -m "RSI deck round N: +<k> −<j>"`. Never `git add figures/` or `.venv/`. Never push.
9. **Exit.** Print a 3-line summary. Do not start another round.

## Stop conditions

- Round 12 done, or the deck is ≥ 60 slides: do a **polish round** instead of an add round — reorder
  within sections for flow, tighten context lines, fix any crop you flagged earlier, verify all refs —
  then write `DONE` as the last line of `iterations.md` and exit. If `DONE` is already there, exit
  immediately without changes.
- If `python3 deck.py` fails and you can't fix it in 10 minutes, `git checkout -- deck.py`, log the
  failure in `iterations.md`, and exit. A broken deck is worse than a missed round.
- If arXiv or the network is down, log it and exit; don't invent content.

## Don'ts

- Don't edit `thumbnail.jpg`, `research.md` (append-only if at all), or anything outside this folder.
- Don't add text-only slides, quote slides, or "summary" slides.
- Don't reword existing context lines unless they are wrong or violate the rules above.
- Don't spend the round re-reading Dream-RSI; it's already well covered. Spend it on what's missing.
