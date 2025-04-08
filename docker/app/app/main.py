from flask import Flask, jsonify
import psycopg2
import logging
from config import Config
from dotenv import load_dotenv
import traceback

load_dotenv()

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
        logging.error("DB 연결 실패:\n" + traceback.format_exc())
        return jsonify({"error": "DB 연결 실패"}), 500
    
# ✅ 서버 실행 코드 추가
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
