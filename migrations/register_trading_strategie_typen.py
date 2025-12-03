#!/usr/bin/env python3
"""
Migration Script: Trading Strategie Typen Modul registrieren
Basierend auf Lance Breitstein's Trading-Framework

Ausführen mit:
    python migrations/register_trading_strategie_typen.py
"""

import sys
import os

# Projektpfad hinzufügen
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, LearningModule, ModuleCategory, ModuleSubcategory

def register_module():
    """Registriert das Trading Strategie Typen Modul in der Datenbank"""
    
    with app.app_context():
        # Prüfen ob Modul bereits existiert
        existing = LearningModule.query.filter_by(slug='trading-strategie-typen').first()
        if existing:
            print("✅ Modul 'trading-strategie-typen' existiert bereits!")
            print(f"   ID: {existing.id}")
            print(f"   Titel: {existing.title}")
            print(f"   Kategorie: {existing.subcategory.name if existing.subcategory else 'Keine'}")
            return existing
        
        # Kategorie finden oder erstellen: Trading-Psychologie
        category = ModuleCategory.query.filter_by(slug='trading-psychologie').first()
        if not category:
            # Alternative: Trading-Grundlagen
            category = ModuleCategory.query.filter_by(slug='trading-grundlagen').first()
        if not category:
            # Fallback: Neue Kategorie erstellen
            category = ModuleCategory(
                name='Trading-Psychologie',
                slug='trading-psychologie',
                description='Module zur Trading-Psychologie und Mindset',
                sort_order=10,
                icon='🧠'
            )
            db.session.add(category)
            db.session.flush()
            print("📁 Neue Kategorie 'Trading-Psychologie' erstellt")
        
        # Unterkategorie finden oder erstellen: Strategie-Framework
        subcategory = ModuleSubcategory.query.filter_by(slug='strategie-framework').first()
        if not subcategory:
            subcategory = ModuleSubcategory.query.filter_by(slug='grundlagen').first()
        if not subcategory:
            # Erstelle neue Unterkategorie
            subcategory = ModuleSubcategory(
                name='Strategie-Framework',
                slug='strategie-framework',
                description='Grundlegende Trading-Konzepte und Frameworks',
                category_id=category.id,
                sort_order=1,
                icon='📊'
            )
            db.session.add(subcategory)
            db.session.flush()
            print("📂 Neue Unterkategorie 'Strategie-Framework' erstellt")
        
        # Neues Modul erstellen
        new_module = LearningModule(
            title='Trading Strategie Typen',
            slug='trading-strategie-typen',
            description='Verstehe die zwei fundamentalen Trading-Strategietypen: Price Expansion und Price Reversion. Lerne, wann welche Strategie funktioniert und warum du beide beherrschen solltest.',
            template_file='trading-strategie-typen.html',
            subcategory_id=subcategory.id,
            required_subscription='premium',  # Premium/Elite/Elite Pro
            estimated_duration=30,  # 30 Minuten
            difficulty='Anfänger',
            is_published=True,
            sort_order=1,
            icon='📊'
        )
        
        db.session.add(new_module)
        db.session.commit()
        
        print("✅ Modul erfolgreich registriert!")
        print(f"   ID: {new_module.id}")
        print(f"   Titel: {new_module.title}")
        print(f"   Slug: {new_module.slug}")
        print(f"   Kategorie: {category.name}")
        print(f"   Unterkategorie: {subcategory.name}")
        print(f"   Subscription: {new_module.required_subscription}")
        print(f"   Dauer: {new_module.estimated_duration} Minuten")
        print(f"   Schwierigkeit: {new_module.difficulty}")
        print(f"   Veröffentlicht: {'Ja' if new_module.is_published else 'Nein'}")
        
        return new_module


def main():
    print("\n" + "="*60)
    print("📊 Trading Strategie Typen - Modul Migration")
    print("="*60 + "\n")
    
    try:
        module = register_module()
        print("\n" + "="*60)
        print("🎉 Migration erfolgreich abgeschlossen!")
        print("="*60)
        print("\n🔗 Das Modul ist erreichbar unter:")
        print("   → /trading-strategie-typen")
        print("   → /module/trading-strategie-typen")
        print("\n")
    except Exception as e:
        print(f"\n❌ Fehler bei der Migration: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

