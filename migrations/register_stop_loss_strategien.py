#!/usr/bin/env python3
"""
Migration Script: Stop-Loss Strategien Modul registrieren
Erstellt: 12. Dezember 2025
Beschreibung: Registriert das Stop-Loss Strategien Modul in der Datenbank
Quelle: Lance Breitstein - Stop Loss Guide
"""

import sys
import os

# Füge das Hauptverzeichnis zum Pfad hinzu
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, LearningModule, ModuleCategory, ModuleSubcategory

def register_stop_loss_strategien():
    """Registriert das Stop-Loss Strategien Modul"""
    
    with app.app_context():
        # Prüfe ob Modul bereits existiert
        existing = LearningModule.query.filter_by(slug='stop-loss-strategien').first()
        if existing:
            print(f"✅ Modul 'stop-loss-strategien' existiert bereits (ID: {existing.id})")
            return existing
        
        # Finde oder erstelle die Kategorie "Risikomanagement"
        category = ModuleCategory.query.filter_by(slug='risikomanagement').first()
        if not category:
            # Erstelle die Kategorie
            category = ModuleCategory(
                name='Risikomanagement',
                slug='risikomanagement',
                description='Alles über Risikomanagement, Position Sizing und Stop-Loss Strategien',
                icon='🛡️',
                sort_order=4,
                is_published=True
            )
            db.session.add(category)
            db.session.commit()
            print(f"➕ Kategorie 'Risikomanagement' erstellt (ID: {category.id})")
        
        # Finde oder erstelle die Unterkategorie "Stop-Loss Strategien"
        subcategory = ModuleSubcategory.query.filter_by(slug='stop-loss-strategien-sub').first()
        if not subcategory:
            subcategory = ModuleSubcategory(
                name='Stop-Loss Strategien',
                slug='stop-loss-strategien-sub',
                description='Professionelle Stop-Loss Techniken und Exits',
                icon='🎯',
                category_id=category.id,
                sort_order=2
            )
            db.session.add(subcategory)
            db.session.commit()
            print(f"➕ Unterkategorie 'Stop-Loss Strategien' erstellt (ID: {subcategory.id})")
        
        # Erstelle das Modul
        module = LearningModule(
            title='Stop-Loss wie die Profis',
            slug='stop-loss-strategien',
            description='Lerne wie professionelle Trader ihre Stops setzen – basierend auf Logik, Daten und Strategie. 5 bewährte Strategien mit Kerzen-Charts.',
            template_file='stop-loss-strategien.html',
            icon='🛡️',
            estimated_duration=45,
            category_id=category.id,
            subcategory_id=subcategory.id,
            sort_order=1,
            is_published=True,
            is_lead_magnet=False,
            required_subscription_levels=['premium', 'elite', 'elite_pro', 'masterclass']
        )
        
        db.session.add(module)
        db.session.commit()
        
        print(f"✅ Modul 'Stop-Loss wie die Profis' erfolgreich registriert!")
        print(f"   ID: {module.id}")
        print(f"   Slug: {module.slug}")
        print(f"   Kategorie: {category.name}")
        print(f"   Unterkategorie: {subcategory.name}")
        print(f"   Subscription-Levels: {module.required_subscription_levels}")
        print(f"   Route: /stop-loss-strategien")
        print(f"")
        print(f"📊 Enthaltene Grafiken (5 SVGs):")
        print(f"   - stop_loss_breakout.svg (Breakout Stop)")
        print(f"   - stop_loss_trend.svg (Higher Lows)")
        print(f"   - stop_loss_moving_average.svg (MA Surfing)")
        print(f"   - stop_loss_trendline.svg (Trendlinie)")
        print(f"   - stop_loss_trailing.svg (Trailing Stop)")
        
        return module

if __name__ == '__main__':
    print("=" * 60)
    print("🔧 Stop-Loss Strategien Modul Migration")
    print("   Quelle: Lance Breitstein - How to Set Stop Losses")
    print("=" * 60)
    
    try:
        module = register_stop_loss_strategien()
        print("\n✅ Migration erfolgreich abgeschlossen!")
    except Exception as e:
        print(f"\n❌ Fehler bei Migration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


