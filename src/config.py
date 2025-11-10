import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    ws_url: str
    clients: int
    duration: int

    @staticmethod
    def load_from_env() -> "Config":
        return Config(
            ws_url=os.getenv("WS_URL", "ws://localhost:8080"),
            clients=int(os.getenv("CLIENTS", "10")),
            duration=int(os.getenv("DURATION", "5"))
        )