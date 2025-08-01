"""
Custom Exceptions
"""
from typing import Any, Dict, Optional
from fastapi import HTTPException


class STTException(Exception):
    """Base STT Exception"""
    
    def __init__(self, message: str, status_code: int = 500, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ModelNotLoadedException(STTException):
    """모델이 로드되지 않았을 때 발생하는 예외"""
    
    def __init__(self, message: str = "모델이 로드되지 않았습니다."):
        super().__init__(message, status_code=500)


class FileValidationException(STTException):
    """파일 검증 실패 시 발생하는 예외"""
    
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message, status_code=status_code)


class TranscriptionException(STTException):
    """음성 변환 실패 시 발생하는 예외"""
    
    def __init__(self, message: str = "음성 변환에 실패했습니다."):
        super().__init__(message, status_code=500)


class FileProcessingException(STTException):
    """파일 처리 실패 시 발생하는 예외"""
    
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message, status_code=status_code)


class ConfigurationException(STTException):
    """설정 오류 시 발생하는 예외"""
    
    def __init__(self, message: str = "설정 오류가 발생했습니다."):
        super().__init__(message, status_code=500)


class ServiceUnavailableException(STTException):
    """서비스 사용 불가 시 발생하는 예외"""
    
    def __init__(self, message: str = "서비스를 사용할 수 없습니다."):
        super().__init__(message, status_code=503) 