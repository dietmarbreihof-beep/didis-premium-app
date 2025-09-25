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

