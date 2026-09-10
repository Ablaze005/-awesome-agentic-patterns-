# Multi-Agent Chat Pattern

This pattern demonstrates how several agents can collaborate in a chat. Each agent holds a role, and together they produce a more complete answer.

## Why This Pattern Matters

Multi-agent chat mirrors how teams work: one agent gathers facts, another structures the answer, and another reviews it. This often leads to better outputs than one model acting alone.

## Architecture Overview

```text
User
  |
  v
Coordinator
  |
  +--> Researcher
  +--> Writer
  +--> Reviewer
```

## Setup

```bash
python example.py
```
