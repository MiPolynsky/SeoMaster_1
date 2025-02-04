from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import User, PageMetadata
import admin

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Успешный вход в систему!', 'success')
            return redirect(url_for('admin.index'))
        flash('Неверное имя пользователя или пароль', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))

@app.route('/')
def index():
    metadata = PageMetadata.query.filter_by(url_path='/').first()
    services = [
        {
            'title': 'Аудит сайта',
            'description': 'Комплексный анализ вашего сайта для выявления технических ошибок и потенциала роста',
            'icon': 'fa-magnifying-glass-chart',
            'url': '/service/audit'
        },
        {
            'title': 'Семантическое ядро',
            'description': 'Подбор ключевых слов и фраз для эффективного продвижения вашего сайта',
            'icon': 'fa-sitemap',
            'url': '/service/semantic'
        },
        {
            'title': 'Копирайтинг',
            'description': 'Создание уникального контента, оптимизированного под поисковые системы',
            'icon': 'fa-pen-fancy',
            'url': '/service/copywriting'
        }
    ]
    return render_template('index.html', services=services, metadata=metadata)

@app.route('/services')
def services():
    metadata = PageMetadata.query.filter_by(url_path='/services').first()
    all_services = [
        {
            'title': 'Аудит сайта',
            'description': 'Комплексный анализ вашего сайта для выявления технических ошибок и потенциала роста',
            'icon': 'fa-magnifying-glass-chart',
            'url': '/service/audit'
        },
        {
            'title': 'Семантическое ядро',
            'description': 'Подбор ключевых слов и фраз для эффективного продвижения вашего сайта',
            'icon': 'fa-sitemap',
            'url': '/service/semantic'
        },
        {
            'title': 'Копирайтинг',
            'description': 'Создание уникального контента, оптимизированного под поисковые системы',
            'icon': 'fa-pen-fancy',
            'url': '/service/copywriting'
        },
        {
            'title': 'Продвижение интернет-магазинов',
            'description': 'Специализированное SEO для электронной коммерции',
            'icon': 'fa-cart-shopping',
            'url': '/service/ecommerce'
        },
        {
            'title': 'Продвижение сайтов-визиток',
            'description': 'Оптимизация небольших корпоративных сайтов',
            'icon': 'fa-building',
            'url': '/service/business'
        },
        {
            'title': 'Продвижение одностраничных сайтов',
            'description': 'SEO-оптимизация лендингов для максимальной конверсии',
            'icon': 'fa-file',
            'url': '/service/landing'
        }
    ]
    return render_template('services.html', services=all_services, metadata=metadata)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/service/audit')
def service_audit():
    return render_template('service_audit.html')

@app.route('/service/semantic')
def service_semantic():
    return render_template('service_semantic.html')

@app.route('/service/copywriting')
def service_copywriting():
    return render_template('service_copywriting.html')

@app.route('/service/ecommerce')
def service_ecommerce():
    return render_template('service_ecommerce.html')

@app.route('/service/business')
def service_business():
    return render_template('service_business.html')

@app.route('/service/landing')
def service_landing():
    return render_template('service_landing.html')

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin_user = User(username='admin')
        admin_user.set_password('admin')
        db.session.add(admin_user)
        db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)