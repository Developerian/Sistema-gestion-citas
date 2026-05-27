# Usamos una versión 'slim' para que la imagen no sea tan pesada
FROM python:3.12-slim

# Instalamos herramientas necesarias para que Django pueda hablar con Postgres
# y para que los comandos de red (como pg_isready) funcionen.
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalamos las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de tu código
COPY . .

# Por defecto, el CMD se ejecutará desde el docker-compose, 
# así que aquí no es obligatorio ponerlo, pero es buena práctica.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]