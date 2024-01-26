# 멀티 아키텍처를 지원하는 Python 3.7 베이스 이미지
FROM python:3.7-slim

# gcc, libasound2-dev, libportaudio2, libportaudiocpp0 및 PortAudio 개발 파일 설치
RUN apt-get update \
    && apt-get install -y gcc libasound2-dev libportaudio2 libportaudiocpp0 portaudio19-dev

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사
COPY requirements.txt .

# 필요한 Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 나머지 애플리케이션 파일 복사
COPY . .

# 컨테이너 시작 시 실행할 명령어
CMD ["python", "./src/app.py"]
