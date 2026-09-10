"""Minimal FastAPI app for an agent endpoint."""

from fastapi import FastAPI

app = FastAPI(title="Agent API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat")
def chat(message: str) -> dict[str, str]:
    response = f"Agent reply: {message}"
    return {"response": response}
