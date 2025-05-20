from socketify import App
import time

PORT = 8000
EXPECTED_CLIENTS = 10
MESSAGE_COUNT = 1000

app = App()
connected_clients = 0

@app.ws("/")
def ws(ws):
    @ws.on("open")
    def on_open():
        global connected_clients
        ws.subscribe("room")
        connected_clients += 1
        print(f"Client connected ({connected_clients}/{EXPECTED_CLIENTS})")
        
        if connected_clients == EXPECTED_CLIENTS:
            print("All clients connected. Starting test...")
            start_time = time.time()
            
            app.publish("room", "test-payload")
            
            end_time = time.time()
            print(f"Test completed in {(end_time - start_time)*1000:.2f}ms")
            print(f"Sent {MESSAGE_COUNT} messages to {EXPECTED_CLIENTS} clients")
    
    @ws.on("close")
    def on_close():
        global connected_clients
        connected_clients -= 1

print(f"Socketify server starting on port {PORT}")
print(f"Waiting for {EXPECTED_CLIENTS} clients to connect...")
app.listen(PORT)
app.run()