from enum import unique
from turtle import title
from FlaskBlogApp import db
from datetime import datetime
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(36), nullable=False)
    profile_image = db.Column(db.String(30), default='default_profile_image.jpg')
    articles = db.relationship('Article', backref='author', lazy=True) # Article - relationship with the model not the table
    def __repr__(self):
        return f"{self.username}: {self.email}"

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_title = db.Column(db.String(50), nullable=False)
    article_body = db.Column(db.Text(), nullable=False)
    article_image = db.Column(db.String(30), default='default_article_image.jpg', nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # user.id of the table not of the class

    def __repr__(self):
        return f"{self.date_created}: {self.article_title}"

    
