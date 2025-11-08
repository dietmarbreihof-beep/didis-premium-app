#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migration Script: Registriere Position-Vergrößern-Modul
Erstellt: Oktober 2025
"""

import sys
import os

# Füge Parent-Directory zum Python-Path hinzu
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, LearningModule, ModuleCategory, ModuleSubcategory
from datetime import datetime
import json

def register_position_vergroessern_module():
    """Registriert das Position-Vergrößern-Modul in der Datenbank"""
    
    with app.app_context():
        print("[INFO] Starte Migration: Position vergrößern Modul")
        
        try:
            # 1. Prüfe ob Modul bereits existiert
            existing = LearningModule.query.filter_by(slug='position-vergroessern').first()
            if existing:
                print(f"[INFO] Modul existiert bereits - aktualisiere Einstellungen...")
                
                # Update existing module
                existing.title = 'Position vergrößern: Die Expected-Value-Methode'
                existing.icon = '📊'
                existing.is_lead_magnet = False
                existing.required_subscription_levels = json.dumps(["premium", "elite", "masterclass"])
                existing.description = 'Lerne professionelles Aufstocken von Positionen basierend auf Expected Value, nicht auf Emotionen. Lance\'s bewährte Methode für mathematisch fundierte Trades.'
                existing.estimated_duration = 35
                existing.difficulty_level = 'intermediate'
                existing.template_file = 'position-vergroessern.html'
                
                db.session.commit()
                print(f"[OK] Modul aktualisiert: {existing.title}")
                print(f"  Icon: {existing.icon}")
                print(f"  Lead-Magnet: {existing.is_lead_magnet}")
                print(f"  Subscription: {existing.required_subscription_levels}")
                return True
            
            # 2. Finde "Risikomanagement" oder "Trading Strategien" Kategorie
            category = ModuleCategory.query.filter(
                ModuleCategory.name.like('%Risikomanagement%') |
                ModuleCategory.name.like('%Trading Strategien%')
            ).first()
            
            if not category:
                print("[INFO] Kategorie nicht gefunden - suche alternative Kategorie...")
                # Versuche "Advanced" oder "Strategie" Kategorie
                category = ModuleCategory.query.filter(
                    ModuleCategory.name.like('%Advanced%') |
                    ModuleCategory.name.like('%Strategie%')
                ).first()
            
            if not category:
                print("[INFO] Keine passende Kategorie gefunden - erstelle 'Trading Konzepte'...")
                # Erstelle Kategorie falls nicht vorhanden
                category = ModuleCategory(
                    name='3. Trading Konzepte',
                    slug='trading-konzepte',
                    icon='lightbulb',
                    description='Expected Value, Position Sizing und professionelle Trading-Methoden',
                    sort_order=3,
                    is_active=True
                )
                db.session.add(category)
                db.session.flush()  # Um ID zu erhalten
                print(f"[OK] Kategorie erstellt: {category.name}")
            else:
                print(f"[OK] Kategorie gefunden: {category.name}")
            
            # 3. Keine Unterkategorie - direkt unter Hauptkategorie
            
            # 4. Erstelle das Position-Vergrößern-Modul
            module = LearningModule(
                category_id=category.id,
                subcategory_id=None,  # Keine Unterkategorie
                title='Position vergrößern: Die Expected-Value-Methode',
                slug='position-vergroessern',
                description='Lerne professionelles Aufstocken von Positionen basierend auf Expected Value, nicht auf Emotionen. Lance\'s bewährte Methode zeigt dir, wann Aufstockungen mathematisch sinnvoll sind und wann sie dein Kapital gefährden. Mit interaktiven Szenarien und Datenanalyse-Tools.',
                icon='📊',
                template_file='position-vergroessern.html',
                content_type='html',
                is_published=True,
                is_lead_magnet=False,
                required_subscription_levels=json.dumps(["premium", "elite", "masterclass"]),
                sort_order=10,
                estimated_duration=35,  # 35 Minuten geschätzt
                difficulty_level='intermediate',  # Für fortgeschrittene Anfänger
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
            print(f"  Difficulty: {module.difficulty_level}")
            print(f"  Subscription Levels: {module.required_subscription_levels}")
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Fehler beim Registrieren des Moduls: {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == '__main__':
    print("[INFO] Starte Position-Vergrößern-Modul Migration...")
    success = register_position_vergroessern_module()
    
    if success:
        print("\n[SUCCESS] Migration erfolgreich abgeschlossen!")
        print("[INFO] Das Modul ist jetzt verfügbar unter:")
        print("  - /position-vergroessern (Direkte Route)")
        print("  - /module/position-vergroessern (Über Modul-System)")
    else:
        print("\n[ERROR] Migration fehlgeschlagen!")


