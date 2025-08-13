# 安全環境變數設定指南

## 本地開發環境

### 1. 複製範本檔案
```bash
cp .env.example .env
```

### 2. 生成安全的 SECRET_KEY
```bash
# 方法 1: 使用 openssl
openssl rand -base64 32

# 方法 2: 使用 Python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. 設定 Gmail SMTP (如需真實發送)
1. 前往 Google 帳戶設定 > 安全性
2. 啟用「兩步驟驗證」
3. 產生「應用程式密碼」
4. 將應用程式密碼填入 `SENDER_PASSWORD`

## 生產環境部署

### GitHub Actions 秘密變數
在 GitHub repository 設定中加入以下 Secrets：
- `SECRET_KEY`
- `SENDER_EMAIL`
- `SENDER_PASSWORD`
- `SMTP_SERVER`
- `SMTP_PORT`

### Docker 部署
```bash
# 使用環境變數啟動
docker run -e SECRET_KEY="your-secret" \
           -e SENDER_EMAIL="your-email" \
           -e SENDER_PASSWORD="your-password" \
           your-app-image
```

### 系統環境變數
```bash
# 設定系統環境變數
export SECRET_KEY="your-generated-secret-key"
export SENDER_EMAIL="your-email@gmail.com"
export SENDER_PASSWORD="your-app-password"
```

## 安全檢查清單

- [ ] `.env` 檔案已加入 `.gitignore`
- [ ] 使用強隨機密碼作為 `SECRET_KEY`
- [ ] Gmail 使用應用程式密碼而非帳戶密碼
- [ ] 生產環境使用系統環境變數或 GitHub Secrets
- [ ] 定期更新密碼和密鑰
- [ ] 不在程式碼中硬編碼任何敏感資訊

## 環境變數優先順序

應用程式會按以下順序尋找設定：
1. 系統環境變數 (最高優先級)
2. `.env` 檔案
3. 程式碼中的預設值 (最低優先級)

這樣設計可確保生產環境可以覆蓋本地設定。
