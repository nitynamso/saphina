# Base ligera y moderna
FROM python:3.12-slim-bookworm

# Evita archivos .pyc y fuerza logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instalamos dependencias de sistema: 
# build-essential y libpq-dev (para Postgres) 
# + librerías de imágenes para Wagtail (jpeg, zlib, webp)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    && rm -rf /var/lib/apt/lists/*

# Creamos un usuario de sistema para no correr como root
RUN useradd -m wagtail

# Instalamos gunicorn y dependencias de Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir gunicorn dj-database-url python-dotenv \
    && pip install --no-cache-dir -r requirements.txt

# Copiamos el código y damos permisos al usuario wagtail
COPY --chown=wagtail:wagtail . /app/

# Creamos carpetas de estáticos y media con permisos correctos
RUN mkdir -p /app/static /app/media && chown -R wagtail:wagtail /app/static /app/media

# Cambiamos al usuario seguro
USER wagtail

EXPOSE 8000

# El comando se queda igual, pero ahora corre bajo un usuario seguro
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "saphinagroup.wsgi:application"]