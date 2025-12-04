"""
Migrations-Script: How to find DEP Modul registrieren

Dieses Script registriert das "How to find DEP - Deep Episodic Pivots" Modul in der Datenbank.
Basierend auf StockBee Guide: Deep Episodic Pivots - Die Kunst der verzögerten Reaktionen finden.

Verwendung:
    python migrations/register_how_to_find_dep.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, LearningModule, ModuleCategory, ModuleSubcategory

def register_how_to_find_dep_module():
    """Registriert das How to find DEP Modul in der Datenbank"""
    
    with app.app_context():
        try:
            print("🚀 Starte How to find DEP Modul-Registrierung...")
            
            # 1. Finde oder erstelle Hauptkategorie "Trading-Setups"
            main_category = ModuleCategory.query.filter_by(
                name="Trading-Setups"
            ).first()
            
            if not main_category:
                print("📁 Erstelle Hauptkategorie 'Trading-Setups'...")
                main_category = ModuleCategory(
                    name="Trading-Setups",
                    slug="trading-setups",
                    description="Bewährte Trading-Setups und Strategien",
                    icon="🎯",
                    sort_order=5
                )
                db.session.add(main_category)
                db.session.flush()  # Get ID
                print(f"✅ Hauptkategorie erstellt (ID: {main_category.id})")
            else:
                print(f"✅ Hauptkategorie gefunden (ID: {main_category.id})")
            
            # 2. Finde oder erstelle Unterkategorie "Momentum Trading"
            subcategory = ModuleSubcategory.query.filter_by(
                category_id=main_category.id,
                name="Momentum Trading"
            ).first()
            
            if not subcategory:
                print("📂 Erstelle Unterkategorie 'Momentum Trading'...")
                subcategory = ModuleSubcategory(
                    category_id=main_category.id,
                    name="Momentum Trading",
                    slug="momentum-trading",
                    description="Momentum-basierte Trading-Strategien und Setups",
                    icon="⚡",
                    sort_order=1
                )
                db.session.add(subcategory)
                db.session.flush()
                print(f"✅ Unterkategorie erstellt (ID: {subcategory.id})")
            else:
                print(f"✅ Unterkategorie gefunden (ID: {subcategory.id})")
            
            # 3. Prüfe ob Modul bereits existiert
            existing_module = LearningModule.query.filter_by(
                slug='how-to-find-dep'
            ).first()
            
            if existing_module:
                print("⚠️ Modul 'how-to-find-dep' existiert bereits!")
                print("   Aktualisiere bestehenden Eintrag...")
                
                # Update existing
                existing_module.category_id = main_category.id
                existing_module.subcategory_id = subcategory.id
                existing_module.title = "How to find DEP - Deep Episodic Pivots"
                existing_module.description = "Lerne verzögerte Reaktionen zu finden: Der 'Delayed Reaction 9 Million' Scan, Setup-Typen, Timing-Regeln und die Kunst der Priorisierung. StockBee Guide für katalysator-basiertes Trading."
                existing_module.icon = "🔍"
                existing_module.content_type = "html"
                existing_module.template_file = "how-to-find-dep.html"
                existing_module.is_published = True
                existing_module.is_lead_magnet = False
                existing_module.estimated_duration = 30
                existing_module.difficulty_level = "intermediate"
                existing_module.sort_order = 20
                
                print("✅ Modul aktualisiert")
                
            else:
                print("📝 Erstelle neues Modul 'How to find DEP'...")
                
                # Create new module
                new_module = LearningModule(
                    category_id=main_category.id,
                    subcategory_id=subcategory.id,
                    title="How to find DEP - Deep Episodic Pivots",
                    slug="how-to-find-dep",
                    description="Lerne verzögerte Reaktionen zu finden: Der 'Delayed Reaction 9 Million' Scan, Setup-Typen, Timing-Regeln und die Kunst der Priorisierung. StockBee Guide für katalysator-basiertes Trading.",
                    icon="🔍",
                    content_type="html",
                    template_file="how-to-find-dep.html",
                    is_published=True,
                    is_lead_magnet=False,  # Premium Modul
                    estimated_duration=30,  # 30 Minuten
                    difficulty_level="intermediate",  # Fortgeschritten
                    sort_order=20
                )
                
                db.session.add(new_module)
                print("✅ Modul erstellt")
            
            # 4. Commit to database
            db.session.commit()
            
            print("\n" + "="*60)
            print("✅ How to find DEP Modul erfolgreich registriert!")
            print("="*60)
            print(f"\n📊 Details:")
            print(f"   Hauptkategorie: {main_category.name}")
            print(f"   Unterkategorie: {subcategory.name}")
            print(f"   Modul-Slug: how-to-find-dep")
            print(f"   Template: templates/how-to-find-dep.html")
            print(f"   Status: Premium (Premium/Elite/Elite Pro)")
            print(f"   Schwierigkeit: Fortgeschritten")
            print(f"   Dauer: 30 Minuten")
            print(f"\n🌐 URL: /how-to-find-dep")
            print(f"📱 Admin: /admin/modules")
            print("\n✅ Bereit für Deployment!")
            
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
    print("🔍 How to find DEP Modul Migration")
    print("="*60 + "\n")
    
    success = register_how_to_find_dep_module()
    
    if success:
        print("\n✅ Migration erfolgreich abgeschlossen!")
    else:
        print("\n❌ Migration fehlgeschlagen!")
        sys.exit(1)

