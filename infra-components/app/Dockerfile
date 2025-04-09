# 앱을 컨테이너로 패키징할 때 사용되는 Docker 빌드 스크립트
# Python 애플리케이션에서 필요한 라이브러리 목록
# .env DB 연결 정보와 로그 저장 위치 같은 환경 변수 설정 파일

FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY .env .

CMD [ "python", "app/main.py" ]