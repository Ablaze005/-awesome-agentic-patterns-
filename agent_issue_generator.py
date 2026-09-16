# agent_issue_generator.py
import os
import requests
import textwrap

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
REPO = os.getenv("GITHUB_REPOSITORY")

if not GITHUB_TOKEN:
    raise RuntimeError("GITHUB_TOKEN is required")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is required")
if not REPO:
    raise RuntimeError("GITHUB_REPOSITORY is required")

OWNER, NAME = REPO.split("/")
GITHUB_API = f"https://api.github.com/repos/{OWNER}/{NAME}"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.1-8b-instant"


def get_repo_summary():
    """Fetch a simple summary of repo files to give Groq context."""
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    resp = requests.get(f"{GITHUB_API}/contents", headers=headers)
    resp.raise_for_status()
    items = resp.json()
    names = [item["name"] for item in items]
    return "Repository files:\n" + "\n".join(names)


def generate_issues_from_groq(context, count=3):
    """Ask Groq to propose agentic pattern issues."""
    prompt = textwrap.dedent(f"""
    You are an AI assistant helping maintain an agentic-patterns repository.

    Based on the following repository context:

    {context}

    Generate {count} GitHub issues that propose concrete, actionable improvements or new agentic patterns.
    For each issue, respond in the following strict JSON format:

    [
      {{
        "title": "...",
        "body": "..."
      }},
      ...
    ]

    Do NOT include any extra text outside the JSON.
    """)

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You generate high-quality GitHub issues for an agentic-patterns repo."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.4,
    }

    resp = requests.post(GROQ_API_URL, headers=headers, json=payload)
    resp.raise_for_status()
    content = resp.json()["choices"][0]["message"]["content"].strip()

    # Parse JSON safely
    import json
    try:
        issues = json.loads(content)
    except json.JSONDecodeError:
        # Fallback: create a single generic issue if parsing fails
        issues = [
            {
                "title": "Improve agentic debugging pattern",
                "body": "Groq response could not be parsed as JSON. Add better validation and logging to the issue generator.",
            }
        ]

    # Limit to requested count
    return issues[:count]


def create_issue(title, body):
    """Create a GitHub issue in the current repo."""
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    payload = {
        "title": title,
        "body": body,
    }
    resp = requests.post(f"{GITHUB_API}/issues", headers=headers, json=payload)
    resp.raise_for_status()
    return resp.json()["html_url"]


def main():
    print("🔍 Gathering repository context...")
    context = get_repo_summary()

    print("🧠 Asking Groq to generate issues...")
    issues = generate_issues_from_groq(context, count=3)

    print(f"📝 Creating {len(issues)} issues...")
    for i, issue in enumerate(issues, start=1):
        title = issue.get("title", f"Agentic pattern proposal #{i}")
        body = issue.get("body", "No body provided by Groq.")
        url = create_issue(title, body)
        print(f"✅ Issue {i} created: {url}")


if __name__ == "__main__":
    main()
