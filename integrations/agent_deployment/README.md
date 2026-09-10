# Agent Deployment Pattern (Docker + Render)

This minimal FastAPI service provides a production-friendly boundary around an
agent function. Replace `run_agent` in `server.py` with a call to your model or
agent framework; credentials stay in environment variables.

## Files

- `server.py` - FastAPI app with `/run-agent` and `/health`.
- `Dockerfile` - Small Python image running as a non-root user.
- `render.yaml` - Render Blueprint for Docker deployment.
- `.env.example` - Local environment variable template.

## Run locally

Create a virtual environment, install dependencies, and configure variables:

```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell:
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn server:app --reload --port 8000
```

Test the service:

```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/run-agent \
  -H "Content-Type: application/json" \
  -d "{\"prompt\":\"Summarize this deployment pattern\"}"
```

## Build and run with Docker

Run these commands from this directory:

```bash
docker build -t agent-deployment-pattern .
docker run --rm -p 8000:8000 --env-file .env agent-deployment-pattern
```

The container binds to `0.0.0.0` and uses `PORT` (default `8000`). Render sets
`PORT` automatically, so the same image works locally and in the cloud.

## Deploy to Render

1. Push this repository to GitHub and create a new **Blueprint** in Render.
2. Select the repository and approve the `render.yaml` configuration.
3. In the Render dashboard, set `AGENT_API_KEY` to the provider secret.
4. Adjust `AGENT_MODEL` and `AGENT_CONFIG` as needed.
5. Deploy. Render builds the `Dockerfile`, injects `PORT`, and checks
   `/health` before routing traffic.

Render secrets are managed in the dashboard and are not stored in
`render.yaml`. For a manual setup, choose **New > Web Service**, select
**Docker**, use this repository's `Dockerfile`, and set the same environment
variables. Do not hard-code API keys in the image or source code.
