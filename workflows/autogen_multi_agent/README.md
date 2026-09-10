# AutoGen Multi-Agent Pattern

AutoGen is designed for conversations among multiple agents. Each agent can play a specialized role such as planner, researcher, or summarizer. This pattern is useful when the task is too complex for a single model call.

## Why This Pattern Matters

Multi-agent systems help divide complex work into smaller, specialized tasks. This improves reasoning, lowers context overload, and creates natural collaboration between agents.

## Architecture Overview

```text
User request
   |
   v
Coordinator
   |
   +--> Researcher
   +--> Writer
   +--> Reviewer
   |
   v
Final response
```

## Setup

```bash
pip install pyautogen
```

## How to Run

```bash
python example.py
```

## Example Flow

- coordinator receives the task
- specialized agents contribute ideas
- final output is combined into one answer
