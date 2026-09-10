"""Minimal vector search example with Qdrant-like semantics."""

DOCUMENTS = [
    "The onboarding guide explains how to create a project.",
    "The product team uses weekly release reviews.",
    "Customer support handles refunds through the billing portal.",
]


def search(query: str, limit: int = 2) -> list[str]:
    query_lower = query.lower()
    matches = []

    for document in DOCUMENTS:
        if query_lower in document.lower():
            matches.append(document)

    return matches[:limit]


def main() -> None:
    results = search("onboarding")
    print("Relevant documents:")
    for result in results:
        print(f"- {result}")


if __name__ == "__main__":
    main()
