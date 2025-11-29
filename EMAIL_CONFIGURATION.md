# Email-Konfiguration für Didis Trading Academy

## Lokale Entwicklung

Erstelle eine `.env` Datei im Root-Verzeichnis mit folgenden Variablen:

```env
# Flask Environment
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-me

# Email Configuration (Gmail Beispiel)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=deine-email@gmail.com
MAIL_PASSWORD=dein-app-passwort-hier
MAIL_DEFAULT_SENDER=noreply@didis-academy.com

# Base URL für Email-Links
BASE_URL=http://localhost:5000
```

## Gmail App-Passwort einrichten

### Schritt 1: 2-Faktor-Authentifizierung aktivieren

1. Gehe zu [Google Account Security](https://myaccount.google.com/security)
2. Aktiviere "Bestätigung in zwei Schritten"

### Schritt 2: App-Passwort generieren

1. Gehe zu [App Passwords](https://myaccount.google.com/apppasswords)
2. Wähle "App auswählen" → "Sonstige"
3. Name eingeben: "Didis Trading Academy"
4. Klicke auf "Generieren"
5. Kopiere das 16-stellige App-Passwort (ohne Leerzeichen)
6. Setze dieses als `MAIL_PASSWORD` in der `.env` Datei

### Schritt 3: Test

```bash
python -c "from app import send_email; send_email('deine-test-email@gmail.com', 'Test', 'verify_email', username='Test', verification_link='http://test.de')"
```

## Railway Production Deployment

### Environment Variables setzen

Im Railway Dashboard unter "Variables":

```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=deine-email@gmail.com
MAIL_PASSWORD=dein-app-passwort
MAIL_DEFAULT_SENDER=noreply@didis-academy.com
BASE_URL=https://didis-premium-app-production.up.railway.app
```

### Migration ausführen

Nach dem Deployment im Railway Terminal:

```bash
python migrations/add_email_verification_tokens.py
```

## Alternative Email-Provider

### SendGrid

```env
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=apikey
MAIL_PASSWORD=dein-sendgrid-api-key
MAIL_DEFAULT_SENDER=verified-sender@deine-domain.com
```

### Mailgun

```env
MAIL_SERVER=smtp.mailgun.org
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=postmaster@deine-domain.mailgun.org
MAIL_PASSWORD=dein-mailgun-password
MAIL_DEFAULT_SENDER=noreply@deine-domain.com
```

### AWS SES

```env
MAIL_SERVER=email-smtp.eu-central-1.amazonaws.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=dein-ses-smtp-username
MAIL_PASSWORD=dein-ses-smtp-password
MAIL_DEFAULT_SENDER=verified-email@deine-domain.com
```

## Troubleshooting

### Email wird nicht gesendet

1. **Prüfe Logs**: Schaue in die Konsole auf Fehlermeldungen
2. **SMTP-Credentials**: Doppelcheck von Username/Password
3. **Gmail-Sperre**: Google blockiert manchmal "unsichere Apps" → App-Passwort verwenden!
4. **Port 587 blockiert**: Versuche Port 465 mit `MAIL_USE_SSL=True`
5. **Firewall**: Prüfe ob ausgehende SMTP-Verbindungen erlaubt sind

### Email landet im Spam

1. **SPF-Records**: Setze SPF-Record für deine Domain
2. **DKIM**: Konfiguriere DKIM für bessere Zustellbarkeit
3. **Verified Sender**: Bei Gmail sollte MAIL_DEFAULT_SENDER = MAIL_USERNAME sein
4. **Email-Content**: Vermeide Spam-Wörter wie "FREE", "CLICK HERE" etc.

### Test-Email senden

```python
from app import app, send_email

with app.app_context():
    success = send_email(
        to='test@example.com',
        subject='Test Email',
        template='verify_email',
        username='TestUser',
        verification_link='https://example.com/verify/test-token'
    )
    print(f"Email sent: {success}")
```

## Sicherheit

- **NIEMALS** MAIL_PASSWORD in Git committen!
- `.env` ist in `.gitignore` → wird nicht versioniert
- Für Production nur verified Email-Adressen verwenden
- Rate Limiting für Email-Versand aktivieren (bereits implementiert)

