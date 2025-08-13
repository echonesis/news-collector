# News Collector 系統架構與機制

## 系統概覽

News Collector 是一個智能新聞訂閱系統，包含以下核心組件：

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Chrome Extension│    │   Backend API   │    │  News Sources   │
│                 │    │                 │    │                 │
│ • 訂閱管理UI    │───▶│ • 訂閱管理      │───▶│ • Google News   │
│ • 用戶介面      │    │ • 新聞收集      │    │ • RSS Feeds     │
│                 │    │ • 電子報發送    │    │                 │
└─────────────────┘    │ • 排程系統      │    └─────────────────┘
                       └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │    Database     │
                       │                 │
                       │ • 訂閱記錄      │
                       │ • 新聞資料      │
                       │ • 發送記錄      │
                       └─────────────────┘
```

## 核心機制

### 1. 智能歡迎系統

當用戶建立新訂閱時，系統會執行智能歡迎邏輯：

```python
def handle_new_subscription(subscription):
    # 1. 檢查是否已有該主題的新聞（最近7天）
    existing_news = check_existing_news(subscription.topic)
    
    if existing_news:
        # 2a. 有現有新聞 -> 立即發送歡迎email
        send_welcome_email(subscription, existing_news)
        return "sent_welcome_email"
    else:
        # 2b. 沒有現有新聞 -> 嘗試收集新聞
        collected_news = collect_news(subscription.topic)
        
        if collected_news:
            # 3a. 收集到新聞 -> 發送歡迎email
            send_welcome_email(subscription, collected_news)
            return "collected_and_sent"
        else:
            # 3b. 沒有收集到新聞 -> 等待下次排程
            return "wait_for_schedule"
```

**行為說明**：
- **立即回饋**：用戶訂閱後立即獲得相關新聞
- **智能收集**：自動嘗試為新主題收集新聞
- **避免空email**：確保用戶不會收到空的電子報

### 2. 新聞收集機制

系統使用RSS源進行新聞收集：

```python
class NewsCollectorService:
    def __init__(self):
        self.sources = {
            'google_news_rss': 'https://news.google.com/rss/search?q={topic}&hl=zh-TW&gl=TW&ceid=TW:zh-Hant'
        }
    
    def collect_news(self, topic, limit=10):
        # 1. 構建RSS URL
        url = self.sources['google_news_rss'].format(topic=topic)
        
        # 2. 解析RSS feed
        feed = feedparser.parse(url)
        
        # 3. 提取新聞資訊
        news_items = []
        for entry in feed.entries[:limit]:
            news_item = {
                'title': entry.title,
                'summary': entry.summary,
                'url': entry.link,
                'source': 'Google News',
                'topic': topic,
                'published_at': parse_date(entry.published)
            }
            news_items.append(news_item)
        
        return news_items
```

**特點**：
- **多源支持**：可擴展支持多個新聞源
- **去重機制**：避免重複儲存相同新聞
- **主題相關**：根據訂閱主題精準收集

### 3. 智能排程系統

系統使用APScheduler實現智能排程：

```python
def setup_scheduled_jobs(scheduler):
    # 每小時檢查一次是否有需要發送的電子報
    scheduler.add_job(
        func=check_and_send_newsletters,
        trigger='interval',
        hours=1,
        id='newsletter_check'
    )

def should_send_newsletter(subscription, now):
    if not subscription.last_sent:
        return True  # 從未發送過
    
    time_diff = now - subscription.last_sent
    frequency_hours = {
        'daily': 24,
        'weekly': 168,   # 7 * 24
        'monthly': 720   # 30 * 24
    }
    
    required_hours = frequency_hours.get(subscription.frequency, 24)
    return time_diff.total_seconds() >= required_hours * 3600
```

**邏輯特點**：
- **頻率控制**：嚴格按照用戶設定的頻率發送
- **避免重複**：已發送的訂閱不會重複發送
- **靈活調整**：支持daily/weekly/monthly三種頻率

### 4. 電子報生成機制

系統支持兩種email服務模式：

#### 模擬模式（開發/測試）
```python
class MockEmailService:
    def send_newsletter(self, recipient_email, topic, news_items):
        # 1. 生成HTML格式電子報
        html_content = self._generate_newsletter_html(topic, news_items)
        
        # 2. 儲存到本地文件供檢查
        self._save_to_file(html_content)
        
        # 3. 記錄發送日誌
        print(f"📧 [模擬] 電子報已發送至 {recipient_email}")
        return True
```

#### 真實模式（生產環境）
```python
class EmailService:
    def send_newsletter(self, recipient_email, topic, news_items):
        # 1. 使用SMTP發送真實email
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
        return True
```

### 5. 資料模型設計

#### 訂閱模型（Subscription）
```python
class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(200), nullable=False)      # 主題
    email = db.Column(db.String(120), nullable=False)      # 收件信箱
    frequency = db.Column(db.String(20), nullable=False)   # 頻率
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)        # 是否啟用
    last_sent = db.Column(db.DateTime, nullable=True)      # 最後發送時間
```

#### 新聞模型（NewsItem）
```python
class NewsItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)      # 標題
    summary = db.Column(db.Text, nullable=True)            # 摘要
    url = db.Column(db.String(1000), nullable=False)       # 連結
    source = db.Column(db.String(100), nullable=True)      # 來源
    topic = db.Column(db.String(200), nullable=False)      # 主題
    published_at = db.Column(db.DateTime, nullable=True)   # 發布時間
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

## 環境配置

### 環境變數
```bash
# Email 模式選擇
EMAIL_MODE=mock          # mock: 模擬模式, real: 真實模式

# SMTP 設定（真實模式時使用）
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password

# 資料庫設定
DATABASE_URL=sqlite:///news_collector.db

# 安全密鑰
SECRET_KEY=your-secret-key-here
```

### Chrome Extension 設定
```json
{
  "manifest_version": 3,
  "name": "News Collector Manager",
  "permissions": ["storage", "activeTab"],
  "host_permissions": ["http://localhost:8000/*"],
  "action": {
    "default_popup": "popup/popup.html"
  },
  "background": {
    "service_worker": "background/background.js"
  }
}
```

## 工作流程

### 典型使用流程

1. **用戶訂閱**
   ```
   用戶在Chrome Extension中填寫訂閱資訊
   ↓
   系統檢查是否有現有新聞
   ↓
   立即發送歡迎email或等待排程
   ```

2. **新聞收集**
   ```
   排程系統每小時檢查
   ↓
   識別需要發送的訂閱
   ↓
   收集相關新聞
   ↓
   生成並發送電子報
   ```

3. **電子報發送**
   ```
   收集新聞 → 生成HTML → 發送email → 更新記錄
   ```

### 錯誤處理機制

- **新聞收集失敗**：記錄錯誤，跳過該次發送
- **Email發送失敗**：記錄失敗狀態，不更新last_sent時間
- **資料庫錯誤**：回滾事務，返回錯誤訊息
- **RSS源無回應**：使用預設空結果，避免系統崩潰

## 擴展性設計

### 新增新聞源
```python
# 在NewsCollectorService中新增源
self.sources = {
    'google_news_rss': 'https://news.google.com/rss/...',
    'new_source': 'https://new-source.com/api/...'
}
```

### 新增發送頻率
```python
# 在scheduler_service.py中新增頻率
frequency_hours = {
    'daily': 24,
    'weekly': 168,
    'monthly': 720,
    'hourly': 1,     # 新增每小時
    'yearly': 8760   # 新增每年
}
```

### 新增通知方式
```python
# 可擴展支持SMS、Slack等通知方式
class NotificationService:
    def send_sms(self, phone, content): pass
    def send_slack(self, webhook, content): pass
```

這個架構設計確保了系統的可擴展性、穩定性和用戶體驗。
