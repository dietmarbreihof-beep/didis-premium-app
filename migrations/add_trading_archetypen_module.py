#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migration: Füge Trading-Archetypen Modul hinzu
Datum: 2025-10-25
Beschreibung: Registriert das neue Modul "Trading-Methoden Vertiefung" (Trading-Archetypen)
"""

import sys
import os

# Füge Parent-Directory zum Python-Path hinzu
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, LearningModule, ModuleCategory, ModuleSubcategory
from datetime import datetime
import json

def add_trading_archetypen_module():
    """Fügt das Trading-Archetypen Modul zur Datenbank hinzu"""

    with app.app_context():
        print("[INFO] Starte Migration: Trading-Archetypen Modul")

        # 1. Prüfe ob Modul bereits existiert
        existing = LearningModule.query.filter_by(slug='trading-archetypen').first()
        if existing:
            print(f"[OK] Modul existiert bereits: {existing.title}")
            return True

        # 2. Finde "Trading-Strategien" oder "Technische Analyse" Kategorie
        category = ModuleCategory.query.filter(
            (ModuleCategory.name.like('%Trading-Strateg%')) |
            (ModuleCategory.name.like('%Technische Analyse%')) |
            (ModuleCategory.name.like('%Strategy%'))
        ).first()

        if not category:
            print("[INFO] Kategorie 'Trading-Strategien' nicht gefunden - erstelle neue Kategorie")
            # Erstelle Kategorie falls nicht vorhanden
            category = ModuleCategory(
                name='1. Trading-Strategien',
                slug='trading-strategien',
                icon='🎯',
                description='Grundlegende und fortgeschrittene Trading-Methoden und -Strategien',
                sort_order=1,
                is_active=True
            )
            db.session.add(category)
            db.session.flush()  # Um ID zu erhalten
            print(f"[OK] Kategorie erstellt: {category.name}")
        else:
            print(f"[OK] Kategorie gefunden: {category.name}")

        # 3. Prüfe auf passende Unterkategorie (optional)
        subcategory = None
        if category:
            subcategory = ModuleSubcategory.query.filter(
                ModuleSubcategory.category_id == category.id,
                (ModuleSubcategory.name.like('%Methoden%') |
                 ModuleSubcategory.name.like('%Trading-Styles%'))
            ).first()

        if subcategory:
            print(f"[OK] Unterkategorie gefunden: {subcategory.name}")
        else:
            print("[INFO] Keine Unterkategorie - Modul wird direkt unter Kategorie eingefügt")

        # 4. Erstelle das Trading-Archetypen Modul
        module = LearningModule(
            category_id=category.id,
            subcategory_id=subcategory.id if subcategory else None,
            title='Trading-Methoden Vertiefung',
            slug='trading-archetypen',
            description='Verstehe die drei Säulen erfolgreichen Tradings: Buy & Hold, Position Trading und Swing Trading. Lerne den Keulen-Kombi-Prozess und finde deinen systematischen Edge.',
            icon='🎯',
            template_file='trading_archetypen.html',
            content_type='html',
            is_published=True,
            is_lead_magnet=False,
            required_subscription_levels=json.dumps(["premium", "elite", "masterclass"]),
            estimated_duration=25,  # 20-25 Minuten
            difficulty_level='intermediate',
            sort_order=100,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        db.session.add(module)
        db.session.commit()

        print(f"[SUCCESS] Modul erfolgreich erstellt!")
        print(f"  ID: {module.id}")
        print(f"  Titel: {module.title}")
        print(f"  Slug: {module.slug}")
        print(f"  Kategorie: {category.name}")
        if subcategory:
            print(f"  Unterkategorie: {subcategory.name}")
        print(f"  Template: {module.template_file}")
        print(f"  Schwierigkeitsgrad: {module.difficulty_level}")
        print(f"  Geschätzte Dauer: {module.estimated_duration} Minuten")
        print(f"  Erforderliche Subscription-Level: {module.required_subscription_levels}")

        return True

if __name__ == '__main__':
    try:
        success = add_trading_archetypen_module()
        if success:
            print("\n[OK] Migration erfolgreich abgeschlossen!")
            sys.exit(0)
        else:
            print("\n[ERROR] Migration fehlgeschlagen!")
            sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Migration fehlgeschlagen: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
