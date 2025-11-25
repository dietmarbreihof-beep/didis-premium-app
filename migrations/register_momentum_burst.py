"""
Migrations-Script: Momentum Burst Modul registrieren

Dieses Script registriert das "Momentum Burst" Modul in der Datenbank.
Basierend auf StockBee Guides - fortgeschrittenes Trading-Setup.

Verwendung:
    python migrations/register_momentum_burst.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, LearningModule, ModuleCategory, ModuleSubcategory

def register_momentum_burst_module():
    """Registriert das Momentum Burst Modul in der Datenbank"""
    
    with app.app_context():
        try:
            print("🚀 Starte Momentum Burst Modul-Registrierung...")
            
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
                    description="Kurzfristige Momentum-basierte Trades",
                    icon="📈",
                    sort_order=1
                )
                db.session.add(subcategory)
                db.session.flush()
                print(f"✅ Unterkategorie erstellt (ID: {subcategory.id})")
            else:
                print(f"✅ Unterkategorie gefunden (ID: {subcategory.id})")
            
            # 3. Prüfe ob Modul bereits existiert
            existing_module = LearningModule.query.filter_by(
                slug='momentum-burst'
            ).first()
            
            if existing_module:
                print("⚠️ Modul 'momentum-burst' existiert bereits!")
                print("   Aktualisiere bestehenden Eintrag...")
                
                # Update existing
                existing_module.category_id = main_category.id
                existing_module.subcategory_id = subcategory.id
                existing_module.title = "Momentum Burst - Die 3-5 Tage Profit-Formel"
                existing_module.description = "Lerne das Momentum Burst Setup: 8-40% Gewinn in 3-5 Tagen durch Range Expansion und perfektes Timing. Inkl. Mythen-Busting und Trading-Checkliste."
                existing_module.icon = "📈"
                existing_module.content_type = "html"
                existing_module.template_file = "momentum-burst.html"
                existing_module.is_published = True
                existing_module.is_lead_magnet = False
                existing_module.estimated_duration = 60
                existing_module.difficulty_level = "advanced"
                existing_module.sort_order = 10
                
                print("✅ Modul aktualisiert")
                
            else:
                print("📝 Erstelle neues Modul 'Momentum Burst'...")
                
                # Create new module
                new_module = LearningModule(
                    category_id=main_category.id,
                    subcategory_id=subcategory.id,
                    title="Momentum Burst - Die 3-5 Tage Profit-Formel",
                    slug="momentum-burst",
                    description="Lerne das Momentum Burst Setup: 8-40% Gewinn in 3-5 Tagen durch Range Expansion und perfektes Timing. Inkl. Mythen-Busting und Trading-Checkliste.",
                    icon="📈",
                    content_type="html",
                    template_file="momentum-burst.html",
                    is_published=True,
                    is_lead_magnet=False,  # Premium Modul
                    estimated_duration=60,  # 60 Minuten
                    difficulty_level="advanced",  # Fortgeschritten
                    sort_order=10
                )
                
                db.session.add(new_module)
                print("✅ Modul erstellt")
            
            # 4. Commit to database
            db.session.commit()
            
            print("\n" + "="*60)
            print("✅ Momentum Burst Modul erfolgreich registriert!")
            print("="*60)
            print(f"\n📊 Details:")
            print(f"   Hauptkategorie: {main_category.name}")
            print(f"   Unterkategorie: {subcategory.name}")
            print(f"   Modul-Slug: momentum-burst")
            print(f"   Template: templates/momentum-burst.html")
            print(f"   Status: Premium (Elite/Elite Pro)")
            print(f"   Schwierigkeit: Fortgeschritten")
            print(f"   Dauer: 60 Minuten")
            print(f"\n🌐 URL: /module/momentum-burst")
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
    print("🚀 Momentum Burst Modul Migration")
    print("="*60 + "\n")
    
    success = register_momentum_burst_module()
    
    if success:
        print("\n✅ Migration erfolgreich abgeschlossen!")
    else:
        print("\n❌ Migration fehlgeschlagen!")
        sys.exit(1)



