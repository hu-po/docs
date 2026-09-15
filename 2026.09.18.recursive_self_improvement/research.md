# Research notes — Recursive Self-Improvement (2026.09.18)

Anchor paper: **Dream-RSI: Recursive Self-Improvement through Evolving Worlds**
(arXiv:2609.14858, Google / Google DeepMind / UMD / UVA, Sept 14 2026).
Code: github.com/zhengkid/Dream-RSI (paper only so far; code + discovered programs "being prepared").
Project page: dream-rsi.com (7 sections; has an interactive live-demo canvas of one loop iteration —
worth screen-sharing on stream).

## The one-sentence version

A discovery loop (propose → evaluate → keep) is driven by an *exploration policy* that decides which
branches to extend, how many in parallel, and when to stop. Improving that policy online is slow because
you only learn whether it was good after a long, expensive rollout. Dream-RSI's move: the discovery trees
you already ran *are* a simulator of the search space you already saw. Replay candidate policies over
those trees (zero execution cost), let an LLM rewrite the policy code, pick the best, redeploy.
Only the policy code changes — the coding agent, evaluator, and model weights stay fixed.

## Why this follows last week

Last week: world models for robots (Ha & Schmidhuber → Dreamer → WAMs). Dream-RSI cites Ha &
Schmidhuber, Dyna, and all four Dreamers explicitly. The pitch is literally "Dreamer, but the environment
is the discovery process." Section 4 of the deck is a direct callback.

## Proposed arc (8 sections, mirrors the WAM deck)

| # | Section | Beat |
|---|---------|------|
| 01 | The machines are doing math now | Hook: AlphaEvolve, Tao's "exploration at scale," Anthropic Riemann zeta (Aug 26), OpenAI Navier–Stokes (Sept 26). These loops run thousands of propose–evaluate cycles. Compute is the ceiling. |
| 02 | The old dream | What "recursive" means: the thing being improved is the improver. Gödel Machine (2003) → STOP (2023) → Darwin Gödel Machine → Hyperagents → the 2026 RSI surveys. |
| 03 | Anatomy of a discovery loop | FunSearch → AlphaEvolve → the open clones (OpenEvolve, ShinkaEvolve, CodeEvolve) → the 2026 refinements (PACEvolve, DeltaEvolve, ThetaEvolve, MLEvolve). Every one of them hard-codes the exploration strategy. |
| 04 | Exploration is the bottleneck | EvoX (meta-evolution), SwarmResearch, SkyDiscover, Meta-Harness, Learning to Discover at Test Time. Meta-level feedback is delayed and expensive — the dilemma Dream-RSI opens with. |
| 05 | Dream about it (callback) | World Models, Dyna, DreamerV1→V4, K-Search (a world model *for kernel search* — the bridge paper). What if the world model is of the search itself? |
| 06 | Dream-RSI | Fig 1 loop; Fig 2 replay simulator; discovery-tree formalism; replay objective (quality − β₁·cost + β₂·parallelism); policy is code, rewritten by an LLM; monotone-selection guarantee. |
| 07 | Does it work? | Fig 3 Lasso (162× fewer agent calls vs SimpleTES, 1.22× runtime); Table 1 math (2/3 tasks match baseline); Fig 4 KernelBench (4/4 kernels, 2.43× fewer generations on VGG16, 2.09× score on ConvDiv); Fig 5 replay beats prompt-guidance; Fig 6 the policy learns to *conserve* compute then re-explore on plateau. |
| 08 | The catch, and what's next | Replay = off-policy evaluation on logged trees: it can only reveal children that were actually generated; counterfactual branches don't exist. Only the scheduler improves — weights, evaluator, agent are frozen. Is that "RSI"? Contrast NeoHorse-1 (weights change), Meta^n, MetaSkill-Evolve, EnvHarness, R-Zero/Absolute Zero. |

## Candidate papers

Legend: ★ = must-have, ○ = strong, · = optional / one figure. "Fig" = likely figure to pull.

### 01 Hook — discovery loops are producing real results
| | arXiv | Title | Why | Fig |
|-|-------|-------|-----|-----|
| ★ | 2506.13131 | AlphaEvolve: A coding agent for scientific and algorithmic discovery | The reference discovery loop; Dream-RSI's whole framing assumes it. | System overview fig; matmul/kissing-number results table |
| ○ | 2511.02864 | Mathematical exploration and discovery at scale (Georgiev, Gómez-Serrano, Tao, Wagner) | Tao on AlphaEvolve at 67 problems; "thousands of cycles" scale. | Problem-coverage figure |
| ○ | — | Anthropic, "Learning more about Claude's mathematical capabilities" (Riemann zeta), Aug 2026 | Cited by Dream-RSI as open-ended math optimization. News hook. | Screenshot |
| ○ | — | OpenAI, "On the Navier–Stokes millennium prize problem," Sept 2026 | Cited by Dream-RSI. News hook; chat will want to talk about it. | Screenshot |
| · | Nature 625:468 (2024) | FunSearch: Mathematical discoveries from program search with LLMs | Origin of the genre; cap-set result. | Fig 1 loop |

### 02 The old dream — what "recursive" means
| | arXiv | Title | Why | Fig |
|-|-------|-------|-----|-----|
| ★ | cs/0309048 | Gödel Machines (Schmidhuber 2003) | The original RSI formalism; self-modifying proof searcher. Set expectations vs. what 2026 "RSI" papers actually do. | The classic block diagram |
| ○ | 2310.02304 | Self-Taught Optimizer (STOP): Recursively Self-Improving Code Generation | First LLM-era RSI: the improver improves the improver's code. Same shape as Dream-RSI's policy rewriting. | Fig 1 |
| ★ | 2505.22954 | Darwin Gödel Machine (Zhang, Hu, Lu, Lange, Clune) | Open-ended agent self-modification with archive; empirical, not provable. | Archive tree fig; SWE-bench curve |
| ○ | 2603.19461 | Hyperagents (Clune et al.) | Agents that modify their own improvement process — meta-level RSI. | Overview |
| ○ | 2607.07663 | Recursive Self-Improvement in AI: From Bounded Self-Refinement to Autonomous Research Loops | Survey; gives a taxonomy slide (what layer is being improved). | Taxonomy fig |
| · | preprints 202608.0051 | The path to recursive self-improving agents (Liu et al., Aug 2026) | Dream-RSI's first citation. Framework diagram. | Framework fig |
| · | 2608.24735 | Meta^n: Recursive Self-Improvement through Emergent Depth | Fixed meta-op, recurse on input — a different reading of "recursive." | Fig 1 |

### 03 Anatomy of a discovery loop
| | arXiv | Title | Why | Fig |
|-|-------|-------|-----|-----|
| ○ | 2510.14150 | CodeEvolve (open-source AlphaEvolve) | Open clone; shows the island/MAP-Elites database. | Architecture |
| ○ | ICLR 2026 | ShinkaEvolve (Lange, Imajuku, Cetin — Sakana) | Sample-efficient evolution; novelty rejection. | Fig 1 / sample-efficiency curve |
| ○ | 2601.10657 | PACEvolve: Progress-Aware Consistent Evolution (Google) | Same Google group's lineage (Yan, Peng, Coleman). Fixed, hand-designed exploration = the baseline Dream-RSI beats. | Fig 1 |
| · | 2605.07039 | PACEvolve++ | Test-time learning for evolutionary search agents. | Overview |
| ○ | 2602.02919 | DeltaEvolve: momentum-driven evolution | History structured as semantic deltas — a contrast to history-as-simulator. | Fig 1 |
| ○ | 2511.23473 | ThetaEvolve: Test-time learning on open problems | Wang et al.; weights update during discovery (contrast). | Fig 1 |
| · | 2606.06473 | MLEvolve | Retrospective cross-branch info to guide search. | Overview |
| · | 2604.19341 | Structured Scaling of AI Discovery Across Diverse Scientific Domains (Ye et al.) | "Evaluation-driven scaling" — thousands of cycles; cost curve. | Scaling fig |

### 04 Exploration is the bottleneck (meta-level)
| | arXiv | Title | Why | Fig |
|-|-------|-------|-----|-----|
| ★ | 2602.23413 | EvoX: Meta-Evolution for Automated Discovery (Berkeley/Sky) | Explicitly optimizes the search strategy online — the direct predecessor Dream-RSI positions against. | Meta-evolution loop fig |
| ○ | 2607.02807 | SwarmResearch: Orchestrating Coding Agents for Open-Ended Discovery | Dynamic orchestration of search branches. | Orchestration fig |
| · | CAIS '26 | SkyDiscover | Adaptive discovery infrastructure. | Arch fig |
| ○ | 2603.28052 | Meta-Harness: End-to-End Optimization of Model Harnesses (Finn, Khattab) | Harness-as-the-thing-being-optimized; ties to NeoHorse "routing harness." | Fig 1 |
| ○ | 2601.16175 | Learning to Discover at Test Time (Yuksekgonul, Guestrin, Zou …) | Discovery as test-time learning; delayed reward. | Fig 1 |
| · | 2605.08083 | LLMs Improving LLMs: Agentic Discovery for Test-Time Scaling (Zheng — same first author) | First author's prior work; shows the lineage. | Fig 1 |

### 05 Dream about it — world models callback
| | arXiv | Title | Why | Fig |
|-|-------|-------|-----|-----|
| ★ | 1803.10122 | World Models (Ha & Schmidhuber) | Reuse last week's Fig 1 / Fig 4 — the callback lands harder with the same figure. | Already have S1-F1, S2-F4 |
| ○ | — | Dyna (Sutton 1990) | The original "learn from simulated experience." No arXiv; use the Dyna diagram from Sutton & Barto. | Dyna architecture |
| ○ | 1912.01603 | Dream to Control (DreamerV1) | Latent imagination; "dreaming" word origin. | Fig 1 |
| ○ | 2301.04104 | DreamerV3 | Already have S0-F1 from last week. | reuse |
| ○ | 2509.24527 | Training Agents Inside of Scalable World Models (DreamerV4) | Latest Dreamer; Dream-RSI cites it. | Fig 1 |
| ★ | 2602.19128 | K-Search: LLM Kernel Generation via Co-Evolving Intrinsic World Model (Cao, Gonzalez, Stoica) | THE bridge paper: a world model *of kernel search*; Dream-RSI cites it and evaluates on kernels too. | Fig 1 |
| · | 2005.01643 | Offline RL: Tutorial, Review, Perspectives (Levine et al.) | Replay-over-logged-data = offline RL. Sets up Act 08's critique. | Fig 1 (online vs off-policy vs offline) |

### 06–07 Dream-RSI itself
| Fig | What | Use |
|-----|------|-----|
| Fig 1 | Three-stage loop (Online Explore → Construct Replay Simulator → Dreaming-based Policy Improvement) | Section 06 opener |
| Fig 2 | Discovery history as replay simulator; alternative policies scored on recorded tree | Section 06, the key idea |
| §3 eq (1) | Replay objective: max score − β₁·N + β₂·(N / rounds) | Render as a text slide |
| §3 text | Decision interface: policy picks batch C ⊆ {root} ∪ leaves, |C| ≤ W | Diagram it ourselves (one text slide) |
| Fig 3 | Lasso regularization-path: runtime on 6 held-out datasets + cost curve | Section 07 |
| Table 1 | Math tasks (Sum Diff etc.) — mixed results; be honest about 2/3 | Section 07 |
| Fig 4 | KernelBench: VGG16, LayerNorm, ConvDiv, ConvMax trajectories vs fixed exploration | Section 07 |
| Fig 5 | Replay simulator vs prompt-level guidance on ConvDiv — guidance *hurts* | Section 07 — best discussion slide |
| Fig 6 | Round-best perf + evaluated attempts per round E0–E8 — policy conserves compute then re-explores | Section 07 closer |

Setup details worth a slide: Gemini-3.1 Pro (10 workers × 11 steps = 110 calls/round) and Gemini-3.7-Flash
(32 × 20 = 640 calls/round) via Gemini CLI; baseline "Recursive Fixed Exploration" = same everything,
policy frozen.

### 08 The catch, and what's next
| | arXiv | Title | Why | Fig |
|-|-------|-------|-----|-----|
| ○ | 1511.03722 | Doubly Robust Off-policy Value Evaluation for RL (Jiang & Li) | Replay is OPE on logged trajectories; support/coverage problem. | Fig 1 or none (text slide) |
| ★ | 2609.08183 | NeoHorse-1: Towards RSI via Agentic Post-Training with Routing Harness | Same week, same buzzword, opposite mechanism (weights change, open 4B/9B). Perfect foil. | Routing/curriculum fig; benchmark table |
| ○ | 2607.05297 | MetaSkill-Evolve: RSI via Two-Timescale Meta-Skill Evolution | Two timescales (task skill vs meta-skill) — same "two loops" shape as Dream-RSI. | Fig 1 |
| ○ | 2608.19880 | EnvHarness: Awakening Static Worlds for Agent Learning | Evolving the *environment* — the piece Dream-RSI freezes. | Fig 1 |
| ○ | 2508.05004 | R-Zero: Self-Evolving Reasoning LLM from Zero Data | Self-play from nothing; where the "R" in RSI could go. | Fig 1 |
| · | 2505.03335 | Absolute Zero: Reinforced Self-play Reasoning with Zero Data | Same. | Fig 1 |
| · | 2605.06614 / 2604.01687 / 2605.14477 | SkillOS / CoEvoSkills / Test-Time Learning with an Evolving Library | Skill-level self-evolution — the other layer. Pick one. | one fig |
| · | 2512.13564 | Memory in the Age of AI Agents (survey) | "History as static context" — the view Dream-RSI argues against. | Taxonomy fig |
| · | 2603.21331 / 2502.10517 | AutoKernel / KernelBench | Kernel-eng context for Fig 4. | one fig |

## Open questions to seed the voice-agent back-and-forth
1. Replay can only reveal recorded children. A "better" policy that would have opened a branch nobody
   opened gets zero credit. How much of the gain is real vs. re-ranking the past?
2. The monotone guarantee is on *replay* score over fixed history. Online transfer is unproven — Fig 3/4
   are the only evidence. What's the equivalent of "sim-to-real gap" here?
3. Guidance hurts (Fig 5). Why? Over-constraining diverse parallel threads. Does that generalize to
   how we prompt coding agents day to day?
4. Fig 6: the policy *reduces* compute when winning and *increases* it on plateau. Is that learned or is
   it what the β₁/β₂ objective forces?
5. Only the scheduler improves. Weights, evaluator, agent frozen. Gödel Machine standard vs. this —
   where on the RSI ladder does "learned scheduler" sit? NeoHorse-1 as counterpoint.
6. Same-week: two "towards RSI" papers, two totally different mechanisms. Is "RSI" now just a marketing
   word for "outer loop"?
7. tatbot angle (optional): a stroke-parameter search over the robot is exactly a discovery tree with
   expensive evaluation. Would a replay simulator over past sessions help?

## Not yet done
- Pull figures (`figures/<id>_S<sec>-F<n>.<ext>`) for the ★/○ rows.
- Thumbnail.
- Fill README References with the final list.
- Check whether the Dream-RSI code lands before Friday (repo says "being prepared").
