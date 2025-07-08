from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.recognition.face_recognition import router as recognition_router
from app.core.config import settings

app = FastAPI(title="CVPR Facial Recognition API")
print(f"Starting {settings.APP_NAME} on port {settings.PORT}")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS, #Lista de ips permitidas
    allow_credentials=True, # Permite cookies y autenticación
    allow_methods=["*"],    # Permite todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],    # Permite todos los headers (authentication, content-type, etc.)
)

@app.get("/")
def root():
    return {"mensaje": "Bienvenido a la API de reconocimiento facial"}

# Montamos el router del endpoint
app.include_router(recognition_router, prefix="/api")

