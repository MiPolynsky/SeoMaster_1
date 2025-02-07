from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, Response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
import os
from datetime import datetime
import xml.etree.ElementTree as ET
from database import db
from models import User, PageMetadata, Feedback, IndustryPage

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

@app.before_request
def redirect_to_domain():
    if request.headers.get('Host') == 'good-seo.replit.app':
        url = request.url.replace('good-seo.replit.app', 'good-seo.online', 1)
        return redirect(url, code=301)

@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt')

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

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

    if IndustryPage.query.count() == 0:
        industries = [
            {
                'industry_code': 'dentistry',
                'name': 'Стоматология',
                'title': 'SEO продвижение стоматологии | Раскрутка сайта стоматологической клиники',
                'description': 'Профессиональное SEO продвижение сайтов стоматологических клиник. Увеличение целевого трафика и привлечение новых пациентов.',
                'h1': 'SEO продвижение стоматологии',
                'icon': 'fa-tooth'
            },
            {
                'industry_code': 'furniture',
                'name': 'Мебельный салон',
                'title': 'SEO продвижение мебельного магазина | Раскрутка сайта мебели',
                'description': 'Комплексное SEO продвижение сайтов мебельных салонов и магазинов. Увеличение продаж мебели через поисковые системы.',
                'h1': 'SEO продвижение мебельного салона',
                'icon': 'fa-couch'
            },
            {
                'industry_code': 'fitness',
                'name': 'Фитнес-клуб',
                'title': 'SEO продвижение фитнес-клуба | Раскрутка сайта фитнес-центра',
                'description': 'Эффективное SEO продвижение сайтов фитнес-клубов. Привлечение новых клиентов через поисковые системы.',
                'h1': 'SEO продвижение фитнес-клуба',
                'icon': 'fa-dumbbell'
            },
            {
                'industry_code': 'tourism',
                'name': 'Туризм',
                'title': 'SEO продвижение туристического сайта | Раскрутка турагентства',
                'description': 'Профессиональное SEO продвижение туристических сайтов. Увеличение продаж туров через поисковые системы.',
                'h1': 'SEO продвижение туристического сайта',
                'icon': 'fa-plane'
            },
            {
                'industry_code': 'cars',
                'name': 'Автосалоны',
                'title': 'SEO продвижение автосалона | Раскрутка сайта автодилера',
                'description': 'Комплексное SEO продвижение сайтов автосалонов. Увеличение продаж автомобилей через интернет.',
                'h1': 'SEO продвижение автосалона',
                'icon': 'fa-car'
            },
            {
                'industry_code': 'beauty',
                'name': 'Салон красоты',
                'title': 'SEO продвижение салона красоты | Раскрутка сайта beauty-индустрии',
                'description': 'Эффективное SEO продвижение сайтов салонов красоты. Привлечение клиентов через поисковые системы.',
                'h1': 'SEO продвижение салона красоты',
                'icon': 'fa-spa'
            },
            {
                'industry_code': 'repairs',
                'name': 'Ремонт квартир',
                'title': 'SEO продвижение сайта ремонтных услуг | Раскрутка компании по ремонту',
                'description': 'Профессиональное SEO продвижение сайтов ремонтных компаний. Привлечение заказов через поисковые системы.',
                'h1': 'SEO продвижение сайта ремонтной компании',
                'icon': 'fa-paint-roller'
            },
            {
                'industry_code': 'flowers',
                'name': 'Магазин цветов',
                'title': 'SEO продвижение цветочного магазина | Раскрутка сайта доставки цветов',
                'description': 'Комплексное SEO продвижение сайтов цветочных магазинов. Увеличение продаж через поисковые системы.',
                'h1': 'SEO продвижение магазина цветов',
                'icon': 'fa-fan'
            },
            {
                'industry_code': 'construction',
                'name': 'Строительство',
                'title': 'SEO продвижение строительной компании | Раскрутка сайта застройщика',
                'description': 'Профессиональное SEO продвижение строительных компаний. Привлечение клиентов через поисковые системы.',
                'h1': 'SEO продвижение строительной компании',
                'icon': 'fa-hammer'
            },
            {
                'industry_code': 'agriculture',
                'name': 'Сельхозтехника',
                'title': 'SEO продвижение сайта сельхозтехники | Раскрутка агротехники',
                'description': 'Эффективное SEO продвижение сайтов сельскохозяйственной техники. Увеличение продаж через интернет.',
                'h1': 'SEO продвижение сайта сельхозтехники',
                'icon': 'fa-tractor'
            },
            {
                'industry_code': 'printing',
                'name': 'Полиграфия',
                'title': 'SEO продвижение типографии | Раскрутка полиграфической компании',
                'description': 'Комплексное SEO продвижение сайтов полиграфических компаний. Привлечение заказов через поисковые системы.',
                'h1': 'SEO продвижение типографии',
                'icon': 'fa-print'
            },
            {
                'industry_code': 'insurance',
                'name': 'Страхование',
                'title': 'SEO продвижение страховой компании | Раскрутка страхового брокера',
                'description': 'Профессиональное SEO продвижение сайтов страховых компаний. Привлечение клиентов через поисковые системы.',
                'h1': 'SEO продвижение страховой компании',
                'icon': 'fa-shield-alt'
            },
            {
                'industry_code': 'industry',
                'name': 'Промышленность',
                'title': 'SEO продвижение промышленной компании | Раскрутка производства',
                'description': 'Эффективное SEO продвижение промышленных предприятий. Увеличение B2B продаж через интернет.',
                'h1': 'SEO продвижение промышленной компании',
                'icon': 'fa-industry'
            },
            {
                'industry_code': 'realestate',
                'name': 'Недвижимость',
                'title': 'SEO продвижение агентства недвижимости | Раскрутка риэлторской компании',
                'description': 'Комплексное SEO продвижение сайтов недвижимости. Привлечение клиентов через поисковые системы.',
                'h1': 'SEO продвижение агентства недвижимости',
                'icon': 'fa-home'
            },
            {
                'industry_code': 'windows',
                'name': 'Пластиковые окна',
                'title': 'SEO продвижение компании пластиковых окон | Раскрутка оконной компании',
                'description': 'Профессиональное SEO продвижение сайтов оконных компаний. Увеличение продаж через интернет.',
                'h1': 'SEO продвижение компании пластиковых окон',
                'icon': 'fa-window-maximize'
            },
            {
                'industry_code': 'hotels',
                'name': 'Гостиницы',
                'title': 'SEO продвижение гостиницы | Раскрутка сайта отеля',
                'description': 'Эффективное SEO продвижение сайтов гостиниц и отелей. Привлечение гостей через поисковые системы.',
                'h1': 'SEO продвижение гостиницы',
                'icon': 'fa-hotel'
            },
            {
                'industry_code': 'cosmetics',
                'name': 'Косметика',
                'title': 'SEO продвижение магазина косметики | Раскрутка косметического бренда',
                'description': 'Комплексное SEO продвижение косметических магазинов. Увеличение продаж через поисковые системы.',
                'h1': 'SEO продвижение магазина косметики',
                'icon': 'fa-magic'
            },
            {
                'industry_code': 'kids',
                'name': 'Детские товары',
                'title': 'SEO продвижение магазина детских товаров | Раскрутка детского магазина',
                'description': 'Профессиональное SEO продвижение магазинов детских товаров. Привлечение целевых покупателей.',
                'h1': 'SEO продвижение магазина детских товаров',
                'icon': 'fa-baby'
            },
            {
                'industry_code': 'pharmacy',
                'name': 'Аптеки',
                'title': 'SEO продвижение аптеки | Раскрутка аптечной сети',
                'description': 'Эффективное SEO продвижение сайтов аптек. Увеличение продаж через поисковые системы.',
                'h1': 'SEO продвижение аптеки',
                'icon': 'fa-pills'
            }
        ]

        for industry_data in industries:
            industry = IndustryPage(**industry_data)
            db.session.add(industry)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error initializing industries: {e}")


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
        website_url = request.form.get('website_url')
        phone = request.form.get('phone')
        message = request.form.get('message')

        if not all([name, website_url, phone, message]):
            flash('Пожалуйста, заполните все поля формы', 'error')
            return redirect(url_for('contact'))

        feedback = Feedback(
            name=name,
            website_url=website_url,
            phone=phone,
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

@app.route('/sitemap.xml')
def sitemap():
    root = ET.Element('urlset')
    root.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')

    urls = [
        '/',
        '/services',
        '/contact',
        '/service/audit',
        '/service/semantic',
        '/service/copywriting',
        '/service/ecommerce',
        '/service/business',
        '/service/landing'
    ]

    for url in urls:
        url_elem = ET.SubElement(root, 'url')
        loc = ET.SubElement(url_elem, 'loc')
        full_url = 'https://good-seo.online' + url
        loc.text = full_url

        lastmod = ET.SubElement(url_elem, 'lastmod')
        lastmod.text = datetime.now().strftime('%Y-%m-%d')

        changefreq = ET.SubElement(url_elem, 'changefreq')
        changefreq.text = 'weekly'

        priority = ET.SubElement(url_elem, 'priority')
        priority.text = '1.0' if url == '/' else '0.8'

    tree = ET.ElementTree(root)
    xml_str = ET.tostring(root, encoding='unicode', method='xml')

    return Response(xml_str, mimetype='application/xml')

@app.route('/industry/<industry_code>')
def industry_page(industry_code):
    industry = IndustryPage.query.filter_by(industry_code=industry_code).first_or_404()
    return render_template('industry.html', industry=industry)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_404.html'), 404

with app.app_context():
    db.create_all()
    init_metadata()
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        admin_user = User(username='admin')
        admin_user.set_password('JDczyrf8800@')
        db.session.add(admin_user)
        db.session.commit()
    else:
        admin_user.set_password('JDczyrf8800@')
        db.session.commit()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)