from database import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class PageMetadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_path = db.Column(db.String(128), unique=True, nullable=False)
    title = db.Column(db.String(128))
    description = db.Column(db.String(256))
    h1 = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    website_url = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='new')

class IndustryPage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    industry_code = db.Column(db.String(50), unique=True, nullable=False)  # dentistry, furniture, etc
    title = db.Column(db.String(128))
    description = db.Column(db.String(256))
    h1 = db.Column(db.String(128))
    seo_text = db.Column(db.Text)
    icon = db.Column(db.String(50))  # FontAwesome icon class
    name = db.Column(db.String(100))  # Display name
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())