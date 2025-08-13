# News Collector 文檔索引

歡迎來到News Collector的完整文檔！這裡包含了所有你需要了解的系統資訊。

## 📖 文檔導覽

### 🚀 [快速開始 - README](../README.md)
系統概覽、核心特性和快速安裝指南。

### 🔧 [API 文檔 - api.md](api.md)
完整的API端點說明，包含：
- 所有API端點詳細說明
- 請求/回應範例
- 錯誤處理說明
- 使用範例和測試命令

### 🏗️ [系統架構 - architecture.md](architecture.md)
深入的技術架構說明，包含：
- 系統整體架構圖
- 核心機制詳解（智能歡迎、排程、新聞收集）
- 資料模型設計
- 工作流程說明
- 擴展性設計

### 🚀 [部署指南 - deployment.md](deployment.md)
從開發到生產的完整部署流程，包含：
- 環境需求和安裝步驟
- 詳細的使用指南
- 高級配置（Gmail SMTP、資料庫等）
- 監控與維護
- 故障排除
- 生產環境部署

### 💻 [開發指南 - development.md](development.md)
開發環境設置和專案擴展指南。

## 🎯 根據使用場景選擇文檔

### 👨‍💻 **我是開發者**
1. 先閱讀 [README](../README.md) 了解系統概覽
2. 查看 [架構文檔](architecture.md) 理解系統設計
3. 參考 [API文檔](api.md) 進行開發
4. 使用 [部署指南](deployment.md) 設置開發環境

### 🚀 **我要部署系統**
1. 閱讀 [README](../README.md) 了解系統需求
2. 跟隨 [部署指南](deployment.md) 逐步部署
3. 參考 [API文檔](api.md) 進行測試
4. 查看 [架構文檔](architecture.md) 了解系統機制

### 🔍 **我要了解系統原理**
1. 從 [架構文檔](architecture.md) 開始深入了解
2. 查看 [API文檔](api.md) 了解功能實現
3. 參考 [部署指南](deployment.md) 了解實際運作

### 🐛 **我遇到問題**
1. 查看 [部署指南](deployment.md) 的故障排除章節
2. 檢查 [API文檔](api.md) 的錯誤處理說明
3. 參考 [架構文檔](architecture.md) 了解系統機制

## 📝 核心概念快速索引

### 智能歡迎機制
- **文檔位置**: [architecture.md - 智能歡迎系統](architecture.md#1-智能歡迎系統)
- **API測試**: [api.md - 建立新訂閱](api.md#2-建立新訂閱)

### 新聞收集
- **實現原理**: [architecture.md - 新聞收集機制](architecture.md#2-新聞收集機制)
- **API測試**: [api.md - 測試新聞收集](api.md#5-測試新聞收集)

### 排程系統
- **機制說明**: [architecture.md - 智能排程系統](architecture.md#3-智能排程系統)
- **API測試**: [api.md - 測試排程功能](api.md#9-測試排程功能)

### 電子報發送
- **實現方式**: [architecture.md - 電子報生成機制](architecture.md#4-電子報生成機制)
- **配置說明**: [deployment.md - Gmail SMTP 設置](deployment.md#gmail-smtp-設置)

## 🔗 快速鏈接

### 常用API測試命令
```bash
# 健康檢查
curl http://localhost:8000/api/health

# 建立訂閱
curl -X POST http://localhost:8000/api/subscriptions \
  -H "Content-Type: application/json" \
  -d '{"topic": "AI", "email": "test@example.com", "frequency": "daily"}'

# 檢查訂閱狀態
curl http://localhost:8000/api/subscription-status

# 測試新聞收集
curl -X POST http://localhost:8000/api/test-news-collection \
  -H "Content-Type: application/json" \
  -d '{"topic": "AI", "limit": 3}'
```

### 重要檔案位置
- 主要配置：`backend/.env`
- 服務入口：`backend/main.py`
- Chrome Extension：`extension/manifest.json`
- API路由：`backend/src/api/__init__.py`
- 排程服務：`backend/src/services/scheduler_service.py`

## 📞 技術支援

如果文檔中沒有解答你的問題：
1. 檢查系統日誌和錯誤訊息
2. 參考故障排除指南
3. 查看具體的錯誤代碼和API回應
4. 開啟GitHub Issue提供詳細資訊

---

📚 **建議**: 如果是第一次使用，建議按照「開發者」路線閱讀文檔，即使你不是開發者，這樣能幫助你更好地理解系統運作原理。
