"""
STT Service
"""
import os
import shutil
from typing import Dict, Any, Optional
from fastapi import UploadFile, HTTPException
from faster_whisper import WhisperModel
from src.core.config import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

class STTService:
    """Speech-to-Text Service"""
    
    def __init__(self):
        self.model: Optional[WhisperModel] = None
        self._is_loaded = False
    
    def load_model(self) -> None:
        """Load FastWhisper model"""
        try:
            logger.info(f"Loading FastWhisper model: {settings.WHISPER_MODEL}")
            self.model = WhisperModel(
                model_size_or_path=settings.WHISPER_MODEL,
                device=settings.WHISPER_DEVICE,
                compute_type=settings.WHISPER_COMPUTE_TYPE
            )
            self._is_loaded = True
            logger.info("FastWhisper model loaded successfully")
        except ImportError:
            logger.error("faster-whisper package is not installed")
            raise RuntimeError("faster-whisper package is not installed")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise RuntimeError(f"Failed to load model: {e}")
    
    def is_model_loaded(self) -> bool:
        """Check if model is loaded"""
        return self._is_loaded and self.model is not None
    
    def validate_file(self, file: UploadFile) -> None:
        """Validate uploaded file"""
        if not file:
            raise HTTPException(status_code=400, detail="파일이 없습니다.")
        
        if file.filename == "":
            raise HTTPException(status_code=400, detail="파일이 선택되지 않았습니다.")
        
        # Check file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400, 
                detail=f"지원하지 않는 파일 형식입니다. 지원 형식: {', '.join(settings.ALLOWED_EXTENSIONS)}"
            )
        
        # Check file size (if available)
        if hasattr(file, 'size') and file.size and file.size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"파일 크기가 너무 큽니다. 최대 크기: {settings.MAX_FILE_SIZE // (1024*1024)}MB"
            )
    
    def save_uploaded_file(self, file: UploadFile) -> str:
        """Save uploaded file to temporary location"""
        try:
            # Create upload directory
            os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)
            
            # Generate unique filename
            file_path = os.path.join(settings.UPLOAD_FOLDER, file.filename)
            
            # Save file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            logger.info(f"File saved: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Failed to save file: {e}")
            raise HTTPException(status_code=500, detail=f"파일 저장 실패: {str(e)}")
    
    def transcribe_audio(self, audio_path: str) -> Dict[str, Any]:
        """Transcribe audio file"""
        if not self.is_model_loaded():
            raise HTTPException(status_code=500, detail="모델이 로드되지 않았습니다.")
        
        try:
            logger.info(f"Transcribing audio: {audio_path}")
            segments, info = self.model.transcribe(audio_path)
            
            # Convert generator to list and combine all segments
            segments_list = list(segments)
            text = " ".join([segment.text for segment in segments_list])
            
            result = {
                "text": text,
                "language": info.language,
                "language_probability": info.language_probability,
                "segments_count": len(segments_list)
            }
            
            logger.info(f"Transcription completed. Language: {info.language}")
            return result
            
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise HTTPException(status_code=500, detail=f"음성 변환 실패: {str(e)}")
    
    def cleanup_file(self, file_path: str) -> None:
        """Clean up temporary file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"File cleaned up: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to cleanup file {file_path}: {e}")
    
    async def process_audio_file(self, file: UploadFile) -> Dict[str, Any]:
        """Process uploaded audio file"""
        # Validate file
        self.validate_file(file)
        
        # Save file
        file_path = self.save_uploaded_file(file)
        
        try:
            # Transcribe audio
            result = self.transcribe_audio(file_path)
            return result
        finally:
            # Cleanup file
            self.cleanup_file(file_path)

# Global STT service instance
stt_service = STTService() 