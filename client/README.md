# STT 웹 클라이언트

FastWhisper STT 서버를 테스트하기 위한 웹 기반 클라이언트입니다.

## 기능

- 음성 파일 업로드
- STT 서버와 통신
- 브라우저 기반 사용자 친화적 인터페이스

## 설치

의존성 설치
```bash
pip install -r requirements.txt
```

## 사용법

### 웹 클라이언트 실행
```bash
python run_web.py
```
브라우저에서 자동으로 http://localhost:3000 이 열립니다.

## 주요 기능

- 브라우저 기반 사용자 친화적 인터페이스
- 서버 연결 상태 실시간 확인
- 파일 업로드 및 경로 입력 지원
- 변환 결과 실시간 표시
- tkinter 설치 불필요

## 지원 파일 형식

- WAV
- MP3
- M4A
- FLAC
- OGG

## 주의사항

1. STT 서버가 실행 중이어야 합니다 (http://localhost:7926)
2. 웹 브라우저가 필요합니다 