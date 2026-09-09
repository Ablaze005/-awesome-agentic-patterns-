"""Store and recall agent memories with Supabase pgvector."""

import os
from typing import Any

from openai import OpenAI
from supabase import Client, create_client


# Configuration: set these values in the environment before running the script.
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

EMBEDDING_MODEL = "text-embedding-3-small"
SIMILARITY_THRESHOLD = 0.25
DEFAULT_MATCH_COUNT = 5


def require_setting(name: str, value: str | None) -> str:
    """Return a required setting or raise a useful configuration error."""
    if not value:
        raise RuntimeError(
            f"Missing {name}. Set it in the environment before running this example."
        )
    return value


def embed(openai_client: OpenAI, text: str) -> list[float]:
    """Create an embedding for a piece of text."""
    response = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
    )
    return response.data[0].embedding


def remember(
    supabase: Client,
    openai_client: OpenAI,
    content: str,
    metadata: dict[str, Any] | None = None,
) -> None:
    """Persist one text memory and its embedding."""
    row = {
        "content": content,
        "embedding": embed(openai_client, content),
        "metadata": metadata or {},
    }
    supabase.table("agent_memories").insert(row).execute()


def recall(
    supabase: Client,
    openai_client: OpenAI,
    query: str,
    *,
    match_count: int = DEFAULT_MATCH_COUNT,
    threshold: float = SIMILARITY_THRESHOLD,
) -> list[dict[str, Any]]:
    """Return memories whose cosine similarity meets the threshold."""
    response = supabase.rpc(
        "match_agent_memories",
        {
            "query_embedding": embed(openai_client, query),
            "match_threshold": threshold,
            "match_count": match_count,
        },
    ).execute()
    return response.data


def main() -> None:
    """Save sample memories and retrieve context for a new agent query."""
    supabase = create_client(
        require_setting("SUPABASE_URL", SUPABASE_URL),
        require_setting("SUPABASE_KEY", SUPABASE_KEY),
    )
    openai_client = OpenAI(api_key=require_setting("OPENAI_API_KEY", OPENAI_API_KEY))

    sample_memories = [
        (
            "The user prefers oat milk in their coffee.",
            {"category": "preference"},
        ),
        (
            "The user is learning Spanish and practices every morning.",
            {"category": "goal"},
        ),
    ]

    for content, metadata in sample_memories:
        remember(supabase, openai_client, content, metadata)

    query = "What does the user prefer to drink?"
    matches = recall(supabase, openai_client, query)

    print("Saved 2 memories.")
    print(f"\nMemories related to: {query}")
    for match in matches:
        print(
            f"- {match['content']} "
            f"(similarity: {float(match['similarity']):.2f})"
        )


if __name__ == "__main__":
    main()
