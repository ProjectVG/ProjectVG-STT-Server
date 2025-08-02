"""
Request DTOs
"""
from typing import Optional
from pydantic import BaseModel, Field

class TranscribeRequest(BaseModel):
    filename: str = Field(...)
    file_size: Optional[int] = Field(None)
    content_type: Optional[str] = Field(None)
    language: Optional[str] = Field(None, description="언어 코드 (예: ko, en, ja, zh 등)") 