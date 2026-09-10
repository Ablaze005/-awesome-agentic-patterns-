# Qdrant Vectorstore Integration

Qdrant is a high-performance vector store useful for retrieval-based AI applications. This pattern keeps agent memory or knowledge retrieval fast and scalable.

## Why This Pattern Matters

When an agent needs to search across many documents, vector search is more flexible than a pure keyword match. Qdrant offers a modern, efficient way to store embeddings and retrieve relevant data.

## Architecture Overview

```text
Data / docs
   |
   v
Embedding model
   |
   v
Qdrant collection
   |
   +--> similarity search
   +--> relevant context
```

## Setup

```bash
pip install qdrant-client
```

## How to Run

```bash
python example.py
```
