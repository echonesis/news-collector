#!/usr/bin/env python3
"""
電子郵件服務測試腳本
用於診斷和測試 SMTP 連接問題
"""

import os
import sys
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 添加專案路徑到 Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.email_service import EmailService

def test_email_service():
    """測試電子郵件服務"""
    print("🔧 電子郵件服務測試")
    print("=" * 50)
    
    # 檢查環境變數
    print("📋 檢查環境變數:")
    email_mode = os.getenv('EMAIL_MODE', 'mock')
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = os.getenv('SMTP_PORT', '587')
    sender_email = os.getenv('SENDER_EMAIL', '')
    sender_password = os.getenv('SENDER_PASSWORD', '')
    
    print(f"   EMAIL_MODE: {email_mode}")
    print(f"   SMTP_SERVER: {smtp_server}")
    print(f"   SMTP_PORT: {smtp_port}")
    print(f"   SENDER_EMAIL: {sender_email[:5]}...{sender_email[-10:] if len(sender_email) > 15 else sender_email}")
    print(f"   SENDER_PASSWORD: {'✅ 已設置' if sender_password else '❌ 未設置'}")
    print()
    
    if email_mode != 'real':
        print("⚠️  EMAIL_MODE 不是 'real'，將使用 Mock 服務")
        print("   如要測試真實郵件發送，請設置 EMAIL_MODE=real")
        return
    
    if not sender_email or not sender_password:
        print("❌ 缺少必要的環境變數 SENDER_EMAIL 或 SENDER_PASSWORD")
        print("\n💡 設置方法:")
        print("   1. 複製 .env.example 為 .env")
        print("   2. 填入實際的 SMTP 設定")
        print("   3. 如使用 Gmail，需要設置應用程式密碼")
        return
    
    # 測試 SMTP 連接
    print("🔗 測試 SMTP 連接...")
    email_service = EmailService()
    
    success, message = email_service.test_connection()
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
        print("\n🔧 疑難排解:")
        print("   1. 檢查網路連接")
        print("   2. 確認 SMTP 伺服器和埠號正確")
        print("   3. 如使用 Gmail:")
        print("      - 啟用兩步驟驗證")
        print("      - 產生應用程式密碼")
        print("      - 使用應用程式密碼而非一般密碼")
        print("   4. 檢查防火牆設定")
        return
    
    # 測試發送郵件
    test_email = input("\n📧 輸入測試收件者電子郵件 (按 Enter 跳過): ").strip()
    if test_email:
        print(f"\n📤 發送測試電子報至 {test_email}...")
        
        # 模擬新聞資料
        test_news = [
            {
                'title': '測試新聞標題',
                'summary': '這是一個測試電子報的摘要內容',
                'url': 'https://example.com',
                'source': '測試來源',
                'published_at': '2024-01-01T00:00:00'
            }
        ]
        
        success = email_service.send_newsletter(test_email, "測試主題", test_news)
        if success:
            print("✅ 測試電子報發送成功！")
        else:
            print("❌ 測試電子報發送失敗")
    
    print("\n✨ 測試完成")

if __name__ == "__main__":
    try:
        test_email_service()
    except KeyboardInterrupt:
        print("\n\n⚠️  測試已取消")
    except Exception as e:
        print(f"\n❌ 測試過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc()
