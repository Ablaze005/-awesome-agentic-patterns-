# Memory Architecture Overview

Agents commonly need multiple memory layers:

- short-term memory for the current conversation
- episodic memory for recent events
- semantic memory for similar or related facts
- persistent memory for user preferences or long-term context

A layered design keeps the system flexible. For example, a Redis store may handle session state, while a vector store can search embeddings for related memories.
