"""
Migrations-Script: Breaking News Trading Modul registrieren

Dieses Script registriert das "Breaking News Trading" Modul in der Datenbank.
Basierend auf Lance Breitstein's 3-teiliger News-Trading-Strategie.

Verwendung:
    python migrations/register_breaking_news_trading.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, LearningModule, ModuleCategory, ModuleSubcategory

def register_breaking_news_trading_module():
    """Registriert das Breaking News Trading Modul in der Datenbank"""
    
    with app.app_context():
        try:
            print("🚀 Starte Breaking News Trading Modul-Registrierung...")
            
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
            
            # 2. Finde oder erstelle Unterkategorie "News Trading"
            subcategory = ModuleSubcategory.query.filter_by(
                category_id=main_category.id,
                name="News Trading"
            ).first()
            
            if not subcategory:
                print("📂 Erstelle Unterkategorie 'News Trading'...")
                subcategory = ModuleSubcategory(
                    category_id=main_category.id,
                    name="News Trading",
                    slug="news-trading",
                    description="Strategien zum Handeln von Breaking News und Katalysatoren",
                    icon="📰",
                    sort_order=2
                )
                db.session.add(subcategory)
                db.session.flush()
                print(f"✅ Unterkategorie erstellt (ID: {subcategory.id})")
            else:
                print(f"✅ Unterkategorie gefunden (ID: {subcategory.id})")
            
            # 3. Prüfe ob Modul bereits existiert
            existing_module = LearningModule.query.filter_by(
                slug='breaking-news-trading'
            ).first()
            
            if existing_module:
                print("⚠️ Modul 'breaking-news-trading' existiert bereits!")
                print("   Aktualisiere bestehenden Eintrag...")
                
                # Update existing
                existing_module.category_id = main_category.id
                existing_module.subcategory_id = subcategory.id
                existing_module.title = "Breaking News Trading - Die Kunst der News-Analyse"
                existing_module.description = "Lerne News-Quellen zu nutzen, Filter aufzubauen und Headlines zu analysieren. Lance Breitstein's 3-teilige Strategie für profitables News-Trading."
                existing_module.icon = "📰"
                existing_module.content_type = "html"
                existing_module.template_file = "breaking-news-trading.html"
                existing_module.is_published = True
                existing_module.is_lead_magnet = False
                existing_module.estimated_duration = 45
                existing_module.difficulty_level = "intermediate"
                existing_module.sort_order = 15
                
                print("✅ Modul aktualisiert")
                
            else:
                print("📝 Erstelle neues Modul 'Breaking News Trading'...")
                
                # Create new module
                new_module = LearningModule(
                    category_id=main_category.id,
                    subcategory_id=subcategory.id,
                    title="Breaking News Trading - Die Kunst der News-Analyse",
                    slug="breaking-news-trading",
                    description="Lerne News-Quellen zu nutzen, Filter aufzubauen und Headlines zu analysieren. Lance Breitstein's 3-teilige Strategie für profitables News-Trading.",
                    icon="📰",
                    content_type="html",
                    template_file="breaking-news-trading.html",
                    is_published=True,
                    is_lead_magnet=False,  # Premium Modul
                    estimated_duration=45,  # 45 Minuten
                    difficulty_level="intermediate",  # Fortgeschritten
                    sort_order=15
                )
                
                db.session.add(new_module)
                print("✅ Modul erstellt")
            
            # 4. Commit to database
            db.session.commit()
            
            print("\n" + "="*60)
            print("✅ Breaking News Trading Modul erfolgreich registriert!")
            print("="*60)
            print(f"\n📊 Details:")
            print(f"   Hauptkategorie: {main_category.name}")
            print(f"   Unterkategorie: {subcategory.name}")
            print(f"   Modul-Slug: breaking-news-trading")
            print(f"   Template: templates/breaking-news-trading.html")
            print(f"   Status: Premium (Elite/Elite Pro)")
            print(f"   Schwierigkeit: Fortgeschritten")
            print(f"   Dauer: 45 Minuten")
            print(f"\n🌐 URL: /module/breaking-news-trading")
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
    print("📰 Breaking News Trading Modul Migration")
    print("="*60 + "\n")
    
    success = register_breaking_news_trading_module()
    
    if success:
        print("\n✅ Migration erfolgreich abgeschlossen!")
    else:
        print("\n❌ Migration fehlgeschlagen!")
        sys.exit(1)



