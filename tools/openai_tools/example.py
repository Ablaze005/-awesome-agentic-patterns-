"""OpenAI-style tool pattern using a local function registry."""

from typing import Callable


def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny and 24C."


def get_time(zone: str) -> str:
    return f"The current time in {zone} is 09:00."


TOOLS: dict[str, Callable[..., str]] = {
    "get_weather": get_weather,
    "get_time": get_time,
}


def call_tool(name: str, *args: str) -> str:
    tool = TOOLS[name]
    return tool(*args)


def main() -> None:
    print(call_tool("get_weather", "Paris"))
    print(call_tool("get_time", "UTC"))


if __name__ == "__main__":
    main()
