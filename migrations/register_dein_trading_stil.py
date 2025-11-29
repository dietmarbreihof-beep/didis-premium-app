#!/usr/bin/env python3
"""
Migration Script: Registriere "Dein Trading-Stil" Modul
Erstellt: November 2025
Beschreibung: StockBee-basiertes Lernmodul über die wichtigste Entscheidung - den Trading-Stil wählen

Verwendung:
    python migrations/register_dein_trading_stil.py

Das Modul wird in der Kategorie "Trading-Psychologie" / "Grundlagen" registriert.
"""

import sys
import os

# Füge das Projektverzeichnis zum Python-Pfad hinzu
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, ModuleCategory, ModuleSubcategory, LearningModule

def register_module():
    """Registriert das 'Dein Trading-Stil' Modul in der Datenbank."""
    
    with app.app_context():
        # Prüfe ob Modul bereits existiert
        existing_module = LearningModule.query.filter_by(slug='dein-trading-stil').first()
        
        if existing_module:
            print(f"✅ Modul bereits vorhanden: {existing_module.title}")
            print(f"   Template: {existing_module.template_file}")
            print(f"   Kategorie: {existing_module.subcategory.name if existing_module.subcategory else 'Keine'}")
            return existing_module
        
        # Finde die passende Kategorie (gleiche wie "Wie man Trader wird")
        category = ModuleCategory.query.filter(
            ModuleCategory.name.ilike('%psychologie%')
        ).first()
        
        if not category:
            category = ModuleCategory.query.filter(
                ModuleCategory.name.ilike('%grundlagen%')
            ).first()
        
        if not category:
            # Erstelle neue Kategorie wenn keine passende gefunden
            category = ModuleCategory.query.filter_by(slug='neue-module').first()
            if not category:
                category = ModuleCategory(
                    name='🆕 Neue Module',
                    slug='neue-module',
                    description='Neu hinzugefügte Module zur Kategorisierung',
                    sort_order=999
                )
                db.session.add(category)
                db.session.flush()
                print(f"📁 Kategorie erstellt: {category.name}")
        
        # Finde oder erstelle Unterkategorie "Trading-Grundlagen"
        subcategory = None
        if category:
            subcategory = ModuleSubcategory.query.filter(
                ModuleSubcategory.category_id == category.id,
                ModuleSubcategory.slug == 'trading-grundlagen'
            ).first()
            
            if not subcategory:
                # Versuche jede Unterkategorie in dieser Kategorie
                subcategory = ModuleSubcategory.query.filter(
                    ModuleSubcategory.category_id == category.id
                ).first()
            
            if not subcategory:
                subcategory = ModuleSubcategory(
                    name='Trading-Grundlagen',
                    slug='trading-grundlagen',
                    category_id=category.id,
                    description='Fundamentale Konzepte für angehende Trader',
                    sort_order=1
                )
                db.session.add(subcategory)
                db.session.flush()
                print(f"📂 Unterkategorie erstellt: {subcategory.name}")
        
        # Ermittle die nächste sort_order (nach "Wie man Trader wird")
        existing_wie_man = LearningModule.query.filter_by(slug='wie-man-trader-wird').first()
        sort_order = 2  # Standard: nach "Wie man Trader wird"
        if existing_wie_man:
            sort_order = existing_wie_man.sort_order + 1
        
        # Erstelle das Modul
        new_module = LearningModule(
            title='Dein Trading-Stil: Die wichtigste Entscheidung',
            slug='dein-trading-stil',
            description='Die wichtigste Entscheidung, die du als Trader treffen wirst: Day-Trading, Swing-Trading oder Position-Trading? Basierend auf StockBee-Weisheiten über Persönlichkeit, Lifestyle, Kapital und Volatilitätsrisiko.',
            content_type='html',
            template_file='dein-trading-stil.html',
            difficulty='Anfänger',
            duration_minutes=35,
            subscription_required='premium',
            subcategory_id=subcategory.id if subcategory else None,
            sort_order=sort_order,
            is_published=True,
            view_count=0
        )
        
        db.session.add(new_module)
        db.session.commit()
        
        print(f"✅ Modul erfolgreich registriert!")
        print(f"   Titel: {new_module.title}")
        print(f"   Slug: {new_module.slug}")
        print(f"   Template: {new_module.template_file}")
        print(f"   Subscription: {new_module.subscription_required}")
        print(f"   Sort Order: {new_module.sort_order}")
        print(f"   URL: /dein-trading-stil oder /module/dein-trading-stil")
        
        return new_module

def main():
    print("=" * 70)
    print("📚 Migration: Dein Trading-Stil - Die wichtigste Entscheidung")
    print("=" * 70)
    
    try:
        module = register_module()
        print("\n✅ Migration erfolgreich abgeschlossen!")
        print("\n📌 Hinweis: Vergiss nicht, das Modul über den Admin-Bereich")
        print("   der richtigen Kategorie zuzuordnen, falls gewünscht.")
    except Exception as e:
        print(f"\n❌ Fehler bei der Migration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()

