# News Collector - Render 部署指南

## 🚀 快速部署到 Render

本專案已針對 Render 平台進行優化，使用現有的 Dockerfile 即可輕鬆部署為生產環境。

### 部署步驟

#### 1. 準備 Render 帳戶
- 註冊 [Render](https://render.com) 帳戶
- 連接您的 GitHub 帳戶

#### 2. 創建新的 Web Service
1. 登入 Render Dashboard
2. 點擊 "New +" → "Web Service"
3. 選擇此 GitHub repository
4. 配置以下設定：

**基本設定:**
- **Name:** `news-collector-api`
- **Region:** `Singapore` (或最近的區域)
- **Branch:** `main`
- **Root Directory:** `backend`

**構建與運行設定:**
- **Runtime:** `Docker`
- **Dockerfile Path:** `backend/Dockerfile`

#### 3. 環境變數設定

在 Render Dashboard 的 Environment 設定中添加：

**必要環境變數:**
```
EMAIL_MODE=real
DEBUG=False
SECRET_KEY=<自動生成或手動設定>
PORT=8000
```

**郵件服務設定 (使用真實 SMTP):**
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
```

**資料庫設定:**
```
DATABASE_URL=<PostgreSQL 連接字串>
```

#### 4. 資料庫設定 (推薦)

**使用 Render PostgreSQL:**
1. 創建新的 PostgreSQL database
2. 複製連接字串到 `DATABASE_URL` 環境變數

**或使用 SQLite (開發用):**
- 不設定 `DATABASE_URL`，系統會使用內建 SQLite

### 🐳 Docker 配置特色

本專案使用優化的 Dockerfile：

```dockerfile
FROM python:3.11-slim
WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# 安裝 Python 依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式碼
COPY . .

# 建立資料目錄
RUN mkdir -p instance

# 設置環境變數
ENV PYTHONPATH=/app
ENV EMAIL_MODE=real
ENV DEBUG=False

EXPOSE 8000

# 使用 Gunicorn 作為生產環境 WSGI 服務器
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120", "main:app"]
```

### 🔧 生產環境特色

- **WSGI Server:** 使用 Gunicorn 提供高效能
- **資料庫:** 支援 PostgreSQL 和 SQLite
- **自動初始化:** 應用程式自動建立資料庫表格
- **排程器:** 背景新聞收集和郵件發送
- **CORS:** 配置跨域資源共享
- **環境變數:** 安全的配置管理
- **真實郵件:** 使用 SMTP 發送實際電子郵件

### 🚨 安全考量

1. **SECRET_KEY:** 使用強隨機密鑰
2. **EMAIL_MODE:** 設為 `real` 啟用真實郵件發送
3. **SMTP 密碼:** 使用應用程式密碼，非一般登入密碼
4. **DATABASE_URL:** 使用 PostgreSQL 提供更好的效能和穩定性

### 📊 監控與維護

- **日誌:** Render 提供即時日誌查看
- **健康檢查:** 應用程式自動監控 (`/api/health`)
- **自動重啟:** 服務異常時自動重啟
- **SSL:** Render 自動提供 HTTPS

### 🔗 部署後測試

部署完成後，您的 API 將可在以下網址使用：
```
https://news-collector-api.onrender.com
```

測試 API 健康狀況：
```bash
curl https://news-collector-api.onrender.com/api/health
```

### 📝 開發與生產環境

**開發環境運行:**
```bash
cd backend
python main.py
```

**生產環境 (Docker):**
```bash
cd backend
docker build -t news-collector .
docker run -p 8000:8000 --env-file .env news-collector
```

### 故障排除

**常見問題:**

1. **構建失敗:** 檢查 Dockerfile 語法和依賴
2. **啟動失敗:** 檢查環境變數和資料庫連接
3. **郵件發送失敗:** 驗證 SMTP 設定和應用程式密碼

**查看日誌:**
- 在 Render Dashboard 的 Logs 頁面查看詳細錯誤訊息

---

## 📝 注意事項

- Render 免費方案有一些限制（睡眠模式、運算時間等）
- 建議升級到付費方案以獲得更好的效能
- 定期備份資料庫資料
- 本專案使用現有的 Dockerfile，無需額外配置
