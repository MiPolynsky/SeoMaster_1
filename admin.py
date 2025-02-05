from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, LoginManager
from flask import redirect, url_for, flash
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired
from models import User, PageMetadata, Feedback
from app import app, db

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

class PageMetadataView(SecureModelView):
    column_list = ['url_path', 'title', 'description', 'h1', 'created_at', 'updated_at']
    form_columns = ['url_path', 'title', 'description', 'h1']
    column_searchable_list = ['url_path', 'title']
    column_filters = ['created_at', 'updated_at']

    form_overrides = {
        'url_path': StringField,
        'title': StringField,
        'description': TextAreaField,
        'h1': StringField
    }

    form_args = {
        'url_path': {
            'label': 'URL путь',
            'validators': [DataRequired()]
        },
        'title': {
            'label': 'Заголовок',
            'validators': [DataRequired()]
        },
        'description': {
            'label': 'Описание',
            'validators': [DataRequired()]
        },
        'h1': {
            'label': 'H1 заголовок',
            'validators': [DataRequired()]
        }
    }

    form_widget_args = {
        'url_path': {
            'class': 'form-control'
        },
        'title': {
            'class': 'form-control'
        },
        'description': {
            'class': 'form-control',
            'rows': 3
        },
        'h1': {
            'class': 'form-control'
        }
    }

    can_create = True
    can_edit = True
    can_delete = True

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.created_at = db.func.now()
        model.updated_at = db.func.now()

class FeedbackModelView(SecureModelView):
    column_list = ['name', 'email', 'subject', 'status', 'created_at']
    column_searchable_list = ['name', 'email', 'subject', 'message']
    column_filters = ['status', 'created_at']
    form_excluded_columns = ['created_at']

    form_overrides = {
        'name': StringField,
        'email': StringField,
        'subject': StringField,
        'message': TextAreaField,
        'status': StringField
    }

    form_args = {
        'name': {
            'label': 'Имя',
            'validators': [DataRequired()]
        },
        'email': {
            'label': 'Email',
            'validators': [DataRequired()]
        },
        'subject': {
            'label': 'Тема',
            'validators': [DataRequired()]
        },
        'message': {
            'label': 'Сообщение',
            'validators': [DataRequired()]
        },
        'status': {
            'label': 'Статус'
        }
    }

    form_widget_args = {
        'name': {
            'class': 'form-control'
        },
        'email': {
            'class': 'form-control'
        },
        'subject': {
            'class': 'form-control'
        },
        'message': {
            'class': 'form-control',
            'rows': 5
        },
        'status': {
            'class': 'form-control'
        }
    }

    can_create = False
    can_delete = True
    can_edit = True
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

admin = Admin(app, name='SEO Admin', template_mode='bootstrap3', index_view=SecureAdminIndexView())
admin.add_view(PageMetadataView(PageMetadata, db.session))
admin.add_view(FeedbackModelView(Feedback, db.session))