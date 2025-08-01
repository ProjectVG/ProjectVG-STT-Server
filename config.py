import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a', 'flac', 'ogg'}
    
    # FastWhisper 설정
    WHISPER_MODEL = os.environ.get('WHISPER_MODEL') or 'base'
    WHISPER_DEVICE = os.environ.get('WHISPER_DEVICE') or 'cpu'
    WHISPER_COMPUTE_TYPE = os.environ.get('WHISPER_COMPUTE_TYPE') or 'float32' 