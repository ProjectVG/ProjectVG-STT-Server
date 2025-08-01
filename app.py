#!/usr/bin/env python3
"""
STT Server Application Entry Point
"""
import uvicorn
from src.core.app import app
from src.services.stt_service import stt_service
from src.utils.logger import get_logger

logger = get_logger(__name__)

def main():
    """Main application entry point"""
    try:
        # Load STT model
        logger.info("Starting STT Server...")
        stt_service.load_model()
        logger.info("STT Server started successfully")
        
        # Run server
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=7920,
            log_level="info"
        )
    except Exception as e:
        logger.error(f"Failed to start STT Server: {e}")
        raise

if __name__ == "__main__":
    main() 