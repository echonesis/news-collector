from flask import Flask
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import os
from dotenv import load_dotenv
from database import db

# 載入環境變數
load_dotenv()

# 初始化 Flask 應用
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///news_collector.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化擴展
db.init_app(app)
CORS(app)

# 初始化排程器
scheduler = BackgroundScheduler()

def create_tables():
    """建立資料庫表格"""
    with app.app_context():
        db.create_all()

def start_scheduler():
    """啟動排程器"""
    from src.services.scheduler_service import setup_scheduled_jobs
    setup_scheduled_jobs(scheduler)
    scheduler.start()

if __name__ == '__main__':
    # 匯入模組 (避免循環導入)
    from src.models import *
    from src.api import *
    
    create_tables()
    start_scheduler()
    
    print("🚀 News Collector API 啟動中...")
    print("📍 API 端點: http://localhost:8000")
    print("📧 管理介面: Chrome Extension")
    
    app.run(host='0.0.0.0', port=8000, debug=True)
