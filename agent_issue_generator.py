"""Generate actionable repository issues with a Groq-powered agent."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import requests

REPO_OWNER = os.getenv("GITHUB_REPOSITORY", "Ablaze005/-awesome-agentic-patterns-").split(
    "/", 1
)[0]
REPO_NAME = os.getenv("GITHUB_REPOSITORY", "Ablaze005/-awesome-agentic-patterns-").split(
    "/", 1
)[-1]
GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} is required")
    return value


def github_headers() -> dict[str, str]:
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {required_env('GH_TOKEN')}",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def list_files() -> list[str]:
    root = Path(__file__).resolve().parent
    return sorted(
        str(path.relative_to(root))
        for path in root.rglob("*")
        if path.is_file() and ".git" not in path.parts
    )


def list_issues() -> list[str]:
    response = requests.get(
        f"{GITHUB_API_URL}/issues",
        headers=github_headers(),
        params={"state": "all", "per_page": 100},
        timeout=30,
    )
    response.raise_for_status()
    return [
        issue["title"]
        for issue in response.json()
        if "pull_request" not in issue
    ]


def generate_issue(repo_files: list[str], existing_issues: list[str]) -> str:
    prompt = f"""You are an agentic-patterns expert.

Repository files:
{chr(10).join(repo_files)}

Existing issue titles:
{chr(10).join(existing_issues) or "(none)"}

Propose one actionable issue for a missing or improvable agentic pattern.
Do not duplicate an existing issue. Return exactly this format:
Title: <concise issue title>
Description: <what should be added or changed>
Why it matters: <the benefit>
Steps to implement:
1. <step>
2. <step>
"""
    response = requests.post(
        GROQ_API_URL,
        headers={
            "Authorization": f"Bearer {required_env('GROQ_API_KEY')}",
            "Content-Type": "application/json",
        },
        json={
            "model": GROQ_MODEL,
            "temperature": 0.2,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=60,
    )
    response.raise_for_status()
    content: str = response.json()["choices"][0]["message"]["content"].strip()
    if not content.startswith("Title:"):
        raise ValueError("The model response did not start with 'Title:'")
    return content


def create_issue(content: str) -> dict[str, Any]:
    lines = content.splitlines()
    title = lines[0].removeprefix("Title:").strip()
    body = "\n".join(lines[1:]).strip()
    if not title or not body:
        raise ValueError("Generated issue must contain a title and body")

    response = requests.post(
        f"{GITHUB_API_URL}/issues",
        headers=github_headers(),
        json={"title": title, "body": body},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def main() -> None:
    repo_files = list_files()
    existing_issues = list_issues()

    for _ in range(3):
        issue_content = generate_issue(repo_files, existing_issues)
        title = issue_content.splitlines()[0].removeprefix("Title:").strip()
        if title in existing_issues:
            print(f"Skipped duplicate issue: {title}")
            continue
        result = create_issue(issue_content)
        existing_issues.append(title)
        print(f"Created issue: {result.get('html_url', title)}")


if __name__ == "__main__":
    main()
