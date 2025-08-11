from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'dev-key'
DEBUG = True
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = ['django.contrib.staticfiles','portfolio']
MIDDLEWARE = ['django.middleware.security.SecurityMiddleware','django.middleware.common.CommonMiddleware']
ROOT_URLCONF = 'django_project.urls'
TEMPLATES = [{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[BASE_DIR/'templates'],'APP_DIRS':True,'OPTIONS':{}}]
WSGI_APPLICATION = 'django_project.wsgi.application'
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR/'static']