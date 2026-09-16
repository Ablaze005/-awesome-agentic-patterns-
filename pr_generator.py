"""Generate an agentic-pattern file and open a pull request for it."""

from __future__ import annotations

import base64
import os
from datetime import datetime, timezone
from typing import Any

import requests

GITHUB_API_ROOT = "https://api.github.com"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} is required")
    return value


def repository() -> tuple[str, str]:
    value = required_env("GITHUB_REPOSITORY")
    parts = value.split("/", 1)
    if len(parts) != 2 or not all(parts):
        raise RuntimeError("GITHUB_REPOSITORY must have the form OWNER/REPOSITORY")
    return parts[0], parts[1]


def github_headers() -> dict[str, str]:
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {required_env('GH_TOKEN')}",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def github_request(method: str, path: str, **kwargs: Any) -> requests.Response:
    response = requests.request(
        method,
        f"{GITHUB_API_ROOT}{path}",
        headers=github_headers(),
        timeout=30,
        **kwargs,
    )
    response.raise_for_status()
    return response


def groq_generate(content: str) -> str:
    """Generate new pattern file content using Groq."""
    response = requests.post(
        GROQ_API_URL,
        headers={
            "Authorization": f"Bearer {required_env('GROQ_API_KEY')}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "temperature": 0.2,
            "messages": [
                {
                    "role": "system",
                    "content": "You generate complete Markdown agentic pattern files.",
                },
                {
                    "role": "user",
                    "content": (
                        "Generate a new, self-contained agentic pattern Markdown file. "
                        "Include a title, problem, design, implementation guidance, and examples. "
                        f"Existing repository files:\n{content}"
                    ),
                },
            ],
        },
        timeout=60,
    )
    response.raise_for_status()
    generated = response.json()["choices"][0]["message"]["content"].strip()
    if not generated:
        raise ValueError("Groq returned empty pattern content")
    return generated


def get_default_branch() -> str:
    owner, name = repository()
    response = github_request("GET", f"/repos/{owner}/{name}")
    return response.json()["default_branch"]


def get_repo_files() -> list[str]:
    owner, name = repository()
    response = github_request(
        "GET",
        f"/repos/{owner}/{name}/git/trees/{get_default_branch()}",
        params={"recursive": "1"},
    )
    return [
        item["path"]
        for item in response.json().get("tree", [])
        if item.get("type") == "blob"
    ]


def create_branch(branch_name: str, base_branch: str) -> None:
    owner, name = repository()
    ref = github_request("GET", f"/repos/{owner}/{name}/git/ref/heads/{base_branch}").json()
    github_request(
        "POST",
        f"/repos/{owner}/{name}/git/refs",
        json={"ref": f"refs/heads/{branch_name}", "sha": ref["object"]["sha"]},
    )


def commit_file(branch: str, filename: str, content: str) -> None:
    owner, name = repository()
    encoded = base64.b64encode(content.encode("utf-8")).decode("ascii")
    github_request(
        "PUT",
        f"/repos/{owner}/{name}/contents/{filename}",
        json={
            "message": f"Add new agentic pattern: {filename}",
            "content": encoded,
            "branch": branch,
        },
    )


def create_pr(branch: str, filename: str, base_branch: str) -> str:
    owner, name = repository()
    response = github_request(
        "POST",
        f"/repos/{owner}/{name}/pulls",
        json={
            "title": f"Add new agentic pattern: {filename}",
            "body": f"Automatically generated new agentic pattern file `{filename}`.",
            "head": branch,
            "base": base_branch,
        },
    )
    return response.json()["html_url"]


def main() -> None:
    print("Scanning repository...")
    base_branch = get_default_branch()
    files = get_repo_files()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"patterns/pattern_{timestamp}.md"
    branch = f"auto-pattern-{timestamp}"

    print("Generating new pattern content...")
    content = groq_generate("\n".join(files))
    print(f"Creating branch: {branch}")
    create_branch(branch, base_branch)
    print(f"Committing file: {filename}")
    commit_file(branch, filename, content)
    print("Opening pull request...")
    print("Pull request created:", create_pr(branch, filename, base_branch))


if __name__ == "__main__":
    main()
