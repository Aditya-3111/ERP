"""
FinLedger Pro - Django settings.

Everything that changes between computers (database login, secret key, allowed
websites ...) comes from  backend/.env  - copy .env.example to .env and edit it.
"""
from datetime import timedelta
from pathlib import Path

from .env import get, get_bool, get_list

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- security
SECRET_KEY = get('SECRET_KEY', 'django-insecure-change-me-in-your-env-file')
DEBUG = get_bool('DEBUG', True)
ALLOWED_HOSTS = get_list('ALLOWED_HOSTS', 'localhost,127.0.0.1,testserver')

# ------------------------------------------------------------ applications
# NOTE: our own apps come FIRST on purpose - that lets apps.core replace the
# built-in "runserver" command with one that creates the database for you.
INSTALLED_APPS = [
    # --- FinLedger modules (one Django app per business module)
    'apps.core',          # users, roles, company, financial years, dashboard
    'apps.finance',       # account groups, ledgers, vouchers, reports
    'apps.inventory',     # stock items, godowns, MRN
    'apps.crm',           # customers, leads, quotations, purchase orders
    'apps.hr',            # employees, attendance, payroll
    'apps.gate',          # visitors, gate entries
    'apps.pos',           # point of sale
    'apps.production',    # BOM, production orders
    'apps.maintenance',   # assets, work orders, breakdowns
    'apps.admin_panel',   # menus, backups, settings, webhooks ...
    # --- Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # --- third party
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',
    'import_export',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# ---------------------------------------------------------------- database
# MySQL / MariaDB is the real database.  "sqlite" exists only so that the
# automatic tests can run on a computer without MySQL.
DB_ENGINE = get('DB_ENGINE', 'mysql').lower()
DB_NAME = get('DB_NAME', 'finledger_pro')
DB_USER = get('DB_USER', 'root')
DB_PASSWORD = get('DB_PASSWORD', '')
DB_HOST = get('DB_HOST', '127.0.0.1')
DB_PORT = get('DB_PORT', '3306')

if DB_ENGINE == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': DB_NAME,
            'USER': DB_USER,
            'PASSWORD': DB_PASSWORD,
            'HOST': DB_HOST,
            'PORT': DB_PORT,
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
            'TEST': {'CHARSET': 'utf8mb4', 'COLLATION': 'utf8mb4_unicode_ci'},
        }
    }
elif DB_ENGINE == 'sqlite':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': get('SQLITE_PATH', str(BASE_DIR / 'db.sqlite3')),
        }
    }
else:
    raise ValueError("DB_ENGINE in .env must be 'mysql' or 'sqlite'")

# On `runserver`, create the database + tables + starting data automatically.
AUTO_SETUP_DB = get_bool('AUTO_SETUP_DB', True)
SEED_DEMO_DATA = get_bool('SEED_DEMO_DATA', True)
ADMIN_USERNAME = get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = get('ADMIN_PASSWORD', 'admin')
ADMIN_EMAIL = get('ADMIN_EMAIL', 'admin@finledger.local')

# ---------------------------------------------------------------- accounts
AUTH_USER_MODEL = 'core.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ----------------------------------------------------- language & timezone
LANGUAGE_CODE = 'en-us'
TIME_ZONE = get('TIME_ZONE', 'Asia/Kolkata')
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ------------------------------------------------------------------- files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --------------------------------------------------------------------- API
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_PAGINATION_CLASS': 'apps.core.pagination.StandardPagination',
    'PAGE_SIZE': 20,
    # money fields are sent as JSON numbers (not strings)
    'COERCE_DECIMAL_TO_STRING': False,
    'EXCEPTION_HANDLER': 'apps.core.exceptions.api_exception_handler',
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=8),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'guid',
}

# ------------------------------------------------------------------- CORS
# The React dev server (Vite) runs on port 5173 by default.
CORS_ALLOWED_ORIGINS = get_list(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000',
)
CORS_ALLOW_CREDENTIALS = True
