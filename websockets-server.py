import asyncio
import websockets
import sys

PORT = 8000
EXPECTED_CLIENTS = 50
MESSAGE_COUNT =  100

connected_clients = set()
main_future = None

async def handler(websocket):
    global main_future
    connected_clients.add(websocket)
    print(f"Client connected ({len(connected_clients)}/{EXPECTED_CLIENTS})")

    try:
        if len(connected_clients) == EXPECTED_CLIENTS:
            print("All clients connected. Starting test...")
            start_time = asyncio.get_event_loop().time()
            
            for i in range(MESSAGE_COUNT):
                websockets.broadcast(connected_clients, "test-payload")
            
            end_time = asyncio.get_event_loop().time()
            print(f"Test completed in {(end_time - start_time)*1000:.2f}ms")
            print(f"Sent {MESSAGE_COUNT} messages to {EXPECTED_CLIENTS} clients")

        await websocket.wait_closed()

    finally:
        connected_clients.remove(websocket)
        
        if len(connected_clients) == 0:
            main_future.set_result(None)

async def main():
    global main_future

    print(f"Websockets server starting on port {PORT}")
    print(f"Waiting for {EXPECTED_CLIENTS} clients to connect...")
    
    main_future = asyncio.Future()
    
    async with websockets.serve(handler, "localhost", PORT):
        await main_future

asyncio.run(main())