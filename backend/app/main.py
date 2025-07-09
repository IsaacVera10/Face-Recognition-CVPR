from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.recognition import router as recognition_router
from app.api.routes.users import router as users_router
from app.api.routes.logs import router as logs_router
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
app.include_router(users_router, prefix="/api")
app.include_router(logs_router, prefix="/api")

