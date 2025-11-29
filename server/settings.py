import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------------------------------
#   CONFIGURACIÓN GENERAL
# ----------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "cambiame-por-una-clave-real")

DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = ["*"]   # Acepta cualquier origen (solo recomendado para desarrollo)

# Render HTTPS redirect fixer (IMPORTANTE)
SECURE_SSL_REDIRECT = False

# ----------------------------------------------------
#   APLICACIONES INSTALADAS
# ----------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Terceros
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",

    # Tu app principal
    "server",
]

# ----------------------------------------------------
#   MIDDLEWARE
# ----------------------------------------------------
MIDDLEWARE = [
    # DEBE IR PRIMERO o el preflight OPTIONS falla
    "corsheaders.middleware.CorsMiddleware",

    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",

    # CSRF puede bloquear preflight → lo configuramos abajo
    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ----------------------------------------------------
#   CORS TOTALMENTE ABIERTO
# ----------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = ["*"]

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

# ----------------------------------------------------
#   CSRF (IMPORTANTE PARA EVITAR ERRORES)
# ----------------------------------------------------
CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
    "http://localhost:5173",
]

# ----------------------------------------------------
#   URLS Y TEMPLATES
# ----------------------------------------------------
ROOT_URLCONF = "server.urls"

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

WSGI_APPLICATION = "server.wsgi.application"

# ----------------------------------------------------
#   BASE DE DATOS
# ----------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ----------------------------------------------------
#   VALIDACIÓN DE PASSWORDS
# ----------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    { "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator" },
    { "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator" },
    { "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator" },
    { "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator" },
]

# ----------------------------------------------------
#   INTERNACIONALIZACIÓN
# ----------------------------------------------------
LANGUAGE_CODE = "es"
TIME_ZONE = "America/Argentina/Buenos_Aires"
USE_I18N = True
USE_TZ = True

# ----------------------------------------------------
#   ARCHIVOS ESTÁTICOS
# ----------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# ----------------------------------------------------
#   CUSTOM USER MODEL
# ----------------------------------------------------
AUTH_USER_MODEL = "server.User"

# ----------------------------------------------------
#   STRIPE
# ----------------------------------------------------
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

# ----------------------------------------------------
#   DJANGO REST FRAMEWORK
# ----------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}
