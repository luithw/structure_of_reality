---
layout: post
title: "From Surviving to Foraging: A Step Toward Artificial Spatial Intelligence"
date: 2026-04-26
description: "FAR Arena's latest PhaseAware CLS result shows a shift from passive survival toward active foraging, while transport generalization remains unsolved."
tags: [artificial-intelligence, artificial-spatial-intelligence, far-arena, reinforcement-learning, spatial-intelligence]
---

One of the easiest traps in reinforcement learning is to mistake survival for intelligence.

In our FAR Arena experiments, earlier agents learned to stay alive for a while, but they often failed at the actual task: leave home, search for food, collect it, and return. A policy that survives by doing very little can look deceptively good if the metric is survival time alone. But spatial intelligence is not just about avoiding death. It is about competent movement through space under uncertainty.

Our latest PhaseAware CLS agent shows an important shift: it begins to learn the foraging loop itself.

## The Problem: Survival Is Not Enough

In the FAR Arena benchmark, the agent must operate in a 2D environment using local sensory information. The desired behavior is simple to describe but hard to learn:

1. Start from home.
2. Explore outward.
3. Find food.
4. Return home.
5. Repeat under changed geometry.

Earlier RNN agents sometimes achieved decent survival. One prior run reached strong transport survival and reasonable home-return reliability, but still collected no food. That is not spatial competence. It is a survival policy that avoids the core challenge.

The key question became: how do we bias the agent toward genuine spatial behavior rather than passive survival?

## The New Agent: PhaseAware CLS

The latest agent introduces a more structured architecture inspired by complementary learning systems and animal navigation.

Instead of asking a plain recurrent network to learn everything from scratch, the PhaseAware CLS agent combines several inductive biases:

### 1. Phase-aware control

Foraging is not one behavior. It is at least two:

- outbound exploration
- inbound return-home behavior

A single undifferentiated policy can easily confuse these modes. The new agent explicitly models behavioral phase, allowing it to treat “search for food” and “return home” as different control regimes.

This matters because the correct action depends heavily on context. Moving away from home may be good while searching, but disastrous when energy is low or food has been found. Phase awareness gives the policy a scaffold for switching between these regimes.

### 2. Complementary learning systems

The agent uses a CLS-style design: fast episodic spatial memory plus slower neural policy learning.

Biological intelligence appears to rely on this kind of division. The hippocampal system supports rapid memory for places and episodes, while cortical systems learn slower reusable structure. In the FAR Arena setting, this means the agent does not have to compress all spatial experience into a recurrent hidden state. It can store recent spatial evidence explicitly.

### 3. Episodic spatial memory

The agent maintains a lightweight spatial grid that records useful context such as visited regions, food encounters, home-relative information, and trajectory history.

This gives the agent something like a minimal spatial memory. It can avoid treating every moment as isolated. If it has searched a region, encountered food, or moved away from home, that information remains available to guide later behavior.

This is likely one of the reasons food collection improved: the agent has a better inductive bias for spatial search.

### 4. A rule-prior residual scaffold

The agent is not purely neural from the first timestep. It is guided by a simple forage-return behavioral prior, and the neural network learns residual corrections on top of it.

This is important. In sparse spatial tasks, learning everything from random exploration is extremely inefficient. A weak hand-designed prior gives the system a behavioral backbone: move outward, search, and attempt to return. The neural policy can then refine rather than invent the entire loop from scratch.

### 5. Event-based reward shaping

The training setup rewards meaningful spatial events, not just survival. Finding food, returning home, completing excursions, and moving efficiently are all treated as important signals.

This shifts optimization away from “stay alive somehow” and toward “perform the spatial task.”

## The Result

The latest PhaseAware CLS Level 1 run completed with a notable behavioral improvement.

Training evaluation showed:

- Mean survival: about 181 steps
- Best survival: 600 steps
- Mean food collected: 6.5
- Best training food: 20
- Excursion success rate: 10%
- Home-return reliability: 20%

The key number is not survival. It is food.

Earlier agents could sometimes survive but collected little or no food. This agent collected food consistently in the training layout. That means it began to learn the actual foraging behavior, not just a degenerate survival strategy.

In other words, we have moved from “stay alive” toward “go out and get something.”

That is a meaningful step.

## The Caveat: Transport Still Fails

The result is not a solved benchmark.

Under geometry transport, performance dropped sharply:

- Transport survival: about 72 steps
- Transport excursion success: 0%
- Transport home-return reliability: 20%
- Transport food collection remained weak

This shows that the agent’s competence is still brittle. It can learn a foraging loop in the training geometry, but the behavior does not yet generalize robustly when the environment changes.

That distinction matters. Artificial spatial intelligence should not merely memorize one arena. It should transfer spatial strategies across layouts.

So the current result is best understood as a transition point:

- We have improved task acquisition.
- We have not yet achieved robust transport generalization.

## Why This Matters

This finding supports a broader hypothesis: spatial intelligence may require structured memory and behavioral organization, not just larger recurrent policies.

The plain RNN approach can learn useful temporal patterns, but it struggles to discover the full forage-return loop from sparse feedback. The PhaseAware CLS agent improves because it decomposes the problem:

- memory handles recent spatial experience
- phase handles behavioral mode
- the rule prior supplies initial competence
- the neural network learns corrections
- reward shaping emphasizes task events

This combination makes the learning problem more natural.

The agent is still far from human or animal-like spatial competence. But the direction is promising: instead of optimizing for a scalar reward and hoping navigation emerges, we are building architectures that reflect the structure of spatial behavior.

## The Next Step

The next challenge is transport.

To improve generalization, we likely need stronger home-anchored exploration and less geometry-specific learning. Several directions are now obvious:

1. Increase or stabilize rule-prior authority during early training.
2. Add explicit outbound/inbound phase supervision.
3. Train on randomized geometries rather than a single layout.
4. Penalize brittle memorization and over-revisitation.
5. Strengthen the spatial memory readout so the policy uses relational cues, not just local habits.
6. Evaluate trajectories visually to see where the transport behavior collapses.

The goal is not simply to get a higher score. The goal is to discover the architectural ingredients required for agents that can understand and reuse space.

## Conclusion

The latest PhaseAware CLS experiment shows a real improvement: the agent began to forage.

That may sound small, but it is a crucial distinction. A system that survives without collecting food has learned to avoid failure. A system that leaves home, finds food, and attempts to return has begun to solve the spatial problem.

We are not at robust artificial spatial intelligence yet. But this result suggests that the path forward is not just bigger networks or longer training. It is better structure: phase-aware behavior, fast spatial memory, learned residual control, and task-aligned training signals.

The shift from passive survival to active foraging is the first sign that the architecture is pointing in the right direction.
