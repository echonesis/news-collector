# Gmail 電子郵件設定指南

## 🔧 修復 "Connection unexpectedly closed" 問題

您遇到的問題是因為需要設定 Gmail 應用程式密碼才能發送電子郵件。

## 📧 設定步驟

### 1. 啟用兩步驟驗證
1. 前往 [Google 帳戶設定](https://myaccount.google.com/)
2. 點選「安全性」
3. 在「登入 Google」下方，點選「兩步驟驗證」
4. 按照指示啟用兩步驟驗證

### 2. 產生應用程式密碼
1. 在「安全性」頁面中，找到「應用程式密碼」
2. 如果沒有看到此選項，請確認已啟用兩步驟驗證
3. 點選「應用程式密碼」
4. 選擇「郵件」和您的裝置
5. 產生密碼並複製 16 字符的密碼

### 3. 更新 .env 文件
將產生的應用程式密碼填入 `.env` 文件：

```bash
SENDER_EMAIL=echonesis@gmail.com
SENDER_PASSWORD=your-16-character-app-password
```

## 🧪 測試設定

設定完成後，運行測試腳本：

```bash
cd /Users/cfh00895945/workspaces/test_lab/test_copilot
source .venv/bin/activate
cd news-collector/backend
python test_send_email.py
```

## 🔍 疑難排解

### 常見問題：

1. **535 Authentication failed**
   - 確認已啟用兩步驟驗證
   - 使用應用程式密碼，不是一般 Google 密碼
   - 檢查應用程式密碼是否正確複製

2. **Connection unexpectedly closed**
   - 通常是認證問題導致連接被中斷
   - 檢查網路連接
   - 確認防火牆設定

3. **SMTP 連接超時**
   - 檢查網路連接
   - 確認 SMTP 伺服器設定正確（smtp.gmail.com:587）

## 📝 目前設定狀況

- ✅ 編碼問題已修復
- ✅ SMTP 連接設定正確
- ⚠️  需要設定有效的 Gmail 應用程式密碼

設定完應用程式密碼後，電子報功能就能正常運作了！
