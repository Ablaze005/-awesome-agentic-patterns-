"""Simple Supabase-style backend model using in-memory data."""


class SupabaseClient:
    def __init__(self):
        self.rows = []

    def insert(self, table: str, row: dict) -> None:
        self.rows.append({"table": table, **row})

    def fetch_all(self, table: str) -> list[dict]:
        return [row for row in self.rows if row["table"] == table]


def main() -> None:
    client = SupabaseClient()
    client.insert("agent_events", {"event": "user_login"})
    client.insert("agent_events", {"event": "message_sent"})

    print(client.fetch_all("agent_events"))


if __name__ == "__main__":
    main()
