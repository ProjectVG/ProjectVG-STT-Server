#!/bin/bash

echo "FastWhisper STT Server Docker 실행 중..."

# Docker 이미지 빌드
echo "Docker 이미지 빌드 중..."
docker-compose build

# 컨테이너 실행
echo "컨테이너 실행 중..."
docker-compose up -d

echo "서버가 http://localhost:5000 에서 실행 중입니다."
echo "로그 확인: docker-compose logs -f"
echo "서버 중지: docker-compose down" 