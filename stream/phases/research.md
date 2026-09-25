# Phase: research (one round)

You are running one round of the **research loop** for the next hu-po stream. It runs unattended.
Do the round, log it, commit, and exit. The next invocation reads your log and continues.

- Stream folder: `{{DIR}}` (inside a git worktree on its own branch. Never push, and never touch `~/docs`).
- Tools: `{{TOOLS}}` (run them as `{{TOOLS}}/py <tool>.py ...`).
- Read `{{TOOLS}}/FORMAT.md` first. It defines the format and the deck rules.
- Read `{{DIR}}/log.md` next. It holds the round history and tells you which round you are on.
- Today is {{TODAY}}. The stream is on {{STREAM_DATE}}.

The goal of the research loop is `analysis.json` + `review.html`: the week's papers, scored and clustered
into themes, each with a best visual that you have actually looked at, ready for Hugo to star or veto.
**You do not choose a topic or title. You propose title candidates that come out of the themes.**

## Files you own

| file | what |
|---|---|
| `ledger.jsonl` | written by `sweep.py`. One row per paper: arXiv-verified metadata, signals, role (week / recent / ancestor), `covered_in` = past streams that already used it. Don't hand-edit it. |
| `inbox.md` | Links Hugo dropped in by hand (X, Reddit, anything). arXiv ids in it are swept automatically. Non-arXiv links are yours to read. |
| `analysis.json` | your output (schema below) |
| `analysis.md` | a readable companion: the week in 5 sentences, then each theme with its reasoning, the threads to older work, and what you left out and why |
| `figures/` | from `figures.py` (gitignored). Check `figures/captions.json` before pulling again. |
| `log.md` | the round log (append) |

`analysis.json` schema:
```json
{"summary": "3-6 sentences: what the week was about, from the data",
 "title_candidates": [{"title": "Figure Review 002: ...", "why": "one line"}],
 "themes": [{"id": "t1", "name": "short name", "why": "what ties these papers together, 1-2 sentences",
             "papers": [{"id": "2609.24972", "why": "one line: what this paper contributes to the theme",
                         "figs": ["2609.24972_S1-F1"], "media": ["web_rrsi-demo"]}],
             "ancestors": ["2210.03629"], "callbacks": ["2026.09.18.recursive_self_improvement"]}],
 "news": [{"what": "model/product launch, one line", "url": "https://..."}]}
```

## What a round does

**Round 1 (no ledger.jsonl yet).**
1. `{{TOOLS}}/py sweep.py {{DIR}} --end {{SWEEP_END}}`. This runs the open sources, a 7-day window, 21-day
   lookback, and Semantic Scholar ancestors. It also rebuilds the cross-week index.
2. Read the ledger. Read the abstracts of the top ~80 `week` rows plus every `inbox` row, and skim the
   `recent` and `ancestor` rows.
3. Search the week's news: model and product launches, from the launch posts themselves, for `news`.
   Use WebSearch/WebFetch, and never use numbers you haven't read at the source.
4. Write a first `analysis.json`: the 3 strongest themes that emerge from clusters of papers, about 4
   papers each (a theme needs ≥3 papers, or 2 with very strong signals), plus title candidates. Name
   the runner-up clusters in `analysis.md` under what you left out. Build nothing yet.

**Later rounds.** Each round, do the most valuable thing still missing. Pick from:
- **Visuals.** For themed papers that have no `figs` yet: `{{TOOLS}}/py figures.py pull {{DIR}} <ids>`, then
  **open and look at every figure you intend to list** (Read the jpg). List only the 1–2 best per
  paper. Fix bad crops with `figures.py crop` (the PDF page and box, in points).
  Run `{{TOOLS}}/py figures.py qa {{DIR}}` and resolve what it flags.
- **Project pages and GitHub READMEs.** For papers whose ledger `links` have a `project` or `github`
  entry, run `figures.py page {{DIR}} <url>` to list the media (many project pages render with JS, so use
  WebFetch too), then `figures.py get {{DIR}} <media-url> <stem> --caption "..." --from <page>`.
  Videos and GIFs that show the result are often the best slide a robotics, video or 3D paper has.
- **Threads.** Use the `ancestor` rows and `{{TOOLS}}/index.jsonl` (past streams) to add `ancestors` and
  `callbacks` to themes where they sharpen the theme. A historical figure (e.g. the original Dreamer
  diagram) can go in a theme's `papers` if it earns a slide.
- **Gaps.** Find a strong paper the sources missed, via arXiv listings, the bibliographies of the
  themed papers, or HF trending. Add its id to `inbox.md`, then re-run `sweep.py`, which re-verifies it
  and keeps the other rows.
- **Theme quality.** Merge weak themes, split overloaded ones, drop a theme whose visuals are poor,
  and sharpen the `why` lines and title candidates.

**Every round ends the same way.**
1. Validate that `analysis.json` parses, that every `figs`/`media` stem exists in `figures/`, and that
   every paper id is in the ledger.
2. `{{TOOLS}}/py review.py build {{DIR}}`
3. Append to `log.md`:
   ```
   ## Research round N — <output of `date '+%F %H:%M'`>
   Did: <what, 2-4 lines>
   Themes: <names, with paper count each>
   Open: <what the next round should do>
   ```
4. `git add -A {{DIR}} && git commit -m "{{STREAM_DATE}} research round N: <short>"`. figures/,
   review.html and picks.json are gitignored. Never push.
5. Print a 3-line summary and exit.

## Stop

When every themed paper has a visual you have looked at, themes have settled, and there are 3 themes
of about 4 papers each, or after round {{MAX_ROUNDS}}: do the end-of-round steps, then
add the line `RESEARCH DONE` as the last line of `log.md` and exit. If it is already there, exit
immediately. If the network or arXiv is down, log that and exit. Never invent content.
