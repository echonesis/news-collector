from database import db
from datetime import datetime

class Subscription(db.Model):
    """訂閱模型"""
    __tablename__ = 'subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    frequency = db.Column(db.String(20), nullable=False)  # daily, weekly, monthly
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    last_sent = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<Subscription {self.topic} - {self.email}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'topic': self.topic,
            'email': self.email,
            'frequency': self.frequency,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active,
            'last_sent': self.last_sent.isoformat() if self.last_sent else None
        }

class NewsItem(db.Model):
    """新聞條目模型"""
    __tablename__ = 'news_items'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    summary = db.Column(db.Text, nullable=True)
    url = db.Column(db.String(1000), nullable=False)
    source = db.Column(db.String(100), nullable=True)
    topic = db.Column(db.String(200), nullable=False)
    published_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<NewsItem {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'summary': self.summary,
            'url': self.url,
            'source': self.source,
            'topic': self.topic,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Newsletter(db.Model):
    """電子報模型"""
    __tablename__ = 'newsletters'
    
    id = db.Column(db.Integer, primary_key=True)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscriptions.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='sent')  # sent, failed
    
    subscription = db.relationship('Subscription', backref='newsletters')
    
    def __repr__(self):
        return f'<Newsletter {self.id} - {self.subscription.topic}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'subscription_id': self.subscription_id,
            'content': self.content,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'status': self.status
        }
