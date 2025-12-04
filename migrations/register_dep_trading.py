"""
Migrations-Script: DEP Trading Modul registrieren

Dieses Script registriert das "DEP Trading - Deep Episodic Pivots" Modul in der Datenbank.
Basierend auf StockBee's Guide "How to find DEP - Deep Episodic Pivots".

Verwendung:
    python migrations/register_dep_trading.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, LearningModule, ModuleCategory, ModuleSubcategory

def register_dep_trading_module():
    """Registriert das DEP Trading Modul in der Datenbank"""
    
    with app.app_context():
        try:
            print("🚀 Starte DEP Trading Modul-Registrierung...")
            
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
            
            # 2. Finde oder erstelle Unterkategorie "Episodic Pivots"
            subcategory = ModuleSubcategory.query.filter_by(
                category_id=main_category.id,
                name="Episodic Pivots"
            ).first()
            
            if not subcategory:
                print("📂 Erstelle Unterkategorie 'Episodic Pivots'...")
                subcategory = ModuleSubcategory(
                    category_id=main_category.id,
                    name="Episodic Pivots",
                    slug="episodic-pivots",
                    description="Deep Episodic Pivots (DEP) - Delayed Reaction Setups",
                    icon="🎯",
                    sort_order=3
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
                existing_module.title = "DEP Trading - Deep Episodic Pivots finden"
                existing_module.description = "Lerne wie du delayed reaction EP Setups findest. Ein einfacher Scan, 5-10 Minuten täglich, 2-3 Kandidaten pro Tag. StockBee's bewährte Methode für profitable DEP-Trades."
                existing_module.icon = "🎯"
                existing_module.content_type = "html"
                existing_module.template_file = "dep-trading.html"
                existing_module.is_published = True
                existing_module.is_lead_magnet = False
                existing_module.estimated_duration = 30
                existing_module.difficulty_level = "intermediate"
                existing_module.sort_order = 20
                
                print("✅ Modul aktualisiert")
                
            else:
                print("📝 Erstelle neues Modul 'DEP Trading'...")
                
                # Create new module
                new_module = LearningModule(
                    category_id=main_category.id,
                    subcategory_id=subcategory.id,
                    title="DEP Trading - Deep Episodic Pivots finden",
                    slug="how-to-find-dep",
                    description="Lerne wie du delayed reaction EP Setups findest. Ein einfacher Scan, 5-10 Minuten täglich, 2-3 Kandidaten pro Tag. StockBee's bewährte Methode für profitable DEP-Trades.",
                    icon="🎯",
                    content_type="html",
                    template_file="dep-trading.html",
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
            print("✅ DEP Trading Modul erfolgreich registriert!")
            print("="*60)
            print(f"\n📊 Details:")
            print(f"   Hauptkategorie: {main_category.name}")
            print(f"   Unterkategorie: {subcategory.name}")
            print(f"   Modul-Slug: how-to-find-dep")
            print(f"   Template: templates/dep-trading.html")
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
    print("🎯 DEP Trading Modul Migration")
    print("="*60 + "\n")
    
    success = register_dep_trading_module()
    
    if success:
        print("\n✅ Migration erfolgreich abgeschlossen!")
    else:
        print("\n❌ Migration fehlgeschlagen!")
        sys.exit(1)

