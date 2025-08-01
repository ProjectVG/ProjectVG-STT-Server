"""
API Routes
"""
from fastapi import APIRouter, File, UploadFile, Depends
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
router = APIRouter(prefix="/api/v1", tags=["STT"])

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        model_loaded=stt_service.is_model_loaded(),
        service="STT Server"
    )

@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(file: UploadFile = File(...)):
    """Transcribe uploaded audio file"""
    logger.info(get_log_message("API", "REQUEST_RECEIVED", filename=file.filename))
    result = await stt_service.process_audio_file(file)
    logger.info(get_log_message("API", "REQUEST_COMPLETED", filename=file.filename))
    return TranscriptionResponse(**result)

@router.get("/info", response_model=ServiceInfoResponse)
async def get_service_info():
    """Get service information"""
    return ServiceInfoResponse(
        service="STT Server",
        version="1.0.0",
        model=settings.WHISPER_MODEL,
        device=settings.WHISPER_DEVICE,
        supported_formats=list(settings.ALLOWED_EXTENSIONS),
        max_file_size_mb=settings.MAX_FILE_SIZE // (1024*1024),
        features=["transcription", "language_detection", "segment_analysis"]
    ) 