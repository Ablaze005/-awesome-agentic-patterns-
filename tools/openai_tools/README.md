# OpenAI Tool Calling Pattern

OpenAI tool calling allows models to decide when to call functions such as a search API, calculator, or database lookup. This turns a model into a practical agent that can operate on real tools.

## Why This Pattern Matters

A language model can generate text, but tools let it perform actions. This makes it valuable for automation, data retrieval, and workflow orchestration.

## Architecture Overview

```text
User request
   |
   v
Model
   |
   +--> Tool call detection
   +--> Function execution
   +--> Final answer
```

## Setup

```bash
pip install openai
```

## How to Run

```bash
python example.py
```

## Example Flow

- the model decides a tool is needed
- the tool returns structured output
- the model combines the result into a response
