"""
API Routes
"""
from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from src.services.stt_service import stt_service
from src.core.config import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Create router
router = APIRouter(prefix="/api/v1", tags=["STT"])

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": stt_service.is_model_loaded(),
        "service": "STT Server"
    }

@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """Transcribe uploaded audio file"""
    try:
        logger.info(f"Received transcription request for file: {file.filename}")
        result = await stt_service.process_audio_file(file)
        logger.info("Transcription request completed successfully")
        return result
    except Exception as e:
        logger.error(f"Transcription request failed: {e}")
        raise

@router.get("/info")
async def get_service_info():
    """Get service information"""
    return {
        "service": "STT Server",
        "version": "1.0.0",
        "model": settings.WHISPER_MODEL,
        "device": settings.WHISPER_DEVICE,
        "supported_formats": list(settings.ALLOWED_EXTENSIONS),
        "max_file_size_mb": settings.MAX_FILE_SIZE // (1024*1024)
    } 