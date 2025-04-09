-- 1. DB 생성 (이미 생성된 상태라면 생략 가능)
CREATE DATABASE weather;

-- 2. 테이블 생성
CREATE TABLE IF NOT EXISTS weather_data (
  id SERIAL PRIMARY KEY,
  city VARCHAR(50),
  temperature FLOAT,
  humidity INT,
  recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. 초기 데이터 삽입 (선택)
INSERT INTO weather_data (city, temperature, humidity)
VALUES ('Seoul', 23.4, 65);