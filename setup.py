from setuptools import setup, find_packages

setup(
    name="fastwhisper-stt-server",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "faster-whisper",
        "flask==3.0.0",
        "flask-cors==4.0.0",
        "python-dotenv==1.0.0",
        "requests==2.31.0",
    ],
    author="STT Server Developer",
    description="FastWhisper를 사용한 STT 서버",
    python_requires=">=3.8",
) 