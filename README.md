# Live WebSocket Poll

A small real-time polling app. A Python WebSocket server tracks votes in memory, and a plain HTML/CSS/JS frontend shows live, animated progress bars as votes come in.

## How it works

- `server1.py` runs a WebSocket server (via the `websockets` library) on `ws://localhost:8765`. It keeps a vote count for each option and broadcasts the current totals to every connected browser whenever a new vote arrives.
- `index.html` / `style.css` / `index.js` make up the frontend. The page connects to the server over a WebSocket, sends a vote when a button is clicked, and updates the bars and counters whenever it receives a new broadcast.

## Project structure

| File | Purpose |
|------|---------|
| `server1.py` | WebSocket server — holds the vote state and broadcasts updates |
| `index.html` | Poll page markup |
| `style.css` | Styling for the poll page |
| `index.js` | Frontend WebSocket client logic |
| `requirements.txt` | Python dependency list |

## Requirements

- Python 3.8+
- The `websockets` package

Install it with:

```bash
pip install -r requirements.txt
```

## Run it

1. Start the server:

   ```bash
   python server1.py
   ```

   You should see `Polling WebSocket Server started on ws://localhost:8765`.

2. Open `index.html` in a browser (just double-click it, or use a tool like VS Code's Live Server).

3. Click an option to vote. Open the page in a few browser tabs to see the bars update live across all of them.

## Notes

- All vote data is kept in memory on the server — it resets every time the server restarts.
- This is a local demo: the frontend connects to `ws://localhost:8765`, so the server needs to be running on the same machine you're viewing the page from.

## Author

Elisee Biyong Enane
