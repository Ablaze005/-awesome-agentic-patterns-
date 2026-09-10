# Anthropic Tools Pattern

This pattern follows the same principle as OpenAI tool calling, but with an Anthropic-focused design. It is useful when you want a model to use functions in a structured and controlled way.

## Why This Pattern Matters

Tool use gives the model a way to access live data and perform actions. This is a key building block for production-grade agents.

## Architecture Overview

```text
Prompt
  |
  v
Model
  |
  +--> Tool selection
  +--> Tool execution
  +--> Final synthesis
```

## Setup

```bash
pip install anthropic
```

## How to Run

```bash
python example.py
```
