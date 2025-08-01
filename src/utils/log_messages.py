"""
Log Messages
"""
from typing import Dict, Any

# API 관련 로그 메시지
API_LOGS = {
    "REQUEST_RECEIVED": "요청 수신: {filename}",
    "REQUEST_COMPLETED": "요청 완료: {filename}",
    "REQUEST_FAILED": "요청 실패: {filename} - {error}",
    "HEALTH_CHECK": "헬스체크 요청",
    "INFO_REQUEST": "서비스 정보 요청",
}

# 서비스 관련 로그 메시지
SERVICE_LOGS = {
    "MODEL_LOADING": "모델 로딩 중: {model}",
    "MODEL_LOADED": "모델 로딩 완료",
    "MODEL_LOAD_FAILED": "모델 로딩 실패: {error}",
    "FILE_SAVED": "파일 저장 완료: {filepath}",
    "FILE_SAVE_FAILED": "파일 저장 실패: {error}",
    "TRANSCRIPTION_STARTED": "음성 변환 시작: {filepath}",
    "TRANSCRIPTION_COMPLETED": "음성 변환 완료: {language}",
    "TRANSCRIPTION_FAILED": "음성 변환 실패: {error}",
    "FILE_CLEANED": "파일 정리 완료: {filepath}",
    "FILE_CLEANUP_FAILED": "파일 정리 실패: {filepath} - {error}",
}

# 시스템 관련 로그 메시지
SYSTEM_LOGS = {
    "APP_CREATED": "FastAPI 애플리케이션 생성 완료",
    "EXCEPTION_HANDLERS_REGISTERED": "예외 핸들러 등록 완료",
    "SERVER_STARTED": "STT 서버 시작",
    "SERVER_START_FAILED": "STT 서버 시작 실패: {error}",
}

# 예외 관련 로그 메시지
EXCEPTION_LOGS = {
    "STT_EXCEPTION": "STT 예외 발생: {message} (상태: {status_code})",
    "HTTP_EXCEPTION": "HTTP 예외 발생: {detail} (상태: {status_code})",
    "VALIDATION_EXCEPTION": "검증 예외 발생: {error}",
    "GENERAL_EXCEPTION": "일반 예외 발생: {error}",
}

def get_log_message(category: str, key: str, **kwargs) -> str:
    """로그 메시지를 가져오는 함수"""
    log_dicts = {
        "API": API_LOGS,
        "SERVICE": SERVICE_LOGS,
        "SYSTEM": SYSTEM_LOGS,
        "EXCEPTION": EXCEPTION_LOGS,
    }
    
    message = log_dicts.get(category, {}).get(key, "로그 메시지가 정의되지 않았습니다.")
    
    # 키워드 인자로 메시지 포맷팅
    if kwargs:
        try:
            message = message.format(**kwargs)
        except KeyError:
            pass
    
    return message 