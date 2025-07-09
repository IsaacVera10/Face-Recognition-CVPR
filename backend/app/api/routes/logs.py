from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from app.core.database import get_db
from app.models.logs import RecognitionLog as RecognitionLogModel
from app.models.user import User
from app.schemas.recognition_log import RecognitionLog as RecognitionLogSchema, RecognitionLogListItem
from typing import List
from datetime import date

router = APIRouter()

def calculate_age(birthdate: date) -> int:
    today = date.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

@router.get("/recognition/logs", response_model=List[RecognitionLogListItem])
def get_recognition_logs(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    logs = (
        db.query(RecognitionLogModel)
        .options(joinedload(RecognitionLogModel.user))
        .order_by(RecognitionLogModel.timestamp.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    response = []
    for log in logs:
        user = log.user
        age = calculate_age(user.date_of_birth) if user and user.date_of_birth else None
        response.append(
            RecognitionLogListItem(
                name=user.name if user else "Unknown",
                confidence=round(log.confidence * 100, 1) if log.confidence <= 1.0 else float(log.confidence),
                timestamp=log.timestamp.isoformat(),
                location=log.location,
                user_id=user.user_id if user else "",
                age=age,
                gender=user.gender if user else None,
                date_of_birth=user.date_of_birth.isoformat() if user and user.date_of_birth else None,
                tags=[tag.strip() for tag in user.tags.split(",")] if user and user.tags else [],
                notes="Authorized personnel" if user and "Authorized" in (user.tags or "") else None,
            )
        )
    return response