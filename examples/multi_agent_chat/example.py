"""Simple multi-agent chat simulation using LangGraph and ChatGroq."""

import os
from typing import TypedDict
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field


load_dotenv()


class ResearchOutput(BaseModel):
    title: str = Field(description="Research topic title")
    summary: str = Field(description="Summary of the key research points")



class AgentState(TypedDict):
    user_input: str
    plan: str
    research: str
    review: str



llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.7,
    api_key=os.getenv("GROQ_API_KEY"),
)


researcher_llm = llm.with_structured_output(ResearchOutput)


def planner_node(state: AgentState) -> dict:
    prompt = f"Create a step-by-step plan to answer the user request:\n\n{state['user_input']}"
    response = llm.invoke(prompt)
    return {"plan": response.content}


def researcher_node(state: AgentState) -> dict:
    #TODO : Insted of self answer we can add a web_search_tool in the researcher
    #from langchain_community.tools import tool
    #create a tool node and add to this function for better output 
    
    prompt = (
        f"Topic: {state['user_input']}\n"
        f"Plan: {state['plan']}\n"
        "Conduct thorough research and provide a title and summary."
    )
    result: ResearchOutput = researcher_llm.invoke(prompt)
    formatted = f"Title: {result.title}\nSummary: {result.summary}"
    return {"research": formatted}


def reviewer_node(state: AgentState) -> dict:
    prompt = (
        f"Original User Request: {state['user_input']}\n"
        f"Research:\n{state['research']}\n\n"
        "Review the research for accuracy, clarity, and completeness. Provide final feedback."
    )
    response = llm.invoke(prompt)
    return {"review": response.content}



workflow = StateGraph(AgentState)


workflow.add_node("planner", planner_node)
workflow.add_node("researcher", researcher_node)
workflow.add_node("reviewer", reviewer_node)


workflow.add_edge(START, "planner")
workflow.add_edge("planner", "researcher")
workflow.add_edge("researcher", "reviewer")
workflow.add_edge("reviewer", END)


agent_app = workflow.compile()


if __name__ == "__main__":
    initial_input = "Explain how multi-agent architectures work in LangGraph."
    print(f"User Request: {initial_input}\n")

    result = agent_app.invoke({"user_input": initial_input})

  
    print(result["plan"])
    print(result["research"])
    print(result["review"])
