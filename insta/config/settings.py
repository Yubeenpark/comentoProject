
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hs@8(zy@c!x%2k6b6eymga*z9v14=y+vs_qdlk##mt9^)yy0^w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'social_django',
    # 'debug_toolbar',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'accounts',
    'post',
    'rest_framework',

    #google
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    #'goologin.apps.GoologinConfig',

    #channel
    'channels',
    'chat',
    'django_elasticsearch_dsl',
    'notifications',
    'webpush',

]

ELASTICSEARCH_DSL = {
    'default': {
        'host': '13.124.1.210:9200'
    },
}






MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_AUTO_SIGNUP = False
ACCOUNT_SIGNUP_FORM_CLASS = 'accounts.forms.SignupForm'
ACCOUNT_USERNAME_REQUIRED = True

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'profile', ],  # 'user_friends'는 요청 안 함
        # 'AUTH_PARAMS': {'auth_type': 'reauthenticate'}, # 매번 비밀번호 묻지 않으려면 주석처리
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email',
            'name',
            'gender',
        ],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': lambda request: 'kr_KR',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.4',
    },
}

SOCIAL_AUTH_FACEBOOK_KEY = '306630417852-doj12cvctbqsokfvbpu2n62hb3vr2bbk.apps.googleusercontent.com'
SOCIAL_AUTH_FACEBOOK_SECRET = 'kiUvdZCgAXlPGO-aw0eZxBr-'

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'config', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',  
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '306630417852-doj12cvctbqsokfvbpu2n62hb3vr2bbk.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'kiUvdZCgAXlPGO-aw0eZxBr-'

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.routing.application'
# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


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

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

# INTERNAL_IPS = [
#     '127.0.0.1',
# ]

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'config', 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTHENTICATION_BACKENDS = (
    #'social_core.backends.google.GoogleOAuth2', # Google
    #'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.google.GoogleOAuth2',
     # Django 기본 유저모델
)
SOCIAL_AUTH_URL_NAMESPACE = 'accounts:social'



SITE_ID = 1

LOGIN_URL = '/accounts/google/'
# 로그인 성공 시에 연결될 URL
LOGIN_REDIRECT_URL = '/accounts/google/'

#channel

#ASGI_APPLICATION = "config.routing.application"
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

# logging
LOGGING = {
    'version': 1,
    # 기존의 로깅 설정을 비활성화 할 것인가?
    'disable_existing_loggers': False,

    # 포맷터
    # 로그 레코드는 최종적으로 텍스트로 표현됨
    # 이 텍스트의 포맷 형식 정의
    # 여러 포맷 정의 가능
    'formatters': {
        'format1': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        },
        'format2': {
            'format': '%(levelname)s %(message)s'
        },
    },

    # 핸들러
    # 로그 레코드로 무슨 작업을 할 것인지 정의
    # 여러 핸들러 정의 가능
    'handlers': {
        # 로그 파일을 만들어 텍스트로 로그레코드 저장
        "file_debug": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "format1",
            "filename": "debug.log"
        },
        # 콘솔(터미널)에 출력
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'format1',
        },
        "file_error": {
            "class": "logging.FileHandler",
            "level": "ERROR",
            "formatter": "format1",
            "filename": "error.log"
        }
    },

    # 로거
    # 로그 레코드 저장소
    # 로거를 이름별로 정의
    'loggers': {
        'chat': {
            'handlers':['file_debug','console','file_error'],
            'level': 'DEBUG',
        },

        'accounts': {
            'handlers': ['file_debug', 'console' ,'file_error'],
            'level': 'DEBUG',
        },
        'post': {
                'handlers': ['file_debug', 'console' ,'file_error'],
                'level': 'DEBUG',
        }
    },
        
    

}