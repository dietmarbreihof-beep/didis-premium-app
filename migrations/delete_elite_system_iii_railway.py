"""
Migration: Löscht die Kategorie "5. Elite - System III" auf Railway
Ausführung: python migrations/delete_elite_system_iii_railway.py

Dieses Script:
1. Verschiebt Module nach "Neue Module"
2. Löscht alle Unterkategorien
3. Löscht die Hauptkategorie
"""

import sys
import os

# Pfad zur App hinzufügen
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_migration():
    """Führt die Migration aus"""
    from app import app, db, ModuleCategory, ModuleSubcategory, LearningModule
    
    with app.app_context():
        print("=" * 60)
        print("🗑️  RAILWAY MIGRATION: Lösche 'Elite - System III'")
        print("=" * 60)
        
        # 1. Finde die Kategorie
        category = ModuleCategory.query.filter_by(slug='elite-system-iii').first()
        
        if not category:
            print("\n✅ Kategorie 'elite-system-iii' existiert nicht (bereits gelöscht)")
            return True
        
        print(f"\n📍 Kategorie gefunden: ID={category.id}, Name='{category.name}'")
        
        # 2. Finde/Erstelle "Neue Module" Kategorie
        neue_module_cat = ModuleCategory.query.filter_by(slug='neue-module').first()
        if not neue_module_cat:
            print("\n⚠️  Erstelle 'Neue Module' Kategorie...")
            neue_module_cat = ModuleCategory(
                name='🆕 Neue Module',
                slug='neue-module',
                icon='🆕',
                description='Automatisch erkannte Module - Bitte in die richtige Kategorie verschieben',
                sort_order=999
            )
            db.session.add(neue_module_cat)
            db.session.flush()
            print(f"   ✅ Erstellt mit ID: {neue_module_cat.id}")
        
        # 3. Verschiebe Module
        modules = LearningModule.query.filter_by(category_id=category.id).all()
        print(f"\n📦 Verschiebe {len(modules)} Module...")
        
        for module in modules:
            print(f"   → {module.title}")
            module.category_id = neue_module_cat.id
            module.subcategory_id = None
        
        # 4. Lösche Unterkategorien
        subcategories = ModuleSubcategory.query.filter_by(category_id=category.id).all()
        print(f"\n📂 Lösche {len(subcategories)} Unterkategorien...")
        
        for subcat in subcategories:
            print(f"   🗑️ {subcat.name}")
            # Module ohne Unterkategorie setzen
            LearningModule.query.filter_by(subcategory_id=subcat.id).update(
                {'subcategory_id': None}
            )
            db.session.delete(subcat)
        
        # 5. Lösche Hauptkategorie
        print(f"\n🗑️  Lösche Hauptkategorie '{category.name}'...")
        db.session.delete(category)
        
        # 6. Commit
        db.session.commit()
        print("\n✅ ERFOLG! Kategorie auf Railway gelöscht!")
        
        # 7. Zeige Ergebnis
        print("\n📊 Verbleibende Kategorien:")
        for cat in ModuleCategory.query.order_by(ModuleCategory.sort_order).all():
            count = LearningModule.query.filter_by(category_id=cat.id).count()
            print(f"   {cat.sort_order}. {cat.name} ({count} Module)")
        
        return True

if __name__ == '__main__':
    success = run_migration()
    sys.exit(0 if success else 1)

