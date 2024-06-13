from fastapi import FastAPI
import uvicorn
import httpx
import asyncio
from threading import Thread, Event

app = FastAPI()
pause_event = Event()
stop_event = Event()
pong_time_ms = 1000
peer_url = None

@app.post("/ping")
async def ping():
    return {"message": "pong"}

async def ping_peer():
    global peer_url, pong_time_ms
    async with httpx.AsyncClient() as client:
        while not stop_event.is_set():
            pause_event.wait()
            try:
                response = await client.post(f"{peer_url}/ping")
                if response.status_code == 200:
                    print("Received pong, sleeping for", pong_time_ms, "ms")
                    await asyncio.sleep(pong_time_ms / 1000.0)
            except Exception as e:
                print(f"Error pinging peer: {e}")
                await asyncio.sleep(1)  # Add a delay before retrying

def start_ping_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    thread = Thread(target=loop.run_until_complete, args=(ping_peer(),))
    thread.start()
    return thread

@app.on_event("startup")
async def startup_event():
    global pause_event, stop_event
    pause_event.set()
    stop_event.clear()
    start_ping_thread()

@app.on_event("shutdown")
async def shutdown_event():
    stop_event.set()

def run_server(host, port, peer):
    global peer_url
    peer_url = peer
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python server.py <host> <port> <peer_url>")
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])
    peer = sys.argv[3]
    run_server(host, port, peer)
