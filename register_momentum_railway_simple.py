"""
Vereinfachtes Migrations-Script für Railway (ohne Emojis)
Registriert Momentum Burst Modul in der Datenbank
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, LearningModule, ModuleCategory, ModuleSubcategory

def register_momentum_burst():
    """Registriert das Momentum Burst Modul"""
    
    with app.app_context():
        try:
            print("=" * 60)
            print("Momentum Burst Modul-Registrierung")
            print("=" * 60)
            
            # 1. Finde oder erstelle Hauptkategorie
            main_category = ModuleCategory.query.filter_by(
                slug="trading-setups"
            ).first()
            
            if not main_category:
                print("Erstelle Hauptkategorie 'Trading-Setups'...")
                main_category = ModuleCategory(
                    name="Trading-Setups",
                    slug="trading-setups",
                    description="Bewaehrte Trading-Setups und Strategien",
                    icon="TARGET",
                    sort_order=5
                )
                db.session.add(main_category)
                db.session.flush()
                print(f"OK - Hauptkategorie erstellt (ID: {main_category.id})")
            else:
                print(f"OK - Hauptkategorie gefunden (ID: {main_category.id})")
            
            # 2. Finde oder erstelle Unterkategorie
            subcategory = ModuleSubcategory.query.filter_by(
                category_id=main_category.id,
                slug="momentum-trading"
            ).first()
            
            if not subcategory:
                print("Erstelle Unterkategorie 'Momentum Trading'...")
                subcategory = ModuleSubcategory(
                    category_id=main_category.id,
                    name="Momentum Trading",
                    slug="momentum-trading",
                    description="Kurzfristige Momentum-basierte Trades",
                    icon="CHART",
                    sort_order=1
                )
                db.session.add(subcategory)
                db.session.flush()
                print(f"OK - Unterkategorie erstellt (ID: {subcategory.id})")
            else:
                print(f"OK - Unterkategorie gefunden (ID: {subcategory.id})")
            
            # 3. Prüfe ob Modul bereits existiert
            existing_module = LearningModule.query.filter_by(
                slug='momentum-burst'
            ).first()
            
            if existing_module:
                print("WARNUNG: Modul existiert bereits!")
                print("Aktualisiere bestehenden Eintrag...")
                
                existing_module.category_id = main_category.id
                existing_module.subcategory_id = subcategory.id
                existing_module.title = "Momentum Burst - Die 3-5 Tage Profit-Formel"
                existing_module.description = "Lerne das Momentum Burst Setup: 8-40% Gewinn in 3-5 Tagen durch Range Expansion und perfektes Timing."
                existing_module.icon = "CHART_UP"
                existing_module.content_type = "html"
                existing_module.template_file = "momentum-burst.html"
                existing_module.is_published = True
                existing_module.is_lead_magnet = False
                existing_module.estimated_duration = 60
                existing_module.difficulty_level = "advanced"
                existing_module.sort_order = 10
                
                print("OK - Modul aktualisiert")
                
            else:
                print("Erstelle neues Modul 'Momentum Burst'...")
                
                new_module = LearningModule(
                    category_id=main_category.id,
                    subcategory_id=subcategory.id,
                    title="Momentum Burst - Die 3-5 Tage Profit-Formel",
                    slug="momentum-burst",
                    description="Lerne das Momentum Burst Setup: 8-40% Gewinn in 3-5 Tagen durch Range Expansion und perfektes Timing.",
                    icon="CHART_UP",
                    content_type="html",
                    template_file="momentum-burst.html",
                    is_published=True,
                    is_lead_magnet=False,
                    estimated_duration=60,
                    difficulty_level="advanced",
                    sort_order=10
                )
                
                db.session.add(new_module)
                print("OK - Modul erstellt")
            
            # 4. Commit
            db.session.commit()
            
            print("\n" + "=" * 60)
            print("ERFOLGREICH: Momentum Burst Modul registriert!")
            print("=" * 60)
            print("\nDetails:")
            print(f"  Kategorie: {main_category.name}")
            print(f"  Unterkategorie: {subcategory.name}")
            print(f"  Slug: momentum-burst")
            print(f"  Template: momentum-burst.html")
            print(f"  Status: Premium (Elite/Elite Pro)")
            print(f"\nURL: /module/momentum-burst")
            print("Admin: /admin/modules")
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"\nFEHLER: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    success = register_momentum_burst()
    
    if success:
        print("\nMigration erfolgreich!")
        sys.exit(0)
    else:
        print("\nMigration fehlgeschlagen!")
        sys.exit(1)



