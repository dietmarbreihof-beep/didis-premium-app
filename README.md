# 🏆 Didis Premium Trading Academy

Eine moderne Flask-basierte Web-Applikation für eine Premium Trading-Akademie mit interaktiven Lernmodulen, Benutzerauthentifizierung und Subscription-Management.

## ✨ Features

### 🎓 Lernmanagementsystem
- **Interaktive Lernmodule** mit progressiver Freischaltung
- **3-Ebenen-Navigationssystem** (Kategorien → Unterkategorien → Module)
- **Fortschritts-Tracking** mit personalisierten Lernpfaden
- **Integrierte Quizzes** mit sofortigem Feedback
- **Dynamische Inhalte** mit Jinja2-Templates

### 🔐 Benutzerauthentifizierung
- **Sichere Registrierung** mit Email-Verifizierung
- **Session-Management** mit konfigurierbaren Timeouts
- **Passwort-Hashing** mit Werkzeug Security
- **Rollen-basierte Zugriffskontrolle** (Admin/Premium/Basic)

### 💳 Subscription-System
- **Flexible Mitgliedschaftsmodelle** (Basic, Premium)
- **Automatische Modul-Freischaltung** basierend auf Subscription
- **Upgrade-Mechanismus** mit nahtloser Erfahrung
- **Subscription-Status-Tracking**

### 🎨 Modern Design System
- **Gold-Akzente** für Premium-Gefühl (#b8860b, #daa520, #f4e97b)
- **Dunkle Farbpalette** für professionelles Aussehen
- **Responsive Design** für alle Geräte
- **Smooth Animationen** und Übergänge
- **Glasmorphismus-Effekte** für moderne Optik

### 🛠️ Admin-Panel
- **Benutzerverwaltung** mit Rollen-Zuweisungen
- **Modul-Management** mit Drag & Drop Sortierung
- **Subscription-Übersicht** und -verwaltung
- **Analytics Dashboard** (geplant)

## 🚀 Tech Stack

- **Backend:** Flask 3.0.0 + SQLAlchemy 2.0.23
- **Frontend:** Jinja2 Templates + Vanilla CSS/JS
- **Datenbank:** SQLite (Development) / PostgreSQL (Produktion)
- **Authentifizierung:** Session-basiert mit Werkzeug
- **Deployment:** Docker + Gunicorn (geplant)

## 📁 Projekt-Struktur

```
didis-premium-app/
├── app.py                 # Haupt-Flask-App
├── database.py            # Datenbankmodelle und -konfiguration
├── requirements_extended.txt  # Python-Dependencies
├── templates/             # Jinja2-Templates
│   ├── base.html         # Basis-Template
│   ├── home.html         # Startseite
│   ├── auth/             # Authentifizierungs-Templates
│   ├── module/           # Lernmodul-Templates
│   └── admin/            # Admin-Panel-Templates
├── static/               # Statische Dateien (CSS, JS, Bilder)
└── instance/            # App-Instanz-Dateien (Datenbank, Logs)
```

## 🔧 Installation & Setup

### Voraussetzungen
- Python 3.9+
- pip
- Git

### 1. Repository klonen
```bash
git clone https://github.com/[dein-username]/didis-premium-app.git
cd didis-premium-app
```

### 2. Virtual Environment erstellen
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Dependencies installieren
```bash
pip install -r requirements_extended.txt
```

### 4. Umgebungsvariablen konfigurieren
Erstelle eine `.env` Datei:
```bash
SECRET_KEY=dein-super-sicherer-secret-key-hier
DATABASE_URL=sqlite:///didis_academy.db
FLASK_ENV=development
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@domain.com
MAIL_PASSWORD=<GENERATE_VIA_GOOGLE_APP_PASSWORDS>
```

### 5. Datenbank initialisieren
```bash
python init_db.py
```

### 6. App starten
```bash
python app.py
```

Die App ist dann unter `http://localhost:5000` erreichbar.

## 👤 Demo-Accounts

### Admin-Account
- **Username:** `admin`
- **Passwort:** `admin`
- **Berechtigung:** Vollzugriff auf alle Features

### Premium-Account
- **Username:** `didi`
- **Passwort:** `didi`
- **Berechtigung:** Zugriff auf alle Lernmodule

### Basic-Account  
- **Username:** `newbie`
- **Passwort:** `newbie`
- **Berechtigung:** Limitierter Zugriff

## 🎯 Lernmodule

### 📈 Trading-Grundlagen
- **Support & Resistance** - AVWAP-basierte Analyse
- **Chart-Patterns** - Erkennung und Trading
- **Risk Management** - Position Sizing mit Kelly-Formel

### 🧠 Trading-Psychologie
- **Meta-Learning** - Wie man das Lernen lernt
- **Emotionskontrolle** - Disziplin im Trading
- **Mindset-Entwicklung** - Erfolgreiche Denkweise

### 🔍 Technische Analyse
- **Candlestick-Patterns** - Interpretation und Anwendung
- **Indikatoren** - Moving Averages, RSI, MACD
- **Volume-Analyse** - Bestätigung von Preisbewegungen

### 📊 Fundamentalanalyse
- **Unternehmensanalyse** - Bewertungsmethoden
- **Marktanalyse** - Sektorrotation und Trends
- **Makroökonomie** - Einflüsse auf die Märkte

## 🛡️ Sicherheitsfeatures

### 🔐 Authentifizierung
- ✅ **Passwort-Hashing** mit Werkzeug
- ✅ **Session-Sicherheit** mit sicheren Cookies
- ✅ **CSRF-Schutz** (in Entwicklung)
- ⚠️ **Rate-Limiting** (geplant)

### 🔒 Datenschutz
- **DSGVO-konform** geplant
- **Minimal data collection** Prinzip
- **Sichere Datenlagerung**
- **Audit-Logs** (geplant)

## 🚀 Roadmap

### Phase 1: Sicherheit (In Arbeit) ⚠️
- [ ] CSRF-Schutz implementieren
- [ ] Rate-Limiting gegen Brute-Force
- [ ] Security Headers konfigurieren
- [ ] Input-Validierung verstärken

### Phase 2: Features (Q1 2025)
- [ ] Email-Verifizierung
- [ ] Passwort-Reset-Funktionalität
- [ ] Two-Factor Authentication
- [ ] Erweiterte Analytics

### Phase 3: Skalierung (Q2 2025)
- [ ] PostgreSQL-Migration
- [ ] Redis für Sessions
- [ ] Celery für Background-Tasks
- [ ] Docker-Containerisierung

### Phase 4: Premium-Features (Q3 2025)
- [ ] Live-Trading-Integration
- [ ] Real-time Notifications
- [ ] Community-Features
- [ ] Mobile App

## 🤝 Contributing

Beiträge sind willkommen! Bitte:

1. Fork das Repository
2. Erstelle einen Feature-Branch (`git checkout -b feature/AmazingFeature`)
3. Committe deine Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Push zum Branch (`git push origin feature/AmazingFeature`)
5. Öffne einen Pull Request

## 📝 License

Dieses Projekt ist unter der MIT License lizenziert. Siehe `LICENSE` Datei für Details.

## 📞 Support

Bei Fragen oder Problemen:
- 📧 **Email:** support@didis-academy.com  
- 🐛 **Issues:** GitHub Issues Tab
- 📖 **Dokumentation:** Wiki (in Entwicklung)

## 🙏 Acknowledgments

- **Flask Community** für das großartige Framework
- **SQLAlchemy** für die ORM-Unterstützung
- **Bootstrap** für die UI-Komponenten
- **Trading-Community** für Feedback und Ideen

---

<div align="center">
  <strong>🚀 Gemacht mit ❤️ für erfolgreiche Trader</strong>
</div>
