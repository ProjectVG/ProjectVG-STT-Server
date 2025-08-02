# 배포 가이드

STT Server를 다양한 환경에 배포하는 방법을 설명합니다.

## 배포 옵션

### 1. Docker 배포 (권장)

#### 로컬 Docker 배포
```bash
# 1. 프로젝트 클론
git clone <repository-url>
cd STT-Server

# 2. 환경 변수 설정 (선택사항)
cp env.example .env
# .env 파일 편집

# 3. Docker 컨테이너 실행
docker-compose up -d

# 4. 로그 확인
docker-compose logs -f
```

#### 프로덕션 Docker 배포
```bash
# 1. 환경 변수 설정
export WHISPER_MODEL=large
export WHISPER_DEVICE=cuda
export WHISPER_LANGUAGE=ko

# 2. 프로덕션용 Docker Compose 실행
docker-compose -f docker-compose.prod.yml up -d
```

### 2. 로컬 배포

#### 시스템 요구사항
- Python 3.11+
- FFmpeg
- Git

#### 설치 단계
```bash
# 1. 가상환경 생성
python -m venv venv

# 2. 가상환경 활성화
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 환경 변수 설정
cp env.example .env

# 5. 서버 실행
python app.py
```

### 3. 클라우드 배포

#### AWS EC2 배포
```bash
# 1. EC2 인스턴스 생성 (Ubuntu 20.04 LTS)
# 2. Docker 설치
sudo apt update
sudo apt install docker.io docker-compose

# 3. 프로젝트 클론
git clone <repository-url>
cd STT-Server

# 4. 환경 변수 설정
cp env.example .env

# 5. Docker 실행
sudo docker-compose up -d

# 6. 방화벽 설정
sudo ufw allow 7920
```

#### Google Cloud Run 배포
```bash
# 1. Dockerfile 최적화
# 2. 이미지 빌드
docker build -t gcr.io/PROJECT_ID/stt-server .

# 3. 이미지 푸시
docker push gcr.io/PROJECT_ID/stt-server

# 4. Cloud Run 배포
gcloud run deploy stt-server \
  --image gcr.io/PROJECT_ID/stt-server \
  --platform managed \
  --region asia-northeast1 \
  --allow-unauthenticated
```

## 환경 변수 설정

### 필수 환경 변수
```bash
# 서버 설정
HOST=0.0.0.0
PORT=7920

# Whisper 설정
WHISPER_MODEL=base
WHISPER_DEVICE=cpu
WHISPER_COMPUTE_TYPE=float32
WHISPER_LANGUAGE=ko

# 파일 업로드 설정
MAX_FILE_SIZE=16777216
UPLOAD_FOLDER=uploads
```

### 선택적 환경 변수
```bash
# CORS 설정
CORS_ORIGINS=["*"]
CORS_CREDENTIALS=true

# 보안 설정
SECRET_KEY=your-secret-key-here
DEBUG=false
```

## 성능 최적화

### 1. 모델 크기 선택
- **tiny**: 빠른 처리, 낮은 정확도
- **base**: 균형잡힌 성능 (기본값)
- **small**: 높은 정확도
- **medium**: 매우 높은 정확도
- **large**: 최고 정확도, 느린 처리

### 2. GPU 사용 (권장)
```bash
# CUDA 지원 Docker 이미지 사용
WHISPER_DEVICE=cuda
WHISPER_COMPUTE_TYPE=float16
```

### 3. 메모리 최적화
```bash
# Docker 메모리 제한
docker run --memory=4g stt-server

# Python 메모리 최적화
export PYTHONOPTIMIZE=1
```

## 모니터링

### 1. 로그 확인
```bash
# Docker 로그
docker-compose logs -f

# 애플리케이션 로그
tail -f logs/app.log
```

### 2. 헬스 체크
```bash
# 서버 상태 확인
curl http://localhost:7920/api/v1/health

# 자동화된 헬스 체크
while true; do
  curl -f http://localhost:7920/api/v1/health || echo "Server down"
  sleep 30
done
```

### 3. 성능 모니터링
```bash
# CPU/메모리 사용량
docker stats

# 네트워크 트래픽
netstat -i
```

## 보안 고려사항

### 1. 방화벽 설정
```bash
# 필요한 포트만 열기
sudo ufw allow 7920/tcp
sudo ufw enable
```

### 2. HTTPS 설정
```bash
# Nginx 리버스 프록시 설정
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:7920;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. 인증 추가 (선택사항)
```python
# FastAPI에서 인증 미들웨어 추가
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def verify_token(token: str = Depends(security)):
    # 토큰 검증 로직
    if not is_valid_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return token
```

## 문제 해결

### 1. 일반적인 문제

#### 포트 충돌
```bash
# 포트 사용 확인
netstat -tulpn | grep 7920

# 다른 포트 사용
export PORT=8000
```

#### 메모리 부족
```bash
# Docker 메모리 증가
docker run --memory=8g stt-server

# 스왑 메모리 추가
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### GPU 문제
```bash
# CUDA 설치 확인
nvidia-smi

# CPU 모드로 전환
export WHISPER_DEVICE=cpu
```

### 2. 로그 분석
```bash
# 에러 로그 필터링
docker-compose logs | grep ERROR

# 특정 시간대 로그
docker-compose logs --since="2024-01-01T00:00:00"
```

## 백업 및 복구

### 1. 설정 백업
```bash
# 환경 변수 백업
cp .env .env.backup

# Docker 이미지 백업
docker save stt-server > stt-server.tar
```

### 2. 데이터 복구
```bash
# 환경 변수 복구
cp .env.backup .env

# Docker 이미지 복구
docker load < stt-server.tar
```

## 업데이트

### 1. Docker 업데이트
```bash
# 최신 코드 가져오기
git pull origin main

# 이미지 재빌드
docker-compose build --no-cache

# 컨테이너 재시작
docker-compose down
docker-compose up -d
```

### 2. 롤백
```bash
# 이전 버전으로 롤백
git checkout <previous-commit>
docker-compose build --no-cache
docker-compose up -d
``` 