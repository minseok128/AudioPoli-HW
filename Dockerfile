# 파이썬 공식 이미지를 기반으로 설정
FROM arm32v7/python:3.9

# 애플리케이션 파일들이 위치할 작업 디렉토리 생성
WORKDIR /app

# 현재 디렉토리의 파일들을 컨테이너의 /app 디렉토리로 복사
COPY . /app

# 필요한 파이썬 패키지를 설치
RUN pip install -r requirements.txt

# 컨테이너가 시작될 때 실행될 명령어 설정
CMD ["python", "src/app.py"]
