# STT Server

FastAPI와 Faster Whisper를 사용한 음성-텍스트 변환(STT) 서버입니다.

## 🚀 빠른 시작

### 1. 서버 실행
```bash
# Docker 사용 (권장)
docker-compose up -d

# 로컬 실행
python app.py
```

### 2. API 테스트
```bash
# 서버 상태 확인
curl http://localhost:7926/api/v1/health

# 음성 변환
curl -X POST "http://localhost:7926/api/v1/transcribe" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@recording.wav"
```

### 3. 웹 클라이언트
```bash
cd client
python run_web.py
```
브라우저에서 http://localhost:3000 접속

## 📚 주요 기능

- ✅ **음성-텍스트 변환**: Whisper 모델 기반
- ✅ **다국어 지원**: 10개 언어 지원
- ✅ **언어 고정**: 특정 언어로 강제 지정
- ✅ **실시간 처리**: 비동기 처리
- ✅ **REST API**: FastAPI 기반
- ✅ **자동 문서화**: Swagger/ReDoc
- ✅ **Docker 지원**: 컨테이너화
- ✅ **웹 클라이언트**: 테스트용 UI

## 🛠️ 기술 스택

- **Backend**: FastAPI, Uvicorn
- **STT Engine**: Faster Whisper
- **Language**: Python 3.11
- **Container**: Docker & Docker Compose
- **Documentation**: Swagger UI, ReDoc

## 🌍 지원 언어

| 언어 코드 | 언어명 | 언어 코드 | 언어명 |
|-----------|--------|-----------|--------|
| `ko` | 한국어 | `es` | 스페인어 |
| `en` | 영어 | `fr` | 프랑스어 |
| `ja` | 일본어 | `de` | 독일어 |
| `zh` | 중국어 | `it` | 이탈리아어 |
| | | `pt` | 포르투갈어 |
| | | `ru` | 러시아어 |

## 📁 지원 파일 형식

- **WAV** (`.wav`)
- **MP3** (`.mp3`)
- **M4A** (`.m4a`)
- **FLAC** (`.flac`)
- **OGG** (`.ogg`)

## 📖 문서

### 📚 API 문서
- **실시간 문서**: 
  - [Swagger UI](http://localhost:7926/docs) - 대화형 API 문서
- [ReDoc](http://localhost:7926/redoc) - 대안 문서 뷰어
- [OpenAPI 스펙](http://localhost:7926/openapi.json) - OpenAPI 3.0 스펙

## 🔧 설치 방법

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

## 🐳 Docker 명령어

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

## 🔌 포트 설정

- **STT 서버**: http://localhost:7926 (설정 파일에서 변경 가능)
- **웹 클라이언트**: http://localhost:3000

## 🌐 API 엔드포인트

- `GET /api/v1/health` - 서버 상태 확인
- `POST /api/v1/transcribe` - 음성 변환
- `GET /api/v1/info` - 서비스 정보

## ⚙️ 환경 변수

| 변수명 | 기본값 | 설명 |
|--------|--------|------|
| `HOST` | `0.0.0.0` | 서버 호스트 |
| `PORT` | `7926` | 서버 포트 |
| `WHISPER_MODEL` | `base` | Whisper 모델 크기 |
| `WHISPER_DEVICE` | `cpu` | 처리 디바이스 |
| `WHISPER_LANGUAGE` | `None` | 기본 언어 (미설정 시 자동 감지) |
| `MAX_FILE_SIZE` | `16777216` | 최대 파일 크기 (16MB) |

## 📝 사용 예시

### Python (requests)
```python
import requests

# 음성 변환 (한국어 고정)
with open("recording.wav", "rb") as f:
    files = {"file": f}
    response = requests.post(
        "http://localhost:7926/api/v1/transcribe?language=ko", 
        files=files
    )
    print(response.json())
```

### cURL
```bash
# 한국어로 고정하여 변환
curl -X POST "http://localhost:7926/api/v1/transcribe?language=ko" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@recording.wav"
```

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 문의 및 지원

- **이슈 리포트**: GitHub Issues
- **문서 개선**: Pull Request
- **기술 문의**: 프로젝트 팀 