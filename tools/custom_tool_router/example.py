"""Tool routing with a simple intent-based dispatcher."""


def search_docs(query: str) -> str:
    return f"Search results for: {query}"


def calculate_total(items: list[int]) -> str:
    total = sum(items)
    return f"Total: {total}"


def fallback(message: str) -> str:
    return f"No matching tool for: {message}"


ROUTES = {
    "search": search_docs,
    "calculate": calculate_total,
}


def route_request(user_message: str) -> str:
    message = user_message.lower()

    if "search" in message:
        return search_docs(user_message)
    if "total" in message or "sum" in message:
        return calculate_total([10, 15, 20])
    return fallback(user_message)


def main() -> None:
    print(route_request("Please search for onboarding docs"))
    print(route_request("What is the total of 10, 15, and 20?"))
    print(route_request("Tell me a joke"))


if __name__ == "__main__":
    main()
