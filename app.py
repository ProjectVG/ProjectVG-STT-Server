from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import shutil
from dotenv import load_dotenv
from config import Config
from typing import Dict, Any

load_dotenv()

app = FastAPI(title="STT Server", version="1.0.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class STTServer:
    def __init__(self):
        self.model = None
    
    def load_model(self):
        try:
            from faster_whisper import WhisperModel
            self.model = WhisperModel(
                model_size_or_path="base",
                device="cpu",
                compute_type="float32"
            )
            print("FastWhisper 모델이 로드되었습니다.")
        except ImportError:
            print("faster-whisper 패키지가 설치되지 않았습니다.")
    
    def transcribe_audio(self, audio_path: str) -> Dict[str, Any]:
        if not self.model:
            return {"error": "모델이 로드되지 않았습니다."}
        
        try:
            segments, info = self.model.transcribe(audio_path)
            text = " ".join([segment.text for segment in segments])
            return {"text": text, "language": info.language}
        except Exception as e:
            return {"error": str(e)}

stt_server = STTServer()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="파일이 없습니다.")
    
    if file.filename == "":
        raise HTTPException(status_code=400, detail="파일이 선택되지 않았습니다.")
    
    # 파일 확장자 검증
    allowed_extensions = {'.wav', '.mp3', '.m4a', '.flac', '.ogg'}
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="지원하지 않는 파일 형식입니다.")
    
    try:
        # 업로드 폴더 생성
        upload_folder = Config.UPLOAD_FOLDER
        os.makedirs(upload_folder, exist_ok=True)
        
        # 파일 저장
        file_path = os.path.join(upload_folder, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 음성 변환
        result = stt_server.transcribe_audio(file_path)
        
        # 임시 파일 삭제
        os.remove(file_path)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 처리 오류: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    stt_server.load_model()
    uvicorn.run(app, host="0.0.0.0", port=7920) 