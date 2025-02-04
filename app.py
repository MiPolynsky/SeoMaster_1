from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    services = [
        {
            'title': 'Аудит сайта',
            'description': 'Комплексный анализ вашего сайта для выявления технических ошибок и потенциала роста',
            'image': 'https://images.unsplash.com/photo-1542744173-05336fcc7ad4',
            'icon': 'fa-magnifying-glass-chart',
            'url': '/service/audit'
        },
        {
            'title': 'Семантическое ядро',
            'description': 'Подбор ключевых слов и фраз для эффективного продвижения вашего сайта',
            'image': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f',
            'icon': 'fa-sitemap',
            'url': '/service/semantic'
        },
        {
            'title': 'Копирайтинг',
            'description': 'Создание уникального контента, оптимизированного под поисковые системы',
            'image': 'https://images.unsplash.com/photo-1488190211105-8b0e65b80b4e',
            'icon': 'fa-pen-fancy',
            'url': '/service/copywriting'
        }
    ]
    return render_template('index.html', services=services)

@app.route('/services')
def services():
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
    return render_template('services.html', services=all_services)

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Маршруты для отдельных услуг
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