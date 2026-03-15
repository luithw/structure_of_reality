---
layout: post
title: "FAR Arena: A Transport Test for Artificial Spatial Intelligence"
date: 2026-03-15 01:21:30 -0700
author: Tim Lui
tags: [AI, artificial-spatial-intelligence, reinforcement-learning, consciousness, research]
excerpt: "A new benchmark for testing whether an artificial agent can rapidly acquire a usable internal map in a novel environment and survive by learning to forage, avoid danger, and return home."
---

Most AI benchmarks still let systems get away with the wrong kind of competence.

An agent can learn to classify images, imitate trajectories, or even solve reinforcement learning tasks in environments that look different on the surface while remaining structurally familiar underneath. But what happens when you drop an agent into a genuinely new place and ask it to survive?

That is the core question behind **FAR Arena**: **Forage-Avoid-Return**, a minimalist benchmark for what I call **Artificial Spatial Intelligence**.

The idea is simple to state and surprisingly demanding to solve. An agent lives in a partially observed 2D world. It must leave safety, find food, avoid danger, and make it back home before it dies. Then it must do it again. And again. Not in one familiar map, but in new environments it has never seen before.

This is not a benchmark about texture recognition, memorizing layouts, or exploiting visual shortcuts. It is about whether an artificial system can rapidly acquire a useful internal understanding of a novel space and use that understanding to stay alive.

## Why spatial generalization matters

A lot of machine learning progress has come from scaling pattern recognition. But spatial intelligence is a different kind of challenge.

If you place an animal in a new environment, it does not need thousands of gradient steps before it can begin forming a usable map. It explores, integrates partial observations, learns where safety is, notices which routes are risky, and gradually improves. That kind of rapid adaptation in a novel environment feels much closer to intelligence than simply performing well on another variation of the training set.

FAR is designed to target exactly that gap.

The benchmark strips away many of the usual shortcuts. Instead of giving the agent rich vision, it uses a sparse geometric sensor: a **1D ray-scan fan**, like a simple 2D LiDAR. Each observation is just a line of distances, optionally with lightweight semantic information such as whether a ray hit a wall, food, a predator, or home. On harder settings, even those labels can be removed.

This matters because single observations are often ambiguous. Different places can look locally similar. To succeed, an agent must integrate experience over time, remember where it has been, form a usable internal structure of the environment, and act under uncertainty.

That is the heart of spatial intelligence.

## The task: forage, avoid, return

FAR is built around a recurrent survival loop rather than a one-shot objective.

The world contains four key elements:
- an **agent** with limited energy,
- a **home zone** that functions as a safe haven,
- **food** that replenishes energy,
- and eventually **predators** that threaten survival.

The agent cannot simply wander forever. Energy drains over time. To remain viable, it must repeatedly:

1. leave home,
2. find food,
3. avoid threats,
4. and return home before it is too late.

This cyclic structure is important. It forces a balance between exploration, exploitation, risk management, and homing. A system that only survives by hiding at home fails. A system that greedily chases food but cannot return fails. A system that explores well but cannot respond to danger fails.

The benchmark is not asking whether an agent can solve a single navigation target. It is asking whether it can sustain an intelligent spatial life.

## The central evaluation: the Transport Test

The main evaluation in FAR is what I call the **Transport** or **Drop-In** test.

First, the agent is trained across a distribution of environments. Then it is dropped into a **new** environment distribution with a blank episodic state. Its recurrent hidden state is cleared. Its fast memory is reset. Its internal map buffer, if it has one, starts empty.

Then we measure how quickly it becomes competent.

Can it establish a safe route back to home? Can it complete a successful foraging excursion? Can it recover stable behavior after only limited interaction in the new world?

This is measured in two regimes:

- **Frozen-parameter Transport**: the agent's learned weights are fixed; only fast internal state may adapt.
- **Plastic Transport**: the agent is allowed controlled online learning after drop-in.

That distinction matters. If an agent adapts quickly in the frozen regime, then the adaptation is coming from its architecture and episodic mechanisms, not from slow parameter updates. That is a much stronger test of rapid spatial generalization.

## The scientific hypothesis

My central hypothesis is that the best-performing systems on this benchmark will not be simple reactive policies, and likely not even plain recurrent networks alone.

Instead, I expect strong performance to require something closer to a **complementary learning system**:

- a **fast, plastic subsystem** that rapidly encodes episode-specific spatial structure,
- and a **slow, stable subsystem** that stores general priors and reusable behavioral skills.

In neuroscience terms, this resembles a **hippocampus-cortex division**.

The fast tier should help the agent answer questions like:

- Where is home relative to where I am now?
- Which corridors have I already explored?
- Which route felt safe a minute ago?
- Where did I encounter food or danger in this particular episode?

The slow tier should carry broader knowledge:

- how to move effectively,
- what obstacle geometry tends to imply,
- how to respond to predators,
- and what exploratory behaviors work well across many environments.

The claim is not that biology must be copied literally. The claim is that **a separation between fast episodic structure and slow general priors may be necessary for rapid map acquisition under novelty**.

Importantly, this is falsifiable.

If a single-tier recurrent policy, with no explicit fast episodic mapping mechanism, consistently matches or beats two-tier systems on frozen-parameter Transport under strong geometry and dynamics shifts, then the hypothesis is weakened.

That is exactly the kind of result the benchmark is meant to uncover.

## A ladder of increasing difficulty

FAR is staged across several levels so that failures are interpretable.

### Level 0: Homing in empty space

This tests basic control, odometry, and return-to-home behavior without food or predators.

### Level 1: Fixed food, no predators

Now the agent must solve the basic forage-and-return loop. It has to explore, find resources, and make it back efficiently.

### Level 2: Stochastic food processes

Food is no longer fixed. It appears according to changing spatial and temporal statistics. This tests adaptive search under uncertainty.

### Level 3: Predators added

This is the full triad: forage, avoid, return. The agent must trade off reward-seeking against real danger.

Future versions may add hidden-information and adversarial scenarios, but the initial focus is on getting a clean and rigorous benchmark for fast spatial adaptation.

## Why the sensor design matters

One of the most important design choices in FAR is the use of a line-scan sensor rather than conventional vision.

This is deliberate.

With high-dimensional images, it is often hard to know what problem an agent is really solving. Is it learning geometry? Is it memorizing textures? Is it relying on artifact-level cues in the data? Sparse ray observations make the structure of the task much clearer.

They also make memory unavoidable.

A single ray-scan does not tell you where you are in a global sense. Many positions look similar. Home is not allowed to act as a long-range beacon by default. That means the task cannot collapse into "follow the beacon." If the agent wants to leave safety and come back successfully, it must build and use internal state.

This gives FAR a nice scientific property: when an agent succeeds, the success is much more likely to reflect actual spatial competence.

## Evaluation should be about viability, not reward tricks

Another principle behind FAR is that **life and death outcomes are the gold standard**, not reward engineering.

Reinforcement learning can still be used for training, but the benchmark is not defined by shaped reward. The final question is not whether the agent optimized a clever scalar objective in one training distribution. The real question is whether it remains viable under survival dynamics in novel environments.

That means the most important metrics are things like:

- survival time,
- successful excursion rate,
- home return reliability,
- energy efficiency,
- and adaptation speed after transport.

Reward shaping may still be useful as curriculum or scaffolding during training. But if a result depends entirely on finely tuned shaping, it is scientifically weak. The benchmark is meant to push toward robust behavioral competence, not clever exploitation of training signals.

## What should the baselines be?

To make the benchmark meaningful, FAR compares several increasingly capable agent families:

- reactive feed-forward policies,
- recurrent policies like LSTMs or GRUs,
- memory-augmented architectures,
- explicit two-tier complementary-learning-style agents,
- world-model and planning systems,
- and, where possible, classical mapping-plus-planning baselines.

This progression matters because it helps answer a deeper question: **what kind of architectural machinery is actually required for transport competence?**

If a reactive baseline fails badly, that is expected. If a recurrent network improves but still adapts slowly, that tells us something. If a two-tier architecture shows a major frozen-transport advantage, that is evidence for the core hypothesis. If classical mapping methods outperform everything, that is also informative.

The point is not to defend one ideology. It is to create a benchmark where architecture really matters and where the differences are measurable.

## FAR as a platform for automated scientific iteration

I also think FAR is valuable for another reason: it is a good substrate for the **automation of science**.

Each candidate agent design can be treated as a reproducible artifact. Each experiment run can become a node in a design tree with lineage, metrics, and natural-language notes. An LLM can then act as a hypothesis generator, proposing new architectures or edits based on prior failures and successes.

That creates a loop:

1. propose a new brain architecture,
2. evaluate it under a stable benchmark,
3. record results and failure modes,
4. branch the promising ideas,
5. repeat.

This only works if the infrastructure is disciplined. Agent interfaces must stay minimal. Evaluation suites must be stable. Seeds, environment versions, and artifact hashes must be tracked. Otherwise the scientific story becomes muddy.

But if done well, this kind of system could become a practical engine for discovering architectural principles rather than just tuning hyperparameters.

## What success would look like

A successful ASI-like agent in FAR should not merely score well. It should behave in recognizably intelligent ways after being dropped into a novel environment.

In the first moments after transport, I would expect it to:

- actively scan the geometry,
- infer whether the environment is open or maze-like,
- establish a safe return corridor to home,
- adapt its foraging routes based on what it encounters,
- and recover useful competence quickly rather than only after extensive online learning.

Quantitatively, I would expect:

- reactive systems to show a sharp train-to-test collapse,
- recurrent systems to do better but remain limited,
- and two-tier systems to show a clear advantage in time-to-competence and sustained viability under transport.

If that pattern appears, it would support the idea that fast episodic spatial memory is a core ingredient of artificial spatial intelligence.

If it does not, that is equally important. It would suggest either that the hypothesis is wrong or that simpler architectures are more powerful than expected.

Either way, we learn something real.

## Why I'm building this

At a deeper level, FAR is an attempt to push beyond benchmarks that mainly reward interpolation.

I am interested in a kind of intelligence that can enter a new world, build a usable internal model quickly, and act in a way that preserves its own viability. That feels closer to the foundations of animal cognition, and maybe closer to what robust embodied AI will require.

The benchmark is intentionally minimalist: sparse geometry, partial observability, cyclical survival pressure. But that simplicity is a strength. It makes the scientific question sharper.

Can we build an artificial system that does not just react, or optimize in-distribution, but **learns a place fast enough to live in it**?

That is what FAR is for.

---

This essay is part of the broader **Structure of Reality** series: an attempt to connect philosophy, intelligence, cognition, and AI engineering into one continuous line of inquiry.