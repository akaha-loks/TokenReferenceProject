"""
Django settings for TokenReferenceProject project.
"""

from pathlib import Path
import os
import cloudinary

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-ru)x29uv0=m=qzdv^o+r87)@(kplu)o#(gg*$^67g=&_1j(xw='

DEBUG = False

ALLOWED_HOSTS = ["token-reference.onrender.com"]


INSTALLED_APPS = [
    "jazzmin",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'ckeditor_uploader',
    'main.apps.MainConfig',
    'cloudinary',
    'cloudinary_storage',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # 👈 обязательно
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'TokenReference.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'TokenReference.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Asia/Bishkek'

USE_I18N = True
USE_TZ = True


# =========================
# STATIC FILES (админка)
# =========================

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# =========================
# MEDIA (Cloudinary)
# =========================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


# =========================
# AUTH
# =========================

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'post_list'
LOGOUT_REDIRECT_URL = 'welcome'


# =========================
# JAZZMIN
# =========================

JAZZMIN_SETTINGS = {
    "site_title": "Token Reference",
    "site_header": "Token Reference",
    "site_brand": "TokenReference",
    "welcome_sign": "Добро пожаловать в админку",
    "copyright": "Token Reference",
    "theme": "darkly",
    "icons": {
        "main.Token": "fas fa-key",
        "main.Post": "fas fa-book",
    },
    "show_sidebar": True,
    "navigation_expanded": True,
    "order_with_respect_to": ["main", "auth"],
    "custom_links": {
        "main": [{
            "name": "Сайт",
            "url": "/",
            "icon": "fas fa-globe",
            "permissions": ["main.view_post"],
        }]
    },
    "show_ui_builder": False,
}


# =========================
# CKEDITOR
# =========================

CKEDITOR_UPLOAD_PATH = "instruction_images/"

CKEDITOR_CONFIGS = {
    'default': {
        'height': 350,
        'width': 600,
        'toolbar': [
            ['Format'],
            ['Bold', 'Italic'],
            ['NumberedList', 'BulletedList'],
            ['Link'],
            ['Image'],
        ],
    },
}


# =========================
# CLOUDINARY
# =========================

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
