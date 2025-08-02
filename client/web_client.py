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
                """HTML 템플릿 파일을 읽어서 반환"""
                template_path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
                with open(template_path, 'r', encoding='utf-8') as f:
                    return f.read()
        
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