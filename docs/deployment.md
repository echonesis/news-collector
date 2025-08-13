# News Collector 部署與使用指南

## 快速開始

### 系統需求

- Python 3.8+
- Chrome 瀏覽器
- SQLite（內建）

### 安裝步驟

#### 1. 後端服務設置

```bash
# 克隆專案
git clone <repository-url>
cd news-collector

# 設置Python虛擬環境
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# 或
.venv\Scripts\activate     # Windows

# 安裝依賴
cd backend
pip install -r requirements.txt

# 設置環境變數
cp .env.example .env
# 編輯 .env 文件設置您的配置
```

#### 2. 環境配置

編輯 `backend/.env` 文件：

```bash
# Email 模式（開發建議使用mock）
EMAIL_MODE=mock

# 真實Email設定（生產環境使用）
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password

# 資料庫（SQLite預設）
DATABASE_URL=sqlite:///news_collector.db

# 安全密鑰
SECRET_KEY=your-random-secret-key
```

#### 3. 啟動後端服務

```bash
cd backend
python main.py
```

服務將在 `http://localhost:8000` 啟動。

#### 4. Chrome Extension 安裝

1. 開啟Chrome瀏覽器
2. 進入 `chrome://extensions/`
3. 開啟「開發者模式」
4. 點擊「載入未封裝項目」
5. 選擇 `extension` 資料夾

## 使用指南

### 基本使用流程

#### 1. 建立訂閱

使用Chrome Extension：
1. 點擊瀏覽器中的News Collector圖標
2. 填寫訂閱資訊：
   - 主題：如"AI 人工智慧"、"區塊鏈"等
   - 頻率：daily/weekly/monthly
   - Email：您的收件信箱
3. 點擊「訂閱」

**API方式**：
```bash
curl -X POST http://localhost:8000/api/subscriptions \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "AI",
    "email": "your-email@example.com",
    "frequency": "daily"
  }'
```

#### 2. 檢查訂閱狀態

```bash
# 查看所有訂閱
curl -X GET http://localhost:8000/api/subscriptions

# 查看訂閱狀態詳情
curl -X GET http://localhost:8000/api/subscription-status
```

#### 3. 手動觸發功能

```bash
# 手動收集新聞
curl -X POST http://localhost:8000/api/test-news-collection \
  -H "Content-Type: application/json" \
  -d '{"topic": "AI", "limit": 5}'

# 手動發送電子報
curl -X POST http://localhost:8000/api/send-newsletters

# 測試email發送
curl -X POST http://localhost:8000/api/test-email \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "topic": "AI"}'
```

## 高級配置

### Gmail SMTP 設置

如果要使用真實email發送功能：

1. **啟用2步驟驗證**：
   - 前往Google帳戶設定
   - 啟用2步驟驗證

2. **生成應用程式密碼**：
   - 在Google帳戶中選擇「應用程式密碼」
   - 選擇「郵件」和您的設備
   - 複製生成的16位密碼

3. **更新環境變數**：
   ```bash
   EMAIL_MODE=real
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SENDER_EMAIL=your-gmail@gmail.com
   SENDER_PASSWORD=your-16-digit-app-password
   ```

### 資料庫配置

預設使用SQLite，如需使用其他資料庫：

```bash
# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost/newsdb

# MySQL
DATABASE_URL=mysql://user:password@localhost/newsdb
```

## 監控與維護

### 檢查系統健康

```bash
# 健康檢查
curl -X GET http://localhost:8000/api/health

# 查看新聞收集情況
curl -X GET "http://localhost:8000/api/news?limit=10"
```

### 日誌檢查

- **後端日誌**：在終端查看Python服務輸出
- **Email日誌**：`backend/logs/` 目錄中的HTML文件（模擬模式）

### 資料庫管理

```bash
# 進入Python環境查看資料
python -c "
from main import app, db
from src.models import Subscription, NewsItem
with app.app_context():
    print('訂閱數量:', Subscription.query.count())
    print('新聞數量:', NewsItem.query.count())
"
```

## 故障排除

### 常見問題

#### 1. 服務無法啟動

**問題**：ModuleNotFoundError或ImportError

**解決**：
```bash
# 檢查虛擬環境
which python
pip list

# 重新安裝依賴
pip install -r requirements.txt

# 設置PYTHONPATH
export PYTHONPATH=$(pwd)
python main.py
```

#### 2. Chrome Extension無法載入

**問題**：manifest錯誤或權限問題

**解決**：
1. 檢查`manifest.json`語法
2. 確認所有檔案路徑正確
3. 重新載入extension

#### 3. 新聞收集失敗

**問題**：無法收集到新聞

**可能原因**：
- 網路連線問題
- RSS源無回應
- 中文主題可能需要英文關鍵字

**解決**：
```bash
# 測試網路連線
curl "https://news.google.com/rss/search?q=AI"

# 使用英文主題測試
curl -X POST http://localhost:8000/api/test-news-collection \
  -H "Content-Type: application/json" \
  -d '{"topic": "artificial intelligence", "limit": 3}'
```

#### 4. Email發送失敗

**問題**：SMTP認證失敗

**解決**：
1. 檢查Gmail應用程式密碼設定
2. 確認2步驟驗證已啟用
3. 測試SMTP設定：

```python
import smtplib
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('your-email@gmail.com', 'your-app-password')
    print("SMTP設定正確")
    server.quit()
except Exception as e:
    print(f"SMTP錯誤: {e}")
```

### 性能優化

#### 1. 資料庫優化

```python
# 新增索引提升查詢效能
with app.app_context():
    db.engine.execute('CREATE INDEX idx_news_topic ON news_items(topic)')
    db.engine.execute('CREATE INDEX idx_news_created ON news_items(created_at)')
```

#### 2. 新聞收集優化

- 調整收集頻率避免過度請求
- 實施緩存機制
- 新增更多新聞源

#### 3. Email發送優化

- 使用專業SMTP服務（如SendGrid）
- 實施發送頻率限制
- 新增退信處理機制

## 生產部署

### Docker 部署

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY backend/ .

RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python", "main.py"]
```

```bash
# 建立並運行
docker build -t news-collector .
docker run -p 8000:8000 news-collector
```

### Nginx 反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 系統服務設置

```bash
# 建立systemd服務文件
sudo nano /etc/systemd/system/news-collector.service
```

```ini
[Unit]
Description=News Collector Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/news-collector/backend
Environment=PATH=/path/to/.venv/bin
ExecStart=/path/to/.venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 啟用服務
sudo systemctl enable news-collector
sudo systemctl start news-collector
```

這個指南涵蓋了從開發到生產的完整部署流程，確保系統可以穩定運行。
