---
name: creative-content-workflows
description: "Class-level workflow for creative outputs: diagrams, mockups, visual art, animation, audio, music, and presentation-ready assets."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [creative, design, diagrams, mockups, art, animation, audio, music, visuals]
---

# Creative Content Workflows

Use this umbrella when the goal is to produce a creative artifact rather than a utilitarian answer.

## Core idea
Choose the medium first, then optimize for clarity, consistency, and deliverability.

## Workflow families

### Diagrams and structured visuals
Use when the output is an architecture diagram, flowchart, sequence diagram, infographic, or hand-drawn schematic.
- Keep the visual hierarchy obvious.
- Prefer labeled components and readable spacing.
- Match the style to the audience and purpose.

### Mockups and design prototypes
Use when the output is a landing page, slide mockup, throwaway concept, or design system exercise.
- Build fast variants first.
- Compare alternatives before polishing.
- Keep the mockup self-contained and easy to revise.

### Generative art and interactive visuals
Use when the output is a visual experiment, sketch, animation, or code-driven scene.
- Decide whether the goal is static art, motion, or interaction.
- Keep parameters visible and adjustable.
- Prefer reproducible setups over one-off magic.

### Audio and music
Use when the output is a song, sound design, or music prompt.
- Separate lyrical intent, sonic style, and structural cues.
- Keep the prompt specific enough to reproduce.
- Verify that the delivered artifact matches the requested mood and format.

### Text shaping and ideation
Use when the task is to humanize prose, generate ideas, or polish creative wording.
- Preserve the underlying meaning.
- Remove generic filler.
- Make the voice match the intended audience.

## Decision rules
- If the output will be used by humans as an artifact, choose the medium explicitly.
- If the task mixes multiple media, decide the primary deliverable before generating anything.
- If there are multiple style options, draft variants before committing.

## Pitfalls
- Do not overfit to the tool instead of the audience.
- Do not make the visual pretty but unreadable.
- Do not bake in too much style before the composition is right.
- Do not leave generative prompts vague when a reproducible output is needed.

## Legacy subclasses absorbed into this umbrella
This class-level workflow replaces the narrower standalone skills for diagrams, mockups, infographic design, visual art, animation, audio generation, music prompting, text humanization, and creative browser demos.
