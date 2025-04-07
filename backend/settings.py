import os
from pathlib import Path
# import dj_database_url 
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 Secret Key & Debug
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', '9XOGyqqV-euH5TA8yRnYMtOFWm5C-QQigkB4gWRNsCGanEgn1H4ZVsoG23Pi0q7P-Q4')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# 🌍 Allowed Hosts
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,0.0.0.0').split(',')


# ✅ Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
    'django_extensions',

    # Local apps
    'api',
    'authentication',
]

# ✅ REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# ✅ Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# DATABASE_URL should be set to connect correctly to the database in Docker
DATABASE_URL = os.getenv('DATABASE_URL', 'postgres://raphwealth_user:1985-franK@db:5432/raphwealth_db')  # Use 'db' instead of 'localhost'

url = urlparse(DATABASE_URL)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': url.path[1:],  # Remove the leading slash
        'USER': url.username,
        'PASSWORD': url.password,
        'HOST': url.hostname,  # This should now resolve to 'db' inside the Docker network
        'PORT': url.port,
    }
}

# ✅ Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ✅ Custom User
AUTH_USER_MODEL = 'authentication.User'

# 🌐 Language & Timezone
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ✅ Static & Media Files
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Ensure directories exist
os.makedirs(STATIC_ROOT, exist_ok=True)
os.makedirs(MEDIA_ROOT, exist_ok=True)

# ✅ CORS
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = os.getenvCORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # For local dev
    "https://your-react-app.netlify.app",  # For production
]

# ✅ Local SVG fix
if DEBUG:
    import mimetypes
    mimetypes.add_type("image/svg+xml", ".svg", True)
