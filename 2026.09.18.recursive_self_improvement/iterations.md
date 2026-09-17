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
- Close is now two sections (split in round 3 because the old 08 blurb carried two beats and the second one grew to 6 slides):
  08 "The catch" = replay is offline evaluation on logged trees (Levine F1) + is a learned scheduler recursive at all (Generalized Agent Iteration F2:
  the modifier inside the agent = RSI, outside = plain GPI). 09 "What's next" = frozen → trained-in-the-loop → post-trained → harness → both nested →
  environment: ThetaEvolve → NeoHorse-1 → ModularRSI → ScienceBuddy (F2b mechanism, F8a dynamics) → EnvHarness. NeoHorse-1 stays the foil.
- "Four papers in one week say RSI": Dream-RSI (scheduler, Sep 14) / NeoHorse-1 (weights, Sep 8) / ModularRSI (harness, Sep 14) / ScienceBuddy (harness inner, weights outer, Sep 15).
  Generalized Agent Iteration (Sep 11) is the fifth same-week paper and is the lens, not a mechanism. RSIAgent (Sep 14, frozen memory) still unused.
- Section 04 now has Escher-Loop after EvoX: optimizers scored by the win/loss of the task agents they produce — the online, expensive way to evaluate
  the improver that Dream-RSI's replay replaces. Closes with EvoTrace/EvoReplay (logged runs as objects) as the set-up for 05.
- Section 03 (anatomy) kept: opens with SimpleTES (the baseline for Dream-RSI's headline numbers, C × L × K budget), closes on EvoTrace F4 (what edits are).
- "Old dream" is Gödel (2003) → STOP (2023) → DGM (2025) → Hyperagents (2026) → survey taxonomy (2607.07663 F1). Survey F3 (persistence ladder) pulled, unused.
- Queued, pulled and inspected: 2606.09312 F2 (compiler world model — Dreamer-style latent z_t over schedule actions, TVM not LLM) for 05 between Dreamer 4 and K-Search if 05 needs a 5th slide.
- Section sizes: 3 / 5 / 4 / 5 / 4 / 2 / 4 / 2 / 6. 06 is 2 by design (the two Dream-RSI figures). 09 is the largest; do not add to it again without removing.
- Dream-RSI repo (2026-09-16 round 3 re-check): still paper + assets; "Discovered programs / Full codebase / Reproduction scripts: being prepared". dream-rsi.com unchanged.
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

## Round 2 — 2026-09-16 21:45
+ 2607.07663 F1 (02 old dream): the survey's two-axis taxonomy (what changes × who validates), representative systems per cell. Resolves the open survey question; closes 02 with the vocabulary the rest of the deck uses. Caption fetched from arXiv HTML (captions.json had none for this id).
+ 2605.20086 F4 (03 anatomy): EvoTrace edit taxonomy — hyperparameter tuning is ~45% of edits and has odds ratio < 1; external dependency / efficiency / architecture help most. Shows what the loops actually spend their attempts on.
+ 2605.20086 F2 (04 exploration): EvoTrace/EvoReplay — a logged evolutionary run as a structured object, and interventions rerun on it. Closes 04 as the set-up for "the tree is a simulator".
+ 2609.14857 F1 (08 catch): ModularRSI, posted the same day as Dream-RSI: contrastive trajectory pairs → module-wise harness edits → validation gates. Third "RSI" of the week; the thing that changes is the harness. Dense but three-box structure reads at slide size.
Story: 08 blurb now "Three papers in one week say RSI and mean three different things." No section changes.
Rejected: 2609.13406 Generalized Agent Iteration (Tang, 2026-09-11) — formal GPI-style framework unifying policy iteration and RSI; pull_figures found 0 figures (no HTML figs / PDF crops). Would be a strong 08 slide if a diagram exists; check the PDF by hand next round.
Rejected: 2609.15364 RSIAgent (Zhu, 2026-09-14) — training-free memory construction with broad-then-deep exploration; "RSI" = growing a frozen memory. Not pulled; fourth same-week RSI paper if the close wants it.
Rejected: 2609.15802 Economics of RSI (Cunningham, 2026-09-14) — feedback-loop graphs of AI R&D elasticities; off-theme for a figures deck about discovery loops.
Rejected: 2607.07663 F2 (t-SNE corpus map, no information) and F3 (persistence ladder; kept as candidate, see status).
Rejected: 2606.09312 F2 (compiler world model) — good figure, pulled, deferred to keep the round at 4 adds (see status).
Rejected: 2609.17523 ScienceBuddy, 2609.11873 "The Last AI Built by Humans" — titles only, not examined.
Dream-RSI repo / dream-rsi.com: unchanged (paper + assets; code, programs, scripts still "being prepared").
Seed question: EvoTrace says ~45% of edits in evolutionary coding runs are hyperparameter tweaks and those are the least likely to help. Dream-RSI's policy only decides which node to expand, not what edit to make. Is scheduling the right lever, or is the waste inside the node?
Slides: 41 · Sections: 8 · Papers: 24

## Round 3 — 2026-09-16 22:45
+ 2609.13406 F2 (08 catch): Generalized Agent Iteration's policy / critic / modifier cycle — modifier inside the agent is RSI, outside it is GPI. Answers round 2's "check the PDF by hand": the figure is a vector TikZ drawing pull_figures misses; manual crop p6 `68,50,545,222` (first pass caught the caption line; tightened).
+ 2604.23472 F1 (04 exploration): Escher-Loop — task-agent and optimizer-agent populations; optimizers scored by relative win/loss of the agents they produce and rewrite themselves. The online way to score the improver, right after EvoX.
+ 2609.17523 F2 panel B (09 next): ScienceBuddy recursive-in-recursive — inner recursion evolves the harness with the model fixed, outer recursion GRPO-trains the model under the selected harness. Saved as `2609.17523_S0-F2b.jpg` (PIL crop of the HTML fig, y 1044–1690); full F2 is a product wall. Caption taken from PDF p2 (HTML has none for Fig 2).
+ 2609.17523 F8 panel (a) (09 next): three cycles of ten harness steps then twenty RL updates, colored by cycle; the only curve in the deck that shows two loops alternating. Saved as `2609.17523_S4-F8a.jpg` (left column of F8).
Story: 08 split into 08 "The catch" (Levine F1, GAI F2) and 09 "What's next" (ThetaEvolve → NeoHorse-1 → ModularRSI → ScienceBuddy ×2 → EnvHarness). Reason: the old 08 blurb carried two separate beats and the second grew to 6 slides. Blurb: four papers in one week. 9 sections, at the max.
Rejected: 2609.17523 F1 — three-panel product graphic with icons (224 tools, robot); the F2 panel B says the same thing without marketing.
Rejected: 2604.23472 F2/F3 (Escher-Loop best-so-far vs cumulative tokens on kissing number / circle packing / Heilbronn) — decent curves but one Escher-Loop slide is enough for 04.
Rejected: 2607.21461 AREX (Lu, 2026-07-23, "recursively self-improving" deep-research agent) — inner research loop + outer answer-refinement loop; "RSI" = iterative answer verification, not a discovery loop. Not pulled.
Rejected: 2606.09032 Text World Models survey (Li, 2026-06-08) — survey of transition models over textual states; 05 already has K-Search as the bridge and the compiler world model queued. Not pulled.
Rejected: 2609.15364 RSIAgent — still not pulled; 09 is full.
Dream-RSI repo / dream-rsi.com: unchanged.
Seed question: By Generalized Agent Iteration's dial, RSI means the modifier lives inside the agent. In Dream-RSI the modifier is the LLM that rewrites exploration-policy code and it is the same frozen model that does the exploring. Is that inside or outside — and does ScienceBuddy, which trains the weights under the evolved harness, count as more recursive or just more expensive?
Slides: 46 · Sections: 9 · Papers: 27
