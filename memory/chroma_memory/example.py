"""Simple semantic memory with Chroma."""

try:
    import chromadb
except ImportError as exc:
    raise SystemExit(
        "Install the dependency with: pip install chromadb"
    ) from exc


# This example keeps the code tiny and easy to understand.
# It stores a few example memories and then retrieves the closest match.

def main() -> None:
    client = chromadb.Client()
    collection = client.create_collection(name="agent_memories")

    documents = [
        "The user likes to work in the morning and responds well to short tasks.",
        "The user prefers concise answers and examples with code.",
        "The user is learning Spanish and wants explanations in simple language.",
    ]

    collection.add(
        ids=["m1", "m2", "m3"],
        documents=documents,
    )

    results = collection.query(
        query_texts=["What kind of answers does the user prefer?"],
        n_results=2,
    )

    print("Relevant memories:")
    for item in results["documents"][0]:
        print(f"- {item}")


if __name__ == "__main__":
    main()
