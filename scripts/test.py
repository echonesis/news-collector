#!/usr/bin/env python3
"""
News Collector 測試腳本
用於驗證基本功能，不依賴外部套件
"""

import json
import sys
import os

def test_project_structure():
    """測試專案結構"""
    print("🔍 檢查專案結構...")
    
    required_files = [
        'README.md',
        'backend/main.py',
        'backend/requirements.txt',
        'extension/manifest.json',
        'extension/popup/popup.html',
        'docker-compose.yml'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ 缺少檔案: {missing_files}")
        return False
    else:
        print("✅ 專案結構完整")
        return True

def test_extension_manifest():
    """測試 Chrome Extension manifest"""
    print("🔍 檢查 Extension manifest...")
    
    try:
        with open('extension/manifest.json', 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        required_fields = ['manifest_version', 'name', 'version', 'permissions']
        for field in required_fields:
            if field not in manifest:
                print(f"❌ manifest.json 缺少欄位: {field}")
                return False
        
        print("✅ Extension manifest 格式正確")
        return True
        
    except Exception as e:
        print(f"❌ 讀取 manifest.json 失敗: {e}")
        return False

def test_api_structure():
    """測試 API 結構"""
    print("🔍 檢查 API 結構...")
    
    api_files = [
        'backend/src/models/__init__.py',
        'backend/src/api/__init__.py',
        'backend/src/services/news_service.py',
        'backend/src/services/email_service.py'
    ]
    
    for file_path in api_files:
        if not os.path.exists(file_path):
            print(f"❌ 缺少 API 檔案: {file_path}")
            return False
    
    print("✅ API 結構完整")
    return True

def main():
    """主測試函數"""
    print("🧪 News Collector 專案測試\n")
    
    tests = [
        test_project_structure,
        test_extension_manifest,
        test_api_structure
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 測試結果: {passed}/{total} 通過")
    
    if passed == total:
        print("🎉 所有測試通過！專案結構設置完成。")
        print("\n📋 下一步:")
        print("1. 設定後端環境: cd backend && pip install -r requirements.txt")
        print("2. 建立 .env 檔案並設定 SMTP 資訊")
        print("3. 載入 Chrome Extension")
        print("4. 啟動服務: python backend/main.py")
        return 0
    else:
        print("❌ 部分測試失敗，請檢查專案結構")
        return 1

if __name__ == '__main__':
    sys.exit(main())
