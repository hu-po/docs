# 2026.09.25 analysis (research rounds 1–3)

## The week in 5 sentences

1. The top of the ledger is harness self-improvement: RRSI (Google, 174 HF upvotes) and SoL-Pi (NVIDIA, 129) both run RSI at the harness layer, a week after the 09.18 RSI stream.
2. The biggest cluster by count turns code into training ground: codebases, scientific repos and running apps become verifiable RL environments and skills (CodeMidas, ScienceIDE, RecreationWorld, ProgramDistill, Code2Skill).
3. Multi-agent research systems now run for days (Agora, Agensh, Stellar Colosseum, Lean Pool), and in the same week papers report cheating, collusion and weak taste.
4. Outside agents, video world models add 3D-aware memory and geometry-native latents, and robot papers put explicit grounding under the policy.
5. Five papers take on-policy distillation apart, and DeepSeek-V4.1-Flash leads a smaller cluster on the cost of long context.

## Themes

**t1 Harness self-improvement (7).** RRSI, SoL-Pi, the Zoom harness-component study, Harness-Zero, co-evolving harnesses, Weco, Designer-RSI. What ties them: the scaffolding around a frozen model gets optimized with ML tools (regularization, scaling, ablation, distillation). Threads: ADAS (2408.08435) and AFlow (2410.10762) as the workflow-search ancestors, SWE-agent (2405.15793) for the agent-computer interface, and a callback to 09.18. Risk: overlaps 09.18 heavily, so lead with what is new (overfitting and OOD transfer, harness→weights).

**t2 Code becomes the environment (7).** CodeMidas, ScienceIDE, RecreationWorld, ProgramDistill, Code2Skill, FrogNano, DSec. RecreationWorld and ProgramDistill share one idea: recover behavior from a running reference. Threads: SWE-bench (2310.06770), SWE-smith (2504.21798), Terminal-Bench (2601.11868).

**t3 Research swarms (7).** Agora, Agensh, Stellar Colosseum, Lean Pool, emergent cheating, emergent collusion, Taste-Bench. Scale and failure modes side by side. Threads: AI Scientist-v2 (2504.08066), Generative Agents (2304.03442).

**t4 Self-evolving skills, indexes and memory (6).** GUI skill revision, GraphSkillEvo, EvoOntology, Self-Evolving Search Index, Procedural Graphs, EvolveTrade. Weakest signals of the eight (hf 15–140), but the visuals hold up: each paper has an overview diagram plus an improvement-over-evolution-rounds curve, so it stays its own section. If it has to shrink, EvolveTrade is the weakest fit. Threads: Voyager (2305.16291), Reflexion (2303.11366).

**t5 World models with memory and geometry (7).** WorldCrafter, GAE, Zing-0.5, Video DeltaNet, physics-violating attention, JEPA-Anything, GameHorizon. Likely the best project-page videos. Callback: 09.11 World Action Models. Threads: Wan, Self Forcing, VGGT.

**t6 Grounding robot policies (7).** GAM, RoboDawn, ActionPiece, in-context robot learning, world-model→VLA distillation, HuRo, Fingers as Legs. Callback: 09.11. Threads: RT-2, OpenVLA.

**t7 On-policy distillation, taken apart (6).** EOS mismatch, privileged information, 1% tokens, discrepancy calibration, RetireOPD, plus PPO value flattening (RL-side sibling). Thread: GKD (2306.13649). Expect result curves; check legibility.

**t8 Paying for long context (6).** DeepSeek-V4.1-Flash, Fathom, MoE-from-SSD, Flash-dLLM, SpectralShift, Complex KDA. Thread: PagedAttention, FlashAttention.

**t9 Talking while the agent works (5).** Realtime-Venus, Gander (Multimodal Duplex Interaction Agent), StepAudio 3 Realtime, SteerDuplex, OmniVChat. What ties them: a full-duplex voice/video model is the live frontend (listening, backchanneling, taking interruptions) while a separate loop reasons or runs tools in the background and returns results mid-conversation. Realtime-Venus literally delegates to a "Harness", which links this theme to t1. Gander and StepAudio 3 Realtime are from the 3 weeks before the window (`recent`), but they are the clearest diagrams of the split. Threads: Moshi (2410.00037, the base model SteerDuplex fine-tunes), and a callback to the 2024.09.27 Voice Mode stream. This is also the setup Hugo streams with (talking to a voice agent live).

## Visuals (round 2)

All 53 themed papers now have 1–3 looked-at figures (157 visuals: 131 arXiv figures, 26 web media). Bad auto-crops were redone from the PDF. CodeMidas had no extractable figures and now has three manual crops.
- t1: SoL-Pi's proposal-tree teaser video, RRSI's evolve-vs-OOD gain scatter, Weco's rewrite trajectory. Harness-Zero and 2609.09134 have one diagram each.
- t2: the RecreationWorld reference/recreation screenshot pair (Food Truck app) and the ProgramDistill explainer video are the anchors. DSec is infrastructure, so it fits best as the closer.
- t3: Agora's 12-day contribution timeline, Agensh's 1→1,024-agent curve, the collusion comic, the Taste-Bench decision fork. Stellar Colosseum and the cheating case study have one figure each.
- t5: revisit-consistency grids with point clouds (WorldCrafter, GAE) and small before/after physics videos.
- t6: real-robot video for GAM, THAW, HuRo and Fingers-as-Legs. RoboDawn, GPT-Policy and ActionPiece have figures only.
- t7: mostly training-dynamics curves. 2609.21619 F1 and RetireOPD F3 are the concept diagrams.
- t8: DeepSeek's KV-bytes-per-token chart (model card) and decode-FLOPs-vs-context curve open it.

## Visuals (round 3)

- t9: Realtime-Venus's example-interaction strip (proactive alert, delegation, interruption) plus its two-loop system diagram and benchmark radars from the project page; Gander's teaser and its delegate/keep-chatting/revise/deliver timeline; StepAudio's Think-While-Speaking and 320 ms state-token diagrams; SteerDuplex's steerability taxonomy and a re-cropped SFT-vs-RL barge-in chart (the auto crop included a table); OmniVChat's data-studio flow and RL curves (from the README).
- Looked at and not used: Gander's demo videos (Chinese UI, small text, mostly empty screen), OmniVChat's README GIFs and Figure 1 (silent selfie clips, a portrait strip), and MiniMax-H3's result grids (half prompt text).

## Left out, and why

- **MiniMax-H3 physical-reasoning eval** (2609.18323): an omni *generation* eval, not duplex interaction, and its figures are text-heavy prompt grids.
- **LimiX-2** (2609.17488, 659 upvotes, the most-upvoted paper of the week): tabular foundation model, and it doesn't cluster with anything. It could be a one-off slide if Hugo wants it (figures pulled: the Elo overview F1 and the parameter-scaling curve F12 are the candidates).
- **Image generation/editing** (Paint-Anything, UFO, RULER SVG, StableVQ): scattered, with no shared idea.
- Education, safety benchmarks, fraud detection, domain benchmarks: single papers, and they don't cluster.
- Math proofs (Komlós, Sylvester), which have no visuals.

## News (cold open, no slides unless noted)

Claude Opus 5.5 (Sep 22, has accuracy-vs-cost charts), GPT-6 Sol/Luna (Sep 22), MiMo-V2.6 open weights (Sep 22), Grok 4.7 (Sep 21). DeepSeek-V4.1-Flash launched Sep 10 (outside the window), and its paper is in t8.
