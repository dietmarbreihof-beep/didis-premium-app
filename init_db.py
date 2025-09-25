#!/usr/bin/env python3
"""
Database-Initialisierung für Didis Trading Academy
Führt die komplette Database-Setup aus
"""

import os
import sys
from datetime import datetime

# Flask App importieren
from app import app, db
# Database Models aus app.py verwenden (nicht aus database.py)
from app import LearningModule, ModuleCategory

def create_admin_user():
    """Erstellt einen Standard-Admin-User"""
    try:
        # Für jetzt überspringen - verwenden wir die Demo-User aus app.py
        print("ℹ️  Admin-User: Verwende Demo-Accounts (admin/admin)")
        return True
        
    except Exception as e:
        print(f"❌ Fehler beim Erstellen des Admin-Users: {e}")
        return False

def create_demo_user():
    """Erstellt einen Demo-User für Tests"""
    try:
        # Für jetzt überspringen - verwenden wir die Demo-User aus app.py
        print("ℹ️  Demo-User: Verwende Demo-Accounts (admin/admin, didi/didi, etc.)")
        return True
        
    except Exception as e:
        print(f"❌ Fehler beim Erstellen des Demo-Users: {e}")
        return False

def init_database():
    """Hauptfunktion zur Database-Initialisierung"""
    print("🚀 Starte Database-Initialisierung...")
    print("=" * 50)
    
    try:
        with app.app_context():
            # 1. Alle Tabellen erstellen
            print("📊 Erstelle Database-Tabellen...")
            db.create_all()
            print("✅ Tabellen erfolgreich erstellt!")
            
            # 2. Module-Tabelle prüfen
            try:
                module_count = LearningModule.query.count()
                category_count = ModuleCategory.query.count()
                print(f"📚 Module: {module_count}, Kategorien: {category_count}")
            except Exception as e:
                print(f"⚠️  Module-Tabelle Problem: {e}")
            
            # 3. User-System Info
            print("👥 User-System: Demo-Accounts + Registrierungs-System aktiv")
            
            # 4. Standard-User erstellen
            print("\n👤 Erstelle Standard-User...")
            create_admin_user()
            create_demo_user()
            
            # 5. Finale Statistiken
            print("\n📈 Finale Database-Statistiken:")
            try:
                modules = LearningModule.query.count() 
                print(f"   📚 Module: {modules}")
                
                categories = ModuleCategory.query.count()
                print(f"   📂 Kategorien: {categories}")
                
            except Exception as e:
                print(f"   ⚠️  Statistik-Fehler: {e}")
            
            print("\n" + "=" * 50)
            print("🎉 Database-Initialisierung erfolgreich abgeschlossen!")
            print("\n🔑 Login-Daten (Demo-Accounts):")
            print("   Admin: admin / admin")
            print("   Elite: didi / didi")
            print("   Premium: premium / premium")
            print("   Test: test / test")
            print("\n🆕 Oder registrieren Sie sich für ein echtes Konto!")
            print("\n🚀 Starten Sie die App mit: python app.py")
            
            return True
            
    except Exception as e:
        print(f"\n❌ FEHLER bei Database-Initialisierung: {e}")
        print("💡 Mögliche Lösungen:")
        print("   - Stellen Sie sicher, dass keine andere App-Instanz läuft")
        print("   - Löschen Sie die .db-Datei und versuchen Sie es erneut")
        print("   - Prüfen Sie die Dateiberechtigungen")
        return False

if __name__ == '__main__':
    print("🎯 Didis Trading Academy - Database Setup")
    print(f"⏰ Zeitpunkt: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    success = init_database()
    
    if success:
        print("\n✅ Setup abgeschlossen!")
        sys.exit(0)
    else:
        print("\n❌ Setup fehlgeschlagen!")
        sys.exit(1)
