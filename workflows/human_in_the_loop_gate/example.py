"""Human-in-the-loop approval gate for high-risk agent tools."""

from typing import Callable

HIGH_RISK_TOOLS = {"delete_file", "send_email", "execute_code"}
APPROVED: set[str] = set()


def execute_tool(name: str, payload: dict, executor: Callable[[dict], str]) -> str:
    """Run a tool, blocking high-risk calls until they are approved."""
    if name in HIGH_RISK_TOOLS and name not in APPROVED:
        return f"BLOCKED: {name} requires human approval before execution"
    return executor(payload)


def approve_tool(name: str) -> None:
    """Record human approval for a high-risk tool."""
    APPROVED.add(name)


def search_docs(payload: dict) -> str:
    return f"Search results for: {payload['query']}"


def delete_file(payload: dict) -> str:
    return f"Deleted file: {payload['path']}"


def main() -> None:
    print(execute_tool("search_docs", {"query": "onboarding"}, search_docs))
    print(execute_tool("delete_file", {"path": "/tmp/report.txt"}, delete_file))

    approve_tool("delete_file")
    print(execute_tool("delete_file", {"path": "/tmp/report.txt"}, delete_file))


if __name__ == "__main__":
    main()
