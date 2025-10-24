#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migration Script: Registriere 99% Noise vs. 0,1% Edge Modul
Erstellt: 24. Oktober 2025
"""

import sys
import os

# Füge Parent-Directory zum Python-Path hinzu
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, LearningModule, ModuleCategory
from datetime import datetime
import json

def register_noise_vs_edge_module():
    """Registriert das Noise vs. Edge Modul in der Datenbank"""
    
    with app.app_context():
        print("[INFO] Starte Migration: Noise vs. Edge Modul")
        
        try:
            # 1. Prüfe ob Modul bereits existiert
            existing = LearningModule.query.filter_by(slug='noise-vs-edge').first()
            if existing:
                print(f"[INFO] Modul existiert bereits - aktualisiere Einstellungen...")
                
                # Update existing module
                existing.title = '99% Noise vs. 0,1% Edge'
                existing.icon = '🎯'
                existing.is_lead_magnet = True  # Als Lead-Magnet!
                existing.required_subscription_levels = json.dumps([])  # Frei für alle
                existing.description = 'Die Kunst, profitable Setups in einem Ozean von Noise zu identifizieren. Lerne die 0,1% Edge-Charakteristiken aus Lance\'s Trading-System. Warum nur 1-5 Ticker pro Tag echte Edge bieten und wie du sie findest.'
                existing.estimated_duration = 35
                existing.difficulty_level = 'beginner'
                existing.template_file = 'noise-vs-edge.html'
                existing.is_published = True
                
                db.session.commit()
                print(f"[OK] Modul aktualisiert: {existing.title}")
                print(f"  Icon: {existing.icon}")
                print(f"  Lead-Magnet: {existing.is_lead_magnet}")
                print(f"  Template: {existing.template_file}")
                return True
            
            # 2. Finde "Trading-Psychologie" oder "Strategie" Kategorie
            category = ModuleCategory.query.filter(
                ModuleCategory.name.like('%Strategie%') |
                ModuleCategory.name.like('%Psychologie%') |
                ModuleCategory.name.like('%Strategy%')
            ).first()
            
            if not category:
                print("[INFO] Kategorie 'Trading-Strategie' nicht gefunden - erstelle sie...")
                # Erstelle Kategorie falls nicht vorhanden
                category = ModuleCategory(
                    name='1. Trading-Strategie',
                    slug='trading-strategie',
                    icon='chart_with_upwards_trend',
                    description='Setup-Selektion, Timing und Trading-Strategien',
                    sort_order=1,
                    is_active=True
                )
                db.session.add(category)
                db.session.flush()  # Um ID zu erhalten
                print(f"[OK] Kategorie erstellt: {category.name}")
            else:
                print(f"[OK] Kategorie gefunden: {category.name}")
            
            # 3. Erstelle das Noise vs. Edge Modul
            module = LearningModule(
                category_id=category.id,
                subcategory_id=None,  # Keine Unterkategorie
                title='99% Noise vs. 0,1% Edge',
                slug='noise-vs-edge',
                description='Die Kunst, profitable Setups in einem Ozean von Noise zu identifizieren. Lerne die 0,1% Edge-Charakteristiken aus Lance\'s Trading-System. Warum nur 1-5 Ticker pro Tag echte Edge bieten und wie du sie findest.',
                icon='🎯',
                template_file='noise-vs-edge.html',
                content_type='html',
                is_published=True,
                is_lead_magnet=True,  # Als Lead-Magnet - frei für alle!
                required_subscription_levels=json.dumps([]),  # Leer = frei
                sort_order=5,
                estimated_duration=35,  # 35 Minuten geschätzt
                difficulty_level='beginner',  # Für Anfänger geeignet
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            db.session.add(module)
            db.session.commit()
            
            print(f"[SUCCESS] Modul erstellt: {module.title}")
            print(f"  ID: {module.id}")
            print(f"  Slug: {module.slug}")
            print(f"  Kategorie: {category.name}")
            print(f"  Template: {module.template_file}")
            print(f"  Lead-Magnet: {module.is_lead_magnet}")
            print(f"  Duration: {module.estimated_duration} min")
            print(f"  URL: /module/noise-vs-edge")
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Fehler beim Registrieren des Moduls: {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == '__main__':
    print("[INFO] Starte Noise vs. Edge Migration...")
    success = register_noise_vs_edge_module()
    
    if success:
        print("\n[SUCCESS] Migration erfolgreich abgeschlossen!")
        print("[INFO] Das Modul ist jetzt verfuegbar unter: /module/noise-vs-edge")
    else:
        print("\n[ERROR] Migration fehlgeschlagen!")
