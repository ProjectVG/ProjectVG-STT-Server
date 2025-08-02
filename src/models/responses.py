"""
Response DTOs
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class TranscriptionSegment(BaseModel):
    """음성 변환 세그먼트 정보"""
    start: float = Field(..., description="시작 시간 (초)")
    end: float = Field(..., description="종료 시간 (초)")
    text: str = Field(..., description="변환된 텍스트")
    confidence: Optional[float] = Field(None, description="신뢰도 (0.0 ~ 1.0)")

class TranscriptionResponse(BaseModel):
    """음성 변환 응답"""
    text: str = Field(..., description="변환된 전체 텍스트")
    language: str = Field(..., description="감지된 언어 코드")
    language_probability: float = Field(..., description="언어 감지 확률 (0.0 ~ 1.0)")
    segments_count: int = Field(..., description="세그먼트 개수")
    segments: Optional[List[TranscriptionSegment]] = Field(None, description="세그먼트 상세 정보")
    processing_time: Optional[float] = Field(None, description="처리 시간 (초)")
    file_info: Optional[Dict[str, Any]] = Field(None, description="업로드된 파일 정보")

class HealthResponse(BaseModel):
    """서버 상태 응답"""
    status: str = Field(..., description="서버 상태 (healthy/unhealthy)")
    model_loaded: bool = Field(..., description="Whisper 모델 로딩 상태")
    service: str = Field(..., description="서비스 이름")
    timestamp: datetime = Field(default_factory=datetime.now, description="응답 시간")
    uptime: Optional[float] = Field(None, description="서버 가동 시간 (초)")

class ServiceInfoResponse(BaseModel):
    """서비스 정보 응답"""
    service: str = Field(..., description="서비스 이름")
    version: str = Field(..., description="서비스 버전")
    model: str = Field(..., description="사용 중인 Whisper 모델")
    device: str = Field(..., description="사용 중인 디바이스 (cpu/gpu)")
    supported_formats: List[str] = Field(..., description="지원하는 파일 형식 목록")
    max_file_size_mb: int = Field(..., description="최대 파일 크기 (MB)")
    features: Optional[List[str]] = Field(None, description="지원하는 기능 목록")

class ErrorResponse(BaseModel):
    """에러 응답"""
    error: str = Field(..., description="에러 메시지")
    status_code: int = Field(..., description="HTTP 상태 코드")
    type: str = Field(..., description="에러 타입")
    details: Optional[Dict[str, Any]] = Field(None, description="상세 에러 정보")
    timestamp: datetime = Field(default_factory=datetime.now, description="에러 발생 시간") 