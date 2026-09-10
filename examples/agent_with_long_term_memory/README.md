# Agent With Long-Term Memory

This example shows how an agent can keep persistent memories across sessions and use them to personalize future replies.

## Why This Pattern Matters

Memory is what turns a stateless model into a long-lived assistant. This is especially useful for personalization, reminders, and continuity across conversations.

## Architecture Overview

```text
User conversation
   |
   v
Memory store
   |
   +--> profile
   +--> preferences
   +--> past tasks
   |
   v
Agent prompt injection
```

## Setup

```bash
python example.py
```

## How to Run

```bash
python example.py
```
