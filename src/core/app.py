"""
FastAPI Application Factory
"""
from fastapi import FastAPI, File, UploadFile, Query
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.core.config import settings
from src.api.routes import router
from src.services.stt_service import stt_service
from src.utils.logger import get_logger
from src.utils.exception_handlers import register_exception_handlers
from src.utils.log_messages import get_log_message

logger = get_logger(__name__)

def create_app() -> FastAPI:
    """Create FastAPI application"""
    
    # Create FastAPI app
    app = FastAPI(
        title="STT Server API",
        description="""
        FastAPI 기반 음성-텍스트 변환(STT) 서버입니다.
        
        ## 주요 기능
        
        * **음성 변환**: 음성 파일을 텍스트로 변환
        * **언어 감지**: 자동 언어 감지 및 고정 언어 설정
        * **다양한 형식 지원**: WAV, MP3, M4A, FLAC, OGG
        * **실시간 처리**: 비동기 처리로 빠른 응답
        
        ## 사용 방법
        
        1. **서버 상태 확인**: `GET /api/v1/health`
        2. **음성 변환**: `POST /api/v1/stt/transcribe`
        3. **서비스 정보**: `GET /api/v1/info`
        
        ## 지원 언어
        
        * `ko`: 한국어
        * `en`: 영어
        * `ja`: 일본어
        * `zh`: 중국어
        * `es`: 스페인어
        * `fr`: 프랑스어
        * `de`: 독일어
        * `it`: 이탈리아어
        * `pt`: 포르투갈어
        * `ru`: 러시아어
        
        ## 기술 스택
        
        * **Backend**: FastAPI, Uvicorn
        * **STT Engine**: Faster Whisper
        * **Language**: Python 3.11
        * **Container**: Docker & Docker Compose
        """,
        version="1.0.0",
        contact={
            "name": "STT Server Team",
            "email": "support@stt-server.com",
        },
        license_info={
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT",
        },
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        servers=[
            {
                "url": "http://localhost:7920",
                "description": "개발 서버"
            },
            {
                "url": "https://api.stt-server.com",
                "description": "프로덕션 서버"
            }
        ],
        tags_metadata=[
            {
                "name": "STT",
                "description": "음성-텍스트 변환 관련 API",
                "externalDocs": {
                    "description": "Whisper 모델 정보",
                    "url": "https://github.com/guillaumekln/faster-whisper",
                },
            },
        ]
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_CREDENTIALS,
        allow_methods=settings.CORS_METHODS,
        allow_headers=settings.CORS_HEADERS,
    )
    
    # Include API routes
    app.include_router(router)
    
    # Root endpoint
    @app.get("/", tags=["Root"])
    async def root():
        """
        루트 엔드포인트
        
        서버가 정상적으로 실행 중인지 확인하고 API 문서 링크를 제공합니다.
        """
        return {
            "message": "STT Server is running",
            "version": "1.0.0",
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/api/v1/stt/health",
            "info": "/api/v1/stt/info"
        }
    
    # Health check endpoint (legacy)
    @app.get("/health", tags=["Legacy"])
    async def health_check():
        """
        레거시 헬스 체크 엔드포인트
        
        이전 버전과의 호환성을 위해 제공됩니다.
        새로운 API는 `/api/v1/stt/health`를 사용하세요.
        """
        return {"status": "healthy"}
    
    # Legacy transcribe endpoint for nginx compatibility
    @app.post("/transcribe", tags=["Legacy"])
    async def legacy_transcribe(
        file: UploadFile = File(...),
        language: Optional[str] = Query(None, description="언어 코드")
    ):
        """
        레거시 음성 변환 엔드포인트 (nginx 호환성)
        
        nginx에서 /api/v1/stt/transcribe를 /transcribe로 변환하여 전달하므로
        호환성을 위해 제공됩니다.
        """
        logger.info(get_log_message("API", "REQUEST_RECEIVED", filename=file.filename))
        result = await stt_service.process_audio_file(file, language)
        logger.info(get_log_message("API", "REQUEST_COMPLETED", filename=file.filename))
        logger.info(f"레거시 API 응답 결과 - 텍스트: '{result.get('text', 'N/A')}', 언어: '{result.get('language', 'N/A')}'")
        return result
    
    # Register exception handlers
    register_exception_handlers(app)
    
    logger.info(get_log_message("SYSTEM", "APP_CREATED"))
    return app

# Create app instance
app = create_app() 