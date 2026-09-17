# Iteration log — Recursive Self-Improvement deck

Build: `python3 deck.py` in this folder (SECTIONS/PAPERS in deck.py drive slides.html + README refs).
Figures: `.venv/bin/python pull_figures.py <arxiv-id> ...` (captions land in figures/captions.json).
Manual PDF crop: `.venv/bin/python pull_figures.py --crop <id>:<S-F>:<page>:<x0,y0,x1,y1>`.
Serve: `python3 -m http.server 8765 --bind 127.0.0.1` (running; nzxt tunnels 8765).

## Seed — 2026-09-15 (Mon)
34 slides: title, 8 section dividers, 24 figure slides, refs. 18 papers. Story arc per research.md.
Sections are provisional — rounds may rename, reorder, merge or split them; log the reason here.

## Story status
- Hinge: Dream-RSI = Dreamer where the environment is the discovery tree (callback to 2026.09.11 WAM stream).
- Tension for the close: only the scheduler learns; replay = offline evaluation on logged trees; NeoHorse-1 as foil.
  Section 08 now runs frozen → trained-in-the-loop → post-trained: Offline RL → ThetaEvolve (snowflake/flame) → NeoHorse-1 → EnvHarness.
- Section 03 (anatomy) kept: it now opens with SimpleTES, the baseline Dream-RSI's headline numbers (162×, 50×) are measured against,
  and its C × L × K budget split is literally the set of knobs an exploration policy turns. 3 slides; fine at that size.
- "Old dream" is now Gödel (2003) → STOP (2023) → DGM (2025) → Hyperagents (2026). STOP's Fig 1 (search strategies the model itself proposed)
  is the 2023 version of "the improver rewrites the search". Survey taxonomy (2607.07663) still open — its pulled figs have no captions; look at them next round.
- Dream-RSI repo (2026-09-16): still paper + assets only; code / programs / scripts "being prepared". dream-rsi.com unchanged.
- Thumbnail made 2026-09-15 with Google Flow (Nano Banana Pro, 16:9, 1376x768): white bengal cat at a lab bench dreaming a fractal tree of itself — the replay-simulator hinge. Flow project "Sep 15 - 12:37" has the prompt + a second variant.

## Round 1 — 2026-09-16 20:45
+ 2310.02304 F1 (02 old dream): STOP's self-proposed improvement strategies (GA, bandit, annealing, beam) — the 2023 form of "improver rewrites the search"; answers the open STOP question. Recropped from PDF p1 to drop the "*Work done while at MSR" footnote.
+ 2604.19341 F1 panel (a) (03 anatomy): SimpleTES loop with the C × L × K budget split; the named baseline in Dream-RSI's Lasso/math results. Saved as `2604.19341_S0-F1a.jpg` (PIL crop of the HTML fig, top 700px); full F1 is a 4-panel wall, unusable whole.
+ 2511.23473 F1 (08 catch): ThetaEvolve's three-row AlphaEvolve / RL / ThetaEvolve diagram — snowflake vs flame makes "what actually changes" visual, right before NeoHorse-1. Original pull had only the top bitmap; recropped full figure from PDF p2.
Story: unchanged arc; section 03 and old-dream open questions resolved (see status). 
Rejected: 2606.21090 (Self-Improvement Can Self-Regress, Lin, 2026-06-17) — Fig 1 is a stylized smooth curve, Fig 3 needs "campaign"/"CARE v2" explained; single-task RL over-optimization on Qwen-2.5, tangential to discovery loops. Pulled as S0-F1/S0-F3 if wanted later.
Rejected: Dream-RSI GitHub assets (tagline graphic, stats banner) — marketing graphics, not figures.
Rejected: 2605.21240 APEX, 2504.14363 Retrospective Replay — not examined beyond titles; low priority.
Seed question: AlphaEvolve freezes the model and searches programs; ThetaEvolve trains the model inside the search; Dream-RSI freezes both and trains the scheduler. Which of the three is the "recursive" one, and does the answer depend on what you count as the agent?
Slides: 37 · Sections: 8 · Papers: 21
