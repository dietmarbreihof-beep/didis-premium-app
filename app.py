# app.py - Didis Premium Trading Academy mit Menüsystem
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os
import enum
import secrets
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Environment Variables laden
load_dotenv()

# App-Konfiguration
app = Flask(__name__)

# Sicherheitskonfiguration - Persistent Secret Key
SECRET_KEY_FILE = os.path.join(os.path.dirname(__file__), '.secret_key')

# Secret Key aus ENV, File oder neu generieren
if os.environ.get('SECRET_KEY'):
    app.secret_key = os.environ.get('SECRET_KEY')
    print("[CONFIG] Secret Key aus Environment Variable geladen")
elif os.path.exists(SECRET_KEY_FILE):
    try:
        with open(SECRET_KEY_FILE, 'r') as f:
            app.secret_key = f.read().strip()
        print("[CONFIG] Secret Key aus .secret_key Datei geladen")
    except Exception as e:
        print(f"[WARNING] Fehler beim Laden des Secret Keys: {e}")
        app.secret_key = secrets.token_hex(32)
else:
    # Neuen Secret Key generieren und speichern
    app.secret_key = secrets.token_hex(32)
    try:
        with open(SECRET_KEY_FILE, 'w') as f:
            f.write(app.secret_key)
        # Nur Owner lesbar/schreibbar (Unix-Systeme)
        if os.name != 'nt':  # Nicht Windows
            os.chmod(SECRET_KEY_FILE, 0o600)
        print(f"[CONFIG] Neuer Secret Key generiert und gespeichert in {SECRET_KEY_FILE}")
    except Exception as e:
        print(f"[WARNING] Konnte Secret Key nicht speichern: {e}")

# Session-Konfiguration
app.config.update(
    SESSION_COOKIE_SECURE=True if os.environ.get('RAILWAY_ENVIRONMENT') else False,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=timedelta(hours=2),
    SESSION_REFRESH_EACH_REQUEST=True
)

# Database-Pfad konfigurieren
basedir = os.path.abspath(os.path.dirname(__file__))

# Nutze PostgreSQL wenn DATABASE_URL gesetzt ist (Railway), sonst SQLite
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # Fix: Railway nutzt postgres://, aber SQLAlchemy braucht postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Lokales SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'didis_academy.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database initialisieren
db = SQLAlchemy(app)

# CSRF-Schutz initialisieren (mit Exemptions für API-Routes)
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

# Exempt API und JSON-Routes von CSRF (werden via andere Methoden geschützt)
csrf.exempt('health_check')
csrf.exempt('setup_demo_users')
csrf.exempt('emergency_admin_setup')
csrf.exempt('debug_modules')
csrf.exempt('api_modules_search')

print("[SECURITY] CSRF-Schutz aktiviert (mit API-Exemptions)")

# Analytics-Modell direkt definieren (für korrekte db-Instanz)
class VisitorAnalytics(db.Model):
    """Tracking für Besucher-Analytics mit IP-basierter Deduplizierung"""
    __tablename__ = 'visitor_analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Visitor Information
    ip_address = db.Column(db.String(45), nullable=False)  # IPv6 support
    user_agent = db.Column(db.Text)
    
    # Page Information
    page_url = db.Column(db.String(500), nullable=False)
    page_title = db.Column(db.String(200))
    referrer = db.Column(db.String(500))
    
    # Session Information
    session_id = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Null für anonyme Besucher
    
    # Timestamps
    visited_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Geographic Information (optional)
    country = db.Column(db.String(2))  # ISO country code
    city = db.Column(db.String(100))
    
    # Device Information
    device_type = db.Column(db.String(20))  # mobile, desktop, tablet
    browser = db.Column(db.String(50))
    os = db.Column(db.String(50))
    
    def to_dict(self):
        return {
            'id': self.id,
            'ip_address': self.ip_address,
            'page_url': self.page_url,
            'page_title': self.page_title,
            'visited_at': self.visited_at.isoformat() if self.visited_at else None,
            'user_id': self.user_id,
            'device_type': self.device_type,
            'browser': self.browser,
            'os': self.os
        }

print("VisitorAnalytics-Modell definiert")

# Analytics-Middleware direkt implementieren
def track_visitor():
    """Einfache Visitor-Tracking Funktion"""
    # Prüfe ob Request getrackt werden soll
    static_extensions = ['.css', '.js', '.ico', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.woff', '.woff2', '.ttf']
    if any(request.path.endswith(ext) for ext in static_extensions):
        return
    
    if request.path.startswith('/api/'):
        return
    
    # Bot-Erkennung
    user_agent = request.headers.get('User-Agent', '').lower()
    bot_patterns = ['bot', 'crawler', 'spider', 'scraper', 'curl', 'wget']
    if any(pattern in user_agent for pattern in bot_patterns):
        return
    
    try:
        # Client-IP ermitteln
        if request.headers.get('X-Forwarded-For'):
            ip_address = request.headers.get('X-Forwarded-For').split(',')[0].strip()
        elif request.headers.get('X-Real-IP'):
            ip_address = request.headers.get('X-Real-IP')
        elif request.headers.get('CF-Connecting-IP'):
            ip_address = request.headers.get('CF-Connecting-IP')
        else:
            ip_address = request.remote_addr or '127.0.0.1'
        
        # Session-ID generieren
        if 'analytics_session_id' not in session:
            import uuid
            session['analytics_session_id'] = str(uuid.uuid4())
        
        # Device-Type bestimmen (einfache Version)
        user_agent_string = request.headers.get('User-Agent', '')
        if 'mobile' in user_agent_string.lower():
            device_type = 'mobile'
        elif 'tablet' in user_agent_string.lower():
            device_type = 'tablet'
        else:
            device_type = 'desktop'
        
        # Page-Title mapping
        page_titles = {
            '/': 'Home - Didis Premium Trading Academy',
            '/login': 'Login - Didis Premium Trading Academy',
            '/admin/analytics': 'Analytics Dashboard - Didis Premium Trading Academy',
            '/trading-tools': 'Trading-Tools - Didis Premium Trading Academy'
        }
        
        # Analytics-Eintrag erstellen
        analytics_entry = VisitorAnalytics(
            ip_address=ip_address,
            user_agent=user_agent_string[:500] if user_agent_string else None,  # Limit für DB
            page_url=request.url,
            page_title=page_titles.get(request.path, f"Seite {request.path} - Didis Premium Trading Academy"),
            referrer=request.headers.get('Referer'),
            session_id=session['analytics_session_id'],
            user_id=session.get('user_id'),
            device_type=device_type,
            browser='Unknown',
            os='Unknown'
        )
        
        db.session.add(analytics_entry)
        db.session.commit()
        
    except Exception as e:
        # Fehler beim Tracking sollen die App nicht crashen
        print(f"Analytics Tracking Error: {e}")
        db.session.rollback()

# Registriere die Tracking-Funktion
app.before_request(track_visitor)
print("Analytics-Tracking aktiviert")

# === SMART INITIALIZATION (NUR beim ersten Start!) ===
def init_modules_on_startup():
    """
    Smart Initialization - lädt Module NUR beim ersten Start
    
    WICHTIG: 
    - Prüft ob Datenbank bereits Module enthält
    - Wenn leer: Lädt Seed-Daten (siehe init_demo_modules)
    - Wenn nicht leer: Nur Validierung, KEINE Überschreibung!
    
    Admin-Route für manuelle Sync: /admin/sync-modules-from-code
    """
    try:
        with app.app_context():
            # Prüfe ob Module existieren
            try:
                module_count = LearningModule.query.count()
                category_count = ModuleCategory.query.count()
            except Exception as db_error:
                print(f"[DB] Datenbank-Fehler beim Zählen: {db_error}")
                # Tabellen existieren nicht - erstellen
                db.create_all()
                module_count = 0
                category_count = 0
            
            if module_count == 0 and category_count == 0:
                # Erste Installation: Seed Daten laden
                print("\n" + "="*60)
                print("[INIT] Erste Installation erkannt - lade Seed-Daten")
                print("="*60)
                init_demo_modules()
                db.session.commit()
                print("[INIT] Seed-Daten erfolgreich geladen")
                print("="*60 + "\n")
            else:
                # Normale Operation: Nur Status ausgeben
                print(f"[INIT] Datenbank bereits initialisiert:")
                print(f"       - {category_count} Kategorien")
                print(f"       - {module_count} Module")
                print(f"[INIT] Keine automatische Sync - Admin-Änderungen bleiben erhalten")
                
                # Optional: Validiere Datenkonsistenz
                validate_module_integrity()
            
            # Prüfe ob Demo-User existieren (wichtig für Railway!)
            user_count = User.query.count()
            if user_count == 0:
                print("[INIT] Keine Benutzer gefunden - erstelle Demo-User...")
                create_demo_users_on_startup()
                print("[INIT] ✅ Demo-User erstellt")
            
            # WICHTIG: Stelle sicher dass "Neue Module" Kategorie IMMER existiert
            ensure_neue_module_category()
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Fehler bei Init: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def validate_module_integrity():
    """
    Validiert die Integrität der Modul-Daten
    Prüft auf verwaiste Module, fehlende Kategorien etc.
    """
    try:
        # Prüfe auf Module ohne Kategorie
        orphaned_modules = LearningModule.query.filter_by(category_id=None).all()
        if orphaned_modules:
            print(f"[WARNING] {len(orphaned_modules)} Module ohne Kategorie gefunden")
        
        # Prüfe auf Module mit ungültiger Kategorie
        all_modules = LearningModule.query.all()
        all_category_ids = {cat.id for cat in ModuleCategory.query.all()}
        
        invalid_category_modules = []
        for mod in all_modules:
            if mod.category_id and mod.category_id not in all_category_ids:
                invalid_category_modules.append(mod.title)
        
        if invalid_category_modules:
            print(f"[WARNING] {len(invalid_category_modules)} Module mit ungültiger Kategorie:")
            for title in invalid_category_modules[:5]:  # Nur erste 5 zeigen
                print(f"           - {title}")
        
        if not orphaned_modules and not invalid_category_modules:
            print("[VALIDATION] Modul-Integrität OK")
            
    except Exception as e:
        print(f"[WARNING] Validierung fehlgeschlagen: {e}")

def create_demo_users_on_startup():
    """
    Erstellt Demo-User automatisch beim ersten Start
    ROBUST: UPSERT-Logik, detaillierte Fehlerbehandlung, garantierte Admin-Erstellung
    """
    demo_users_data = [
        {'username': 'admin', 'email': 'admin@didis-academy.com', 'password': 'admin', 
         'first_name': 'Admin', 'last_name': 'User'},
        {'username': 'didi', 'email': 'didi@didis-academy.com', 'password': 'didi',
         'first_name': 'Dietmar', 'last_name': 'Breihof'},
        {'username': 'premium', 'email': 'premium@didis-academy.com', 'password': 'premium',
         'first_name': 'Premium', 'last_name': 'User'},
        {'username': 'test', 'email': 'test@didis-academy.com', 'password': 'test',
         'first_name': 'Test', 'last_name': 'User'}
    ]
    
    created_count = 0
    updated_count = 0
    
    for user_data in demo_users_data:
        try:
            # UPSERT: Prüfe ob User bereits existiert
            existing_user = User.query.filter_by(username=user_data['username']).first()
            
            if existing_user:
                print(f"[INIT]    - {user_data['username']} existiert bereits (ID: {existing_user.id})")
                # Optional: Passwort aktualisieren (für Development)
                # existing_user.set_password(user_data['password'])
                # updated_count += 1
                continue
            
            # Erstelle neuen User
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                is_active=True,
                email_verified=True
            )
            user.set_password(user_data['password'])
            db.session.add(user)
            created_count += 1
            print(f"[INIT]    - {user_data['username']} ✅ NEU erstellt")
            
        except Exception as e:
            print(f"[ERROR] Fehler beim Erstellen von {user_data['username']}: {e}")
            db.session.rollback()
            continue
    
    try:
        db.session.commit()
        print(f"[INIT] Demo-User Erstellung abgeschlossen: {created_count} neu, {updated_count} aktualisiert")
        return True
    except Exception as e:
        print(f"[ERROR] Demo-User Commit fehlgeschlagen: {e}")
        db.session.rollback()
        return False

def ensure_neue_module_category():
    """
    Stellt sicher dass die geschützte 'Neue Module' Kategorie existiert
    Diese Kategorie wird für unkategorisierte Module verwendet
    """
    neue_module = ModuleCategory.query.filter_by(slug='neue-module').first()
    
    if not neue_module:
        print("[INIT] Erstelle geschützte 'Neue Module' Kategorie...")
        neue_module = ModuleCategory(
            name='🆕 Neue Module',
            slug='neue-module',
            icon='🆕',
            description='Automatisch erkannte Module - Bitte in die richtige Kategorie verschieben',
            sort_order=999,
            is_active=True,
            is_protected=True  # Geschützt - kann nicht gelöscht werden!
        )
        db.session.add(neue_module)
        db.session.commit()
        print("[INIT] ✅ 'Neue Module' Kategorie erstellt (geschützt)")
    elif not neue_module.is_protected:
        # Falls existiert aber nicht geschützt: Schutz aktivieren
        neue_module.is_protected = True
        db.session.commit()
        print("[INIT] ✅ 'Neue Module' Kategorie jetzt geschützt")
    else:
        print("[INIT] ✅ 'Neue Module' Kategorie bereits vorhanden und geschützt")
    
    return neue_module

# ❌ WICHTIG: Automatische Sync bei Startup wurde DEAKTIVIERT
# Grund: Überschreibt Admin-Änderungen in der Datenbank!
# Lösung: Nur beim ersten Start (leere DB) werden Seed-Daten geladen
# Für manuelle Sync: Admin-Route /admin/sync-modules-from-code verwenden

# === USER MODELS ===

from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    
    # Account Status
    is_active = db.Column(db.Boolean, default=True)
    email_verified = db.Column(db.Boolean, default=True)  # Für einfache Registrierung
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def subscription_type(self):
        """Gibt den aktuellen Subscription-Typ zurück - für Demo FREE"""
        return SubscriptionType.FREE

# === MENÜSYSTEM MODELS ===

class SubscriptionType(enum.Enum):
    FREE = "free"
    BASIC = "basic" 
    PREMIUM = "premium"  # 30-Minuten-Depot
    ELITE = "elite"      # 5-Minuten-Depot + VIP
    MASTERCLASS = "masterclass"

class ModuleCategory(db.Model):
    """Hauptkategorien wie 'Fundamentalanalyse', 'Technische Analyse'"""
    __tablename__ = 'module_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    icon = db.Column(db.String(20), default="📊")
    description = db.Column(db.Text)
    sort_order = db.Column(db.Integer, default=100)
    is_active = db.Column(db.Boolean, default=True)
    is_protected = db.Column(db.Boolean, default=False)  # Geschützte Kategorien (z.B. "Neue Module")
    
    # Relationships
    subcategories = db.relationship('ModuleSubcategory', backref='category', lazy=True)
    modules = db.relationship('LearningModule', backref='category', lazy=True)
    
    def to_dict(self, include_unpublished=False):
        """
        Konvertiert Kategorie zu Dictionary
        
        Args:
            include_unpublished (bool): Wenn True, werden auch unpublished Module inkludiert (für Admin)
        """
        # Alle Module in dieser Kategorie (published oder alle)
        if include_unpublished:
            all_modules = self.modules
        else:
            all_modules = [mod for mod in self.modules if mod.is_published]
        
        # Module ohne Unterkategorie (direkte Module)
        direct_modules = [mod for mod in all_modules if mod.subcategory_id is None]
        
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'icon': self.icon,
            'description': self.description,
            'sort_order': self.sort_order,
            'is_protected': self.is_protected,
            'subcategories': [sub.to_dict(include_unpublished) for sub in self.subcategories if sub.is_active],
            'modules': [mod.to_dict() for mod in all_modules],
            'direct_modules': [mod.to_dict() for mod in direct_modules]
        }

class ModuleSubcategory(db.Model):
    """Unterkategorien wie '1.1 Bilanzanalyse', '1.2 Kennzahlen'"""
    __tablename__ = 'module_subcategories'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('module_categories.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(20), default="📋")
    sort_order = db.Column(db.Integer, default=100)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    modules = db.relationship('LearningModule', backref='subcategory', lazy=True)
    
    def to_dict(self, include_unpublished=False):
        """
        Konvertiert Unterkategorie zu Dictionary
        
        Args:
            include_unpublished (bool): Wenn True, werden auch unpublished Module inkludiert (für Admin)
        """
        if include_unpublished:
            modules = self.modules
        else:
            modules = [mod for mod in self.modules if mod.is_published]
        
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'icon': self.icon,
            'sort_order': self.sort_order,
            'modules': [mod.to_dict() for mod in modules]
        }

class LearningModule(db.Model):
    """Einzelne Lernmodule"""
    __tablename__ = 'learning_modules'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('module_categories.id'), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('module_subcategories.id'), nullable=True)
    
    # Modul Info
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(20), default="🎯")
    
    # Content
    template_file = db.Column(db.String(200))  # z.B. "magic_line.html"
    content_type = db.Column(db.String(50), default="html")  # html, video, pdf, streamlit
    external_url = db.Column(db.String(500))  # Für Streamlit-Integration
    
    # Access Control
    is_published = db.Column(db.Boolean, default=True)  # GEÄNDERT: Default TRUE (Module sofort sichtbar für Admins)
    is_lead_magnet = db.Column(db.Boolean, default=False)
    required_subscription_levels = db.Column(db.JSON, default=list)  # ["premium", "elite"]
    
    # Lead-Magnet Settings
    lead_magnet_form_url = db.Column(db.String(500))
    lead_magnet_email_template = db.Column(db.Text)
    
    # Sorting & Meta
    sort_order = db.Column(db.Integer, default=100)
    estimated_duration = db.Column(db.Integer, default=30)  # Minuten
    difficulty_level = db.Column(db.String(20), default="beginner")  # beginner, intermediate, advanced
    
    # Tracking
    view_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user_progress = db.relationship('ModuleProgress', backref='module', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'description': self.description,
            'icon': self.icon,
            'content_type': self.content_type,
            'is_lead_magnet': self.is_lead_magnet,
            'required_subscription_levels': self.required_subscription_levels,
            'estimated_duration': self.estimated_duration,
            'difficulty_level': self.difficulty_level,
            'sort_order': self.sort_order
        }
    
    def user_has_access(self, user_subscription="free"):
        """Prüft ob User Zugriff hat"""
        if self.is_lead_magnet:
            return True
        return user_subscription in self.required_subscription_levels

class ModuleProgress(db.Model):
    """User Progress Tracking"""
    __tablename__ = 'module_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)  # Session-ID oder User-ID
    module_id = db.Column(db.Integer, db.ForeignKey('learning_modules.id'), nullable=False)
    
    progress_percentage = db.Column(db.Integer, default=0)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# === AUTO-ZUORDNUNG: Module ohne Kategorie (NACH Model-Definitionen!) ===
from sqlalchemy import event, text

@event.listens_for(LearningModule, 'before_insert')
def auto_assign_neue_module_category(mapper, connection, target):
    """
    Ordnet Module ohne Kategorie automatisch zu 'Neue Module' zu
    Verhindert dass Module "verloren" gehen
    """
    if target.category_id is None:
        print(f"[AUTO-ASSIGN] Modul '{target.title}' ohne Kategorie - ordne zu 'Neue Module' zu")
        
        # Finde "Neue Module" Kategorie ID (direkt via SQL weil wir in before_insert Hook sind)
        result = connection.execute(
            text("SELECT id FROM module_categories WHERE slug = :slug"),
            {"slug": "neue-module"}
        ).first()
        
        if result:
            target.category_id = result[0]
            print(f"[AUTO-ASSIGN] ✅ Modul '{target.title}' → Neue Module (ID: {result[0]})")
        else:
            print(f"[WARNING] 'Neue Module' Kategorie nicht gefunden! Modul bleibt ohne Kategorie.")

# === MENÜ HELPER FUNCTIONS ===

def get_menu_structure():
    """Lädt die komplette Menüstruktur für die Navigation"""
    try:
        categories = ModuleCategory.query.filter_by(is_active=True).order_by(ModuleCategory.sort_order).all()
        return [cat.to_dict() for cat in categories]
    except:
        return []

def get_accessible_modules_count(user_subscription="free"):
    """Zählt verfügbare Module für User"""
    try:
        all_modules = LearningModule.query.filter_by(is_published=True).all()
        accessible = 0
        lead_magnets = 0
        
        for module in all_modules:
            if module.is_lead_magnet:
                lead_magnets += 1
                accessible += 1
            elif user_subscription in module.required_subscription_levels:
                accessible += 1
        
        return {
            'total': len(all_modules),
            'accessible': accessible,
            'lead_magnets': lead_magnets
        }
    except:
        return {'total': 0, 'accessible': 0, 'lead_magnets': 0}

@app.context_processor
def inject_menu():
    """Template-Kontext für alle Templates verfügbar machen"""
    menu_structure = get_menu_structure()
    
    # User Subscription ermitteln
    user_subscription = "free"
    if session.get('logged_in'):
        user_subscription = session.get('user', {}).get('membership', 'free')
    
    # Modul-Statistiken
    stats = get_accessible_modules_count(user_subscription)
    
    return {
        'menu_structure': menu_structure,
        'total_modules': stats['total'],
        'accessible_modules': stats['accessible'],
        'lead_magnets': stats['lead_magnets']
    }

# === ROUTES ===

# Health Check Endpoint für Railway
@app.route('/health')
def health_check():
    """Health check endpoint für Deployment-Monitoring"""
    try:
        # Prüfe Datenbank-Verbindung (SQLAlchemy 2.0 kompatibel)
        from sqlalchemy import text
        db.session.execute(text('SELECT 1'))
        
        # Prüfe ob Demo-User existieren (für Railway-Deployment)
        user_count = User.query.count()
        
        # KRITISCH: Prüfe ob Admin-User existiert
        admin_user = User.query.filter_by(username='admin').first()
        admin_exists = admin_user is not None
        admin_active = admin_user.is_active if admin_user else False
        
        # Modul-Statistiken
        module_count = LearningModule.query.count()
        category_count = ModuleCategory.query.count()
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'Didis Premium Trading Academy',
            'version': '1.1.0',
            'database': {
                'users': user_count,
                'modules': module_count,
                'categories': category_count
            },
            'auth': {
                'admin_exists': admin_exists,
                'admin_active': admin_active,
                'can_login': admin_exists and admin_active
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/emergency-admin-setup', methods=['GET', 'POST'])
def emergency_admin_setup():
    """
    🚨 NOTFALL: Erstellt Admin-User wenn DB komplett leer ist
    Nur verfügbar wenn KEINE User existieren (Sicherheit!)
    """
    try:
        user_count = User.query.count()
        
        if user_count > 0:
            return jsonify({
                'error': 'Sicherheits-Sperre: User existieren bereits!',
                'user_count': user_count,
                'hint': 'Diese Route ist nur verfügbar wenn die Datenbank komplett leer ist.'
            }), 403
        
        if request.method == 'POST':
            admin_password = request.form.get('password', 'admin')  # Default: admin
            
            # Erstelle Admin-User
            admin = User(
                username='admin',
                email='admin@didis-academy.com',
                first_name='Admin',
                last_name='User',
                is_active=True,
                email_verified=True
            )
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.commit()
            
            print(f"[EMERGENCY] Admin-User erstellt via Emergency-Setup")
            
            return jsonify({
                'success': True,
                'message': 'Admin-User erfolgreich erstellt!',
                'username': 'admin',
                'next_step': 'Bitte melden Sie sich jetzt an: /login'
            }), 200
        
        # GET: Zeige Formular
        return jsonify({
            'info': 'Emergency Admin Setup verfügbar',
            'users_in_db': user_count,
            'instructions': 'POST mit "password" Parameter um Admin zu erstellen'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/setup-demo-users')
def setup_demo_users():
    """
    🔧 VERALTET: Demo-User werden jetzt automatisch beim Start erstellt!
    
    Diese Route existiert nur noch als Fallback für manuelle Erstellung.
    Normalerweise werden Demo-User automatisch erstellt wenn die DB leer ist.
    """
    try:
        # Prüfe ob bereits User existieren
        existing_count = User.query.count()
        if existing_count > 0:
            return jsonify({
                'status': 'already_exists',
                'message': f'{existing_count} Benutzer bereits in Datenbank',
                'info': 'Demo-User wurden bereits automatisch erstellt beim App-Start',
                'note': 'Diese Route ist nicht mehr notwendig - Demo-User werden automatisch erstellt!'
            }), 200
        
        # Fallback: Erstelle Demo-User manuell
        print("[MANUAL] Erstelle Demo-User manuell via /setup-demo-users Route")
        create_demo_users_on_startup()
        
        return jsonify({
            'status': 'success',
            'message': '4 Demo-Benutzer erfolgreich erstellt',
            'users': ['admin', 'didi', 'premium', 'test'],
            'info': 'Sie können sich jetzt mit admin/admin oder didi/didi anmelden',
            'note': 'Zukünftig werden Demo-User automatisch beim App-Start erstellt!'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/')
def home():
    """Startseite mit verfügbaren Modulen"""
    try:
        # Ensure database is initialized
        db.create_all()
        
        # WICHTIG: Keine automatische Sync mehr!
        # Module werden nur beim ersten Start (leere DB) oder manuell via Admin geladen
        # Siehe: /admin/sync-modules-from-code für manuelle Sync
        
        # Lead-Magnete für nicht-eingeloggte User
        if not session.get('logged_in'):
            try:
                lead_magnets = LearningModule.query.filter_by(
                    is_published=True,
                    is_lead_magnet=True
                ).order_by(LearningModule.sort_order).limit(6).all()
            except Exception as e:
                print(f"Database error for lead magnets: {e}")
                lead_magnets = []
            
            return render_template('home.html', 
                                 featured_modules=lead_magnets,
                                 show_signup_cta=True)
    
        # Für eingeloggte User: Persönliche Empfehlungen
        user_subscription = session.get('user', {}).get('membership', 'free')
        
        try:
            # Kürzlich hinzugefügte Module
            recent_modules = LearningModule.query.filter_by(is_published=True).order_by(
                LearningModule.created_at.desc()
            ).limit(3).all()
            
            # Empfohlene Module basierend auf Subscription
            recommended = LearningModule.query.filter(
                LearningModule.is_published == True
            ).order_by(LearningModule.view_count.desc()).limit(3).all()
            
            # Nur Module mit Zugriff
            accessible_recommended = [mod for mod in recommended if mod.user_has_access(user_subscription)]
            
        except Exception as e:
            print(f"Database error for logged in user: {e}")
            recent_modules = []
            accessible_recommended = []
        
        return render_template('home.html',
                             recent_modules=recent_modules,
                             recommended_modules=accessible_recommended,
                             user_subscription=user_subscription)
    
    except Exception as e:
        print(f"Critical error in home route: {e}")
        # Fallback: Simple welcome page
        return f"""
        <h1>🏆 Didis Premium Trading Academy</h1>
        <p>Willkommen! Die App wird gerade initialisiert...</p>
        <p><a href="/login">Zum Login</a></p>
        <p>Error: {e}</p>
        """

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Einfache Benutzer-Registrierung ohne E-Mail-Verifizierung"""
    if request.method == 'POST':
        try:
            # Formulardaten extrahieren
            email = request.form['email'].lower().strip()
            username = request.form['username'].strip()
            password = request.form['password']
            password_confirm = request.form.get('password_confirm', '')
            first_name = request.form.get('first_name', '').strip()
            last_name = request.form.get('last_name', '').strip()
            
            # Validierung
            if len(password) < 8:
                flash('Passwort muss mindestens 8 Zeichen lang sein.', 'error')
                return render_template('auth/register.html')
            
            if password != password_confirm:
                flash('Die Passwörter stimmen nicht überein.', 'error')
                return render_template('auth/register.html')
            
            # Prüfen ob E-Mail bereits existiert
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Diese E-Mail-Adresse ist bereits registriert.', 'error')
                return render_template('auth/register.html')
            
            # Prüfen ob Username bereits existiert
            existing_username = User.query.filter_by(username=username).first()
            if existing_username:
                flash('Dieser Benutzername ist bereits vergeben.', 'error')
                return render_template('auth/register.html')
            
            # Neuen User erstellen
            user = User(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
                email_verified=True  # Sofort aktiv
            )
            user.set_password(password)
            
            # User in Database speichern
            db.session.add(user)
            db.session.commit()
            
            flash('Registrierung erfolgreich! Sie können sich jetzt anmelden.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Fehler bei der Registrierung: {str(e)}', 'error')
    
    return render_template('auth/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Benutzer-Login - erweitert für echte User mit Debug-Logging"""
    if request.method == 'POST':
        email_or_username = request.form['email_or_username']
        password = request.form['password']
        
        print(f"[LOGIN] Login-Versuch: {email_or_username}")
        
        # Zuerst echte User prüfen
        user = None
        if '@' in email_or_username:
            # E-Mail-Login
            user = User.query.filter_by(email=email_or_username.lower()).first()
            print(f"[LOGIN] Email-Suche: {'User gefunden' if user else 'NICHT gefunden'}")
        else:
            # Username-Login
            user = User.query.filter_by(username=email_or_username).first()
            print(f"[LOGIN] Username-Suche: {'User gefunden' if user else 'NICHT gefunden'}")
        
        if not user:
            print(f"[LOGIN] ❌ FEHLER: User '{email_or_username}' nicht in Datenbank!")
            print(f"[LOGIN] Tipp: Verfügbare User: {[u.username for u in User.query.limit(10).all()]}")
            flash('Ungültige Anmeldedaten. Benutzer nicht gefunden.', 'error')
            return render_template('auth/login.html')
        
        if not user.is_active:
            print(f"[LOGIN] ❌ FEHLER: User '{user.username}' ist deaktiviert!")
            flash('Ihr Account wurde deaktiviert. Bitte kontaktieren Sie den Support.', 'error')
            return render_template('auth/login.html')
        
        if not user.check_password(password):
            print(f"[LOGIN] ❌ FEHLER: Falsches Passwort für User '{user.username}'")
            flash('Ungültige Anmeldedaten. Falsches Passwort.', 'error')
            return render_template('auth/login.html')
        
        # Erfolgreicher DB-User Login
        print(f"[LOGIN] ✅ SUCCESS: User '{user.username}' erfolgreich authentifiziert")
        
        session['logged_in'] = True
        session['user_id'] = str(user.id)
        
        # Bestimme Membership (Standard: elite für admin/didi, sonst premium für Test-User)
        if user.username in ['admin', 'didi']:
            membership = 'elite'
        elif user.username in ['premium', 'test']:
            membership = 'premium'
        else:
            # Für echte registrierte User: Prüfe Subscription-System
            # Vorerst default auf 'free'
            membership = 'free'
        
        print(f"[LOGIN] Membership: {membership}")
        
        session['user'] = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'membership': membership
        }
        
        # Last Login aktualisieren
        try:
            user.last_login = datetime.utcnow()
            db.session.commit()
        except Exception as e:
            print(f"[WARNING] Fehler beim Last-Login-Update: {e}")
        
        flash(f'Willkommen zurück, {user.first_name or user.username}!', 'success')
        
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('home'))
    
    return render_template('auth/login.html')

@app.route('/account/change-password', methods=['GET', 'POST'])
def change_password():
    """Passwort ändern für eingeloggte User"""
    if not session.get('logged_in'):
        flash('Bitte melden Sie sich an.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        
        if not user:
            flash('Benutzer nicht gefunden.', 'error')
            return redirect(url_for('home'))
        
        old_password = request.form.get('old_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validierung: Altes Passwort korrekt
        if not user.check_password(old_password):
            flash('Altes Passwort ist falsch.', 'error')
            return render_template('account/change_password.html')
        
        # Validierung: Neue Passwörter identisch
        if new_password != confirm_password:
            flash('Die neuen Passwörter stimmen nicht überein.', 'error')
            return render_template('account/change_password.html')
        
        # Validierung: Mindestlänge
        if len(new_password) < 8:
            flash('Neues Passwort muss mindestens 8 Zeichen lang sein.', 'error')
            return render_template('account/change_password.html')
        
        # Validierung: Nicht identisch mit altem Passwort
        if old_password == new_password:
            flash('Neues Passwort muss sich vom alten unterscheiden.', 'error')
            return render_template('account/change_password.html')
        
        # Passwort ändern
        try:
            user.set_password(new_password)
            db.session.commit()
            
            print(f"[PASSWORD] User '{user.username}' hat Passwort erfolgreich geändert")
            flash('✅ Passwort erfolgreich geändert!', 'success')
            flash('Sie können sich jetzt mit Ihrem neuen Passwort anmelden.', 'info')
            
            # Optional: Session beenden und Neuanmeldung erzwingen
            # session.clear()
            # return redirect(url_for('login'))
            
            return redirect(url_for('home'))
            
        except Exception as e:
            db.session.rollback()
            print(f"[ERROR] Passwort-Änderung fehlgeschlagen: {e}")
            flash(f'Fehler beim Ändern des Passworts: {str(e)}', 'error')
            return render_template('account/change_password.html')
    
    return render_template('account/change_password.html')

@app.route('/logout')
def logout():
    """Benutzer-Logout"""
    session.clear()
    flash('Du wurdest erfolgreich abgemeldet.', 'success')
    return redirect(url_for('home'))

@app.route('/admin/init-demo-data')
def admin_init_demo_data():
    """⚠️ GEFÄHRLICH: Erstellt Demo-Module (kann bestehende überschreiben!)"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        flash('Nur Admins können Demo-Daten initialisieren.', 'error')
        return redirect(url_for('login'))
    
    # Sicherheitsabfrage
    if not request.args.get('confirm') == 'yes':
        flash('⚠️ WARNUNG: Diese Aktion kann bestehende Module überschreiben!', 'warning')
        flash('Fügen Sie ?confirm=yes zur URL hinzu um fortzufahren', 'info')
        return redirect(url_for('admin_modules'))
    
    try:
        # Force database initialization
        db.create_all()
        
        print("[ADMIN] ⚠️ Demo-Module werden erstellt (kann Duplikate erzeugen)")
        
        # Initialize demo modules
        result = init_demo_modules()
        
        flash('✅ Demo-Module erstellt! Prüfen Sie auf Duplikate!', 'warning')
        return redirect(url_for('modules_overview'))
        
    except Exception as e:
        flash(f'❌ Fehler bei Demo-Daten-Initialisierung: {str(e)}', 'error')
        print(f"[ERROR] Admin init error: {str(e)}")
        return redirect(url_for('home'))

@app.route('/admin/force-reload-modules')  
def admin_force_reload_modules():
    """⚠️ EXTREM GEFÄHRLICH: Löscht ALLE Module und lädt Demo-Module neu!"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        flash('Nur Admins können Module neu laden.', 'error')
        return redirect(url_for('login'))
    
    # Doppelte Sicherheitsabfrage
    if not request.args.get('confirm') == 'DELETE-ALL-MODULES':
        flash('⚠️⚠️⚠️ WARNUNG: Diese Aktion LÖSCHT ALLE Kategorien und Module!', 'error')
        flash('Alle manuellen Änderungen gehen unwiderruflich verloren!', 'error')
        flash('Fügen Sie ?confirm=DELETE-ALL-MODULES zur URL hinzu um fortzufahren', 'warning')
        return redirect(url_for('admin_modules'))
    
    try:
        # Clear all existing modules and categories
        print("[ADMIN] ⚠️⚠️⚠️ LÖSCHEN ALLER MODULE UND KATEGORIEN!")
        LearningModule.query.delete()
        ModuleSubcategory.query.delete() 
        ModuleCategory.query.delete()
        db.session.commit()
        
        # Reinitialize everything
        print("[ADMIN] Lade Demo-Module neu...")
        init_demo_modules()
        
        # WICHTIG: Stelle sicher dass "Neue Module" wieder existiert
        ensure_neue_module_category()
        
        flash('⚠️ ALLE Module wurden gelöscht und auf Demo-Stand zurückgesetzt!', 'error')
        flash('Alle manuellen Änderungen sind verloren!', 'warning')
        return redirect(url_for('modules_overview'))
        
    except Exception as e:
        flash(f'❌ Fehler beim Neu-Laden: {str(e)}', 'error')
        print(f"[ERROR] Force reload error: {str(e)}")
        return redirect(url_for('home'))

@app.route('/demo-login')
def demo_login():
    """Demo-Login für verschiedene Subscription-Typen"""
    subscription_type = request.args.get('type', 'free')
    
    demo_users = {
        'free': {'username': 'Demo Free', 'membership': 'free'},
        'basic': {'username': 'Demo Basic', 'membership': 'basic'},
        'premium': {'username': 'Demo Premium', 'membership': 'premium'},
        'elite': {'username': 'Demo Elite', 'membership': 'elite'}
    }
    
    if subscription_type in demo_users:
        session['logged_in'] = True
        session['user_id'] = f'demo-{subscription_type}'
        session['user'] = demo_users[subscription_type]
        session['is_demo'] = True
        
        flash(f'Demo-Login als {subscription_type.title()} User', 'success')
    
    return redirect(url_for('home'))

@app.route('/modules')
def modules():
    """Übersicht aller Module"""
    user_subscription = "free"
    username = None
    if session.get('logged_in'):
        user_subscription = session.get('user', {}).get('membership', 'free')
        username = session.get('user', {}).get('username')
    
    # Admin und Didi haben immer Zugriff auf alle Module
    is_admin = username in ['admin', 'didi']
    
    # Erweiterte Menüstruktur mit direkten Modulen
    try:
        categories = ModuleCategory.query.filter_by(is_active=True).order_by(ModuleCategory.sort_order).all()
        menu_structure = []
        
        for category in categories:
            # Admin sieht ALLE Module (published + unpublished)
            cat_data = category.to_dict(include_unpublished=is_admin)
            
            # Direkte Module (ohne Unterkategorie) hinzufügen
            # ADMIN-MODUS: Admins sehen ALLE Module (auch unpublished)
            if is_admin:
                direct_modules = LearningModule.query.filter_by(
                    category_id=category.id, 
                    subcategory_id=None
                ).order_by(LearningModule.sort_order).all()
            else:
                direct_modules = LearningModule.query.filter_by(
                    category_id=category.id, 
                    subcategory_id=None,
                    is_published=True
                ).order_by(LearningModule.sort_order).all()
            
            cat_data['direct_modules'] = []
            for module in direct_modules:
                module_data = module.to_dict()
                # Admin und Didi haben immer Zugriff
                module_data['user_has_access'] = is_admin or module.user_has_access(user_subscription)
                cat_data['direct_modules'].append(module_data)
            
            # Auch für Module in Unterkategorien den Zugriff prüfen
            for subcat in cat_data['subcategories']:
                for module_data in subcat['modules']:
                    module_obj = LearningModule.query.get(module_data['id'])
                    if module_obj:
                        # Admin und Didi haben immer Zugriff
                        module_data['user_has_access'] = is_admin or module_obj.user_has_access(user_subscription)
            
            menu_structure.append(cat_data)
            
    except Exception as e:
        print(f"Fehler beim Laden der Menüstruktur: {e}")
        menu_structure = get_menu_structure()
    
    # Statistiken berechnen
    stats = get_accessible_modules_count(user_subscription)
    
    return render_template('modules_overview.html', 
                         menu_structure=menu_structure,
                         user_subscription=user_subscription,
                         accessible_modules=stats['accessible'],
                         total_modules=stats['total'],
                         lead_magnets=stats['lead_magnets'])

@app.route('/module/<slug>')
def module_view(slug):
    """Erweiterte Modul-Ansicht"""
    try:
        module = LearningModule.query.filter_by(slug=slug, is_published=True).first()
    except:
        module = None
        
    if not module:
        flash('Modul nicht gefunden.', 'error')
        return redirect(url_for('home'))
    
    # Zugriff prüfen
    user_subscription = "free"
    username = None
    if session.get('logged_in'):
        user_subscription = session.get('user', {}).get('membership', 'free')
        username = session.get('user', {}).get('username')
    
    # Admin und Didi haben immer Zugriff auf alle Module
    is_admin = username in ['admin', 'didi']
    
    if not is_admin and not module.user_has_access(user_subscription):
        flash('Für dieses Modul benötigst du ein Premium-Abonnement.', 'warning')
        return redirect(url_for('upgrade_required', module_slug=slug))
    
    # Progress tracking (optional)
    if session.get('logged_in'):
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
    try:
        module.view_count += 1
        db.session.commit()
    except:
        pass
    

    # Content-Type bestimmen
    if module.content_type == "streamlit" and module.external_url:
        # Streamlit-Module: Weiterleitung zur Streamlit-App
        return redirect(module.external_url)
    elif module.template_file:
        # Prüfe ob es eine standalone HTML-Seite ist (z.B. better-volume-lernseite.html)
        # Diese Seiten haben DOCTYPE und sind komplett eigenständig
        if module.template_file in ['better-volume-lernseite.html']:
            # Standalone HTML direkt ausliefern ohne Template-Engine
            try:
                return send_from_directory('templates', module.template_file)
            except Exception as e:
                # Fallback: Versuche als reguläres Template
                print(f"Fehler beim Laden von standalone HTML: {e}")
                pass
        
        # Bestehende HTML-Templates nutzen (wie magic_line.html)
        # Navigation-Daten ermitteln
        prev_module, next_module = get_module_navigation(module)
        return render_template(module.template_file, 
                             module=module, 
                             prev_module=prev_module, 
                             next_module=next_module)
    else:
        # Standard-Template für neue Module
        # Navigation-Daten ermitteln
        prev_module, next_module = get_module_navigation(module)
        return render_template('module_default.html', 
                             module=module, 
                             prev_module=prev_module, 
                             next_module=next_module)

@app.route('/module/better-volume-indicator')
def better_volume_indicator():
    """Better Volume Indicator - Standalone HTML Page (Lead Magnet)"""
    # Kein Login erforderlich - Lead Magnet
    import os
    try:
        # Lese die HTML-Datei direkt
        template_path = os.path.join(app.root_path, 'templates', 'better-volume-lernseite.html')
        with open(template_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        from flask import Response
        return Response(html_content, mimetype='text/html')
    except Exception as e:
        print(f"Error loading Better Volume page: {e}")
        flash('Modul konnte nicht geladen werden.', 'error')
        return redirect(url_for('home'))

@app.route('/upgrade-required/<module_slug>')
def upgrade_required(module_slug):
    """Upgrade-Seite für gesperrte Module"""
    try:
        module = LearningModule.query.filter_by(slug=module_slug).first()
    except:
        module = None
    return render_template('upgrade_required.html', module=module)

@app.route('/avwap-pinch')
def avwap_pinch():
    """AVWAP Pinch - Interactive Learning Module"""
    # Zugriff prüfen
    if not session.get('logged_in'):
        flash('Bitte melde dich an, um auf dieses Modul zuzugreifen.', 'warning')
        return redirect(url_for('login'))
    
    # Session State für Fortschritt initialisieren
    if 'pinch_step' not in session:
        session['pinch_step'] = 0
    if 'pinch_quiz_scores' not in session:
        session['pinch_quiz_scores'] = {}
    
    return render_template('avwap_pinch.html')

@app.route('/avwap-pinch/update-progress', methods=['POST'])
def avwap_pinch_update_progress():
    """Update progress for AVWAP Pinch module"""
    if not session.get('logged_in'):
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.get_json()
    step = data.get('step', 0)
    quiz_scores = data.get('quiz_scores', {})
    
    # Session State aktualisieren
    session['pinch_step'] = step
    session['pinch_quiz_scores'] = quiz_scores
    session.permanent = True
    
    return jsonify({'success': True, 'step': step})

@app.route('/volume-analyse-grundlagen')
def volume_analyse_grundlagen():
    """Interaktive Lernseite für Volumen-Analyse Grundlagen"""
    track_visitor()  # Analytics
    
    # Zugriff prüfen (optional - kann auch öffentlich sein)
    # if not session.get('logged_in'):
    #     flash('Bitte melde dich an, um auf dieses Modul zuzugreifen.', 'warning')
    #     return redirect(url_for('login'))
    
    return render_template('volume-analyse-grundlagen.html')

@app.route('/symmetrie-trading')
def symmetrie_trading():
    """Interaktive Lernseite für Symmetrie im Trading"""
    track_visitor()  # Analytics
    
    # Zugriff prüfen (optional - kann auch öffentlich sein)
    # if not session.get('logged_in'):
    #     flash('Bitte melde dich an, um auf dieses Modul zuzugreifen.', 'warning')
    #     return redirect(url_for('login'))
    
    return render_template('symmetrie-trading.html')

# Legacy Routes (kompatibel mit bestehender App)

@app.route('/marktampel-allokation')
def marktampel_allokation():
    """Marktampel & Allokation Modul"""
    # Prüfen ob als eigenständige Route oder über Modul-System aufgerufen
    module_slug = 'marktampel-allokation'
    
    try:
        module = LearningModule.query.filter_by(slug=module_slug, is_published=True).first()
    except:
        module = None
    
    # Zugriff prüfen (falls über Modul-System)
    if module:
        user_subscription = "free"
        username = None
        if session.get('logged_in'):
            user_subscription = session.get('user', {}).get('membership', 'free')
            username = session.get('user', {}).get('username')
        
        # Admin und Didi haben immer Zugriff auf alle Module
        is_admin = username in ['admin', 'didi']
        
        if not is_admin and not module.user_has_access(user_subscription):
            flash('Für dieses Modul benötigst du ein Premium-Abonnement.', 'warning')
            return redirect(url_for('upgrade_required', module_slug=module_slug))
        
        # Progress tracking (optional)
        if session.get('logged_in'):
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
        try:
            module.view_count += 1
            db.session.commit()
        except:
            pass
    
    # Navigation-Daten ermitteln
    prev_module, next_module = get_module_navigation(module) if module else (None, None)
    
    return render_template('marktampel_allokation_standalone.html', 
                         module=module, 
                         prev_module=prev_module, 
                         next_module=next_module)

@app.route('/expected-value')
def expected_value():
    """Expected Value (EV) - Trading Konzepte Modul"""
    # Prüfe ob es ein entsprechendes Modul in der DB gibt
    module = None
    try:
        module = LearningModule.query.filter_by(slug='expected-value').first()
    except:
        pass
    
    # Zugriff prüfen (Expected Value ist Premium Content)
    user_subscription = "free"
    username = None
    if session.get('logged_in'):
        user_subscription = session.get('user', {}).get('membership', 'free')
        username = session.get('user', {}).get('username')
    
    # Admin und Didi haben immer Zugriff auf alle Module
    is_admin = username in ['admin', 'didi']
    
    # Prüfe Premium/Elite-Zugriff
    if not is_admin and user_subscription not in ['premium', 'elite']:
        flash('Für dieses Modul benötigst du ein Premium-Abonnement.', 'warning')
        return redirect(url_for('upgrade_required', module_slug='expected-value'))
    
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
    
    return render_template('expected_value.html', 
                         module=module, 
                         prev_module=prev_module, 
                         next_module=next_module)

@app.route('/ev-calculator')
def ev_calculator():
    """Expected Value Rechner - Trading Tool"""
    # Zugriff prüfen (EV-Rechner ist für alle verfügbar)
    user_subscription = "free"
    username = None
    if session.get('logged_in'):
        user_subscription = session.get('user', {}).get('membership', 'free')
        username = session.get('user', {}).get('username')
    
    # Progress tracking für eingeloggte User
    if session.get('logged_in'):
        user_id = session.get('user_id', 'anonymous')
        # Optional: Track tool usage
        pass
    
    return render_template('ev_calculator.html')

@app.route('/Screenshots/<filename>')
def serve_screenshots(filename):
    """Serve screenshot files from templates/Screenshots directory"""
    return send_from_directory('templates/Screenshots', filename)

@app.route('/boersencrash-maerz-2025')
def boersencrash_maerz_2025():
    """Börsencrash März 2025 - Crash-Beispiel Modul aus Grundlagen"""
    # Prüfe ob es ein entsprechendes Modul in der DB gibt
    module = None
    try:
        module = LearningModule.query.filter_by(slug='boersencrash-maerz-2025').first()
    except:
        pass
    
    # Falls kein Modul in DB, erstelle ein temporäres für Template-Kompatibilität
    if not module:
        from types import SimpleNamespace
        module = SimpleNamespace(
            title='Börsencrash März 2025',
            description='Die Vorboten eines historischen Crashs - Eine Fallstudie der dramatischen Ereignisse',
            slug='boersencrash-maerz-2025',
            icon='📉',
            estimated_duration=25,
            difficulty='Grundlagen',
            subscription_requirement='free',  # Für alle verfügbar als Grundlagen-Beispiel
            view_count=1,
            id=999  # Temporäre ID
        )
    
    # Zugriff prüfen (Crash-Beispiel ist für alle verfügbar als Grundlagen-Content)
    user_subscription = "free"
    username = None
    if session.get('logged_in'):
        user_subscription = session.get('user', {}).get('membership', 'free')
        username = session.get('user', {}).get('username')
    
    # Progress tracking (optional)
    if session.get('logged_in') and hasattr(module, 'id') and module.id != 999:
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
    
    # View count erhöhen (nur für echte DB-Module)
    if hasattr(module, 'id') and module.id != 999:
        try:
            real_module = LearningModule.query.get(module.id)
            if real_module:
                real_module.view_count += 1
                db.session.commit()
        except:
            pass
    
    # Navigation-Daten ermitteln
    prev_module, next_module = get_module_navigation(module) if hasattr(module, 'id') and module.id != 999 else (None, None)
    
    return render_template('boersencrash_maerz_2025.html', 
                         module=module, 
                         prev_module=prev_module, 
                         next_module=next_module)

@app.route('/playbook')
def playbook():
    """Trading Mindset Masterclass - Playbook Modul"""
    # Prüfe ob es ein entsprechendes Modul in der DB gibt
    module = None
    try:
        module = LearningModule.query.filter_by(slug='playbook').first()
    except:
        pass
    
    # Falls kein Modul in DB, erstelle ein temporäres für Template-Kompatibilität
    if not module:
        from types import SimpleNamespace
        module = SimpleNamespace(
            title='Trading Mindset Masterclass',
            description='Warum mehr Informationen nicht die Antwort sind',
            slug='playbook',
            icon='🧠',
            estimated_duration=45,
            difficulty_level='intermediate',
            view_count=0
        )
    
    # Zugriff prüfen (Playbook ist Premium Content)
    user_subscription = "free"
    if session.get('logged_in'):
        user_subscription = session.get('user', {}).get('membership', 'free')
    
    # Für Demo-Zwecke erstmal für alle verfügbar
    # if user_subscription == "free":
    #     flash('Für dieses Modul benötigst du ein Premium-Abonnement.', 'warning')
    #     return redirect(url_for('upgrade_required', module_slug='playbook'))
    
    # Progress tracking (optional)
    if session.get('logged_in'):
        user_id = session.get('user_id', 'anonymous')
        try:
            if hasattr(module, 'id'):
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
    if hasattr(module, 'id'):
        try:
            module.view_count += 1
            db.session.commit()
        except:
            pass
    
    # Navigation-Daten ermitteln
    prev_module, next_module = get_module_navigation(module) if module else (None, None)
    
    return render_template('Playbook.html', 
                         module=module, 
                         prev_module=prev_module, 
                         next_module=next_module)

@app.route('/trading-tools')
def trading_tools():
    """Trading-Tools Übersichtsseite"""
    user_subscription = "free"
    if session.get('logged_in'):
        user_subscription = session.get('user', {}).get('membership', 'free')
    
    # Tool-Definitionen mit Status und Zugriffsberechtigung
    tools = [
        {
            'title': 'Trading-Playbook Grundlagen',
            'description': 'Die ultimative Masterclass über Metalearning und den Trading-Prozess. Verstehe wie professionelle Trader wirklich denken und arbeiten.',
            'icon': '👑',
            'url': '/trading-playbook-masterclass',
            'status': 'available',
            'required_subscription': ['elite'],
            'estimated_time': '120 min',
            'difficulty': 'Expert',
            'category': 'Elite - System III'
        },
        {
            'title': 'Trading-Playbook System III',
            'description': 'Professionelle Trade-Vorbereitung nach dem "Mice au Place" System. Von der Marktanalyse bis zur perfekten Trade-Execution.',
            'icon': '📋',
            'url': '/trading-playbook-system-iii',
            'status': 'available',
            'required_subscription': ['premium', 'elite'],
            'estimated_time': '45-60 min',
            'difficulty': 'Fortgeschritten',
            'category': 'Trade-Vorbereitung'
        },
        {
            'title': 'Das Informations-Paradox',
            'description': 'Warum mehr Informationen nicht die Antwort sind. Entwickle das richtige Trading-Mindset.',
            'icon': '🧠',
            'url': '/playbook',
            'status': 'available',
            'required_subscription': ['premium', 'elite'],
            'estimated_time': '45 min',
            'difficulty': 'Fortgeschritten',
            'category': 'Mindset & Psychologie'
        },
        {
            'title': 'Kelly-Simulator',
            'description': 'Berechne die optimale Positionsgröße mit dem Kelly-Kriterium. Interaktiver Rechner und Simulator.',
            'icon': '🧮',
            'url': '/position-sizing-kelly',
            'status': 'available',
            'required_subscription': ['premium', 'elite'],
            'estimated_time': '30 min',
            'difficulty': 'Fortgeschritten',
            'category': 'Risikomanagement'
        },
        {
            'title': 'ABCD Trade-Grades Position Sizing Calculator',
            'description': 'Exponentielles Bet-Sizing für Elite-Trader. Interaktive Lernseite mit Poker-Analogie, 5 Tabs und progressiver Freischaltung. Lerne wie Du A-Trades von D-Trades unterscheidest und Deine Performance exponentiell steigerst.',
            'icon': '🎯',
            'url': '/position-sizing-abcd-calculator',
            'status': 'available',
            'required_subscription': ['premium', 'elite'],
            'estimated_time': '45 min',
            'difficulty': 'Fortgeschritten',
            'category': 'Risikomanagement'
        },
        {
            'title': 'Allokation Asset-Klassen',
            'description': 'Professionelle Portfolio-Analyse mit Marktampel-System und optimaler Asset-Allokation.',
            'icon': '📊',
            'url': '/marktampel-allokation',
            'status': 'available',
            'required_subscription': ['basic', 'premium', 'elite'],
            'estimated_time': '25 min',
            'difficulty': 'Mittel',
            'category': 'Portfolio-Management'
        },
        {
            'title': 'Expected Value Rechner',
            'description': 'Berechne den Erwartungswert deiner Trades. Interaktiver Rechner mit Praxisbeispielen für rationale Trading-Entscheidungen.',
            'icon': '📊',
            'url': '/ev-calculator',
            'status': 'available',
            'required_subscription': [],  # Kostenlos verfügbar
            'estimated_time': '15 min',
            'difficulty': 'Einfach',
            'category': 'Trading Konzepte'
        }
    ]
    
    # Zugriffsberechtigung für jedes Tool prüfen
    for tool in tools:
        # Wenn keine Subscription erforderlich (leere Liste), ist Tool für alle verfügbar
        if not tool['required_subscription']:
            tool['user_has_access'] = True
        else:
            tool['user_has_access'] = user_subscription in tool['required_subscription']
    
    return render_template('trading_tools.html', 
                         tools=tools, 
                         user_subscription=user_subscription)

@app.route('/position-sizing-kelly')
def position_sizing_kelly():
    """Kelly-Kriterium Position Sizing Rechner"""
    # Prüfe ob es ein entsprechendes Modul in der DB gibt
    module = None
    try:
        module = LearningModule.query.filter_by(slug='kelly-kriterium').first()
    except:
        pass
    
    # Falls kein Modul in DB, erstelle ein temporäres für Template-Kompatibilität
    if not module:
        from types import SimpleNamespace
        module = SimpleNamespace(
            title='Kelly-Kriterium: Optimales Position Sizing',
            description='Berechne die optimale Positionsgröße mit dem Kelly-Kriterium',
            slug='kelly-kriterium',
            icon='🧮',
            estimated_duration=30,
            difficulty_level='advanced',
            required_subscription_levels=['premium', 'elite']
        )
    
    # Zugriff prüfen (Kelly-Simulator ist Premium Content)
    user_subscription = session.get('user', {}).get('membership', 'free') if session.get('logged_in') else 'free'
    
    # Für Demo-Zwecke: Alle können zugreifen
    # if user_subscription not in ['premium', 'elite']:
    #     return redirect(url_for('upgrade_required', module_slug='kelly-kriterium'))
    
    # View Count erhöhen
    try:
        if hasattr(module, 'view_count'):
            module.view_count += 1
            db.session.commit()
    except:
        pass
    
    # Navigation-Daten ermitteln
    prev_module, next_module = get_module_navigation(module) if module else (None, None)
    
    return render_template('Position_Sizing_Kelly.html', 
                         module=module, 
                         prev_module=prev_module, 
                         next_module=next_module)

@app.route('/trading-playbook-system-iii')
def trading_playbook_system_iii():
    """Trading-Playbook System III - Professionelle Trade-Vorbereitung"""
    # Prüfe ob es ein entsprechendes Modul in der DB gibt
    module = None
    try:
        module = LearningModule.query.filter_by(slug='trading-playbook-system-iii').first()
    except:
        pass
    
    # Falls kein Modul in DB, erstelle ein temporäres für Template-Kompatibilität
    if not module:
        from types import SimpleNamespace
        module = SimpleNamespace(
            title='Trading-Playbook System III',
            description='Professionelle Trade-Vorbereitung nach dem "Mice au Place" System. Von der Marktanalyse bis zur perfekten Trade-Execution.',
            slug='trading-playbook-system-iii',
            icon='📋',
            estimated_duration=60,
            difficulty_level='advanced',
            required_subscription_levels=['premium', 'elite']
        )
    
    # Zugriff prüfen (Premium Content)
    user_subscription = session.get('user', {}).get('membership', 'free') if session.get('logged_in') else 'free'
    username = session.get('user', {}).get('username') if session.get('logged_in') else None
    
    # Admin und Didi haben immer Zugriff
    is_admin = username in ['admin', 'didi']
    
    # Temporär für Tests deaktiviert - alle Benutzer haben Zugriff
    # if not is_admin and user_subscription not in ['premium', 'elite']:
    #     flash('Für dieses Modul benötigst du ein Premium-Abonnement.', 'warning')
    #     return redirect(url_for('upgrade_required', module_slug='trading-playbook-system-iii'))
    
    # Progress tracking (optional)
    if session.get('logged_in'):
        user_id = session.get('user_id', 'anonymous')
        try:
            if hasattr(module, 'id'):
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
    if hasattr(module, 'id'):
        try:
            module.view_count += 1
            db.session.commit()
        except:
            pass
    
    # Navigation-Daten ermitteln
    prev_module, next_module = get_module_navigation(module) if hasattr(module, 'id') else (None, None)
    
    return render_template('trading_playbook_system_iii.html', 
                         module=module, 
                         prev_module=prev_module, 
                         next_module=next_module)

@app.route('/trading-playbook-masterclass')
def trading_playbook_masterclass():
    """Trading-Playbook Grundlagen - Metalearning & The Process"""
    # Prüfe ob es ein entsprechendes Modul in der DB gibt
    module = None
    try:
        module = LearningModule.query.filter_by(slug='trading-playbook-masterclass').first()
    except:
        pass
    
    # Falls kein Modul in DB, erstelle ein temporäres für Template-Kompatibilität
    if not module:
        from types import SimpleNamespace
        module = SimpleNamespace(
            title='Trading-Playbook Grundlagen - Metalearning & The Process',
            description='Die ultimative Masterclass über Metalearning und den Trading-Prozess. Verstehe wie professionelle Trader wirklich denken und arbeiten.',
            slug='trading-playbook-masterclass',
            icon='👑',
            estimated_duration=120,
            difficulty_level='advanced',
            view_count=0
        )
    
    # Zugriff prüfen (Masterclass ist Elite Content)
    user_subscription = session.get('user', {}).get('membership', 'free') if session.get('logged_in') else 'free'
    username = session.get('user', {}).get('username') if session.get('logged_in') else None
    
    # Admin und Didi haben immer Zugriff
    is_admin = username in ['admin', 'didi']
    
    if not is_admin and user_subscription not in ['elite']:
        flash('Für diese Elite-Masterclass benötigst du ein Elite-Abonnement.', 'warning')
        return redirect(url_for('upgrade_required', module_slug='trading-playbook-masterclass'))
    
    # Progress tracking (optional)
    if session.get('logged_in'):
        user_id = session.get('user_id', 'anonymous')
        try:
            if hasattr(module, 'id'):
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
    if hasattr(module, 'id'):
        try:
            module.view_count += 1
            db.session.commit()
        except:
            pass
    
    # Navigation-Daten ermitteln
    prev_module, next_module = get_module_navigation(module) if hasattr(module, 'id') else (None, None)
    
    return render_template('trading_playbook_masterclass.html', 
                         module=module, 
                         prev_module=prev_module, 
                         next_module=next_module)

@app.route('/bridgewater-quadranten')
def bridgewater_quadranten():
    """Bridgewater Quadranten Masterclass Modul"""
    # Prüfe ob es ein entsprechendes Modul in der DB gibt
    module = None
    try:
        module = LearningModule.query.filter_by(slug='bridgewater-quadranten').first()
    except:
        pass
    
    # Falls kein Modul in DB, erstelle ein temporäres für Template-Kompatibilität
    if not module:
        from types import SimpleNamespace
        module = SimpleNamespace(
            title='Bridgewater Quadranten Masterclass',
            description='Ray Dalios vollständiges Wirtschafts-Framework: Die vier "Jahreszeiten" der Wirtschaft verstehen',
            slug='bridgewater-quadranten',
            icon='📊',
            estimated_duration=90,
            difficulty_level='intermediate',
            view_count=0
        )
    
    # Zugriff prüfen (Bridgewater Quadranten ist Premium Content)
    user_subscription = session.get('user', {}).get('membership', 'free') if session.get('logged_in') else 'free'
    
    # Für Demo-Zwecke: Premium und Elite können zugreifen
    if user_subscription not in ['premium', 'elite'] and hasattr(module, 'required_subscription_levels'):
        flash('Für dieses Modul benötigst du ein Premium-Abonnement.', 'warning')
        return redirect(url_for('upgrade_required', module_slug='bridgewater-quadranten'))
    
    # Progress tracking (optional)
    if session.get('logged_in'):
        user_id = session.get('user_id', 'anonymous')
        try:
            if hasattr(module, 'id'):
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
    if hasattr(module, 'id'):
        try:
            module.view_count += 1
            db.session.commit()
        except:
            pass
    
    # Navigation-Daten ermitteln
    prev_module, next_module = get_module_navigation(module) if module else (None, None)
    
    return render_template('bridgewater_quadranten_complete.html', 
                         module=module, 
                         prev_module=prev_module, 
                         next_module=next_module)

@app.route('/tirone-quadrant-lines')
def tirone_quadrant_lines():
    """Tirone Levels & Quadrant Lines Modul"""
    # Prüfe ob es ein entsprechendes Modul in der DB gibt
    module = None
    try:
        module = LearningModule.query.filter_by(slug='tirone-quadrant-lines').first()
    except:
        pass
    
    # Falls kein Modul in DB, erstelle ein temporäres für Template-Kompatibilität
    if not module:
        from types import SimpleNamespace
        module = SimpleNamespace(
            title='Tirone Levels & Quadrant Lines',
            description='Meistere die wichtigsten TC2000-Indikatoren für präzise Unterstützungs- und Widerstandsanalysen',
            slug='tirone-quadrant-lines',
            icon='📊',
            estimated_duration=75,
            difficulty_level='intermediate',
            view_count=0
        )
    
    # Zugriff prüfen (Premium Content)
    user_subscription = session.get('user', {}).get('membership', 'free') if session.get('logged_in') else 'free'
    
    # Für Demo-Zwecke: Premium und Elite können zugreifen
    if user_subscription not in ['premium', 'elite'] and hasattr(module, 'required_subscription_levels'):
        flash('Für dieses Modul benötigst du ein Premium-Abonnement.', 'warning')
        return redirect(url_for('upgrade_required', module_slug='tirone-quadrant-lines'))
    
    # Progress tracking (optional)
    if session.get('logged_in'):
        user_id = session.get('user_id', 'anonymous')
        try:
            if hasattr(module, 'id'):
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
    if hasattr(module, 'id'):
        try:
            module.view_count += 1
            db.session.commit()
        except:
            pass
    
    # Navigation-Daten ermitteln
    prev_module, next_module = get_module_navigation(module) if hasattr(module, 'id') else (None, None)
    
    return render_template('tirone_quadrant_lines.html', 
                         module=module, 
                         prev_module=prev_module, 
                         next_module=next_module)

@app.route('/position-sizing-abcd-calculator')
def position_sizing_abcd_calculator():
    """ABCD Trade-Grades Position Sizing Calculator"""
    # Prüfe ob es ein entsprechendes Modul in der DB gibt
    module = None
    try:
        module = LearningModule.query.filter_by(slug='position-sizing-abcd-calculator').first()
    except:
        pass
    
    # Falls kein Modul in DB, erstelle ein temporäres für Template-Kompatibilität
    if not module:
        from types import SimpleNamespace
        module = SimpleNamespace(
            title='ABCD Trade-Grades Position Sizing Calculator',
            description='Exponentielles Bet-Sizing für Elite-Trader - Wie Du durch intelligentes Bet-Sizing Deine Trading-Performance exponentiell steigerst',
            slug='position-sizing-abcd-calculator',
            icon='🎯',
            estimated_duration=45,
            difficulty_level='advanced',
            view_count=0
        )
    
    # Zugriff prüfen (Premium Content)
    user_subscription = session.get('user', {}).get('membership', 'free') if session.get('logged_in') else 'free'
    
    # Für Demo-Zwecke: Premium und Elite können zugreifen
    if user_subscription not in ['premium', 'elite'] and hasattr(module, 'required_subscription_levels'):
        flash('Für dieses Modul benötigst du ein Premium-Abonnement.', 'warning')
        return redirect(url_for('upgrade_required', module_slug='position-sizing-abcd-calculator'))
    
    # Progress tracking (optional)
    if session.get('logged_in'):
        user_id = session.get('user_id', 'anonymous')
        try:
            if hasattr(module, 'id'):
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
    if hasattr(module, 'id'):
        try:
            module.view_count += 1
            db.session.commit()
        except:
            pass
    
    # Navigation-Daten ermitteln
    prev_module, next_module = get_module_navigation(module) if hasattr(module, 'id') else (None, None)
    
    return render_template('position_sizing_abcd_calculator.html', 
                         module=module, 
                         prev_module=prev_module, 
                         next_module=next_module)

# === HELPER FUNCTIONS ===

def get_module_navigation(current_module):
    """Ermittelt vorheriges und nächstes Modul für Navigation"""
    if not current_module:
        return None, None
    
    # Prüfe ob es ein echtes Datenbank-Modul ist
    if not hasattr(current_module, 'category_id') or not hasattr(current_module, 'id'):
        # Temporäres Modul (SimpleNamespace) - keine Navigation verfügbar
        return None, None
    
    try:
        # Alle veröffentlichten Module in derselben Kategorie, sortiert nach sort_order
        modules_in_category = LearningModule.query.filter_by(
            category_id=current_module.category_id,
            is_published=True
        ).order_by(LearningModule.sort_order, LearningModule.id).all()
        
        current_index = None
        for i, module in enumerate(modules_in_category):
            if module.id == current_module.id:
                current_index = i
                break
        
        if current_index is None:
            return None, None
    except Exception as e:
        # Bei Fehlern keine Navigation anzeigen
        print(f"Fehler bei Navigation-Ermittlung: {e}")
        return None, None
    
    # Vorheriges Modul
    prev_module = modules_in_category[current_index - 1] if current_index > 0 else None
    
    # Nächstes Modul
    next_module = modules_in_category[current_index + 1] if current_index < len(modules_in_category) - 1 else None
    
    return prev_module, next_module

# === API ROUTES ===

@app.route('/api/check-admin')
def check_admin():
    """API-Route zur Überprüfung des Admin-Status für JavaScript"""
    is_admin = (session.get('logged_in') and 
                session.get('user', {}).get('username') in ['admin', 'didi'])
    return jsonify({'isAdmin': is_admin})

@app.route('/api/debug-session')
def debug_session():
    """Debug-Route zur Überprüfung der Session-Daten (nur für admin/didi)"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify({
        'logged_in': session.get('logged_in'),
        'user_id': session.get('user_id'),
        'user': session.get('user', {}),
        'membership': session.get('user', {}).get('membership'),
        'username': session.get('user', {}).get('username')
    })

# === ADMIN ROUTES ===

@app.route('/admin/modules')
def admin_modules():
    """Admin-Interface für Modul-Management"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        flash('Zugriff verweigert.', 'error')
        return redirect(url_for('home'))
    
    try:
        modules = LearningModule.query.order_by(
            LearningModule.category_id, 
            LearningModule.sort_order
        ).all()
        
        # Alle Kategorien mit Unterkategorien laden
        categories = ModuleCategory.query.order_by(ModuleCategory.sort_order).all()
        
    except:
        modules = []
        categories = []
    
    return render_template('admin/modules.html', modules=modules, categories=categories)

@app.route('/admin/toggle-lead-magnet/<int:module_id>')
def toggle_lead_magnet(module_id):
    """Toggle Lead-Magnet Status eines Moduls"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        return jsonify({'success': False, 'error': 'Admin-Zugriff erforderlich'})
    
    try:
        module = LearningModule.query.get_or_404(module_id)
        module.is_lead_magnet = not module.is_lead_magnet
        if module.is_lead_magnet:
            module.required_subscription_levels = []  # Lead-Magnete sind kostenlos
        db.session.commit()
        return jsonify({'success': True, 'is_lead_magnet': module.is_lead_magnet})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/toggle-published/<int:module_id>')
def toggle_published(module_id):
    """Toggle Published Status eines Moduls"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        return jsonify({'success': False, 'error': 'Admin-Zugriff erforderlich'})
    
    try:
        module = LearningModule.query.get_or_404(module_id)
        module.is_published = not module.is_published
        db.session.commit()
        return jsonify({'success': True, 'is_published': module.is_published})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/update-sort-order', methods=['POST'])
def update_sort_order():
    """Aktualisiere Sortierreihenfolge von Modulen/Kategorien"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        return jsonify({'success': False, 'error': 'Admin-Zugriff erforderlich'})
    
    try:
        data = request.get_json()
        item_type = data.get('type')  # 'category', 'subcategory', 'module'
        items = data.get('items', [])
        
        for item in items:
            if item_type == 'category':
                category = ModuleCategory.query.get(item['id'])
                if category:
                    category.sort_order = item['order']
            elif item_type == 'subcategory':
                subcategory = ModuleSubcategory.query.get(item['id'])
                if subcategory:
                    subcategory.sort_order = item['order']
            elif item_type == 'module':
                module = LearningModule.query.get(item['id'])
                if module:
                    module.sort_order = item['order']
        
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/toggle-category/<int:category_id>')
def toggle_category(category_id):
    """Toggle Active Status einer Kategorie"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        return jsonify({'success': False, 'error': 'Admin-Zugriff erforderlich'})
    
    try:
        category = ModuleCategory.query.get_or_404(category_id)
        category.is_active = not category.is_active
        db.session.commit()
        return jsonify({'success': True, 'is_active': category.is_active})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/toggle-subcategory/<int:subcategory_id>')
def toggle_subcategory(subcategory_id):
    """Toggle Active Status einer Unterkategorie"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        return jsonify({'success': False, 'error': 'Admin-Zugriff erforderlich'})
    
    try:
        subcategory = ModuleSubcategory.query.get_or_404(subcategory_id)
        subcategory.is_active = not subcategory.is_active
        db.session.commit()
        return jsonify({'success': True, 'is_active': subcategory.is_active})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/delete-item', methods=['POST'])
def delete_item():
    """Lösche ein Item (Kategorie, Unterkategorie oder Modul)"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        return jsonify({'success': False, 'error': 'Admin-Zugriff erforderlich'})
    
    try:
        data = request.get_json()
        item_type = data.get('type')
        item_id = data.get('id')
        
        if item_type == 'category':
            category = ModuleCategory.query.get_or_404(item_id)
            # Lösche auch alle Unterkategorien und Module
            for subcategory in category.subcategories:
                for module in subcategory.modules:
                    db.session.delete(module)
                db.session.delete(subcategory)
            db.session.delete(category)
            
        elif item_type == 'subcategory':
            subcategory = ModuleSubcategory.query.get_or_404(item_id)
            # Lösche auch alle Module in dieser Unterkategorie
            for module in subcategory.modules:
                db.session.delete(module)
            db.session.delete(subcategory)
            
        elif item_type == 'module':
            module = LearningModule.query.get_or_404(item_id)
            db.session.delete(module)
        
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/bulk-action', methods=['POST'])
def bulk_action():
    """Führe Bulk-Aktionen auf ausgewählten Items aus"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        return jsonify({'success': False, 'error': 'Admin-Zugriff erforderlich'})
    
    try:
        data = request.get_json()
        action = data.get('action')
        item_type = data.get('type')
        item_ids = data.get('ids', [])
        
        if item_type == 'module':
            modules = LearningModule.query.filter(LearningModule.id.in_(item_ids)).all()
            
            if action == 'publish':
                for module in modules:
                    module.is_published = True
            elif action == 'unpublish':
                for module in modules:
                    module.is_published = False
            elif action == 'lead_magnet':
                for module in modules:
                    module.is_lead_magnet = True
                    module.required_subscription_levels = []
            elif action == 'not_lead_magnet':
                for module in modules:
                    module.is_lead_magnet = False
            elif action == 'delete':
                for module in modules:
                    db.session.delete(module)
        
        db.session.commit()
        return jsonify({'success': True, 'message': f'{len(item_ids)} Items aktualisiert'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/menu-structure')
def admin_menu_structure():
    """Legacy Route - leitet zur neuen einheitlichen Admin-Seite weiter"""
    return redirect(url_for('admin_modules'))

# === ADMIN MENÜ FUNKTIONEN ===

@app.route('/admin/add-category', methods=['POST'])
def add_category():
    """Neue Hauptkategorie hinzufügen"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        flash('Admin-Zugriff erforderlich.', 'error')
        return redirect(url_for('admin_modules'))
    
    try:
        name = request.form.get('name')
        icon = request.form.get('icon', '📊')
        description = request.form.get('description', '')
        
        if not name:
            flash('Name ist erforderlich.', 'error')
            return redirect(url_for('admin_modules'))
        
        # Slug generieren
        slug = name.lower().replace(' ', '-').replace('.', '').replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
        
        # Sort-Order bestimmen
        max_order = db.session.query(db.func.max(ModuleCategory.sort_order)).scalar() or 0
        
        category = ModuleCategory(
            name=name,
            slug=slug,
            icon=icon,
            description=description,
            sort_order=max_order + 1,
            is_active=True
        )
        
        db.session.add(category)
        db.session.commit()
        flash(f'Kategorie "{name}" erfolgreich erstellt!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Fehler beim Erstellen der Kategorie: {str(e)}', 'error')
    
    return redirect(url_for('admin_modules'))

@app.route('/admin/add-subcategory', methods=['POST'])
def add_subcategory():
    """Neue Unterkategorie hinzufügen"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        flash('Admin-Zugriff erforderlich.', 'error')
        return redirect(url_for('admin_modules'))
    
    try:
        category_id = request.form.get('category_id')
        name = request.form.get('name')
        icon = request.form.get('icon', '📁')
        
        if not category_id or not name:
            flash('Kategorie und Name sind erforderlich.', 'error')
            return redirect(url_for('admin_modules'))
        
        # Slug generieren
        slug = name.lower().replace(' ', '-').replace('.', '').replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
        
        # Sort-Order bestimmen
        max_order = db.session.query(db.func.max(ModuleSubcategory.sort_order)).filter_by(category_id=category_id).scalar() or 0
        
        subcategory = ModuleSubcategory(
            category_id=int(category_id),
            name=name,
            slug=slug,
            icon=icon,
            sort_order=max_order + 1,
            is_active=True
        )
        
        db.session.add(subcategory)
        db.session.commit()
        flash(f'Unterkategorie "{name}" erfolgreich erstellt!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Fehler beim Erstellen der Unterkategorie: {str(e)}', 'error')
    
    return redirect(url_for('admin_modules'))

@app.route('/admin/add-module', methods=['POST'])
def add_module():
    """Neues Modul hinzufügen"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        flash('Admin-Zugriff erforderlich.', 'error')
        return redirect(url_for('admin_modules'))
    
    try:
        # Formulardaten extrahieren
        category_id = request.form.get('category_id')
        subcategory_id = request.form.get('subcategory_id') or None
        title = request.form.get('title')
        description = request.form.get('description')
        icon = request.form.get('icon', '🎯')
        template_file = request.form.get('template_file', '')
        external_url = request.form.get('external_url', '')
        estimated_duration = int(request.form.get('estimated_duration', 30))
        difficulty_level = request.form.get('difficulty_level', 'beginner')
        
        # Zugriffssteuerung
        is_lead_magnet = 'is_lead_magnet' in request.form
        is_published = 'is_published' in request.form
        
        # Subscription Levels
        required_levels = []
        if not is_lead_magnet:
            if 'req_basic' in request.form:
                required_levels.append('basic')
            if 'req_premium' in request.form:
                required_levels.append('premium')
            if 'req_elite' in request.form:
                required_levels.append('elite')
        
        if not category_id or not title or not description:
            flash('Kategorie, Titel und Beschreibung sind erforderlich.', 'error')
            return redirect(url_for('admin_modules'))
        
        # Slug generieren
        slug = title.lower().replace(' ', '-').replace('.', '').replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
        
        # Sort-Order bestimmen
        if subcategory_id:
            max_order = db.session.query(db.func.max(LearningModule.sort_order)).filter_by(subcategory_id=subcategory_id).scalar() or 0
        else:
            max_order = db.session.query(db.func.max(LearningModule.sort_order)).filter_by(category_id=category_id, subcategory_id=None).scalar() or 0
        
        # Content-Type bestimmen
        content_type = 'external' if external_url else 'html'
        
        module = LearningModule(
            category_id=int(category_id),
            subcategory_id=int(subcategory_id) if subcategory_id else None,
            title=title,
            slug=slug,
            description=description,
            icon=icon,
            template_file=template_file,
            external_url=external_url,
            content_type=content_type,
            is_published=is_published,
            is_lead_magnet=is_lead_magnet,
            required_subscription_levels=required_levels,
            estimated_duration=estimated_duration,
            difficulty_level=difficulty_level,
            sort_order=max_order + 1
        )
        
        db.session.add(module)
        db.session.commit()
        
        # JSON-Backup erstellen
        try:
            backup_module_to_json(module)
        except Exception as backup_error:
            print(f"⚠️ JSON-Backup fehlgeschlagen: {str(backup_error)}")
        
        flash(f'Modul "{title}" erfolgreich erstellt!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Fehler beim Erstellen des Moduls: {str(e)}', 'error')
    
    return redirect(url_for('admin_modules'))

@app.route('/admin/get-all-categories')
def get_all_categories():
    """📋 Gibt alle Kategorien für Dropdown zurück"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        return jsonify({'success': False, 'error': 'Admin-Zugriff erforderlich'})
    
    try:
        categories = ModuleCategory.query.order_by(ModuleCategory.sort_order).all()
        return jsonify({
            'success': True,
            'categories': [
                {
                    'id': cat.id,
                    'name': cat.name,
                    'slug': cat.slug,
                    'icon': cat.icon
                }
                for cat in categories
            ]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/move-module/<int:module_id>', methods=['POST'])
def move_module(module_id):
    """📦 Verschiebt ein Modul in eine andere Kategorie (Ein-Klick-Verschieben)"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        return jsonify({'success': False, 'error': 'Admin-Zugriff erforderlich'})
    
    try:
        module = LearningModule.query.get_or_404(module_id)
        data = request.get_json()
        new_category_id = data.get('category_id')
        new_subcategory_id = data.get('subcategory_id')
        
        if not new_category_id:
            return jsonify({'success': False, 'error': 'Kategorie-ID fehlt'})
        
        # Kategorie validieren
        new_category = ModuleCategory.query.get(new_category_id)
        if not new_category:
            return jsonify({'success': False, 'error': 'Kategorie nicht gefunden'})
        
        # Alten Kategorie-Namen für Log speichern
        old_category_name = module.category.name if module.category else 'Keine'
        
        # Modul verschieben
        module.category_id = new_category_id
        module.subcategory_id = new_subcategory_id if new_subcategory_id else None
        
        # Entferne den [Vorschlag: ...] Teil aus der Description
        if '[Vorschlag:' in module.description:
            module.description = module.description.split('[Vorschlag:')[0].strip()
        
        # Sort-Order neu berechnen
        if new_subcategory_id:
            max_order = db.session.query(db.func.max(LearningModule.sort_order)).filter_by(subcategory_id=new_subcategory_id).scalar() or 0
        else:
            max_order = db.session.query(db.func.max(LearningModule.sort_order)).filter_by(category_id=new_category_id, subcategory_id=None).scalar() or 0
        module.sort_order = max_order + 1
        
        db.session.commit()
        
        flash(f'✅ Modul "{module.title}" von "{old_category_name}" nach "{new_category.name}" verschoben!', 'success')
        
        return jsonify({
            'success': True,
            'message': f'Modul erfolgreich nach {new_category.name} verschoben',
            'new_category': new_category.name
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/update-marktampel')
def update_marktampel_module():
    """Aktualisiert das Marktampel-Modul auf die neue HTML-Version"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        flash('Admin-Zugriff erforderlich.', 'error')
        return redirect(url_for('home'))
    
    try:
        # Finde das existierende Marktampel-Modul
        module = LearningModule.query.filter_by(slug='marktampel-allokation').first()
        
        if not module:
            flash('Marktampel-Modul nicht gefunden. Führe Migration aus.', 'error')
            return redirect(url_for('admin_modules'))
        
        # Update auf HTML-Version
        module.content_type = 'html'
        module.template_file = 'marktampel_allokation_standalone.html'
        module.external_url = ''
        module.description = 'Professionelle Portfolio-Analyse mit Marktampel-System und optimaler Asset-Allokation'
        module.estimated_duration = 45
        module.difficulty_level = 'intermediate'
        
        db.session.commit()
        
        flash('✅ Marktampel-Modul erfolgreich auf HTML-Version aktualisiert!', 'success')
        return redirect(url_for('admin_modules'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Fehler beim Update: {str(e)}', 'error')
        return redirect(url_for('admin_modules'))

@app.route('/admin/add-position-sizing-calculator')
def add_position_sizing_calculator():
    """🎯 Fügt den ABCD Position-Sizing-Calculator zur Datenbank hinzu"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        flash('Admin-Zugriff erforderlich.', 'error')
        return redirect(url_for('home'))
    
    try:
        # Prüfen ob bereits existiert
        existing_module = LearningModule.query.filter_by(slug='position-sizing-abcd-calculator').first()
        if existing_module:
            flash('⚠️ Position-Sizing-Calculator existiert bereits!', 'warning')
            return redirect(url_for('admin_modules'))
        
        # Risikomanagement-Kategorie finden
        risk_category = ModuleCategory.query.filter_by(slug='risikomanagement').first()
        if not risk_category:
            flash('❌ Risikomanagement-Kategorie nicht gefunden. Führe erst die Demo-Module-Initialisierung aus.', 'error')
            return redirect(url_for('admin_modules'))
        
        # Position Sizing Unterkategorie finden
        position_sizing_subcategory = ModuleSubcategory.query.filter_by(
            category_id=risk_category.id,
            slug='position-sizing'
        ).first()
        
        if not position_sizing_subcategory:
            # Unterkategorie erstellen falls sie nicht existiert
            position_sizing_subcategory = ModuleSubcategory(
                category_id=risk_category.id,
                name='3.1 Position Sizing',
                slug='position-sizing',
                icon='🎯',
                description='Optimale Positionsgrößenbestimmung für verschiedene Trade-Qualitäten',
                sort_order=1,
                is_active=True
            )
            db.session.add(position_sizing_subcategory)
            db.session.flush()
        
        # Sort-Order bestimmen
        max_order = db.session.query(db.func.max(LearningModule.sort_order)).filter_by(
            subcategory_id=position_sizing_subcategory.id
        ).scalar() or 0
        
        # Neues Modul erstellen
        calculator_module = LearningModule(
            category_id=risk_category.id,
            subcategory_id=position_sizing_subcategory.id,
            title='ABCD Trade-Grades Position Sizing Calculator',
            slug='position-sizing-abcd-calculator',
            description='Exponentielles Bet-Sizing für Elite-Trader: Wie Du durch intelligentes Bet-Sizing Deine Trading-Performance exponentiell steigerst. Interaktiver Calculator mit 5 Tabs: Warnung für Anfänger, Live-Calculator, Trade-Grades-Übersicht, Performance-Vergleich und Poker-Analogie.',
            icon='🎯',
            template_file='position_sizing_abcd_calculator.html',
            content_type='html',
            is_published=True,
            is_lead_magnet=False,
            required_subscription_levels=['premium', 'elite'],
            estimated_duration=45,
            difficulty_level='advanced',
            sort_order=max_order + 1
        )
        
        db.session.add(calculator_module)
        db.session.commit()
        
        flash('✅ ABCD Position-Sizing-Calculator erfolgreich zur Datenbank hinzugefügt!', 'success')
        flash('🎯 Modul ist verfügbar unter: /position-sizing-abcd-calculator', 'info')
        flash('📊 Kategorie: 3. Risikomanagement → 3.1 Position Sizing', 'info')
        
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Fehler beim Hinzufügen des Moduls: {str(e)}', 'error')
    
    return redirect(url_for('admin_modules'))

@app.route('/admin/init-database')
def admin_init_database():
    """Admin-Route zum manuellen Initialisieren der Database"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        flash('Admin-Zugriff erforderlich.', 'error')
        return redirect(url_for('home'))
    
    try:
        with app.app_context():
            # Database neu initialisieren
            db.create_all()
            
            # User-Tabelle Status
            try:
                user_count = User.query.count()
                flash(f'✅ Database initialisiert! User-Anzahl: {user_count}', 'success')
            except Exception as e:
                flash(f'⚠️ User-Tabelle Problem: {str(e)}', 'warning')
            
            # Module Status prüfen und ggf. initialisieren
            try:
                module_count = LearningModule.query.count()
                category_count = ModuleCategory.query.count()
                
                flash(f'📚 Aktuelle Database: {module_count} Module, {category_count} Kategorien', 'info')
                
                # Wenn keine Module da sind, Demo-Module erstellen
                if module_count == 0 or category_count == 0:
                    print("[EMERGENCY] Erstelle Demo-Module...")
                    init_demo_modules()
                    
                    # Neu zählen nach Initialisierung
                    new_module_count = LearningModule.query.count()
                    new_category_count = ModuleCategory.query.count()
                    
                    flash(f'🎉 WIEDERHERGESTELLT: {new_module_count} Module, {new_category_count} Kategorien erstellt!', 'success')
                else:
                    flash('✅ Database bereits mit Modulen gefüllt - keine Aktion nötig', 'success')
                    
            except Exception as e:
                flash(f'⚠️ Module-Wiederherstellung Problem: {str(e)}', 'warning')
                # Trotzdem versuchen Demo-Module zu erstellen
                try:
                    init_demo_modules()
                    flash('🔄 Demo-Module als Fallback erstellt', 'info')
                except Exception as inner_e:
                    flash(f'❌ Demo-Module Fallback fehlgeschlagen: {str(inner_e)}', 'error')
                
    except Exception as e:
        flash(f'❌ Database-Fehler: {str(e)}', 'error')
    
    return redirect(url_for('admin_modules'))

@app.route('/admin/force-sync-templates')
def force_sync_templates():
    """🔄 Scannt Templates OHNE bestehende Module zu überschreiben"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        flash('Admin-Zugriff erforderlich.', 'error')
        return redirect(url_for('home'))
    
    try:
        # NUR Template-Scan, KEINE Sync von hart-codierten Modulen!
        flash('⚠️ HINWEIS: Diese Funktion überschreibt KEINE bestehenden Module', 'info')
        return auto_register_modules()
        
    except Exception as e:
        flash(f'❌ Fehler bei Template-Synchronisation: {str(e)}', 'error')
        return redirect(url_for('admin_modules'))

@app.route('/admin/auto-register-modules')
def auto_register_modules():
    """🚀 Automatische Registrierung neuer HTML-Templates"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        flash('Admin-Zugriff erforderlich.', 'error')
        return redirect(url_for('home'))
    
    try:
        from pathlib import Path
        import re
        
        templates_dir = Path("templates")
        registered_count = 0
        updated_count = 0
        errors = []
        
        print("🔍 AUTO-REGISTRIERUNG GESTARTET")
        print("=" * 50)
        
        # Debug-Info für Flash-Messages
        flash('🔍 Auto-Registrierung gestartet...', 'info')
        
        # Alle HTML-Dateien finden (außer System-Templates)
        excluded_patterns = [
            'base.html', 'home.html', 'login.html', 'register.html',
            'modules_overview.html', 'upgrade_required.html', 'module_default.html',
            '_navigation.html', 'Banner5.html'
        ]
        
        excluded_dirs = ['admin', 'auth', 'errors', 'account', 'templates']
        
        html_files = []
        for html_file in templates_dir.glob("*.html"):
            if any(pattern in html_file.name for pattern in excluded_patterns):
                continue
            if any(excluded_dir in str(html_file) for excluded_dir in excluded_dirs):
                continue
            html_files.append(html_file)
        
        print(f"📄 Gefundene HTML-Templates: {len(html_files)}")
        flash(f'📄 {len(html_files)} HTML-Templates gefunden', 'info')
        
        for html_file in html_files:
            try:
                print(f"\n🔍 Analysiere: {html_file.name}")
                
                # Prüfen ob bereits registriert
                existing_module = LearningModule.query.filter_by(
                    template_file=html_file.name
                ).first()
                
                if existing_module:
                    print(f"[OK] Bereits registriert: {existing_module.title}")
                    continue
                
                # Meta-Daten aus HTML extrahieren
                module_info = extract_module_metadata(html_file)
                
                # WICHTIG: Alle automatisch gescannten Module gehen in "Neue Module" Kategorie
                neue_module_category = ModuleCategory.query.filter_by(slug='neue-module').first()
                
                if not neue_module_category:
                    # Fallback: "Neue Module" Kategorie erstellen falls nicht vorhanden
                    neue_module_category = ModuleCategory(
                        name='🆕 Neue Module',
                        slug='neue-module',
                        icon='🆕',
                        description='Automatisch erkannte Module - Bitte in die richtige Kategorie verschieben',
                        sort_order=999,
                        is_active=True,
                        is_protected=True  # Geschützt!
                    )
                    db.session.add(neue_module_category)
                    db.session.flush()
                
                # Speichere den erkannten Kategorie-Vorschlag in der Description
                suggested_category = module_info.get('category', 'technische-analyse')
                module_info['description'] += f" [Vorschlag: {suggested_category}]"
                
                # Neues Modul erstellen in "Neue Module" Kategorie
                create_auto_module(html_file, module_info, neue_module_category)
                registered_count += 1
                
                print(f"[OK] REGISTRIERT: {module_info['title']} → 🆕 Neue Module (Vorschlag: {suggested_category})")
                
            except Exception as e:
                error_msg = f"Fehler bei {html_file.name}: {str(e)}"
                errors.append(error_msg)
                print(f"[ERROR] {error_msg}")
        
        db.session.commit()
        
        # Flash-Nachricht für Frontend
        if registered_count > 0:
            flash(f'✅ {registered_count} neue Module automatisch registriert! Bitte Details im Admin-Panel anpassen.', 'success')
        elif len(html_files) == 0:
            flash('📄 Keine HTML-Templates gefunden.', 'info')
        else:
            flash('📋 Alle verfügbaren Module bereits registriert.', 'info')
        
        if errors:
            flash(f'⚠️ {len(errors)} Fehler bei der Registrierung. Details in der Konsole.', 'warning')
        
        print("\n" + "=" * 50)
        print("[SUMMARY] ZUSAMMENFASSUNG")
        print("=" * 50)
        print(f"[OK] Neue Module: {registered_count}")
        print(f"[ERROR] Fehler: {len(errors)}")
        print("[INFO] Nächste Schritte:")
        print("   1. Admin-Panel öffnen")
        print("   2. Module-Details anpassen")
        print("   3. Module veröffentlichen")
        
    except Exception as e:
        flash(f'❌ Fehler bei automatischer Registrierung: {str(e)}', 'error')
        print(f"💥 Hauptfehler: {str(e)}")
    
    return redirect(url_for('admin_modules'))

@app.route('/admin/register-missing-modules')
def register_missing_modules():
    """🚀 Registriert die wichtigsten fehlenden Module direkt"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        flash('Admin-Zugriff erforderlich.', 'error')
        return redirect(url_for('home'))
    
    try:
        # Wichtige Module die oft fehlen
        critical_modules = [
            {
                'title': 'Tirone Levels und Quadrant Lines',
                'slug': 'tirone-quadrant-lines',
                'template_file': 'tirone_quadrant_lines.html',
                'description': 'Meistere die wichtigsten TC2000-Indikatoren für präzise Unterstützungs- und Widerstandsanalysen',
                'category_slug': 'technische-analyse',
                'icon': '📊',
                'duration': 75,
                'difficulty': 'intermediate'
            },
            {
                'title': 'Expected Value Calculator',
                'slug': 'expected-value-calc',
                'template_file': 'ev_calculator.html',
                'description': 'Interaktiver Expected Value Rechner für Trading-Entscheidungen',
                'category_slug': 'risikomanagement',
                'icon': '🧮',
                'duration': 45,
                'difficulty': 'intermediate'
            },
            {
                'title': 'Trading Tools Collection',
                'slug': 'trading-tools-collection',
                'template_file': 'trading_tools.html',
                'description': 'Sammlung professioneller Trading-Werkzeuge und Kalkulatoren',
                'category_slug': 'technische-analyse',
                'icon': '🛠️',
                'duration': 30,
                'difficulty': 'beginner'
            },
            {
                'title': 'Börsencrash März 2025 Analyse',
                'slug': 'boersencrash-maerz-2025',
                'template_file': 'boersencrash_maerz_2025.html',
                'description': 'Detaillierte Analyse des Börsencrashs vom März 2025',
                'category_slug': 'fundamentalanalyse',
                'icon': '💥',
                'duration': 60,
                'difficulty': 'advanced'
            },
            {
                'title': 'Trading-Playbook Grundlagen - Metalearning & The Process',
                'slug': 'trading-playbook-masterclass',
                'template_file': 'trading_playbook_masterclass.html',
                'description': 'Die ultimative Masterclass über Metalearning und den Trading-Prozess. Verstehe wie professionelle Trader wirklich denken und arbeiten.',
                'category_slug': 'elite-system-iii',
                'icon': '👑',
                'duration': 120,
                'difficulty': 'advanced'
            }
        ]
        
        registered_count = 0
        
        for module_data in critical_modules:
            # Prüfen ob bereits existiert
            existing = LearningModule.query.filter_by(slug=module_data['slug']).first()
            if existing:
                flash(f'⚠️ {module_data["title"]} bereits vorhanden', 'warning')
                continue
            
            # Template-Datei prüfen
            import os
            template_path = os.path.join('templates', module_data['template_file'])
            if not os.path.exists(template_path):
                flash(f'❌ Template nicht gefunden: {module_data["template_file"]}', 'error')
                continue
            
            # Kategorie finden
            category = ModuleCategory.query.filter_by(slug=module_data['category_slug']).first()
            if not category:
                flash(f'❌ Kategorie nicht gefunden: {module_data["category_slug"]}', 'error')
                continue
            
            # Modul erstellen
            module = LearningModule(
                category_id=category.id,
                title=module_data['title'],
                slug=module_data['slug'],
                description=module_data['description'],
                icon=module_data['icon'],
                template_file=module_data['template_file'],
                content_type='html',
                is_published=True,
                is_lead_magnet=False,
                required_subscription_levels=['premium', 'elite'],
                estimated_duration=module_data['duration'],
                difficulty_level=module_data['difficulty'],
                sort_order=100 + registered_count
            )
            
            db.session.add(module)
            registered_count += 1
            flash(f'✅ REGISTRIERT: {module_data["title"]}', 'success')
        
        db.session.commit()
        flash(f'🎉 {registered_count} kritische Module erfolgreich registriert!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Fehler bei Module-Registrierung: {str(e)}', 'error')
    
    return redirect(url_for('admin_modules'))

@app.route('/admin/publish-all-modules')
def publish_all_modules():
    """Publiziert ALLE unpublished Module auf einmal"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        flash('Admin-Zugriff erforderlich.', 'error')
        return redirect(url_for('home'))
    
    try:
        unpublished_modules = LearningModule.query.filter_by(is_published=False).all()
        count = len(unpublished_modules)
        
        if count == 0:
            flash('Alle Module sind bereits veröffentlicht!', 'info')
            return redirect(url_for('admin_modules'))
        
        for module in unpublished_modules:
            module.is_published = True
        
        db.session.commit()
        flash(f'✅ {count} Module erfolgreich veröffentlicht!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Fehler beim Publizieren: {str(e)}', 'error')
    
    return redirect(url_for('admin_modules'))

@app.route('/admin/debug-modules')
def debug_modules():
    """Debug-Informationen über Module und Kategorien"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        return jsonify({'error': 'Admin-Zugriff erforderlich'}), 401
    
    try:
        # Basis-Statistiken
        total_modules = LearningModule.query.count()
        published = LearningModule.query.filter_by(is_published=True).count()
        unpublished = LearningModule.query.filter_by(is_published=False).count()
        
        # Kategorien-Statistiken
        total_categories = ModuleCategory.query.count()
        protected_categories = ModuleCategory.query.filter_by(is_protected=True).count()
        
        # Module in "Neue Module"
        neue_module_cat = ModuleCategory.query.filter_by(slug='neue-module').first()
        in_neue_module = 0
        if neue_module_cat:
            in_neue_module = LearningModule.query.filter_by(category_id=neue_module_cat.id).count()
        
        # Module ohne Kategorie (sollte 0 sein durch Auto-Assign!)
        no_category = LearningModule.query.filter_by(category_id=None).count()
        
        # Module ohne Template
        no_template = LearningModule.query.filter_by(template_file=None).count()
        
        stats = {
            'modules': {
                'total': total_modules,
                'published': published,
                'unpublished': unpublished,
                'no_category': no_category,
                'in_neue_module': in_neue_module,
                'no_template': no_template
            },
            'categories': {
                'total': total_categories,
                'protected': protected_categories,
                'neue_module_exists': neue_module_cat is not None
            },
            'health': {
                'all_modules_have_category': no_category == 0,
                'neue_module_category_exists': neue_module_cat is not None,
                'neue_module_is_protected': neue_module_cat.is_protected if neue_module_cat else False
            }
        }
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/sync-modules-from-code')
def admin_sync_modules_from_code():
    """
    🔄 Manuelle Synchronisation von hart-codierten Modulen aus dem Code
    
    ACHTUNG: Diese Funktion synchronisiert Module aus dem Code in die Datenbank.
    Verwende dies nur wenn du bewusst Code-Änderungen übernehmen willst!
    """
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        flash('Admin-Zugriff erforderlich.', 'error')
        return redirect(url_for('home'))
    
    try:
        print("\n" + "="*60)
        print("[ADMIN] Manuelle Code-zu-DB Synchronisation gestartet")
        print("="*60)
        
        # Rufe die sync_modules_from_local Funktion auf
        sync_modules_from_local()
        db.session.commit()
        
        # Zähle Ergebnisse
        module_count = LearningModule.query.count()
        category_count = ModuleCategory.query.count()
        
        flash(f'✅ Synchronisation erfolgreich abgeschlossen!', 'success')
        flash(f'📊 Aktuelle Datenbank: {category_count} Kategorien, {module_count} Module', 'info')
        
        print(f"[ADMIN] Sync abgeschlossen: {category_count} Kategorien, {module_count} Module")
        print("="*60 + "\n")
        
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Fehler bei Synchronisation: {str(e)}', 'error')
        print(f"[ERROR] Sync fehlgeschlagen: {str(e)}")
        import traceback
        traceback.print_exc()
    
    return redirect(url_for('admin_modules'))

@app.route('/admin/fix-duplicate-categories')
def fix_duplicate_categories():
    """🔧 Behebt doppelte Kategorien in der Datenbank"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        flash('Admin-Zugriff erforderlich.', 'error')
        return redirect(url_for('home'))
    
    try:
        # Doppelte Kategorien finden und zusammenführen
        categories = ModuleCategory.query.all()
        category_groups = {}
        
        # Kategorien nach Name gruppieren
        for category in categories:
            name = category.name
            if name in category_groups:
                category_groups[name].append(category)
            else:
                category_groups[name] = [category]
        
        merged_count = 0
        deleted_count = 0
        
        for name, cat_list in category_groups.items():
            if len(cat_list) > 1:
                flash(f'🔍 Doppelte Kategorie gefunden: {name} ({len(cat_list)}x)', 'info')
                
                # Erste Kategorie als Master behalten
                master_category = cat_list[0]
                
                # Module von anderen Kategorien zur Master-Kategorie verschieben
                for duplicate_cat in cat_list[1:]:
                    modules_to_move = LearningModule.query.filter_by(category_id=duplicate_cat.id).all()
                    
                    for module in modules_to_move:
                        module.category_id = master_category.id
                        flash(f'📦 Modul verschoben: {module.title} → {master_category.name}', 'info')
                    
                    # Doppelte Kategorie löschen
                    db.session.delete(duplicate_cat)
                    deleted_count += 1
                    flash(f'🗑️ Doppelte Kategorie gelöscht: {duplicate_cat.name} (ID: {duplicate_cat.id})', 'warning')
                
                merged_count += 1
        
        db.session.commit()
        
        if merged_count > 0:
            flash(f'✅ {merged_count} doppelte Kategorien zusammengeführt, {deleted_count} Duplikate entfernt!', 'success')
        else:
            flash('✅ Keine doppelten Kategorien gefunden - alles sauber!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Fehler beim Bereinigen der Kategorien: {str(e)}', 'error')
    
    return redirect(url_for('admin_modules'))

def extract_module_metadata(html_file):
    """Extrahiert Meta-Informationen aus HTML-Template"""
    import re
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Standard-Defaults
        info = {
            'title': generate_title_from_filename(html_file.stem),
            'description': f'Interaktives Lernmodul: {generate_title_from_filename(html_file.stem)}',
            'icon': '📊',
            'category': 'technische-analyse',
            'difficulty': 'intermediate',
            'duration': 60,
            'is_premium': True
        }
        
        # Title aus HTML <title> Tag extrahieren
        title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        if title_match:
            title_text = title_match.group(1).strip()
            if " - " in title_text:
                info['title'] = title_text.split(" - ")[0].strip()
            else:
                info['title'] = title_text
        
        # Description aus Meta-Tags extrahieren
        desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', content, re.IGNORECASE)
        if desc_match:
            info['description'] = desc_match.group(1).strip()
        
        # Hero-Subtitle als Fallback für Description
        hero_match = re.search(r'class=["\']hero-subtitle["\'][^>]*>(.*?)</[^>]+>', content, re.IGNORECASE | re.DOTALL)
        if hero_match and not desc_match:
            hero_text = re.sub(r'<[^>]+>', '', hero_match.group(1)).strip()
            if hero_text and len(hero_text) > 10:
                info['description'] = hero_text
        
        # Kategorie aus Dateiname ableiten
        filename_lower = html_file.stem.lower()
        category_mapping = {
            'expected_value': {'category': 'trading-konzepte', 'icon': '📊'},
            'tirone': {'category': 'technische-analyse', 'icon': '📈'},
            'quadrant': {'category': 'technische-analyse', 'icon': '📈'},
            'risk': {'category': 'risikomanagement', 'icon': '⚠️'},
            'risiko': {'category': 'risikomanagement', 'icon': '⚠️'},
            'psychology': {'category': 'trading-psychologie', 'icon': '🧠'},
            'psychologie': {'category': 'trading-psychologie', 'icon': '🧠'},
            'fundamental': {'category': 'fundamentalanalyse', 'icon': '📋'},
            'bridgewater': {'category': 'grundlagen', 'icon': '🏛️'},
            'quadranten': {'category': 'grundlagen', 'icon': '🏛️'},
            'kelly': {'category': 'risikomanagement', 'icon': '⚖️'},
            'position': {'category': 'risikomanagement', 'icon': '⚖️'},
            'sizing': {'category': 'risikomanagement', 'icon': '⚖️'},
            'magic_line': {'category': 'technische-analyse', 'icon': '🎯'},
            'playbook': {'category': 'trading-strategien', 'icon': '📚'},
            'darwin': {'category': 'trading-philosophie', 'icon': '🧬'},
            'marktampel': {'category': 'risikomanagement', 'icon': '🚦'}
        }
        
        for keyword, mapping in category_mapping.items():
            if keyword in filename_lower:
                info['category'] = mapping['category']
                info['icon'] = mapping['icon']
                break
        
        # Duration aus HTML-Kommentaren extrahieren
        duration_match = re.search(r'<!-- duration: (\d+) -->', content, re.IGNORECASE)
        if duration_match:
            info['duration'] = int(duration_match.group(1))
        elif 'complete' in filename_lower or 'masterclass' in filename_lower:
            info['duration'] = 120
        elif 'basic' in filename_lower or 'intro' in filename_lower:
            info['duration'] = 45
        
        # Lead-Magnet Detection
        if any(keyword in filename_lower for keyword in ['lead', 'magnet', 'free', 'basic', 'intro']):
            info['is_premium'] = False
        
        # Difficulty aus Dateiname
        if 'basic' in filename_lower or 'intro' in filename_lower:
            info['difficulty'] = 'beginner'
        elif 'advanced' in filename_lower or 'masterclass' in filename_lower or 'complete' in filename_lower:
            info['difficulty'] = 'advanced'
        
        return info
        
    except Exception as e:
        print(f"[WARNING] Fehler beim Extrahieren der Meta-Daten von {html_file.name}: {str(e)}")
        return {
            'title': generate_title_from_filename(html_file.stem),
            'description': f'Automatisch erkanntes Modul: {html_file.stem}',
            'icon': '📄',
            'category': 'technische-analyse',
            'difficulty': 'intermediate',
            'duration': 60,
            'is_premium': True
        }

def generate_title_from_filename(filename):
    """Generiert schönen Titel aus Dateiname"""
    title = filename.replace('_', ' ').replace('-', ' ')
    
    # Spezielle Ersetzungen
    replacements = {
        'expected value': 'Expected Value (EV)',
        'tirone quadrant lines': 'Tirone Levels & Quadrant Lines',
        'magic line': 'Magic Line Strategie',
        'bridgewater quadranten': 'Bridgewater Quadranten',
        'kelly simulator': 'Kelly-Kriterium Simulator',
        'position sizing kelly': 'Position Sizing mit Kelly',
        'trading playbook': 'Trading Playbook',
        'darwin investing': 'Darwin Investing Philosophie',
        'marktampel allokation': 'Marktampel & Asset Allokation',
        'daily report card': 'Daily Trading Report Card',
        'meta learning': 'Meta-Learning für Trader'
    }
    
    title_lower = title.lower()
    for key, value in replacements.items():
        if key in title_lower:
            return value
    
    # Standard Title Case
    return title.title()

def backup_module_to_json(module):
    """💾 Sichert Modul-Definition in JSON-Backup-Datei"""
    import json
    import os
    from datetime import datetime
    
    backup_file = 'modules_backup.json'
    
    try:
        # Lade existierende Backups
        if os.path.exists(backup_file):
            with open(backup_file, 'r', encoding='utf-8') as f:
                backups = json.load(f)
        else:
            backups = {'modules': [], 'last_updated': None}
        
        # Modul-Definition erstellen
        module_def = {
            'id': module.id,
            'title': module.title,
            'slug': module.slug,
            'description': module.description,
            'icon': module.icon,
            'template_file': module.template_file,
            'external_url': module.external_url,
            'content_type': module.content_type,
            'category_slug': module.category.slug if module.category else None,
            'subcategory_id': module.subcategory_id,
            'is_published': module.is_published,
            'is_lead_magnet': module.is_lead_magnet,
            'required_subscription_levels': module.required_subscription_levels,
            'estimated_duration': module.estimated_duration,
            'difficulty_level': module.difficulty_level,
            'sort_order': module.sort_order,
            'created_at': module.created_at.isoformat() if module.created_at else None,
            'backed_up_at': datetime.utcnow().isoformat()
        }
        
        # Prüfe ob Modul bereits existiert (Update statt Duplicate)
        existing_idx = None
        for idx, existing_module in enumerate(backups['modules']):
            if existing_module.get('slug') == module.slug:
                existing_idx = idx
                break
        
        if existing_idx is not None:
            # Update existing
            backups['modules'][existing_idx] = module_def
            print(f"💾 JSON-Backup aktualisiert: {module.title}")
        else:
            # Add new
            backups['modules'].append(module_def)
            print(f"💾 JSON-Backup erstellt: {module.title}")
        
        backups['last_updated'] = datetime.utcnow().isoformat()
        
        # Speichere Backup
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backups, f, indent=2, ensure_ascii=False)
        
        return True
        
    except Exception as e:
        print(f"❌ JSON-Backup Fehler: {str(e)}")
        return False

def restore_modules_from_json():
    """📥 Stellt Module aus JSON-Backup wieder her"""
    import json
    import os
    
    backup_file = 'modules_backup.json'
    
    if not os.path.exists(backup_file):
        print("ℹ️ Keine JSON-Backup-Datei gefunden")
        return 0
    
    try:
        with open(backup_file, 'r', encoding='utf-8') as f:
            backups = json.load(f)
        
        restored_count = 0
        
        for module_def in backups.get('modules', []):
            # Prüfe ob Modul bereits existiert
            existing = LearningModule.query.filter_by(slug=module_def['slug']).first()
            if existing:
                continue
            
            # Kategorie finden
            category = ModuleCategory.query.filter_by(slug=module_def['category_slug']).first()
            if not category:
                print(f"⚠️ Kategorie nicht gefunden für {module_def['title']}: {module_def['category_slug']}")
                continue
            
            # Modul wiederherstellen
            new_module = LearningModule(
                title=module_def['title'],
                slug=module_def['slug'],
                description=module_def['description'],
                icon=module_def['icon'],
                template_file=module_def.get('template_file'),
                external_url=module_def.get('external_url'),
                content_type=module_def.get('content_type', 'html'),
                category_id=category.id,
                subcategory_id=module_def.get('subcategory_id'),
                is_published=module_def.get('is_published', False),
                is_lead_magnet=module_def.get('is_lead_magnet', False),
                required_subscription_levels=module_def.get('required_subscription_levels', []),
                estimated_duration=module_def.get('estimated_duration', 60),
                difficulty_level=module_def.get('difficulty_level', 'intermediate'),
                sort_order=module_def.get('sort_order', 100)
            )
            
            db.session.add(new_module)
            restored_count += 1
            print(f"📥 Wiederhergestellt: {module_def['title']}")
        
        db.session.commit()
        print(f"✅ {restored_count} Module aus JSON-Backup wiederhergestellt")
        return restored_count
        
    except Exception as e:
        print(f"❌ JSON-Restore Fehler: {str(e)}")
        db.session.rollback()
        return 0

def find_or_create_category_for_module(category_slug):
    """Findet oder erstellt Kategorie für Modul"""
    category = ModuleCategory.query.filter_by(slug=category_slug).first()
    
    if category:
        return category
    
    # Neue Kategorie erstellen
    category_definitions = {
        'technische-analyse': {'name': '2. Technische Analyse', 'icon': '📈', 'order': 2},
        'fundamentalanalyse': {'name': '1. Fundamentalanalyse', 'icon': '📋', 'order': 1},
        'trading-psychologie': {'name': '4. Trading Psychologie', 'icon': '🧠', 'order': 4},
        'risikomanagement': {'name': '3. Risikomanagement', 'icon': '⚠️', 'order': 3},
        'trading-konzepte': {'name': '5. Trading Konzepte', 'icon': '🎯', 'order': 5},
        'grundlagen': {'name': '0. Grundlagen', 'icon': '🏛️', 'order': 0},
        'trading-strategien': {'name': '6. Trading Strategien', 'icon': '📚', 'order': 6},
        'trading-philosophie': {'name': '7. Trading Philosophie', 'icon': '🧬', 'order': 7},
        'elite-system-iii': {'name': '5. Elite - System III', 'icon': '👑', 'order': 5}
    }
    
    cat_def = category_definitions.get(category_slug, {
        'name': category_slug.replace('-', ' ').title(),
        'icon': '📊',
        'order': 99
    })
    
    category = ModuleCategory(
        name=cat_def['name'],
        slug=category_slug,
        icon=cat_def['icon'],
        description=f'Module der Kategorie {cat_def["name"]}',
        sort_order=cat_def['order']
    )
    
    db.session.add(category)
    db.session.flush()
    
    print(f"[OK] Neue Kategorie erstellt: {cat_def['name']}")
    return category

def create_auto_module(html_file, module_info, category):
    """Erstellt automatisch registriertes Modul"""
    # Slug generieren
    slug = html_file.stem.lower().replace('_', '-')
    
    # Slug-Eindeutigkeit prüfen
    counter = 1
    original_slug = slug
    while LearningModule.query.filter_by(slug=slug).first():
        slug = f"{original_slug}-{counter}"
        counter += 1
    
    # Sort-Order bestimmen
    max_order = db.session.query(db.func.max(LearningModule.sort_order)).filter_by(
        category_id=category.id,
        subcategory_id=None
    ).scalar() or 0
    
    # Subscription Levels
    required_levels = [] if not module_info['is_premium'] else ['premium', 'elite']
    
    module = LearningModule(
        category_id=category.id,
        subcategory_id=None,
        title=module_info['title'],
        slug=slug,
        description=module_info['description'],
        icon=module_info['icon'],
        template_file=html_file.name,
        content_type='html',
        is_published=False,  # Standardmäßig unveröffentlicht für Review
        is_lead_magnet=not module_info['is_premium'],
        required_subscription_levels=required_levels,
        estimated_duration=module_info['duration'],
        difficulty_level=module_info['difficulty'],
        sort_order=max_order + 1
    )
    
    db.session.add(module)
    return module

@app.route('/admin/export-structure')
def export_structure():
    """Exportiere die komplette Menüstruktur als JSON"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        return jsonify({'success': False, 'error': 'Admin-Zugriff erforderlich'})
    
    try:
        categories = ModuleCategory.query.filter_by(is_active=True).order_by(ModuleCategory.sort_order).all()
        structure = []
        
        for category in categories:
            cat_data = {
                'name': category.name,
                'slug': category.slug,
                'icon': category.icon,
                'description': category.description,
                'sort_order': category.sort_order,
                'subcategories': [],
                'modules': []
            }
            
            # Subkategorien
            for subcat in category.subcategories:
                if subcat.is_active:
                    subcat_data = {
                        'name': subcat.name,
                        'slug': subcat.slug,
                        'icon': subcat.icon,
                        'sort_order': subcat.sort_order,
                        'modules': []
                    }
                    
                    # Module in Subkategorie
                    for module in subcat.modules:
                        if module.is_published:
                            subcat_data['modules'].append({
                                'title': module.title,
                                'slug': module.slug,
                                'description': module.description,
                                'icon': module.icon,
                                'template_file': module.template_file,
                                'external_url': module.external_url,
                                'is_published': module.is_published,
                                'is_lead_magnet': module.is_lead_magnet,
                                'required_subscription_levels': module.required_subscription_levels,
                                'estimated_duration': module.estimated_duration,
                                'difficulty_level': module.difficulty_level,
                                'sort_order': module.sort_order
                            })
                    
                    cat_data['subcategories'].append(subcat_data)
            
            # Module direkt in Kategorie
            for module in category.modules:
                if not module.subcategory_id and module.is_published:
                    cat_data['modules'].append({
                        'title': module.title,
                        'slug': module.slug,
                        'description': module.description,
                        'icon': module.icon,
                        'template_file': module.template_file,
                        'external_url': module.external_url,
                        'is_published': module.is_published,
                        'is_lead_magnet': module.is_lead_magnet,
                        'required_subscription_levels': module.required_subscription_levels,
                        'estimated_duration': module.estimated_duration,
                        'difficulty_level': module.difficulty_level,
                        'sort_order': module.sort_order
                    })
            
            structure.append(cat_data)
        
        return jsonify({'success': True, 'structure': structure})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# === API ENDPOINTS ===

@app.route('/api/modules/search')
def api_modules_search():
    """API für Modul-Suche"""
    query = request.args.get('q', '')
    user_subscription = session.get('user', {}).get('membership', 'free')
    
    if not query:
        return jsonify({'modules': []})
    
    try:
        modules = LearningModule.query.filter(
            LearningModule.title.contains(query),
            LearningModule.is_published == True
        ).limit(10).all()
        
        results = []
        for module in modules:
            if module.user_has_access(user_subscription):
                results.append({
                    'title': module.title,
                    'slug': module.slug,
                    'description': module.description,
                    'icon': module.icon,
                    'category': module.category.name if module.category else '',
                    'url': url_for('module_view', slug=module.slug)
                })
    except:
        results = []
    
    return jsonify({'modules': results})

# === STATIC FILE ROUTES ===


# === MIGRATION FUNCTIONS ===

def migrate_didis_streamlit_modules():
    """Migriert alle Didis Streamlit-Module aus dem anderen Projekt"""
    print("[INFO] Migriere Didis Streamlit-Module...")
    
    # Module-Daten
    modules_data = [
        {
            "title": "Trading mit Risiko",
            "slug": "trading-mit-risiko",
            "description": "Grundlagen des Risikomanagements im Trading",
            "category": "risikomanagement",
            "content_type": "streamlit",
            "external_url": "http://localhost:8501/(0.0)_💰_Trading_mit_Risiko",
            "required_subscription_levels": [],
            "is_lead_magnet": True,
            "estimated_duration": 45,
            "difficulty_level": "beginner",
            "icon": "💰",
            "sort_order": 1
        },
        {
            "title": "Marktampel & Allokation",
            "slug": "marktampel-allokation",
            "description": "Professionelle Portfolio-Analyse mit Marktampel-System und optimaler Asset-Allokation",
            "category": "risikomanagement",
            "content_type": "html",
            "template_file": "marktampel_allokation_standalone.html",
            "external_url": "",
            "required_subscription_levels": [],
            "is_lead_magnet": True,
            "estimated_duration": 45,
            "difficulty_level": "intermediate",
            "icon": "🚦",
            "sort_order": 2
        },
        {
            "title": "Die 3 Trader-Archetypen",
            "slug": "drei-trader-archetypen",
            "description": "Verstehe die verschiedenen Trader-Typen und finde deinen Stil",
            "category": "trading-psychologie",
            "content_type": "streamlit",
            "external_url": "http://localhost:8501/(0.2)_Die_3_Trader_Archetypen",
            "required_subscription_levels": [],
            "is_lead_magnet": True,
            "estimated_duration": 40,
            "difficulty_level": "beginner",
            "icon": "👥",
            "sort_order": 3
        },
        {
            "title": "Winner identifizieren",
            "slug": "winner-identifizieren",
            "description": "Lerne wie du die besten Aktien für dein Portfolio findest",
            "category": "fundamentalanalyse",
            "content_type": "streamlit",
            "external_url": "http://localhost:8501/(1.0)_📘_Winner_identifizieren",
            "required_subscription_levels": [],
            "is_lead_magnet": True,
            "estimated_duration": 60,
            "difficulty_level": "intermediate",
            "icon": "📘",
            "sort_order": 4
        },
        {
            "title": "AVWAP Grundlagen",
            "slug": "avwap-grundlagen",
            "description": "Teil I: Die Grundlagen von AVWAP (Advanced Volume Weighted Average Price)",
            "category": "technische-analyse",
            "content_type": "streamlit",
            "external_url": "http://localhost:8501/(2.2)_Teil_I_AVWAP_Grundlagen",
            "required_subscription_levels": ["premium", "elite"],
            "is_lead_magnet": False,
            "estimated_duration": 75,
            "difficulty_level": "intermediate",
            "icon": "📊",
            "sort_order": 14
        },
        {
            "title": "AVWAP Anwenden",
            "slug": "avwap-anwenden",
            "description": "Teil II: AVWAP in der Praxis anwenden",
            "category": "technische-analyse",
            "content_type": "streamlit",
            "external_url": "http://localhost:8501/(2.2.1)_Teil_II_AVWAP_Anwenden",
            "required_subscription_levels": ["premium", "elite"],
            "is_lead_magnet": False,
            "estimated_duration": 90,
            "difficulty_level": "intermediate",
            "icon": "📊",
            "sort_order": 15
        },
        {
            "title": "AVWAP Entry & Exit Techniken",
            "slug": "avwap-entry-exit-techniken",
            "description": "Professionelle Entry- und Exit-Strategien mit AVWAP",
            "category": "technische-analyse",
            "content_type": "streamlit",
            "external_url": "http://localhost:8501/(2.2.2)_AVWAP_Entry_Exit_Techniken",
            "required_subscription_levels": ["premium", "elite"],
            "is_lead_magnet": False,
            "estimated_duration": 105,
            "difficulty_level": "advanced",
            "icon": "🎯",
            "sort_order": 16
        },
        {
            "title": "The AVWAP Pinch",
            "slug": "avwap-pinch",
            "description": "Kapitel 5: Lerne den AVWAP Pinch zu erkennen und zu handeln - Energy and persistence conquer all things",
            "category": "technische-analyse",
            "content_type": "html",
            "template_name": "avwap_pinch.html",
            "required_subscription_levels": ["premium", "elite"],
            "is_lead_magnet": False,
            "estimated_duration": 120,
            "difficulty_level": "advanced",
            "icon": "🎯",
            "sort_order": 17
        },
        {
            "title": "Trading Psychologie",
            "slug": "trading-psychologie-streamlit",
            "description": "Die psychologischen Aspekte des Tradings (Streamlit Version)",
            "category": "trading-psychologie",
            "content_type": "streamlit",
            "external_url": "http://localhost:8501/(7.0)_🧠_Psychologie",
            "required_subscription_levels": ["premium", "elite"],
            "is_lead_magnet": False,
            "estimated_duration": 75,
            "difficulty_level": "intermediate",
            "icon": "🧠",
            "sort_order": 24
        }
    ]
    
    migrated_count = 0
    errors = []
    
    for module_data in modules_data:
        try:
            # Prüfen ob bereits vorhanden
            existing = LearningModule.query.filter_by(slug=module_data['slug']).first()
            if existing:
                # Spezielle Behandlung für Marktampel-Modul: Update auf HTML-Version
                if module_data['slug'] == 'marktampel-allokation' and existing.content_type == 'streamlit':
                    print(f"[INFO] Aktualisiere Marktampel-Modul auf HTML-Version...")
                    existing.content_type = module_data['content_type']
                    existing.template_file = module_data.get('template_file')
                    existing.external_url = module_data.get('external_url', '')
                    existing.description = module_data['description']
                    existing.estimated_duration = module_data.get('estimated_duration', existing.estimated_duration)
                    existing.difficulty_level = module_data.get('difficulty_level', existing.difficulty_level)
                    db.session.commit()
                    migrated_count += 1
                    print(f"[OK] Marktampel-Modul aktualisiert: {module_data['title']}")
                    continue
                else:
                    print(f"[INFO] Modul bereits vorhanden: {module_data['title']}")
                    continue
            
            # Kategorie finden
            category = ModuleCategory.query.filter_by(slug=module_data['category']).first()
            if not category:
                print(f"[ERROR] Kategorie nicht gefunden: {module_data['category']}")
                continue
            
            # Neues Modul erstellen
            module = LearningModule(
                category_id=category.id,
                title=module_data['title'],
                slug=module_data['slug'],
                description=module_data['description'],
                icon=module_data['icon'],
                content_type=module_data['content_type'],
                template_file=module_data.get('template_file'),
                external_url=module_data.get('external_url', ''),
                is_published=module_data.get('is_published', True),
                is_lead_magnet=module_data.get('is_lead_magnet', False),
                required_subscription_levels=module_data.get('required_subscription_levels', ['premium', 'elite']),
                estimated_duration=module_data.get('estimated_duration', 60),
                difficulty_level=module_data.get('difficulty_level', 'intermediate'),
                sort_order=module_data.get('sort_order', 100 + migrated_count)
            )
            
            db.session.add(module)
            db.session.commit()
            
            migrated_count += 1
            print(f"[OK] Migriert: {module_data['title']}")
            
        except Exception as e:
            error_msg = f"Fehler bei {module_data['title']}: {str(e)}"
            errors.append(error_msg)
            print(f"[ERROR] {error_msg}")
    
    print(f"\n🎉 Migration abgeschlossen: {migrated_count} Module migriert, {len(errors)} Fehler")
    return migrated_count, errors

# === DEMO-DATEN INITIALISIERUNG ===

def init_demo_modules():
    """Erstellt Demo-Module für die Menüstruktur"""
    print("📦 Erstelle Demo-Module...")
    
    # 0. Grundlagen (neue Kategorie für grundlegende Konzepte)
    cat0 = ModuleCategory(
        name='0. Grundlagen',
        slug='grundlagen',
        icon='🎓',
        description='Fundamentale Konzepte und Frameworks für erfolgreiches Trading und Investieren',
        sort_order=0,
        is_protected=True  # Geschützt - Core Content
    )
    db.session.add(cat0)
    db.session.flush()
    
    # 1. Fundamentalanalyse
    cat1 = ModuleCategory(
        name='1. Fundamentalanalyse',
        slug='fundamentalanalyse',
        icon='📊',
        description='Bewertung von Unternehmen anhand ihrer Geschäftszahlen',
        sort_order=1
    )
    db.session.add(cat1)
    db.session.flush()
    
    sub1_1 = ModuleSubcategory(
        category_id=cat1.id,
        name='1.1 Bilanzanalyse',
        slug='bilanzanalyse',
        icon='📋',
        sort_order=1
    )
    db.session.add(sub1_1)
    db.session.flush()
    
    sub1_2 = ModuleSubcategory(
        category_id=cat1.id,
        name='1.2 Kennzahlen',
        slug='kennzahlen',
        icon='🔢',
        sort_order=2
    )
    db.session.add(sub1_2)
    db.session.flush()
    
    # 2. Technische Analyse
    cat2 = ModuleCategory(
        name='2. Technische Analyse',
        slug='technische-analyse',
        icon='📈',
        description='Chartanalyse und Trading-Strategien',
        sort_order=2
    )
    db.session.add(cat2)
    db.session.flush()
    
    sub2_1 = ModuleSubcategory(
        category_id=cat2.id,
        name='2.1 Chart-Patterns',
        slug='chart-patterns',
        icon='📊',
        sort_order=1
    )
    db.session.add(sub2_1)
    db.session.flush()
    
    sub2_2 = ModuleSubcategory(
        category_id=cat2.id,
        name='2.2 Indikatoren',
        slug='indikatoren',
        icon='📉',
        sort_order=2
    )
    db.session.add(sub2_2)
    db.session.flush()
    
    # 3. Risikomanagement
    cat3 = ModuleCategory(
        name='3. Risikomanagement',
        slug='risikomanagement',
        icon='🛡️',
        description='Kapitalschutz und Money Management',
        sort_order=3
    )
    db.session.add(cat3)
    db.session.flush()
    
    sub3_1 = ModuleSubcategory(
        category_id=cat3.id,
        name='3.1 Position Sizing',
        slug='position-sizing',
        icon='⚖️',
        sort_order=1
    )
    db.session.add(sub3_1)
    db.session.flush()
    
    # 4. Trading Psychologie
    cat4 = ModuleCategory(
        name='4. Trading Psychologie',
        slug='trading-psychologie',
        icon='🧠',
        description='Mentale Aspekte des erfolgreichen Tradings',
        sort_order=4
    )
    db.session.add(cat4)
    db.session.flush()
    
    sub4_1 = ModuleSubcategory(
        category_id=cat4.id,
        name='4.1 Emotionen kontrollieren',
        slug='emotionen',
        icon='😌',
        sort_order=1
    )
    db.session.add(sub4_1)
    db.session.flush()
    
    # === MODULE ERSTELLEN ===
    
    # Bridgewater Quadranten Modul (Grundlagen)
    bridgewater_module = LearningModule(
        category_id=cat0.id,  # Grundlagen-Kategorie
        subcategory_id=None,  # Direkt in der Hauptkategorie
        title='Bridgewater Quadranten Masterclass',
        slug='bridgewater-quadranten',
        description='Ray Dalios vollständiges Wirtschafts-Framework: Die vier "Jahreszeiten" der Wirtschaft verstehen und ein wetterbeständiges Portfolio aufbauen',
        icon='📊',
        template_file='bridgewater_quadranten_complete.html',
        content_type='html',
        is_published=True,
        is_lead_magnet=False,  # Premium Content
        required_subscription_levels=['premium', 'elite'],
        estimated_duration=90,
        difficulty_level='intermediate',
        sort_order=1
    )
    db.session.add(bridgewater_module)
    
    # Positioning & Risikomanagement Modul (Grundlagen)
    positioning_module = LearningModule(
        category_id=cat0.id,  # Grundlagen-Kategorie
        subcategory_id=None,  # Direkt in der Hauptkategorie
        title='Vermögensaufbau Masterclass: Depots nahe Höchstständen halten',
        slug='positioning-risikomanagement',
        description='Der Schlüssel zum langfristigen Vermögensaufbau: Wie Sie Ihre Depots nahe an ihren Höchstständen halten und den Compounding-Effekt maximieren',
        icon='💼',
        template_file='positioning_risikomanagement.html',
        content_type='html',
        is_published=True,
        is_lead_magnet=False,  # Premium Content
        required_subscription_levels=['premium', 'elite'],
        estimated_duration=60,
        difficulty_level='intermediate',
        sort_order=2
    )
    db.session.add(positioning_module)
    
    # Lead-Magnet: Balance Sheet Basics
    lead_magnet1 = LearningModule(
        category_id=cat1.id,
        subcategory_id=sub1_1.id,
        title='Balance Sheet Basics',
        slug='balance-sheet-basics',
        description='Grundlagen der Bilanzanalyse für Aktieninvestoren (KOSTENLOS)',
        icon='📋',
        is_published=True,
        is_lead_magnet=True,
        estimated_duration=45,
        difficulty_level='beginner',
        sort_order=1
    )
    db.session.add(lead_magnet1)
    
    # Kelly-Kriterium Modul (Premium)
    kelly_module = LearningModule(
        category_id=cat3.id,  # Risikomanagement
        subcategory_id=sub3_1.id,  # Position Sizing
        title='Kelly-Kriterium: Optimales Position Sizing',
        slug='kelly-kriterium',
        description='Lerne das Kelly-Kriterium für mathematisch optimales Risikomanagement. Mit interaktivem Rechner und Simulator.',
        icon='🎯',
        template_file='Position_Sizing_Kelly.html',
        is_published=True,
        required_subscription_levels=['premium', 'elite'],
        estimated_duration=90,
        difficulty_level='intermediate',
        sort_order=2
    )
    db.session.add(kelly_module)
    
    # Premium-Module
    premium_module1 = LearningModule(
        category_id=cat1.id,
        subcategory_id=sub1_2.id,
        title='KGV, KBV & Co.',
        slug='kgv-kbv-kennzahlen',
        description='Die wichtigsten Bewertungskennzahlen verstehen und anwenden',
        icon='🔢',
        is_published=True,
        required_subscription_levels=['premium', 'elite'],
        estimated_duration=90,
        difficulty_level='intermediate',
        sort_order=1
    )
    db.session.add(premium_module1)
    
    premium_module2 = LearningModule(
        category_id=cat2.id,
        subcategory_id=sub2_2.id,
        title='Moving Averages Masterclass',
        slug='moving-averages',
        description='Gleitende Durchschnitte richtig nutzen - Von EMA bis Magic Line',
        icon='📉',
        is_published=True,
        required_subscription_levels=['premium', 'elite'],
        estimated_duration=75,
        difficulty_level='intermediate',
        sort_order=1
    )
    db.session.add(premium_module2)
    
    elite_module = LearningModule(
        category_id=cat4.id,
        subcategory_id=sub4_1.id,
        title='Fear & Greed Mastery',
        slug='fear-greed-mastery',
        description='Marktpsychologie verstehen und für profitable Trades nutzen',
        icon='🧠',
        is_published=True,
        required_subscription_levels=['elite'],
        estimated_duration=60,
        difficulty_level='advanced',
        sort_order=1
    )
    db.session.add(elite_module)
    
    # === 5. ELITE - SYSTEM III KATEGORIE ===
    cat5 = ModuleCategory(
        name='5. Elite - System III',
        slug='elite-system-iii',
        icon='👑',
        description='Professionelle Trading-Systeme für Elite-Trader - System III Methodologie',
        sort_order=5
    )
    db.session.add(cat5)
    db.session.flush()
    
    # Subcategory für System III
    sub5_1 = ModuleSubcategory(
        category_id=cat5.id,
        name='5.1 Trade-Vorbereitung',
        slug='trade-vorbereitung',
        icon='📋',
        description='Systematische Trade-Vorbereitung nach dem "Mice au Place" System',
        sort_order=1
    )
    db.session.add(sub5_1)
    db.session.flush()
    
    # Trading-Playbook System III Modul
    trading_playbook_system_iii = LearningModule(
        category_id=cat5.id,
        subcategory_id=sub5_1.id,
        title='Trading-Playbook System III',
        slug='trading-playbook-system-iii',
        description='Professionelle Trade-Vorbereitung nach dem "Mice au Place" System. Von der Marktanalyse bis zur perfekten Trade-Execution.',
        icon='📋',
        template_file='trading_playbook_system_iii.html',
        content_type='html',
        is_published=True,
        required_subscription_levels=['elite'],
        estimated_duration=60,
        difficulty_level='expert',
        sort_order=1
    )
    db.session.add(trading_playbook_system_iii)
    
    # Trading Mindset Masterclass - Playbook (Premium)
    playbook_module = LearningModule(
        category_id=cat4.id,  # Trading Psychologie
        subcategory_id=sub4_1.id,  # Emotionen kontrollieren
        title='Trading Mindset Masterclass',
        slug='playbook',
        description='Warum mehr Informationen nicht die Antwort sind - Eine interaktive Lernreise durch die Trading-Psychologie',
        icon='🧠',
        template_file='Playbook.html',  # Das HTML-Template
        is_published=True,
        required_subscription_levels=['premium', 'elite'],
        estimated_duration=45,
        difficulty_level='intermediate',
        sort_order=2
    )
    db.session.add(playbook_module)
    
    db.session.commit()
    print("[OK] Demo-Module erfolgreich erstellt!")

def sync_modules_from_local():
    """🔄 Auto-Sync: Synchronisiert lokale Module-Strukturen mit Railway-Datenbank
    
    WICHTIG: Füge hier neue Kategorien/Module hinzu, damit sie automatisch online übertragen werden!
    """
    try:
        # 🔧 HIER LOKALE KATEGORIEN DEFINIEREN - Werden automatisch zu Railway synced!
        local_categories = [
            {
                'name': '0. Grundlagen',
                'slug': 'grundlagen', 
                'icon': '🎓',
                'description': 'Fundamentale Konzepte und Frameworks für erfolgreiches Trading und Investieren',
                'sort_order': 0
            },
            {
                'name': '1. Trading-Grundlagen',
                'slug': 'trading-grundlagen',
                'icon': '📊', 
                'description': 'Grundlegende Trading-Konzepte und -Strategien',
                'sort_order': 1
            },
            {
                'name': '2. Technische Analyse',
                'slug': 'technische-analyse',
                'icon': '📈',
                'description': 'Chartanalyse und technische Indikatoren', 
                'sort_order': 2
            },
            {
                'name': '3. Fundamentalanalyse',
                'slug': 'fundamentalanalyse',
                'icon': '💼',
                'description': 'Unternehmensbewertung und fundamentale Analyse',
                'sort_order': 3
            },
            {
                'name': '4. Trading-Psychologie', 
                'slug': 'trading-psychologie',
                'icon': '🧠',
                'description': 'Mentale Aspekte des Tradings und Emotionskontrolle',
                'sort_order': 4
            },
            {
                'name': '5. Elite - System III',
                'slug': 'elite-system-iii', 
                'icon': '👑',
                'description': 'Professionelle Trading-Systeme für Elite-Trader - System III Methodologie',
                'sort_order': 5
            },
            {
                'name': '🆕 Neue Module',
                'slug': 'neue-module',
                'icon': '🆕',
                'description': 'Automatisch erkannte Module - Bitte in die richtige Kategorie verschieben',
                'sort_order': 999
            }
            # 🆕 NEUE KATEGORIEN HIER HINZUFÜGEN → Automatisch online!
        ]
        
        # 🔧 HIER LOKALE MODULE DEFINIEREN - Werden automatisch zu Railway synced!
        local_modules = [
            # Elite System III
            {
                'title': 'Trading-Playbook System III',
                'slug': 'trading-playbook-system-iii',
                'category_slug': 'elite-system-iii',
                'subcategory_name': '5.1 Trade-Vorbereitung',
                'description': 'Professionelle Trade-Vorbereitung nach dem "Mice au Place" System. Von der Marktanalyse bis zur perfekten Trade-Execution.',
                'icon': '📋',
                'template_file': 'trading_playbook_system_iii.html',
                'content_type': 'html',
                'required_subscription_levels': ['elite'],
                'estimated_duration': 60,
                'difficulty_level': 'expert', 
                'sort_order': 1
            },
            {
                'title': 'Trading-Playbook Masterclass',
                'slug': 'trading-playbook-masterclass',
                'category_slug': 'elite-system-iii',
                'description': 'Die ultimative Masterclass über Metalearning und den Trading-Prozess',
                'icon': '👑',
                'template_file': 'trading_playbook_masterclass.html',
                'content_type': 'html',
                'required_subscription_levels': ['elite'],
                'estimated_duration': 120,
                'difficulty_level': 'advanced',
                'sort_order': 2
            },
            {
                'title': 'Trading Playbook',
                'slug': 'playbook',
                'category_slug': 'elite-system-iii',
                'description': 'Das komplette Trading Playbook mit allen Strategien',
                'icon': '📖',
                'template_file': 'Playbook.html',
                'content_type': 'html',
                'required_subscription_levels': ['elite'],
                'estimated_duration': 90,
                'difficulty_level': 'advanced',
                'sort_order': 3
            },
            # Technische Analyse
            {
                'title': 'Magic Line Strategie',
                'slug': 'magic-line',
                'category_slug': 'technische-analyse',
                'subcategory_name': '2.1 Chart-Patterns', 
                'description': 'Meistere die Kunst des perfekten Ein- und Ausstiegs - Didis bewährte Verkaufssignale',
                'icon': '🎯',
                'template_file': 'magic_line.html',
                'content_type': 'html',
                'required_subscription_levels': ['premium', 'elite'],
                'estimated_duration': 120,
                'difficulty_level': 'advanced',
                'sort_order': 1
            },
            {
                'title': 'AVWAP Pinch Strategie',
                'slug': 'avwap-pinch',
                'category_slug': 'technische-analyse',
                'description': 'Die Pinch-Strategie mit AVWAP für präzise Entry- und Exit-Points',
                'icon': '📌',
                'template_file': 'avwap_pinch.html',
                'content_type': 'html',
                'required_subscription_levels': ['premium', 'elite'],
                'estimated_duration': 80,
                'difficulty_level': 'advanced',
                'sort_order': 2
            },
            {
                'title': 'Tirone Levels & Quadrant Lines',
                'slug': 'tirone-quadrant-lines',
                'category_slug': 'technische-analyse',
                'description': 'Meistere die wichtigsten TC2000-Indikatoren für präzise Unterstützungs- und Widerstandsanalysen',
                'icon': '📊',
                'template_file': 'tirone_quadrant_lines.html',
                'content_type': 'html',
                'required_subscription_levels': ['premium', 'elite'],
                'estimated_duration': 75,
                'difficulty_level': 'intermediate',
                'sort_order': 3
            },
            {
                'title': 'Symmetrie im Trading',
                'slug': 'symmetrie-trading',
                'category_slug': 'technische-analyse',
                'description': 'Eine der einfachsten und mächtigsten Heuristiken zur Vorhersage von Kursbewegungen',
                'icon': '🔄',
                'template_file': 'symmetrie-trading.html',
                'content_type': 'html',
                'required_subscription_levels': ['free'],
                'estimated_duration': 45,
                'difficulty_level': 'intermediate',
                'sort_order': 4
            },
            {
                'title': 'Volume-Analyse Grundlagen',
                'slug': 'volume-analyse-grundlagen',
                'category_slug': 'technische-analyse',
                'description': 'Verstehe Volumen-Patterns und nutze sie für bessere Trading-Entscheidungen',
                'icon': '📊',
                'template_file': 'volume-analyse-grundlagen.html',
                'content_type': 'html',
                'required_subscription_levels': ['premium', 'elite'],
                'estimated_duration': 90,
                'difficulty_level': 'intermediate',
                'sort_order': 5
            },
            # Risikomanagement & Position Sizing
            {
                'title': 'Position Sizing Kelly',
                'slug': 'position-sizing-kelly',
                'category_slug': 'grundlagen',
                'description': 'Kelly-Kriterium für optimales Position Sizing mit interaktivem Rechner',
                'icon': '🎯',
                'template_file': 'Position_Sizing_Kelly.html',
                'content_type': 'html',
                'required_subscription_levels': ['premium', 'elite'],
                'estimated_duration': 90,
                'difficulty_level': 'intermediate',
                'sort_order': 1
            },
            {
                'title': 'Position Sizing ABCD Calculator',
                'slug': 'position-sizing-abcd-calculator',
                'category_slug': 'grundlagen',
                'description': 'Der ultimative ABCD Position Sizing Rechner mit Lance Breitstein Grading-System',
                'icon': '🎯',
                'template_file': 'position_sizing_abcd_calculator.html',
                'content_type': 'html',
                'required_subscription_levels': ['premium', 'elite'],
                'estimated_duration': 120,
                'difficulty_level': 'advanced',
                'sort_order': 2
            },
            {
                'title': 'Kelly Simulator',
                'slug': 'kelly-simulator',
                'category_slug': 'grundlagen',
                'description': 'Interaktiver Kelly-Kriterium Simulator zum Experimentieren',
                'icon': '⚖️',
                'template_file': 'Kelly_Simulator.html',
                'content_type': 'html',
                'required_subscription_levels': ['premium', 'elite'],
                'estimated_duration': 45,
                'difficulty_level': 'intermediate',
                'sort_order': 3
            },
            {
                'title': 'Positioning & Risikomanagement',
                'slug': 'positioning-risikomanagement',
                'category_slug': 'grundlagen',
                'description': 'Professionelles Risikomanagement und Position Sizing für Trading-Erfolg',
                'icon': '⚠️',
                'template_file': 'positioning_risikomanagement.html',
                'content_type': 'html',
                'required_subscription_levels': ['premium', 'elite'],
                'estimated_duration': 90,
                'difficulty_level': 'intermediate',
                'sort_order': 4
            },
            {
                'title': 'Expected Value (EV)',
                'slug': 'expected-value',
                'category_slug': 'grundlagen',
                'description': 'Das fundamentale Konzept für rationale Trading-Entscheidungen',
                'icon': '📊',
                'template_file': 'expected_value.html',
                'content_type': 'html',
                'required_subscription_levels': ['premium', 'elite'],
                'estimated_duration': 90,
                'difficulty_level': 'intermediate',
                'sort_order': 5
            },
            {
                'title': 'EV Calculator',
                'slug': 'ev-calculator',
                'category_slug': 'grundlagen',
                'description': 'Interaktiver Expected Value Rechner für Trading-Entscheidungen',
                'icon': '🧮',
                'template_file': 'ev_calculator.html',
                'content_type': 'html',
                'required_subscription_levels': ['free'],
                'estimated_duration': 45,
                'difficulty_level': 'beginner',
                'sort_order': 6
            },
            {
                'title': 'Marktampel & Asset Allokation',
                'slug': 'marktampel-allokation',
                'category_slug': 'grundlagen',
                'description': 'Systematisches Marktampel-System für optimale Asset-Allokation',
                'icon': '🚦',
                'template_file': 'marktampel_allokation.html',
                'content_type': 'html',
                'required_subscription_levels': ['free'],
                'estimated_duration': 45,
                'difficulty_level': 'beginner',
                'sort_order': 7
            },
            {
                'title': 'Marktampel Standalone',
                'slug': 'marktampel-standalone',
                'category_slug': 'grundlagen',
                'description': 'Standalone Version des Marktampel-Systems',
                'icon': '🚦',
                'template_file': 'marktampel_allokation_standalone.html',
                'content_type': 'html',
                'required_subscription_levels': ['free'],
                'estimated_duration': 30,
                'difficulty_level': 'beginner',
                'sort_order': 8
            },
            {
                'title': 'Bridgewater Quadranten',
                'slug': 'bridgewater-quadranten',
                'category_slug': 'grundlagen',
                'description': 'Ray Dalios All-Weather-Portfolio und die vier Wirtschaftsquadranten',
                'icon': '🏛️',
                'template_file': 'bridgewater_quadranten_complete.html',
                'content_type': 'html',
                'required_subscription_levels': ['premium', 'elite'],
                'estimated_duration': 120,
                'difficulty_level': 'advanced',
                'sort_order': 9
            },
            # Trading-Psychologie
            {
                'title': 'Meta-Learning Quiz',
                'slug': 'meta-learning-quiz',
                'category_slug': 'trading-psychologie',
                'description': 'Interaktives Quiz zum Meta-Learning für Trader',
                'icon': '🧠',
                'template_file': 'meta_learning_quiz.html',
                'content_type': 'html',
                'required_subscription_levels': ['free'],
                'estimated_duration': 30,
                'difficulty_level': 'beginner',
                'sort_order': 1
            },
            {
                'title': 'Die Wahrheit über die Lernkurve',
                'slug': 'die-wahrheit-lernkurve',
                'category_slug': 'trading-psychologie',
                'description': 'Wie du wirklich besser wirst im Trading - Die Realität der Lernkurve',
                'icon': '📈',
                'template_file': 'die_wahrheit_lernkurve.html',
                'content_type': 'html',
                'required_subscription_levels': ['free'],
                'estimated_duration': 45,
                'difficulty_level': 'beginner',
                'sort_order': 2
            },
            {
                'title': 'Finde deinen Trading-Weg',
                'slug': 'finde-deinen-trading-weg',
                'category_slug': 'trading-psychologie',
                'description': 'Entdecke deinen persönlichen Trading-Stil und -Ansatz',
                'icon': '🧭',
                'template_file': 'finde_deinen_trading_weg.html',
                'content_type': 'html',
                'required_subscription_levels': ['free'],
                'estimated_duration': 60,
                'difficulty_level': 'beginner',
                'sort_order': 3
            },
            {
                'title': 'Darwin Investing',
                'slug': 'darwin-investing',
                'category_slug': 'trading-psychologie',
                'description': 'Evolution und Adaption im Trading - Survival of the Fittest',
                'icon': '🧬',
                'template_file': 'darwin_investing.html',
                'content_type': 'html',
                'required_subscription_levels': ['premium', 'elite'],
                'estimated_duration': 75,
                'difficulty_level': 'intermediate',
                'sort_order': 4
            },
            {
                'title': 'Daily Trading Report Card',
                'slug': 'daily-report-card',
                'category_slug': 'trading-psychologie',
                'description': 'Systematische Selbstreflexion für kontinuierliche Verbesserung',
                'icon': '📋',
                'template_file': 'daily_report_card_lernseite.html',
                'content_type': 'html',
                'required_subscription_levels': ['free'],
                'estimated_duration': 45,
                'difficulty_level': 'beginner',
                'sort_order': 5
            },
            # Trading-Grundlagen
            {
                'title': 'Börsencrash März 2025 Analyse',
                'slug': 'boersencrash-maerz-2025',
                'category_slug': 'trading-grundlagen',
                'description': 'Detaillierte Analyse des Börsencrashs vom März 2025 und was wir daraus lernen',
                'icon': '💥',
                'template_file': 'boersencrash_maerz_2025.html',
                'content_type': 'html',
                'required_subscription_levels': ['free'],
                'estimated_duration': 60,
                'difficulty_level': 'intermediate',
                'sort_order': 1
            },
            {
                'title': 'Trading Tools Übersicht',
                'slug': 'trading-tools',
                'category_slug': 'trading-grundlagen',
                'description': 'Sammlung professioneller Trading-Werkzeuge und Kalkulatoren',
                'icon': '🛠️',
                'template_file': 'trading_tools.html',
                'content_type': 'html',
                'required_subscription_levels': ['free'],
                'estimated_duration': 30,
                'difficulty_level': 'beginner',
                'sort_order': 2
            },
            {
                'title': 'Poker vs Trading - Der Vergleich',
                'slug': 'poker-cards-comparison',
                'category_slug': 'trading-grundlagen',
                'description': 'Was Poker und Trading gemeinsam haben und wie du davon profitieren kannst',
                'icon': '🃏',
                'template_file': 'poker-cards-comparison.html',
                'content_type': 'html',
                'required_subscription_levels': ['free'],
                'estimated_duration': 40,
                'difficulty_level': 'beginner',
                'sort_order': 3
            }
            # 🆕 NEUE MODULE HIER HINZUFÜGEN → Automatisch online!
        ]
        
        synced_categories = 0
        synced_modules = 0
        
        # Kategorien synchronisieren
        for cat_data in local_categories:
            existing_cat = ModuleCategory.query.filter_by(slug=cat_data['slug']).first()
            if not existing_cat:
                new_category = ModuleCategory(
                    name=cat_data['name'],
                    slug=cat_data['slug'],
                    icon=cat_data['icon'],
                    description=cat_data['description'],
                    sort_order=cat_data['sort_order']
                )
                db.session.add(new_category)
                synced_categories += 1
                print(f"🆕 Auto-synced new category: {cat_data['name']}")
        
        if synced_categories > 0:
            db.session.commit()
        
        # Module synchronisieren
        for mod_data in local_modules:
            existing_mod = LearningModule.query.filter_by(slug=mod_data['slug']).first()
            if not existing_mod:
                # Kategorie finden
                category = ModuleCategory.query.filter_by(slug=mod_data['category_slug']).first()
                if category:
                    # Subcategory finden oder erstellen
                    subcategory = None
                    if mod_data.get('subcategory_name'):
                        subcategory_slug = mod_data['subcategory_name'].lower().replace(' ', '-').replace('.', '')
                        subcategory = ModuleSubcategory.query.filter_by(
                            category_id=category.id,
                            slug=subcategory_slug
                        ).first()
                        
                        if not subcategory:
                            subcategory = ModuleSubcategory(
                                category_id=category.id,
                                name=mod_data['subcategory_name'],
                                slug=subcategory_slug,
                                icon=mod_data.get('icon', '📄'),
                                sort_order=1
                            )
                            db.session.add(subcategory)
                            db.session.flush()
                    
                    new_module = LearningModule(
                        category_id=category.id,
                        subcategory_id=subcategory.id if subcategory else None,
                        title=mod_data['title'],
                        slug=mod_data['slug'],
                        description=mod_data['description'],
                        icon=mod_data['icon'],
                        template_file=mod_data.get('template_file'),
                        content_type=mod_data.get('content_type', 'html'),
                        is_published=True,
                        required_subscription_levels=mod_data.get('required_subscription_levels', ['premium', 'elite']),
                        estimated_duration=mod_data.get('estimated_duration', 60),
                        difficulty_level=mod_data.get('difficulty_level', 'intermediate'),
                        sort_order=mod_data.get('sort_order', 1)
                    )
                    db.session.add(new_module)
                    synced_modules += 1
                    print(f"🆕 Auto-synced new module: {mod_data['title']}")
        
        if synced_modules > 0:
            db.session.commit()
        
        if synced_categories > 0 or synced_modules > 0:
            print(f"[INFO] Auto-Sync completed: {synced_categories} categories, {synced_modules} modules synced to Railway")
            
    except Exception as e:
        print(f"[ERROR] Auto-sync error: {str(e)}")
        db.session.rollback()

# === ERROR HANDLERS ===

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    try:
        db.session.rollback()
    except:
        pass
    return render_template('errors/500.html'), 500

# === APP STARTEN ===

def init_database():
    """Initialisiert die Database mit allen Tabellen"""
    try:
        # Alle Tabellen erstellen
        db.create_all()
        print("[OK] Database-Tabellen erstellt!")
        
        # User-Tabelle prüfen
        try:
            user_count = User.query.count()
            print(f"[INFO] Anzahl User in Database: {user_count}")
        except Exception as e:
            print(f"[INFO] User-Tabelle wird erstellt: {e}")
        
        # Demo-Module erstellen (nur beim ersten Mal)
        if not ModuleCategory.query.first():
            init_demo_modules()
            print("[OK] Demo-Module erstellt!")
        
        # Didis Streamlit-Module migrieren (einmalig)
        if not LearningModule.query.filter_by(content_type="streamlit").first():
            migrate_didis_streamlit_modules()
            print("[OK] Streamlit-Module migriert!")
            
        return True
        
    except Exception as e:
        print(f"[ERROR] Database-Initialisierung fehlgeschlagen: {e}")
        return False

# === NEUE KATEGORIE-MANAGEMENT ROUTEN ===

@app.route('/admin/add-category', methods=['POST'])
def admin_add_category():
    """Neue Hauptkategorie hinzufügen"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        flash('Admin-Zugriff erforderlich.', 'error')
        return redirect(url_for('login'))
    
    try:
        name = request.form.get('name')
        icon = request.form.get('icon', '📊')
        description = request.form.get('description', '')
        sort_order = int(request.form.get('sort_order', 100))
        
        if not name:
            flash('Kategorie-Name ist erforderlich.', 'error')
            return redirect(url_for('admin_modules'))
        
        # Slug generieren
        slug = name.lower().replace(' ', '-').replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
        slug = ''.join(c for c in slug if c.isalnum() or c == '-')
        
        # Prüfen ob Slug bereits existiert
        counter = 1
        original_slug = slug
        while ModuleCategory.query.filter_by(slug=slug).first():
            slug = f"{original_slug}-{counter}"
            counter += 1
        
        # Neue Kategorie erstellen
        category = ModuleCategory(
            name=name,
            slug=slug,
            icon=icon,
            description=description,
            sort_order=sort_order,
            is_active=True
        )
        
        db.session.add(category)
        db.session.commit()
        
        flash(f'Kategorie "{name}" wurde erfolgreich erstellt.', 'success')
        return redirect(url_for('admin_modules'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Fehler beim Erstellen der Kategorie: {str(e)}', 'error')
        return redirect(url_for('admin_modules'))

@app.route('/admin/add-subcategory', methods=['POST'])
def admin_add_subcategory():
    """Neue Unterkategorie hinzufügen"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        flash('Admin-Zugriff erforderlich.', 'error')
        return redirect(url_for('login'))
    
    try:
        category_id = int(request.form.get('category_id'))
        name = request.form.get('name')
        icon = request.form.get('icon', '📋')
        sort_order = int(request.form.get('sort_order', 100))
        
        if not name or not category_id:
            flash('Name und Kategorie sind erforderlich.', 'error')
            return redirect(url_for('admin_modules'))
        
        # Prüfen ob Kategorie existiert
        category = ModuleCategory.query.get(category_id)
        if not category:
            flash('Kategorie nicht gefunden.', 'error')
            return redirect(url_for('admin_modules'))
        
        # Slug generieren
        slug = name.lower().replace(' ', '-').replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
        slug = ''.join(c for c in slug if c.isalnum() or c == '-')
        
        # Prüfen ob Slug bereits existiert
        counter = 1
        original_slug = slug
        while ModuleSubcategory.query.filter_by(slug=slug, category_id=category_id).first():
            slug = f"{original_slug}-{counter}"
            counter += 1
        
        # Neue Unterkategorie erstellen
        subcategory = ModuleSubcategory(
            category_id=category_id,
            name=name,
            slug=slug,
            icon=icon,
            sort_order=sort_order,
            is_active=True
        )
        
        db.session.add(subcategory)
        db.session.commit()
        
        flash(f'Unterkategorie "{name}" wurde erfolgreich erstellt.', 'success')
        return redirect(url_for('admin_modules'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Fehler beim Erstellen der Unterkategorie: {str(e)}', 'error')
        return redirect(url_for('admin_modules'))

@app.route('/admin/edit-category', methods=['POST'])
def admin_edit_category():
    """Kategorie bearbeiten"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        flash('Admin-Zugriff erforderlich.', 'error')
        return redirect(url_for('login'))
    
    try:
        category_id = int(request.form.get('category_id'))
        name = request.form.get('name')
        icon = request.form.get('icon')
        description = request.form.get('description', '')
        sort_order = int(request.form.get('sort_order', 100))
        
        category = ModuleCategory.query.get(category_id)
        if not category:
            flash('Kategorie nicht gefunden.', 'error')
            return redirect(url_for('admin_modules'))
        
        # Update category
        category.name = name
        category.icon = icon
        category.description = description
        category.sort_order = sort_order
        
        db.session.commit()
        
        flash(f'Kategorie "{name}" wurde erfolgreich aktualisiert.', 'success')
        return redirect(url_for('admin_modules'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Fehler beim Aktualisieren der Kategorie: {str(e)}', 'error')
        return redirect(url_for('admin_modules'))

@app.route('/admin/edit-subcategory', methods=['POST'])
def admin_edit_subcategory():
    """Unterkategorie bearbeiten"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        flash('Admin-Zugriff erforderlich.', 'error')
        return redirect(url_for('login'))
    
    try:
        subcategory_id = int(request.form.get('subcategory_id'))
        category_id = int(request.form.get('category_id'))
        name = request.form.get('name')
        icon = request.form.get('icon')
        sort_order = int(request.form.get('sort_order', 100))
        
        subcategory = ModuleSubcategory.query.get(subcategory_id)
        if not subcategory:
            flash('Unterkategorie nicht gefunden.', 'error')
            return redirect(url_for('admin_modules'))
        
        # Update subcategory
        subcategory.category_id = category_id
        subcategory.name = name
        subcategory.icon = icon
        subcategory.sort_order = sort_order
        
        db.session.commit()
        
        flash(f'Unterkategorie "{name}" wurde erfolgreich aktualisiert.', 'success')
        return redirect(url_for('admin_modules'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Fehler beim Aktualisieren der Unterkategorie: {str(e)}', 'error')
        return redirect(url_for('admin_modules'))

@app.route('/admin/get-subcategory/<int:subcategory_id>')
def admin_get_subcategory(subcategory_id):
    """Unterkategorie-Details für Bearbeitung abrufen"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        return jsonify({'success': False, 'error': 'Admin-Zugriff erforderlich'}), 401
    
    subcategory = ModuleSubcategory.query.get(subcategory_id)
    if not subcategory:
        return jsonify({'success': False, 'error': 'Unterkategorie nicht gefunden'})
    
    return jsonify({
        'success': True,
        'subcategory': {
            'id': subcategory.id,
            'category_id': subcategory.category_id,
            'name': subcategory.name,
            'slug': subcategory.slug,
            'icon': subcategory.icon,
            'sort_order': subcategory.sort_order,
            'is_active': subcategory.is_active
        }
    })

@app.route('/admin/toggle-category-status/<int:category_id>', methods=['POST'])
def admin_toggle_category_status(category_id):
    """Kategorie-Status umschalten"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        return jsonify({'success': False, 'error': 'Admin-Zugriff erforderlich'}), 401
    
    try:
        category = ModuleCategory.query.get(category_id)
        if not category:
            return jsonify({'success': False, 'error': 'Kategorie nicht gefunden'})
        
        category.is_active = not category.is_active
        db.session.commit()
        
        return jsonify({'success': True, 'is_active': category.is_active})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/toggle-subcategory-status/<int:subcategory_id>', methods=['POST'])
def admin_toggle_subcategory_status(subcategory_id):
    """Unterkategorie-Status umschalten"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        return jsonify({'success': False, 'error': 'Admin-Zugriff erforderlich'}), 401
    
    try:
        subcategory = ModuleSubcategory.query.get(subcategory_id)
        if not subcategory:
            return jsonify({'success': False, 'error': 'Unterkategorie nicht gefunden'})
        
        subcategory.is_active = not subcategory.is_active
        db.session.commit()
        
        return jsonify({'success': True, 'is_active': subcategory.is_active})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/delete-category/<int:category_id>', methods=['DELETE'])
def admin_delete_category(category_id):
    """Kategorie löschen"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        return jsonify({'success': False, 'error': 'Admin-Zugriff erforderlich'}), 401
    
    try:
        category = ModuleCategory.query.get(category_id)
        if not category:
            return jsonify({'success': False, 'error': 'Kategorie nicht gefunden'})
        
        # SCHUTZ: Geschützte Kategorien können nicht gelöscht werden!
        if category.is_protected:
            return jsonify({
                'success': False, 
                'error': f'Die Kategorie "{category.name}" ist geschützt und kann nicht gelöscht werden!'
            }), 403
        
        # Alle Module in dieser Kategorie auf "nicht zugeordnet" setzen
        modules = LearningModule.query.filter_by(category_id=category_id).all()
        for module in modules:
            module.category_id = None
            module.subcategory_id = None
        
        # Alle Unterkategorien löschen
        subcategories = ModuleSubcategory.query.filter_by(category_id=category_id).all()
        for subcategory in subcategories:
            db.session.delete(subcategory)
        
        # Kategorie löschen
        db.session.delete(category)
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/delete-subcategory/<int:subcategory_id>', methods=['DELETE'])
def admin_delete_subcategory(subcategory_id):
    """Unterkategorie löschen"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        return jsonify({'success': False, 'error': 'Admin-Zugriff erforderlich'}), 401
    
    try:
        subcategory = ModuleSubcategory.query.get(subcategory_id)
        if not subcategory:
            return jsonify({'success': False, 'error': 'Unterkategorie nicht gefunden'})
        
        # Alle Module in dieser Unterkategorie in die Hauptkategorie verschieben
        modules = LearningModule.query.filter_by(subcategory_id=subcategory_id).all()
        for module in modules:
            module.subcategory_id = None
        
        # Unterkategorie löschen
        db.session.delete(subcategory)
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/get-category/<int:category_id>')
def admin_get_category(category_id):
    """Kategorie-Details für Bearbeitung abrufen"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        return jsonify({'success': False, 'error': 'Admin-Zugriff erforderlich'}), 401
    
    category = ModuleCategory.query.get(category_id)
    if not category:
        return jsonify({'success': False, 'error': 'Kategorie nicht gefunden'})
    
    return jsonify({
        'success': True,
        'category': {
            'id': category.id,
            'name': category.name,
            'slug': category.slug,
            'icon': category.icon,
            'description': category.description,
            'sort_order': category.sort_order,
            'is_active': category.is_active
        }
    })

@app.route('/admin/get-subcategories/<int:category_id>')
def admin_get_subcategories(category_id):
    """Unterkategorien für eine Kategorie abrufen"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        return jsonify({'success': False, 'error': 'Admin-Zugriff erforderlich'}), 401
    
    subcategories = ModuleSubcategory.query.filter_by(category_id=category_id).order_by(ModuleSubcategory.sort_order).all()
    
    return jsonify({
        'success': True,
        'subcategories': [{
            'id': sub.id,
            'name': sub.name,
            'icon': sub.icon,
            'sort_order': sub.sort_order
        } for sub in subcategories]
    })

@app.route('/admin/change-module-subscription', methods=['POST'])
def admin_change_module_subscription():
    """Modul-Subscription-Level ändern"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        return jsonify({'success': False, 'error': 'Admin-Zugriff erforderlich'}), 401
    
    try:
        data = request.json
        module_id = data.get('module_id')
        subscription_level = data.get('subscription_level')
        
        module = LearningModule.query.get(module_id)
        if not module:
            return jsonify({'success': False, 'error': 'Modul nicht gefunden'})
        
        # Subscription-Level setzen
        if subscription_level == 'free':
            module.is_lead_magnet = True
            module.required_subscription_levels = []
        elif subscription_level == 'basic':
            module.is_lead_magnet = False
            module.required_subscription_levels = []
        elif subscription_level == 'premium':
            module.is_lead_magnet = False
            module.required_subscription_levels = ['premium']
        elif subscription_level == 'elite':
            module.is_lead_magnet = False
            module.required_subscription_levels = ['elite']
        
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/move-module', methods=['POST'])
def admin_move_module():
    """Modul in andere Kategorie/Unterkategorie verschieben"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        flash('Admin-Zugriff erforderlich.', 'error')
        return redirect(url_for('login'))
    
    try:
        module_id = int(request.form.get('module_id'))
        category_id = int(request.form.get('category_id'))
        subcategory_id = request.form.get('subcategory_id')
        
        module = LearningModule.query.get(module_id)
        if not module:
            flash('Modul nicht gefunden.', 'error')
            return redirect(url_for('admin_modules'))
        
        # Kategorie prüfen
        category = ModuleCategory.query.get(category_id)
        if not category:
            flash('Kategorie nicht gefunden.', 'error')
            return redirect(url_for('admin_modules'))
        
        # Unterkategorie prüfen (optional)
        if subcategory_id:
            subcategory_id = int(subcategory_id)
            subcategory = ModuleSubcategory.query.get(subcategory_id)
            if not subcategory or subcategory.category_id != category_id:
                flash('Unterkategorie nicht gefunden oder gehört nicht zur ausgewählten Kategorie.', 'error')
                return redirect(url_for('admin_modules'))
        else:
            subcategory_id = None
        
        # Modul verschieben
        module.category_id = category_id
        module.subcategory_id = subcategory_id
        
        db.session.commit()
        
        category_name = category.name
        subcategory_name = f" > {ModuleSubcategory.query.get(subcategory_id).name}" if subcategory_id else ""
        flash(f'Modul "{module.title}" wurde erfolgreich nach "{category_name}{subcategory_name}" verschoben.', 'success')
        return redirect(url_for('admin_modules'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Fehler beim Verschieben des Moduls: {str(e)}', 'error')
        return redirect(url_for('admin_modules'))

@app.route('/admin/delete-module/<int:module_id>', methods=['DELETE'])
def admin_delete_module(module_id):
    """Modul permanent löschen"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        return jsonify({'success': False, 'error': 'Admin-Zugriff erforderlich'}), 401
    
    try:
        module = LearningModule.query.get(module_id)
        if not module:
            return jsonify({'success': False, 'error': 'Modul nicht gefunden'})
        
        module_title = module.title
        
        # Erst alle Abhängigkeiten löschen
        try:
            # Module Progress löschen (falls vorhanden)
            ModuleProgress.query.filter_by(module_id=module_id).delete()
            
            # Modul löschen
            db.session.delete(module)
            db.session.commit()
            
            return jsonify({
                'success': True, 
                'message': f'Modul "{module_title}" wurde erfolgreich gelöscht.'
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': f'Fehler beim Löschen: {str(e)}'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'Unbekannter Fehler: {str(e)}'})

@app.route('/admin/update-module-sort-order', methods=['POST'])
def admin_update_module_sort_order():
    """Einzelnes Modul Sortierungs-Reihenfolge ändern"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        return jsonify({'success': False, 'error': 'Admin-Zugriff erforderlich'}), 401
    
    try:
        data = request.json
        module_id = data.get('module_id')
        new_sort_order = data.get('sort_order')
        
        if not module_id or new_sort_order is None:
            return jsonify({'success': False, 'error': 'Modul-ID und Sortierungs-Reihenfolge sind erforderlich'})
        
        module = LearningModule.query.get(module_id)
        if not module:
            return jsonify({'success': False, 'error': 'Modul nicht gefunden'})
        
        # Sortierungs-Reihenfolge aktualisieren
        module.sort_order = int(new_sort_order)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'Sortierungs-Reihenfolge für "{module.title}" wurde auf {new_sort_order} geändert.'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'Fehler beim Aktualisieren der Sortierung: {str(e)}'})

# === ANALYTICS DASHBOARD ===

@app.route('/admin/analytics-test')
def admin_analytics_test():
    """Einfacher Analytics Test"""
    print("Analytics Test Route aufgerufen!")
    return f"<h1>Analytics Test</h1><p>Session: {session}</p><p>User: {session.get('user', {})}</p>"

@app.route('/admin/analytics')
def admin_analytics():
    """Admin Analytics Dashboard"""
    print(f"Analytics Route aufgerufen - Session: {session}")
    print(f"Logged in: {session.get('logged_in')}")
    print(f"User: {session.get('user', {})}")
    
    # Prüfe ob User eingeloggt und Admin/Didi ist
    user = session.get('user', {})
    if not user or user.get('username') not in ['admin', 'didi']:
        print(f"Analytics Zugriff verweigert - User: {user}")
        flash('Admin-Zugriff erforderlich.', 'error')
        return redirect(url_for('login'))
    
    try:
        # Verwende das lokale VisitorAnalytics-Modell
        from sqlalchemy import func, distinct, cast, Date
        from datetime import datetime, timedelta
        
        # Zeiträume für verschiedene Statistiken
        periods = {
            'today': 1,
            'week': 7,
            'month': 30,
            'quarter': 90
        }
        
        # Grundstatistiken sammeln
        stats = {}
        for period_name, days in periods.items():
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            # Unique Visitors
            unique_visitors = db.session.query(
                func.count(distinct(VisitorAnalytics.ip_address))
            ).filter(
                VisitorAnalytics.visited_at >= cutoff_date
            ).scalar() or 0
            
            # Page Views
            page_views = VisitorAnalytics.query.filter(
                VisitorAnalytics.visited_at >= cutoff_date
            ).count()
            
            # Top Pages
            top_pages = db.session.query(
                VisitorAnalytics.page_url,
                VisitorAnalytics.page_title,
                func.count(VisitorAnalytics.id).label('views'),
                func.count(func.distinct(VisitorAnalytics.ip_address)).label('unique_visitors')
            ).filter(
                VisitorAnalytics.visited_at >= cutoff_date
            ).group_by(
                VisitorAnalytics.page_url,
                VisitorAnalytics.page_title
            ).order_by(
                func.count(VisitorAnalytics.id).desc()
            ).limit(5).all()
            
            # Device Stats
            device_stats = db.session.query(
                VisitorAnalytics.device_type,
                func.count(func.distinct(VisitorAnalytics.ip_address)).label('unique_visitors'),
                func.count(VisitorAnalytics.id).label('total_views')
            ).filter(
                VisitorAnalytics.visited_at >= cutoff_date
            ).group_by(
                VisitorAnalytics.device_type
            ).all()
            
            # Referrer Stats
            referrer_stats = db.session.query(
                VisitorAnalytics.referrer,
                func.count(func.distinct(VisitorAnalytics.ip_address)).label('unique_visitors'),
                func.count(VisitorAnalytics.id).label('total_visits')
            ).filter(
                VisitorAnalytics.visited_at >= cutoff_date,
                VisitorAnalytics.referrer.isnot(None),
                VisitorAnalytics.referrer != ''
            ).group_by(
                VisitorAnalytics.referrer
            ).order_by(
                func.count(VisitorAnalytics.id).desc()
            ).limit(5).all()
            
            stats[period_name] = {
                'unique_visitors': unique_visitors,
                'page_views': page_views,
                'top_pages': top_pages,
                'device_stats': device_stats,
                'referrer_stats': referrer_stats
            }
        
        # Tägliche Statistiken für Charts (letzte 30 Tage)
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        daily_stats = db.session.query(
            cast(VisitorAnalytics.visited_at, Date).label('date'),
            func.count(func.distinct(VisitorAnalytics.ip_address)).label('unique_visitors'),
            func.count(VisitorAnalytics.id).label('page_views')
        ).filter(
            VisitorAnalytics.visited_at >= cutoff_date
        ).group_by(
            cast(VisitorAnalytics.visited_at, Date)
        ).order_by(
            cast(VisitorAnalytics.visited_at, Date)
        ).all()
        
        # Chart-Daten für JavaScript vorbereiten
        chart_data = {
            'dates': [stat.date.strftime('%Y-%m-%d') for stat in daily_stats],
            'unique_visitors': [stat.unique_visitors for stat in daily_stats],
            'page_views': [stat.page_views for stat in daily_stats]
        }
        
        return render_template('admin/analytics.html', 
                             stats=stats, 
                             chart_data=chart_data,
                             periods=periods)
        
    except Exception as e:
        flash(f'Fehler beim Laden der Analytics: {str(e)}', 'error')
        return redirect(url_for('admin_modules'))

@app.route('/admin/analytics/api/data')
def admin_analytics_api():
    """API-Endpoint für Analytics-Daten (AJAX)"""
    # Prüfe ob User eingeloggt und Admin/Didi ist  
    user = session.get('user', {})
    if not user or user.get('username') not in ['admin', 'didi']:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        # Verwende das lokale VisitorAnalytics-Modell
        from sqlalchemy import func, distinct, cast, Date
        from datetime import datetime, timedelta
        
        # Parameter aus Request
        days = int(request.args.get('days', 30))
        metric = request.args.get('metric', 'overview')
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        if metric == 'overview':
            # Unique Visitors
            unique_visitors = db.session.query(
                func.count(distinct(VisitorAnalytics.ip_address))
            ).filter(
                VisitorAnalytics.visited_at >= cutoff_date
            ).scalar() or 0
            
            # Page Views
            page_views = VisitorAnalytics.query.filter(
                VisitorAnalytics.visited_at >= cutoff_date
            ).count()
            
            # Top Pages
            top_pages_query = db.session.query(
                VisitorAnalytics.page_url,
                VisitorAnalytics.page_title,
                func.count(VisitorAnalytics.id).label('views'),
                func.count(func.distinct(VisitorAnalytics.ip_address)).label('unique_visitors')
            ).filter(
                VisitorAnalytics.visited_at >= cutoff_date
            ).group_by(
                VisitorAnalytics.page_url,
                VisitorAnalytics.page_title
            ).order_by(
                func.count(VisitorAnalytics.id).desc()
            ).limit(10).all()
            
            data = {
                'unique_visitors': unique_visitors,
                'page_views': page_views,
                'top_pages': [
                    {
                        'url': page.page_url,
                        'title': page.page_title,
                        'views': page.views,
                        'unique_visitors': page.unique_visitors
                    } for page in top_pages_query
                ]
            }
        elif metric == 'devices':
            device_stats = db.session.query(
                VisitorAnalytics.device_type,
                func.count(func.distinct(VisitorAnalytics.ip_address)).label('unique_visitors'),
                func.count(VisitorAnalytics.id).label('total_views')
            ).filter(
                VisitorAnalytics.visited_at >= cutoff_date
            ).group_by(
                VisitorAnalytics.device_type
            ).all()
            
            data = {
                'devices': [
                    {
                        'type': stat.device_type,
                        'unique_visitors': stat.unique_visitors,
                        'total_views': stat.total_views
                    } for stat in device_stats
                ]
            }
        elif metric == 'daily':
            daily_stats = db.session.query(
                cast(VisitorAnalytics.visited_at, Date).label('date'),
                func.count(func.distinct(VisitorAnalytics.ip_address)).label('unique_visitors'),
                func.count(VisitorAnalytics.id).label('page_views')
            ).filter(
                VisitorAnalytics.visited_at >= cutoff_date
            ).group_by(
                cast(VisitorAnalytics.visited_at, Date)
            ).order_by(
                cast(VisitorAnalytics.visited_at, Date)
            ).all()
            
            data = {
                'daily_stats': [
                    {
                        'date': stat.date.strftime('%Y-%m-%d'),
                        'unique_visitors': stat.unique_visitors,
                        'page_views': stat.page_views
                    } for stat in daily_stats
                ]
            }
        else:
            return jsonify({'error': 'Invalid metric'}), 400
        
        return jsonify(data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        # Module-Sync beim Start (verhindert dass bei jedem Request läuft!)
        print("[STARTUP] Führe einmaligen Module-Sync aus...")
        init_modules_on_startup()
        
        # Database initialisieren
        db_success = init_database()
        
        if not db_success:
            print("[WARNING] App startet trotz Database-Problemen...")
        
        # Volumen-Analyse Modul initialisieren
        try:
            from init_volume_module import init_volume_module
            init_volume_module()
            print("[INFO] Volumen-Analyse Modul initialisiert")
        except Exception as e:
            print(f"[WARNING] Volumen-Modul-Init fehlgeschlagen: {e}")
    
    print("[START] Didis Premium Trading Academy mit Menüsystem startet...")
    print("[INFO] Öffne Browser: http://localhost:5000")
    print("[INFO] Features: Menüsystem, Lead-Magnete, Admin-Panel")
    print("[INFO] Login-Accounts:")
    print("   - admin/admin (Elite Access + Admin)")
    print("   - didi/didi (Elite Access + Admin)")
    print("   - premium/premium (Premium Access)")
    print("   - test/test (Premium Access)")
    print("[INFO] Admin-Panel: http://localhost:5000/admin/modules")
    print("[INFO] Zum Beenden: Ctrl+C")
    
    app.run(debug=True, host='0.0.0.0', port=5000)