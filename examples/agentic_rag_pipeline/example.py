"""Minimal retrieval-augmented generation pipeline placeholder."""

DOCS = {
    "pricing": "Our Pro plan costs $29 per month.",
    "security": "All data is encrypted in transit and at rest.",
}


def retrieve(question: str) -> str:
    if "price" in question.lower():
        return DOCS["pricing"]
    if "security" in question.lower():
        return DOCS["security"]
    return "No matching document found."


def answer(question: str) -> str:
    context = retrieve(question)
    return f"Answer based on context: {context}"


def main() -> None:
    print(answer("What is the price of the Pro plan?"))


if __name__ == "__main__":
    main()
