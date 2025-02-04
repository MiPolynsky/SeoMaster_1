from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    services = [
        {
            'title': 'Аудит сайта',
            'description': 'Комплексный анализ вашего сайта для выявления технических ошибок и потенциала роста',
            'image': 'https://images.unsplash.com/photo-1542744173-05336fcc7ad4',
            'icon': 'fa-magnifying-glass-chart'
        },
        {
            'title': 'Семантическое ядро',
            'description': 'Подбор ключевых слов и фраз для эффективного продвижения вашего сайта',
            'image': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f',
            'icon': 'fa-sitemap'
        },
        {
            'title': 'Копирайтинг',
            'description': 'Создание уникального контента, оптимизированного под поисковые системы',
            'image': 'https://images.unsplash.com/photo-1488190211105-8b0e65b80b4e',
            'icon': 'fa-pen-fancy'
        }
    ]
    return render_template('index.html', services=services)

@app.route('/services')
def services():
    all_services = [
        {
            'title': 'Аудит сайта',
            'description': 'Комплексный анализ вашего сайта для выявления технических ошибок и потенциала роста',
            'icon': 'fa-magnifying-glass-chart'
        },
        {
            'title': 'Семантическое ядро',
            'description': 'Подбор ключевых слов и фраз для эффективного продвижения вашего сайта',
            'icon': 'fa-sitemap'
        },
        {
            'title': 'Копирайтинг',
            'description': 'Создание уникального контента, оптимизированного под поисковые системы',
            'icon': 'fa-pen-fancy'
        },
        {
            'title': 'Продвижение интернет-магазинов',
            'description': 'Специализированное SEO для электронной коммерции',
            'icon': 'fa-cart-shopping'
        },
        {
            'title': 'Продвижение сайтов-визиток',
            'description': 'Оптимизация небольших корпоративных сайтов',
            'icon': 'fa-building'
        },
        {
            'title': 'Продвижение одностраничных сайтов',
            'description': 'SEO-оптимизация лендингов для максимальной конверсии',
            'icon': 'fa-file'
        }
    ]
    return render_template('services.html', services=all_services)

@app.route('/contact')
def contact():
    return render_template('contact.html')
