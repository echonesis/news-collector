from datetime import datetime
import os

class MockEmailService:
    """模擬電子郵件服務 - 用於測試"""
    
    def __init__(self):
        self.sent_emails = []
    
    def send_newsletter(self, recipient_email, topic, news_items):
        """模擬發送電子報"""
        try:
            # 記錄發送的email
            email_record = {
                'recipient': recipient_email,
                'topic': topic,
                'news_count': len(news_items),
                'sent_at': datetime.now().isoformat(),
                'content': self._generate_newsletter_html(topic, news_items)
            }
            
            self.sent_emails.append(email_record)
            
            print(f"📧 [模擬] 電子報已發送至 {recipient_email}")
            print(f"   主題: {topic}")
            print(f"   新聞數量: {len(news_items)}")
            
            # 儲存到文件以便檢查
            self._save_to_file(email_record)
            
            return True
            
        except Exception as e:
            print(f"[模擬] 發送電子報失敗: {e}")
            return False
    
    def _save_to_file(self, email_record):
        """儲存email內容到文件"""
        try:
            filename = f"sent_email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            filepath = os.path.join('logs', filename)
            
            # 確保logs目錄存在
            os.makedirs('logs', exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(email_record['content'])
            
            print(f"   📁 Email內容已儲存至: {filepath}")
            
        except Exception as e:
            print(f"   儲存email內容失敗: {e}")
    
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
                # 處理新聞項目（可能是字典或對象）
                if isinstance(item, dict):
                    title = item.get('title', '無標題')
                    url = item.get('url', '#')
                    summary = item.get('summary', '')
                    source = item.get('source', '未知')
                    published_at = item.get('published_at', '')
                else:
                    title = getattr(item, 'title', '無標題')
                    url = getattr(item, 'url', '#')
                    summary = getattr(item, 'summary', '')
                    source = getattr(item, 'source', '未知')
                    published_at = getattr(item, 'published_at', '')
                
                # 清理summary中的HTML標籤
                import re
                clean_summary = re.sub('<.*?>', '', summary)[:200] + '...' if len(summary) > 200 else summary
                
                html += f"""
                <div class="news-item">
                    <div class="news-title">
                        <a href="{url}" target="_blank">{title}</a>
                    </div>
                    <div class="news-summary">{clean_summary}</div>
                    <div class="news-meta">
                        來源: {source} | 
                        時間: {str(published_at).split('T')[0] if published_at else '未知'}
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
