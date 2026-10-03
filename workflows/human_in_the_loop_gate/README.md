# Human-in-the-Loop Approval Gate

High-impact agent tools (file deletion, outbound email, code execution) should not run without explicit approval. This pattern wraps tool execution with a simple risk check and approval gate so unsafe calls are blocked until a human confirms them.

## Why This Pattern Matters

Autonomous agents can act quickly, but some actions are irreversible or sensitive. A lightweight approval gate keeps low-risk tools fast while forcing review for dangerous ones.

## Architecture Overview

```text
Tool call request
   |
   +--> low risk  --> execute immediately
   |
   +--> high risk --> blocked until approved --> execute
```

## How It Works

- classify tools by risk level
- allow safe tools to run without friction
- block high-risk tools until approval is recorded
- execute approved tools on the next attempt

## Setup

No external dependencies are required.

```bash
python example.py
```

## Limitations

- approval is in-memory only in this example
- production systems should persist approvals and tie them to authenticated users
- consider timeouts and scoped approvals for multi-step workflows
