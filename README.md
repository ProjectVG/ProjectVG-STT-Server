# Faster Whisper STT Server

Faster Whisper를 사용한 음성-텍스트 변환(STT) 서버입니다.

## 설치 방법

### Docker 사용 (권장)

1. Docker와 Docker Compose 설치
2. 프로젝트 클론
3. 서버 실행
```bash
# Windows
docker-run.bat

# Linux/Mac
./docker-run.sh
```

### 로컬 설치

1. 가상환경 생성 및 활성화
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

2. 의존성 설치
```bash
pip install -r requirements.txt
```

3. 서버 실행
```bash
python app.py
```

## Docker 명령어

```bash
# 서버 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 서버 중지
docker-compose down

# 이미지 재빌드
docker-compose build --no-cache
```

## 포트 설정

- **STT 서버**: http://localhost:7920
- **웹 클라이언트**: http://localhost:3000

## 주요 기능

- 음성 파일 업로드 및 텍스트 변환
- 실시간 음성 인식 (향후 구현 예정)
- REST API 제공 