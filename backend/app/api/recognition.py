from fastapi import APIRouter, UploadFile, File
from typing import List
from app.services.detector import detect_faces
from app.models.response import FaceRecognitionResponse
import cv2
import numpy as np

router = APIRouter()

@router.post("/recognize", response_model=List[FaceRecognitionResponse])
async def recognize(file: UploadFile = File(...)):
    image_bytes = await file.read()
    face_locations, _ = detect_faces(image_bytes)

    results = []
    for (top, right, bottom, left) in face_locations:
        results.append(FaceRecognitionResponse(
            name="Unknown",
            bbox=[left, top, right, bottom]
        ))
    
    # DEBUG
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)

    cv2.imwrite("deteccion_debug.jpg", image)
    #DEBUG
    return results