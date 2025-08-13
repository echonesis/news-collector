# News Collector - 智能新聞訂閱系統

一個智能的新聞收集與訂閱系統，支持自動收集新聞並通過電子郵件發送給訂閱用戶。

## ✨ 核心特性

- 🔍 **智能新聞收集**：自動從Google News RSS收集相關新聞
- 📧 **自動電子報**：定期發送格式精美的HTML電子報
- 🎯 **智能歡迎系統**：新訂閱者立即獲得相關新聞
- ⏰ **靈活排程**：支持daily/weekly/monthly發送頻率
- 🎨 **Chrome Extension**：簡潔易用的訂閱管理介面
- 🔧 **開發友好**：模擬模式便於開發測試

## 🚀 快速開始

### 1. 啟動後端服務

```bash
cd backend
pip install -r requirements.txt
python main.py
```

### 2. 安裝Chrome Extension

1. 開啟 `chrome://extensions/`
2. 開啟「開發者模式」
3. 載入 `extension` 資料夾

### 3. 建立第一個訂閱

在Chrome Extension中填寫：
- 主題：AI 人工智慧
- 頻率：daily
- Email：your-email@example.com

## 📖 文檔

- **[API 文檔](docs/api.md)** - 完整的API端點說明和範例
- **[系統架構](docs/architecture.md)** - 深入了解系統設計和機制
- **[部署指南](docs/deployment.md)** - 從開發到生產的完整部署流程
- **[開發指南](docs/development.md)** - 開發環境設置和擴展指南

## 🏗️ 系統架構

```
Chrome Extension ──► Backend API ──► News Sources (RSS)
                         │
                         ▼
                    SQLite Database
                         │
                         ▼
                   Email Service
```

## 🔧 技術棧

- **後端**: Python, Flask, SQLAlchemy, APScheduler
- **前端**: Chrome Extension (Manifest V3)
- **資料庫**: SQLite (可擴展至PostgreSQL/MySQL)
- **新聞源**: Google News RSS
- **排程**: APScheduler
- **Email**: SMTP (支援Gmail)

## 📋 主要功能

### 智能歡迎機制
- 檢查現有新聞並立即發送
- 自動收集新主題新聞
- 避免空電子報

### 排程系統
- 每小時檢查待發送訂閱
- 嚴格按照頻率控制發送
- 避免重複發送

### 電子報系統
- 精美的HTML格式
- 模擬模式便於測試
- 真實SMTP發送支援

## �️ API 端點

| 端點 | 方法 | 功能 |
|------|------|------|
| `/api/health` | GET | 健康檢查 |
| `/api/subscriptions` | POST | 建立訂閱 |
| `/api/subscriptions` | GET | 查詢訂閱 |
| `/api/test-news-collection` | POST | 測試新聞收集 |
| `/api/test-email` | POST | 測試email發送 |
| `/api/send-newsletters` | POST | 手動發送電子報 |
| `/api/subscription-status` | GET | 檢查訂閱狀態 |

## 📝 使用範例

### 建立訂閱
```bash
curl -X POST http://localhost:8000/api/subscriptions \
  -H "Content-Type: application/json" \
  -d '{"topic": "AI", "email": "user@example.com", "frequency": "daily"}'
```

### 測試新聞收集
```bash
curl -X POST http://localhost:8000/api/test-news-collection \
  -H "Content-Type: application/json" \
  -d '{"topic": "AI", "limit": 5}'
```

## 🔧 環境配置

```bash
# 開發模式（推薦）
EMAIL_MODE=mock

# 生產模式
EMAIL_MODE=real
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
```

## 🎯 開發測試流程

1. **健康檢查**: `curl http://localhost:8000/api/health`
2. **建立訂閱**: 使用Chrome Extension或API
3. **檢查狀態**: `curl http://localhost:8000/api/subscription-status`
4. **測試收集**: `curl -X POST http://localhost:8000/api/test-news-collection`
5. **查看結果**: 檢查 `backend/logs/` 中的HTML文件

## 🚀 部署選項

- **本地開發**: Python直接運行
- **Docker**: 容器化部署
- **系統服務**: systemd服務
- **反向代理**: Nginx配置

---

**News Collector** - 讓新聞主動找到你 📰✨
