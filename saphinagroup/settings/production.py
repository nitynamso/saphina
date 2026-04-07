import os
import dj_database_url
from .base import *

# 1. DEBUG
# Lo dejamos en True para que veas errores, pero WhiteNoise necesita una ayuda extra:
DEBUG = True

# 2. SECRET KEY Y HOSTS
SECRET_KEY = os.environ.get("SECRET_KEY")
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

# 3. BASE DE DATOS
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# 4. CONFIGURACIÓN DE WHITE NOISE (ESTO ES LO QUE FALTA)
# Estas líneas obligan a WhiteNoise a servir archivos aunque DEBUG sea True
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True

# 5. ESTÁTICOS Y MEDIA (RUTAS ABSOLUTAS PARA DOCKER)
STATIC_ROOT = "/app/static"
MEDIA_ROOT = "/app/media"

# 6. STORAGES CORREGIDO PARA WHITENOISE
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# 7. SEGURIDAD PROXY
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS if host]

# LOGS
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