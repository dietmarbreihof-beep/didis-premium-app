#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migration Script: Registriere Risikomanagement-Modul
Erstellt: 19. Oktober 2025
"""

import sys
import os

# Füge Parent-Directory zum Python-Path hinzu
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, LearningModule, ModuleCategory, ModuleSubcategory
from datetime import datetime
import json

def register_risikomanagement_module():
    """Registriert das Risikomanagement-Modul in der Datenbank"""
    
    with app.app_context():
        print("[INFO] Starte Migration: Risikomanagement Modul")
        
        try:
            # 1. Prüfe ob Modul bereits existiert
            existing = LearningModule.query.filter_by(slug='risikomanagement').first()
            if existing:
                print(f"[INFO] Modul existiert bereits - aktualisiere Einstellungen...")
                
                # Update existing module
                existing.title = 'Risikomanagement: Dein Überlebensguide'
                existing.icon = '⚡'  # Blitz-Emoji
                existing.is_lead_magnet = False  # NICHT als Lead-Magnet
                existing.required_subscription_levels = json.dumps(["elite", "masterclass"])
                existing.description = 'Lerne die essenziellen Prinzipien des Risikomanagements für langfristigen Trading-Erfolg. Verstehe Loss Limits, Position Sizing, die brutale Mathematik des Verlierens und die Psychologie des Risikomanagements.'
                existing.estimated_duration = 45
                existing.difficulty_level = 'beginner'
                existing.template_file = 'risikomanagement.html'
                
                db.session.commit()
                print(f"[OK] Modul aktualisiert: {existing.title}")
                print(f"  Icon: {existing.icon}")
                print(f"  Lead-Magnet: {existing.is_lead_magnet}")
                print(f"  Subscription: {existing.required_subscription_levels}")
                return True
            
            # 2. Finde "Risikomanagement" Kategorie
            category = ModuleCategory.query.filter(
                ModuleCategory.name.like('%Risikomanagement%') |
                ModuleCategory.name.like('%Risk Management%')
            ).first()
            
            if not category:
                print("[INFO] Kategorie 'Risikomanagement' nicht gefunden - erstelle sie...")
                # Erstelle Kategorie falls nicht vorhanden
                category = ModuleCategory(
                    name='4. Risikomanagement',
                    slug='risikomanagement',
                    icon='shield',
                    description='Loss Limits, Position Sizing und Risk Management Strategien',
                    sort_order=4,
                    is_active=True
                )
                db.session.add(category)
                db.session.flush()  # Um ID zu erhalten
                print(f"[OK] Kategorie erstellt: {category.name}")
            else:
                print(f"[OK] Kategorie gefunden: {category.name}")
            
            # 3. Keine Unterkategorie - direkt unter Hauptkategorie
            
            # 4. Erstelle das Risikomanagement-Modul
            module = LearningModule(
                category_id=category.id,
                subcategory_id=None,  # Keine Unterkategorie
                title='Risikomanagement: Dein Überlebensguide',
                slug='risikomanagement',
                description='Lerne die essenziellen Prinzipien des Risikomanagements für langfristigen Trading-Erfolg. Verstehe Loss Limits, Position Sizing, die brutale Mathematik des Verlierens und die Psychologie des Risikomanagements.',
                icon='⚡',  # Blitz-Emoji
                template_file='risikomanagement.html',
                content_type='html',
                is_published=True,
                is_lead_magnet=False,  # NICHT als Lead-Magnet - nur fuer Elite
                required_subscription_levels=json.dumps(["elite", "masterclass"]),  # Nur Elite und Masterclass
                sort_order=5,
                estimated_duration=45,  # 45 Minuten geschaetzt
                difficulty_level='beginner',  # Fuer Anfaenger geeignet
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
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Fehler beim Registrieren des Moduls: {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == '__main__':
    print("[INFO] Starte Risikomanagement-Modul Migration...")
    success = register_risikomanagement_module()
    
    if success:
        print("\n[SUCCESS] Migration erfolgreich abgeschlossen!")
        print("[INFO] Das Modul ist jetzt verfuegbar unter: /module/risikomanagement")
    else:
        print("\n[ERROR] Migration fehlgeschlagen!")

