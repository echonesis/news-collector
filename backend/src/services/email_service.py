import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
import socket
import time

class EmailService:
    """電子郵件服務"""
    
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL', '')
        self.sender_password = os.getenv('SENDER_PASSWORD', '')
        self.timeout = 30  # 設定超時時間
        self.max_retries = 3  # 最大重試次數
    
    def send_newsletter(self, recipient_email, topic, news_items):
        """發送電子報"""
        for attempt in range(self.max_retries):
            try:
                # 驗證配置
                if not self.sender_email or not self.sender_password:
                    raise ValueError("未設置發送者電子郵件或密碼")
                
                # 建立郵件內容
                subject = f"📰 {topic} - 新聞電子報 ({datetime.now().strftime('%Y-%m-%d')})"
                html_content = self._generate_newsletter_html(topic, news_items)
                
                # 建立郵件
                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = self.sender_email
                msg['To'] = recipient_email
                
                # 添加 HTML 內容
                html_part = MIMEText(html_content, 'html', 'utf-8')
                msg.attach(html_part)
                
                # 發送郵件 - 增強錯誤處理和重試機制
                success = self._send_email_with_retry(msg)
                
                if success:
                    print(f"電子報已發送至 {recipient_email}")
                    return True
                else:
                    print(f"第 {attempt + 1} 次嘗試發送失敗")
                    if attempt < self.max_retries - 1:
                        time.sleep(2 ** attempt)  # 指數退避延遲
                        continue
                
            except ValueError as e:
                print(f"配置錯誤: {e}")
                return False
            except Exception as e:
                print(f"第 {attempt + 1} 次發送電子報失敗: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # 指數退避延遲
                    continue
        
        print(f"經過 {self.max_retries} 次嘗試後發送失敗")
        return False
    
    def _send_email_with_retry(self, msg):
        """使用重試機制發送郵件"""
        try:
            # 建立 SMTP 連接並設定超時
            server = smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=self.timeout)
            
            try:
                # 啟用除錯 (生產環境可關閉)
                if os.getenv('DEBUG', 'False').lower() == 'true':
                    server.set_debuglevel(1)
                
                # 啟動 TLS 加密
                server.starttls()
                
                # 登入 SMTP 伺服器
                server.login(self.sender_email, self.sender_password)
                
                # 發送郵件
                server.send_message(msg)
                
                print("SMTP 連接成功，郵件已發送")
                return True
                
            finally:
                # 確保連接被正確關閉
                try:
                    server.quit()
                except:
                    server.close()
                    
        except smtplib.SMTPAuthenticationError as e:
            error_msg = f"SMTP authentication failed: {str(e)}"
            print(error_msg.encode('utf-8', errors='ignore').decode('utf-8'))
            print("Please check SENDER_EMAIL and SENDER_PASSWORD settings")
            return False
            
        except smtplib.SMTPConnectError as e:
            error_msg = f"SMTP connection failed: {str(e)}"
            print(error_msg.encode('utf-8', errors='ignore').decode('utf-8'))
            print(f"Cannot connect to {self.smtp_server}:{self.smtp_port}")
            return False
            
        except smtplib.SMTPServerDisconnected as e:
            error_msg = f"SMTP server disconnected unexpectedly: {str(e)}"
            print(error_msg.encode('utf-8', errors='ignore').decode('utf-8'))
            return False
            
        except socket.timeout as e:
            error_msg = f"SMTP connection timeout: {str(e)}"
            print(error_msg.encode('utf-8', errors='ignore').decode('utf-8'))
            return False
            
        except Exception as e:
            error_msg = f"SMTP send failed: {str(e)}"
            print(error_msg.encode('utf-8', errors='ignore').decode('utf-8'))
            return False
    
    def test_connection(self):
        """測試 SMTP 連接配置"""
        try:
            if not self.sender_email or not self.sender_password:
                return False, "Email or password not configured"
            
            # 測試 SMTP 連接
            server = smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=self.timeout)
            
            try:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.quit()
                return True, "SMTP connection test successful"
                
            except smtplib.SMTPAuthenticationError as e:
                return False, f"SMTP authentication failed: {str(e)}"
            except smtplib.SMTPConnectError as e:
                return False, f"Cannot connect to SMTP server {self.smtp_server}:{self.smtp_port} - {str(e)}"
            except Exception as e:
                return False, f"SMTP connection test failed: {str(e)}"
            finally:
                try:
                    server.quit()
                except:
                    pass
                    
        except Exception as e:
            return False, f"Connection test error: {str(e)}"
    
    def _generate_newsletter_html(self, topic, news_items):
        """產生電子報 HTML 內容"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .header {{ background: linear-gradient(135deg, #007cff, #0056cc); color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .news-item {{ border-bottom: 1px solid #eee; padding: 15px 0; }}
                .news-item:last-child {{ border-bottom: none; }}
                .news-title {{ font-size: 16px; font-weight: 600; margin-bottom: 8px; }}
                .news-title a {{ color: #007cff; text-decoration: none; }}
                .news-title a:hover {{ text-decoration: underline; }}
                .news-summary {{ color: #666; font-size: 14px; line-height: 1.5; margin-bottom: 8px; }}
                .news-meta {{ font-size: 12px; color: #999; }}
                .footer {{ background-color: #f8f9fa; padding: 15px; text-align: center; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📰 {topic}</h1>
                    <p>新聞電子報 - {datetime.now().strftime('%Y年%m月%d日')}</p>
                </div>
                <div class="content">
        """
        
        if not news_items:
            html += "<p>今日暫無相關新聞。</p>"
        else:
            for item in news_items:
                html += f"""
                <div class="news-item">
                    <div class="news-title">
                        <a href="{item.get('url', '#')}" target="_blank">{item.get('title', '無標題')}</a>
                    </div>
                    <div class="news-summary">{item.get('summary', '')}</div>
                    <div class="news-meta">
                        來源: {item.get('source', '未知')} | 
                        時間: {str(item.get('published_at', '')).split('T')[0] if item.get('published_at') else '未知'}
                    </div>
                </div>
                """
        
        html += f"""
                </div>
                <div class="footer">
                    <p>此電子報由 News Collector 自動產生</p>
                    <p>如不想繼續收到此電子報，請聯繫管理員</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
