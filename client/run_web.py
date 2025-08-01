#!/usr/bin/env python3

import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from web_client import STTWebClient

if __name__ == "__main__":
    print("STT 웹 클라이언트를 시작합니다...")
    client = STTWebClient()
    try:
        client.start()
    except KeyboardInterrupt:
        print("\n클라이언트를 종료합니다.") 