#!/usr/bin/env python3
"""
Migration Script: Registriere "Wie man Trader wird" Modul
Erstellt: November 2025
Beschreibung: StockBee-basiertes Lernmodul über die fundamentalen Fragen vor dem Trading-Start

Verwendung:
    python migrations/register_wie_man_trader_wird.py

Das Modul wird in der Kategorie "Trading-Psychologie" oder "Grundlagen" registriert.
"""

import sys
import os

# Füge das Projektverzeichnis zum Python-Pfad hinzu
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, ModuleCategory, ModuleSubcategory, LearningModule

def register_module():
    """Registriert das 'Wie man Trader wird' Modul in der Datenbank."""
    
    with app.app_context():
        # Prüfe ob Modul bereits existiert
        existing_module = LearningModule.query.filter_by(slug='wie-man-trader-wird').first()
        
        if existing_module:
            print(f"✅ Modul bereits vorhanden: {existing_module.title}")
            print(f"   Template: {existing_module.template_file}")
            print(f"   Kategorie: {existing_module.subcategory.name if existing_module.subcategory else 'Keine'}")
            return existing_module
        
        # Finde oder erstelle die passende Kategorie
        # Suche nach "Trading-Psychologie" oder "Grundlagen"
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
        
        # Finde oder erstelle Unterkategorie
        subcategory = None
        if category:
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
        
        # Erstelle das Modul
        new_module = LearningModule(
            title='Wie man Trader wird',
            slug='wie-man-trader-wird',
            description='Die fundamentalen Fragen, die du dir stellen musst, BEVOR du mit Trading startest. Basierend auf StockBee-Weisheiten: Ziele, Zeitrahmen, Kapital, Lernkurve.',
            content_type='html',
            template_file='wie-man-trader-wird.html',
            difficulty='Anfänger',
            duration_minutes=45,
            subscription_required='premium',
            subcategory_id=subcategory.id if subcategory else None,
            sort_order=1,
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
        print(f"   URL: /wie-man-trader-wird")
        
        return new_module

def main():
    print("=" * 60)
    print("📚 Migration: Wie man Trader wird - Modul registrieren")
    print("=" * 60)
    
    try:
        module = register_module()
        print("\n✅ Migration erfolgreich abgeschlossen!")
    except Exception as e:
        print(f"\n❌ Fehler bei der Migration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()

