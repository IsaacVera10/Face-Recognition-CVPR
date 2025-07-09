from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class RecognitionLog(Base):
    __tablename__ = "recognition_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    timestamp = Column(DateTime)
    location = Column(String(100))
    confidence = Column(Float)

    # Relaciones
    user = relationship("User", backref="recognition_logs")
