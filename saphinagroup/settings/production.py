import os
import dj_database_url
from .base import *

# 1. DEBUG DINÁMICO
# Ahora sí podrás activarlo desde el .env poniendo DEBUG=1
DEBUG = True
# 2. SECRET KEY
# Obligatorio tenerla en el .env del servidor
SECRET_KEY = os.environ.get("SECRET_KEY")

# 3. DOMINIOS (ALLOWED HOSTS)
# Se leen del .env separados por comas: saphina.auralint.com,saphinagroup.com
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

# 4. BASE DE DATOS (PostgreSQL)
# Esto conecta Django con el contenedor de Postgres automáticamente
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# 5. SEGURIDAD DETRÁS DE PROXY (Nginx Proxy Manager)
# Esto es VITAL para que no te dé errores de "Insecure Connection"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "1") == "1"
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# 6. ORÍGENES DE CONFIANZA PARA CSRF
# Sin esto, el admin de Wagtail te dará error 403 al intentar entrar
CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS if host]

# 7. ESTÁTICOS Y MEDIA
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}

STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# 8. LOGS (Para ver qué pasa en la terminal de Docker)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}

try:
    from .local import *
except ImportError:
    pass