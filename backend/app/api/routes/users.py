from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.user import User
from app.models.logs import RecognitionLog
from app.schemas.user import UserPreview, UserDetail
from app.schemas.recognition_log import RecognitionHistoryResponse, RecognitionHistoryItem
from app.core.database import get_db
from datetime import date, datetime

router = APIRouter()

def calcular_edad(date_of_birth: date) -> int:
    today = date.today()
    return today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))


@router.get("/users/by-page", response_model=List[UserDetail])
def get_users_by_page(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    users = (
        db.query(User)
        .order_by(User.last_seen.desc().nullslast())
        .offset(offset)
        .limit(limit)
        .all()
    )
    response = [
        UserDetail(
            id=user.id,
            user_id=user.user_id,
            name=user.name,
            image_url=user.image_url,
            age=calcular_edad(user.date_of_birth) if user.date_of_birth else None,
            gender=user.gender,
            date_of_birth=user.date_of_birth.isoformat() if user.date_of_birth else None,
            recognition_count=user.recognition_count or 0,
            last_seen=user.last_seen.isoformat() if user.last_seen else None,
            last_location=user.last_location,
            tags=[tag.strip() for tag in user.tags.split(",")] if user.tags else [],
        )
        for user in users
    ]

    return response


def calculate_age(birthdate: date) -> int:
    today = date.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

@router.get("/users/{user_id}", response_model=UserDetail)
def get_user_detail(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Calcula la edad si hay fecha de nacimiento
    age = None
    if user.date_of_birth:
        age = calculate_age(user.date_of_birth)
    
    return UserDetail(
        id=user.id,
        user_id=user.user_id,
        name=user.name,
        image_url=user.image_url,
        age=age,
        gender=user.gender,
        date_of_birth=user.date_of_birth.isoformat() if user.date_of_birth else None,
        recognition_count=user.recognition_count or 0,
        last_seen=user.last_seen.isoformat() if user.last_seen else None,
        last_location=user.last_location,
        tags=[tag.strip() for tag in user.tags.split(",")] if user.tags else [],
    )

@router.get("/users/{user_id}/recognition-history", response_model=RecognitionHistoryResponse)
def get_recognition_history(
    user_id: str,
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    logs = (
        db.query(RecognitionLog)
        .filter(RecognitionLog.user_id == user_id)
        .order_by(RecognitionLog.timestamp.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    if logs is None:
        raise HTTPException(status_code=404, detail="User not found or no logs")

    items = [
        RecognitionHistoryItem(
            datetime=log.timestamp.isoformat(),
            location=log.location,
            score=round(log.confidence * 100, 1) if log.confidence <= 1.0 else float(log.confidence)
        )
        for log in logs
    ]
    return RecognitionHistoryResponse(recognition_history=items)
