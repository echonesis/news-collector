import requests
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from src.models import NewsItem
from database import db

class NewsCollectorService:
    """新聞收集服務"""
    
    def __init__(self):
        self.sources = {
            'google_news_rss': 'https://news.google.com/rss/search?q={topic}&hl=zh-TW&gl=TW&ceid=TW:zh-Hant',
            'yahoo_news_rss': 'https://tw.news.yahoo.com/rss'
        }
    
    def collect_news(self, topic, limit=10):
        """收集指定主題的新聞"""
        news_items = []
        
        try:
            # 使用 Google News RSS
            google_news = self._fetch_google_news(topic, limit)
            news_items.extend(google_news)
            
            return news_items[:limit]
            
        except Exception as e:
            print(f"收集新聞時發生錯誤: {e}")
            return []
    
    def _fetch_google_news(self, topic, limit):
        """從 Google News RSS 取得新聞"""
        news_items = []
        
        try:
            url = self.sources['google_news_rss'].format(topic=topic)
            feed = feedparser.parse(url)
            
            for entry in feed.entries[:limit]:
                news_item = {
                    'title': entry.title,
                    'summary': getattr(entry, 'summary', '')[:500],
                    'url': entry.link,
                    'source': 'Google News',
                    'topic': topic,
                    'published_at': self._parse_date(getattr(entry, 'published', None))
                }
                news_items.append(news_item)
                
        except Exception as e:
            print(f"從 Google News 取得新聞失敗: {e}")
        
        return news_items
    
    def _parse_date(self, date_string):
        """解析日期字串"""
        if not date_string:
            return datetime.utcnow()
        
        try:
            # 嘗試解析 RSS 日期格式
            return datetime.strptime(date_string, '%a, %d %b %Y %H:%M:%S %Z')
        except:
            return datetime.utcnow()
    
    def save_news_items(self, news_items):
        """儲存新聞到資料庫"""
        saved_count = 0
        
        for item_data in news_items:
            try:
                # 檢查是否已存在
                existing = NewsItem.query.filter_by(
                    url=item_data['url'],
                    topic=item_data['topic']
                ).first()
                
                if not existing:
                    news_item = NewsItem(**item_data)
                    db.session.add(news_item)
                    saved_count += 1
            
            except Exception as e:
                print(f"儲存新聞項目失敗: {e}")
                continue
        
        try:
            db.session.commit()
            print(f"成功儲存 {saved_count} 則新聞")
        except Exception as e:
            db.session.rollback()
            print(f"儲存新聞到資料庫失敗: {e}")
        
        return saved_count
