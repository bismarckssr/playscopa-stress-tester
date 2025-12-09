import asyncio
from dataclasses import dataclass

from src.Config import Config
from src.StressClient import StressClient


@dataclass
class StressEngine:
    config: Config

    def __post_init__(self):
        if not isinstance(self.config, Config):
            raise TypeError("Il parametro config deve essere di classe Config")

    async def run(self):
        async with asyncio.TaskGroup() as tg:
            for i in range(self.config.clients):
                stress_client = StressClient(i, self.config.ws_url)
                tg.create_task(stress_client.start_stress())
                await asyncio.sleep(0.00004)
