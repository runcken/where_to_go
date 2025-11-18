import os
from environs import Env
from pathlib import Path


env = Env()
env.read_env()

SECRET_KEY = env.str('SECRET_KEY')

DEBUG = env.bool('DEBUG', False)

if DEBUG:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
else:
    ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': env.str('DATABASE_NAME', str(BASE_DIR / 'db.sqlite3')),
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'places.apps.PlacesConfig',
    'adminsortable2',
    'tinymce'
]

TINYMCE_DEFAULT_CONFIG = {
    'height': 360,
    'width': '100%',
    'plugins': '''
        textcolor save link image media preview codesample contextmenu
        table code lists fullscreen insertdatetime nonbreaking
        contextmenu directionality searchplace wordcount visualblocks
        visualchars code fullscreen autolink lists charmap print hr
        anchor pagebreak
        ''',
    'toolbar': '''
        undo redo | formatselect | bold italic backcolor |
        alignleft aligncenter alignright align justify |
        bullist numlist outdent indent |removeformat | help
        ''',
    'menubar': True,
    'statusbar': True,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'where_to_go.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'where_to_go.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = env.str('STATIC_URL', '/static/')

STATICFILES_DIRS = [os.path.join(BASE_DIR, env.str('STATIC_DIRS', 'static'))]

MEDIA_ROOT = os.path.join(BASE_DIR, env.str('MEDIA_ROOT', 'media'))

MEDIA_URL = env.str('MEDIA_URL', '/media/')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
