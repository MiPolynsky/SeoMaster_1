from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
import os
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from models import User, PageMetadata, Feedback
import admin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def init_metadata():
    if PageMetadata.query.count() == 0:
        initial_metadata = [
            {
                'url_path': '/',
                'title': 'SEO Услуги - Главная',
                'description': 'Профессиональное SEO продвижение сайтов. Увеличьте видимость вашего сайта в поисковых системах.',
                'h1': 'Профессиональное SEO продвижение'
            },
            {
                'url_path': '/services',
                'title': 'SEO Услуги - Наши услуги',
                'description': 'Полный спектр SEO услуг для вашего бизнеса. От аудита до продвижения.',
                'h1': 'Все услуги'
            },
            {
                'url_path': '/contact',
                'title': 'SEO Услуги - Контакты',
                'description': 'Свяжитесь с нами для консультации по SEO продвижению вашего сайта.',
                'h1': 'Наши контакты'
            },
            {
                'url_path': '/service/audit',
                'title': 'SEO Услуги - Аудит сайта',
                'description': 'Профессиональный аудит сайта для выявления всех ошибок и потенциала роста.',
                'h1': 'Аудит сайта'
            },
            {
                'url_path': '/service/semantic',
                'title': 'SEO Услуги - Семантическое ядро',
                'description': 'Разработка эффективного семантического ядра для вашего сайта.',
                'h1': 'Разработка семантического ядра'
            },
            {
                'url_path': '/service/copywriting',
                'title': 'SEO Услуги - Копирайтинг',
                'description': 'Профессиональный SEO-копирайтинг для вашего сайта.',
                'h1': 'SEO-копирайтинг'
            },
            {
                'url_path': '/service/ecommerce',
                'title': 'SEO Услуги - Продвижение интернет-магазинов',
                'description': 'Специализированное SEO-продвижение для интернет-магазинов.',
                'h1': 'Продвижение интернет-магазинов'
            },
            {
                'url_path': '/service/business',
                'title': 'SEO Услуги - Продвижение сайтов-визиток',
                'description': 'Эффективное продвижение сайтов-визиток и корпоративных сайтов.',
                'h1': 'Продвижение сайтов-визиток'
            },
            {
                'url_path': '/service/landing',
                'title': 'SEO Услуги - Продвижение одностраничных сайтов',
                'description': 'SEO-продвижение лендингов и одностраничных сайтов.',
                'h1': 'Продвижение одностраничных сайтов'
            }
        ]

        for metadata in initial_metadata:
            page_metadata = PageMetadata(**metadata)
            db.session.add(page_metadata)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error initializing metadata: {e}")

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

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    metadata = PageMetadata.query.filter_by(url_path='/contact').first()
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        if not all([name, email, subject, message]):
            flash('Пожалуйста, заполните все поля формы', 'error')
            return redirect(url_for('contact'))

        feedback = Feedback(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        try:
            db.session.add(feedback)
            db.session.commit()
            flash('Спасибо за ваше сообщение! Мы свяжемся с вами в ближайшее время.', 'success')
            return redirect(url_for('contact'))
        except Exception as e:
            db.session.rollback()
            flash('Произошла ошибка при отправке сообщения. Пожалуйста, попробуйте позже.', 'error')
            return redirect(url_for('contact'))

    return render_template('contact.html', metadata=metadata)

@app.route('/service/audit')
def service_audit():
    metadata = PageMetadata.query.filter_by(url_path='/service/audit').first()
    return render_template('service_audit.html', metadata=metadata)

@app.route('/service/semantic')
def service_semantic():
    metadata = PageMetadata.query.filter_by(url_path='/service/semantic').first()
    return render_template('service_semantic.html', metadata=metadata)

@app.route('/service/copywriting')
def service_copywriting():
    metadata = PageMetadata.query.filter_by(url_path='/service/copywriting').first()
    return render_template('service_copywriting.html', metadata=metadata)

@app.route('/service/ecommerce')
def service_ecommerce():
    metadata = PageMetadata.query.filter_by(url_path='/service/ecommerce').first()
    return render_template('service_ecommerce.html', metadata=metadata)

@app.route('/service/business')
def service_business():
    metadata = PageMetadata.query.filter_by(url_path='/service/business').first()
    return render_template('service_business.html', metadata=metadata)

@app.route('/service/landing')
def service_landing():
    metadata = PageMetadata.query.filter_by(url_path='/service/landing').first()
    return render_template('service_landing.html', metadata=metadata)

with app.app_context():
    db.create_all()
    init_metadata()  # Initialize metadata after tables are created

    # Create admin user if it doesn't exist
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        admin_user = User(username='admin')
        admin_user.set_password('admin')
        db.session.add(admin_user)
        db.session.commit()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)