"""
Configuration Management
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application Settings"""
    
    # Server Settings
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=7920, env="PORT")
    DEBUG: bool = Field(default=True, env="DEBUG")
    
    # File Upload Settings
    UPLOAD_FOLDER: str = Field(default="uploads", env="UPLOAD_FOLDER")
    MAX_FILE_SIZE: int = Field(default=16 * 1024 * 1024, env="MAX_FILE_SIZE")  # 16MB
    ALLOWED_EXTENSIONS: set = Field(default={".wav", ".mp3", ".m4a", ".flac", ".ogg"})
    
    # FastWhisper Settings
    WHISPER_MODEL: str = Field(default="base", env="WHISPER_MODEL")
    WHISPER_DEVICE: str = Field(default="cpu", env="WHISPER_DEVICE")
    WHISPER_COMPUTE_TYPE: str = Field(default="float32", env="WHISPER_COMPUTE_TYPE")
    WHISPER_LANGUAGE: Optional[str] = Field(default=None, env="WHISPER_LANGUAGE")
    
    # CORS Settings
    CORS_ORIGINS: list = Field(default=["*"], env="CORS_ORIGINS")
    CORS_CREDENTIALS: bool = Field(default=True, env="CORS_CREDENTIALS")
    CORS_METHODS: list = Field(default=["*"], env="CORS_METHODS")
    CORS_HEADERS: list = Field(default=["*"], env="CORS_HEADERS")
    
    # Security Settings
    SECRET_KEY: str = Field(default="dev-secret-key", env="SECRET_KEY")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()

def get_settings() -> Settings:
    """Get application settings"""
    return settings 