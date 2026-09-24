# 2026.09.25 analysis (research rounds 1–3, trimmed to 3 themes)

## The week in 3 sentences

1. The top of the ledger is harness self-improvement: RRSI (Google, 174 HF upvotes) and SoL-Pi (NVIDIA, 129) both run RSI at the harness layer, a week after the 09.18 RSI stream.
2. Video world models add 3D-aware memory and geometry-native latents, and push toward playable, real-time control.
3. Robot papers put explicit grounding under the policy (3D objects, action tokens, world-model features, a VLM command interface) instead of relying on end-to-end VLA scale.

## Themes

**t1 Harness self-improvement (4).** SoL-Pi searches harnesses with scaled auto-research loops, RRSI regularizes the edits so gains survive out of distribution, and Harness-Zero distills harness behavior back into the weights. EvoOntology carries the idea past the harness: a semantic layer that data agents revise from execution feedback. Threads: ADAS (2408.08435) for workflow search, Voyager (2305.16291) for skills that grow during deployment, and a callback to 09.18. Risk: overlap with 09.18, so lead with what is new (OOD transfer, harness→weights).

**t2 World models with memory and geometry (4).** WorldCrafter (camera-queryable implicit 3D memory), GAE (a geometry-native latent space shared by perception and generation), JEPA-Anything (one predictive recipe across seven world domains) and Zing-0.5 (a 5B playable world model with joint keyboard and text control). Threads: VGGT (2503.11651), Self Forcing (2506.08009). Callback: 09.11 World Action Models.

**t3 Grounding robot policies (4).** GAM (3D object grounding as the foundation), RoboDawn (an agentic VLM drives the robot through discrete commands), ActionPiece (action tokenization that keeps adjustments across demonstrations) and THAW (world-model representations distilled into a compact VLA, which bridges t2 into t3). Threads: RT-2, OpenVLA. Callback: 09.11.

## Visuals

At most 2 per paper, 23 in all, each one looked at in research round 2: 16 arXiv figures and 7 web media.
- t1: SoL-Pi's proposal-tree teaser video, RRSI's overview and evolve-vs-OOD gain scatter, the Harness-Zero diagram, EvoOntology's content-layer diagram.
- t2: WorldCrafter's teaser and classroom revisit video, GAE's overview and progressive RGB/geometry video, JEPA-Anything's scenario atlas and ten-task results, Zing-0.5's sled-rider control strip and data pipeline.
- t3: GAM's grounding teaser and out-of-distribution sorting video, RoboDawn's teaser and overview, ActionPiece's overview and rank-consistency figure, THAW's size-vs-accuracy figure and real-robot rollouts.

## Left out, and why

On 09.24 the research was trimmed from 9 themes (58 papers, 168 visuals) to these 3. The cut themes are in the git history of this file. They were harness-adjacent self-evolving skills (EvoOntology kept, in t1), code as the RL environment, research swarms, on-policy distillation, long-context cost, and full-duplex voice agents.
- Within the kept themes: the Zoom harness-design study, Weco, Designer-RSI, co-evolving harnesses (t1); Video DeltaNet, physics-violating attention, GameHorizon (t2); in-context robot learning, HuRo, Fingers as Legs (t3).
- **LimiX-2** (2609.17488, the most-upvoted paper of the week) fits no theme. Its F12 parameter-scaling curve would work as a one-off slide.

## News (cold open, no slides unless noted)

Claude Opus 5.5 (Sep 22, has accuracy-vs-cost charts), GPT-6 Sol/Luna (Sep 22), MiMo-V2.6 open weights (Sep 22), Grok 4.7 (Sep 21).
