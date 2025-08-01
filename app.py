from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from config import Config

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

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
        except ImportError:
            print("faster-whisper 패키지가 설치되지 않았습니다.")
    
    def transcribe_audio(self, audio_path):
        if not self.model:
            return {"error": "모델이 로드되지 않았습니다."}
        
        try:
            segments, info = self.model.transcribe(audio_path)
            text = " ".join([segment.text for segment in segments])
            return {"text": text, "language": info.language}
        except Exception as e:
            return {"error": str(e)}

stt_server = STTServer()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({'error': '파일이 없습니다.'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '파일이 선택되지 않았습니다.'}), 400
    
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        result = stt_server.transcribe_audio(filename)
        return jsonify(result)
    
    return jsonify({'error': '파일 업로드 실패'}), 400

if __name__ == '__main__':
    stt_server.load_model()
    app.run(debug=True, host='0.0.0.0', port=7920) 