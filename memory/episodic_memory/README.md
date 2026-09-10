# Episodic Memory Pattern

Episodic memory stores events in sequence so an agent can remember what happened, in what order, and how it responded. This pattern is especially useful for interactive assistants that need to keep track of recent experiences and user interactions over time.

## Why This Pattern Matters

Agents often need more than static facts. They also need event history: what the user asked, what the assistant did, and what happened next. Episodic memory keeps that trail in a readable form that is easier to reason about than a raw log.

## Architecture Overview

```text
Time-based event stream
   |
   +--> Event 1: user asks for summary
   +--> Event 2: assistant explains topic
   +--> Event 3: user requests follow-up
   |
   v
Agent memory layer
   |
   +--> recent events
   +--> timestamps
   +--> summary context
```

## How It Works

- record important moments
- attach timestamps
- keep an ordered event log
- recall recent experiences before answering

## Setup

No external dependencies are required for the simple version shown here.

```bash
python example.py
```

## Example Flow

1. Add an event to the memory list.
2. Save a short summary.
3. Retrieve the last few events.
4. Summarize the current context.
