from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from models import User, PageMetadata, Feedback
from app import app, db

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
admin.add_view(FeedbackModelView(Feedback, db.session, name='Обратная связь'))