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
- Section 03 (anatomy) now opens (round 6) with Compute Allocation F1 (2605.29268): eight loops on circle packing n=26, sum of radii vs reported LLM calls, ~510× budget spread — the cost of "a lot of engineering" in one plot. Then SimpleTES (C × L × K budget) → ShinkaEvolve F2 (four hand-written parent-sampling rules, the literal exploration policy the blurb says stayed fixed) → PACEvolve → DeltaEvolve → EvoTrace F4 (what edits are). Budget → split → which parent → context → what edits.
- "Old dream" is Gödel (2003) → STOP (2023) → DGM (2025) → Hyperagents (2026) → survey taxonomy (2607.07663 F1). Survey F3 (persistence ladder) pulled, unused.
- 05 got its 5th slide in round 4: CompilerDream F5 (2404.16077, real vs imagined compiler trajectory) — literally Dreamer over a compiler, so it beats the queued 2606.09312 F2 (still pulled, now unused).
- 08 "The catch" now has an off-policy-evaluation slide (ADWM F1, 2606.05558) between Levine and GAI: on-policy / learned-simulator OPE with its two failure modes / their fix. Dream-RSI replays a logged tree rather than a learned simulator; the distribution-shift issue is the same one as "can't credit branches nobody opened".
- 08 got its prehistory in round 6: Li et al. 2011 replay (1003.5956 F2) sits right after Levine — logged data from a uniformly random bucket, keep only events where the tested policy agrees with the log, offline estimate matches live CTR. Unbiased only because the log was random; that is the same "can't credit branches nobody opened" constraint. 08 order now: Levine → Li replay → ADWM → Trusting Trust → GAI.
- 08 got a third catch in round 5: Trusting Trust Revisited (2609.17817, Sep 15) F2 between ADWM and GAI — the frozen evaluator is the attack surface; poisoned benchmarks contaminate DGM / SICA / Hyperagents (two of them are section-02 slides) and the poison persists across generations. 08 order: Levine (setting) → ADWM (evaluating a policy you never ran) → Trusting Trust (trusting the score) → GAI (is it recursive). Blurb gained "The evaluator is frozen and trusted."
- 01 got a 4th slide: the Station (2608.23691) — same 12 AlphaEvolve problems, no scripted loop, agents publish into a shared archive. The one non-tree discovery loop in the deck.
- 01 got a 5th in round 5: optimize_anything F7 (2605.19633, GEPA group) — circle packing n=26, best score vs evaluator calls with each jump's strategy labeled, vs ShinkaEvolve / OpenEvolve / AlphaEvolve. Sits between the AlphaEvolve constructions and Georgiev's thread-scaling curve: same problem, four loops, cost on the x-axis.
- 04 opens (round 5) with Exploration Collapse F2 (2510.15047, EMNLP 2026 Findings): vanilla RL on an LLM agent drives Pass@1 up while Pass@k falls; a world-modeling SFT cold start (SPA) lifts both. The empirical case for the section title, and the first appearance of "world model" before 05. 04 is now 6; the round-4 note that 04 was full is superseded because this slide is the section's thesis, not another loop diagram.
- Section sizes: 5 / 5 / 6 / 6 / 5 / 2 / 4 / 5 / 6 (55 slides). 06 is 2 by design (all six Dream-RSI figures are in the deck; 07 cannot grow from the paper itself). 03, 04 and 09 are at 6; do not add to any of them without removing. Room: 07 (4, but only from non-Dream-RSI results), 08 (5), 01/02/05 (5). Deck is 5 under the 60 polish trigger; rounds 7+ should add at most 2 and consider one removal each (DeltaEvolve F1 in 03 and Dreamer F1 in 05 are the weakest-on-their-own slides).
- Dream-RSI repo (2026-09-17 round 6 re-check): still paper + assets, 4 commits; "Discovered programs / Full codebase / Reproduction scripts: being prepared". dream-rsi.com unchanged.
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

## Round 4 — 2026-09-17 01:55
+ 2608.23691 F1 (01 machines): the Station — open-world multi-agent environment run on 12 of the AlphaEvolve construction problems, no coordinator or scripted pipeline; (a) rooms, (b) agents from GPT/Claude/Gemini publish into a shared Archive Room. Five of twelve problems gave results novel relative to the literature. The one discovery loop in the deck that is not a tree.
+ 2404.16077 F5 (05 dream): CompilerDream — real compiler trajectory vs the world model's imagined one under the same three passes, with per-step MSE. A Dreamer-style world model of a code-optimization process, sitting between Dreamer 4 and K-Search. Supersedes the queued 2606.09312 F2.
+ 2606.05558 F1 (08 catch): ADWM — on-policy vs learned-simulator off-policy evaluation (distribution shift, compounding error) vs their diffusion world model with policy guidance. Gives 08 the OPE vocabulary between Levine's three settings and GAI's dial.
Story: unchanged arc; 08 now reads Levine (settings) → ADWM (failure modes of evaluating a policy you never ran) → GAI (is it recursive). No section changes.
Rejected: 2404.16077 F1 (pipeline with BLAS/TensorFlow/Linux logos, too product-y) and F2 (full design overview, two-row wall).
Rejected: 2608.23691 F2 (bar charts of paper types / finding types — counts, not a loop); F10–F14 (kissing configurations, Ramsey coverage — need the math).
Rejected: 2606.05558 F2 (ADWM architecture — soft tokens, projector, reward head; needs the paper).
Rejected: 2608.16884 (Dupont, 2026-08-17, ω < 2.371177 via AlphaEvolve) — a note, pull_figures found 0 figures.
Rejected: 2609.00069 Auditing Harness Tampering (Wang, 2026-08-30) — two-axis taxonomy of tampered harness edits; relevant to "the catch" but not pulled; 08 wanted the OPE beat more.
Rejected: 2608.13951 HELIX model-harness co-evolution (Fan, 2026-08-14), 2609.06396 MetaRSI/RSI² (Tan, 2026-09-06), 2608.12851 Skill Misevolution (Mao, 2026-08-13) — 09 is full; titles only.
Rejected: 2605.15221 Vesper harness engineering (Ishibashi, 2026-05-13), 2605.22817 Vector Policy Optimization (Bahlous-Boldi, 2026-05-21), 2405.15383 Code World Models + MCTS (Dainese, 2024-05-24) — abs read, not pulled; possible 03/04/05 candidates if a slot opens.
Dream-RSI repo / dream-rsi.com: unchanged (paper + assets; code, programs, scripts still "being prepared").
Seed question: ADWM says a simulator learned from offline data fails in two ways: the new policy visits states the old one never did, and errors compound over steps. Dream-RSI's simulator is not learned, it is the literal logged tree. Which of the two failure modes does that avoid, and which does it make worse?
Slides: 49 · Sections: 9 · Papers: 30

## Round 5 — 2026-09-17 02:30
+ 2605.19633 F7 (01 machines): optimize_anything on circle packing n=26 — best score vs evaluator calls with the strategy behind each jump labeled, plus a magnified panel against ShinkaEvolve, OpenEvolve and AlphaEvolve. Same problem as the AlphaEvolve constructions slide, four loops, cost on the x-axis. Placed between the constructions and Georgiev's thread-scaling curve.
+ 2510.15047 F2 (04 exploration, opener): exploration collapse — vanilla RL on an LLM agent (Sokoban / FrozenLake) raises Pass@1 while Pass@k falls; a world-modeling SFT cold start (SPA) lifts both. F1 (five environments) shows the same thing but the collapse is only clear on Sudoku; F2 is one clean pair of panels.
+ 2609.17817 F2 (08 catch): Trusting Trust Revisited — poisoning DGM / SICA / Hyperagents through a benchmark that rewards vulnerable code; the contamination path is drawn on all three and persists across generations. Two of the three systems are section-02 slides. Caption taken from the PDF (HTML captions.json only had "(a) Darwin Gödel Machine").
Story: 08 blurb gained "The evaluator is frozen and trusted." and now runs Levine → ADWM → Trusting Trust → GAI. 04 opens with the collapse curve (6 slides; superseding round 4's "04 is full" because this is the section's thesis, not another loop diagram). No section added, removed or merged.
Rejected: 2609.04665 HackProbe (Yang, 2026-09-04, reward hacking in self-evolving LMs, frozen comparison core across an air gap) — pull_figures grabbed an icon for F1; the real Figure 1 needs a PDF crop. Good second "trust the score" slide if 08 ever wants one; Trusting Trust is more concrete and same-week.
Rejected: 2605.19633 F1 (optimize_anything loop diagram with side information; product-style banner, and 03 already has three loop diagrams) and F9 (with/without subscores ablation, small effect).
Rejected: 2510.15047 F3 (SPA pipeline — three dense panels of Sokoban ASCII, needs the paper) and F1 (see above).
Rejected: 2609.17817 F3/F4/F5 (code listings of the injected directive per system; F2 says it without code).
Rejected: 2609.08919 Experience Funnel (Gao, 2026-09-08, fast textual state / slow policy distillation alternation), 2608.12522 ε-MemEvo (Liu, 2026-08-12, cross-task memory for program evolution), 2609.12216 Guardrailed Meta-Agent Loops (Ma, 2026-09-10) — abs only, not pulled; 09/03 candidates if a slot opens.
Rejected: 2609.00069 Auditing Harness Tampering (Wang, 2026-08-30) — abs re-read; still the taxonomy-of-tampered-edits paper, still not pulled. Trusting Trust took the "catch" slot this round.
Rejected: 2609.14260 (RSI agents for inverter model identification), 2608.29966 DataFoundry, 2609.11873 "The Last AI Built by Humans" — titles only.
Dream-RSI repo / dream-rsi.com: unchanged (paper + assets, 4 commits; code, programs, scripts still "being prepared").
Seed question: Trusting Trust says a self-modifying agent that scores itself on a poisoned benchmark carries the poison into every later generation, even after the benchmark is cleaned. Dream-RSI never modifies the agent, only the exploration policy, and scores policies on replayed history. Is the logged tree a smaller attack surface than a benchmark, or a bigger one, given the same tree is reused for thousands of dreamed policies?
Slides: 52 · Sections: 9 · Papers: 33

## Round 6 — 2026-09-17 03:15
+ 2605.29268 F1 (03 anatomy, opener): Compute Allocation's cost-performance frontier on circle packing n=26 — ShinkaEvolve, CodeEvolve, OpenEvolve, AdaEvolve, SeaEvo, ThetaEvolve with/without RL, AlphaEvolve dashed, pre-LLM SOTA dotted, sum of radii vs reported LLM calls, ~510× spread. The one-plot version of "the loop got a lot of engineering". PDF crop is clean.
+ 2509.19349 F2 (03 anatomy, after SimpleTES): ShinkaEvolve parent sampling — uniform / hill climbing / power law α / weighted (performance × novelty, novelty = 1/(1+offspring)), each program colored by sampling probability. The exploration policy as four hand-written rules, the thing Dream-RSI replaces. Weighted formula verified against the arXiv HTML.
+ 1003.5956 F2 (08 catch, after Levine): Li, Chu, Langford, Wang 2011 — offline replay estimate vs live bucket CTR per article, Yahoo! Front Page. The classic replay-on-logged-data evaluator; unbiased only because the log came from a uniformly random policy, and it throws away every event where the tested policy disagrees with the log. Algorithm 2 and the random-bucket setup verified from the PDF text (HTML fetch of the PDF failed; extracted with pymupdf).
Story: unchanged arc. 03 reordered to budget → split → parent rule → context → edits. 08 gains a 2011 anchor between Levine's settings and ADWM's learned simulator.
Rejected: 2509.19349 F9 (three ablation curves; left panel — novelty-weighted vs hill climbing vs best-of-N on circle packing — is the "exploration policy matters" curve, but 04 is full and the PDF crop carries a "5. Ablations & Analysis" header; recrop p10 if 04 ever frees a slot), F5 (circle packing curve + evolution tree; tree panel is tiny), F1 (product overview banner).
Rejected: 2605.29268 F2 (fitness vs effective FLOPs, best-depth vs best-of-N, four Qwen sizes — decent but needs V_max/T decoded), F3 (C,T surfaces, ablation grid), F4/F7 (per-seed stagnation — interesting for "exploration collapse" but 04 is full).
Rejected: 1003.5956 F3 (daily overall CTR, same message as F2, fewer points), F4–F7 (error decay and ratio scatters).
Rejected: 2605.09764 LEVI (Tanveer, 2026-05-10; pulled) — F1 is a "15× sample efficiency" banner, F2 an architecture wall with CVT-MAP-Elites; a search-architecture-beats-bigger-model claim that would suit 04 if it had room. Left pulled.
Rejected: 2609.19134 ScienceIDE (Geng, 2026-09-16, scientific codebases as agent-learnable environments) and 2609.19140 AgentLSD (Golinelli, 2026-09-16, adversarial task contamination for security agents) — Sep 16 listings; environment side and evaluator-poisoning side respectively; 09 full, 08 already has Trusting Trust. Titles + abs only.
Rejected (still): 2609.15364 RSIAgent, 2609.04665 HackProbe (needs PDF crop of Fig 1), 2609.00069 Harness Tampering, 2405.15383 Code World Models + MCTS.
Dream-RSI repo / dream-rsi.com: unchanged (paper + assets, 4 commits; code, programs, scripts still "being prepared"). arXiv search for "recursive self-improvement" shows nothing newer than ScienceBuddy (Sep 15).
Seed question: Li et al. got an unbiased replay estimate in 2011 by logging with a uniformly random policy and throwing away every event where the new policy disagreed with the log. Dream-RSI's log comes from a deployed policy that was already trying to be good, not random. What does replay over a non-random tree measure — and would Dream-RSI do better if the online rounds deliberately wasted some budget on random branches?
Slides: 55 · Sections: 9 · Papers: 36

