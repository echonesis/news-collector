from datetime import datetime, timedelta
from src.models import Subscription, NewsItem, Newsletter
from src.services.news_service import NewsCollectorService
from database import db
from main import app
import os

def setup_scheduled_jobs(scheduler):
    """設定排程任務"""
    
    # 每小時檢查是否有需要發送的電子報
    scheduler.add_job(
        func=check_and_send_newsletters,
        trigger="interval",
        hours=1,
        id='newsletter_check'
    )
    
    print("✅ 排程任務已設定")

def check_and_send_newsletters():
    """檢查並發送電子報"""
    with app.app_context():
        try:
            now = datetime.utcnow()
            subscriptions = Subscription.query.filter_by(is_active=True).all()
            
            for subscription in subscriptions:
                if should_send_newsletter(subscription, now):
                    send_newsletter_for_subscription(subscription)
                    
        except Exception as e:
            print(f"檢查電子報任務失敗: {e}")

def should_send_newsletter(subscription, now):
    """判斷是否應該發送電子報"""
    if not subscription.last_sent:
        return True
    
    time_diff = now - subscription.last_sent
    
    frequency_hours = {
        'daily': 24,
        'weekly': 168,  # 7 * 24
        'monthly': 720  # 30 * 24
    }
    
    required_hours = frequency_hours.get(subscription.frequency, 24)
    return time_diff.total_seconds() >= required_hours * 3600

def send_newsletter_for_subscription(subscription):
    """為特定訂閱發送電子報"""
    try:
        # 收集新聞
        news_service = NewsCollectorService()
        news_items = news_service.collect_news(subscription.topic, limit=10)
        
        if news_items:
            # 儲存新聞到資料庫
            news_service.save_news_items(news_items)
            
            # 發送電子報 (根據環境變數選擇服務)
            email_mode = os.getenv('EMAIL_MODE', 'mock')
            
            if email_mode == 'real':
                from src.services.email_service import EmailService
                email_service = EmailService()
            else:
                from src.services.mock_email_service import MockEmailService
                email_service = MockEmailService()
            
            email_success = email_service.send_newsletter(
                subscription.email, 
                subscription.topic, 
                news_items
            )
            
            if email_success:
                print(f"✅ 電子報已發送: {subscription.topic} -> {subscription.email}")
                
                # 記錄發送狀態
                subscription.last_sent = datetime.utcnow()
                db.session.commit()
            else:
                print(f"❌ 電子報發送失敗: {subscription.topic} -> {subscription.email}")
        else:
            print(f"❌ 沒有找到新聞: {subscription.topic}")
        
    except Exception as e:
        print(f"發送電子報失敗 ({subscription.topic}): {e}")
        db.session.rollback()
