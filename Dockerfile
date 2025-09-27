# Dockerfile für Railway Deployment
FROM python:3.11-slim

# Arbeitsverzeichnis setzen
WORKDIR /app

# System-Dependencies installieren
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python Requirements kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App-Code kopieren
COPY . .

# Non-root User erstellen
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Port expose
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')" || exit 1

# App starten - Railway injection für $PORT
CMD sh -c "gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 app:app"
