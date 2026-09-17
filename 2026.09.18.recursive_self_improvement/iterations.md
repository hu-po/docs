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
- "Old dream" is now Gödel (2003) → STOP (2023) → DGM (2025) → Hyperagents (2026) → survey taxonomy (2607.07663 F1: what changes × who validates),
  which gives the deck its vocabulary for the close. Survey F3 (what persists: output / session / harness+skills) pulled, unused — candidate for 08 if a "persistence" beat is wanted.
- Section 08 close is now "three RSI papers in one week": Dream-RSI (scheduler, Sep 14) / NeoHorse-1 (weights, Sep 8) / ModularRSI (harness modules, Sep 14). Blurb updated.
- EvoTrace (2605.20086) is the empirical cousin of the replay simulator: logged runs as structured objects, EvoReplay reruns interventions on them. F2 closes 04; F4 (hyperparameter tuning dominates edits, helps least) sits in 03.
- Queued, pulled and inspected: 2606.09312 F2 (compiler world model — Dreamer-style latent z_t over schedule actions, TVM not LLM) for 05 between Dreamer 4 and K-Search if 05 needs a 5th slide.
- Dream-RSI repo (2026-09-16 late, round 2 re-check): still paper + assets only; code / programs / scripts "being prepared". dream-rsi.com unchanged.
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
