"""Simple multi-agent chat simulation."""

agents = {
    "researcher": "Finds the key facts.",
    "writer": "Drafts a response.",
    "reviewer": "Checks for clarity and consistency.",
}


def main() -> None:
    for name, role in agents.items():
        print(f"{name}: {role}")


if __name__ == "__main__":
    main()
