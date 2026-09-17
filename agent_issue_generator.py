import json
import os
from typing import Any
import requests

# API endpoints
GITHUB_API = "https://api.github.com"
GROQ_API = "https://api.groq.com/openai/v1/chat/completions"

# Groq model
MODEL = "llama-3.1-8b-versatile"

# Settings
ISSUE_COUNT = 3
TIMEOUT = (10, 60)


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} is required")
    return value


def repository_parts() -> tuple[str, str]:
    repository = required_env("GITHUB_REPOSITORY")
    owner, separator, name = repository.partition("/")
    if not separator or not owner or not name:
        raise RuntimeError("GITHUB_REPOSITORY must be in OWNER/REPOSITORY format")
    return owner, name


def github_headers() -> dict[str, str]:
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {required_env('GITHUB_TOKEN')}",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def github_request(method: str, path: str, **kwargs: Any) -> requests.Response:
    response = requests.request(
        method,
        f"{GITHUB_API}{path}",
        headers=github_headers(),
        timeout=TIMEOUT,
        **kwargs,
    )
    response.raise_for_status()
    return response


def get_repo_context() -> str:
    owner, name = repository_parts()

    repository = github_request("GET", f"/repos/{owner}/{name}").json()

    tree = github_request(
        "GET",
        f"/repos/{owner}/{name}/git/trees/{repository['default_branch']}",
        params={"recursive": "1"},
    ).json()

    issues = github_request(
        "GET",
        f"/repos/{owner}/{name}/issues",
        params={"state": "all", "per_page": 100},
    ).json()

    files = [
        item["path"]
        for item in tree.get("tree", [])
        if item.get("type") == "blob"
    ]

    issue_titles = [
        item["title"]
        for item in issues
        if "pull_request" not in item
    ]

    return json.dumps(
        {
            "repository": repository.get("full_name"),
            "description": repository.get("description"),
            "default_branch": repository.get("default_branch"),
            "files": files,
            "existing_issue_titles": issue_titles,
        },
        ensure_ascii=True,
    )


def generate_issues(context: str) -> list[dict[str, str]]:
    system_prompt = (
        "You generate actionable GitHub issues for an agentic-patterns repository. "
        "Return only valid JSON. The top-level value must be an object with an "
        "'issues' array containing exactly three objects. Each object must contain "
        "only string fields named 'title' and 'body'."
    )

    user_prompt = (
        "Analyze this repository context and propose exactly three non-duplicate "
        "issues. Each body must explain the improvement, why it matters, acceptance "
        "criteria, and optional implementation hints.\n\n"
        f"Repository context:\n{context}"
    )

    response = requests.post(
        GROQ_API,
        headers={
            "Authorization": f"Bearer {required_env('GROQ_API_KEY')}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2
        },
        timeout=TIMEOUT,
    )

    response.raise_for_status()

    try:
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        parsed = json.loads(content)
    except Exception as error:
        raise RuntimeError("Groq returned an invalid JSON completion") from error

    issues = parsed.get("issues") if isinstance(parsed, dict) else None

    if not isinstance(issues, list) or len(issues) != ISSUE_COUNT:
        raise RuntimeError("Groq must return exactly three issues")

    validated: list[dict[str, str]] = []

    for issue in issues:
        if (
            not isinstance(issue, dict)
            or set(issue) != {"title", "body"}
            or not isinstance(issue["title"], str)
            or not isinstance(issue["body"], str)
            or not issue["title"].strip()
            or not issue["body"].strip()
        ):
            raise RuntimeError("Groq returned an issue with an invalid schema")

        validated.append(
            {
                "title": issue["title"].strip(),
                "body": issue["body"].strip(),
            }
        )

    return validated


def create_issue(issue: dict[str, str]) -> str:
    owner, name = repository_parts()

    response = github_request(
        "POST",
        f"/repos/{owner}/{name}/issues",
        json={
            "title": issue["title"],
            "body": issue["body"],
        },
    )

    return response.json()["html_url"]


def main() -> None:
    print("Fetching repository context...")
    context = get_repo_context()

    print("Generating exactly three issues with Groq...")
    issues = generate_issues(context)

    print("Creating GitHub issues...")
    for number, issue in enumerate(issues, start=1):
        url = create_issue(issue)
        print(f"Created issue {number}/{ISSUE_COUNT}: {url}")


if __name__ == "__main__":
    main()
