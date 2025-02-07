from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from models import User, PageMetadata, Feedback, IndustryPage
from database import db
from app import app

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

class PageMetadataView(SecureModelView):
    column_list = ['url_path', 'title', 'description', 'h1', 'created_at', 'updated_at']
    column_searchable_list = ['url_path', 'title']
    column_filters = ['created_at', 'updated_at']

    create_modal = True
    edit_modal = True

    def scaffold_form(self):
        form_class = super(PageMetadataView, self).scaffold_form()
        form_class.url_path = StringField('URL путь', validators=[DataRequired()])
        form_class.title = StringField('Заголовок', validators=[DataRequired()])
        form_class.description = TextAreaField('Описание', validators=[DataRequired()])
        form_class.h1 = StringField('H1 заголовок', validators=[DataRequired()])
        return form_class

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.created_at = db.func.now()
        model.updated_at = db.func.now()

class IndustryPageView(SecureModelView):
    column_list = ['industry_code', 'name', 'title', 'h1', 'updated_at']
    column_searchable_list = ['industry_code', 'name', 'title']
    column_filters = ['created_at', 'updated_at']

    create_modal = True
    edit_modal = True

    # Configure which fields should use a larger input area
    form_widget_args = {
        'seo_text': {
            'rows': 15,
            'style': 'font-family: monospace; width: 100%;'
        }
    }

    # Add help text for the SEO text field
    form_args = {
        'seo_text': {
            'description': 'Поддерживает HTML-разметку. Используйте теги для форматирования текста.'
        }
    }

    def scaffold_form(self):
        form_class = super(IndustryPageView, self).scaffold_form()
        form_class.industry_code = StringField('Код тематики', validators=[DataRequired()])
        form_class.name = StringField('Название', validators=[DataRequired()])
        form_class.title = StringField('Title', validators=[DataRequired()])
        form_class.description = TextAreaField('Description', validators=[DataRequired()])
        form_class.h1 = StringField('H1', validators=[DataRequired()])
        form_class.seo_text = TextAreaField('SEO текст')
        form_class.icon = StringField('Иконка FontAwesome', validators=[DataRequired()])
        return form_class

class FeedbackModelView(SecureModelView):
    column_list = ['name', 'email', 'phone', 'status', 'created_at']
    column_searchable_list = ['name', 'email', 'phone', 'message']
    column_filters = ['status', 'created_at']
    form_excluded_columns = ['created_at']

    create_modal = True
    edit_modal = True

    def scaffold_form(self):
        form_class = super(FeedbackModelView, self).scaffold_form()
        form_class.name = StringField('Имя', validators=[DataRequired()])
        form_class.email = StringField('Email', validators=[DataRequired()])
        form_class.phone = StringField('Номер телефона', validators=[DataRequired()])
        form_class.message = TextAreaField('Сообщение', validators=[DataRequired()])
        form_class.status = SelectField('Статус', 
                                   choices=[('new', 'Новое'), 
                                          ('read', 'Прочитано'), 
                                          ('responded', 'Отвечено')],
                                   validators=[DataRequired()])
        return form_class

    column_default_sort = ('created_at', True)

class SecureAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        return super(SecureAdminIndexView, self).index()

admin = Admin(app, 
             name='SEO Admin',
             template_mode='bootstrap3',
             index_view=SecureAdminIndexView(),
             base_template='admin/base.html')

admin.add_view(PageMetadataView(PageMetadata, db.session, name='Метаданные'))
admin.add_view(IndustryPageView(IndustryPage, db.session, name='Тематики'))
admin.add_view(FeedbackModelView(Feedback, db.session, name='Обратная связь'))