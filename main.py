import asyncio
import websockets
import socket
import requests
from datetime import datetime


def get_public_ip():
    try:
        public_ip = requests.get('https://api.ipify.org').text
    except requests.RequestException:
        public_ip = "Could not retrieve public IP"
    return public_ip


async def handle_connection(websocket, path):
    client_ip = websocket.remote_address[0]
    async for message in websocket:
        timestamp = datetime.now().strftime("[%Y-%b-%d @%I:%M%p]")
        log_entry = f"{timestamp} {client_ip} Received Data: {message}\n"
        print(log_entry.strip())

        log_filename = datetime.now().strftime(
            "./logs/%Y-%m-%d_%H-%M-%S-log.txt")
        with open(log_filename, "a") as log_file:
            log_file.write(log_entry)

        await websocket.send(f"Server response to {client_ip}: {message}")


async def main():
    public_ip = get_public_ip()
    print(f"WebSocket server started on ws://{public_ip}:35319")

    async with websockets.serve(handle_connection, "localhost", 35319):
        await asyncio.Future()


asyncio.run(main())
