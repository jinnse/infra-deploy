from flask import Flask, jsonify
import psycopg2
import logging
from config import Config

app = Flask(__name__)

# 로깅 설정
logging.basicConfig(
    filename=Config.LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

@app.route('/')
def index():
    return jsonify({"message": "Flask app is running!"})

@app.route('/weather')
def weather_data():
    try:
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM weather LIMIT 5;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(rows)
    except Exception as e:
        logging.error(f"DB 연결 실패: {e}")
        return jsonify({"error": "DB 연결 실패"}), 500
