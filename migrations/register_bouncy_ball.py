"""
Migration Script: Bouncy Ball Setup Modul registrieren
Datum: 14. November 2024
Beschreibung: Registriert das Bouncy Ball Setup Modul in der Datenbank
"""

import sys
import os

# Füge Parent-Directory zum Python-Path hinzu
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, LearningModule, ModuleCategory, ModuleSubcategory
from datetime import datetime

def register_bouncy_ball_module():
    """Registriere Bouncy Ball Setup Modul"""
    with app.app_context():
        try:
            # Prüfe ob Modul bereits existiert
            existing_module = LearningModule.query.filter_by(slug='bouncy-ball-setup').first()
            if existing_module:
                print(f"✅ Modul 'bouncy-ball-setup' existiert bereits (ID: {existing_module.id})")
                print(f"   Aktualisiere Modul-Details...")
                
                # Update existing module
                existing_module.title = "Bouncy Ball Setup"
                existing_module.description = "Didis-Charts Intraday-Strategie für explosive Breakouts und Breakdowns nach Konsolidierung. Lerne die 4 kritischen Merkmale und analysiere Real-World-Beispiele von VVOS, SMCI und Ford."
                existing_module.icon = "🎾"
                existing_module.content_type = "html"
                existing_module.template_file = "bouncy-ball-setup.html"
                existing_module.is_published = True
                existing_module.is_lead_magnet = False
                existing_module.required_subscription_levels = ['premium', 'elite', 'elite_pro']
                existing_module.estimated_duration = 45
                existing_module.difficulty_level = "advanced"
                
                db.session.commit()
                print(f"✅ Modul erfolgreich aktualisiert!")
                return
            
            # Suche die richtige Kategorie - Didis-Charts System III
            category = ModuleCategory.query.filter_by(slug='elite-system-iii').first()
            if not category:
                # Fallback: Technische Analyse
                category = ModuleCategory.query.filter_by(slug='technische-analyse').first()
            
            if not category:
                print("❌ Fehler: Keine passende Kategorie gefunden!")
                print("   Erstelle Kategorie 'Didis-Charts System III'...")
                
                category = ModuleCategory(
                    name="Didis-Charts System III",
                    slug="elite-system-iii",
                    description="Didis-Charts Elite Trading System - Fortgeschrittene Intraday-Strategien",
                    icon="👑",
                    sort_order=6,
                    is_published=True,
                    required_subscription_level='elite'
                )
                db.session.add(category)
                db.session.commit()
                print(f"✅ Kategorie erstellt (ID: {category.id})")
            
            # Prüfe/Erstelle Unterkategorie "Intraday-Setups"
            subcategory = ModuleSubcategory.query.filter_by(
                category_id=category.id,
                slug='intraday-setups'
            ).first()
            
            if not subcategory:
                print("   Erstelle Unterkategorie 'Intraday-Setups'...")
                subcategory = ModuleSubcategory(
                    category_id=category.id,
                    name="Intraday-Setups",
                    slug="intraday-setups",
                    description="Bewährte Intraday Trading Setups für aktive Trader",
                    icon="⚡",
                    sort_order=1
                )
                db.session.add(subcategory)
                db.session.commit()
                print(f"✅ Unterkategorie erstellt (ID: {subcategory.id})")
            
            # Finde höchste sort_order in dieser Unterkategorie
            max_order = db.session.query(db.func.max(LearningModule.sort_order)).filter_by(
                subcategory_id=subcategory.id
            ).scalar() or 0
            
            # Erstelle neues Modul
            new_module = LearningModule(
                category_id=category.id,
                subcategory_id=subcategory.id,
                title="Bouncy Ball Setup",
                slug="bouncy-ball-setup",
                description="Didis-Charts Intraday-Strategie für explosive Breakouts und Breakdowns nach Konsolidierung. Lerne die 4 kritischen Merkmale und analysiere Real-World-Beispiele von VVOS, SMCI und Ford.",
                icon="🎾",
                content_type="html",
                template_file="bouncy-ball-setup.html",
                is_published=True,
                is_lead_magnet=False,
                required_subscription_levels=['premium', 'elite', 'elite_pro'],
                estimated_duration=45,  # 45 Minuten
                difficulty_level="advanced",
                sort_order=max_order + 1,
                view_count=0
            )
            
            db.session.add(new_module)
            db.session.commit()
            
            print(f"✅ Modul 'Bouncy Ball Setup' erfolgreich registriert!")
            print(f"   - ID: {new_module.id}")
            print(f"   - Kategorie: {category.name} (ID: {category.id})")
            print(f"   - Unterkategorie: {subcategory.name} (ID: {subcategory.id})")
            print(f"   - Slug: {new_module.slug}")
            print(f"   - Route: /bouncy-ball-setup")
            print(f"   - Subscription: Premium/Elite/Elite Pro")
            print(f"   - Schwierigkeit: Fortgeschritten")
            print(f"   - Dauer: 45 Minuten")
            print(f"   - Sort Order: {new_module.sort_order}")
            
        except Exception as e:
            print(f"❌ Fehler beim Registrieren des Moduls: {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()

if __name__ == "__main__":
    print("=" * 60)
    print("Bouncy Ball Setup - Modul-Registrierung")
    print("=" * 60)
    register_bouncy_ball_module()
    print("=" * 60)
    print("✅ Migration abgeschlossen!")
    print("\n📝 Nächste Schritte:")
    print("   1. Lade die Screenshot-Bilder hoch:")
    print("      - VVOS_Phase1_Anstieg.jpg")
    print("      - VVOS_Phase2_Konsolidierung.jpg")
    print("      - VVOS_Phase3_Breakout.jpg")
    print("      - SMCI_Phase1_Abverkauf.jpg")
    print("      - SMCI_Phase2_Konsolidierung.jpg")
    print("      - Ford_Earnings_Breakdown.jpg")
    print("   2. Speichere Bilder in: static/screenshots/")
    print("   3. Teste Route: http://localhost:5000/bouncy-ball-setup")
    print("   4. Git push für Railway Deployment")
    print("=" * 60)

