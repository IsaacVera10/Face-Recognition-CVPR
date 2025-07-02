from pydantic import BaseModel
from typing import List

class FaceRecognitionResponse(BaseModel):
    name: str
    bbox: List[int]  # [left, top, right, bottom]