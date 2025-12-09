import asyncio

from src.Config import Config as cfg
from src.StressEngine import StressEngine


async def main():
    config = cfg.load_from_env()
    engine = StressEngine(config)
    await engine.run()


if __name__ == "__main__":
    asyncio.run(main())
