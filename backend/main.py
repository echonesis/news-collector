from flask import Flask
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import os
from dotenv import load_dotenv
from database import db

# 載入環境變數
load_dotenv()

# 匯入模型和 API (在全域範圍)
from src.models import *
from src.api import register_routes

# 初始化 Flask 應用
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# 資料庫配置 - 支援 PostgreSQL 和 SQLite
database_url = os.getenv('DATABASE_URL', 'sqlite:///news_collector.db')
# Render 的 PostgreSQL URL 格式轉換
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

# 初始化擴展
db.init_app(app)
CORS(app)

# 初始化排程器
scheduler = BackgroundScheduler()

def create_tables():
    """建立資料庫表格"""
    try:
        with app.app_context():
            db.create_all()
            print("✅ 資料庫表格建立成功")
    except Exception as e:
        print(f"❌ 資料庫表格建立失敗: {e}")
        raise

def start_scheduler():
    """啟動排程器"""
    try:
        from src.services.scheduler_service import setup_scheduled_jobs
        setup_scheduled_jobs(scheduler)
        if not scheduler.running:
            scheduler.start()
            print("✅ 排程器啟動成功")
    except Exception as e:
        print(f"❌ 排程器啟動失敗: {e}")
        # 不要拋出異常，讓應用程式繼續運行

def init_app():
    """初始化應用程式 (用於 Gunicorn)"""
    try:
        # 註冊路由
        register_routes(app)
        print("✅ API 路由註冊完成")
        
        # 建立資料庫表格
        create_tables()
        
        # 啟動排程器
        start_scheduler()
        
        print("✅ News Collector API 初始化完成")
        print(f"📧 Email Mode: {os.getenv('EMAIL_MODE', 'mock')}")
        
        return app
    except Exception as e:
        print(f"❌ 應用程式初始化失敗: {e}")
        raise

# 為 Gunicorn 提供應用程式實例
if os.getenv('GUNICORN_CMD_ARGS') or 'gunicorn' in os.environ.get('SERVER_SOFTWARE', '') or __name__ != '__main__':
    # 在 Gunicorn 環境中運行
    try:
        app = init_app()
    except Exception as e:
        print(f"❌ Gunicorn 初始化失敗: {e}")
        # 提供一個基本的應用程式實例
        register_routes(app)

if __name__ == '__main__':
    # 開發環境直接運行
    try:
        register_routes(app)
        create_tables()
        start_scheduler()
        
        # 獲取環境變數
        port = int(os.getenv('PORT', 8000))
        debug_mode = os.getenv('DEBUG', 'True').lower() == 'true'
        
        print("🚀 News Collector API 啟動中...")
        print(f"📍 Port: {port}")
        print(f"📧 Email Mode: {os.getenv('EMAIL_MODE', 'mock')}")
        print("📊 管理介面: Chrome Extension")
        
        app.run(host='0.0.0.0', port=port, debug=debug_mode)
    except Exception as e:
        print(f"❌ 開發環境啟動失敗: {e}")
        raise
