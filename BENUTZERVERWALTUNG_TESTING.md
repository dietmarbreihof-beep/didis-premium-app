# Testing-Checklist: Produktive Benutzerverwaltung

## Pre-Deployment Checks

### 1. Migration ausführen

```bash
python migrations/add_email_verification_tokens.py
```

**Erwartetes Ergebnis:**
- ✅ Tabelle 'email_verification_tokens' erfolgreich erstellt
- ✅ 7 Spalten: id, user_id, token, token_type, created_at, expires_at, used_at

### 2. Email-Konfiguration testen

**Lokal (.env Datei erstellen):**

```bash
# .env
FLASK_ENV=development
SECRET_KEY=test-secret-key-change-me
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=deine-test-email@gmail.com
MAIL_PASSWORD=dein-app-passwort
MAIL_DEFAULT_SENDER=noreply@didis-academy.com
BASE_URL=http://localhost:5000
```

**Test-Email senden:**

```python
from app import app, send_email

with app.app_context():
    success = send_email(
        to='deine-test-email@gmail.com',
        subject='Test Email',
        template='verify_email',
        username='TestUser',
        verification_link='http://localhost:5000/verify-email/test-token-123'
    )
    print(f"Email sent: {success}")
```

---

## Test-Szenarien

### Szenario 1: Erfolgreiche Registrierung mit Email-Verifizierung

**Schritte:**

1. Navigiere zu `/register`
2. Fülle Formular aus:
   - Username: `testuser1`
   - Email: `test@example.com`
   - Vorname: Test
   - Nachname: User
   - Passwort: `TestPass123!`
   - Passwort bestätigen: `TestPass123!`
   - AGB akzeptieren
3. Klicke "Konto erstellen"

**Erwartetes Ergebnis:**
- ✅ Flash-Message: "Registrierung erfolgreich! Bitte prüfe deine Emails zur Verifizierung."
- ✅ Redirect zu `/login`
- ✅ User in DB mit `email_verified=False`
- ✅ Verification-Token in DB erstellt
- ✅ Verifizierungs-Email gesendet

**Prüfen in DB:**

```python
from app import app, db, User, EmailVerificationToken

with app.app_context():
    user = User.query.filter_by(email='test@example.com').first()
    print(f"User: {user.username}, Verified: {user.email_verified}")
    
    token = EmailVerificationToken.query.filter_by(user_id=user.id).first()
    print(f"Token: {token.token}, Type: {token.token_type}, Valid: {token.is_valid()}")
```

4. Email öffnen und Verifizierungs-Link klicken

**Erwartetes Ergebnis:**
- ✅ User wird zu `/verify-email/<token>` weitergeleitet
- ✅ Flash-Message: "Email erfolgreich bestätigt! Du kannst dich jetzt anmelden."
- ✅ User in DB: `email_verified=True`, `is_active=True`
- ✅ Token als `used_at` markiert
- ✅ Welcome-Email gesendet

5. Login versuchen mit `testuser1` / `TestPass123!`

**Erwartetes Ergebnis:**
- ✅ Erfolgreicher Login
- ✅ Redirect zu `/` (Home)
- ✅ Session enthält User-Daten
- ✅ `subscription_type=FREE`

---

### Szenario 2: Login ohne Email-Verifizierung

**Schritte:**

1. Registriere User (wie Szenario 1)
2. **OHNE** Email zu verifizieren, versuche Login

**Erwartetes Ergebnis:**
- ❌ Login abgelehnt
- ⚠️ Flash-Message: "Bitte bestätige zuerst deine Email-Adresse. Prüfe dein Postfach."
- 🔄 Bleibt auf `/login`

---

### Szenario 3: Abgelaufener Verifizierungs-Token

**Vorbereitung (manuell Token manipulieren):**

```python
from app import app, db, EmailVerificationToken
from datetime import datetime, timedelta

with app.app_context():
    token = EmailVerificationToken.query.first()
    token.expires_at = datetime.utcnow() - timedelta(hours=1)  # Vor 1 Stunde abgelaufen
    db.session.commit()
```

**Schritte:**

1. Klicke auf abgelaufenen Verifizierungs-Link

**Erwartetes Ergebnis:**
- ❌ Verifizierung abgelehnt
- ⚠️ Flash-Message: "Dieser Verifizierungs-Link ist abgelaufen. Bitte registriere dich erneut."
- 🔄 Redirect zu `/register`

---

### Szenario 4: Passwort vergessen & Reset

**Schritte:**

1. Navigiere zu `/login`
2. Klicke "Passwort vergessen?"
3. Gib Email ein: `test@example.com`
4. Klicke "Reset-Link senden"

**Erwartetes Ergebnis:**
- ✅ Flash-Message: "Falls ein Account mit dieser Email existiert, wurde ein Reset-Link gesendet."
- ✅ Redirect zu `/login`
- ✅ Reset-Token in DB erstellt (`token_type='reset_password'`)
- ✅ Reset-Email gesendet

5. Öffne Email und klicke Reset-Link

**Erwartetes Ergebnis:**
- ✅ Redirect zu `/reset-password/<token>`
- ✅ Formular für neues Passwort wird angezeigt

6. Neues Passwort setzen:
   - Passwort: `NewPass456!`
   - Passwort bestätigen: `NewPass456!`

**Erwartetes Ergebnis:**
- ✅ Flash-Message: "Passwort erfolgreich geändert! Du kannst dich jetzt anmelden."
- ✅ Redirect zu `/login`
- ✅ Token als `used_at` markiert
- ✅ Passwort in DB aktualisiert

7. Login mit neuem Passwort: `test@example.com` / `NewPass456!`

**Erwartetes Ergebnis:**
- ✅ Erfolgreicher Login

---

### Szenario 5: Passwort-Validierung

**Schritte:**

1. Registrierung mit schwachem Passwort: `test123`

**Erwartetes Ergebnis:**
- ❌ Registrierung abgelehnt
- ⚠️ Flash-Message: "Passwort muss mindestens einen Großbuchstaben enthalten."

2. Registrierung mit: `Test123`

**Erwartetes Ergebnis:**
- ❌ Registrierung abgelehnt
- ⚠️ Flash-Message: "Passwort muss mindestens ein Sonderzeichen enthalten..."

3. Registrierung mit: `Test123!`

**Erwartetes Ergebnis:**
- ✅ Registrierung erfolgreich

---

### Szenario 6: Passwort-Bestätigung

**Schritte:**

1. Registrierung mit:
   - Passwort: `Test123!`
   - Passwort bestätigen: `Test456!` (unterschiedlich)

**Erwartetes Ergebnis:**
- ❌ Registrierung abgelehnt
- ⚠️ Flash-Message: "Die Passwörter stimmen nicht überein."

---

### Szenario 7: Rate Limiting

**Schritte:**

1. Versuche 4 Registrierungen innerhalb 1 Minute

**Erwartetes Ergebnis:**
- ✅ Erste 3 Registrierungen OK
- ❌ 4. Registrierung abgelehnt
- ⚠️ Error 429: "Too Many Requests"

2. Versuche 6 Login-Versuche innerhalb 1 Minute

**Erwartetes Ergebnis:**
- ✅ Erste 5 Login-Versuche OK
- ❌ 6. Login-Versuch abgelehnt
- ⚠️ Error 429: "Too Many Requests"

3. Versuche 4 Passwort-Reset-Anfragen innerhalb 1 Stunde

**Erwartetes Ergebnis:**
- ✅ Erste 3 Anfragen OK
- ❌ 4. Anfrage abgelehnt
- ⚠️ Error 429: "Too Many Requests"

---

### Szenario 8: Admin-Funktionalität (Nicht betroffen)

**Schritte:**

1. Login als `admin` / `admin` (Demo-Account)

**Erwartetes Ergebnis:**
- ✅ Login erfolgreich (Demo-Accounts umgehen Email-Verifizierung)
- ✅ Subscription: `elite`
- ✅ Admin-Panel erreichbar: `/admin/users`

2. Erstelle neuen User über Admin-Panel

**Erwartetes Ergebnis:**
- ✅ User wird direkt aktiviert (`email_verified=True`)
- ✅ Keine Email-Verifizierung erforderlich
- ✅ Subscription kann direkt gesetzt werden

---

## Security Tests

### CSRF-Protection

**Test:**

```bash
curl -X POST http://localhost:5000/register \
  -d "email=test@example.com&username=test&password=Test123!" \
  --cookie "session=..."
```

**Erwartetes Ergebnis:**
- ❌ Request abgelehnt
- 🔒 Error 400: "CSRF token missing"

### SQL-Injection

**Test:** Username-Feld: `admin' OR '1'='1`

**Erwartetes Ergebnis:**
- ✅ SQLAlchemy verhindert Injection
- ✅ Username wird als String behandelt

---

## Performance Tests

### Token-Generation

**Test:**

```python
import time
from app import app, generate_verification_token

with app.app_context():
    start = time.time()
    for i in range(100):
        token = generate_verification_token(1, 'verify_email')
    end = time.time()
    print(f"100 Tokens generated in {end - start:.2f}s")
```

**Erwartetes Ergebnis:**
- ✅ < 1 Sekunde für 100 Tokens

### Email-Versand

**Test:** Sende 10 Emails hintereinander

**Erwartetes Ergebnis:**
- ✅ Alle Emails versendet
- ⚠️ Prüfe Gmail/SMTP Rate Limits (100 Emails/Tag für Free Gmail)

---

## Deployment-Checks (Railway)

### 1. Environment Variables gesetzt

```bash
railway variables
```

**Muss enthalten:**
- ✅ `MAIL_SERVER`
- ✅ `MAIL_PORT`
- ✅ `MAIL_USE_TLS`
- ✅ `MAIL_USERNAME`
- ✅ `MAIL_PASSWORD`
- ✅ `MAIL_DEFAULT_SENDER`
- ✅ `BASE_URL`
- ✅ `SECRET_KEY` (kryptographisch sicher!)
- ✅ `FLASK_ENV=production`

### 2. Migration ausgeführt

```bash
railway run python migrations/add_email_verification_tokens.py
```

### 3. Test-Registrierung auf Production

1. Öffne `https://didis-premium-app-production.up.railway.app/register`
2. Registriere Test-User
3. Prüfe ob Email ankommt
4. Verifiziere Email
5. Login testen

**Erwartetes Ergebnis:**
- ✅ Alle Schritte funktionieren auf Production
- ✅ HTTPS-only Cookies funktionieren
- ✅ Emails werden zugestellt

---

## Rollback-Plan

Falls etwas schief geht:

### Option 1: Email-Verifizierung temporär deaktivieren

In `app.py` Zeile ~853:

```python
# TEMPORÄR: Für Notfall
email_verified=True  # statt False
```

### Option 2: Alte User manuell aktivieren

```python
from app import app, db, User

with app.app_context():
    users = User.query.filter_by(email_verified=False).all()
    for user in users:
        user.email_verified = True
        user.is_active = True
    db.session.commit()
    print(f"Activated {len(users)} users")
```

### Option 3: Migration rückgängig machen

```python
from app import app, db

with app.app_context():
    db.engine.execute("DROP TABLE email_verification_tokens")
```

---

## Monitoring

### Wichtige Logs prüfen

```bash
# Railway Logs
railway logs

# Suche nach:
grep "Email sent" logs
grep "Email-Fehler" logs
grep "Verifizierung" logs
```

### Metrics tracken

- Registrierungen pro Tag
- Email-Verifizierungsrate (%)
- Passwort-Reset-Anfragen
- Failed Login-Attempts

---

## Bekannte Einschränkungen

1. **Gmail Daily Limit:** 100 Emails/Tag für Free Accounts
2. **Email-Zustellung:** Kann 1-5 Minuten dauern
3. **Spam-Filter:** Erste Emails können im Spam landen
4. **Token-Expiry:** 24h für Verifizierung, 6h für Passwort-Reset

---

## Support-Fragen

**User: "Ich habe keine Email erhalten"**

Antwort:
1. Prüfe Spam-Ordner
2. Warte 5 Minuten
3. Versuche erneute Registrierung (alte Email wird überschrieben)
4. Prüfe ob Email-Adresse korrekt war

**User: "Verifizierungs-Link funktioniert nicht"**

Antwort:
1. Prüfe ob Link abgelaufen ist (24h)
2. Registriere dich erneut
3. Kopiere Link komplett (manchmal werden sie in Emails umgebrochen)

**Admin: "Muss User manuell aktivieren"**

Lösung:

```python
from app import app, db, User

with app.app_context():
    user = User.query.filter_by(email='user@example.com').first()
    user.email_verified = True
    user.is_active = True
    db.session.commit()
```

---

## Erfolgs-Kriterien

- ✅ User kann sich registrieren
- ✅ Email-Verifizierung funktioniert
- ✅ Login nur nach Verifizierung möglich
- ✅ Passwort-Reset funktioniert
- ✅ Alle Passwort-Validierungen greifen
- ✅ Rate Limiting funktioniert
- ✅ CSRF-Protection aktiv
- ✅ Admin-Funktionen unberührt
- ✅ Demo-Accounts funktionieren weiterhin
- ✅ Production-Deployment erfolgreich

