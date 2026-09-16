# workflows/multi_agent_debugging/debug_wrapper.py
from logger import DebugLogger

class DebugAgentWrapper:
    def __init__(self, agent, name="Agent"):
        self.agent = agent
        self.name = name
        self.logger = DebugLogger()

    def send(self, message):
        self.logger.log_agent_message(self.name, message)
        response = self.agent.send(message)
        self.logger.log_agent_message(self.name, response)
        return response

    def call_tool(self, tool_name, payload):
        self.logger.log_tool_call(self.name, tool_name, payload)
        return self.agent.call_tool(tool_name, payload)

    def update_memory(self, key, value):
        self.logger.log_memory_update(self.name, key, value)
        self.agent.memory[key] = value
