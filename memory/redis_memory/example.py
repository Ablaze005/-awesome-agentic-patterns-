"""Minimal Redis-backed memory for a simple agent."""

import json
import os

import redis


# Use environment variables when available so the example is easy to configure.
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))


def get_client() -> redis.Redis:
    """Create and validate a Redis connection."""
    client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    try:
        client.ping()
    except redis.RedisError as exc:
        raise RuntimeError(
            "Redis is not running. Start it with: docker run --name redis-memory-demo -p 6379:6379 -d redis:7"
        ) from exc

    print("Connected to Redis successfully.")
    return client


def save_profile(client: redis.Redis, user_id: str, profile: dict) -> None:
    """Store a structured memory block for a user."""
    key = f"agent:profile:{user_id}"
    client.hset(key, mapping=profile)


def get_profile(client: redis.Redis, user_id: str) -> dict:
    """Read a stored user profile from Redis."""
    key = f"agent:profile:{user_id}"
    raw_profile = client.hgetall(key)
    return dict(raw_profile)


def add_interaction(client: redis.Redis, user_id: str, message: str) -> None:
    """Append a recent message to the conversation memory list."""
    key = f"agent:conversation:{user_id}"
    client.rpush(key, message)
    client.ltrim(key, -10, -1)  # keep only the newest 10 messages


def get_recent_interactions(client: redis.Redis, user_id: str) -> list[str]:
    """Return the most recent messages for this conversation."""
    key = f"agent:conversation:{user_id}"
    return client.lrange(key, 0, -1)


def build_memory_summary(user_profile: dict, recent_messages: list[str]) -> str:
    """Turn raw memory into a compact summary for the agent."""
    summary = [
        f"Name: {user_profile.get('name', 'Unknown')}",
        f"Preferred language: {user_profile.get('preferred_language', 'Not set')}",
        f"Timezone: {user_profile.get('timezone', 'Not set')}",
        f"Recent interactions: {len(recent_messages)}",
    ]
    return "\n".join(summary)


def main() -> None:
    """Save memory, read it back, and print a simple context summary."""
    client = get_client()

    # In a real app, the user ID would come from the authenticated session.
    user_id = "user-123"

    # Store a simple user profile as structured memory.
    profile = {
        "name": "Ava",
        "preferred_language": "Spanish",
        "timezone": "UTC+1",
    }
    save_profile(client, user_id, profile)

    # Store recent messages as a compact rolling history.
    messages = [
        "User: I am learning Spanish.",
        "Assistant: That is a great goal. Keep practicing.",
        "User: Please answer in Spanish.",
    ]
    for message in messages:
        add_interaction(client, user_id, message)

    # Read the stored memory back.
    saved_profile = get_profile(client, user_id)
    recent_messages = get_recent_interactions(client, user_id)

    print(f"User profile: {saved_profile}")
    print("Recent messages:")
    for message in recent_messages:
        print(f"- {message}")

    print("Memory summary:")
    print(build_memory_summary(saved_profile, recent_messages))

    # A real agent would inject this summary into its prompt before sending to the model.


if __name__ == "__main__":
    main()
