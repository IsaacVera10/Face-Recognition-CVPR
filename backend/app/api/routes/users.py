from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.models.user import User
from app.schemas import UserPreview
from app.core.database import get_db

router = APIRouter()

@router.get("/users/by-page", response_model=List[UserPreview])
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
        UserPreview(
            id=user.id,
            name=user.name,
            image_url=user.image_url,
            last_seen=user.last_seen.isoformat() if user.last_seen else None,
            recognition_count=user.recognition_count or 0,
            tags=[tag.strip() for tag in user.tags.split(",")] if user.tags else [],
        )
        for user in users
    ]
    return response