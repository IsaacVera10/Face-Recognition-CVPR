import asyncio
import websockets

async def test_ws():
    ws_url = "wss://dependable-appreciation-production.up.railway.app/api/ws/recognize"  # O el de ngrok si es remoto
    with open("test.jpg", "rb") as f:
        image_bytes = f.read()
    async with websockets.connect(ws_url) as websocket:
        await websocket.send(image_bytes)
        result = await websocket.recv()
        print("Respuesta del modelo:", result)

asyncio.run(test_ws())