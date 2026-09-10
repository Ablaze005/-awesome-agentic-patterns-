"""A minimal long-term memory example for an agent."""

MEMORY = {
    "preferred_language": "Spanish",
    "favorite_tool": "calculator",
    "user_name": "Ava",
}


def build_prompt(user_message: str) -> str:
    context = (
        f"User name: {MEMORY['user_name']}\n"
        f"Preferred language: {MEMORY['preferred_language']}\n"
        f"Favorite tool: {MEMORY['favorite_tool']}\n"
        f"Latest user message: {user_message}"
    )
    return context


def main() -> None:
    prompt = build_prompt("Please answer in Spanish.")
    print(prompt)


if __name__ == "__main__":
    main()
