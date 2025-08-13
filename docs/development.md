# News Collector 開發文件

## 專案架構

### Chrome Extension（前端管理介面）
- **位置**: `extension/`
- **功能**: 提供簡潔的訂閱管理介面
- **技術**: HTML, CSS, JavaScript (Manifest V3)

### 後端 API 服務
- **位置**: `backend/`
- **功能**: 新聞收集、電子報生成、排程任務
- **技術**: Flask, SQLAlchemy, APScheduler

## API 端點

### 訂閱管理
- `POST /api/subscriptions` - 建立新訂閱
- `GET /api/subscriptions` - 取得訂閱列表
- `DELETE /api/subscriptions/{id}` - 取消訂閱

### 系統
- `GET /api/health` - 健康檢查

## 資料模型

### Subscription（訂閱）
- topic: 主題
- email: 收件信箱
- frequency: 頻率（daily/weekly/monthly）
- is_active: 是否啟用
- last_sent: 最後發送時間

### NewsItem（新聞項目）
- title: 標題
- summary: 摘要
- url: 連結
- source: 來源
- topic: 主題

### Newsletter（電子報記錄）
- subscription_id: 訂閱 ID
- content: 內容摘要
- sent_at: 發送時間
- status: 狀態

## 部署指南

### 本地開發
1. 設定後端環境
2. 安裝 Chrome Extension
3. 設定 SMTP 郵件服務

### 生產環境
- 使用 Docker Compose 部署
- 設定環境變數
- 配置 SSL 憑證

## 維護要點

1. **小而美的設計原則**
   - 單一責任：每個模組專注特定功能
   - 最小依賴：避免過度設計
   - 容易擴展：模組化架構

2. **監控建議**
   - 定期檢查排程任務執行狀況
   - 監控郵件發送成功率
   - 追蹤訂閱數量變化

3. **安全考量**
   - API 端點加入適當驗證
   - 郵件密碼使用應用程式密碼
   - 定期更新依賴套件
