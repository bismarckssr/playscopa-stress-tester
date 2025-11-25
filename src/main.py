from src.config import Config as cfg
from src.client import StressClient
import asyncio

# Caricamento configurazione
configObj = cfg.load_from_env()
tasks_lists = set()


async def main():
    if not configObj.clients or not configObj.ws_url:
        print("Imposta STRESSER_SESSIONS e WEBSOCKET_URL!")
        exit(1)
    stress_clients_counter = configObj.clients
    async with asyncio.TaskGroup() as tg:
        for i in range(stress_clients_counter):
            stress_client = StressClient(i, configObj.ws_url)
            task = tg.create_task(stress_client.start_stress())
            tasks_lists.add(task)
            await asyncio.sleep(
                0.00004
            )  # Funziona bene in locale, via cloudflare manco per scherzo


if __name__ == "__main__":
    asyncio.run(main())
