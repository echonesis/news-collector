#!/bin/bash

# Render 構建腳本
set -o errexit

echo "🔧 開始構建 News Collector API..."

# 安裝依賴
echo "📦 安裝 Python 依賴..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ 構建完成！"
