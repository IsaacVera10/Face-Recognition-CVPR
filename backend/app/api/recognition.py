def recognize_face(frame):
    # Aquí irá el reconocimiento real (modelo, embeddings, etc.)
    # Por ahora, solo una respuesta dummy
    return "Persona Desconocida"


import random

def recognize_faces_in_boxes(frame, boxes):
    personas_ficticias = [
        "Lauren Alexis", "Faith Lianne", "Alexa Pearl",
        "Soft Sparkling", "Persona Desconocida"
    ]

    results = []
    for box in boxes:
        x, y, w, h = box["x"], box["y"], box["w"], box["h"]
        # Aquí podrías extraer el rostro con:
        # face = frame[y:y+h, x:x+w]

        nombre = random.choice(personas_ficticias)
        confidence = round(random.uniform(0.75, 0.99), 2) if nombre != "Persona Desconocida" else 0.5

        results.append({
            "name": nombre,
            "confidence": confidence,
            "box": box
        })

    return results