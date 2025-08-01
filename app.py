#!/usr/bin/env python3
"""
STT Server Application Entry Point
"""
import uvicorn
from src.core.app import app
from src.services.stt_service import stt_service
from src.utils.logger import get_logger
from src.utils.log_messages import get_log_message

logger = get_logger(__name__)

def main():
    """Main application entry point"""
    try:
        # Load STT model
        logger.info(get_log_message("SYSTEM", "SERVER_STARTED"))
        stt_service.load_model()
        
        # Run server
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=7920,
            log_level="info"
        )
    except Exception as e:
        logger.error(get_log_message("SYSTEM", "SERVER_START_FAILED", error=str(e)))
        raise

if __name__ == "__main__":
    main() 