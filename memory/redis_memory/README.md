# Redis Memory for Agent Context

Redis is a great fit for agent memory when you need fast, lightweight access to recent facts, conversation history, and temporary session state. This pattern stores a small memory layer in Redis so the agent can recall what happened in the last few turns without needing a large database or a full vector search stack.

## Why This Pattern Matters

Large language models do not retain memory between runs unless you add it yourself. A Redis-backed memory layer solves that by giving the agent:

- fast access to recent messages
- a place to store user preferences
- short-term task state for workflows
- a clean way to reset or refresh context

This is especially useful for chatbots, copilots, and support agents that need to remember recent context during a session.

## Architecture Overview

```text
User Message
     |
     v
Agent
     |
     +--> Redis Memory Store
     |       - session data
     |       - user preferences
     |       - recent conversation
     |
     +--> LLM / Tool Call
```

The agent saves important facts into Redis and reads them back before generating a response. This is simple, reliable, and fast.

## What This Example Does

This example demonstrates three common memory patterns:

- storing user preferences
- recording recent conversation events
- retrieving a compact memory summary before answering a question

## Setup

### 1. Install Redis

You can run Redis locally with Docker:

```bash
docker run --name redis-memory-demo -p 6379:6379 -d redis:7
```

### 2. Install the Python package

```bash
pip install redis
```

### 3. Run the example

```bash
python example.py
```

## How It Works

1. The script opens a Redis connection.
2. It stores a few user facts in a hash.
3. It appends recent interactions to a list.
4. It reads the stored values back and prints a memory summary.

This keeps the example simple while showing a practical memory pattern for real agents.

## Example Output

```text
Connected to Redis successfully.
User profile: {'name': 'Ava', 'preferred_language': 'Spanish', 'timezone': 'UTC+1'}
Recent messages:
- User: I am learning Spanish.
- Assistant: That is a great goal. Keep practicing.
- User: Please answer in Spanish.
Memory summary:
Name: Ava
Preferred language: Spanish
Timezone: UTC+1
Recent interactions: 3
```

## How to Run

```bash
python example.py
```

If Redis is not running, the script prints a clear message telling you how to start it.

## Best Practices

- Keep Redis memory focused on short-term context.
- Store only the data the agent actually needs.
- Expire old session state when it is no longer useful.
- Use a permanent database for long-term memory or retrieval features.

## When to Use This Pattern

Use Redis memory when:

- the agent needs session continuity
- your app is conversational and stateful
- you want a simple memory layer without a heavy vector database
- you need fast access to recent state and user context

This pattern is a solid foundation for episodic memory, session memory, and lightweight personalization.
