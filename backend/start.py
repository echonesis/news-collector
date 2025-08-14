"""
Render 部署啟動腳本
專為 Render 平台優化的生產環境配置
"""
import os
from datetime import datetime
from flask import Flask
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from database import db

# 導入模型和 API (避免循環導入)
from src.models import *
from src.api import register_routes

# 載入環境變數
load_dotenv()

def create_app():
    """建立並配置 Flask 應用程式"""
    app = Flask(__name__)
    
    # 生產環境配置
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'render-production-key')
    
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
    
    app.config['ENV'] = 'production'
    app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # 初始化擴展
    db.init_app(app)
    
    # CORS 配置 - 生產環境可限制特定域名
    allowed_origins = os.getenv('ALLOWED_ORIGINS', '*').split(',')
    CORS(app, origins=allowed_origins)
    
    # 註冊 API 路由
    register_routes(app)
    
    # 建立資料庫表格
    with app.app_context():
        try:
            db.create_all()
            print("✅ 資料庫初始化完成")
        except Exception as e:
            print(f"❌ 資料庫初始化失敗: {e}")
            raise
    
    # 添加健康檢查路由 (移除重複定義)
    
    return app

def setup_scheduler(app):
    """設置背景排程器"""
    scheduler = BackgroundScheduler()
    
    with app.app_context():
        from src.services.scheduler_service import setup_scheduled_jobs
        setup_scheduled_jobs(scheduler)
        scheduler.start()
        print("✅ 排程器啟動完成")
    
    return scheduler

# 建立應用程式實例
app = create_app()
scheduler = setup_scheduler(app)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    host = os.getenv('HOST', '0.0.0.0')
    
    print("🚀 News Collector API 正在 Render 上啟動...")
    print(f"📍 Port: {port}")
    print("📧 Email Mode:", os.getenv('EMAIL_MODE', 'mock'))
    
    app.run(
        host=host,
        port=port,
        debug=app.config['DEBUG'],
        threaded=True
    )
