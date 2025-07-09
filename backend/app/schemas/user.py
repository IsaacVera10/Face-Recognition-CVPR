from pydantic import BaseModel
from typing import List, Optional

class UserPreview(BaseModel):
    id: int                # internal DB id (puedes usar user_id si prefieres)
    name: str
    image_url: Optional[str] = None
    last_seen: Optional[str] = None   # formato ISO o texto "hace X días"
    recognition_count: int
    tags: List[str]

    class Config:
        from_attributes = True

class UserDetail(BaseModel):
    id: int
    user_id: str
    name: str
    image_url: Optional[str]
    age: Optional[int]
    gender: Optional[str]
    date_of_birth: Optional[str]  # O datetime.date si prefieres
    recognition_count: int
    last_seen: Optional[str]
    last_location: Optional[str]
    tags: List[str]

    class Config:
        from_attributes = True  # Para Pydantic v2