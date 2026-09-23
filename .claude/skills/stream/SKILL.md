---
name: stream
description: The hu-po weekly stream pipeline (figure review) — sweep open sources into a verified paper ledger, cluster it into themes with figures an agent has looked at, gate on Hugo's review, build the deck, check it before publishing. Use when Hugo says /stream, asks to start a week's stream, run research or deck rounds, look at the review, or check a stream before publishing.
---

# /stream — how a hu-po stream gets made

**Data → analysis → deck.** Nobody picks the topic first: the title comes out of the week's papers, and
Hugo chooses it at the review gate. The format (what a slide is, the deck size, the rules) lives in
`stream/FORMAT.md`. Read it before any phase, and change it (with a changelog line) when Hugo changes the format.

## The pipeline

| step | tool / prompt | model | output |
|---|---|---|---|
| scaffold | `stream/new.sh [YYYY.MM.DD]` | no model | git worktree + branch `stream/<date>`, folder `<date>.untitled/` |
| **sweep** | `stream/py sweep.py <folder>` (research round 1) | no model | `ledger.jsonl` |
| **research rounds** | `stream/run.sh research <date>`, one round per `phases/research.md` | Opus 5.5 | `analysis.json/.md`, `figures/`, `review.html` |
| **review gate** | `stream/py review.py serve <folder>` | Hugo | `picks.json`: stars, vetoes, preferred figures, title, notes |
| **deck rounds** | `stream/run.sh deck <date>` (`phases/deck.md`: seed → improve → polish) | Opus 5.5 | `deck.json` → `slides.html`, folder renamed to its title |
| thumbnail prompts | `stream/run.sh thumbnail <date>` | Sonnet 5 | `thumbnail_prompt.md`; Hugo makes `thumbnail.jpg` |
| **finalize** | `stream/py finalize.py <folder> [--fill-youtube] [--require-youtube]` | no model | YouTube link from the channel feed; every link and file checked |

The review page's **Save & start deck** button runs the deck rounds and the thumbnail prompts. The
research rounds and the deck rounds each stop by writing `RESEARCH DONE` / `DECK DONE` in the folder's
log. Override the model with `STREAM_MODEL=<model>`.

### Sweep (sweep.py)

- **Main window:** the last 7 days.
  - HuggingFace daily papers (with upvotes and comments).
  - dair-ai ML-Papers-of-the-Week (weeks overlapping the window).
  - EmergentMind and alphaXiv (what's trending now).
  - Links Hugo drops in the folder's `inbox.md` (X, Reddit, anything; X and Reddit are never scraped).
- **Lookback:** the top HF papers of the 21 days before the window, as context.
- **Ancestors:** older arXiv papers that ≥3 of the week's top 60 papers cite (Semantic Scholar
  references). These are the historical threads that tie the week into larger themes.
- **Cross-week memory:** `stream/index.jsonl` indexes every past stream folder. Papers a past stream
  already covered are flagged, and the research agent can use past streams for callbacks.
- **Verification:** every id is resolved against the arXiv API. Titles, authors and dates come only from there.
- **Score:** 10·log10(1+HF upvotes) + 2·log10(1+comments) + 8 dair + 5 EmergentMind + 5 alphaXiv + 25 inbox
  + 3 per citing paper. The score is a sort order for the agent, not a decision.

### Research rounds

The agent reads the top ~80 abstracts. It clusters them into 5–9 themes, where each theme needs ≥3
papers. For each paper it pulls figures (arXiv HTML → ar5iv → PDF crop) plus project-page and README
media, **opens every image it lists**, and keeps the 1–3 best. It adds ancestors and callbacks where
they sharpen a theme, and lists the week's launches for a live (no-slide) cold open. It proposes title
candidates but never chooses one.

### Deck rounds

Hugo's picks override the analysis: a veto is final and a star is required. Round 1 seeds the deck from
the themes that survived review. Each later round fixes the weakest slides first (recrops, better media,
order, tighter factual lines). The polish round adds nothing.

## When Hugo invokes /stream

Work out where the week stands before doing anything: `git worktree list`, then the newest
`<worktree>/<date>.*/log.md`.
- **Research done, no picks.json** → summarize `analysis.md` (themes and paper counts, title candidates,
  anything odd) and point Hugo at the review page. The review page and picks never leave the machine.
- **Deck done** → run `finalize.py` and report what isn't ready (thumbnail, links, crops flagged by
  `figures.py qa`).
- **Publishing:** show Hugo exactly what will merge (`git diff --stat main...stream/<date>`), and let him
  run the merge and push himself.
- Any single round can be run by hand in the session by following its phase file.

## What stays local (gitignored)

`figures/`, `review.html`, `picks.json`, `log.md`, `usage.jsonl`, `inbox.md`, `sweep.json`, `run.log`.
The public repo gets the README, `deck.json`, `slides.html`, the thumbnail and its prompts, the ledger
and the analysis. Never commit machine names, schedules or spend to this repo.

## Rules in every phase

- Everything arXiv comes from the API. Never type titles, authors or dates from memory.
- Look at every figure before it goes in the analysis or the deck.
- Agents commit only on the stream branch and never push.
