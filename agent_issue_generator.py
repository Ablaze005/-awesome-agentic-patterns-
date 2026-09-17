import os
import json
import requests
import textwrap

# Environment variables
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

# Correct Groq endpoint + correct model
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.1-8b-versatile"


def get_repo_summary():
    """Fetch a simple list of repo files."""
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    resp = requests.get(f"{GITHUB_API}/contents", headers=headers)
    resp.raise_for_status()
    items = resp.json()
    names = [item["name"] for item in items]
    return "Repository files:\n" + "\n".join(names)


def generate_issues(context, count=3):
    """Generate issues using Groq."""
    prompt = textwrap.dedent(f"""
    You are an AI assistant generating GitHub issues for an agentic-patterns repository.

    Context:
    {context}

    Generate {count} issues in JSON format:
    [
      {{
        "title": "...",
        "body": "..."
      }}
    ]
    """)

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Generate high-quality GitHub issues."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.4,
    }

    resp = requests.post(GROQ_URL, headers=headers, json=payload)
    resp.raise_for_status()

    content = resp.json()["choices"][0]["message"]["content"].strip()

    try:
        issues = json.loads(content)
    except json.JSONDecodeError:
        issues = [
            {
                "title": "Fix issue generator JSON parsing",
                "body": "Groq returned invalid JSON. Improve parsing and validation.",
            }
        ]

    return issues[:count]


def create_issue(title, body):
    """Create a GitHub issue."""
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    payload = {"title": title, "body": body}
    resp = requests.post(f"{GITHUB_API}/issues", headers=headers, json=payload)
    resp.raise_for_status()
    return resp.json()["html_url"]


def main():
    print("🔍 Fetching repo context...")
    context = get_repo_summary()

    print("🧠 Generating issues via Groq...")
    issues = generate_issues(context, count=3)

    print("📝 Creating issues...")
    for i, issue in enumerate(issues, start=1):
        url = create_issue(issue["title"], issue["body"])
        print(f"✅ Issue {i} created: {url}")


if __name__ == "__main__":
    main()
