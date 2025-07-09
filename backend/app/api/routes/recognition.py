import os
from fastapi import APIRouter, UploadFile, File
import httpx
from dotenv import load_dotenv
from app.core.config import settings

load_dotenv()  # Carga las variables del .env

router = APIRouter()

LOCAL_MODEL_URL = settings.LOCAL_MODEL_URL

@router.post("/recognize")
async def recognize_face(file: UploadFile = File(...)):
    contents = await file.read()
    async with httpx.AsyncClient() as client:
        files = {'file': ('frame.jpg', contents, file.content_type)}
        resp = await client.post(LOCAL_MODEL_URL, files=files)
    print("Status code:", resp.status_code)
    print("Response text:", resp.text)
    return resp.json()
