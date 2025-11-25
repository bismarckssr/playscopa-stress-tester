# Playscopa Stress Tester

A WebSocket stress testing tool for [Playscopa](https://playscopa.online/), an online implementation of the Italian card game Scopa.

## :clipboard: Description

This tool allows you to test the performance and stability of the Playscopa WebSocket server by simulating a large number of concurrent connected clients. Each virtual client behaves like a real player: connects to the server, responds to pings, receives starting cards, and executes moves during the game.

### :sparkles: Features

- **Concurrent connections**: Creates thousands of concurrent WebSocket clients
- **Realistic behavior**: Each client simulates a real player
  - Responds to welcome messages
  - Handles ping/pong
  - Receives and plays cards
  - Chooses combos when requested
- **Asynchronous architecture**: Uses `asyncio` for efficient connection management
- **Configurable**: Customizable number of clients and test duration

## :package: Requirements

- Python 3.11+
- pip

## :rocket: Installation

1. Clone the repository:
```bash
git clone https://github.com/bismarckssr/playscopa-stress-tester.git
cd playscopa-stress-tester
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## :gear: Configuration

Create a `.env` file in the project root (you can copy `.env.example`):

```env
WEBSOCKET_URL = "https://ws.playscopa.online/"
STRESSER_SESSIONS = 1000
DURATION = 600
```

### Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `WEBSOCKET_URL` | WebSocket server URL to test | `ws://localhost:8080` |
| `STRESSER_SESSIONS` | Number of concurrent clients to simulate | `10` |
| `DURATION` | Test duration in seconds (not yet implemented) | `5` |

## :dart: Usage

Run the stress test:

```bash
python -m src.main
```

The program will create the specified number of clients and connect them to the server with a small delay between connections (0.00004s) to avoid immediately overwhelming the server.

## :building_construction: Architecture

### Project Structure

```
src/
├── __init__.py
├── main.py          # Application entry point
├── config.py        # Configuration management from .env
└── client.py        # WebSocket client implementation
```

### Main Components

#### StressClient (`client.py`)

Each `StressClient` instance represents a virtual client that:

1. **Listener Loop** (`_listener_loop`): Receives and processes messages from the server
   - `welcome`: Responds with options request
   - `ping`: Responds with pong
   - `start`/`turn`: Activates sending a move
   - `startingCards`: Saves received cards
   - `remove_table_cards_combosAvail`: Chooses the first available combo

2. **Sender** (`_sender`): Sends moves to the server
   - Waits for cards to be available
   - Waits for turn
   - Sends a random move

3. **Synchronization**: Uses `asyncio.Event` to coordinate listener and sender:
   - `cards_populated`: Signals when cards are available
   - `clear_to_send`: Signals when it's the client's turn

## :wrench: Technical Notes

- The 0.00004s delay between connections works well locally but may require adjustments in production (especially behind Cloudflare)
- Uses `asyncio.TaskGroup` for clean concurrent task management
- Connection timeout set to 30 seconds
- This is not a DDoS attack: it's an authorized testing tool for your own server

## :warning: Limitations

- The `DURATION` parameter is configurable but not yet implemented
- Clients don't implement complete game logic (e.g., advanced game strategy)
- No detailed statistics collection (to be implemented)

## :hammer_and_wrench: Development

To install development dependencies:

```bash
pip install -r requirements-dev.txt
```

## :page_facing_up: License

MIT License - see [LICENSE](LICENSE) for details.

Copyright (c) 2025 bismarckssr

## :balance_scale: Disclaimer

This tool was created exclusively for testing servers for which you have authorization. Improper use for DDoS attacks or overloading unauthorized servers is illegal and unethical.
