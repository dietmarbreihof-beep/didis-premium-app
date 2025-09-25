# app.py - Didis Premium Trading Academy mit erweitertem Menü-System
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
import os
import enum
import re
from datetime import datetime, timedelta

# App-Konfiguration
app = Flask(__name__)
app.secret_key = 'dein-geheimer-schluessel-hier-aendern'

# Database-Pfad konfigurieren
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'didis_academy.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database initialisieren
db = SQLAlchemy(app)

# === MODELS (erweitert) ===

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
    
    # Relationships
    subcategories = db.relationship('ModuleSubcategory', backref='category', lazy=True)
    modules = db.relationship('LearningModule', backref='category', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'icon': self.icon,
            'description': self.description,
            'sort_order': self.sort_order,
            'subcategories': [sub.to_dict() for sub in self.subcategories if sub.is_active],
            'modules': [mod.to_dict() for mod in self.modules if mod.is_published]
        }

class ModuleSubcategory(db.Model):
    """Unterkategorien wie '1.1 Bilanzanalyse', '1.2 Kennzahlen'"""
    __tablename__ = 'module_subcategories'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('module_categories.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(20), default="📋")
    sort_order = db.Column(db.Integer, default=100)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    modules = db.relationship('LearningModule', backref='subcategory', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'icon': self.icon,
            'sort_order': self.sort_order,
            'modules': [mod.to_dict() for mod in self.modules if mod.is_published]
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
    
    # Content (ERWEITERT für Streamlit)
    template_file = db.Column(db.String(200))  # z.B. "magic_line.html"
    content_type = db.Column(db.String(50), default="html")  # html, video, pdf, streamlit
    external_url = db.Column(db.String(500))  # Für Streamlit-Integration
    
    # Access Control
    is_published = db.Column(db.Boolean, default=False)
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
            'external_url': self.external_url,
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

# === HELPER FUNCTIONS ===

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

# === MAIN ROUTES ===

@app.route('/')
def home():
    """Startseite mit verfügbaren Modulen"""
    # Lead-Magnete für nicht-eingeloggte User
    if not session.get('logged_in'):
        try:
            lead_magnets = LearningModule.query.filter_by(
                is_published=True,
                is_lead_magnet=True
            ).order_by(LearningModule.sort_order).limit(6).all()
        except:
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
        
    except:
        recent_modules = []
        accessible_recommended = []
    
    return render_template('home.html',
                         recent_modules=recent_modules,
                         recommended_modules=accessible_recommended,
                         user_subscription=user_subscription)

@app.route('/modules')
def modules():
    """ERWEITERTE Übersicht aller Module mit Filtern"""
    menu_structure = get_menu_structure()
    
    user_subscription = "free"
    if session.get('logged_in'):
        user_subscription = session.get('user', {}).get('membership', 'free')
    
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
    if session.get('logged_in'):
        user_subscription = session.get('user', {}).get('membership', 'free')
    
    if not module.user_has_access(user_subscription):
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
    
    # Template bestimmen
    if module.template_file:
        # Bestehende Templates nutzen (wie magic_line.html)
        return render_template(module.template_file, module=module)
    else:
        # Standard-Template für neue Module
        return render_template('module_default.html', module=module)

@app.route('/upgrade-required/<module_slug>')
def upgrade_required(module_slug):
    """Upgrade-Seite für gesperrte Module"""
    try:
        module = LearningModule.query.filter_by(slug=module_slug).first()
    except:
        module = None
    return render_template('upgrade_required.html', module=module)

# === ADMIN ROUTES (erweitert) ===

def admin_required():
    """Decorator für Admin-Zugriff"""
    if not session.get('logged_in') or session.get('user', {}).get('username') not in ['admin', 'didi']:
        return False
    return True

@app.route('/admin/menu-structure')
def admin_menu_structure():
    """Vollständige Menü-Verwaltung"""
    if not admin_required():
        flash('Admin-Zugriff erforderlich.', 'error')
        return redirect(url_for('home'))
    
    # Alle Kategorien mit Subcategorien und Modulen laden
    try:
        categories = ModuleCategory.query.order_by(ModuleCategory.sort_order).all()
        
        # Statistiken
        stats = {
            'total_categories': ModuleCategory.query.count(),
            'total_subcategories': ModuleSubcategory.query.count(),
            'total_modules': LearningModule.query.count(),
            'published_modules': LearningModule.query.filter_by(is_published=True).count(),
            'lead_magnets': LearningModule.query.filter_by(is_lead_magnet=True).count()
        }
    except:
        categories = []
        stats = {}
    
    return render_template('admin/menu_structure.html', 
                         categories=categories, 
                         stats=stats)

@app.route('/admin/add-category', methods=['POST'])
def add_category():
    """Neue Hauptkategorie hinzufügen"""
    if not admin_required():
        flash('Admin-Zugriff erforderlich.', 'error')
        return redirect(url_for('home'))
    
    name = request.form.get('name', '').strip()
    icon = request.form.get('icon', '📊').strip()
    description = request.form.get('description', '').strip()
    
    if not name:
        flash('Kategorie-Name ist erforderlich.', 'error')
        return redirect(url_for('admin_menu_structure'))
    
    # Auto-Slug generieren
    slug = name.lower().replace(' ', '-').replace('.', '').replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    
    # Nächste Sort-Order ermitteln
    try:
        max_order = db.session.query(db.func.max(ModuleCategory.sort_order)).scalar() or 0
        
        category = ModuleCategory(
            name=name,
            slug=slug,
            icon=icon,
            description=description,
            sort_order=max_order + 1
        )
        db.session.add(category)
        db.session.commit()
        
        flash(f'Kategorie "{name}" erfolgreich erstellt.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Fehler beim Erstellen der Kategorie: {str(e)}', 'error')
    
    return redirect(url_for('admin_menu_structure'))

@app.route('/admin/streamlit-import')
def streamlit_import_page():
    """Hauptseite für Streamlit-Modul Import"""
    if not admin_required():
        flash('Admin-Zugriff erforderlich.', 'error')
        return redirect(url_for('home'))
    
    return render_template('admin/streamlit_import.html')

# === AUTHENTICATION ROUTES ===

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Benutzer-Login"""
    if request.method == 'POST':
        email_or_username = request.form['email_or_username']
        password = request.form['password']
        
        # Einfache Demo-User-Validierung
        demo_users = {
            'admin': {'password': 'admin', 'membership': 'elite', 'first_name': 'Admin'},
            'didi': {'password': 'didi', 'membership': 'elite', 'first_name': 'Dietmar'},
            'premium': {'password': 'premium', 'membership': 'premium', 'first_name': 'Premium User'},
            'test': {'password': 'test', 'membership': 'premium', 'first_name': 'Test User'}
        }
        
        if email_or_username in demo_users and demo_users[email_or_username]['password'] == password:
            user_data = demo_users[email_or_username]
            
            # Session setzen
            session['logged_in'] = True
            session['user_id'] = email_or_username
            session['user'] = {
                'id': email_or_username,
                'username': email_or_username,
                'email': f'{email_or_username}@didis-academy.com',
                'membership': user_data['membership']
            }
            
            flash(f'Willkommen zurück, {user_data["first_name"]}!', 'success')
            
            # Redirect zu gewünschter Seite oder Home
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Ungültige Anmeldedaten.', 'error')
    
    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    """Benutzer-Logout"""
    session.clear()
    flash('Du wurdest erfolgreich abgemeldet.', 'success')
    return redirect(url_for('home'))

# === DEMO-DATEN ERWEITERT ===

def init_demo_modules():
    """Erstellt Demo-Module für die Menüstruktur"""
    print("📦 Erstelle Demo-Module...")
    
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
    
    # Magic Line Strategie (dein bestehendes Modul!)
    magic_line_module = LearningModule(
        category_id=cat2.id,
        subcategory_id=sub2_1.id,
        title='Magic Line Strategie',
        slug='magic-line',
        description='Meistere die Kunst des perfekten Ein- und Ausstiegs - Didis bewährte Verkaufssignale',
        icon='🎯',
        template_file='magic_line.html',  # Dein bestehendes Template!
        content_type='html',
        is_published=True,
        required_subscription_levels=['premium', 'elite'],
        estimated_duration=120,
        difficulty_level='advanced',
        sort_order=1
    )
    db.session.add(magic_line_module)
    
    # Lead-Magnet: Balance Sheet Basics
    lead_magnet1 = LearningModule(
        category_id=cat1.id,
        subcategory_id=sub1_1.id,
        title='Balance Sheet Basics',
        slug='balance-sheet-basics',
        description='Grundlagen der Bilanzanalyse für Aktieninvestoren (KOSTENLOS)',
        icon='📋',
        content_type='html',
        is_published=True,
        is_lead_magnet=True,
        estimated_duration=45,
        difficulty_level='beginner',
        sort_order=1
    )
    db.session.add(lead_magnet1)
    
    db.session.commit()
    print("✅ Demo-Module erfolgreich erstellt!")

# Legacy Routes (kompatibel mit bestehender App)
@app.route('/magic-line')
def magic_line():
    """Legacy Route - leitet zum neuen Modul-System weiter"""
    return redirect(url_for('module_view', slug='magic-line'))

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

if __name__ == '__main__':
    with app.app_context():
        try:
            # Database erstellen
            db.create_all()
            
            # Nur beim ersten Mal Demo-Daten erstellen
            if not ModuleCategory.query.first():
                init_demo_modules()
            
        except Exception as e:
            print(f"⚠️ Database-Fehler: {e}")
            print("📝 App startet trotzdem...")
    
    print("🚀 Didis Premium Trading Academy mit erweitertem Menü-System startet...")
    print("📱 Öffne Browser: http://localhost:5000")
    print("✨ Neue Features: 3-Ebenen-Menü, Streamlit-Integration, Admin-Panel")
    print("🔑 Admin-Accounts:")
    print("   - admin/admin (Elite Access + Admin)")
    print("   - didi/didi (Elite Access + Admin)")
    print("🔧 Admin-Panel: http://localhost:5000/admin/menu-structure")
    print("🔄 Streamlit-Import: http://localhost:5000/admin/streamlit-import")
    print("🛑 Zum Beenden: Ctrl+C")
    
    app.run(debug=True, port=5000)
