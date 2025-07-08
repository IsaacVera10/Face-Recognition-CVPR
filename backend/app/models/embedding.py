from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func
from app.core.database import Base

class Embedding(Base):
    __tablename__ = "embeddings"

    id_embedding = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="CASCADE"))
    vector = Column(ARRAY(Float), nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    pose = Column(String(20))  # Opcional: frontal, perfil, etc.

    usuario = relationship("Usuario", backref="embeddings")