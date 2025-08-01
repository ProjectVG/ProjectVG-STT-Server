"""
Logging Utilities
"""
import logging
import sys
from typing import Optional
from src.core.config import settings

def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """Get configured logger"""
    logger = logging.getLogger(name)
    
    if not logger.handlers:  # Avoid adding handlers multiple times
        logger.setLevel(level or logging.INFO)
        
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(console_handler)
    
    return logger 