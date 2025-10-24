# ✅ Testing Checklist - Security Features

## 🚀 Quick Test (5 Minuten)

### 1. App starten
```bash
python app.py
```
**Erwartete Ausgabe:**
```
⚠️  WARNING: Kein SECRET_KEY gesetzt. Verwende temporären Key für Development.
[START] Didis Premium Trading Academy mit Menüsystem startet...
```

### 2. CSRF-Schutz testen

**Test 1: Login-Form hat CSRF-Token**
```
1. Browser öffnen: http://localhost:5000/login
2. Rechtsklick → "Seitenquelltext anzeigen"
3. Suche nach: csrf_token
4. ✅ Sollte gefunden werden: <input type="hidden" name="csrf_token" value="...">
```

**Test 2: POST ohne Token wird blockiert**
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email_or_username=admin&password=admin"

# ❌ Erwartete Antwort: 400 Bad Request oder Redirect mit Flash-Message
```

### 3. Rate Limiting testen

**Test: Login Brute-Force Schutz**
```bash
# Führe 6x schnell hintereinander aus:
for i in {1..6}; do
  echo "Versuch $i:"
  curl -s -X POST http://localhost:5000/login \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "email_or_username=wrong&password=wrong" | grep -o "429\|200"
done

# ✅ Erwartet:
# Versuch 1-5: 200 (oder 302 Redirect)
# Versuch 6: 429 (Too Many Requests)
```

### 4. Password-Validation testen

**Test 1: Schwache Passwörter**
```
Browser: http://localhost:5000/register

Versuche zu registrieren mit:
- Password: "12345678"
  ❌ Erwarteter Fehler: "Passwort muss mindestens einen Großbuchstaben enthalten"

- Password: "password"
  ❌ Erwarteter Fehler: "Dieses Passwort ist zu häufig verwendet"

- Password: "Pass123"
  ❌ Erwarteter Fehler: "Passwort muss mindestens ein Sonderzeichen enthalten"
```

**Test 2: Starkes Passwort**
```
Password: "MySecure#Pass123"
✅ Sollte akzeptiert werden
```

### 5. Change-Password Route testen

**Test 1: Route ist geschützt (Login required)**
```bash
curl -I http://localhost:5000/account/change-password

# ✅ Sollte redirecten zu /login (302)
```

**Test 2: Password ändern**
```
1. Login: http://localhost:5000/login (admin/admin)
2. Gehe zu: http://localhost:5000/account/change-password
3. Formular ausfüllen:
   - Altes Passwort: admin
   - Neues Passwort: NewSecure#123
   - Bestätigen: NewSecure#123
4. ✅ "Passwort erfolgreich geändert!"
5. Logout und login mit neuem Passwort
```

**Test 3: Validierungen**
```
Falsches altes Passwort:
❌ "Altes Passwort ist falsch"

Passwörter stimmen nicht überein:
❌ "Passwörter stimmen nicht überein"

Schwaches neues Passwort ("weak"):
❌ "Passwort muss mindestens 8 Zeichen lang sein"
```

### 6. Admin-Routes testen

**Test: Admin-Required Decorator**
```bash
# Ohne Login:
curl -I http://localhost:5000/admin/modules
# ✅ Sollte redirecten zu /login

# Als nicht-Admin:
# 1. Login als normaler User
# 2. Gehe zu /admin/modules
# ❌ "Zugriff verweigert: Admin-Rechte erforderlich"
```

---

## 📊 Erwartete Ergebnisse (Summary)

| Test | Erwartet | Status |
|------|----------|--------|
| CSRF-Token in Forms | ✅ Vorhanden | ⬜ |
| POST ohne CSRF-Token | ❌ Geblockt | ⬜ |
| Login Rate Limit (6. Versuch) | ❌ 429 Error | ⬜ |
| Register Rate Limit (4. Versuch) | ❌ 429 Error | ⬜ |
| Schwaches Passwort "12345678" | ❌ Abgelehnt | ⬜ |
| Starkes Passwort "Secure#123" | ✅ Akzeptiert | ⬜ |
| Change-Password ohne Login | ❌ Redirect /login | ⬜ |
| Change-Password mit Login | ✅ Funktioniert | ⬜ |
| Admin-Route ohne Login | ❌ Redirect /login | ⬜ |
| Admin-Route als User | ❌ Zugriff verweigert | ⬜ |

---

## 🐛 Häufige Probleme

### "ModuleNotFoundError: No module named 'flask_limiter'"
```bash
pip install Flask-Limiter==3.5.0
```

### "429 Too Many Requests" beim Testen
```
Warte 1 Minute oder starte App neu
(Rate Limiter nutzt In-Memory-Storage)
```

### "CSRF token missing"
```
- Prüfe ob {{ csrf_token() }} im Template ist
- Lösche Browser-Cookies
- Starte App neu
```

---

## ✅ Alle Tests bestanden?

**Wenn JA:**
- ✅ App ist lokal production-ready
- ✅ Kann zu Railway deployed werden
- ✅ Alle Security-Features funktionieren

**Nächste Schritte:**
1. Siehe DEPLOYMENT_GUIDE.md
2. Deploy zu Railway
3. Wiederhole Tests auf Production-URL
