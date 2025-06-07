import json
import websocket

# Connect to WebSocket
ws = websocket.create_connection("http://challenge.nahamcon.com:32207")

# Send numbers in chunks of 10,000
chunk_size = 10000
max_number = 2000000

for i in range(0, max_number + 1, chunk_size):
    chunk = list(range(i, min(i + chunk_size, max_number + 1)))
    payload = {
        "action": "check",
        "numbers": chunk
    }
    ws.send(json.dumps(payload))
    print(f"Sent chunk {i} - {i + len(chunk) - 1}")
    
    # Optional: receive server response
    # response = ws.recv()
    # print(response)

ws.close()