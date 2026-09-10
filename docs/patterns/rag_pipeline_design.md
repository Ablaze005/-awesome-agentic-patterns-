# RAG Pipeline Design

A retrieval-augmented generation pipeline connects an external knowledge source to a model. The goal is to ground answers in context retrieved from documents or databases.

## Typical Pipeline

1. Accept a user question.
2. Search for relevant documents.
3. Combine those documents with the prompt.
4. Ask the model to answer using that context.
5. Return a grounded answer.

## Benefits

- better factual accuracy
- reduced hallucination
- support for domain-specific knowledge
