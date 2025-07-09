from fastapi import FastAPI, UploadFile, File, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from PIL import Image
import io
import base64
import numpy as np
import torch
import faiss
from facenet_pytorch import MTCNN, InceptionResnetV1
import os
import base64
from starlette.websockets import WebSocketDisconnect
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


# === CONFIGURACIÓN ===
RESIZE_TO = 160
EMBEDDING_DIM = 512
THRESHOLD = 0.8
MAX_DISTANCE = 1.2
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# === MODELOS ===
mtcnn = MTCNN(image_size=RESIZE_TO, margin=10, device=device)
model = InceptionResnetV1(pretrained='vggface2').eval().to(device)

# === BASE DE DATOS ===
embeddings = np.load("embeddings.npy").astype('float32')
names = np.load("names.npy")
user_ids = np.load("user_ids.npy")
index = faiss.read_index("faiss_index_uid.bin")

# === FASTAPI APP ===
app = FastAPI(title="PRUEBA-WS-ACTIVO")

# Permitir requests desde tu app Flutter (ajusta si usas IP real)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === MODELOS DE RESPUESTA ===
class FaceResult(BaseModel):
    user_id: str
    confidence: float
    box: List[int]

class PredictionResponse(BaseModel):
    results: List[FaceResult]

# === ENDPOINT ===
@app.post("/recognize", response_model=PredictionResponse)
async def recognize_face(file: UploadFile = File(...)):
    print("🟢 Frame recibido")
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    boxes, _ = mtcnn.detect(image)

    results = []
    if boxes is not None:
        for box in boxes:
            x1, y1, x2, y2 = [int(coord) for coord in box]
            face = image.crop((x1, y1, x2, y2)).resize((RESIZE_TO, RESIZE_TO))
            face_tensor = mtcnn(face)

            if face_tensor is not None:
                face_tensor = face_tensor.unsqueeze(0).to(device)
                with torch.no_grad():
                    emb = model(face_tensor).cpu().numpy().astype('float32')

                D, I = index.search(emb, 1)
                distance = D[0][0]
                idx = I[0][0]

                if distance < THRESHOLD:
                    confidence = max(0, 1 - distance / MAX_DISTANCE)
                    user_id = user_ids[idx]
                else:
                    confidence = 0.0
                    user_id = "Desconocido"

                results.append(FaceResult(
                    user_id=user_id,
                    confidence=round(confidence, 2),
                    box=[x1, y1, x2, y2]
                ))

    return {"results": results}



@app.websocket("/ws/recognize")
async def recognize_face_ws(websocket: WebSocket):
    print("🟢 Frame recibido")
    await websocket.accept()
    saved = False  # <--- Bandera para guardar solo el primer frame
    try:
        while True:
            # Recibe la imagen como binario
            contents = await websocket.receive_bytes()
            
            # ===== Guardar el primer frame recibido =====
            if not saved:
                with open("frame_debug.jpg", "wb") as f:
                    f.write(contents)
                print("🟡 Frame guardado en frame_debug.jpg")
                saved = True
            # ============================================

            image = Image.open(io.BytesIO(contents)).convert("RGB")

            boxes, _ = mtcnn.detect(image)
            results = []
            if boxes is not None:
                for box in boxes:
                    x1, y1, x2, y2 = [int(coord) for coord in box]
                    face = image.crop((x1, y1, x2, y2)).resize((RESIZE_TO, RESIZE_TO))
                    face_tensor = mtcnn(face)
                    if face_tensor is not None:
                        face_tensor = face_tensor.unsqueeze(0).to(device)
                        with torch.no_grad():
                            emb = model(face_tensor).cpu().numpy().astype('float32')
                        D, I = index.search(emb, 1)
                        distance = D[0][0]
                        idx = I[0][0]
                        if distance < THRESHOLD:
                            confidence = max(0, 1 - distance / MAX_DISTANCE)
                            user_id = user_ids[idx]
                        else:
                            confidence = 0.0
                            user_id = "Desconocido"
                        results.append({
                            "user_id": user_id,
                            "confidence": round(confidence, 2),
                            "box": [x1, y1, x2, y2]
                        })
                        print(results)
            await websocket.send_json({"results": results})
    except WebSocketDisconnect:
        print("Cliente relay desconectado (modelo).")
    except Exception as e:
        print("WS error:", e)
