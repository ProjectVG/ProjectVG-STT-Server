"""
API Routes
"""
from typing import Optional
from fastapi import APIRouter, File, UploadFile, Depends, Query, HTTPException
from fastapi.responses import JSONResponse
from src.services.stt_service import stt_service
from src.core.config import settings
from src.utils.logger import get_logger
from src.utils.log_messages import get_log_message
from src.models.responses import (
    TranscriptionResponse, HealthResponse, ServiceInfoResponse
)

logger = get_logger(__name__)

# Create router
router = APIRouter(prefix="/api/v1/stt", tags=["STT"])

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    서버 상태 확인
    
    서버의 전반적인 상태와 모델 로딩 상태를 확인합니다.
    
    Returns:
        HealthResponse: 서버 상태 정보
            - status: 서버 상태 ("healthy" 또는 "unhealthy")
            - model_loaded: Whisper 모델 로딩 상태
            - service: 서비스 이름
            - timestamp: 응답 시간
            - uptime: 서버 가동 시간 (초)
    
    Example:
        ```json
        {
            "status": "healthy",
            "model_loaded": true,
            "service": "STT Server",
            "timestamp": "2024-01-01T12:00:00",
            "uptime": 3600.5
        }
        ```
    """
    return HealthResponse(
        status="healthy",
        model_loaded=stt_service.is_model_loaded(),
        service="STT Server"
    )

@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(
    file: UploadFile = File(..., description="음성 파일 (WAV, MP3, M4A, FLAC, OGG)"),
    language: Optional[str] = Query(
        None, 
        description="언어 코드 (예: ko, en, ja, zh 등). 미지정 시 자동 감지",
        example="ko"
    )
):
    """
    음성 파일을 텍스트로 변환
    
    업로드된 음성 파일을 Whisper 모델을 사용하여 텍스트로 변환합니다.
    
    Args:
        file: 변환할 음성 파일
        language: 언어 코드 (선택사항)
    
    Returns:
        TranscriptionResponse: 변환 결과
            - text: 변환된 텍스트
            - language: 감지된 언어
            - language_probability: 언어 감지 확률
            - segments_count: 세그먼트 개수
            - processing_time: 처리 시간 (초)
            - file_info: 파일 정보
    
    Raises:
        400: 파일 형식이 지원되지 않거나 파일이 너무 큼
        422: 파일 업로드 실패
        500: 모델 로딩 실패 또는 변환 오류
    
    Example:
        ```json
        {
            "text": "안녕하세요. 오늘 날씨가 좋네요.",
            "language": "ko",
            "language_probability": 0.95,
            "segments_count": 1,
            "processing_time": 2.5,
            "file_info": {
                "filename": "recording.wav",
                "content_type": "audio/wav",
                "size": 1024000
            }
        }
        ```
    """
    logger.info(get_log_message("API", "REQUEST_RECEIVED", filename=file.filename))
    result = await stt_service.process_audio_file(file, language)
    logger.info(get_log_message("API", "REQUEST_COMPLETED", filename=file.filename))
    logger.info(f"API 응답 결과 - 텍스트: '{result.get('text', 'N/A')}', 언어: '{result.get('language', 'N/A')}'")
    return TranscriptionResponse(**result)

@router.get("/info", response_model=ServiceInfoResponse)
async def get_service_info():
    """
    서비스 정보 조회
    
    STT 서버의 설정 정보와 지원 기능을 조회합니다.
    
    Returns:
        ServiceInfoResponse: 서비스 정보
            - service: 서비스 이름
            - version: 서비스 버전
            - model: 사용 중인 Whisper 모델
            - device: 사용 중인 디바이스 (CPU/GPU)
            - supported_formats: 지원하는 파일 형식
            - max_file_size_mb: 최대 파일 크기 (MB)
            - features: 지원하는 기능 목록
    
    Example:
        ```json
        {
            "service": "STT Server",
            "version": "1.0.0",
            "model": "base",
            "device": "cpu",
            "supported_formats": [".wav", ".mp3", ".m4a", ".flac", ".ogg"],
            "max_file_size_mb": 16,
            "features": ["transcription", "language_detection", "segment_analysis"]
        }
        ```
    """
    return ServiceInfoResponse(
        service="STT Server",
        version="1.0.0",
        model=settings.WHISPER_MODEL,
        device=settings.WHISPER_DEVICE,
        supported_formats=list(settings.ALLOWED_EXTENSIONS),
        max_file_size_mb=settings.MAX_FILE_SIZE // (1024*1024),
        features=["transcription", "language_detection", "segment_analysis"]
    ) 