# 🗄️ Database Setup - Didis Trading Academy

## 🚀 Schnell-Setup (Empfohlen)

### Option 1: Automatisches Setup beim App-Start
```bash
python app.py
```
Die Database wird automatisch beim ersten Start initialisiert!

### Option 2: Manuelles Setup-Script
```bash
python init_db.py
```
Führt eine komplette Database-Initialisierung durch.

## 🔧 Erweiterte Optionen

### Admin-Interface verwenden
1. App starten: `python app.py`
2. Als Admin anmelden: `admin/admin`
3. Zu Admin-Panel: http://localhost:5000/admin/modules
4. Button "🗄️ Database initialisieren" klicken

### Manuelle Database-Erstellung (Python Console)
```python
from app import app, db
from database import User, Subscription, Module, ModuleAccess

with app.app_context():
    # Alle Tabellen erstellen
    db.create_all()
    
    # Status prüfen
    print(f"User: {User.query.count()}")
    print("✅ Database bereit!")
```

## 📊 Was wird erstellt?

### Database-Tabellen:
- ✅ **users** - Echte Benutzer-Accounts
- ✅ **subscriptions** - Abo-Verwaltung  
- ✅ **modules** - Lernmodule (aus database.py)
- ✅ **module_access** - Zugriffs-Kontrolle
- ✅ **module_categories** - Modul-Kategorien (aus app.py)
- ✅ **module_subcategories** - Unterkategorien
- ✅ **learning_modules** - Lernmodule (aus app.py)
- ✅ **module_progress** - Fortschritts-Tracking

### Standard-User (bei init_db.py):
- 👤 **admin / admin123** - Administrator
- 👤 **demo / demo123** - Demo-User

### Demo-User (immer verfügbar):
- 👤 **admin / admin** - Elite + Admin
- 👤 **didi / didi** - Elite + Admin
- 👤 **premium / premium** - Premium
- 👤 **test / test** - Premium

## 🔍 Troubleshooting

### Problem: "User-Tabelle nicht verfügbar"
```bash
# Database neu erstellen
rm didis_academy.db
python init_db.py
```

### Problem: "Import-Fehler"
```bash
# Dependencies installieren
pip install python-dotenv
```

### Problem: "Permission denied"
- Prüfen Sie Dateiberechtigungen
- Schließen Sie andere App-Instanzen
- Als Administrator ausführen

## ✅ Erfolgs-Check

Nach dem Setup sollten Sie sehen:
```
✅ Database-Tabellen erstellt!
📊 Anzahl User in Database: X
✅ Demo-Module erstellt!
✅ Streamlit-Module migriert!
```

## 🎯 Nächste Schritte

1. **App starten:** `python app.py`
2. **Browser öffnen:** http://localhost:5000
3. **Registrieren:** Neues Konto erstellen
4. **Oder Demo:** admin/admin für sofortigen Zugang
5. **Admin-Panel:** http://localhost:5000/admin/modules

## 📞 Support

Bei Problemen:
1. Prüfen Sie die Konsolen-Ausgabe
2. Löschen Sie die .db-Datei und starten neu
3. Stellen Sie sicher, dass alle Dependencies installiert sind

