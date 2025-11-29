"""
Migration: Tägliche Modul-Freischaltung System

Erstellt:
1. UserModuleUnlock Tabelle
2. subscription_started_at Feld im User Model

Ausführen:
    python migrations/add_module_unlock_system.py
"""

import os
import sys

# Projektverzeichnis zum Path hinzufügen
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, User, UserModuleUnlock
from datetime import datetime
from sqlalchemy import inspect, text


def check_column_exists(table_name, column_name):
    """Prüft ob eine Spalte in einer Tabelle existiert"""
    with app.app_context():
        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns(table_name)]
        return column_name in columns


def check_table_exists(table_name):
    """Prüft ob eine Tabelle existiert"""
    with app.app_context():
        inspector = inspect(db.engine)
        return table_name in inspector.get_table_names()


def migrate():
    """Führt die Migration aus"""
    with app.app_context():
        print("="*60)
        print("🔄 Migration: Tägliche Modul-Freischaltung")
        print("="*60)
        
        changes_made = False
        
        # 1. UserModuleUnlock Tabelle erstellen
        if not check_table_exists('user_module_unlocks'):
            print("\n📊 Erstelle Tabelle 'user_module_unlocks'...")
            try:
                # Nur diese spezifische Tabelle erstellen
                UserModuleUnlock.__table__.create(db.engine)
                print("   ✅ Tabelle erstellt")
                changes_made = True
            except Exception as e:
                print(f"   ❌ Fehler: {e}")
                # Fallback: Alle Tabellen erstellen
                try:
                    db.create_all()
                    print("   ✅ Tabelle erstellt (via create_all)")
                    changes_made = True
                except Exception as e2:
                    print(f"   ❌ Fallback-Fehler: {e2}")
        else:
            print("\n📊 Tabelle 'user_module_unlocks' existiert bereits ✓")
        
        # 2. subscription_started_at Feld zum User Model hinzufügen
        if not check_column_exists('users', 'subscription_started_at'):
            print("\n📝 Füge Feld 'subscription_started_at' zu 'users' hinzu...")
            try:
                # SQLite: ALTER TABLE
                db.session.execute(text(
                    "ALTER TABLE users ADD COLUMN subscription_started_at JSON"
                ))
                db.session.commit()
                print("   ✅ Feld hinzugefügt")
                changes_made = True
            except Exception as e:
                print(f"   ⚠️ Warnung: {e}")
                print("   ℹ️  Feld existiert möglicherweise bereits")
                db.session.rollback()
        else:
            print("\n📝 Feld 'subscription_started_at' existiert bereits ✓")
        
        # 3. Bestehende User: FREE-Start-Datum auf created_at setzen
        print("\n🔧 Initialisiere subscription_started_at für bestehende User...")
        try:
            users_updated = 0
            users = User.query.all()
            
            for user in users:
                if not user.subscription_started_at:
                    # Initiales Start-Datum = Registrierungsdatum für FREE
                    user.subscription_started_at = {
                        'free': user.created_at.isoformat() if user.created_at else datetime.utcnow().isoformat()
                    }
                    
                    # Wenn User Premium/Elite hat, auch dieses Level initialisieren
                    if user.subscription_type.value != 'free':
                        level = user.subscription_type.value
                        # Start-Datum = subscription_updated_at oder created_at
                        start_date = user.subscription_updated_at or user.created_at or datetime.utcnow()
                        user.subscription_started_at[level] = start_date.isoformat()
                    
                    users_updated += 1
            
            if users_updated > 0:
                db.session.commit()
                print(f"   ✅ {users_updated} User aktualisiert")
                changes_made = True
            else:
                print("   ℹ️  Alle User bereits initialisiert")
                
        except Exception as e:
            print(f"   ❌ Fehler: {e}")
            db.session.rollback()
        
        # 4. Zusammenfassung
        print("\n" + "="*60)
        if changes_made:
            print("✅ Migration erfolgreich abgeschlossen!")
        else:
            print("ℹ️  Keine Änderungen notwendig - Schema ist aktuell")
        print("="*60)
        
        # Status-Ausgabe
        print("\n📊 Aktueller Status:")
        print(f"   - User: {User.query.count()}")
        print(f"   - Modul-Freischaltungen: {UserModuleUnlock.query.count()}")
        
        # Prüfe ob Scheduler aktiv sein sollte
        print("\n💡 Nächste Schritte:")
        print("   1. App neustarten für Scheduler-Aktivierung")
        print("   2. Erste Freischaltung: Manuell via Admin oder warten auf Mitternacht")
        print("   3. Admin-Route: /admin/trigger-module-unlock (manueller Trigger)")


def rollback():
    """Macht die Migration rückgängig (nur für Notfälle!)"""
    with app.app_context():
        print("⚠️  WARNUNG: Rollback löscht alle Modul-Freischaltungen!")
        confirm = input("Fortfahren? (ja/nein): ")
        
        if confirm.lower() != 'ja':
            print("Abgebrochen.")
            return
        
        try:
            # Tabelle löschen
            if check_table_exists('user_module_unlocks'):
                db.session.execute(text("DROP TABLE user_module_unlocks"))
                db.session.commit()
                print("✅ Tabelle 'user_module_unlocks' gelöscht")
            
            # Hinweis: subscription_started_at Feld bleibt erhalten (keine Daten verloren)
            print("ℹ️  'subscription_started_at' Feld wurde beibehalten")
            print("✅ Rollback abgeschlossen")
            
        except Exception as e:
            print(f"❌ Fehler beim Rollback: {e}")
            db.session.rollback()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Migration: Tägliche Modul-Freischaltung')
    parser.add_argument('--rollback', action='store_true', help='Migration rückgängig machen')
    
    args = parser.parse_args()
    
    if args.rollback:
        rollback()
    else:
        migrate()

