# database.py - Database Models für Didis Trading Academy
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import enum

db = SQLAlchemy()

class SubscriptionType(enum.Enum):
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"  # 30-Minuten-Depot
    ELITE = "elite"      # 5-Minuten-Depot + VIP
    MASTERCLASS = "masterclass"

class ModuleCategory(enum.Enum):
    STRATEGY = "strategy"
    ANALYSIS = "analysis"
    PSYCHOLOGY = "psychology"
    RISK_MANAGEMENT = "risk_management"
    LEAD_MAGNET = "lead_magnet"

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
    email_verified = db.Column(db.Boolean, default=True)  # Für einfache Registrierung ohne E-Mail-Verifizierung
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # WooCommerce Integration
    woocommerce_id = db.Column(db.Integer, unique=True, nullable=True)
    
    # Relationships
    subscriptions = db.relationship('Subscription', backref='user', lazy=True)
    module_access = db.relationship('ModuleAccess', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def current_subscription(self):
        """Gibt das aktuelle aktive Abonnement zurück"""
        active_subscription = Subscription.query.filter_by(
            user_id=self.id,
            is_active=True
        ).filter(
            Subscription.expires_at > datetime.utcnow()
        ).first()
        
        return active_subscription
    
    @property
    def subscription_type(self):
        """Gibt den aktuellen Subscription-Typ zurück"""
        current = self.current_subscription
        if current:
            return current.subscription_type
        return SubscriptionType.FREE
    
    def has_access_to_module(self, module_id):
        """Prüft ob User Zugriff auf ein bestimmtes Modul hat"""
        # Lead-Magnete sind immer frei zugänglich
        module = Module.query.get(module_id)
        if module and module.is_lead_magnet:
            return True
            
        # Prüfe spezifische Modul-Zugriffe
        specific_access = ModuleAccess.query.filter_by(
            user_id=self.id,
            module_id=module_id,
            is_active=True
        ).first()
        
        if specific_access:
            return True
            
        # Prüfe Subscription-basierte Zugriffe
        current_sub = self.current_subscription
        if not current_sub:
            return False
            
        return module and current_sub.subscription_type.value in module.required_subscription_levels
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'subscription_type': self.subscription_type.value,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    subscription_type = db.Column(db.Enum(SubscriptionType), nullable=False)
    
    # Zeitraum
    starts_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_trial = db.Column(db.Boolean, default=False)
    
    # WooCommerce Integration
    woocommerce_order_id = db.Column(db.Integer, nullable=True)
    woocommerce_subscription_id = db.Column(db.Integer, nullable=True)
    
    # Preise
    price_paid = db.Column(db.Numeric(10, 2), nullable=True)
    currency = db.Column(db.String(3), default='EUR')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @staticmethod
    def create_trial(user_id, subscription_type=SubscriptionType.PREMIUM, days=14):
        """Erstellt ein Trial-Abonnement"""
        trial = Subscription(
            user_id=user_id,
            subscription_type=subscription_type,
            expires_at=datetime.utcnow() + timedelta(days=days),
            is_trial=True
        )
        return trial

class Module(db.Model):
    __tablename__ = 'modules'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)  # URL-freundlich
    description = db.Column(db.Text)
    
    # Modul-Eigenschaften
    category = db.Column(db.Enum(ModuleCategory), nullable=False)
    is_published = db.Column(db.Boolean, default=False)
    is_lead_magnet = db.Column(db.Boolean, default=False)
    
    # Template Info
    template_file = db.Column(db.String(200))  # z.B. "magic_line.html"
    icon = db.Column(db.String(50), default="🎯")
    
    # Subscription Requirements (JSON Array)
    required_subscription_levels = db.Column(db.JSON, default=list)  # ["premium", "elite"]
    
    # Sortierung
    sort_order = db.Column(db.Integer, default=100)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    module_access = db.relationship('ModuleAccess', backref='module', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'description': self.description,
            'category': self.category.value,
            'icon': self.icon,
            'is_lead_magnet': self.is_lead_magnet,
            'required_subscription_levels': self.required_subscription_levels
        }

class ModuleAccess(db.Model):
    __tablename__ = 'module_access'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    
    # Access Control
    is_active = db.Column(db.Boolean, default=True)
    granted_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)  # Null = dauerhaft
    
    # Lead-Magnet Tracking
    lead_source = db.Column(db.String(100))  # "social_media", "email", "direct"
    
    # Progress Tracking
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    progress_percentage = db.Column(db.Integer, default=0)

# Helper Functions
def init_default_modules():
    """Erstellt Standard-Module in der Database"""
    default_modules = [
        {
            'title': 'Magic Line Strategie',
            'slug': 'magic-line',
            'description': 'Meistere die Kunst des perfekten Ein- und Ausstiegs',
            'category': ModuleCategory.STRATEGY,
            'template_file': 'magic_line.html',
            'icon': '🎯',
            'required_subscription_levels': ['premium', 'elite', 'masterclass'],
            'is_published': True,
            'sort_order': 1
        },
        {
            'title': 'Rally-Strategie',
            'slug': 'rally-strategie',
            'description': 'Eine Rally für jede Jahreszeit',
            'category': ModuleCategory.STRATEGY,
            'icon': '📈',
            'required_subscription_levels': ['premium', 'elite', 'masterclass'],
            'is_published': False,  # Noch in Entwicklung
            'sort_order': 2
        },
        {
            'title': 'Risikomanagement Basics',
            'slug': 'risiko-basics',
            'description': 'Die Grundlagen des Risikomanagements (Lead-Magnet)',
            'category': ModuleCategory.RISK_MANAGEMENT,
            'icon': '⚠️',
            'is_lead_magnet': True,
            'is_published': True,
            'sort_order': 10
        }
    ]
    
    for module_data in default_modules:
        existing = Module.query.filter_by(slug=module_data['slug']).first()
        if not existing:
            module = Module(**module_data)
            db.session.add(module)
    
    db.session.commit()

def init_db(app):
    """Initialisiert die Database"""
    with app.app_context():
        db.create_all()
        init_default_modules()
        print("✅ Database initialisiert!")