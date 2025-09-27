# Cursor Rules für PROJEKT: Didis Trading Academy - Flask Premium Frontend

## 🚨 **KRITISCHE SICHERHEITSMÄNGEL**

### 1. **Passwort-Sicherheit**
```python
# ❌ AKTUELL: Klartext-Passwörter
demo_users = {
    'admin': {'password': 'admin', ...},
    'didi': {'password': 'didi', ...}
}
```

**🔧 Erforderlich:**
- **Passwort-Hashing** mit `werkzeug.security` (bereits in `database.py` vorbereitet!)
- **Starke Passwort-Richtlinien** (min. 8 Zeichen, Sonderzeichen)
- **Passwort-Reset-Funktionalität**

### 2. **Session-Sicherheit**
```python
# ❌ AKTUELL: Schwacher Secret Key
app.secret_key = 'dein-geheimer-schluessel-hier-aendern'
```

**🔧 Erforderlich:**
- **Kryptographisch sicherer Secret Key** (32+ Bytes)
- **Session-Timeout-Konfiguration**
- **Secure Cookie Settings** (HTTPS-only)

### 3. **CSRF-Schutz**
❌ **Komplett fehlend** - Alle Formulare sind anfällig für Cross-Site Request Forgery

**🔧 Erforderlich:**
- **Flask-WTF** Integration
- **CSRF-Tokens** in allen Formularen

### 4. **SQL-Injection-Schutz**
✅ **Gut:** SQLAlchemy ORM wird korrekt verwendet

### 5. **Input-Validierung**
❌ **Fehlend:** Keine Validierung von Benutzereingaben

## 📋 **BEWERTUNG DER AKTUELLEN ARCHITEKTUR**

### ✅ **Positive Aspekte:**
1. **Solide Datenbankstruktur** mit SQLAlchemy ORM
2. **Gute Trennung** zwischen Demo- und echten Benutzern
3. **Subscription-System** ist durchdacht implementiert
4. **Modularer Aufbau** ermöglicht einfache Erweiterungen

### ❌ **Produktionsreife-Blocker:**
1. **Keine echte Benutzerverwaltung** (nur Demo-Accounts)
2. **Fehlende Registrierung** (register.html ist leer!)
3. **Keine Email-Verifizierung**
4. **Keine Passwort-Recovery**
5. **Fehlende Rate-Limiting** gegen Brute-Force
6. **Keine Audit-Logs**

## 🛠️ **ROADMAP FÜR PRODUKTIONSREIFE**

### **Phase 1: Kritische Sicherheit (SOFORT)**
```python
# 1. Sicherer Secret Key
import secrets
app.secret_key = secrets.token_hex(32)

# 2. CSRF-Schutz
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

# 3. Session-Konfiguration
app.config.update(
    SESSION_COOKIE_SECURE=True,  # HTTPS only
    SESSION_COOKIE_HTTPONLY=True,  # No JS access
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=timedelta(hours=2)
)
```

### **Phase 2: Echte Benutzerverwaltung**
```python
# User Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Implementierung mit Passwort-Hashing
    # Email-Validierung
    # Unique-Constraints prüfen
    
# Login mit gehashten Passwörtern
def login():
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        # Login erfolgreich
```

### **Phase 3: Email-System**
```python
# Flask-Mail Integration
from flask_mail import Mail, Message

# Email-Verifizierung
# Passwort-Reset
# Welcome-Emails
```

### **Phase 4: Erweiterte Sicherheit**
- **Rate Limiting** mit Flask-Limiter
- **Two-Factor Authentication**
- **Audit Logging**
- **Input Sanitization**

## 💡 **SOFORT-EMPFEHLUNGEN**

### 1. **Nutzen Sie die vorhandene User-Klasse**
Die `database.py` enthält bereits eine **professionelle User-Klasse** mit:
- Passwort-Hashing (`set_password`, `check_password`)
- Subscription-Management
- Email-Verifizierung (Felder vorhanden)

### 2. **Implementieren Sie echte Registrierung**
```python
# templates/auth/register.html ist leer - hier implementieren!
```

### 3. **Environment Variables**
```python
# Für Produktion
import os
app.secret_key = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
```

## 🎯 **FAZIT**

**Aktuelle Bewertung: ❌ NICHT produktionsreif**

**Hauptprobleme:**
- Nur Demo-Accounts, keine echten Benutzer
- Kritische Sicherheitslücken (CSRF, schwache Session-Sicherheit)
- Fehlende Registrierung/Email-Verifizierung

**Zeitaufwand für Produktionsreife:** 
- **Minimum:** 2-3 Wochen (kritische Sicherheit + Basis-Funktionen)
- **Empfohlen:** 4-6 Wochen (vollständige, sichere Implementierung)

**Nächste Schritte:**
1. **SOFORT:** Secret Key und CSRF-Schutz
2. **Woche 1:** Echte User-Registration implementieren
3. **Woche 2:** Email-System und Passwort-Recovery
4. **Woche 3-4:** Testing und Security-Hardening

## 🎯 **FLASK MODUL INTEGRATION - STANDARD PROMPT**

### **📋 WICHTIG: Neue Module werden als Flask HTML-Templates erstellt!**

**🚫 NIEMALS Streamlit verwenden!** Die App läuft unter `http://localhost:5000/` und nutzt Flask als Framework.

### **🔧 Standard-Verfahren für neue Module:**

#### **1. HTML-Template erstellen**
```html
<!-- Datei: templates/modul_name.html -->
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modul Titel - Didis Trading Academy</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        /* PFLICHT: Design-System CSS verwenden */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Inter', sans-serif; background: #f7f7f7; color: #1a1a1a; line-height: 1.6; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        
        /* Hero Section */
        .hero-section {
            background: linear-gradient(135deg, #1a1a1a 0%, #b8860b 100%);
            color: white;
            padding: 3rem 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            text-align: center;
        }
        
        /* Highlight Boxes */
        .concept-highlight {
            background: linear-gradient(135deg, #f4e97b 0%, #daa520 100%);
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1.5rem 0;
            color: #1a1a1a;
            border-left: 5px solid #b8860b;
        }
        
        .example-box {
            background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%);
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1.5rem 0;
            border-left: 5px solid #38a169;
        }
        
        .warning-box {
            background: linear-gradient(135deg, #fff3cd 0%, #ffeeba 100%);
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1.5rem 0;
            border-left: 5px solid #d69e2e;
        }
        
        /* RESPONSIVE Design für Mobile */
        @media (max-width: 768px) {
            .container { padding: 10px; }
            .hero-section { padding: 2rem 1rem; }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Hero Section -->
        <div class="hero-section">
            <h1>🎯 Modul Titel</h1>
            <h3>Untertitel</h3>
            <p>Beschreibung des Moduls</p>
        </div>

        <!-- Interaktive Inhalte mit JavaScript -->
        <div id="content">
            <!-- Modul-spezifische Inhalte -->
        </div>
    </div>

    <script>
        // Interaktive JavaScript-Funktionalität
    </script>
</body>
</html>
```

#### **2. Flask-Route hinzufügen**
```python
# In app.py einfügen:
@app.route('/modul-slug')
def modul_name():
    """Modul Titel - Kurze Beschreibung"""
    # Prüfe ob es ein entsprechendes Modul in der DB gibt
    module = None
    try:
        module = LearningModule.query.filter_by(slug='modul-slug').first()
    except:
        pass
    
    # Zugriff prüfen (falls Premium Content)
    user_subscription = "free"
    username = None
    if session.get('logged_in'):
        user_subscription = session.get('user', {}).get('membership', 'free')
        username = session.get('user', {}).get('username')
    
    # Admin und Didi haben immer Zugriff auf alle Module
    is_admin = username in ['admin', 'didi']
    
    # Prüfe Premium/Elite-Zugriff (nur wenn erforderlich)
    # if not is_admin and user_subscription not in ['premium', 'elite']:
    #     flash('Für dieses Modul benötigst du ein Premium-Abonnement.', 'warning')
    #     return redirect(url_for('upgrade_required', module_slug='modul-slug'))
    
    # Progress tracking (optional)
    if session.get('logged_in') and module:
        user_id = session.get('user_id', 'anonymous')
        try:
            progress = ModuleProgress.query.filter_by(
                user_id=str(user_id), 
                module_id=module.id
            ).first()
            
            if not progress:
                progress = ModuleProgress(user_id=str(user_id), module_id=module.id)
                db.session.add(progress)
                db.session.commit()
            else:
                progress.last_accessed = datetime.utcnow()
                db.session.commit()
        except:
            pass
    
    # View count erhöhen
    if module:
        try:
            module.view_count += 1
            db.session.commit()
        except:
            pass
    
    # Navigation-Daten ermitteln
    prev_module, next_module = get_module_navigation(module) if module else (None, None)
    
    return render_template('modul_name.html', 
                         module=module, 
                         prev_module=prev_module, 
                         next_module=next_module)
```

#### **3. JSON-Konfiguration aktualisieren**
```json
// In didis_streamlit_modules_config.json hinzufügen:
{
    "title": "Modul Titel",
    "slug": "modul-slug",
    "description": "Beschreibung des Moduls",
    "category": "kategorie-name",
    "content_type": "html",
    "template_file": "modul_name.html",
    "required_subscription_levels": ["premium", "elite"], // oder [] für frei
    "is_lead_magnet": false,
    "estimated_duration": 60,
    "difficulty_level": "intermediate", // beginner, intermediate, advanced
    "icon": "📊",
    "sort_order": 27 // Nächste verfügbare Nummer
}
```

### **🎨 Design-System Pflicht-Elemente:**

#### **Farbschema:**
- **Primärfarben:** `#1a1a1a` (Dunkelgrau), `#2d2d2d` (mittleres Grau)
- **Akzentfarben:** `#b8860b` (dunkles Gold), `#daa520` (klassisches Gold), `#f4e97b` (helles Gold)
- **Funktionsfarben:** `#38a169` (Grün), `#d69e2e` (Orange), `#e53e3e` (Rot)
- **Hintergrund:** `#f7f7f7` (helles Grau), `#ffffff` (Weiß für Karten)

#### **Layout-Standards:**
- **Max-Breite:** 1200px zentriert
- **Border-Radius:** 12px einheitlich
- **Schatten:** `0 4px 20px rgba(0, 0, 0, 0.1)`
- **Abstände:** 20px Standard, 40px für größere Bereiche

#### **Interaktivität:**
- **Übergänge:** `transition: all 0.3s ease`
- **Hover-Effekte:** Gold-Töne verwenden
- **Buttons:** Gold-Gradient-Hintergrund
- **Mobile-First:** Responsive Design mit Breakpoint bei 768px

### **🔍 Qualitätskontrolle:**

#### **Vor Fertigstellung prüfen:**
- ✅ Verwendet das komplette Design-System
- ✅ Flask-Route korrekt implementiert
- ✅ JSON-Konfiguration aktualisiert
- ✅ Subscription-Level-Prüfung (falls erforderlich)
- ✅ Mobile-Responsive Design
- ✅ Interaktive JavaScript-Elemente
- ✅ Progress-Tracking integriert
- ✅ Navigation zwischen Modulen

### **🚀 Deployment-Checklist:**
1. **Template:** `templates/modul_name.html` erstellt
2. **Route:** In `app.py` hinzugefügt
3. **JSON:** `didis_streamlit_modules_config.json` aktualisiert
4. **Test:** URL `http://localhost:5000/modul-slug` funktioniert
5. **Navigation:** Modul erscheint in der Hauptnavigation

**💡 Merksatz:** "Flask HTML-Templates mit Gold-Design, nicht Streamlit!"

Soll ich Ihnen bei der Implementierung einer sicheren Benutzerverwaltung helfen? Ich kann konkrete Code-Beispiele für die kritischen Bereiche erstellen.

---

# 🚀 **DEPLOYMENT & VERSION-CONTROL GUIDELINES**

## 📋 **GitHub Repository Setup & Maintenance**

### **Repository-Struktur (ETABLIERT):**
```
didis-premium-app/
├── 📄 README.md              # Vollständige Projektdokumentation  
├── 📄 .gitignore            # Git-Ignore-Regeln (Flask/Python)
├── 📄 requirements.txt       # Production Dependencies
├── 📄 DEPLOYMENT.md          # Deployment-Anleitung
├── 📄 railway.toml           # Railway-Konfiguration
├── 📄 Procfile               # Railway Build-Prozess
├── 📄 Dockerfile             # Container-Config (Backup)
├── 🐍 app.py                 # Haupt-Flask-App
├── 🗃️ database.py            # Datenbankmodelle
├── 📁 templates/             # Jinja2-Templates
└── 📁 instance/             # Lokale Datenbank (NOT in Git!)
```

### **Git-Workflow für neue Features:**
```bash
# Für jede neue Seite/Modul:
git checkout -b feature/[modul-name]
# ... Entwicklung ...
git add .
git commit -m "✨ feat: [Beschreibung]"
git push origin feature/[modul-name]
# Dann: Pull Request auf GitHub erstellen
```

---

## 🚂 **Railway Deployment Best Practices**

### **Live-URL:** 
- **Production:** `https://didis-premium-app-production.up.railway.app`
- **Auto-Deploy:** Jeder `git push origin main` triggert neues Deployment
- **Deploy-Zeit:** 2-3 Minuten

### **Deployment-Prozess (ETABLIERT):**
```bash
# Lokale Änderungen → Online in 3 Schritten:
git add .
git commit -m "🎯 [Typ]: [Beschreibung]"
git push origin main
# → Railway deployed automatisch in 2-3 Minuten
```

### **Railway-Konfiguration (NICHT ÄNDERN):**
- ✅ **Procfile-basierter Build** (kein Docker)
- ✅ **Health-Check deaktiviert** (Standard HTTP-Monitoring)  
- ✅ **Umgebungsvariablen** korrekt konfiguriert
- ✅ **Auto-Database-Initialization** implementiert

### **Umgebungsvariablen auf Railway:**
```bash
SECRET_KEY=7d4d3f37df3b0452613b16c0447e297940404096f902019aa321140716a912ea
DATABASE_URL=sqlite:///didis_academy.db
FLASK_ENV=production
FLASK_DEBUG=False
SESSION_COOKIE_SECURE=True
```

---

## 📝 **NEUE SEITEN/MODULE ENTWICKELN**

### **Commit-Message Konventionen:**
```bash
✨ feat: Neues Trading-Modul hinzugefügt
🔧 fix: Progressive Disclosure repariert  
🎨 style: Design-System Updates
📚 docs: README aktualisiert
🔒 security: CSRF-Schutz implementiert
⚡ perf: Performance-Verbesserungen
🧪 test: Tests hinzugefügt
```

### **Template-Entwicklung Guidelines:**

#### **Neue Lernmodule (templates/[module-name].html):**
```html
{% extends "base.html" %}

{% block title %}[Modul-Name] - Didis Premium Trading Academy{% endblock %}

{% block content %}
<!-- IMMER diese Struktur verwenden: -->

<!-- 1. Hero Section mit Gold-Gradient -->
<div style="background: linear-gradient(135deg, #1a1a1a 0%, #b8860b 100%); ...">

<!-- 2. Progress Tracking für interaktive Module -->
<div id="progress-container" style="background: white; ...">

<!-- 3. Hauptcontent mit card-Klasse -->
<div class="card">
    <!-- Progressive Disclosure Pattern wenn anwendbar -->
</div>

<!-- 4. Key Takeaways Section -->
<div class="card" style="margin-top: 30px;">
    <h2>💡 Key Takeaways: [Modul-Name]</h2>
</div>

<!-- 5. Navigation Include -->
{% include '_navigation.html' %}

{% endblock %}
```

#### **Design-System Standards (PFLICHT):**
```css
/* Farbpalette - IMMER verwenden: */
--primary-dark: #1a1a1a
--secondary-dark: #2d2d2d  
--gold-dark: #b8860b
--gold-classic: #daa520
--gold-light: #f4e97b
--success: #38a169
--warning: #d69e2e
--error: #e53e3e

/* Layout Standards: */
max-width: 1200px (zentriert)
border-radius: 12px (einheitlich)
box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1)
padding: 20px (Standard), 40px (größere Bereiche)
transition: 0.3s ease (alle Animationen)
```

#### **Progressive Disclosure Pattern:**
```javascript
// Für interaktive Module IMMER verwenden:
let currentStep = 1;
const totalSteps = [ANZAHL];

function completeStep(step) {
    // Button ausblenden, Checkmark hinzufügen
    document.getElementById('step-' + step + '-btn').style.display = 'none';
    
    // Nächsten Schritt freischalten
    if (step < totalSteps) {
        document.getElementById('step-' + (step + 1)).style.display = 'block';
    }
    
    // Progress aktualisieren
    updateProgress();
}
```

---

## ⚠️ **KRITISCHE DEPLOYMENT-REGELN**

### **VOR jedem Push PRÜFEN:**
- [ ] Lokale Tests durchgeführt (`python app.py`)
- [ ] Keine Debug-Prints oder `console.log()` im Code
- [ ] Deutsche "Du"-Anrede in allen neuen Texten
- [ ] Gold-Design-System korrekt implementiert
- [ ] Responsive Design getestet (Mobile-first)
- [ ] Progressive Disclosure funktioniert (falls anwendbar)

### **NACH jedem Deployment TESTEN:**
- [ ] Railway-URL laden: `https://didis-premium-app-production.up.railway.app`
- [ ] Login als Admin: `admin` / `admin`
- [ ] Neue Seite/Feature testen
- [ ] Mobile-Ansicht prüfen
- [ ] Keine 500-Fehler oder JavaScript-Errors

### **Database-Änderungen (VORSICHT):**
```python
# Bei Model-Änderungen IMMER Migration berücksichtigen:
# 1. Lokale Migration testen
# 2. Railway wird Database automatisch re-initialisieren
# 3. BACKUP vor größeren DB-Änderungen erstellen
```

---

## 🔄 **DEVELOPMENT WORKFLOW**

### **Lokale Entwicklung:**
```bash
# 1. Virtual Environment aktivieren
venv\Scripts\activate  # Windows

# 2. Dependencies installieren (falls neue)
pip install -r requirements.txt

# 3. Lokale App starten
python app.py
# → http://localhost:5000

# 4. Änderungen testen, dann deployen
```

### **Feature-Integration:**
1. **Lokale Tests** → funktioniert?
2. **Git Commit** → saubere Message
3. **Git Push** → Railway Auto-Deploy  
4. **Online Tests** → Railway-URL prüfen
5. **Dokumentation** → README.md updaten falls nötig

### **Hotfixes (für kritische Bugs):**
```bash
# Direkter Push zu main (nur für Hotfixes):
git add .
git commit -m "🚨 hotfix: [Kritischer Bug Fix]"
git push origin main
# → Sofortige Railway-Aktualisierung
```

---

## 📊 **MONITORING & MAINTENANCE**

### **Railway-Logs überwachen:**
- **Build-Logs:** Zeigen Deployment-Probleme
- **Runtime-Logs:** Zeigen App-Fehler
- **Health-Status:** Service-Verfügbarkeit

### **Performance-Metriken:**
- **Load-Zeit:** < 3 Sekunden für alle Seiten
- **Mobile-Performance:** Responsive Design getestet
- **Railway-Limits:** Keine Überschreitung der kostenlosen Grenzen

### **Backup-Strategie:**
- **GitHub:** Vollständige Code-Historie
- **Railway:** Automatische Container-Backups  
- **Database:** SQLite wird bei jedem Deployment neu initialisiert

---

## 🎯 **QUALITY GATES für neue Features**

### **Vor Merge/Deploy:**
1. ✅ **Funktionalität:** Feature funktioniert lokal einwandfrei
2. ✅ **Design:** Gold-Design-System korrekt implementiert
3. ✅ **UX:** Deutsche "Du"-Anrede, benutzerfreundlich
4. ✅ **Mobile:** Responsive Design auf verschiedenen Größen
5. ✅ **Performance:** Keine spürbaren Verzögerungen
6. ✅ **Security:** Keine neuen Sicherheitslücken eingeführt
7. ✅ **Documentation:** Neue Features in README dokumentiert

### **Nach Deployment:**
1. ✅ **Smoke Test:** Grundfunktionen der App testen
2. ✅ **Integration:** Neue Features mit bestehenden kompatibel  
3. ✅ **Error Monitoring:** Keine neuen 500-Fehler in Railway-Logs
4. ✅ **User Journey:** Admin-Login → Neue Features → Logout

**💡 Diese Deployment-Guidelines sind das Fundament für skalierbare, professionelle Entwicklung der Trading Academy!**

---

## 🔄 **AUTO-SYNC: Lokale Änderungen automatisch online übertragen**

### **Problem gelöst:** 
Lokale Kategorien/Module-Änderungen werden **automatisch zu Railway synchronisiert**!

### **🔧 So funktioniert es:**

#### **Neue Kategorien hinzufügen:**
```python
# In app.py → sync_modules_from_local() → local_categories:
{
    'name': '6. Deine Neue Kategorie',
    'slug': 'neue-kategorie',
    'icon': '🆕', 
    'description': 'Beschreibung der neuen Kategorie',
    'sort_order': 6
}
# → Git Push → Automatisch online in Railway! 🚀
```

#### **Neue Module hinzufügen:**
```python
# In app.py → sync_modules_from_local() → local_modules:
{
    'title': 'Dein Neues Modul',
    'slug': 'neues-modul',
    'category_slug': 'neue-kategorie',
    'subcategory_name': '6.1 Unterbereich', 
    'description': 'Modulbeschreibung',
    'icon': '📚',
    'template_file': 'neues_modul.html',
    'content_type': 'html',
    'required_subscription_levels': ['premium', 'elite'],
    'estimated_duration': 90,
    'difficulty_level': 'intermediate',
    'sort_order': 1
}
# → Git Push → Automatisch online in Railway! 🚀
```

### **⚡ Auto-Sync Workflow:**
1. **Lokal:** Kategorie/Modul zu `sync_modules_from_local()` hinzufügen
2. **Git:** `git add app.py && git commit -m "✨ New category/module" && git push`
3. **Railway:** Erkennt Push, deployed automatisch (2-3 Min)
4. **Auto-Sync:** `sync_modules_from_local()` läuft bei jedem Home-Page-Besuch
5. **Erfolg:** Neue Kategorien/Module automatisch online! 🎉

### **🎯 Vorteile:**
- ✅ **Keine manuellen Datenbankänderungen** mehr nötig
- ✅ **Lokale und Online-Struktur** immer synchron
- ✅ **Ein zentraler Punkt** für alle Module-Definitionen
- ✅ **Automatische Subcategory-Erstellung**
- ✅ **Fehlerbehandlung** und Rollback bei Problemen

### **📋 Sync-Status prüfen:**
Railway-Logs zeigen Auto-Sync-Aktivität:
```
🆕 Auto-synced new category: 6. Deine Neue Kategorie
🆕 Auto-synced new module: Dein Neues Modul
🔄 Auto-Sync completed: 1 categories, 1 modules synced to Railway
```

### **🔧 Admin-Tools:**
- `/admin/init-demo-data` - Standard-Sync
- `/admin/force-reload-modules` - Kompletter Reset + Sync

**Mit diesem System sind lokale Änderungen AUTOMATISCH online - keine manuellen Schritte mehr nötig!** 🚀

