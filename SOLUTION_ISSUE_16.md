# Solution for Issue #16

## 🛠️ Proposed Solution (by Aditya Waghamare)

### Analysis
Autonomous AI agents require robust, structured observability pipelines to capture intermediate thoughts, tool calls, state changes, errors, and conversation histories in real-time. This pattern introduces a production-ready Python implementation featuring structured JSON logging, event tracers, error hooks, and OpenTelemetry integration.

### Fix
Add `patterns/agent_logging_monitoring.py` demonstrating comprehensive agent tracing, structured logging, and observability.

### Implementation
```python
"""
Agent Logging & Monitoring Pattern
Author: Aditya Waghamare <adityawaghamare7620@gmail.com>

Provides a production-grade pattern for logging agent tool calls, state transitions,
errors, conversation history, and OpenTelemetry spans.
"""

import json
import logging
import sys
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

# Optional OpenTelemetry integration (graceful fallback if not installed)
try:
    from opentelemetry import trace
    from opentelemetry.trace import Status, StatusCode
    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False


class AgentState(str, Enum):
    IDLE = "IDLE"
    THINKING = "THINKING"
    CALLING_TOOL = "CALLING_TOOL"
    ERROR = "ERROR"
    COMPLETED = "COMPLETED"


@dataclass
class AgentLogEntry:
    timestamp: float
    state: str
    event_type: str
    details: Dict[str, Any]
    conversation_history_length: int


class StructuredJSONFormatter(logging.Formatter):
    """Outputs logs in structured JSON format for easy ingestion into Datadog, ELK, etc."""
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": record.created,
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if hasattr(record, "agent_data"):
            log_record["agent_data"] = record.agent_data
        return json.dumps(log_record)


class MonitoredAgent:
    def __init__(self, name: str, enable_otel: bool = True):
        self.name = name
        self.state = AgentState.IDLE
        self.conversation_history: List[Dict[str, str]] = []
        self.logs: List[AgentLogEntry] = []
        
        # Setup Logger
        self.logger = logging.getLogger(f"Agent.{name}")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(StructuredJSONFormatter())
            self.logger.addHandler(handler)
            
        # Setup OpenTelemetry tracer if requested and available
        self.tracer = None
        if enable_otel and OTEL_AVAILABLE:
            self.tracer = trace.get_tracer(f"agent.{name}")

    def _transition_state(self, new_state: AgentState, event_type: str, details: Dict[str, Any]):
        old_state = self.state
        self.state = new_state
        entry = AgentLogEntry(
            timestamp=time.time(),
            state=new_state.value,
            event_type=event_type,
            details={"previous_state": old_state.value, **details},
            conversation_history_length=len(self.conversation_history)
        )
        self.logs.append(entry)
        
        self.logger.info(
            f"State transition: {old_state.value} -> {new_state.value} [{event_type}]",
            extra={"agent_data": entry.__dict__}
        )

    def run_step(self, user_input: str, tool_fn: Callable[[str], str]) -> str:
        self.conversation_history.append({"role": "user", "content": user_input})
        self._transition_state(AgentState.THINKING, "user_input_received", {"input": user_input})

        # Optional OpenTelemetry span
        span = None
        if self.tracer:
            span = self.tracer.start_span(f"{self.name}.execute_step")
            span.set_attribute("agent.name", self.name)
            span.set_attribute("user.input", user_input)

        try:
            # Simulate tool call
            self._transition_state(AgentState.CALLING_TOOL, "tool_invocation", {"tool_name": tool_fn.__name__})
            start_time = time.time()
            result = tool_fn(user_input)
            duration = time.time() - start_time
            
            if self.tracer:
                span.set_attribute("tool.duration_ms", duration * 1000)

            self.conversation_history.append({"role": "assistant", "content": result})
            self._transition_state(AgentState.COMPLETED, "step_success", {"result": result, "duration_s": duration})
            
            if span and OTEL_AVAILABLE:
                span.set_status(Status(StatusCode.OK))
                span.end()

            return result

        except Exception as e:
            self._transition_state(AgentState.ERROR, "step_error", {"error": str(e)})
            self.logger.error(f"Agent execution error: {e}", exc_info=True)
            
            if span and OTEL_AVAILABLE:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                span.end()
            raise e


# Example Usage & Testing
if __name__ == "__main__":
    def sample_search_tool(query: str) -> str:
        return f"Results for: {query}"

    agent = MonitoredAgent(name="ResearchAssistant", enable_otel=False)
    output = agent.run_step("latest advancements in agentic workflows", sample_search_tool)
    print("Agent Output:", output)
    print(f"Total Log Entries Recorded: {len(agent.logs)}")
```

### Testing
- Verified state transitions correctly track `IDLE` -> `THINKING` -> `CALLING_TOOL` -> `COMPLETED`.
- Confirmed JSON output format parses correctly with standard log collectors.
- Tested graceful fallback when OpenTelemetry SDK is not installed.

Signed-off-by: Aditya Waghamare <adityawaghamare7620@gmail.com>


---
*Submitted by Aditya Waghamare*
💰 **Payout Address (Base L2 / EVM):** `0xb61dBcdBc3407F71EaCb64D4CBFAcf9FFfe2415C`