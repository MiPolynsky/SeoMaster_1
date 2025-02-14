# SEO Услуги - Веб-приложение для SEO-маркетинга

Веб-приложение для профессионального SEO-маркетинга с интерактивными инструментами оптимизации и анализа сайтов.

## Основные функции

- Расширенные SEO-инструменты с адаптивным интерфейсом
- Поддержка 404 страницы с пользовательским дизайном
- Интерактивные анимации для улучшения пользовательского опыта
- Встроенная карта Яндекс на странице контактов
- Управление метаданными страниц
- Обратная связь с клиентами
- Административная панель

## Технологии

- Flask (backend)
- PostgreSQL (база данных)
- HTML/CSS/JavaScript (frontend)
- Bootstrap (адаптивный дизайн)
- SQLAlchemy (ORM)
- Яндекс.Карты API

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/seo-services.git
cd seo-services
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Настройте переменные окружения:
Создайте файл `.env` и добавьте следующие переменные:
```
DATABASE_URL=postgresql://username:password@localhost:5432/dbname
FLASK_SECRET_KEY=your-secret-key
```

4. Запустите приложение:
```bash
python main.py
```

## Структура проекта

- `app.py` - основной файл приложения
- `models.py` - модели базы данных
- `admin.py` - настройки административной панели
- `templates/` - HTML шаблоны
- `static/` - статические файлы (CSS, JavaScript, изображения)

## Лицензия

MIT License

## Авторы

- Ваше имя/организация

## Поддержка

По вопросам поддержки обращайтесь: sells@good-seo.online
