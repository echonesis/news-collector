#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡化的電子郵件測試腳本
直接發送測試電子報到 echonesis@gmail.com
"""

import os
import sys
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 添加專案路徑到 Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_send_email():
    """測試發送電子報"""
    try:
        from src.services.email_service import EmailService
        
        print("Testing email service...")
        
        # 檢查配置
        email_mode = os.getenv('EMAIL_MODE', 'mock')
        sender_email = os.getenv('SENDER_EMAIL', '')
        sender_password = os.getenv('SENDER_PASSWORD', '')
        
        print(f"EMAIL_MODE: {email_mode}")
        print(f"SENDER_EMAIL: {sender_email}")
        print(f"Password configured: {'Yes' if sender_password else 'No'}")
        
        if email_mode != 'real':
            print("WARNING: EMAIL_MODE is not 'real'")
            return
            
        if not sender_email or not sender_password:
            print("ERROR: Missing SENDER_EMAIL or SENDER_PASSWORD")
            return
        
        # 建立電子郵件服務
        email_service = EmailService()
        
        # 測試連接
        print("\nTesting SMTP connection...")
        success, message = email_service.test_connection()
        print(f"Connection test: {message}")
        
        if not success:
            print("Connection test failed, aborting email send")
            return
        
        # 準備測試新聞資料
        test_news = [
            {
                'title': 'Test Newsletter Title',
                'summary': 'This is a test newsletter content to verify email functionality.',
                'url': 'https://example.com/test-news',
                'source': 'Test Source',
                'published_at': '2024-01-01T00:00:00'
            },
            {
                'title': 'Second Test Article',
                'summary': 'Another test article to show multiple news items in the newsletter.',
                'url': 'https://example.com/test-news-2',
                'source': 'Test Source 2',
                'published_at': '2024-01-01T01:00:00'
            }
        ]
        
        # 發送測試電子報
        recipient = "echonesis@gmail.com"
        topic = "Test Topic"
        
        print(f"\nSending test newsletter to {recipient}...")
        success = email_service.send_newsletter(recipient, topic, test_news)
        
        if success:
            print("✅ Test newsletter sent successfully!")
        else:
            print("❌ Failed to send test newsletter")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_send_email()
