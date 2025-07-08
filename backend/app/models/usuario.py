from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    dni = Column(String(15), unique=True, nullable=False)
    rol = Column(String(50))
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())