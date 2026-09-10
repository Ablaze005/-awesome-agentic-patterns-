"""Simple swarm-style orchestration example."""

from dataclasses import dataclass, field


@dataclass
class Agent:
    name: str
    queue: list[str] = field(default_factory=list)

    def assign(self, task: str) -> None:
        self.queue.append(task)

    def process(self) -> str:
        if not self.queue:
            return f"{self.name}: no tasks waiting"
        task = self.queue.pop(0)
        return f"{self.name} completed: {task}"


def main() -> None:
    coordinator = Agent("Coordinator")
    planner = Agent("Planner")
    executor = Agent("Executor")

    for task in ["design roadmap", "create summary", "finalize deliverable"]:
        coordinator.assign(task)

    planner.assign("design roadmap")
    executor.assign("finalize deliverable")

    print(coordinator.process())
    print(planner.process())
    print(executor.process())


if __name__ == "__main__":
    main()
