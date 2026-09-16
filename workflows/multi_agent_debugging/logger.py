# workflows/multi_agent_debugging/logger.py
import datetime
import json

class DebugLogger:
    def __init__(self, logfile="agent_debug.log"):
        self.logfile = logfile

    def _write(self, entry):
        timestamp = datetime.datetime.utcnow().isoformat()
        with open(self.logfile, "a") as f:
            f.write(f"[{timestamp}] {json.dumps(entry)}\n")

    def log_agent_message(self, agent_name, message):
        self._write({
            "type": "agent_message",
            "agent": agent_name,
            "message": message
        })

    def log_tool_call(self, agent_name, tool_name, payload):
        self._write({
            "type": "tool_call",
            "agent": agent_name,
            "tool": tool_name,
            "payload": payload
        })

    def log_memory_update(self, agent_name, key, value):
        self._write({
            "type": "memory_update",
            "agent": agent_name,
            "key": key,
            "value": value
        })
