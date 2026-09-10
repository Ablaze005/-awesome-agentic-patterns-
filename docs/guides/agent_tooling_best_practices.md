# Agent Tooling Best Practices

## Principles

- keep tools small and explicit
- validate arguments before tool execution
- separate tool definitions from tool logic
- log tool calls for debugging and monitoring
- provide clear error messages

## Common Mistakes

- exposing too many tools at once
- making tool names ambiguous
- letting tool results bypass validation
- hiding failures behind generic messages

## Good Pattern

A simple router can decide whether a request should use a search, calculator, or fallback flow. This keeps the behavior predictable and easy to extend.
