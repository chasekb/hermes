---
name: apple-personal-workflows
description: "Class-level workflow for Apple-native personal tools and Mac desktop control."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [apple, notes, reminders, messaging, findmy, macos, desktop]
---

# Apple Personal Workflows

Use this umbrella when the task is about Apple-native personal workflows rather than general web or terminal automation.

## Core idea
Choose the Apple surface that already owns the data or action:
- notes for quick durable capture
- reminders for tasks and follow-up
- messaging for communication
- Find My for device/location lookup
- Mac desktop control for UI-driven actions

## Workflow families

### Notes and reminders
- Capture concise items.
- Keep titles and bodies specific.
- Use reminders for actionable follow-up rather than freeform notes.

### Messaging
- Use the native messaging channel when the user wants a real message sent.
- Confirm the target carefully when multiple people or threads exist.

### Find My and device lookup
- Use device-aware commands for locating people, devices, or AirTags.
- Prefer the most direct lookup path before escalating.

### Mac desktop control
- Use desktop control only when a direct API or CLI is not available.
- Keep UI actions short, observable, and recoverable.

## Pitfalls
- Do not confuse a note with a reminder.
- Do not send a message to the wrong thread or contact.
- Do not use desktop control when a direct app/tool command exists.
- Do not assume a device is missing before checking the live status.

## Legacy subclasses absorbed into this umbrella
This class-level workflow replaces the narrower standalone skills for Apple notes, reminders, messaging, Find My, and Mac desktop control.
