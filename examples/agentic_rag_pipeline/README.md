# Agentic RAG Pipeline

A retrieval-augmented generation pipeline lets an agent answer questions using relevant external documents instead of relying only on the model's memory.

## Why This Pattern Matters

This approach reduces hallucinations and improves accuracy by grounding responses in factual sources. It is especially important for business Q&A, support agents, and research assistants.

## Architecture Overview

```mermaid
flowchart LR
    Query --> Agent
    Agent --> Retriever
    Retriever --> Memory
    Memory --> Response
```

The user sends a **query**, which the **agent** receives and routes to a **retriever**. The retriever searches a **memory** store (documents, embeddings, or a vector database) for relevant context, then the agent uses that context to produce a grounded **response**.

## Setup

```bash
python example.py
```
