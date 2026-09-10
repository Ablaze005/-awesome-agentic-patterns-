# Custom Tool Router Pattern

A tool router decides which function should run based on the user's request. This keeps agent logic readable and supports clean fallbacks when no tool matches.

## Why This Pattern Matters

As tools grow, manually wiring every request becomes messy. A router keeps the code organized and reduces repetition.

## Architecture Overview

```text
Intent detection
   |
   +--> tool A
   +--> tool B
   +--> fallback
```

## Setup

No third-party package is required.

## How to Run

```bash
python example.py
```
