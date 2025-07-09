from pydantic import BaseModel
from typing import Optional
from typing import List

class RecognitionLog(BaseModel):
    id: int
    user_id: str
    user_name: str
    timestamp: str
    location: str
    confidence: float

    class Config:
        from_attributes = True

from pydantic import BaseModel
from typing import Optional, List

class RecognitionLogListItem(BaseModel):
    name: str
    confidence: float
    timestamp: str
    location: str
    user_id: str
    age: Optional[int]
    gender: Optional[str]
    date_of_birth: Optional[str]
    tags: List[str]
    notes: Optional[str]

    class Config:
        from_attributes = True

class RecognitionHistoryItem(BaseModel):
    datetime: str
    location: str
    score: float

class RecognitionHistoryResponse(BaseModel):
    recognition_history: List[RecognitionHistoryItem]