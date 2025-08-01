"""
Request DTOs
"""
from typing import Optional
from pydantic import BaseModel, Field

class TranscribeRequest(BaseModel):
    filename: str = Field(...)
    file_size: Optional[int] = Field(None)
    content_type: Optional[str] = Field(None) 