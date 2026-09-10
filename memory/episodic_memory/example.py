"""A simple episodic memory example."""

from datetime import datetime

EVENTS = []


def record_event(event: str) -> None:
    """Save a timestamped experience in memory."""
    EVENTS.append({
        "time": datetime.now().isoformat(timespec="seconds"),
        "event": event,
    })


def recent_events(limit: int = 3) -> list[dict]:
    """Return the newest remembered events."""
    return EVENTS[-limit:]


def main() -> None:
    record_event("User asked for help with a Python script.")
    record_event("Assistant suggested a simple refactor.")
    record_event("User asked for a second example.")

    print("Recent episodic memories:")
    for entry in recent_events():
        print(f"{entry['time']} - {entry['event']}")


if __name__ == "__main__":
    main()
