#!/usr/bin/env python3
"""
Migration Script: Registriere "Wie man Trader wird - Teil 3" Modul
====================================================================

Dieses Script registriert das neue Lernmodul in der Datenbank.

Verwendung:
    python migrations/register_wie_man_trader_wird_3.py

Das Modul wird in der Kategorie "Trading-Psychologie" → "Grundlagen" eingefügt,
als Fortsetzung von Teil 1 und Teil 2.
"""

import sys
import os

# Füge das Hauptverzeichnis zum Python-Pfad hinzu
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, LearningModule, ModuleCategory, ModuleSubcategory

def register_module():
    """Registriere das Modul 'Wie man Trader wird - Teil 3' in der Datenbank."""
    
    with app.app_context():
        # Prüfe ob das Modul bereits existiert
        existing_module = LearningModule.query.filter_by(slug='wie-man-trader-wird-3').first()
        
        if existing_module:
            print("✅ Modul 'wie-man-trader-wird-3' existiert bereits.")
            print(f"   ID: {existing_module.id}")
            print(f"   Titel: {existing_module.title}")
            print(f"   Template: {existing_module.template_file}")
            return existing_module
        
        # Finde die passende Kategorie und Unterkategorie
        # Suche nach "Trading-Psychologie" oder "Grundlagen"
        category = None
        subcategory = None
        
        # Versuche zuerst "Trading-Psychologie" zu finden
        category = ModuleCategory.query.filter(
            ModuleCategory.name.ilike('%psychologie%')
        ).first()
        
        if not category:
            # Fallback: Suche nach "Grundlagen"
            category = ModuleCategory.query.filter(
                ModuleCategory.name.ilike('%grundlagen%')
            ).first()
        
        if not category:
            # Letzer Fallback: Nehme die erste Kategorie oder erstelle "Trading-Psychologie"
            category = ModuleCategory.query.first()
            if not category:
                category = ModuleCategory(
                    name="Trading-Psychologie",
                    slug="trading-psychologie",
                    description="Psychologische Aspekte des Tradings",
                    sort_order=10
                )
                db.session.add(category)
                db.session.flush()
                print(f"📁 Neue Kategorie erstellt: {category.name}")
        
        # Suche nach Unterkategorie "Grundlagen"
        if category:
            subcategory = ModuleSubcategory.query.filter(
                ModuleSubcategory.category_id == category.id,
                ModuleSubcategory.name.ilike('%grundlagen%')
            ).first()
            
            if not subcategory:
                # Erstelle Unterkategorie "Grundlagen"
                subcategory = ModuleSubcategory(
                    name="Grundlagen",
                    slug="grundlagen",
                    category_id=category.id,
                    description="Grundlegende Konzepte für angehende Trader",
                    sort_order=1
                )
                db.session.add(subcategory)
                db.session.flush()
                print(f"📂 Neue Unterkategorie erstellt: {subcategory.name}")
        
        # Finde die höchste sort_order in dieser Unterkategorie
        max_sort = db.session.query(db.func.max(LearningModule.sort_order)).filter(
            LearningModule.subcategory_id == (subcategory.id if subcategory else None)
        ).scalar() or 0
        
        # Erstelle das neue Modul
        new_module = LearningModule(
            title="Wie man Trader wird - Teil 3: Setups & Expertise",
            slug="wie-man-trader-wird-3",
            description="Wie du die richtigen Setups für deinen Zeitrahmen findest – und warum alle erfolgreichen Trader im Grunde dasselbe machen. Der dritte und letzte Teil der Serie.",
            category_id=category.id if category else None,
            subcategory_id=subcategory.id if subcategory else None,
            template_file="wie-man-trader-wird-3.html",
            difficulty_level="Anfänger",
            estimated_duration=40,  # 40 Minuten
            is_published=True,
            is_lead_magnet=False,  # Premium-Modul
            required_subscription_levels=["premium", "elite", "elite_pro", "masterclass"],
            sort_order=max_sort + 1
        )
        
        db.session.add(new_module)
        db.session.commit()
        
        print("=" * 60)
        print("✅ MODUL ERFOLGREICH REGISTRIERT!")
        print("=" * 60)
        print(f"   ID: {new_module.id}")
        print(f"   Titel: {new_module.title}")
        print(f"   Slug: {new_module.slug}")
        print(f"   Template: {new_module.template_file}")
        print(f"   Kategorie: {category.name if category else 'Keine'}")
        print(f"   Unterkategorie: {subcategory.name if subcategory else 'Keine'}")
        print(f"   Schwierigkeit: {new_module.difficulty_level}")
        print(f"   Dauer: {new_module.estimated_duration} Minuten")
        print(f"   Premium: Ja (Premium, Elite, Elite Pro, Masterclass)")
        print("=" * 60)
        print(f"\n🌐 URL: /wie-man-trader-wird-3")
        print(f"📚 Modul-URL: /module/wie-man-trader-wird-3")
        
        return new_module


def verify_series():
    """Überprüfe, ob alle drei Teile der Serie registriert sind."""
    
    with app.app_context():
        print("\n" + "=" * 60)
        print("📚 SERIE 'WIE MAN TRADER WIRD' - ÜBERSICHT")
        print("=" * 60)
        
        parts = [
            ('wie-man-trader-wird', 'Teil 1: Die fundamentalen Fragen'),
            ('dein-trading-stil', 'Teil 2: Dein Trading-Stil'),
            ('wie-man-trader-wird-3', 'Teil 3: Setups & Expertise')
        ]
        
        for slug, description in parts:
            module = LearningModule.query.filter_by(slug=slug).first()
            if module:
                status = "✅"
                info = f"ID: {module.id}, Published: {module.is_published}"
            else:
                status = "❌"
                info = "Nicht registriert"
            
            print(f"{status} {description}")
            print(f"   Slug: {slug}")
            print(f"   {info}")
            print()


if __name__ == '__main__':
    print("\n🚀 Starte Migration: Wie man Trader wird - Teil 3\n")
    
    try:
        register_module()
        verify_series()
        print("\n✅ Migration erfolgreich abgeschlossen!")
    except Exception as e:
        print(f"\n❌ Fehler bei der Migration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

