"""Basic multi-agent collaboration sketch."""

from dataclasses import dataclass


@dataclass
class Agent:
    name: str
    role: str

    def respond(self, task: str) -> str:
        return f"{self.name} ({self.role}) says: {task}"


def main() -> None:
    planner = Agent("Planner", "plans the task")
    researcher = Agent("Researcher", "gathers facts")
    writer = Agent("Writer", "writes the answer")

    task = "Create a brief market summary for a new AI product."
    steps = [
        planner.respond(task),
        researcher.respond(task),
        writer.respond(task),
    ]

    for step in steps:
        print(step)


if __name__ == "__main__":
    main()
