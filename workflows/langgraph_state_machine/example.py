"""
A simple LangGraph state machine workflow:
States:
    - input_state: receives user input
    - process_state: validates/transforms the input
    - output_state: returns final result

This example teaches:
    - how to define states
    - how to define transitions
    - how to build a graph
    - how to execute the workflow
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict


# ---------------------------------------------------------
# 1. Define the shared state object
# ---------------------------------------------------------
class WorkflowState(TypedDict):
    user_input: str
    processed_text: str
    error: str


# ---------------------------------------------------------
# 2. Define each state function
# ---------------------------------------------------------

def input_state(state: WorkflowState):
    """
    First state: receives user input.
    In a real agent, this could parse intent or classify the request.
    """
    print("📥 INPUT STATE")
    if not state.get("user_input"):
        state["error"] = "No input provided."
        return state

    print(f"Received input: {state['user_input']}")
    return state


def process_state(state: WorkflowState):
    """
    Second state: validates and transforms the input.
    Here we simply uppercase the text, but this could be:
        - calling tools
        - running LLM reasoning
        - performing calculations
    """
    print("⚙️ PROCESS STATE")

    if state.get("error"):
        return state

    text = state["user_input"]

    # Example transformation
    state["processed_text"] = text.upper()

    print(f"Processed text: {state['processed_text']}")
    return state


def output_state(state: WorkflowState):
    """
    Final state: returns the result.
    This is where the agent produces its final answer.
    """
    print("📤 OUTPUT STATE")

    if state.get("error"):
        print("Error encountered:", state["error"])
        return {"result": None, "error": state["error"]}

    return {"result": state["processed_text"], "error": None}


# ---------------------------------------------------------
# 3. Build the LangGraph state machine
# ---------------------------------------------------------

def build_graph():
    graph = StateGraph(WorkflowState)

    # Register states
    graph.add_node("input_state", input_state)
    graph.add_node("process_state", process_state)
    graph.add_node("output_state", output_state)

    # Define transitions
    graph.set_entry_point("input_state")
    graph.add_edge("input_state", "process_state")
    graph.add_edge("process_state", "output_state")

    # Output state ends the workflow
    graph.add_edge("output_state", END)

    return graph.compile()


# ---------------------------------------------------------
# 4. Run the workflow
# ---------------------------------------------------------

if __name__ == "__main__":
    workflow = build_graph()

    initial_state = {
        "user_input": "hello langgraph",
        "processed_text": "",
        "error": ""
    }

    print("\n🚀 Running State Machine...\n")
    result = workflow.invoke(initial_state)

    print("\n🎉 FINAL RESULT")
    print(result)
