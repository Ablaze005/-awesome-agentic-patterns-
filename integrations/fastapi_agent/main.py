"""Minimal FastAPI app for an agent endpoint."""

from fastapi import FastAPI ,status
from pydantic import BaseModel ,Field
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

example = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.7,
    api_key=os.getenv("GROQ_API_KEY"),
)


app = FastAPI(title="Agent API",version="0.0.1")


#output schema for the agent
class AgentResponse(BaseModel):
    response: str = Field(description="Response from the agent")


#To check the server condition
@app.get("/app/v1/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

#chat and structured_response from the agent
@app.post("/app/v1/chat",response_model=AgentResponse,status_code=status.HTTP_200_OK)
def chat(message: str) -> AgentResponse:
    result = example.invoke(message)
    return AgentResponse(response=result.content)



