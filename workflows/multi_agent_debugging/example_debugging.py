# workflows/multi_agent_debugging/example_debugging.py
from debug_wrapper import DebugAgentWrapper

class SimpleAgent:
    def __init__(self):
        self.memory = {}

    def send(self, message):
        return f"Processed: {message}"

    def call_tool(self, tool_name, payload):
        return f"Tool {tool_name} executed with {payload}"

agent_a = DebugAgentWrapper(SimpleAgent(), name="Agent-A")
agent_b = DebugAgentWrapper(SimpleAgent(), name="Agent-B")

# Example interactions
agent_a.send("Hello Agent B")
agent_b.send("Hello Agent A")

agent_a.call_tool("search", {"query": "agentic patterns"})
agent_b.update_memory("last_message", "debugging example")
