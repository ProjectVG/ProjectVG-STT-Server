# STT Server API 문서

## 개요

STT Server는 FastAPI와 Faster Whisper를 사용한 음성-텍스트 변환(STT) 서버입니다.

- **Base URL**: `http://localhost:7920`
- **API 버전**: v1
- **문서**: `/docs` (Swagger UI), `/redoc` (ReDoc)

## 인증

현재 버전에서는 인증이 필요하지 않습니다.

## 지원 언어

| 언어 코드 | 언어명 | 언어 코드 | 언어명 |
|-----------|--------|-----------|--------|
| `ko` | 한국어 | `es` | 스페인어 |
| `en` | 영어 | `fr` | 프랑스어 |
| `ja` | 일본어 | `de` | 독일어 |
| `zh` | 중국어 | `it` | 이탈리아어 |
| | | `pt` | 포르투갈어 |
| | | `ru` | 러시아어 |

## 지원 파일 형식

- **WAV** (`.wav`)
- **MP3** (`.mp3`)
- **M4A** (`.m4a`)
- **FLAC** (`.flac`)
- **OGG** (`.ogg`)

## 엔드포인트

### 1. 서버 상태 확인

#### `GET /api/v1/health`

서버의 전반적인 상태와 모델 로딩 상태를 확인합니다.

**응답 예시:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "service": "STT Server",
  "timestamp": "2024-01-01T12:00:00",
  "uptime": 3600.5
}
```

**응답 필드:**
- `status`: 서버 상태 (`healthy` 또는 `unhealthy`)
- `model_loaded`: Whisper 모델 로딩 상태
- `service`: 서비스 이름
- `timestamp`: 응답 시간
- `uptime`: 서버 가동 시간 (초)

---

### 2. 음성 변환

#### `POST /api/v1/transcribe`

음성 파일을 텍스트로 변환합니다.

**요청:**
- **Content-Type**: `multipart/form-data`
- **파일**: 음성 파일 (WAV, MP3, M4A, FLAC, OGG)
- **쿼리 파라미터**:
  - `language` (선택): 언어 코드 (예: `ko`, `en`, `ja`)

**요청 예시:**
```bash
curl -X POST "http://localhost:7920/api/v1/transcribe?language=ko" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@recording.wav"
```

**응답 예시:**
```json
{
  "text": "안녕하세요. 오늘 날씨가 좋네요.",
  "language": "ko",
  "language_probability": 0.95,
  "segments_count": 1,
  "processing_time": 2.5,
  "file_info": {
    "filename": "recording.wav",
    "content_type": "audio/wav",
    "size": 1024000
  }
}
```

**응답 필드:**
- `text`: 변환된 전체 텍스트
- `language`: 감지된 언어 코드
- `language_probability`: 언어 감지 확률 (0.0 ~ 1.0)
- `segments_count`: 세그먼트 개수
- `processing_time`: 처리 시간 (초)
- `file_info`: 업로드된 파일 정보
  - `filename`: 파일명
  - `content_type`: 파일 타입
  - `size`: 파일 크기 (바이트)

**에러 응답:**
```json
{
  "error": "지원하지 않는 파일 형식입니다.",
  "status_code": 400,
  "type": "FileValidationException",
  "details": {
    "supported_formats": [".wav", ".mp3", ".m4a", ".flac", ".ogg"]
  },
  "timestamp": "2024-01-01T12:00:00"
}
```

---

### 3. 서비스 정보

#### `GET /api/v1/info`

STT 서버의 설정 정보와 지원 기능을 조회합니다.

**응답 예시:**
```json
{
  "service": "STT Server",
  "version": "1.0.0",
  "model": "base",
  "device": "cpu",
  "supported_formats": [".wav", ".mp3", ".m4a", ".flac", ".ogg"],
  "max_file_size_mb": 16,
  "features": ["transcription", "language_detection", "segment_analysis"]
}
```

**응답 필드:**
- `service`: 서비스 이름
- `version`: 서비스 버전
- `model`: 사용 중인 Whisper 모델
- `device`: 사용 중인 디바이스 (`cpu`/`gpu`)
- `supported_formats`: 지원하는 파일 형식 목록
- `max_file_size_mb`: 최대 파일 크기 (MB)
- `features`: 지원하는 기능 목록

---

## 레거시 엔드포인트

### `GET /health`
레거시 헬스 체크 엔드포인트 (호환성을 위해 유지)

### `POST /transcribe`
레거시 음성 변환 엔드포인트 (호환성을 위해 유지)

---

## 에러 코드

| 상태 코드 | 설명 | 예시 |
|-----------|------|------|
| 400 | 잘못된 요청 | 지원하지 않는 파일 형식, 파일 크기 초과 |
| 422 | 처리 불가능한 엔티티 | 파일 업로드 실패 |
| 500 | 서버 내부 오류 | 모델 로딩 실패, 변환 오류 |

---

## 사용 예시

### Python (requests)

```python
import requests

# 서버 상태 확인
response = requests.get("http://localhost:7920/api/v1/health")
print(response.json())

# 음성 변환 (자동 언어 감지)
with open("recording.wav", "rb") as f:
    files = {"file": f}
    response = requests.post("http://localhost:7920/api/v1/transcribe", files=files)
    print(response.json())

# 음성 변환 (한국어 고정)
with open("recording.wav", "rb") as f:
    files = {"file": f}
    response = requests.post(
        "http://localhost:7920/api/v1/transcribe?language=ko", 
        files=files
    )
    print(response.json())
```

### JavaScript (fetch)

```javascript
// 서버 상태 확인
fetch('http://localhost:7920/api/v1/health')
  .then(response => response.json())
  .then(data => console.log(data));

// 음성 변환
const formData = new FormData();
formData.append('file', audioFile);

fetch('http://localhost:7920/api/v1/transcribe?language=ko', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

### cURL

```bash
# 서버 상태 확인
curl -X GET "http://localhost:7920/api/v1/health"

# 음성 변환
curl -X POST "http://localhost:7920/api/v1/transcribe" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@recording.wav"

# 한국어로 고정하여 변환
curl -X POST "http://localhost:7920/api/v1/transcribe?language=ko" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@recording.wav"
```

---

## 환경 변수

| 변수명 | 기본값 | 설명 |
|--------|--------|------|
| `HOST` | `0.0.0.0` | 서버 호스트 |
| `PORT` | `7920` | 서버 포트 |
| `WHISPER_MODEL` | `base` | Whisper 모델 크기 |
| `WHISPER_DEVICE` | `cpu` | 처리 디바이스 |
| `WHISPER_LANGUAGE` | `None` | 기본 언어 (미설정 시 자동 감지) |
| `MAX_FILE_SIZE` | `16777216` | 최대 파일 크기 (16MB) |

---

## 제한사항

- **최대 파일 크기**: 16MB
- **지원 파일 형식**: WAV, MP3, M4A, FLAC, OGG
- **동시 요청**: 서버 성능에 따라 제한될 수 있음
- **언어 감지**: Whisper 모델의 정확도에 의존

---

## 문의 및 지원

- **문서**: `/docs` (Swagger UI)
- **대안 문서**: `/redoc` (ReDoc)
- **OpenAPI 스펙**: `/openapi.json` 