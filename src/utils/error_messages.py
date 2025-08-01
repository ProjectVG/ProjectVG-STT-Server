"""
Error Messages
"""
from typing import Dict, Any

# 파일 관련 에러 메시지
FILE_ERRORS = {
    "FILE_NOT_FOUND": "파일이 없습니다.",
    "FILE_NOT_SELECTED": "파일이 선택되지 않았습니다.",
    "INVALID_FILE_TYPE": "지원하지 않는 파일 형식입니다. 지원 형식: {formats}",
    "FILE_TOO_LARGE": "파일 크기가 너무 큽니다. 최대 크기: {max_size}MB",
    "FILE_SAVE_FAILED": "파일 저장에 실패했습니다.",
    "FILE_CLEANUP_FAILED": "파일 정리 중 오류가 발생했습니다.",
    "FILE_PROCESSING_FAILED": "파일 처리 중 오류가 발생했습니다.",
}

# 모델 관련 에러 메시지
MODEL_ERRORS = {
    "MODEL_NOT_LOADED": "모델이 로드되지 않았습니다.",
    "MODEL_LOAD_FAILED": "모델 로드에 실패했습니다.",
    "MODEL_PACKAGE_MISSING": "faster-whisper 패키지가 설치되지 않았습니다.",
    "TRANSCRIPTION_FAILED": "음성 변환에 실패했습니다.",
}

# 서버 관련 에러 메시지
SERVER_ERRORS = {
    "INTERNAL_ERROR": "내부 서버 오류가 발생했습니다.",
    "SERVICE_UNAVAILABLE": "서비스를 사용할 수 없습니다.",
    "CONFIGURATION_ERROR": "설정 오류가 발생했습니다.",
    "VALIDATION_ERROR": "입력 데이터 검증에 실패했습니다.",
}

# API 관련 에러 메시지
API_ERRORS = {
    "INVALID_REQUEST": "잘못된 요청입니다.",
    "METHOD_NOT_ALLOWED": "허용되지 않는 HTTP 메서드입니다.",
    "NOT_FOUND": "요청한 리소스를 찾을 수 없습니다.",
    "RATE_LIMIT_EXCEEDED": "요청 한도를 초과했습니다.",
}

# 성공 메시지
SUCCESS_MESSAGES = {
    "FILE_SAVED": "파일이 성공적으로 저장되었습니다.",
    "FILE_CLEANED": "파일이 성공적으로 정리되었습니다.",
    "TRANSCRIPTION_COMPLETED": "음성 변환이 완료되었습니다.",
    "MODEL_LOADED": "모델이 성공적으로 로드되었습니다.",
}

def get_error_message(category: str, key: str, **kwargs) -> str:
    """에러 메시지를 가져오는 함수"""
    error_dicts = {
        "FILE": FILE_ERRORS,
        "MODEL": MODEL_ERRORS,
        "SERVER": SERVER_ERRORS,
        "API": API_ERRORS,
    }
    
    message = error_dicts.get(category, {}).get(key, "알 수 없는 오류가 발생했습니다.")
    
    # 키워드 인자로 메시지 포맷팅
    if kwargs:
        try:
            message = message.format(**kwargs)
        except KeyError:
            pass
    
    return message

def get_success_message(key: str, **kwargs) -> str:
    """성공 메시지를 가져오는 함수"""
    message = SUCCESS_MESSAGES.get(key, "작업이 성공적으로 완료되었습니다.")
    
    if kwargs:
        try:
            message = message.format(**kwargs)
        except KeyError:
            pass
    
    return message 