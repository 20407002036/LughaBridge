"""
Django settings for lughabridge project.

LughaBridge - Real-time Kikuyu ↔ English Translation Chat
"""

from pathlib import Path
import environ
import os
from dotenv import load_dotenv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")  # Load environment variables from .env file

# Environment variables
env = environ.Env(
    DEBUG=(bool, False),
    DEMO_MODE=(bool, False),
)

# Read .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# Demo mode flag
DEMO_MODE = env('DEMO_MODE')

# Hugging Face Inference API mode flag
USE_HF_INFERENCE = env.bool('USE_HF_INFERENCE', default=False)

# Groq API configuration (for faster Swahili translation)
GROQ_API_KEY = env('GROQ_API_KEY', default='')
USE_GROQ_FOR_SWAHILI = env.bool('USE_GROQ_FOR_SWAHILI', default=False)
GROQ_MODEL = env('GROQ_MODEL', default='llama-3.3-70b-versatile')

# Validate that DEMO_MODE and USE_HF_INFERENCE are not both enabled
if DEMO_MODE and USE_HF_INFERENCE:
    raise Exception(
        "DEMO_MODE and USE_HF_INFERENCE cannot both be True. "
        "Choose one: DEMO_MODE for testing with mock data, "
        "USE_HF_INFERENCE for cloud-hosted models, "
        "or both False for local models."
    )

REDIS_URL = env('REDIS_URL', default='redis://localhost:6379/0')

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    # Third-party apps
    "rest_framework",
    "corsheaders",
    "channels",
    "django_q",
    
    # LughaBridge apps
    "rooms",
    "translation",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # Must be first
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "lughabridge.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "lughabridge.wsgi.application"
ASGI_APPLICATION = "lughabridge.asgi.application"


# Channels configuration
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [env('REDIS_URL')],
        },
    },
}


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    "default": env.db('DATABASE_URL', default='sqlite:///db.sqlite3')
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# CORS Settings
CORS_ALLOWED_ORIGINS = env.list(
    'FRONTEND_URL',
    default=['http://localhost:3000']
)
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]


# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}


# Django-Q Configuration
Q_CLUSTER = {
    'name': 'LughaBridge',
    'workers': 4,
    'timeout': 90,
    'retry': 120,
    'queue_limit': 50,
    'bulk': 10,
    'orm': 'default',
    'redis': env('REDIS_URL'),
}


# Hugging Face Model Settings
HF_CACHE_DIR = env('HF_CACHE_DIR', default='/tmp/huggingface_cache')
HF_TOKEN = env('HF_TOKEN', default='')
HF_HUB_ENABLE_HF_TRANSFER = env('HF_HUB_ENABLE_HF_TRANSFER', default='0')

# Set environment variables for transformers library
if HF_TOKEN:
    os.environ['HF_TOKEN'] = HF_TOKEN
if HF_HUB_ENABLE_HF_TRANSFER == '1':
    os.environ['HF_HUB_ENABLE_HF_TRANSFER'] = '1'

SUPPORTED_LANGUAGES = env.list('SUPPORTED_LANGUAGES', default=['kikuyu', 'english'])

# Model paths
MODELS = {
    'asr': {
        'kikuyu': 'badrex/w2v-bert-2.0-kikuyu-asr',
        'swahili': 'thinkKenya/wav2vec2-large-xls-r-300m-sw',
        'english': 'facebook/wav2vec2-large-960h-lv60-self',
    },
    'translation': {
        'model': 'facebook/nllb-200-distilled-600M',
        'lang_codes': {
            'kikuyu': 'kik_Latn',
            'swahili': 'swh_Latn',
            'english': 'eng_Latn',
        }
    },
    'tts': {
        'kikuyu': 'facebook/mms-tts-kik',
        'swahili': 'facebook/mms-tts-swh',
        'english': 'facebook/mms-tts-eng',
    },
}

# Room settings
ROOM_CODE_LENGTH = 6
ROOM_EXPIRY_HOURS = 4
MAX_MESSAGES_PER_ROOM = 100
