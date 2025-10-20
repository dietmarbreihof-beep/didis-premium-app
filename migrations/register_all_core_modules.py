#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migration: Registriere alle wichtigen Core-Module
Datum: 2025-10-20
"""

import sys
import os

# Füge Parent-Directory zum Python-Path hinzu
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, LearningModule, ModuleCategory, ModuleSubcategory
from datetime import datetime
import json

def register_all_core_modules():
    """Registriert alle wichtigen Core-Module in der Datenbank"""
    
    with app.app_context():
        print("[INFO] Starte Migration: Alle Core-Module registrieren")
        
        # Definiere alle Core-Module
        core_modules = [
            {
                'title': 'Magic Line Strategie',
                'slug': 'magic-line',
                'description': 'Meistere die Kunst des perfekten Ein- und Ausstiegs mit der Magic Line Strategie',
                'category_name': '1. Trading Strategien',
                'icon': '🎯',
                'template': 'magic_line.html',
                'subscription': ['premium', 'elite', 'masterclass'],
                'duration': 60,
                'difficulty': 'intermediate'
            },
            {
                'title': 'Marktampel & Asset Allokation',
                'slug': 'marktampel-allokation',
                'description': 'Bridgewater-inspirierte Asset Allokation basierend auf Marktregimen',
                'category_name': '1. Trading Strategien',
                'icon': '🚦',
                'template': 'marktampel_allokation.html',
                'subscription': ['premium', 'elite', 'masterclass'],
                'duration': 45,
                'difficulty': 'intermediate'
            },
            {
                'title': 'Defining Trend',
                'slug': 'defining-trend',
                'description': 'Lerne wie du den Trend korrekt identifizierst und mit ihm handelst',
                'category_name': '2. Technische Analyse',
                'icon': '📈',
                'template': 'defining-trend.html',
                'subscription': ['premium', 'elite', 'masterclass'],
                'duration': 40,
                'difficulty': 'beginner'
            },
            {
                'title': 'Volume Analyse Grundlagen',
                'slug': 'volume-analyse-grundlagen',
                'description': 'Verstehe Volumen-Muster: Kapitulation vs Continuation vs Breaking News',
                'category_name': '2. Technische Analyse',
                'icon': '📊',
                'template': 'volume-analyse-grundlagen.html',
                'subscription': ['premium', 'elite', 'masterclass'],
                'duration': 50,
                'difficulty': 'intermediate'
            },
            {
                'title': 'Position Sizing ABCD Calculator',
                'slug': 'position-sizing-abcd',
                'description': 'Trade-Grade basiertes Position Sizing mit interaktivem Calculator',
                'category_name': '3. Risikomanagement',
                'icon': '📏',
                'template': 'position_sizing_abcd_calculator.html',
                'subscription': ['premium', 'elite', 'masterclass'],
                'duration': 35,
                'difficulty': 'intermediate'
            },
            {
                'title': 'Kelly-Kriterium',
                'slug': 'kelly-kriterium',
                'description': 'Optimales Position Sizing nach dem Kelly-Kriterium',
                'category_name': '3. Risikomanagement',
                'icon': '🎲',
                'template': 'Position_Sizing_Kelly.html',
                'subscription': ['elite', 'masterclass'],
                'duration': 40,
                'difficulty': 'advanced'
            },
            {
                'title': 'Trading Playbook System III',
                'slug': 'trading-playbook-system-iii',
                'description': 'Das komplette Trading Playbook - Prozess, Execution, Review',
                'category_name': '5. Trading Psychology',
                'icon': '📖',
                'template': 'trading_playbook_system_iii.html',
                'subscription': ['elite', 'masterclass'],
                'duration': 90,
                'difficulty': 'advanced'
            },
            {
                'title': 'Börsencrash März 2025',
                'slug': 'boersencrash-maerz-2025',
                'description': 'Fallstudie: Wie du Crashs erkennst und tradest',
                'category_name': '1. Trading Strategien',
                'icon': '📉',
                'template': 'boersencrash_maerz_2025.html',
                'subscription': ['premium', 'elite', 'masterclass'],
                'duration': 55,
                'difficulty': 'intermediate'
            },
            {
                'title': 'Bridgewater Quadranten',
                'slug': 'bridgewater-quadranten',
                'description': 'Verstehe die 4 Wirtschaftsregime nach Ray Dalio',
                'category_name': '1. Trading Strategien',
                'icon': '🔷',
                'template': 'bridgewater_quadranten_complete.html',
                'subscription': ['premium', 'elite', 'masterclass'],
                'duration': 50,
                'difficulty': 'intermediate'
            },
            {
                'title': 'Tirone Levels & Quadrant Lines',
                'slug': 'tirone-quadrant-lines',
                'description': 'Professionelle Support/Resistance-Level mit Tirone',
                'category_name': '2. Technische Analyse',
                'icon': '📐',
                'template': 'tirone_quadrant_lines.html',
                'subscription': ['elite', 'masterclass'],
                'duration': 45,
                'difficulty': 'advanced'
            },
            {
                'title': 'Expected Value Calculator',
                'slug': 'expected-value',
                'description': 'Berechne den Expected Value deiner Trading-Strategien',
                'category_name': '3. Risikomanagement',
                'icon': '💰',
                'template': 'expected_value.html',
                'subscription': ['premium', 'elite', 'masterclass'],
                'duration': 30,
                'difficulty': 'beginner'
            },
            {
                'title': 'Daily Report Card',
                'slug': 'daily-report-card',
                'description': 'Dein täglicher Trading-Bericht für konstante Verbesserung',
                'category_name': '5. Trading Psychology',
                'icon': '📝',
                'template': 'daily_report_card_lernseite.html',
                'subscription': ['premium', 'elite', 'masterclass'],
                'duration': 40,
                'difficulty': 'intermediate'
            }
        ]
        
        created_count = 0
        updated_count = 0
        
        for module_data in core_modules:
            try:
                # Prüfe ob Modul existiert
                existing = LearningModule.query.filter_by(slug=module_data['slug']).first()
                
                # Finde oder erstelle Kategorie
                category = ModuleCategory.query.filter(
                    ModuleCategory.name.like(f"%{module_data['category_name'].split('.')[1].strip()}%")
                ).first()
                
                if not category:
                    # Erstelle Kategorie
                    category_order = int(module_data['category_name'].split('.')[0])
                    category = ModuleCategory(
                        name=module_data['category_name'],
                        slug=module_data['category_name'].lower().replace(' ', '-'),
                        icon='folder',
                        description='',
                        sort_order=category_order,
                        is_active=True
                    )
                    db.session.add(category)
                    db.session.flush()
                
                if existing:
                    # Update
                    existing.title = module_data['title']
                    existing.icon = module_data['icon']
                    existing.description = module_data['description']
                    existing.category_id = category.id
                    existing.template_file = module_data['template']
                    existing.required_subscription_levels = json.dumps(module_data['subscription'])
                    existing.estimated_duration = module_data['duration']
                    existing.difficulty_level = module_data['difficulty']
                    existing.is_published = True
                    updated_count += 1
                else:
                    # Create new
                    module = LearningModule(
                        category_id=category.id,
                        title=module_data['title'],
                        slug=module_data['slug'],
                        description=module_data['description'],
                        icon=module_data['icon'],
                        template_file=module_data['template'],
                        content_type='html',
                        is_published=True,
                        is_lead_magnet=False,
                        required_subscription_levels=json.dumps(module_data['subscription']),
                        estimated_duration=module_data['duration'],
                        difficulty_level=module_data['difficulty'],
                        sort_order=100,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    db.session.add(module)
                    created_count += 1
                
            except Exception as e:
                print(f"[ERROR] Fehler bei Modul '{module_data['slug']}': {e}")
                continue
        
        db.session.commit()
        
        print(f"\n[SUCCESS] Core-Module Migration abgeschlossen!")
        print(f"  Erstellt: {created_count}")
        print(f"  Aktualisiert: {updated_count}")
        print(f"  Gesamt: {created_count + updated_count}")
        
        return True

if __name__ == '__main__':
    print("[INFO] Starte Core-Module Migration...")
    success = register_all_core_modules()
    
    if success:
        print("\n[SUCCESS] Migration erfolgreich!")
    else:
        print("\n[ERROR] Migration fehlgeschlagen!")

