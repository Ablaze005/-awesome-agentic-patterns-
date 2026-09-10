# Supabase Backend Pattern

This backend pattern uses Supabase as a lightweight application backend for agent state, metadata, or conversation logs. It is a practical option when you want storage with a managed Postgres layer.

## Why This Pattern Matters

Agent backends often need quick persistence, row-level security, and data access APIs. Supabase provides a clean path to store and retrieve app data without building a custom backend.

## Architecture Overview

```text
Agent
  |
  v
Supabase table
  |
  +--> app state
  +--> session metadata
  +--> conversation rows
```

## Setup

```bash
pip install supabase
```

## How to Run

```bash
python example.py
```
