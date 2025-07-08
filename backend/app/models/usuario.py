from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.sql.sqltypes import Date
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)                   # Internal DB ID
    user_id = Column(String(32), unique=True, nullable=False, index=True) # e.g., 'ID-78945612'
    name = Column(String(100), nullable=False)
    dni = Column(String(15), unique=True, nullable=False)                # National ID
    role = Column(String(50))                                            # e.g., 'Employee'
    tags = Column(String(200))                                           # e.g., "Authorized,Employee" (simple CSV)
    gender = Column(String(20))                                          # 'Male', 'Female', 'Other'
    date_of_birth = Column(Date)                                         # Date of Birth
    image_url = Column(String(300))                                      # URL to profile image
    recognition_count = Column(Integer, default=0)                       # Total times recognized
    last_seen = Column(DateTime)                                         # Last seen datetime
    last_location = Column(String(100))                                  # Last seen location
    created_at = Column(DateTime(timezone=True), server_default=func.now())