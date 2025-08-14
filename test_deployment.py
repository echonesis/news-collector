#!/usr/bin/env python3
"""
本地測試腳本 - 模擬 Render 部署環境
測試 News Collector API 的基本功能
"""

import os
import sys
import requests
import time

def test_api_endpoint(base_url):
    """測試 API 端點"""
    print(f"🔍 測試 API: {base_url}")
    
    try:
        # 測試健康檢查
        print("  ➤ 測試健康檢查...")
        response = requests.get(f"{base_url}/api/health", timeout=10)
        
        if response.status_code == 200:
            print("  ✅ 健康檢查通過")
            data = response.json()
            print(f"     狀態: {data.get('status')}")
            print(f"     訊息: {data.get('message')}")
        else:
            print(f"  ❌ 健康檢查失敗: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"  ❌ 連接失敗: {e}")
        return False
    
    try:
        # 測試取得訂閱列表
        print("  ➤ 測試取得訂閱列表...")
        response = requests.get(f"{base_url}/api/subscriptions", timeout=10)
        
        if response.status_code == 200:
            print("  ✅ 訂閱 API 正常")
            data = response.json()
            print(f"     現有訂閱數: {len(data.get('subscriptions', []))}")
        else:
            print(f"  ❌ 訂閱 API 失敗: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"  ❌ 訂閱 API 連接失敗: {e}")
    
    return True

def main():
    """主測試函數"""
    print("🚀 News Collector API 部署測試")
    print("=" * 50)
    
    # 測試本地服務
    local_url = "http://localhost:8000"
    print("\n📍 測試本地服務...")
    local_ok = test_api_endpoint(local_url)
    
    if not local_ok:
        print("\n❌ 本地服務未啟動或有問題")
        print("請確保後端服務正在運行:")
        print("  cd backend && python start.py")
        return
    
    # 如果提供了 Render URL，也測試線上服務
    render_url = os.getenv('RENDER_URL')
    if render_url:
        print(f"\n📍 測試 Render 部署服務: {render_url}")
        render_ok = test_api_endpoint(render_url)
        
        if render_ok:
            print("\n✅ Render 部署測試通過！")
        else:
            print("\n❌ Render 部署測試失敗")
    else:
        print("\n💡 提示: 設定 RENDER_URL 環境變數來測試線上部署")
        print("   例如: export RENDER_URL=https://your-app.onrender.com")
    
    print("\n🎉 測試完成")

if __name__ == '__main__':
    main()
