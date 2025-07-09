import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import cv2
import numpy as np
import torch
import faiss
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1


# === Configuración general ===
EMBEDDING_DIM = 512
RESIZE_TO = 160
THRESHOLD = 0.8  # Distancia máxima para considerar "conocido"
MAX_DISTANCE = 1.2  # distancia máxima esperada (ajustable)

# === Cargar modelo y base ===
device = 'cuda' if torch.cuda.is_available() else 'cpu'

mtcnn = MTCNN(image_size=RESIZE_TO, margin=10, device=device)
model = InceptionResnetV1(pretrained='vggface2').eval().to(device)

# Cargar embeddings y nombres
embeddings = np.load("embeddings.npy").astype('float32')
names = np.load("names.npy")

# Cargar índice FAISS
index = faiss.read_index("faiss_index_uid.bin")

# === Captura desde cámara ===
cap = cv2.VideoCapture(0)

print("🎥 Presiona 'q' para salir")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir a PIL
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Detectar rostros
    boxes, _ = mtcnn.detect(img)

    if boxes is not None:
        for box in boxes:
            x1, y1, x2, y2 = [int(coord) for coord in box]
            face_crop = img.crop((x1, y1, x2, y2)).resize((RESIZE_TO, RESIZE_TO))

            # Obtener embedding
            face_tensor = mtcnn(face_crop)
            if face_tensor is not None:
                face_tensor = face_tensor.unsqueeze(0).to(device)
                with torch.no_grad():
                    emb = model(face_tensor).cpu().numpy().astype('float32')

                # Comparar con FAISS
                D, I = index.search(emb, 1)
                distance = D[0][0]
                idx = I[0][0]

                if distance < THRESHOLD:
                    confidence = max(0, 1 - distance / MAX_DISTANCE)
                    confidence_pct = int(confidence * 100)
                    label = f"{names[idx]} [Confianza: {confidence_pct}%]"
                    # names[idx] QUERY
                    
                    # Color dinámico según confianza
                    if confidence_pct >= 80:
                        color = (0, 255, 0)     # Verde
                    elif confidence_pct >= 50:
                        color = (0, 165, 255)   # Naranja
                    else:
                        color = (0, 0, 255)     # Rojo
                else:
                    label = "Desconocido"
                    color = (0, 0, 255)         # Rojo

                # Dibujar
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    cv2.imshow("Reconocimiento Facial (local)", frame)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
