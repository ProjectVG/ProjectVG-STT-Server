"""
FastAPI Application Factory
"""
from fastapi import FastAPI, File, UploadFile
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
        title="STT Server",
        description="FastAPI-based Speech-to-Text Server using Faster Whisper",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
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
    @app.get("/")
    async def root():
        return {
            "message": "STT Server is running",
            "docs": "/docs",
            "health": "/api/v1/health"
        }
    
    # Health check endpoint (legacy)
    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}
    
    # Legacy transcribe endpoint for backward compatibility
    @app.post("/transcribe")
    async def legacy_transcribe(file: UploadFile = File(...)):
        """Legacy transcribe endpoint for backward compatibility"""
        logger.info(get_log_message("API", "REQUEST_RECEIVED", filename=file.filename))
        result = await stt_service.process_audio_file(file)
        logger.info(get_log_message("API", "REQUEST_COMPLETED", filename=file.filename))
        return result
    
    # Register exception handlers
    register_exception_handlers(app)
    
    logger.info(get_log_message("SYSTEM", "APP_CREATED"))
    return app

# Create app instance
app = create_app() 