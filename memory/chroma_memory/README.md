# Chroma Memory for Semantic Recall

Chroma is a lightweight vector database designed for semantic search. It helps an agent store embeddings and retrieve the most relevant memories for a user query. This pattern is useful when the agent needs to remember concepts, notes, and past interactions beyond simple key-value storage.

## Why This Pattern Matters

Traditional memory systems often store raw text with no concept of similarity. A vector store lets the agent search by meaning, not just exact wording. That makes memory retrieval more useful for long-term personalization, research assistants, and document-aware agents.

## Architecture Overview

```text
User query
   |
   v
Agent
   |
   +--> Embedding model
   |
   v
Chroma collection
   |
   +--> Matching memories
   |
   v
Context injection
```

## Setup

```bash
pip install chromadb
```

Then run:

```bash
python example.py
```

## How to Run

```bash
python example.py
```

## Example Flow

1. Encode a few memories into embeddings.
2. Add them to a Chroma collection.
3. Search for similar text.
4. Print relevant memories to the console.

## Best Use Cases

- long-term agent memory
- knowledge base lookup
- personalized recommendation logic
- search over notes and documents
