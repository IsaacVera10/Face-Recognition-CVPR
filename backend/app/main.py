# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import recognize
from app.core.config import settings

app = FastAPI(title="CVPR Facial Recognition API")

# Configuración de CORS para permitir conexión desde la app móvil
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montamos el router del endpoint
app.include_router(recognize.router, prefix="/api")

