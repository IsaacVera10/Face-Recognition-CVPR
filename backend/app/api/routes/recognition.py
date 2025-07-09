import os
from fastapi import APIRouter, UploadFile, File, WebSocket
from starlette.websockets import WebSocketDisconnect
import httpx
from dotenv import load_dotenv
from app.core.config import settings
import websockets
import asyncio

load_dotenv()  # Carga las variables del .env

router = APIRouter()

LOCAL_MODEL_URL = settings.LOCAL_MODEL_URL
LOCAL_MODEL_WS_URL = settings.LOCAL_MODEL_WS_URL

@router.post("/recognize")
async def recognize_face(file: UploadFile = File(...)):
    contents = await file.read()
    async with httpx.AsyncClient() as client:
        files = {'file': ('frame.jpg', contents, file.content_type)}
        resp = await client.post(LOCAL_MODEL_URL, files=files)
    print("Status code:", resp.status_code)
    print("Response text:", resp.text)
    return resp.json()

@router.websocket("/ws/recognize")
async def recognize_face_proxy(websocket: WebSocket):
    await websocket.accept()
    try:
        async with websockets.connect(LOCAL_MODEL_WS_URL) as model_ws:
            while True:
                data = await websocket.receive_bytes()
                await model_ws.send(data)
                response = await model_ws.recv()
                await websocket.send_text(response)
    except WebSocketDisconnect:
        print("Cliente desconectado (relay).")
    except Exception as e:
        print("Proxy error:", e)
        # Aquí ya no pongas await websocket.close()