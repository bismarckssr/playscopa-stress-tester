import asyncio
import json
from dataclasses import dataclass, field

from websockets.asyncio.client import ClientConnection, connect


@dataclass
class StressClient:
    id: int
    ws_url: str

    current_cards: list[dict] = field(init=False)
    cards_populated: asyncio.Event = field(init=False)
    clear_to_send: asyncio.Event = field(init=False)

    # usare un asyncio.Lock richiede 1 altra coroutine. Altrimenti ci si ritrova dentro la stessa coroutine ad aspettare un lock che non verrà mai settato perchè la coroutine stessa è andata in await
    # questo perchè JSS invia PRIMA lo start/turn e poi startingCards. Se arriva prima start/turn e non ha carte da giocare entra in .wait() per il lock. Però il lock viene settato solo dopo quando arriva startingCards. Però come fa a settarsi il lock se la coroutine è sospesa a causa dell'await precedente? :D

    async def _sender(self, connection: ClientConnection) -> None:
        while True:
            await self.cards_populated.wait()
            await self.clear_to_send.wait()
            current_card = self.current_cards.pop()
            await connection.send(
                json.dumps(
                    {
                        "type": "move",
                        "card": {
                            "valore": current_card.get("valore"),
                            "seme": current_card.get("seme"),
                        },
                    }
                )
            )
            if not self.current_cards:
                self.cards_populated.clear()
            self.clear_to_send.clear()

    async def _listener_loop(self, connection: ClientConnection) -> None:
        while True:
            raw_msg = await connection.recv()  # fare await significa sospendere la coroutine fino a quando non viene risvegliata
            msg = json.loads(raw_msg)
            # print(f"Ricevuto messaggio: {msg}")

            if msg.get("type") == "welcome":
                await connection.send(json.dumps({"type": "options"}))

            elif msg.get("type") == "ping":
                await connection.send(json.dumps({"type": "pong"}))

            elif (
                msg.get("type") == "start" or msg.get("type") == "turn"
            ):  # Eseguiamo una mossa a caso in due casi: o quando abbiamo lo start o quando ci capita un turno durante il match
                if msg.get("turn"):
                    self.clear_to_send.set()

            elif msg.get("type") == "startingCards":
                # Salvo le carte in current_cards
                self.current_cards = msg.get("arr")

                # Imposto l'evento
                self.cards_populated.set()

            elif msg.get("type") == "remove_table_cards_combosAvail":
                # Scelgo la prima opzione
                combos = msg.get("combos")
                selected_combo = combos[0]
                await connection.send(
                    json.dumps({"type": "combo_response", "combo": selected_combo})
                )

    async def start_stress(self):
        print(f"Starting stress test with id: {self.id}")
        self.cards_populated = asyncio.Event()
        self.clear_to_send = asyncio.Event()
        try:
            async with connect(self.ws_url, open_timeout=30) as websocket:
                # Iniziando un await il codice non prosegue fino a quando
                # _listener_loop ritorna o va in uno stato di sleep/waiting
                async with asyncio.TaskGroup() as tg:
                    tg.create_task(self._listener_loop(websocket))
                    tg.create_task(self._sender(websocket))
        except TimeoutError:
            print(f"Timeout per {self.id}")
