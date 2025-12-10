#!/usr/bin/env python3
"""
Migration Script: Breakout Trading Modul registrieren
Erstellt: 10. Dezember 2025
Beschreibung: Registriert das Breakout Trading Modul in der Datenbank
"""

import sys
import os

# Füge das Hauptverzeichnis zum Pfad hinzu
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, LearningModule, ModuleCategory, ModuleSubcategory

def register_breakout_trading():
    """Registriert das Breakout Trading Modul"""
    
    with app.app_context():
        # Prüfe ob Modul bereits existiert
        existing = LearningModule.query.filter_by(slug='breakout-trading').first()
        if existing:
            print(f"✅ Modul 'breakout-trading' existiert bereits (ID: {existing.id})")
            return existing
        
        # Finde oder erstelle die Kategorie "Trading-Setups"
        category = ModuleCategory.query.filter_by(slug='trading-setups').first()
        if not category:
            # Erstelle die Kategorie
            category = ModuleCategory(
                name='Trading-Setups',
                slug='trading-setups',
                description='Verschiedene Trading-Setups und Strategien',
                icon='📈',
                sort_order=5,
                is_published=True
            )
            db.session.add(category)
            db.session.commit()
            print(f"➕ Kategorie 'Trading-Setups' erstellt (ID: {category.id})")
        
        # Finde oder erstelle die Unterkategorie "Breakout Trading"
        subcategory = ModuleSubcategory.query.filter_by(slug='breakout-trading-setups').first()
        if not subcategory:
            subcategory = ModuleSubcategory(
                name='Breakout Trading',
                slug='breakout-trading-setups',
                description='Alles über Breakout-Strategien und Entry-Techniken',
                icon='🚀',
                category_id=category.id,
                sort_order=1,
                is_published=True
            )
            db.session.add(subcategory)
            db.session.commit()
            print(f"➕ Unterkategorie 'Breakout Trading' erstellt (ID: {subcategory.id})")
        
        # Erstelle das Modul
        module = LearningModule(
            title='Breakout Trading Meistern',
            slug='breakout-trading',
            description='Lerne die präzise Definition von Breakouts, die drei Arten und warum der erste Tag der einzig valide Einstiegstag ist.',
            template_file='breakout-trading.html',
            icon='🚀',
            difficulty='Fortgeschritten',
            duration_minutes=60,
            subcategory_id=subcategory.id,
            sort_order=1,
            is_published=True,
            is_premium=True,
            required_subscription='premium'
        )
        
        db.session.add(module)
        db.session.commit()
        
        print(f"✅ Modul 'Breakout Trading Meistern' erfolgreich registriert!")
        print(f"   ID: {module.id}")
        print(f"   Slug: {module.slug}")
        print(f"   Kategorie: {category.name}")
        print(f"   Unterkategorie: {subcategory.name}")
        print(f"   Subscription: {module.required_subscription}")
        print(f"   Route: /breakout-trading")
        
        return module

if __name__ == '__main__':
    print("=" * 50)
    print("🔧 Breakout Trading Modul Migration")
    print("=" * 50)
    
    try:
        module = register_breakout_trading()
        print("\n✅ Migration erfolgreich abgeschlossen!")
    except Exception as e:
        print(f"\n❌ Fehler bei Migration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

