"""
Exception Handlers
"""
from typing import Dict, Any
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from src.utils.exceptions import STTException
from src.utils.error_messages import get_error_message
from src.utils.logger import get_logger
from src.utils.log_messages import get_log_message
from src.models.responses import ErrorResponse

logger = get_logger(__name__)

async def stt_exception_handler(request: Request, exc: STTException) -> JSONResponse:
    """STT 커스텀 예외 핸들러"""
    logger.error(get_log_message("EXCEPTION", "STT_EXCEPTION", message=exc.message, status_code=exc.status_code))
    
    error_response = ErrorResponse(
        error=exc.message,
        status_code=exc.status_code,
        type=exc.__class__.__name__,
        details=exc.details
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump()
    )

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """HTTP 예외 핸들러"""
    logger.error(get_log_message("EXCEPTION", "HTTP_EXCEPTION", detail=exc.detail, status_code=exc.status_code))
    
    error_response = ErrorResponse(
        error=exc.detail,
        status_code=exc.status_code,
        type="HTTPException"
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump()
    )

async def validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """검증 예외 핸들러"""
    logger.error(get_log_message("EXCEPTION", "VALIDATION_EXCEPTION", error=str(exc)))
    
    error_response = ErrorResponse(
        error=get_error_message("API", "VALIDATION_ERROR"),
        status_code=422,
        type="ValidationException",
        details={"validation_error": str(exc)}
    )
    
    return JSONResponse(
        status_code=422,
        content=error_response.model_dump()
    )

async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """일반 예외 핸들러"""
    logger.error(get_log_message("EXCEPTION", "GENERAL_EXCEPTION", error=str(exc)), exc_info=True)
    
    error_response = ErrorResponse(
        error=get_error_message("SERVER", "INTERNAL_ERROR"),
        status_code=500,
        type="InternalServerError"
    )
    
    return JSONResponse(
        status_code=500,
        content=error_response.model_dump()
    )

def register_exception_handlers(app):
    """예외 핸들러들을 앱에 등록"""
    from src.utils.exceptions import (
        STTException, ModelNotLoadedException, FileValidationException,
        TranscriptionException, FileProcessingException, ConfigurationException,
        ServiceUnavailableException
    )
    
    # 커스텀 예외 핸들러들
    app.add_exception_handler(STTException, stt_exception_handler)
    app.add_exception_handler(ModelNotLoadedException, stt_exception_handler)
    app.add_exception_handler(FileValidationException, stt_exception_handler)
    app.add_exception_handler(TranscriptionException, stt_exception_handler)
    app.add_exception_handler(FileProcessingException, stt_exception_handler)
    app.add_exception_handler(ConfigurationException, stt_exception_handler)
    app.add_exception_handler(ServiceUnavailableException, stt_exception_handler)
    
    # HTTP 예외 핸들러
    app.add_exception_handler(HTTPException, http_exception_handler)
    
    # 일반 예외 핸들러
    app.add_exception_handler(Exception, general_exception_handler)
    
    logger.info(get_log_message("SYSTEM", "EXCEPTION_HANDLERS_REGISTERED")) 