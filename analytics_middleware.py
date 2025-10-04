# analytics_middleware.py - Visitor Analytics Middleware
from flask import request, session, g
from datetime import datetime
from database import db, VisitorAnalytics
import re
from user_agents import parse

class AnalyticsMiddleware:
    """Middleware für automatisches Visitor-Tracking"""
    
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialisiert die Middleware mit der Flask-App"""
        app.before_request(self.track_visitor)
        
    def get_client_ip(self):
        """Ermittelt die echte Client-IP-Adresse"""
        # Prüfe verschiedene Headers für Proxy/Load Balancer
        if request.headers.get('X-Forwarded-For'):
            # Erste IP in der Liste ist meist die echte Client-IP
            return request.headers.get('X-Forwarded-For').split(',')[0].strip()
        elif request.headers.get('X-Real-IP'):
            return request.headers.get('X-Real-IP')
        elif request.headers.get('CF-Connecting-IP'):  # Cloudflare
            return request.headers.get('CF-Connecting-IP')
        else:
            return request.remote_addr or '127.0.0.1'
    
    def parse_user_agent(self, user_agent_string):
        """Parst User-Agent String für Device/Browser Information"""
        try:
            user_agent = parse(user_agent_string)
            
            # Device Type bestimmen
            if user_agent.is_mobile:
                device_type = 'mobile'
            elif user_agent.is_tablet:
                device_type = 'tablet'
            else:
                device_type = 'desktop'
            
            return {
                'device_type': device_type,
                'browser': f"{user_agent.browser.family} {user_agent.browser.version_string}",
                'os': f"{user_agent.os.family} {user_agent.os.version_string}"
            }
        except:
            return {
                'device_type': 'unknown',
                'browser': 'unknown',
                'os': 'unknown'
            }
    
    def should_track_request(self):
        """Bestimmt ob der Request getrackt werden soll"""
        # Ignoriere statische Dateien
        static_extensions = ['.css', '.js', '.ico', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.woff', '.woff2', '.ttf']
        if any(request.path.endswith(ext) for ext in static_extensions):
            return False
        
        # Ignoriere API-Calls und AJAX-Requests (optional)
        if request.path.startswith('/api/'):
            return False
            
        # Ignoriere Bot-Requests
        user_agent = request.headers.get('User-Agent', '').lower()
        bot_patterns = ['bot', 'crawler', 'spider', 'scraper', 'curl', 'wget']
        if any(pattern in user_agent for pattern in bot_patterns):
            return False
        
        return True
    
    def get_page_title(self):
        """Versucht den Seitentitel zu ermitteln"""
        # Mapping für bekannte Routen
        page_titles = {
            '/': 'Home - Didis Premium Trading Academy',
            '/login': 'Login - Didis Premium Trading Academy',
            '/register': 'Registrierung - Didis Premium Trading Academy',
            '/modules': 'Module - Didis Premium Trading Academy',
            '/trading-tools': 'Trading-Tools - Didis Premium Trading Academy',
            '/admin': 'Admin Dashboard - Didis Premium Trading Academy',
            '/admin/analytics': 'Analytics Dashboard - Didis Premium Trading Academy'
        }
        
        return page_titles.get(request.path, f"Seite {request.path} - Didis Premium Trading Academy")
    
    def track_visitor(self):
        """Hauptfunktion für Visitor-Tracking"""
        # Prüfe ob Request getrackt werden soll
        if not self.should_track_request():
            return
        
        try:
            # Client-Informationen sammeln
            ip_address = self.get_client_ip()
            user_agent_string = request.headers.get('User-Agent', '')
            user_agent_info = self.parse_user_agent(user_agent_string)
            
            # Session-ID generieren falls nicht vorhanden
            if 'analytics_session_id' not in session:
                import uuid
                session['analytics_session_id'] = str(uuid.uuid4())
            
            # User-ID falls eingeloggt
            user_id = session.get('user_id')
            
            # Analytics-Eintrag erstellen
            analytics_entry = VisitorAnalytics(
                ip_address=ip_address,
                user_agent=user_agent_string,
                page_url=request.url,
                page_title=self.get_page_title(),
                referrer=request.headers.get('Referer'),
                session_id=session['analytics_session_id'],
                user_id=user_id,
                device_type=user_agent_info['device_type'],
                browser=user_agent_info['browser'][:50],  # Limit für DB
                os=user_agent_info['os'][:50]  # Limit für DB
            )
            
            # In Datenbank speichern
            db.session.add(analytics_entry)
            db.session.commit()
            
        except Exception as e:
            # Fehler beim Tracking sollen die App nicht crashen
            print(f"Analytics Tracking Error: {e}")
            db.session.rollback()

# Utility-Funktionen für Analytics-Auswertung
class AnalyticsService:
    """Service-Klasse für Analytics-Auswertungen"""
    
    @staticmethod
    def get_unique_visitors_count(days=30):
        """Anzahl unique visitors basierend auf IP-Adressen"""
        from sqlalchemy import func, distinct
        from datetime import datetime, timedelta
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        return db.session.query(
            func.count(distinct(VisitorAnalytics.ip_address))
        ).filter(
            VisitorAnalytics.visited_at >= cutoff_date
        ).scalar() or 0
    
    @staticmethod
    def get_total_page_views(days=30):
        """Gesamtanzahl Seitenaufrufe"""
        from datetime import datetime, timedelta
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        return VisitorAnalytics.query.filter(
            VisitorAnalytics.visited_at >= cutoff_date
        ).count()
    
    @staticmethod
    def get_top_pages(days=30, limit=10):
        """Top-Seiten nach Aufrufen"""
        from sqlalchemy import func
        from datetime import datetime, timedelta
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        return db.session.query(
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
        ).limit(limit).all()
    
    @staticmethod
    def get_device_stats(days=30):
        """Device-Type Statistiken"""
        from sqlalchemy import func
        from datetime import datetime, timedelta
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        return db.session.query(
            VisitorAnalytics.device_type,
            func.count(func.distinct(VisitorAnalytics.ip_address)).label('unique_visitors'),
            func.count(VisitorAnalytics.id).label('total_views')
        ).filter(
            VisitorAnalytics.visited_at >= cutoff_date
        ).group_by(
            VisitorAnalytics.device_type
        ).all()
    
    @staticmethod
    def get_daily_stats(days=7):
        """Tägliche Statistiken für Charts"""
        from sqlalchemy import func, cast, Date
        from datetime import datetime, timedelta
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        return db.session.query(
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
    
    @staticmethod
    def get_referrer_stats(days=30, limit=10):
        """Top-Referrer Statistiken"""
        from sqlalchemy import func
        from datetime import datetime, timedelta
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        return db.session.query(
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
        ).limit(limit).all()
