"""Minimal LangGraph-style state machine example."""


class StateMachine:
    def __init__(self):
        self.state = "idle"

    def transition(self, event: str) -> str:
        if self.state == "idle":
            self.state = "received"
            return "Request received."
        if self.state == "received":
            self.state = "analyzed"
            return "Request analyzed."
        if self.state == "analyzed":
            self.state = "done"
            return "Response prepared."
        return "Workflow complete."


def main() -> None:
    machine = StateMachine()
    for step in ["start", "analyze", "finish"]:
        print(machine.transition(step))


if __name__ == "__main__":
    main()
