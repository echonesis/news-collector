# News Collector API 文檔

## 概覽

News Collector 是一個智能新聞訂閱系統，支持自動收集新聞並通過電子郵件發送給訂閱用戶。

## 基本信息

- **Base URL**: `http://localhost:8000`
- **API Version**: v1
- **Content-Type**: `application/json`

## API 端點

### 1. 健康檢查

檢查服務是否正常運行。

**端點**: `GET /api/health`

**回應範例**:
```json
{
  "status": "healthy",
  "timestamp": "2025-08-13T09:00:00.000000",
  "message": "News Collector API is running"
}
```

---

### 2. 建立新訂閱

建立新的新聞訂閱，支持智能歡迎功能。

**端點**: `POST /api/subscriptions`

**請求參數**:
```json
{
  "topic": "AI 人工智慧",
  "email": "user@example.com",
  "frequency": "daily"
}
```

**參數說明**:
- `topic` (string, 必填): 新聞主題
- `email` (string, 必填): 收件電子信箱
- `frequency` (string, 必填): 發送頻率，可選值: `daily`, `weekly`, `monthly`

**成功回應**:
```json
{
  "message": "訂閱建立成功",
  "subscription": {
    "id": 1,
    "topic": "AI 人工智慧",
    "email": "user@example.com",
    "frequency": "daily",
    "created_at": "2025-08-13T09:03:34.017392",
    "is_active": true,
    "last_sent": null
  },
  "welcome_action": {
    "action": "sent_welcome_email",
    "news_count": 3,
    "message": "立即發送歡迎email，包含現有新聞"
  }
}
```

**歡迎行為說明**:
- `sent_welcome_email`: 找到現有新聞，立即發送歡迎email
- `collected_and_sent`: 收集新新聞並發送歡迎email
- `wait_for_schedule`: 沒有新聞，等待下次排程

**錯誤回應**:
```json
{
  "error": "此主題訂閱已存在"
}
```

---

### 3. 取得訂閱列表

取得所有活躍的訂閱記錄。

**端點**: `GET /api/subscriptions`

**查詢參數**:
- `email` (string, 可選): 篩選特定email的訂閱

**回應範例**:
```json
{
  "subscriptions": [
    {
      "id": 1,
      "topic": "AI 人工智慧",
      "email": "user@example.com",
      "frequency": "daily",
      "created_at": "2025-08-13T09:03:34.017392",
      "is_active": true,
      "last_sent": "2025-08-13T10:00:00.000000"
    }
  ]
}
```

---

### 4. 取消訂閱

取消指定的訂閱（軟刪除）。

**端點**: `DELETE /api/subscriptions/{subscription_id}`

**路徑參數**:
- `subscription_id` (integer): 訂閱ID

**成功回應**:
```json
{
  "message": "訂閱已取消"
}
```

---

### 5. 測試新聞收集

手動觸發新聞收集功能，用於測試。

**端點**: `POST /api/test-news-collection`

**請求參數**:
```json
{
  "topic": "AI",
  "limit": 5
}
```

**參數說明**:
- `topic` (string, 必填): 新聞主題
- `limit` (integer, 可選): 收集數量限制，預設為5

**成功回應**:
```json
{
  "message": "成功收集 3 則新聞，儲存 3 則",
  "topic": "AI",
  "collected": 3,
  "saved": 3,
  "news_items": [
    {
      "title": "群聯推首款 aiDAPTIV+ AI PC，宏碁 華碩率先採用",
      "summary": "群聯推首款 aiDAPTIV+ AI PC...",
      "url": "https://news.example.com/article1",
      "source": "Google News",
      "topic": "AI",
      "published_at": "Wed, 13 Aug 2025 02:40:06 GMT"
    }
  ]
}
```

---

### 6. 查詢新聞記錄

取得已收集的新聞記錄。

**端點**: `GET /api/news`

**查詢參數**:
- `topic` (string, 可選): 篩選特定主題的新聞
- `limit` (integer, 可選): 限制返回數量，預設為10

**回應範例**:
```json
{
  "count": 3,
  "news_items": [
    {
      "id": 1,
      "title": "群聯推首款 aiDAPTIV+ AI PC，宏碁 華碩率先採用",
      "summary": "群聯推首款 aiDAPTIV+ AI PC...",
      "url": "https://news.example.com/article1",
      "source": "Google News",
      "topic": "AI",
      "published_at": "2025-08-13T02:40:06",
      "created_at": "2025-08-13T09:13:25.744654"
    }
  ]
}
```

---

### 7. 測試電子郵件發送

測試電子郵件發送功能。

**端點**: `POST /api/test-email`

**請求參數**:
```json
{
  "email": "test@example.com",
  "topic": "AI"
}
```

**參數說明**:
- `email` (string, 必填): 收件人email
- `topic` (string, 可選): 新聞主題，預設為"AI 人工智慧"

**成功回應**:
```json
{
  "message": "測試email已發送至 test@example.com",
  "topic": "AI",
  "news_count": 3
}
```

---

### 8. 手動發送電子報

手動觸發發送電子報給所有訂閱者。

**端點**: `POST /api/send-newsletters`

**回應範例**:
```json
{
  "message": "電子報發送完成",
  "total_subscriptions": 4,
  "sent": 2,
  "failed": 0
}
```

---

### 9. 測試排程功能

手動觸發排程檢查。

**端點**: `POST /api/test-scheduler`

**回應範例**:
```json
{
  "message": "排程檢查已完成",
  "timestamp": "2025-08-13T09:38:48.064103"
}
```

---

### 10. 檢查訂閱狀態

檢查所有訂閱的狀態和是否需要發送。

**端點**: `GET /api/subscription-status`

**回應範例**:
```json
{
  "total_subscriptions": 4,
  "subscriptions": [
    {
      "id": 1,
      "email": "user@example.com",
      "topic": "AI 人工智慧",
      "frequency": "daily",
      "last_sent": null,
      "should_send_now": true,
      "created_at": "2025-08-13T09:03:34.017392"
    },
    {
      "id": 2,
      "email": "user2@example.com",
      "topic": "AI",
      "frequency": "weekly",
      "last_sent": "2025-08-13T09:36:40.393799",
      "should_send_now": false,
      "created_at": "2025-08-13T09:30:49.180714"
    }
  ]
}
```

## 錯誤處理

所有API端點都會返回適當的HTTP狀態碼：

- `200`: 成功
- `201`: 創建成功
- `400`: 請求參數錯誤
- `404`: 資源不存在
- `409`: 資源衝突（如重複訂閱）
- `500`: 伺服器內部錯誤

錯誤回應格式：
```json
{
  "error": "錯誤描述訊息"
}
```

## 使用範例

### 建立訂閱並測試
```bash
# 1. 建立新訂閱
curl -X POST http://localhost:8000/api/subscriptions \
  -H "Content-Type: application/json" \
  -d '{"topic": "AI", "email": "user@example.com", "frequency": "daily"}'

# 2. 檢查訂閱狀態
curl -X GET http://localhost:8000/api/subscription-status

# 3. 手動觸發電子報
curl -X POST http://localhost:8000/api/send-newsletters

# 4. 測試新聞收集
curl -X POST http://localhost:8000/api/test-news-collection \
  -H "Content-Type: application/json" \
  -d '{"topic": "AI", "limit": 3}'
```
