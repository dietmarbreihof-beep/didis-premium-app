# migrate_analytics.py - Migration für Analytics-Tabelle
"""
Migrations-Skript für die neue VisitorAnalytics-Tabelle.
Führt die Migration sicher durch und erstellt die notwendigen Indizes.
"""

import os
import sys
from datetime import datetime

# App-Pfad hinzufügen
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_migration():
    """Führt die Analytics-Migration durch"""
    try:
        # Flask-App importieren
        from app import app, db
        
        with app.app_context():
            print("Starte Analytics-Migration...")
            
            # Prüfe ob Tabelle bereits existiert
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            if 'visitor_analytics' in existing_tables:
                print("visitor_analytics Tabelle existiert bereits")
                
                # Prüfe Spalten
                columns = [col['name'] for col in inspector.get_columns('visitor_analytics')]
                print(f"Vorhandene Spalten: {', '.join(columns)}")
                
                return True
            
            # Importiere das Analytics-Modell
            try:
                from database import VisitorAnalytics
                print("VisitorAnalytics-Modell importiert")
            except ImportError as e:
                print(f"Fehler beim Importieren des Analytics-Modells: {e}")
                return False
            
            # Erstelle die Tabelle
            print("Erstelle visitor_analytics Tabelle...")
            
            # Prüfe nochmal ob Tabelle existiert nach Import
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            if 'visitor_analytics' not in existing_tables:
                # Erstelle nur die VisitorAnalytics Tabelle
                VisitorAnalytics.__table__.create(db.engine, checkfirst=True)
                print("Tabelle visitor_analytics wurde erstellt")
            else:
                print("Tabelle visitor_analytics existiert bereits")
            
            # Erstelle Indizes für bessere Performance
            print("Erstelle Performance-Indizes...")
            
            from sqlalchemy import text
            
            # Index für IP-Adresse (für Unique Visitor Queries)
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_visitor_analytics_ip 
                ON visitor_analytics(ip_address)
            """))
            
            # Index für Datum (für Zeitraum-Queries)
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_visitor_analytics_date 
                ON visitor_analytics(visited_at)
            """))
            
            # Index für Seiten-URL (für Top-Pages Queries)
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_visitor_analytics_url 
                ON visitor_analytics(page_url)
            """))
            
            # Kombinierter Index für IP + Datum (für Unique Visitors pro Zeitraum)
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_visitor_analytics_ip_date 
                ON visitor_analytics(ip_address, visited_at)
            """))
            
            db.session.commit()
            
            print("Analytics-Migration erfolgreich abgeschlossen!")
            print("Tabelle 'visitor_analytics' wurde erstellt")
            print("Performance-Indizes wurden hinzugefügt")
            
            # Test-Eintrag erstellen (optional)
            create_test_entry = input("\nTest-Eintrag erstellen? (j/n): ").lower().strip()
            if create_test_entry == 'j':
                test_entry = VisitorAnalytics(
                    ip_address='127.0.0.1',
                    user_agent='Migration Test Agent',
                    page_url='/admin/analytics',
                    page_title='Analytics Dashboard - Test',
                    device_type='desktop',
                    browser='Test Browser',
                    os='Test OS'
                )
                db.session.add(test_entry)
                db.session.commit()
                print("Test-Eintrag erstellt")
            
            return True
            
    except Exception as e:
        print(f"Fehler bei der Migration: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_analytics_status():
    """Prüft den Status der Analytics-Implementierung"""
    try:
        from app import app, db
        
        with app.app_context():
            print("\nANALYTICS STATUS CHECK")
            print("=" * 50)
            
            # Prüfe Tabelle
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            
            if 'visitor_analytics' in inspector.get_table_names():
                print("Tabelle: visitor_analytics existiert")
                
                # Anzahl Einträge
                try:
                    from database import VisitorAnalytics
                    count = VisitorAnalytics.query.count()
                    print(f"Einträge: {count} Analytics-Datensätze")
                    
                    if count > 0:
                        # Neuester Eintrag
                        latest = VisitorAnalytics.query.order_by(VisitorAnalytics.visited_at.desc()).first()
                        print(f"Neuester Eintrag: {latest.visited_at}")
                        print(f"Letzte Seite: {latest.page_url}")
                        print(f"Device: {latest.device_type}")
                        
                        # Unique IPs
                        from sqlalchemy import func
                        unique_ips = db.session.query(func.count(func.distinct(VisitorAnalytics.ip_address))).scalar()
                        print(f"Unique IPs: {unique_ips}")
                        
                except Exception as e:
                    print(f"Fehler beim Lesen der Daten: {e}")
                    
            else:
                print("Tabelle: visitor_analytics nicht gefunden")
            
            # Prüfe Middleware
            try:
                from analytics_middleware import AnalyticsMiddleware, AnalyticsService
                print("Middleware: analytics_middleware importierbar")
                print("Service: AnalyticsService verfügbar")
            except ImportError as e:
                print(f"Middleware: Import-Fehler - {e}")
            
            # Prüfe Template
            template_path = os.path.join('templates', 'admin', 'analytics.html')
            if os.path.exists(template_path):
                print("Template: admin/analytics.html existiert")
            else:
                print("Template: admin/analytics.html nicht gefunden")
            
            print("\nAnalytics-Dashboard: http://localhost:5000/admin/analytics")
            print("Hinweis: Nur für admin/didi Benutzer zugänglich")
            
    except Exception as e:
        print(f"Status-Check Fehler: {e}")

if __name__ == '__main__':
    print("ANALYTICS MIGRATION TOOL")
    print("=" * 40)
    
    if len(sys.argv) > 1 and sys.argv[1] == 'status':
        check_analytics_status()
    else:
        print("Dieses Skript erstellt die Analytics-Tabelle und Indizes.")
        print("Stelle sicher, dass die App nicht läuft.")
        
        confirm = input("\nMigration starten? (j/n): ").lower().strip()
        if confirm == 'j':
            success = run_migration()
            if success:
                print("\nMigration erfolgreich!")
                print("Du kannst jetzt die App starten und /admin/analytics besuchen")
            else:
                print("\nMigration fehlgeschlagen!")
                sys.exit(1)
        else:
            print("Migration abgebrochen.")
    
    print("\nVerwendung:")
    print("  python migrate_analytics.py        # Migration durchführen")
    print("  python migrate_analytics.py status # Status prüfen")
