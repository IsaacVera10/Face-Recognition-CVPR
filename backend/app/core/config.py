from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "CVPR Facial API"
    DEBUG: bool = True
    PORT: int = 8000
    ALLOWED_ORIGINS: list[str] = ["*"]  # Puedes especificar dominios permitidos

settings = Settings()