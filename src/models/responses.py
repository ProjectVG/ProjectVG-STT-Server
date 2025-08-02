"""
Response DTOs
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class TranscriptionSegment(BaseModel):
    start: float = Field(...)
    end: float = Field(...)
    text: str = Field(...)
    confidence: Optional[float] = Field(None)

class TranscriptionResponse(BaseModel):
    text: str = Field(...)
    language: str = Field(...)
    language_probability: float = Field(...)
    segments_count: int = Field(...)
    segments: Optional[List[TranscriptionSegment]] = Field(None)
    processing_time: Optional[float] = Field(None)
    file_info: Optional[Dict[str, Any]] = Field(None)

class HealthResponse(BaseModel):
    status: str = Field(...)
    model_loaded: bool = Field(...)
    service: str = Field(...)
    timestamp: datetime = Field(default_factory=datetime.now)
    uptime: Optional[float] = Field(None)

class ServiceInfoResponse(BaseModel):
    service: str = Field(...)
    version: str = Field(...)
    model: str = Field(...)
    device: str = Field(...)
    supported_formats: List[str] = Field(...)
    max_file_size_mb: int = Field(...)
    features: Optional[List[str]] = Field(None)

class ErrorResponse(BaseModel):
    error: str = Field(...)
    status_code: int = Field(...)
    type: str = Field(...)
    details: Optional[Dict[str, Any]] = Field(None)
    timestamp: datetime = Field(default_factory=datetime.now) 