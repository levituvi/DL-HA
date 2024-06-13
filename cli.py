import httpx
import sys

BASE_URL_1 = "http://localhost:8000"
BASE_URL_2 = "http://localhost:8001"

async def start_game(pong_time_ms):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL_1}/ping")
        if response.status_code == 200:
            print(f"Game started with pong_time_ms = {pong_time_ms}")
        else:
            print("Failed to start game")

def pause_game():
    # Not implemented in server
    pass

def resume_game():
    # Not implemented in server
    pass

def stop_game():
    # Not implemented in server
    pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: pong-cli.py <command> [param]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "start":
        if len(sys.argv) != 3:
            print("Usage: pong-cli.py start <pong_time_ms>")
            sys.exit(1)
        pong_time_ms = int(sys.argv[2])
        import asyncio
        asyncio.run(start_game(pong_time_ms))
    elif command == "pause":
        pause_game()
    elif command == "resume":
        resume_game()
    elif command == "stop":
        stop_game()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
