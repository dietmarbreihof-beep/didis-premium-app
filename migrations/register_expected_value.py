#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Migration Script: Expected Value Modul registrieren
Das fundamentalste Trading-Konzept überhaupt
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, LearningModule, ModuleSubcategory

def register_expected_value_module():
    """Registriert das Expected Value-Modul in der Datenbank"""
    
    with app.app_context():
        try:
            # Finde die Subcategory "Intraday-Setups" oder "Trading-Psychologie"
            subcategory = ModuleSubcategory.query.filter_by(
                slug='intraday-setups'
            ).first()
            
            # Fallback: Trading-Psychologie wäre auch passend
            if not subcategory:
                subcategory = ModuleSubcategory.query.filter_by(
                    slug='trading-psychologie'
                ).first()
            
            # Falls noch immer keine Kategorie gefunden
            if not subcategory:
                print("⚠️ Keine passende Subcategory gefunden. Bitte manuell zuordnen.")
                return False
            
            # Prüfe ob Modul bereits existiert
            existing_module = LearningModule.query.filter_by(
                slug='expected-value'
            ).first()
            
            if existing_module:
                print(f"✅ Modul 'Expected Value' existiert bereits (ID: {existing_module.id})")
                
                # Update falls nötig
                existing_module.title = "Expected Value Mastery"
                existing_module.description = "Das fundamentalste Trading-Konzept. Lerne die EV-Formel, warum EV dynamisch ist (Poker-Analogie) und wie du es in jedem Trade anwendest."
                existing_module.icon = "💰"
                existing_module.content_type = "html"
                existing_module.template_file = "expected-value.html"
                existing_module.is_published = True
                existing_module.is_lead_magnet = False
                existing_module.required_subscription_levels = ['elite', 'elite_pro']
                existing_module.estimated_duration = 55
                existing_module.difficulty_level = "advanced"
                existing_module.sort_order = 27
                
                db.session.commit()
                print("✅ Modul aktualisiert!")
                return True
            
            # Erstelle neues Modul
            new_module = LearningModule(
                category_id=subcategory.category_id,
                subcategory_id=subcategory.id,
                title="Expected Value Mastery",
                slug="expected-value",
                description="Das fundamentalste Trading-Konzept. Lerne die EV-Formel, warum EV dynamisch ist (Poker-Analogie) und wie du es in jedem Trade anwendest.",
                icon="💰",
                content_type="html",
                template_file="expected-value.html",
                is_published=True,
                is_lead_magnet=False,
                required_subscription_levels=['elite', 'elite_pro'],
                estimated_duration=55,  # Minuten
                difficulty_level="advanced",
                sort_order=27
            )
            
            db.session.add(new_module)
            db.session.commit()
            
            print("✅ Expected Value-Modul erfolgreich registriert!")
            print(f"   - ID: {new_module.id}")
            print(f"   - Slug: {new_module.slug}")
            print(f"   - Kategorie: {subcategory.name}")
            print(f"   - Schwierigkeit: {new_module.difficulty_level}")
            print(f"   - Dauer: {new_module.estimated_duration} Min")
            print(f"   - Subscription: {new_module.required_subscription_levels}")
            print(f"   - URL: /module/expected-value")
            
            return True
            
        except Exception as e:
            print(f"❌ Fehler beim Registrieren des Moduls: {str(e)}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    print("=" * 60)
    print("Migration: Expected Value Modul registrieren")
    print("=" * 60)
    
    success = register_expected_value_module()
    
    if success:
        print("\n✅ Migration erfolgreich abgeschlossen!")
        print("\n📚 Nächste Schritte:")
        print("   1. Lokal testen: python app.py")
        print("   2. Route aufrufen: http://localhost:5000/module/expected-value")
        print("   3. EV-Calculator testen!")
        print("   4. Git commit: git add . && git commit -m 'feat: Add Expected Value Mastery module'")
        print("   5. Railway push: git push origin main")
    else:
        print("\n❌ Migration fehlgeschlagen!")
        sys.exit(1)

