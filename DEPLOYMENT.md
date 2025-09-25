# 🚀 Deployment Guide - Didis Premium Trading Academy

## 📋 Übersicht

Diese Anleitung erklärt, wie du die Didis Premium Trading Academy von der lokalen Entwicklung bis zur Produktionsumgebung bereitstellst.

## 🔧 Umgebungskonfiguration

### 1. Umgebungsvariablen Setup

Erstelle eine `.env` Datei im Root-Verzeichnis:

```bash
# Security - WICHTIG: Ändere diese Werte!
SECRET_KEY=dein-super-sicherer-secret-key-hier-mindestens-32-zeichen

# Database
DATABASE_URL=sqlite:///didis_academy.db

# Flask Configuration
FLASK_ENV=production  # WICHTIG: Auf production setzen!
FLASK_DEBUG=False     # WICHTIG: Auf False setzen!

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=deine-email@domain.com
MAIL_PASSWORD=dein-app-passwort

# Session Configuration für Produktion
SESSION_COOKIE_SECURE=True   # HTTPS erforderlich
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
PERMANENT_SESSION_LIFETIME=7200
```

### 2. Sicheren Secret Key generieren

```python
import secrets
print(secrets.token_hex(32))
```

## 🏗️ Lokale Entwicklung

### Setup
```bash
# 1. Repository klonen
git clone https://github.com/dein-username/didis-premium-app.git
cd didis-premium-app

# 2. Virtual Environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 3. Dependencies installieren
pip install -r requirements.txt

# 4. .env Datei erstellen (siehe oben)
# 5. Datenbank initialisieren
python init_db.py

# 6. App starten
python app.py
```

## 🌐 Produktions-Deployment

### Option 1: Traditional Server (Ubuntu/Debian)

#### 1. Server Setup
```bash
# Python und pip installieren
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx

# User für die App erstellen
sudo useradd -m -s /bin/bash didis-app
sudo su - didis-app
```

#### 2. App Deploy
```bash
# Repository klonen
git clone https://github.com/dein-username/didis-premium-app.git
cd didis-premium-app

# Virtual Environment
python3 -m venv venv
source venv/bin/activate

# Dependencies
pip install -r requirements.txt

# .env für Produktion erstellen
nano .env  # Fülle Production-Werte ein

# Datenbank initialisieren
python init_db.py

# Test mit Gunicorn
gunicorn --bind 0.0.0.0:8000 app:app
```

#### 3. Systemd Service erstellen
```bash
# Als root
sudo nano /etc/systemd/system/didis-academy.service
```

```ini
[Unit]
Description=Gunicorn instance to serve Didis Academy
After=network.target

[Service]
User=didis-app
Group=www-data
WorkingDirectory=/home/didis-app/didis-premium-app
Environment="PATH=/home/didis-app/didis-premium-app/venv/bin"
ExecStart=/home/didis-app/didis-premium-app/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Service starten
sudo systemctl daemon-reload
sudo systemctl start didis-academy
sudo systemctl enable didis-academy
sudo systemctl status didis-academy
```

#### 4. Nginx Reverse Proxy
```bash
sudo nano /etc/nginx/sites-available/didis-academy
```

```nginx
server {
    listen 80;
    server_name deine-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Statische Dateien direkt servieren
    location /static {
        alias /home/didis-app/didis-premium-app/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# Site aktivieren
sudo ln -s /etc/nginx/sites-available/didis-academy /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

# SSL mit Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d deine-domain.com
```

### Option 2: Docker Deployment

#### 1. Dockerfile erstellen
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Initialize database
RUN python init_db.py

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "app:app"]
```

#### 2. Docker Compose
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=sqlite:///didis_academy.db
    volumes:
      - ./instance:/app/instance
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - /etc/letsencrypt:/etc/letsencrypt
    depends_on:
      - web
    restart: unless-stopped
```

### Option 3: Cloud Platforms

#### Heroku
```bash
# Procfile erstellen
echo "web: gunicorn app:app" > Procfile

# Heroku CLI
heroku login
heroku create didis-premium-academy
heroku config:set SECRET_KEY=dein-secret-key
heroku config:set FLASK_ENV=production
git push heroku main
```

#### Railway
```bash
# railway.toml
[build]
builder = "DOCKERFILE"

[deploy]
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

## 🔒 Sicherheits-Checklist für Produktion

### ✅ Vor dem Deployment prüfen:
- [ ] `SECRET_KEY` ist sicher und eindeutig
- [ ] `FLASK_DEBUG=False` in Produktion
- [ ] `SESSION_COOKIE_SECURE=True` für HTTPS
- [ ] Alle Demo-Passwörter geändert
- [ ] Database-Backups konfiguriert
- [ ] SSL-Zertifikat installiert
- [ ] Firewall konfiguriert (nur Ports 80, 443, 22)
- [ ] Regelmäßige Updates geplant

### 🛡️ Additional Security:
```python
# In app.py für Produktion hinzufügen:
from flask_talisman import Talisman

# Security Headers
Talisman(app, 
    force_https=True,
    strict_transport_security=True,
    content_security_policy={
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline'",
        'style-src': "'self' 'unsafe-inline'"
    }
)
```

## 📊 Monitoring & Maintenance

### Logging Setup
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/didis-academy.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

### Health Check Endpoint
```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}
```

### Database Backup Script
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
cp /home/didis-app/didis-premium-app/didis_academy.db /backup/didis_academy_$DATE.db
find /backup -name "didis_academy_*.db" -mtime +7 -delete
```

## 🚀 CI/CD Pipeline (GitHub Actions)

`.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
        
    - name: Install dependencies
      run: pip install -r requirements.txt
      
    - name: Run tests
      run: python -m pytest tests/
      
    - name: Deploy to server
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.SSH_KEY }}
        script: |
          cd /home/didis-app/didis-premium-app
          git pull origin main
          source venv/bin/activate
          pip install -r requirements.txt
          sudo systemctl restart didis-academy
```

## 📞 Support nach Deployment

- **Logs prüfen:** `sudo journalctl -u didis-academy -f`
- **Service Status:** `sudo systemctl status didis-academy`
- **Nginx Logs:** `sudo tail -f /var/log/nginx/error.log`
- **App Logs:** `tail -f logs/didis-academy.log`

Bei Problemen: Erstelle einen GitHub Issue mit detaillierter Beschreibung! 🚨
