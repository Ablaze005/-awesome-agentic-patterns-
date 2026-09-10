"""Small FastAPI service that exposes an agent execution boundary."""

import os

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel, Field

load_dotenv()

app = FastAPI(title="Agent Deployment Pattern", version="1.0.0")


class AgentRequest(BaseModel):
    """Input accepted by the agent endpoint."""

    prompt: str = Field(min_length=1, max_length=10_000)


class AgentResponse(BaseModel):
    """Stable response shape for clients."""

    response: str
    model: str
    configuration: str


def run_agent(prompt: str) -> str:
    """Execute the agent logic.

    Replace this function with a call to an agent framework or model provider.
    Secrets are read from the environment rather than returned to clients.
    """

    api_key = os.getenv("AGENT_API_KEY")
    if not api_key:
        raise RuntimeError("AGENT_API_KEY is not configured")

    model = os.getenv("AGENT_MODEL", "demo-model")
    configuration = os.getenv("AGENT_CONFIG", "default")
    return (
        f"[{model} / {configuration}] Agent received: {prompt}"
    )


@app.get("/health")
def health() -> dict[str, str]:
    """Health check used by local and cloud deployments."""

    return {"status": "ok"}


@app.post("/run-agent", response_model=AgentResponse)
def run_agent_endpoint(request: AgentRequest) -> AgentResponse:
    """Run the configured agent for one prompt."""

    response = run_agent(request.prompt)
    return AgentResponse(
        response=response,
        model=os.getenv("AGENT_MODEL", "demo-model"),
        configuration=os.getenv("AGENT_CONFIG", "default"),
    )
