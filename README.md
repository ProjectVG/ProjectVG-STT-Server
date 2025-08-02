# FastAPI STT Server

FastAPI와 Faster Whisper를 사용한 음성-텍스트 변환(STT) 서버입니다.

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
- REST API 제공 (FastAPI)
- 자동 API 문서 생성 (/docs)
- 비동기 처리 지원
- **언어 고정 기능**: 특정 언어로 음성 인식 강제 지정

## 언어 설정

### 환경 변수로 설정
`.env` 파일에서 기본 언어를 설정할 수 있습니다:
```bash
WHISPER_LANGUAGE=ko  # 한국어로 고정
```

### API 호출 시 설정
API 호출 시 쿼리 파라미터로 언어를 지정할 수 있습니다:
```bash
POST /api/v1/transcribe?language=ko
```

### 지원 언어
- `ko`: 한국어
- `en`: 영어
- `ja`: 일본어
- `zh`: 중국어
- `es`: 스페인어
- `fr`: 프랑스어
- `de`: 독일어
- `it`: 이탈리아어
- `pt`: 포르투갈어
- `ru`: 러시아어

언어를 지정하지 않으면 자동으로 감지됩니다. 