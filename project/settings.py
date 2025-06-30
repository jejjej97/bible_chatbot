import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'auto-gpt-bot'
DEBUG = False
CSRF_TRUSTED_ORIGINS = ['https://bible_chatbot.onrender.com']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.ngrok-free.app', '.onrender.com']
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',  # ✅ 세션 앱
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chatbot',
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # ✅ 필수
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
ROOT_URLCONF = 'project.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # ✅ admin 사이드바에 필요
                'django.contrib.auth.context_processors.auth',  # ✅ 로그인/세션에 필요
                'django.contrib.messages.context_processors.messages',  # ✅ 메시지 표시에 필요
            ],
        },
    },
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # ✅ 세션 미들웨어
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
WSGI_APPLICATION = 'project.wsgi.application'
STATIC_URL = '/static/'
ALLOWED_HOSTS += ['.onrender.com']
