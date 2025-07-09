from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "CVPR Facial API"
    DEBUG: bool = True
    PORT: int = 8000
    ALLOWED_ORIGINS: List[str] = ["*"]  # Puedes especificar dominios permitidos

    
    DATABASE_PUBLIC_URL: str = "postgresql://postgres:postgres@localhost/reconocimiento" # Valor por defecto

    class Config:
        env_file = ".env"  # Cargar variables desde archivo .env

settings = Settings()