#!/bin/bash

# Render 啟動腳本
# 處理動態端口分配和 Gunicorn 配置

# 設置預設端口（如果 Render 沒有提供）
PORT=${PORT:-10000}

echo "🚀 啟動 News Collector API..."
echo "📍 使用端口: $PORT"
echo "📧 Email Mode: ${EMAIL_MODE:-mock}"
echo "🐍 Python 路徑: $PYTHONPATH"

# 啟動 Gunicorn
exec gunicorn \
    --bind "0.0.0.0:$PORT" \
    --workers 2 \
    --timeout 120 \
    --preload \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    main:app
