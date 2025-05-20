import asyncio
import websockets
import sys

PORT = 8000
EXPECTED_CLIENTS = 10
MESSAGE_COUNT =  1000

connected_clients = set()

async def handler(websocket):
    connected_clients.add(websocket)
    print(f"Client connected ({len(connected_clients)}/{EXPECTED_CLIENTS})")

    try:
        if len(connected_clients) == EXPECTED_CLIENTS:
            print("All clients connected. Starting test...")
            start_time = asyncio.get_event_loop().time()
            
            websockets.broadcast(connected_clients, "test-payload")

            end_time = asyncio.get_event_loop().time()
            print(f"Test completed in {(end_time - start_time)*1000:.2f}ms")
            print(f"Sent {MESSAGE_COUNT} messages to {EXPECTED_CLIENTS} clients")

        await websocket.wait_closed()

    finally:
        connected_clients.remove(websocket)

async def main():
    print(f"Websockets server starting on port {PORT}")
    print(f"Waiting for {EXPECTED_CLIENTS} clients to connect...")
    
    async with websockets.serve(handler, "localhost", PORT):
        await asyncio.Future()

asyncio.run(main())