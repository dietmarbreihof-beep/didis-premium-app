"""
Migrations-Script: How to find DEP Modul entfernen

Dieses Script entfernt das redundante "How to find DEP" Modul aus der Datenbank.
Das Modul wurde durch dep-trading.html ersetzt.

Verwendung:
    python migrations/remove_how_to_find_dep.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, LearningModule, ModuleProgress

def remove_how_to_find_dep_module():
    """Entfernt das How to find DEP Modul aus der Datenbank"""
    
    with app.app_context():
        try:
            print("🗑️ Starte Entfernung des How to find DEP Moduls...")
            
            # Finde das Modul
            module = LearningModule.query.filter_by(slug='how-to-find-dep').first()
            
            if not module:
                print("ℹ️ Modul 'how-to-find-dep' wurde nicht in der Datenbank gefunden.")
                print("   Möglicherweise wurde es bereits entfernt oder existiert nicht.")
                return True
            
            print(f"📋 Gefundenes Modul:")
            print(f"   ID: {module.id}")
            print(f"   Titel: {module.title}")
            print(f"   Slug: {module.slug}")
            
            # Entferne zugehörige Progress-Einträge
            progress_entries = ModuleProgress.query.filter_by(module_id=module.id).all()
            if progress_entries:
                print(f"🗑️ Entferne {len(progress_entries)} Progress-Einträge...")
                for progress in progress_entries:
                    db.session.delete(progress)
            
            # Entferne das Modul
            print("🗑️ Entferne Modul aus der Datenbank...")
            db.session.delete(module)
            
            # Commit
            db.session.commit()
            
            print("\n" + "="*60)
            print("✅ How to find DEP Modul erfolgreich entfernt!")
            print("="*60)
            print(f"\n📊 Entfernte Daten:")
            print(f"   Modul: {module.title}")
            print(f"   Progress-Einträge: {len(progress_entries)}")
            print(f"\n💡 Hinweis: Das neue DEP Trading Modul ist unter /dep-trading verfügbar")
            print("\n✅ Entfernung abgeschlossen!")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ FEHLER: {str(e)}")
            print("   Rollback durchgeführt.")
            import traceback
            traceback.print_exc()
            return False
        
        return True

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🗑️ How to find DEP Modul Entfernung")
    print("="*60 + "\n")
    
    # Sicherheitsabfrage
    response = input("⚠️ Möchtest du das Modul 'how-to-find-dep' wirklich entfernen? (ja/nein): ")
    if response.lower() not in ['ja', 'yes', 'j', 'y']:
        print("❌ Abgebrochen.")
        sys.exit(0)
    
    success = remove_how_to_find_dep_module()
    
    if success:
        print("\n✅ Entfernung erfolgreich abgeschlossen!")
    else:
        print("\n❌ Entfernung fehlgeschlagen!")
        sys.exit(1)

