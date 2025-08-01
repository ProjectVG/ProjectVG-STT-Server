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
        try:
            logger.info(f"Legacy transcribe request for file: {file.filename}")
            result = await stt_service.process_audio_file(file)
            logger.info("Legacy transcribe request completed successfully")
            return result
        except Exception as e:
            logger.error(f"Legacy transcribe request failed: {e}")
            raise
    
    # Exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        logger.error(f"Global exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )
    
    logger.info("FastAPI application created successfully")
    return app

# Create app instance
app = create_app() 