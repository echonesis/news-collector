import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

class EmailService:
    """電子郵件服務"""
    
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL', '')
        self.sender_password = os.getenv('SENDER_PASSWORD', '')
    
    def send_newsletter(self, recipient_email, topic, news_items):
        """發送電子報"""
        try:
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
            
            # 發送郵件
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            print(f"電子報已發送至 {recipient_email}")
            return True
            
        except Exception as e:
            print(f"發送電子報失敗: {e}")
            return False
    
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
                        時間: {item.get('published_at', '').split('T')[0] if item.get('published_at') else '未知'}
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
