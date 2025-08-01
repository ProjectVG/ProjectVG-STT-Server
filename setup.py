from setuptools import setup, find_packages

setup(
    name="fastwhisper-stt-server",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "faster-whisper",
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "python-multipart==0.0.6",
        "python-dotenv==1.0.0",
        "requests==2.31.0",
    ],
    author="STT Server Developer",
    description="FastWhisper를 사용한 STT 서버",
    python_requires=">=3.8",
) 