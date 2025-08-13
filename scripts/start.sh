#!/bin/bash

# News Collector 快速啟動腳本

echo "🚀 啟動 News Collector..."

# 檢查是否在專案根目錄
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ 請在專案根目錄執行此腳本"
    exit 1
fi

# 建立 .env 檔案（如果不存在）
if [ ! -f "backend/.env" ]; then
    echo "📝 建立環境設定檔..."
    cp backend/.env.example backend/.env
    echo "⚠️  請編輯 backend/.env 檔案設定 SMTP 資訊"
fi

# 啟動服務
echo "🏗️  建置並啟動服務..."
docker-compose up --build -d

echo "✅ News Collector 已啟動！"
echo "📍 API 端點: http://localhost:8000"
echo "📧 管理介面: 載入 Chrome Extension (extension/ 資料夾)"
echo ""
echo "🔧 常用指令:"
echo "  查看日誌: docker-compose logs -f"
echo "  停止服務: docker-compose down"
echo "  重啟服務: docker-compose restart"
