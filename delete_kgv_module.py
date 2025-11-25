#!/usr/bin/env python3
"""
Hilfsskript zum Löschen des KGV-Moduls aus der Datenbank
Verwendung: python delete_kgv_module.py
"""

from app import app, db, LearningModule, ModuleProgress

def delete_kgv_module():
    """Löscht das KGV-Modul aus der Datenbank"""
    with app.app_context():
        # Suche nach dem Modul mit dem Slug
        module = LearningModule.query.filter_by(slug='kgv-kbv-kennzahlen').first()
        
        if not module:
            print("❌ Modul 'kgv-kbv-kennzahlen' nicht in der Datenbank gefunden!")
            return False
        
        print(f"📋 Gefundenes Modul:")
        print(f"   - ID: {module.id}")
        print(f"   - Titel: {module.title}")
        print(f"   - Slug: {module.slug}")
        print(f"   - Template: {module.template_file}")
        print(f"   - Kategorie: {module.category.name if module.category else 'Keine'}")
        
        # Bestätigung
        confirm = input("\n⚠️  Modul wirklich löschen? (ja/nein): ").strip().lower()
        
        if confirm not in ['ja', 'j', 'yes', 'y']:
            print("❌ Abgebrochen - Modul wurde NICHT gelöscht")
            return False
        
        try:
            # Lösche Progress-Einträge
            progress_count = ModuleProgress.query.filter_by(module_id=module.id).count()
            if progress_count > 0:
                print(f"🗑️  Lösche {progress_count} Progress-Einträge...")
                ModuleProgress.query.filter_by(module_id=module.id).delete()
            
            # Lösche das Modul
            module_title = module.title
            db.session.delete(module)
            db.session.commit()
            
            print(f"✅ Modul '{module_title}' erfolgreich aus der Datenbank gelöscht!")
            print(f"✅ {progress_count} Progress-Einträge gelöscht")
            
            # Hinweis zur Template-Datei
            if module.template_file:
                print(f"\n⚠️  HINWEIS: Template-Datei manuell löschen falls nicht mehr benötigt:")
                print(f"   templates/{module.template_file}")
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Fehler beim Löschen: {str(e)}")
            return False

if __name__ == '__main__':
    print("="*60)
    print("🗑️  KGV-Modul Lösch-Script")
    print("="*60)
    
    success = delete_kgv_module()
    
    if success:
        print("\n✅ Erfolgreich abgeschlossen!")
        print("💡 Tipp: Starte die App neu, damit die Änderungen wirksam werden")
    else:
        print("\n❌ Fehler beim Löschen")
        print("💡 Tipp: Prüfe ob das Modul überhaupt existiert mit:")
        print("   python -c \"from app import app, LearningModule; ")
        print("   with app.app_context(): print(LearningModule.query.filter_by(slug='kgv-kbv-kennzahlen').first())\"")


