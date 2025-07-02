import face_recognition
import numpy as np
import cv2

def detect_faces(image_bytes: bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detectar caras
    face_locations = face_recognition.face_locations(rgb_image)

    # Por ahora no extraes embeddings
    return face_locations, []