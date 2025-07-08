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
        orm_mode = True