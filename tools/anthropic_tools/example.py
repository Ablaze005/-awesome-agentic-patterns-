"""Minimal Anthropic-style tool orchestration example."""


def lookup_stock(symbol: str) -> str:
    return f"{symbol}: 142.50 USD"


def summarize_report(text: str) -> str:
    return f"Summary: {text[:40]}..."


TOOLS = {
    "lookup_stock": lookup_stock,
    "summarize_report": summarize_report,
}


def run_tool(tool_name: str, value: str) -> str:
    return TOOLS[tool_name](value)


def main() -> None:
    print(run_tool("lookup_stock", "NVDA"))
    print(run_tool("summarize_report", "This quarter the product team shipped faster releases and fewer bugs."))


if __name__ == "__main__":
    main()
