# Agentic RAG Pipeline

A retrieval-augmented generation pipeline lets an agent answer questions using relevant external documents instead of relying only on the model's memory.

## Why This Pattern Matters

This approach reduces hallucinations and improves accuracy by grounding responses in factual sources. It is especially important for business Q&A, support agents, and research assistants.

## Architecture Overview

```text
Question
  |
  v
Retriever
  |
  +--> search documents
  |
  v
Context injection
  |
  v
LLM response
```

## Setup

```bash
python example.py
```
