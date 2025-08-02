"""
STT Service
"""
import os
import shutil
import time
from typing import Dict, Any, Optional
from fastapi import UploadFile
from faster_whisper import WhisperModel
from src.core.config import settings
from src.utils.logger import get_logger
from src.utils.exceptions import (
    ModelNotLoadedException, FileValidationException, 
    TranscriptionException, FileProcessingException
)
from src.utils.error_messages import get_error_message
from src.utils.log_messages import get_log_message

logger = get_logger(__name__)

class STTService:
    """Speech-to-Text Service"""
    
    def __init__(self):
        self.model: Optional[WhisperModel] = None
        self._is_loaded = False
    
    def load_model(self) -> None:
        """Load FastWhisper model"""
        try:
            logger.info(get_log_message("SERVICE", "MODEL_LOADING", model=settings.WHISPER_MODEL))
            self.model = WhisperModel(
                model_size_or_path=settings.WHISPER_MODEL,
                device=settings.WHISPER_DEVICE,
                compute_type=settings.WHISPER_COMPUTE_TYPE
            )
            self._is_loaded = True
            logger.info(get_log_message("SERVICE", "MODEL_LOADED"))
        except ImportError:
            logger.error(get_log_message("SERVICE", "MODEL_LOAD_FAILED", error="faster-whisper 패키지 미설치"))
            raise ModelNotLoadedException(get_error_message("MODEL", "MODEL_PACKAGE_MISSING"))
        except Exception as e:
            logger.error(get_log_message("SERVICE", "MODEL_LOAD_FAILED", error=str(e)))
            raise ModelNotLoadedException(get_error_message("MODEL", "MODEL_LOAD_FAILED"))
    
    def is_model_loaded(self) -> bool:
        """Check if model is loaded"""
        return self._is_loaded and self.model is not None
    
    def validate_file(self, file: UploadFile) -> None:
        """Validate uploaded file"""
        if not file:
            raise FileValidationException(get_error_message("FILE", "FILE_NOT_FOUND"))
        
        if file.filename == "":
            raise FileValidationException(get_error_message("FILE", "FILE_NOT_SELECTED"))
        
        # Check file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in settings.ALLOWED_EXTENSIONS:
            supported_formats = ', '.join(settings.ALLOWED_EXTENSIONS)
            raise FileValidationException(
                get_error_message("FILE", "INVALID_FILE_TYPE", formats=supported_formats)
            )
        
        # Check file size (if available)
        if hasattr(file, 'size') and file.size and file.size > settings.MAX_FILE_SIZE:
            max_size_mb = settings.MAX_FILE_SIZE // (1024*1024)
            raise FileValidationException(
                get_error_message("FILE", "FILE_TOO_LARGE", max_size=max_size_mb)
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
            
            logger.info(get_log_message("SERVICE", "FILE_SAVED", filepath=file_path))
            return file_path
            
        except Exception as e:
            logger.error(get_log_message("SERVICE", "FILE_SAVE_FAILED", error=str(e)))
            raise FileProcessingException(get_error_message("FILE", "FILE_SAVE_FAILED"))
    
    def transcribe_audio(self, audio_path: str, language: Optional[str] = None) -> Dict[str, Any]:
        """Transcribe audio file"""
        if not self.is_model_loaded():
            raise ModelNotLoadedException()
        
        try:
            logger.info(get_log_message("SERVICE", "TRANSCRIPTION_STARTED", filepath=audio_path))
            
            # 언어 설정 (설정 파일의 기본값 또는 파라미터로 전달된 값)
            target_language = language or settings.WHISPER_LANGUAGE
            
            if target_language:
                logger.info(get_log_message("SERVICE", "LANGUAGE_SET", language=target_language))
                segments, info = self.model.transcribe(audio_path, language=target_language)
            else:
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
            
            logger.info(get_log_message("SERVICE", "TRANSCRIPTION_COMPLETED", language=info.language))
            return result
            
        except Exception as e:
            logger.error(get_log_message("SERVICE", "TRANSCRIPTION_FAILED", error=str(e)))
            raise TranscriptionException(get_error_message("MODEL", "TRANSCRIPTION_FAILED"))
    
    def cleanup_file(self, file_path: str) -> None:
        """Clean up temporary file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(get_log_message("SERVICE", "FILE_CLEANED", filepath=file_path))
        except Exception as e:
            logger.warning(get_log_message("SERVICE", "FILE_CLEANUP_FAILED", filepath=file_path, error=str(e)))
            # 파일 정리 실패는 경고만 하고 예외를 발생시키지 않음
    
    async def process_audio_file(self, file: UploadFile, language: Optional[str] = None) -> Dict[str, Any]:
        """Process uploaded audio file"""
        start_time = time.time()
        
        # Validate file
        self.validate_file(file)
        
        # Save file
        file_path = self.save_uploaded_file(file)
        
        try:
            # Transcribe audio
            result = self.transcribe_audio(file_path, language)
            
            # Add processing time
            processing_time = time.time() - start_time
            result["processing_time"] = round(processing_time, 3)
            
            # Add file info
            result["file_info"] = {
                "filename": file.filename,
                "content_type": file.content_type,
                "size": getattr(file, 'size', None)
            }
            
            return result
        finally:
            # Cleanup file
            self.cleanup_file(file_path)

# Global STT service instance
stt_service = STTService() 