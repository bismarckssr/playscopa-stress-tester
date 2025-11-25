import os
from dotenv import load_dotenv
from dataclasses import dataclass


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
