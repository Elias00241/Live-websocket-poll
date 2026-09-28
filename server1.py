import asyncio
import json
import logging
from websockets.server import serve

# Configure clean logging
logging.basicConfig(level=logging.INFO)

# Global State: Tracks active socket connections and vote counts
CONNECTED_CLIENTS = set()
VOTE_STATE = {
    "Python": 0,
    "JavaScript": 0,
    "Go": 0
}

async def broadcast_state():
    """Utility function to send the current vote state to all connected users."""
    if CONNECTED_CLIENTS:
        # Convert our dictionary to a JSON string payload
        payload = json.dumps(VOTE_STATE)
        # Gather all transmission tasks to send concurrently
        await asyncio.gather(*[client.send(payload) for client in CONNECTED_CLIENTS])

async def handler(websocket):
    """Handles individual client life cycles and incoming vote actions."""
    # Register the new client connection
    CONNECTED_CLIENTS.add(websocket)
    logging.info(f"Client connected. Total clients: {len(CONNECTED_CLIENTS)}")
    
    try:
        # Immediately send the current standings to the newly joined user
        await websocket.send(json.dumps(VOTE_STATE))
        
        # Listen indefinitely for incoming messages from this client
        async for message in websocket:
            data = json.loads(message)
            voted_option = data.get("vote")
            
            # If the option exists in our state, increment it
            if voted_option in VOTE_STATE:
                VOTE_STATE[voted_option] += 1
                logging.info(f"Vote received for {voted_option}: {VOTE_STATE[voted_option]}")
                # Broadcast the brand new totals to everyone right away
                await broadcast_state()
                
    except Exception as e:
        logging.error(f"Error handling client: {e}")
    finally:
        # Unregister the client cleanly when they close the tab or disconnect
        CONNECTED_CLIENTS.remove(websocket)
        logging.info(f"Client disconnected. Total clients: {len(CONNECTED_CLIENTS)}")

async def main():
    # Run the WebSocket server on localhost port 8765
    async with serve(handler, "localhost", 8765):
        logging.info("Polling WebSocket Server started on ws://localhost:8765")
        await asyncio.get_running_loop().create_future() # Keep running forever

if __name__ == "__main__":
    asyncio.run(main())




