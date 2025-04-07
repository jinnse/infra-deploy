# Python 3.9 이미지를 사용
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요 라이브러리 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . /app/

# 환경 변수 파일 복사
COPY .env /app/

# 애플리케이션 실행
CMD ["python", "app.py"]