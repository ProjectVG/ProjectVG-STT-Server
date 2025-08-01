import requests
import json
import os
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import webbrowser
import threading

class STTWebClient:
    def __init__(self, server_url="http://localhost:7920"):
        self.server_url = server_url
        self.server = None
        self.port = 3000
    
    def start_web_server(self):
        class STTRequestHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    
                    html = self.get_html()
                    self.wfile.write(html.encode())
                else:
                    self.send_response(404)
                    self.end_headers()
            
            def do_POST(self):
                if self.path == '/transcribe':
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    
                    try:
                        data = urllib.parse.parse_qs(post_data.decode())
                        file_path = data.get('file_path', [''])[0]
                        
                        if file_path and os.path.exists(file_path):
                            result = self.transcribe_file(file_path)
                            response = json.dumps(result, ensure_ascii=False)
                        else:
                            response = json.dumps({"error": "파일이 존재하지 않습니다."}, ensure_ascii=False)
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(response.encode())
                        
                    except Exception as e:
                        self.send_response(500)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        error_response = json.dumps({"error": str(e)}, ensure_ascii=False)
                        self.wfile.write(error_response.encode())
                else:
                    self.send_response(404)
                    self.end_headers()
            
            def transcribe_file(self, file_path):
                try:
                    with open(file_path, 'rb') as audio_file:
                        files = {'file': audio_file}
                        response = requests.post(
                            f"{self.server_url}/transcribe",
                            files=files
                        )
                        
                        if response.status_code == 200:
                            return response.json()
                        else:
                            return {"error": f"서버 오류: {response.status_code}"}
                            
                except Exception as e:
                    return {"error": f"파일 처리 오류: {e}"}
            
            def get_html(self):
                return '''
<!DOCTYPE html>
<html>
<head>
    <title>STT 테스트 클라이언트</title>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        .section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
        .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
        .status.success { background-color: #d4edda; color: #155724; }
        .status.error { background-color: #f8d7da; color: #721c24; }
        input[type="file"], input[type="text"] { margin: 10px 0; padding: 5px; }
        button { padding: 10px 20px; margin: 5px; background-color: #007bff; color: white; border: none; border-radius: 3px; cursor: pointer; }
        button:hover { background-color: #0056b3; }
        #result { margin-top: 20px; padding: 15px; background-color: #f8f9fa; border-radius: 5px; white-space: pre-wrap; }
    </style>
</head>
<body>
    <div class="container">
        <h1>STT 테스트 클라이언트</h1>
        
        <div class="section">
            <h3>서버 상태</h3>
            <div id="serverStatus" class="status">확인 중...</div>
            <button onclick="checkServer()">서버 연결 확인</button>
        </div>
        
        <div class="section">
            <h3>음성 파일 업로드</h3>
            <input type="file" id="audioFile" accept=".wav,.mp3,.m4a,.flac,.ogg">
            <button onclick="transcribeFile()">음성 변환</button>
        </div>
        
        <div class="section">
            <h3>파일 경로 입력</h3>
            <input type="text" id="filePath" placeholder="음성 파일 경로를 입력하세요" style="width: 100%;">
            <button onclick="transcribeByPath()">경로로 변환</button>
        </div>
        
        <div class="section">
            <h3>변환 결과</h3>
            <div id="result">결과가 여기에 표시됩니다.</div>
        </div>
    </div>
    
    <script>
        function checkServer() {
            const statusDiv = document.getElementById('serverStatus');
            statusDiv.textContent = '확인 중...';
            statusDiv.className = 'status';
            
            fetch('http://localhost:7920/health')
                .then(response => {
                    if (response.ok) {
                        statusDiv.textContent = '서버 연결됨 ✅';
                        statusDiv.className = 'status success';
                    } else {
                        statusDiv.textContent = '서버 연결 실패 ❌';
                        statusDiv.className = 'status error';
                    }
                })
                .catch(error => {
                    statusDiv.textContent = '서버 연결 실패 ❌';
                    statusDiv.className = 'status error';
                });
        }
        
        function transcribeFile() {
            const fileInput = document.getElementById('audioFile');
            const file = fileInput.files[0];
            
            if (!file) {
                alert('파일을 선택하세요.');
                return;
            }
            
            const formData = new FormData();
            formData.append('file', file);
            
            document.getElementById('result').textContent = '변환 중...';
            
            fetch('http://localhost:7920/api/v1/transcribe', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    document.getElementById('result').textContent = '오류: ' + data.error;
                } else {
                    document.getElementById('result').textContent = 
                        '변환 결과:\\n' +
                        '텍스트: ' + (data.text || 'N/A') + '\\n' +
                        '언어: ' + (data.language || 'N/A');
                }
            })
            .catch(error => {
                document.getElementById('result').textContent = '오류: ' + error.message;
            });
        }
        
        function transcribeByPath() {
            const filePath = document.getElementById('filePath').value;
            
            if (!filePath) {
                alert('파일 경로를 입력하세요.');
                return;
            }
            
            document.getElementById('result').textContent = '변환 중...';
            
            const formData = new FormData();
            formData.append('file_path', filePath);
            
            fetch('/transcribe', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    document.getElementById('result').textContent = '오류: ' + data.error;
                } else {
                    document.getElementById('result').textContent = 
                        '변환 결과:\\n' +
                        '텍스트: ' + (data.text || 'N/A') + '\\n' +
                        '언어: ' + (data.language || 'N/A');
                }
            })
            .catch(error => {
                document.getElementById('result').textContent = '오류: ' + error.message;
            });
        }
        
        // 페이지 로드 시 서버 상태 확인
        window.onload = function() {
            checkServer();
        };
    </script>
</body>
</html>
                '''
        
        self.server = HTTPServer(('localhost', self.port), STTRequestHandler)
        print(f"웹 클라이언트가 http://localhost:{self.port} 에서 실행 중입니다.")
        print("브라우저에서 위 주소를 열어 클라이언트를 사용하세요.")
        
        # 브라우저 자동 열기
        webbrowser.open(f'http://localhost:{self.port}')
        
        self.server.serve_forever()
    
    def start(self):
        try:
            self.start_web_server()
        except KeyboardInterrupt:
            print("\n웹 클라이언트를 종료합니다.")
            if self.server:
                self.server.shutdown()

if __name__ == "__main__":
    client = STTWebClient()
    client.start() 