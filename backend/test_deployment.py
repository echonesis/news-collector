#!/usr/bin/env python3
"""
部署測試腳本
測試 News Collector API 的基本功能和資料庫連接
"""

import os
import sys

# 添加專案路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_database_connection():
    """測試資料庫連接"""
    try:
        from main import app, db
        from src.models import Subscription, NewsItem
        
        with app.app_context():
            # 測試資料庫連接
            db.create_all()
            print("✅ 資料庫連接成功")
            
            # 測試查詢
            subscriptions = Subscription.query.count()
            news_items = NewsItem.query.count()
            print(f"✅ 資料庫查詢成功 - 訂閱數: {subscriptions}, 新聞數: {news_items}")
            
            return True
            
    except Exception as e:
        print(f"❌ 資料庫測試失敗: {e}")
        return False

def test_imports():
    """測試模組導入"""
    try:
        from main import app
        from database import db
        from src.models import Subscription, NewsItem
        from src.services.email_service import EmailService
        from src.services.news_service import NewsCollectorService
        print("✅ 模組導入成功")
        return True
    except Exception as e:
        print(f"❌ 模組導入失敗: {e}")
        return False

def test_environment():
    """測試環境變數"""
    try:
        email_mode = os.getenv('EMAIL_MODE', 'mock')
        debug = os.getenv('DEBUG', 'True')
        port = os.getenv('PORT', '8000')
        
        print(f"✅ 環境變數檢查:")
        print(f"   EMAIL_MODE: {email_mode}")
        print(f"   DEBUG: {debug}")
        print(f"   PORT: {port}")
        
        return True
    except Exception as e:
        print(f"❌ 環境變數測試失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("🔍 開始部署測試...")
    print("=" * 50)
    
    tests = [
        ("環境變數測試", test_environment),
        ("模組導入測試", test_imports),
        ("資料庫連接測試", test_database_connection),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"💥 {test_name} 失敗")
    
    print("\n" + "=" * 50)
    print(f"🎯 測試結果: {passed}/{total} 通過")
    
    if passed == total:
        print("🎉 所有測試通過！應用程式可以部署")
        return 0
    else:
        print("❌ 部分測試失敗，請檢查配置")
        return 1

if __name__ == '__main__':
    sys.exit(main())
