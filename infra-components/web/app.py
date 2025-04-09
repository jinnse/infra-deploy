from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# Flask 애플리케이션 설정
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# OpenWeatherMap API 설정
API_KEY = os.getenv("API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# 데이터베이스 모델
class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Weather {self.city}>'

# 홈 페이지
@app.route('/')
def index():
    weather_data = Weather.query.all()
    return render_template('index.html', weather_data=weather_data)

# 도시 날씨 정보 조회
@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.form.get('city')
    if not city:
        return redirect(url_for('index'))

    # OpenWeatherMap API 호출
    response = requests.get(f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric")
    data = response.json()

    if data['cod'] != 200:
        # API 호출 실패 시 처리
        return f"Error: {data['message']}", 400

    # 날씨 데이터 파싱
    temperature = data['main']['temp']
    description = data['weather'][0]['description']

    # 데이터베이스에 저장
    new_weather = Weather(city=city, temperature=temperature, description=description)
    db.session.add(new_weather)
    db.session.commit()

    return redirect(url_for('index'))

# 삭제 기능
@app.route('/delete/<int:id>')
def delete(id):
    weather = Weather.query.get_or_404(id)
    db.session.delete(weather)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()  # 데이터베이스 테이블 생성
    app.run(host="0.0.0.0", port=5000)