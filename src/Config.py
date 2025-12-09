import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Config:
    ws_url: str
    clients: int
    duration: int

    @staticmethod
    def load_from_env() -> "Config":
        load_dotenv(".env", override=True)
        return Config(
            ws_url=os.getenv("WEBSOCKET_URL", "ws://localhost:8080"),
            clients=int(os.getenv("STRESSER_SESSIONS", "10")),
            duration=int(os.getenv("DURATION", "5")),
        )
