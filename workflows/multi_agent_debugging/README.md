# Multi-Agent Debugging Pattern

This debugging pattern provides a unified way to log:

- Agent messages
- Tool calls
- Memory writes/reads

## Components

### 1. Logger Utility (`logger.py`)
Handles structured logging into `agent_debug.log`.

### 2. Debug Wrapper (`debug_wrapper.py`)
Wraps any agent and intercepts:
- `.send()`
- `.call_tool()`
- `.update_memory()`

### 3. Example Script (`example_debugging.py`)
Shows two agents interacting with full debugging enabled.

## Expected Output
A complete debugging workflow with:
- Logs
- Example usage
- Documentation
