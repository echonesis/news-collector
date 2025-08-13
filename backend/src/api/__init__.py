from flask import request, jsonify
from main import app
from database import db
from src.models import Subscription
from datetime import datetime
import os

@app.route('/api/subscriptions', methods=['POST'])
def create_subscription():
    """建立新訂閱"""
    try:
        data = request.get_json()
        
        # 驗證必要欄位
        required_fields = ['topic', 'email', 'frequency']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'缺少必要欄位: {field}'}), 400
        
        # 檢查是否已存在相同訂閱
        existing = Subscription.query.filter_by(
            topic=data['topic'],
            email=data['email']
        ).first()
        
        if existing:
            return jsonify({'error': '此主題訂閱已存在'}), 409
        
        # 建立新訂閱
        subscription = Subscription(
            topic=data['topic'],
            email=data['email'],
            frequency=data['frequency']
        )
        
        db.session.add(subscription)
        db.session.commit()
        
        # 新訂閱處理邏輯
        welcome_result = handle_new_subscription(subscription)
        
        return jsonify({
            'message': '訂閱建立成功',
            'subscription': subscription.to_dict(),
            'welcome_action': welcome_result
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'建立訂閱失敗: {str(e)}'}), 500

@app.route('/api/subscriptions', methods=['GET'])
def get_subscriptions():
    """取得所有訂閱"""
    try:
        email = request.args.get('email')
        query = Subscription.query
        
        if email:
            query = query.filter_by(email=email)
        
        subscriptions = query.filter_by(is_active=True).all()
        
        return jsonify({
            'subscriptions': [sub.to_dict() for sub in subscriptions]
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'取得訂閱失敗: {str(e)}'}), 500

@app.route('/api/subscriptions/<int:subscription_id>', methods=['DELETE'])
def delete_subscription(subscription_id):
    """刪除訂閱"""
    try:
        subscription = Subscription.query.get_or_404(subscription_id)
        subscription.is_active = False
        db.session.commit()
        
        return jsonify({'message': '訂閱已取消'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'取消訂閱失敗: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康檢查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'message': 'News Collector API is running'
    }), 200

@app.route('/api/test-news-collection', methods=['POST'])
def test_news_collection():
    """測試新聞收集功能"""
    try:
        data = request.get_json()
        topic = data.get('topic', 'AI 人工智慧')
        limit = data.get('limit', 5)
        
        # 導入新聞收集服務
        from src.services.news_service import NewsCollectorService
        
        news_service = NewsCollectorService()
        news_items = news_service.collect_news(topic, limit)
        
        if news_items:
            # 儲存到資料庫
            saved_count = news_service.save_news_items(news_items)
            
            return jsonify({
                'message': f'成功收集 {len(news_items)} 則新聞，儲存 {saved_count} 則',
                'topic': topic,
                'collected': len(news_items),
                'saved': saved_count,
                'news_items': news_items
            }), 200
        else:
            return jsonify({
                'message': '未收集到新聞',
                'topic': topic,
                'collected': 0,
                'saved': 0,
                'news_items': []
            }), 200
            
    except Exception as e:
        return jsonify({'error': f'新聞收集測試失敗: {str(e)}'}), 500

@app.route('/api/news', methods=['GET'])
def get_news():
    """取得新聞記錄"""
    try:
        from src.models import NewsItem
        
        topic = request.args.get('topic')
        limit = int(request.args.get('limit', 10))
        
        query = NewsItem.query
        if topic:
            query = query.filter_by(topic=topic)
        
        news_items = query.order_by(NewsItem.created_at.desc()).limit(limit).all()
        
        return jsonify({
            'count': len(news_items),
            'news_items': [item.to_dict() for item in news_items]
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'取得新聞失敗: {str(e)}'}), 500

@app.route('/api/test-email', methods=['POST'])
def test_email():
    """測試email發送功能"""
    try:
        data = request.get_json()
        recipient_email = data.get('email')
        topic = data.get('topic', 'AI 人工智慧')
        
        if not recipient_email:
            return jsonify({'error': '請提供收件人email'}), 400
        
        # 取得一些新聞項目來測試
        from src.models import NewsItem
        news_items = NewsItem.query.filter_by(topic=topic).limit(3).all()
        
        if not news_items:
            # 如果沒有新聞，先收集一些
            from src.services.news_service import NewsCollectorService
            news_service = NewsCollectorService()
            collected_news = news_service.collect_news(topic, 3)
            news_service.save_news_items(collected_news)
            
            # 轉換為字典格式
            news_data = collected_news
        else:
            # 轉換現有新聞為字典格式
            news_data = [item.to_dict() for item in news_items]
        
        # 發送email (根據環境變數選擇服務)
        email_mode = os.getenv('EMAIL_MODE', 'mock')
        
        if email_mode == 'real':
            from src.services.email_service import EmailService
            email_service = EmailService()
        else:
            from src.services.mock_email_service import MockEmailService
            email_service = MockEmailService()
        
        success = email_service.send_newsletter(recipient_email, topic, news_data)
        
        if success:
            return jsonify({
                'message': f'測試email已發送至 {recipient_email}',
                'topic': topic,
                'news_count': len(news_data)
            }), 200
        else:
            return jsonify({'error': 'Email發送失敗，請檢查SMTP設定'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Email測試失敗: {str(e)}'}), 500

@app.route('/api/send-newsletters', methods=['POST'])
def send_newsletters():
    """手動觸發發送電子報給所有訂閱者"""
    try:
        # 取得所有活躍訂閱
        subscriptions = Subscription.query.filter_by(is_active=True).all()
        
        if not subscriptions:
            return jsonify({'message': '沒有活躍的訂閱'}), 200
        
        sent_count = 0
        failed_count = 0
        
        # 為每個訂閱發送電子報
        for subscription in subscriptions:
            try:
                # 收集新聞
                from src.services.news_service import NewsCollectorService
                news_service = NewsCollectorService()
                news_items = news_service.collect_news(subscription.topic, limit=5)
                
                if news_items:
                    # 儲存新聞
                    news_service.save_news_items(news_items)
                    
                    # 發送email
                    email_mode = os.getenv('EMAIL_MODE', 'mock')
                    
                    if email_mode == 'real':
                        from src.services.email_service import EmailService
                        email_service = EmailService()
                    else:
                        from src.services.mock_email_service import MockEmailService
                        email_service = MockEmailService()
                    
                    success = email_service.send_newsletter(
                        subscription.email, 
                        subscription.topic, 
                        news_items
                    )
                    
                    if success:
                        sent_count += 1
                        subscription.last_sent = datetime.utcnow()
                    else:
                        failed_count += 1
                else:
                    print(f"沒有找到 {subscription.topic} 的新聞")
                    
            except Exception as e:
                print(f"處理訂閱失敗 {subscription.email}: {e}")
                failed_count += 1
        
        # 保存更新
        db.session.commit()
        
        return jsonify({
            'message': f'電子報發送完成',
            'total_subscriptions': len(subscriptions),
            'sent': sent_count,
            'failed': failed_count
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'發送電子報失敗: {str(e)}'}), 500

def handle_new_subscription(subscription):
    """處理新訂閱的歡迎邏輯"""
    try:
        from src.models import NewsItem
        
        # 檢查是否已有該主題的新聞（最近7天內）
        from datetime import timedelta
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        
        existing_news = NewsItem.query.filter(
            NewsItem.topic == subscription.topic,
            NewsItem.created_at >= seven_days_ago
        ).limit(5).all()
        
        if existing_news:
            # 有現有新聞，立即發送歡迎email
            news_data = [item.to_dict() for item in existing_news]
            send_welcome_email(subscription, news_data)
            
            # 更新last_sent時間
            subscription.last_sent = datetime.utcnow()
            db.session.commit()
            
            return {
                'action': 'sent_welcome_email',
                'news_count': len(news_data),
                'message': '立即發送歡迎email，包含現有新聞'
            }
        else:
            # 沒有現有新聞，收集新聞
            from src.services.news_service import NewsCollectorService
            news_service = NewsCollectorService()
            collected_news = news_service.collect_news(subscription.topic, limit=5)
            
            if collected_news:
                # 儲存新聞
                news_service.save_news_items(collected_news)
                
                # 發送歡迎email
                send_welcome_email(subscription, collected_news)
                
                # 更新last_sent時間
                subscription.last_sent = datetime.utcnow()
                db.session.commit()
                
                return {
                    'action': 'collected_and_sent',
                    'news_count': len(collected_news),
                    'message': '收集新聞並發送歡迎email'
                }
            else:
                # 沒有收集到新聞，等待下次排程
                return {
                    'action': 'wait_for_schedule',
                    'news_count': 0,
                    'message': '沒有收集到新聞，將在下次排程時再試'
                }
                
    except Exception as e:
        print(f"處理新訂閱失敗: {e}")
        return {
            'action': 'error',
            'message': f'處理失敗: {str(e)}'
        }

def send_welcome_email(subscription, news_data):
    """發送歡迎email"""
    try:
        # 根據環境變數選擇email服務
        email_mode = os.getenv('EMAIL_MODE', 'mock')
        
        if email_mode == 'real':
            from src.services.email_service import EmailService
            email_service = EmailService()
        else:
            from src.services.mock_email_service import MockEmailService
            email_service = MockEmailService()
        
        # 發送包含歡迎訊息的電子報
        success = email_service.send_newsletter(
            subscription.email,
            f"歡迎訂閱 - {subscription.topic}",
            news_data
        )
        
        if success:
            print(f"✅ 歡迎email已發送: {subscription.topic} -> {subscription.email}")
        else:
            print(f"❌ 歡迎email發送失敗: {subscription.topic} -> {subscription.email}")
            
        return success
        
    except Exception as e:
        print(f"發送歡迎email失敗: {e}")
        return False

@app.route('/api/test-scheduler', methods=['POST'])
def test_scheduler():
    """測試排程功能"""
    try:
        # 手動觸發排程檢查
        from src.services.scheduler_service import check_and_send_newsletters
        
        print("🔄 手動觸發排程檢查...")
        check_and_send_newsletters()
        
        return jsonify({
            'message': '排程檢查已完成',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'排程測試失敗: {str(e)}'}), 500

@app.route('/api/subscription-status', methods=['GET'])
def subscription_status():
    """檢查所有訂閱的狀態"""
    try:
        subscriptions = Subscription.query.filter_by(is_active=True).all()
        
        status_list = []
        for sub in subscriptions:
            from src.services.scheduler_service import should_send_newsletter
            should_send = should_send_newsletter(sub, datetime.utcnow())
            
            status_list.append({
                'id': sub.id,
                'email': sub.email,
                'topic': sub.topic,
                'frequency': sub.frequency,
                'last_sent': sub.last_sent.isoformat() if sub.last_sent else None,
                'should_send_now': should_send,
                'created_at': sub.created_at.isoformat()
            })
        
        return jsonify({
            'total_subscriptions': len(subscriptions),
            'subscriptions': status_list
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'檢查訂閱狀態失敗: {str(e)}'}), 500
