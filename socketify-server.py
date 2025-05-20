from socketify import App, AppOptions, OpCode, CompressOptions
import time
import sys

PORT = 8000
EXPECTED_CLIENTS = 50
MESSAGE_COUNT = 100

connected_clients = 0

def ws_open(ws):
    global connected_clients
    ws.subscribe("room")
    connected_clients += 1
    print(f"Client connected ({connected_clients}/{EXPECTED_CLIENTS})")
    
    if connected_clients == EXPECTED_CLIENTS:
        print("All clients connected. Starting test...")
        start_time = time.time()
        
        for i in range(MESSAGE_COUNT):
            ws.app.publish("room", "test-payload")
        
        end_time = time.time()
        print(f"Test completed in {(end_time - start_time)*1000:.2f}ms")
        print(f"Sent {MESSAGE_COUNT} messages to {EXPECTED_CLIENTS} clients")

def ws_close(ws, code, message):
    global connected_clients
    connected_clients -= 1
    
    if connected_clients == 0:
        ws.app.close()

def make_app(app):
    app.ws("/*", {
        'open': ws_open,
        'close': ws_close
    })

if __name__ == "__main__":
    print(f"Websockets server starting on port {PORT}")
    print(f"Waiting for {EXPECTED_CLIENTS} clients to connect...")
    
    app = App()
    make_app(app)
    app.listen(PORT)
    app.run()