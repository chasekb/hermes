---
name: productivity-workflows
description: "Class-level workflow for durable notes, office docs, OCR, PDFs, slides, and meeting artifacts."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [productivity, notes, documents, slides, ocr, traceability, office]
---

# Productivity Workflows

Use this umbrella when the task is about creating, transforming, or preserving human-facing work artifacts: notes, documents, slides, PDFs, OCR output, meeting summaries, and execution traces.

## Core loop
1. Identify the durable artifact that should exist when the task is done.
2. Decide whether the source of truth is a note, a doc, a deck, a PDF, or a trace record.
3. Capture only what is durable; keep transient chatter out of the final artifact.
4. Verify the artifact is readable, saved, and resumable.

## Workflow families

### Notes and traceability
Use for durable notes, action logs, decision records, and session summaries.
- Preserve evidence links.
- Separate progress from conclusions.
- Promote only stable outcomes.

### Office documents and collaboration
Use for docs, spreadsheets, and shared workspace artifacts.
- Keep edits concrete and reviewable.
- Prefer structured content over long freeform prose when possible.

### PDFs and OCR
Use for extracting text, cleaning documents, and editing PDF content.
- Extract first, then transform.
- Validate the resulting text before treating it as authoritative.

### Slides and presentations
Use for decks and speaker-ready presentation artifacts.
- Build around one main idea per slide.
- Keep the deck consistent with the source material.

### Meeting and workflow pipelines
Use for recurring pipelines that transform meetings or other events into durable outputs.
- Verify the pipeline is actually fireable.
- Check the output format and destination before declaring success.

## Decision rules
- If the task produces a durable note or decision log, keep the traceability explicit.
- If the task converts source material into a cleaner artifact, validate the transformed output before closing.
- If the task is a repeatable pipeline, verify the live run path instead of relying on configuration alone.

## Pitfalls
- Do not store transient progress as durable knowledge.
- Do not overwrite the source evidence when summarizing it.
- Do not assume a pipeline is working just because it is configured.
- Do not mix raw OCR output, cleaned text, and final publication copy.

## Legacy subclasses absorbed into this umbrella
This class-level workflow replaces the narrower standalone skills for traceability, notes, office docs, OCR/PDF handling, slides, and meeting pipelines.
