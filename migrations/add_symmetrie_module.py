#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migration: Füge Symmetrie Trading Modul hinzu
Datum: 2025-10-11
"""

import sys
import os

# Füge Parent-Directory zum Python-Path hinzu
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, LearningModule, ModuleCategory, ModuleSubcategory
from datetime import datetime
import json

def add_symmetrie_module():
    """Fügt das Symmetrie Trading Modul zur Datenbank hinzu"""
    
    with app.app_context():
        print("[INFO] Starte Migration: Symmetrie Trading Modul")
        
        # 1. Prüfe ob Modul bereits existiert
        existing = LearningModule.query.filter_by(slug='symmetrie-trading').first()
        if existing:
            print(f"[OK] Modul existiert bereits: {existing.title}")
            return True
        
        # 2. Finde "Technische Analyse" Kategorie
        category = ModuleCategory.query.filter(
            ModuleCategory.name.like('%Technische Analyse%') |
            ModuleCategory.name.like('%Technical Analysis%')
        ).first()
        
        if not category:
            print("[ERROR] Kategorie 'Technische Analyse' nicht gefunden!")
            # Erstelle Kategorie falls nicht vorhanden
            category = ModuleCategory(
                name='2. Technische Analyse',
                slug='technische-analyse',
                icon='📈',
                description='Chartanalyse, Indikatoren und Trading-Tools',
                sort_order=2,
                is_active=True
            )
            db.session.add(category)
            db.session.flush()  # Um ID zu erhalten
            print(f"[OK] Kategorie erstellt: {category.name}")
        else:
            print(f"[OK] Kategorie gefunden: {category.name}")
        
        # 3. Finde "Die Kunst des Verkaufens" Unterkategorie
        subcategory = None
        if category:
            subcategory = ModuleSubcategory.query.filter(
                ModuleSubcategory.category_id == category.id,
                (ModuleSubcategory.name.like('%Verkaufen%') | 
                 ModuleSubcategory.name.like('%Selling%'))
            ).first()
        
        if subcategory:
            print(f"[OK] Unterkategorie gefunden: {subcategory.name}")
        else:
            print("[INFO] Keine Unterkategorie - Modul wird direkt unter Kategorie eingefügt")
        
        # 4. Erstelle das Symmetrie-Modul
        module = LearningModule(
            category_id=category.id,
            subcategory_id=subcategory.id if subcategory else None,
            title='Symmetrie im Trading',
            slug='symmetrie-trading',
            description='Lerne eine der einfachsten und mächtigsten Heuristiken zur Vorhersage von Kursbewegungen - mit praktischem QBTS-Beispiel.',
            icon='🔄',
            template_file='symmetrie-trading.html',
            content_type='html',
            is_published=True,
            is_lead_magnet=False,
            required_subscription_levels=json.dumps(["free"]),
            sort_order=200,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.session.add(module)
        db.session.commit()
        
        print(f"[SUCCESS] Modul erstellt: {module.title}")
        print(f"  ID: {module.id}")
        print(f"  Slug: {module.slug}")
        print(f"  Kategorie: {category.name}")
        if subcategory:
            print(f"  Unterkategorie: {subcategory.name}")
        print(f"  Template: {module.template_file}")
        
        return True

if __name__ == '__main__':
    try:
        success = add_symmetrie_module()
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




