#!/usr/bin/env python3
"""Build slides.html from the SECTIONS list below.  python3 deck.py  (writes slides.html next to this file)

Format (same as 2026.09.11): title slide (thumbnail.jpg) -> per section: a divider card, then figure slides
(white-framed figure + one factual context line + mono cite) -> references grid.  No commentary, no timecodes.
Overnight rounds edit SECTIONS/PAPERS only; the chrome below is frozen.
"""
import html, json, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
TITLE = "Recursive Self-Improvement"
DATE = "2026.09.18"

# arXiv id -> (short name, first author, YYYY-MM-DD, full title)
PAPERS = {
    "2609.14858": ("Dream-RSI", "Zheng", "2026-09-14", "Dream-RSI: Recursive Self-Improvement through Evolving Worlds"),
    "2506.13131": ("AlphaEvolve", "Novikov", "2025-06-16", "AlphaEvolve: A coding agent for scientific and algorithmic discovery"),
    "2511.02864": ("Mathematical Exploration at Scale", "Georgiev", "2025-11-03", "Mathematical exploration and discovery at scale"),
    "cs/0309048": ("Gödel Machines", "Schmidhuber", "2003-09-25", "Gödel Machines: Self-Referential Universal Problem Solvers Making Provably Optimal Self-Improvements"),
    "2310.02304": ("STOP", "Zelikman", "2023-10-03", "Self-Taught Optimizer (STOP): Recursively Self-Improving Code Generation"),
    "2505.22954": ("Darwin Gödel Machine", "Zhang", "2025-05-29", "Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents"),
    "2603.19461": ("Hyperagents", "Zhang", "2026-03-19", "Hyperagents"),
    "2607.07663": ("RSI Survey", "Chen", "2026-07-08", "Recursive Self-Improvement in AI: From Bounded Self-Refinement to Autonomous Research Loops"),
    "2601.10657": ("PACEvolve", "Yan", "2026-01-15", "PACEvolve: Enabling Progress-Aware Consistent Evolution"),
    "2602.02919": ("DeltaEvolve", "Jiang", "2026-02-02", "DeltaEvolve: Accelerating Scientific Discovery through Momentum-Driven Evolution"),
    "2602.23413": ("EvoX", "Liu", "2026-02-26", "EvoX: Meta-Evolution for Automated Discovery"),
    "2607.02807": ("SwarmResearch", "Virk", "2026-07-02", "SwarmResearch: Orchestrating Coding Agents for Open-Ended Discovery"),
    "2603.28052": ("Meta-Harness", "Lee", "2026-03-30", "Meta-Harness: End-to-End Optimization of Model Harnesses"),
    "2604.19341": ("SimpleTES", "Ye", "2026-04-21", "Structured Scaling of AI Discovery Across Diverse Scientific Domains"),
    "2511.23473": ("ThetaEvolve", "Wang", "2025-11-28", "ThetaEvolve: Test-time Learning on Open Problems"),
    "2601.16175": ("TTT-Discover", "Yuksekgonul", "2026-01-22", "Learning to Discover at Test Time"),
    "1803.10122": ("World Models", "Ha", "2018-03-27", "World Models"),
    "1912.01603": ("Dreamer", "Hafner", "2019-12-03", "Dream to Control: Learning Behaviors by Latent Imagination"),
    "2509.24527": ("Dreamer 4", "Hafner", "2025-09-29", "Training Agents Inside of Scalable World Models"),
    "2602.19128": ("K-Search", "Cao", "2026-02-22", "K-Search: LLM Kernel Generation via Co-Evolving Intrinsic World Model"),
    "2005.01643": ("Offline RL Tutorial", "Levine", "2020-05-04", "Offline Reinforcement Learning: Tutorial, Review, and Perspectives on Open Problems"),
    "2609.08183": ("NeoHorse-1", "NeoHorse Team", "2026-09-08", "NeoHorse-1: Towards Recursive Self-Improvement via Agentic Post-Training with Routing Harness"),
    "2607.05297": ("MetaSkill-Evolve", "Wang", "2026-07-06", "MetaSkill-Evolve: Recursive Self-Improvement of LLM Agents via Two-Timescale Meta-Skill Evolution"),
    "2608.19880": ("EnvHarness", "Huang", "2026-08-20", "EnvHarness: Awakening Static Worlds for Agent Learning"),
    "2508.05004": ("R-Zero", "Huang", "2025-08-07", "R-Zero: Self-Evolving Reasoning LLM from Zero Data"),
    "2605.20086": ("EvoTrace", "Pelleriti", "2026-05-19", "What Do Evolutionary Coding Agents Evolve?"),
    "2609.14857": ("ModularRSI", "Wu", "2026-09-14", "ModularRSI: Modular and Generalizable Recursive Harness Self-Improvement"),
    "2609.13406": ("Generalized Agent Iteration", "Tang", "2026-09-11", "Generalized Agent Iteration: One Formal Framework for Iterative Policy Improvement and Recursive Self-Improvement"),
    "2604.23472": ("Escher-Loop", "Liu", "2026-04-25", "Escher-Loop: Mutual Evolution by Closed-Loop Self-Referential Optimization"),
    "2609.17523": ("ScienceBuddy", "Xue", "2026-09-15", "ScienceBuddy: Recursive-in-Recursive Self-Improvement for Interactive Scientific Agents"),
    "2608.23691": ("The Station", "Chung", "2026-08-24", "Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment"),
    "2404.16077": ("CompilerDream", "Deng", "2024-04-24", "CompilerDream: Learning a Compiler World Model for General Code Optimization"),
    "2606.05558": ("ADWM", "Liu", "2026-06-04", "Autoregressive Diffusion World Models for Off-Policy Evaluation of LLM Agents"),
    "2605.19633": ("optimize_anything", "Agrawal", "2026-05-19", "optimize_anything: A Universal API for Optimizing any Text Parameter"),
    "2510.15047": ("Exploration Collapse", "Chen", "2025-10-16", "Why Do LLM Agents Fail in Exploring New Environments? A World-Modeling Perspective"),
    "2609.17817": ("Trusting Trust, Revisited", "Roesner", "2026-09-15", "Reflections on Trusting Trust, Revisited: Contaminating Self-Modifying AI Coding Agents with Poisoned Benchmarks"),
    "2605.29268": ("Compute Allocation", "Xing", "2026-05-28", "Compute Allocation for Self-Evolving LLMs: From Depth-Breadth to Multi-Armed Bandits"),
    "2509.19349": ("ShinkaEvolve", "Lange", "2025-09-17", "ShinkaEvolve: Towards Open-Ended And Sample-Efficient Program Evolution"),
    "1003.5956": ("Replay Evaluation", "Li", "2010-03-31", "Unbiased Offline Evaluation of Contextual-bandit-based News Article Recommendation Algorithms"),
    "2605.08083": ("AutoTTS", "Zheng", "2026-05-08", "LLMs Improving LLMs: Agentic Discovery for Test-Time Scaling"),
    "2605.07039": ("PACEvolve++", "Yan", "2026-05-07", "PACEvolve++: Improving Test-time Learning for Evolutionary Search Agents"),
    "2410.04444": ("Gödel Agent", "Yin", "2024-10-06", "Gödel Agent: A Self-Referential Agent Framework for Recursive Self-Improvement"),
    "1911.08265": ("MuZero", "Schrittwieser", "2019-11-19", "Mastering Atari, Go, Chess and Shogi by Planning with a Learned Model"),
    "2609.12459": ("EvoRS", "Li", "2026-09-11", "EvoRS: On-Policy Self-Evolution of Reward Systems for Open-Ended Reinforcement Learning"),
    "2609.11873": ("The Last AI Built by Humans", "Duan", "2026-09-10", "The Last AI Built by Humans: Toward Genuine Recursive Self-Improvement"),
}

# Each slide: dict(fig="<file stem in figures/>", ctx="one or two factual sentences")  (cite line is derived)
SECTIONS = [
    dict(title="The machines are doing math now",
         blurb="Propose, evaluate, keep. Thousands of times. The loops are real, the results are real, and the bill is compute.",
         slides=[
            dict(fig="2506.13131_S2-F2", ctx="AlphaEvolve's discovery process. The user supplies an initial program with the parts to evolve marked, plus evaluation code. A program database samples prompts, an LLM ensemble proposes diffs, evaluators score the result, and the database is updated."),
            dict(fig="2506.13131_S3-F5", ctx="Constructions discovered by AlphaEvolve that beat the previous state of the art: autocorrelation and uncertainty inequalities in analysis, packing problems in geometry, and combinatorial bounds."),
            dict(fig="2605.19633_S5-F7", ctx="Circle packing with 26 circles, one of the AlphaEvolve construction problems, run through optimize_anything (a general text-optimization loop from the GEPA project). Left: best score against number of evaluator calls, with the strategy behind each jump labeled, from force-based optimization to large-neighborhood SLP with dual-informed refinement. Right: the same plot magnified near the top, with ShinkaEvolve, OpenEvolve and the AlphaEvolve result for comparison."),
            dict(fig="2511.02864_S3-F1", ctx="Same problem, more parallel threads: running AlphaEvolve with more threads finds good constructions sooner in wall-clock time, but at a greater total compute cost. Averages over 100 experiments."),
            dict(fig="2608.23691_S2-F1", ctx="The Station, evaluated on 12 of the AlphaEvolve construction problems with no central coordinator or scripted pipeline. (a) Rooms in the environment; at every tick each agent picks a room and an action. (b) Agents from several model families choose their own direction, run experiments and submit papers; a reviewer agent accepts or rejects, and accepted papers stay in the Archive Room for later agents to read, extend and cite."),
         ]),
    dict(title="The old dream",
         blurb="Recursive means the thing being improved is the improver. That idea is older than the transformer, and each era has meant something different by it.",
         slides=[
            dict(fig="cs0309048_S2-F1", ctx="A Gödel machine's storage before any self-improvement: the initial solver, a proof searcher, and the axioms describing its own hardware and utility. The machine may rewrite any part of itself once the proof searcher proves the rewrite is useful."),
            dict(fig="2310.02304_S0-F1", ctx="STOP: a language model is given a seed improver, a program that improves programs, and applies it to itself. The self-improvement strategies shown were proposed and implemented by GPT-4 during that process: genetic algorithm, decomposing and improving parts, multi-armed prompt bandit, varying temperature, simulated annealing, and beam or tree search."),
            dict(fig="2410.04444_S1-F2", ctx="Three agent paradigms as drawn by Gödel Agent (2024). Left: hand-designed agents, each workflow written by an expert. Middle: meta-learning optimized agents, where a fixed meta agent (gray) improves the task agents (green) from a feedback signal. Right: a self-referential agent, where the meta agent is itself learnable and improves both the task agent and its own improvement procedure. Green marks what can change, gray what is fixed."),
            dict(fig="2505.22954_S1-F1", ctx="The Darwin Gödel Machine drops the proofs and keeps the self-modification: a growing archive of coding agents, each produced by an existing agent editing its own code, then evaluated on downstream coding tasks. Parents are chosen from the archive open-endedly, not greedily."),
            dict(fig="2603.19461_S3-F1", ctx="Hyperagents extend the DGM one level up. Agents improve not only the code that does the task but the code that does the improving, and the run can span multiple task domains at once."),
            dict(fig="2607.07663_S0-F1", ctx="The two-axis taxonomy from a 1,250-paper survey of self-improvement. Columns: what changes, whether deployment-time behavior, policy weights, the evaluation machinery, or the research process itself. Rows: who validates the improvement, from a person reviewing each change to a closed loop that generates, validates and applies changes on its own. Representative systems in each cell."),
         ]),
    dict(title="Anatomy of a discovery loop",
         blurb="Between AlphaEvolve and today the loop got a lot of engineering. The exploration strategy stayed hand-written and fixed.",
         slides=[
            dict(fig="2605.29268_S1-F1", ctx="Eight LLM evolution systems on one problem, circle packing with 26 circles: sum of radii against the number of LLM calls each paper reports for its result. Markers are the reported scores; the dashed line is AlphaEvolve's 2.6358 and the dotted line the best pre-LLM result. Reported per-run budgets span roughly 510 times."),
            dict(fig="2604.19341_S0-F1a", ctx="SimpleTES, the baseline Dream-RSI reports its Lasso and math results against. Top: the research community's propose-evaluate-refine cycle. Bottom: the same loop with an LLM as the researcher. The evaluator-query budget N = C × L × K is split across global width C (independent lines in parallel), refinement depth L (rounds carrying the best line forward) and generation batch size K."),
            dict(fig="2509.19349_S3-F2", ctx="ShinkaEvolve's parent sampling: four rules for which archived program to mutate next. Each point is a program, its performance score against how many offspring it already has, colored by the probability the rule assigns it. Uniform samples every program equally; hill climbing takes only the best; power law weights by fitness rank with exponent α; weighted multiplies a performance term by a novelty term that falls with offspring count."),
            dict(fig="2605.08083_S1-F2", ctx="Hand-written test-time scaling strategies drawn as paths in a width–depth control space: width is the number of parallel reasoning branches, depth how far each is continued. Self-consistency at 64 samples sits in a fixed full-budget corner; ASC and ESC adapt only width; Answer Consistency adapts only depth; ST-BoN expands wide, prunes to one branch, then deepens; Parallel-Probe starts wide, prunes and stops early. AutoTTS, from Dream-RSI's first author, has an LLM write new controllers for this space and scores them by replaying pre-collected reasoning trajectories."),
            dict(fig="2601.10657_S1-F1", ctx="PACEvolve's workflow, from the same Google group as Dream-RSI. Idea generation is decoupled from idea selection, with a hierarchical idea memory and progress-aware context management. The exploration strategy itself is designed by hand."),
            dict(fig="2605.20086_S5-F4", ctx="What the edits in evolutionary coding runs actually are, across EvoTrace, a dataset of runs from four frameworks and 16 math and algorithm-design tasks. (a) Share of all edits with each label: hyperparameter tuning dominates. (b) Odds ratio that an edit of each type improves the score: external dependency, efficiency and architectural change help most per edit; hyperparameter tuning and pruning fall below 1."),
         ]),
    dict(title="Exploration is the bottleneck",
         blurb="Which branch, how many in parallel, when to stop. Improve that policy online and you only find out if it was good after a long, expensive rollout.",
         slides=[
            dict(fig="2510.15047_S1-F2", ctx="Exploration collapse. Validation performance of an LLM agent on Sokoban and FrozenLake over RL training steps. Left: Pass@k, whether any of k = 8 sampled trajectories succeeds. Right: Pass@1. Red is vanilla RL, where Pass@k falls as Pass@1 rises; yellow adds state estimation; blue (SPA) first fine-tunes the agent to predict world states from its own interaction data, then runs the same RL."),
            dict(fig="2607.02807_S0-F1", ctx="A SwarmResearch run designing speculative-decoding implementations. Nodes are spawned search agents and their solutions, edges mean the lower node builds on the one above, and the top number is spawn order."),
            dict(fig="2602.23413_S0-F1", ctx="EvoX has two coupled loops: an inner loop that evolves solutions, and an outer loop that evolves the search strategy governing generation. The right panel shows how the choice of search strategy changes outcomes on the same task."),
            dict(fig="2605.07039_S1-F1", ctx="PACEvolve++, the same group's follow-up to PACEvolve. Strategic search decisions are split from implementation: a trainable advisor LLM selects ideas from the search state and proposes the next solution, a stronger frontier coding LLM implements it, and the evaluator's score is fed back to the advisor as reinforcement learning. The advisor's weights are updated during the search itself."),
            dict(fig="2604.23472_S2-F1", ctx="Escher-Loop keeps two populations. Optimizer agents generate new task agents; the task agents are executed for absolute scores, and those same scores are reused as relative win-loss signals to score the optimizers, which also rewrite themselves. Optimizers are judged by the agents they produce, with no separate benchmark."),
            dict(fig="2605.20086_S1-F2", ctx="EvoTrace records each evolutionary run as a structured object: programs, the parent-child graph, prompts and context, scores and evaluator metadata. EvoReplay reconstructs local search states from those traces and reruns controlled interventions on them, including same-prompt replay, retuning, ablation, repair, context replay and model substitution."),
         ]),
    dict(title="Dream about it",
         blurb="Last week: a world model is a compressed picture of the environment you can run forward. What if the environment is the search?",
         slides=[
            dict(fig="1803.10122_S1-F1", ctx="Ha and Schmidhuber open World Models with a panel from Understanding Comics. An agent never acts on the world directly, only on a compressed internal model of it built from limited sensory input."),
            dict(fig="1912.01603_S3-F3", ctx="The three components of Dreamer. (a) From a dataset of past experience, the agent learns to encode observations and actions into compact latent states and to predict rewards. (b) In that latent space it predicts state values and actions, trained by propagating gradients back through imagined trajectories. (c) It encodes the episode so far into a model state and predicts the next action to execute in the real environment."),
            dict(fig="2509.24527_S0-F1", ctx="Dreamer 4 learns to solve control tasks by reinforcement learning entirely inside its world model. The imagined training sequences are decoded for visualization; the model has learned to simulate a wide range of Minecraft situations."),
            dict(fig="2404.16077_S4-F5", ctx="CompilerDream: a Dreamer-style world model of a compiler. Top: the real environment, starting from the cBench stringsearch2 program and applying the passes -sroa, -early-cse, -simplifycfg. Bottom: the world model's imagined trajectory under the same passes, predicting the IR features and the reward at each step; mean squared error between the two is shown at each step."),
            dict(fig="1911.08265_S3-F1", ctx="MuZero plans by tree search inside a learned model. (A) A representation function h maps past observations to a hidden state, a dynamics function g predicts the next hidden state and reward for each action, and a prediction function f gives a policy p and value v at every node, so the tree is imagined without touching the environment. (B) Acting: the search's root visit counts give a policy π, an action is sampled, the episode goes to a replay buffer. (C) Training: the model is unrolled along a stored trajectory and its predictions are fit to what the search and the environment produced."),
            dict(fig="2602.19128_S3-F1", ctx="K-Search: a world model for kernel search. The search state is a tree of closed nodes with attached programs and a frontier of open proposals with predicted values. An LLM reasoner updates, inserts and prunes the tree after each execution."),
         ]),
    dict(title="Dream-RSI",
         blurb="Completed discovery trees already record what happened on every branch. That is a simulator. Replay new exploration policies over it for free.",
         slides=[
            dict(fig="2609.14858_S1-F1", ctx="The Dream-RSI loop. An exploration policy guides a coding agent to expand a discovery tree online and log traces. The tree becomes a replay simulator. The agent then dreams many alternative policies, scores them in replay, and redeploys the best one for the next online round."),
            dict(fig="2609.14858_S1-F2", ctx="Discovery history as a replay simulator. A deployed policy explores online and produces a tree where each node is an attempt with its full observation. Alternative policies can then be tested on the recorded tree, choosing different branches, orders, concurrency and stopping rules, without executing anything new."),
         ]),
    dict(title="Does it work?",
         blurb="Three domains, one controlled baseline: the same discovery agent, evaluator, budget and initial policy, but with the policy frozen. Then the first author's earlier replay-discovered controllers, on benchmarks the replay never saw.",
         slides=[
            dict(fig="2609.14858_S4-F3", ctx="Lasso regularization-path discovery. Top: final wall-clock runtime of the discovered solver on held-out datasets. Bottom: runtime versus cumulative discovery compute across recursive rounds for Gemini-3.1 Pro and Gemini-3.7 Flash. Blue is the fixed-policy baseline, red is Dream-RSI; numbers mark the round."),
            dict(fig="2609.14858_S4-F4", ctx="GPU kernel engineering on four KernelBench tasks. Performance (1/ms) against number of generations. Dream-RSI reaches comparable performance with 2.43x and 1.79x fewer generations on VGG16 and LayerNorm, and 2.09x and 1.44x higher scores at similar budget on ConvDiv and ConvMax."),
            dict(fig="2609.14858_S5-F5", ctx="ConvDiv, four conditions. Adding explicit prompt-level guidance distilled from history (dashed) underperforms the unguided version of the same method, for both fixed exploration and Dream-RSI. Using history as an interactive simulator beats using it as advice."),
            dict(fig="2609.14858_S5-F6", ctx="How the learned exploration policy behaves across recursive rounds on ConvDiv. Top: round-best performance. Bottom: evaluated attempts per round, which drops from 110 to 50 while performance climbs, then rises again once progress plateaus."),
            dict(fig="2605.08083_S5-F3", ctx="AutoTTS, from Dream-RSI's first author, four months earlier: an explorer LLM writes width–depth test-time scaling controllers as code and scores them by replaying pre-collected reasoning trajectories, with no new LLM calls during the search. Accuracy against total tokens on held-out AIME25 and HMMT25 for four Qwen3 sizes; red is the controller discovered on the search set, the others are hand-written strategies scaled by varying the number of sampled trajectories."),
         ]),
    dict(title="The catch",
         blurb="Replay can only reveal branches somebody already opened. The evaluator is frozen and trusted. Only the scheduler learns. Is a learned scheduler recursive?",
         slides=[
            dict(fig="2005.01643_S1-F1", ctx="Online, off-policy and offline reinforcement learning. In the offline setting (c) data is collected once with some policy and the learner never interacts with the environment again. Evaluating a new exploration policy on a recorded discovery tree is this setting."),
            dict(fig="1003.5956_S4-F2", ctx="Replay evaluation on logged data, Yahoo! Front Page, 2009. The log came from a bucket that showed articles uniformly at random; the evaluator keeps an event only when the policy under test would have chosen the article the log shows, discards the rest, and averages the clicks it kept. Each point is one article: click-through rate measured live under the policy (x) against the replay estimate (y), both relative to a hidden constant."),
            dict(fig="2606.05558_S1-F1", ctx="Three ways to evaluate an LLM agent policy. Left: on-policy, run the agent in the real environment. Middle: off-policy, train a simulator on offline data and roll the new policy out in it, which suffers distribution shift between the behavior and target policies and compounding error over multi-step rollouts. Right: ADWM, a diffusion world model with the evaluated policy injected into every denoising step."),
            dict(fig="2609.12459_S3-F2", ctx="A fixed scorer while the policy it scores is trained against it. Left: global reward variance of a continuous rubric-based scorer over GRPO training steps on open-ended writing tasks; it rises, then falls as responses concentrate in a narrower score band, and saturates by step 120. Right: score distributions at step 120 for the same responses from the continuous scorer (μ = 0.82, σ = 0.05) and from a pairwise comparator (μ = 0.50, σ = 0.21)."),
            dict(fig="2609.17817_S3-F2", ctx="Poisoning a self-improving agent through its benchmark, drawn for three systems: (a) Darwin Gödel Machine, (b) Self-Improving Coding Agent, (c) Hyperagents. The agent evaluates itself on a benchmark seeded with tasks that reward vulnerable code; the scored transcript feeds the diagnosis and self-improvement prompts, and the proposed modification is applied to the coding agent or its harness. Devils mark where the contamination travels; the attack succeeds if an evolved agent writes vulnerable code on a neutral task."),
            dict(fig="2609.13406_S3-F2", ctx="Generalized agent iteration as a cycle of policy, critic and modifier. The critic evaluates the policy and the modifier against a base (the environment and goal) and returns feedback; the modifier produces improvements, including, in gray dashed, rewrites of the critic and of itself. The dash-dot border marks the modifier as part of the agent: with the modifier fixed outside the agent the cycle reduces to generalized policy iteration; with it inside, it is recursive self-improvement."),
         ]),
    dict(title="What's next",
         blurb="Six papers in eight days say RSI. One trains the weights, one rewrites the harness, one nests both, one learns the scheduler, two define the word. The environment is frozen in every one of them.",
         slides=[
            dict(fig="2511.23473_S1-F1", ctx="Three loops side by side. Top: AlphaEvolve, where a frozen LLM ensemble (snowflake) proposes edits to programs sampled from a program database. Middle: standard RL, where a single LLM is trained (flame) on prompts from a static dataset. Bottom: ThetaEvolve, a single LLM sampling from a program database, with optional RL training on the verifier's scores."),
            dict(fig="2609.08183_S1-F2", ctx="NeoHorse-1, published the same week. Diverse tasks generate experience through a routing harness backed by a pool of models; that experience becomes a training mixture and the model weights are updated. Here the thing that changes is the model."),
            dict(fig="2609.14857_S2-F1", ctx="ModularRSI, posted the same day as Dream-RSI. Top: rollouts on a task are sorted into positive, negative and contrastive pairs (same task, reward 1 versus 0) and analyzed for recurring failures. Bottom left: a code-modify agent edits one harness module at a time, from observation management to task completion. Bottom right: each modification must pass execution, program-verification and diff-review gates or is rolled back. Here the thing that changes is the harness."),
            dict(fig="2609.17523_S0-F2b", ctx="ScienceBuddy's recursive-in-recursive loop, posted the day after Dream-RSI. Inner recursion, task model fixed: a fixed auxiliary model diagnoses failures and revises harness procedures, and a candidate harness is accepted only if it beats its parent in paired evaluation. Outer recursion, harness fixed: fresh rollouts under the selected harness, rubric rewards, GRPO updates to the model, then model and harness are redeployed together for the next cycle."),
            dict(fig="2609.17523_S4-F8a", ctx="ScienceBuddy learning dynamics over three cycles; colors mark the cycle. Top: validation accuracy over harness-evolution steps, where circles are measured candidates including rejected ones and stars are new bests. Bottom: training reward over the twenty RL updates that follow each block of ten harness steps."),
            dict(fig="2608.19880_S1-F2", ctx="EnvHarness applies the agent-harness idea to the other side of the interface: the base environment stays frozen and plug-in components change what the agent experiences. The environment is the part Dream-RSI holds fixed."),
            dict(fig="2609.11873_S1-F2", ctx="Five levels of RSI autonomy drawn as loops. Gray dashed frames are components humans control, green dashed frames are components inside the agentic loop, and orange outlines mark the component newly taken over at each level: executing tasks (L1), designing the update policy (L2), planning experience acquisition (L3), interacting with the environment (L4), and improving the improvement system itself (L5)."),
         ]),
]

HEAD = '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>{TITLE} &middot; hu-po &middot; {DATE}</title>\n<style>\n  :root{\n    --bg:#0B0E0F; --panel:#141A1B; --ink:#E9EFED; --muted:#93A29E; --faint:#63736F;\n    --live:#56E0BE; --rule:#212A2A;\n    --sans:"Helvetica Neue",Helvetica,Arial,system-ui,sans-serif;\n    --mono:ui-monospace,"SF Mono","DejaVu Sans Mono",Menlo,Consolas,monospace;\n  }\n  *{box-sizing:border-box;margin:0;padding:0}\n  html,body{height:100%;background:#000;color:var(--ink);font-family:var(--sans);overflow:hidden}\n\n  #stage{position:fixed;inset:0;background:#000;overflow:hidden}\n  #deck{width:1920px;height:1080px;position:absolute;left:0;top:0;transform-origin:0 0;background:var(--bg);overflow:hidden}\n  .slide{position:absolute;inset:0;display:none}\n  .slide.on{display:grid}\n\n  /* title */\n  .title{grid-template-rows:1fr;padding:0}\n  .title img{width:100%;height:100%;object-fit:contain;background:var(--bg);display:block}\n\n  /* section divider */\n  .sec{grid-template-rows:1fr;padding:100px 130px}\n  .secbody{display:flex;flex-direction:column;justify-content:center;gap:38px;max-width:1520px}\n  .sec .num{font-family:var(--mono);font-size:30px;letter-spacing:.2em;color:var(--live)}\n  .sec h2{font-size:94px;line-height:1.03;letter-spacing:-.03em;font-weight:700;text-wrap:balance}\n  .sec .blurb{font-size:36px;line-height:1.42;color:var(--muted);max-width:1340px;\n              padding-top:30px;border-top:1px solid var(--rule)}\n\n  /* figure */\n  .fig{grid-template-rows:1fr auto auto;padding:38px 56px 28px;gap:14px}\n  .fig .frame{min-height:0;background:#fff;border:1px solid var(--rule);padding:16px}\n  .fig img{width:100%;height:100%;object-fit:contain;display:block}\n  .fig .ctx{font-size:25px;line-height:1.42;color:var(--ink);text-align:left;\n            max-width:1660px;justify-self:center;text-wrap:pretty}\n  .fig .ctx b{color:#fff;font-weight:600}\n  .fig .cite{font-family:var(--mono);font-size:21px;letter-spacing:.03em;color:var(--faint);text-align:center}\n\n  /* references */\n  .refs{grid-template-rows:1fr;padding:56px 80px}\n  .reflist{display:grid;grid-template-columns:repeat(3,1fr);gap:0 44px;align-content:center}\n  .ref{display:grid;grid-template-columns:118px 1fr;gap:14px;padding:10px 0;border-bottom:1px solid var(--rule)}\n  .ref code{font-family:var(--mono);font-size:17px;color:var(--live)}\n  .ref .t b{display:block;font-size:19px;font-weight:600;line-height:1.22}\n  .ref .t span{font-family:var(--mono);font-size:15px;color:var(--faint)}\n\n  /* overview */\n  #overview{position:fixed;inset:0;background:rgba(6,9,10,.97);z-index:20;display:none;overflow-y:auto;padding:26px}\n  body.ov #overview{display:block}\n  .ovgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:14px}\n  .ov{background:var(--panel);border:1px solid var(--rule);padding:0;cursor:pointer;\n      display:flex;flex-direction:column;gap:0;text-align:left;color:inherit;font:inherit;overflow:hidden}\n  .ov:hover,.ov:focus-visible{border-color:var(--live);outline:none}\n  .ov img{width:100%;aspect-ratio:16/10;object-fit:contain;background:#fff;display:block}\n  .ovcard{width:100%;aspect-ratio:16/10;background:linear-gradient(135deg,#182120,#0E1414);display:block}\n  .ov em{font-family:var(--mono);font-size:11px;font-style:normal;color:var(--muted);\n         padding:7px 8px;line-height:1.3;letter-spacing:.02em}\n  .ov.cur{border-color:var(--live)}\n  .ov.cur em{color:var(--live)}\n\n  /* hud */\n  #hud{position:fixed;left:0;right:0;bottom:0;display:flex;gap:16px;align-items:center;\n       padding:9px 16px;font-family:var(--mono);font-size:12px;letter-spacing:.09em;color:var(--faint);\n       background:linear-gradient(to top,rgba(0,0,0,.85),rgba(0,0,0,0));pointer-events:none;z-index:10}\n  #hud .grow{flex:1}\n  #prog{position:fixed;left:0;top:0;height:3px;background:var(--live);width:0;z-index:11}\n  body.clean #hud,body.clean #prog{opacity:0}\n  @media (prefers-reduced-motion:no-preference){#prog{transition:width .14s linear}}\n</style>\n</head>\n<body>\n<div id="prog"></div>\n<div id="stage"><div id="deck">'
TAIL_PRE = '</div></div>'
TAIL_POST = '</div><div id="hud">\n  <span id="counter">1 / 66</span>\n  <span id="where"></span>\n  <span class="grow"></span>\n  <span>&larr; &rarr; SLIDE &middot; [ ] SECTION &middot; O OVERVIEW &middot; F FULLSCREEN &middot; C CLEAN</span>\n</div>\n<script>\n(function(){\n  var slides=[].slice.call(document.querySelectorAll(\'.slide\'));\n  var deck=document.getElementById(\'deck\');\n  var counter=document.getElementById(\'counter\');\n  var where=document.getElementById(\'where\');\n  var prog=document.getElementById(\'prog\');\n  var ovs=[].slice.call(document.querySelectorAll(\'.ov\'));\n  var cards=[];\n  slides.forEach(function(s,k){ if(s.classList.contains(\'sec\')) cards.push(k); });\n  var i=0;\n\n  function label(k){\n    var b=ovs[k]?ovs[k].querySelector(\'em\'):null;\n    if(!b) return \'\';\n    return b.textContent.replace(/^\\d+\\.\\s*/,\'\');\n  }\n  function show(n){\n    i=Math.max(0,Math.min(slides.length-1,n));\n    slides.forEach(function(s,k){s.classList.toggle(\'on\',k===i);});\n    ovs.forEach(function(b,k){b.classList.toggle(\'cur\',k===i);});\n    counter.textContent=(i+1)+\' / \'+slides.length;\n    where.textContent=label(i);\n    prog.style.width=(i/(slides.length-1)*100)+\'%\';\n    try{history.replaceState(null,\'\',\'#\'+(i+1));}catch(e){}\n  }\n  function fit(){\n    var s=Math.min(innerWidth/1920,innerHeight/1080);\n    deck.style.transform=\'translate(\'+((innerWidth-1920*s)/2)+\'px,\'+((innerHeight-1080*s)/2)+\'px) scale(\'+s+\')\';\n  }\n  addEventListener(\'resize\',fit); fit();\n\n  function fromHash(){var n=parseInt((location.hash||\'\').replace(\'#\',\'\'),10);return isNaN(n)?0:n-1;}\n  show(fromHash());\n  addEventListener(\'hashchange\',function(){if(fromHash()!==i)show(fromHash());});\n\n  function paper(dir){\n    var t=null;\n    for(var k=0;k<cards.length;k++){\n      if(dir>0&&cards[k]>i){t=cards[k];break;}\n      if(dir<0&&cards[k]<i)t=cards[k];\n    }\n    if(t!==null)show(t);\n  }\n\n  document.addEventListener(\'keydown\',function(e){\n    var k=e.key;\n    if(document.body.classList.contains(\'ov\')&&(k===\'Escape\'||k===\'o\'||k===\'O\')){\n      document.body.classList.remove(\'ov\');e.preventDefault();return;}\n    if(k===\'ArrowRight\'||k===\' \'||k===\'PageDown\'||k===\'j\'){show(i+1);e.preventDefault();}\n    else if(k===\'ArrowLeft\'||k===\'PageUp\'||k===\'k\'){show(i-1);e.preventDefault();}\n    else if(k===\']\'){paper(1);e.preventDefault();}\n    else if(k===\'[\'){paper(-1);e.preventDefault();}\n    else if(k===\'Home\'){show(0);}\n    else if(k===\'End\'){show(slides.length-1);}\n    else if(k===\'o\'||k===\'O\'){document.body.classList.add(\'ov\');\n      var c=ovs[i];if(c)c.scrollIntoView({block:\'center\'});e.preventDefault();}\n    else if(k===\'c\'||k===\'C\'){document.body.classList.toggle(\'clean\');}\n    else if(k===\'f\'||k===\'F\'){\n      if(document.fullscreenElement)document.exitFullscreen();\n      else if(document.documentElement.requestFullscreen)document.documentElement.requestFullscreen();}\n  });\n\n  ovs.forEach(function(b){b.addEventListener(\'click\',function(){\n    show(parseInt(b.dataset.i,10));document.body.classList.remove(\'ov\');});});\n\n  document.getElementById(\'stage\').addEventListener(\'click\',function(e){\n    show(e.clientX<innerWidth*0.28?i-1:i+1);});\n})();\n</script>\n</body>\n</html>\n'

def esc(s): return html.escape(s, quote=False)

def fig_file(stem):
    m = sorted(HERE.glob(f"figures/{stem}.*"))
    if not m: raise SystemExit(f"missing figure: {stem}")
    return f"figures/{m[0].name}"

def cite(stem):
    aid, loc = stem.split("_", 1)
    aid = re.sub(r"^cs(\d)", r"cs/\1", aid)
    short, first, date, title = PAPERS[aid]
    fn = re.search(r"F(\d+)", loc).group(1)
    kind = "Table" if loc.startswith("T") else "Fig."
    return f"{first} et al. &middot; {esc(short)} &middot; {kind} {fn} &middot; arXiv:{aid}", short, fn

def build():
    slides, ov = [], []
    thumb = (HERE / "thumbnail.jpg").exists()
    if thumb:
        slides.append(f'<section class="slide title"><img src="thumbnail.jpg" alt="{esc(TITLE)}"></section>')
        ov.append(('<img src="thumbnail.jpg" alt="" loading="lazy">', "Title"))
    else:
        slides.append(f'<section class="slide sec"><div class="secbody"><p class="num">hu-po &middot; {DATE}</p><h2>{esc(TITLE)}</h2></div></section>')
        ov.append(('<span class="ovcard"></span>', "Title"))
    n = len(SECTIONS)
    used = []
    for k, sec in enumerate(SECTIONS, 1):
        slides.append(f'<section class="slide sec"><div class="secbody"><p class="num">{k:02d} / {n:02d}</p>'
                      f'<h2>{esc(sec["title"])}</h2><p class="blurb">{esc(sec["blurb"])}</p></div></section>')
        ov.append(('<span class="ovcard"></span>', sec["title"]))
        for s in sec["slides"]:
            src = fig_file(s["fig"]); c, short, fn = cite(s["fig"])
            aid = s["fig"].split("_")[0]
            if aid not in used: used.append(aid)
            slides.append(f'<section class="slide fig"><div class="frame"><img src="{src}" alt="{esc(short)} figure {fn}"></div>'
                          f'<p class="ctx">{s["ctx"]}</p><p class="cite">{c}</p></section>')
            ov.append((f'<img src="{src}" alt="" loading="lazy">', f"{short} F{fn}"))
    # references, 45 per slide
    refs = []
    for aid in used:
        aid2 = re.sub(r"^cs(\d)", r"cs/\1", aid)
        short, first, date, title = PAPERS[aid2]
        refs.append(f'<div class="ref"><code>{aid2}</code><div class="t"><b>{esc(short)}</b><span>{first} et al. &middot; {date}</span></div></div>')
    for i in range(0, len(refs), 45):
        slides.append('<section class="slide refs"><div class="reflist">' + "".join(refs[i:i+45]) + '</div></section>')
        ov.append(('<span class="ovcard"></span>', "References"))
    ovh = '<div id="overview"><div class="ovgrid">' + "".join(
        f'<button class="ov" data-i="{i}">{img}<em>{i+1}. {esc(lab)}</em></button>' for i, (img, lab) in enumerate(ov)) + '</div>'
    out = HEAD.replace("{TITLE}", esc(TITLE)).replace("{DATE}", DATE) + "".join(slides) + TAIL_PRE + ovh + TAIL_POST
    (HERE / "slides.html").write_text(out)
    nfig = sum(len(s["slides"]) for s in SECTIONS)
    print(f"slides.html: {len(slides)} slides ({len(SECTIONS)} sections, {nfig} figures, {len(used)} papers)")
    # keep README references in sync
    rd = HERE / "README.md"
    if rd.exists():
        t = rd.read_text()
        links = "\n".join(f"- https://arxiv.org/abs/{re.sub(r'^cs(\d)', r'cs/\1', a)}" for a in used)
        t = re.sub(r"(### References\n)[\s\S]*$", r"\1\n" + links + "\n", t)
        rd.write_text(t)

if __name__ == "__main__":
    build()
