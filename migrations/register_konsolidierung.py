#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Migration Script: Konsolidierung Modul registrieren
Basierend auf Lance Beggs' Kurs-Material aus System III
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, LearningModule, ModuleSubcategory

def register_konsolidierung_module():
    """Registriert das Konsolidierungs-Modul in der Datenbank"""
    
    with app.app_context():
        try:
            # Finde die Subcategory "Intraday-Setups" unter System III
            # Alternativ: Erstelle eine neue Subcategory oder verwende eine bestehende
            subcategory = ModuleSubcategory.query.filter_by(
                slug='intraday-setups'
            ).first()
            
            # Fallback: Wenn Intraday-Setups nicht existiert, verwende Chart-Patterns
            if not subcategory:
                subcategory = ModuleSubcategory.query.filter_by(
                    slug='chart-patterns'
                ).first()
            
            # Falls noch immer keine Kategorie gefunden, erstelle eine
            if not subcategory:
                print("⚠️ Keine passende Subcategory gefunden. Bitte manuell zuordnen.")
                return False
            
            # Prüfe ob Modul bereits existiert
            existing_module = LearningModule.query.filter_by(
                slug='konsolidierung'
            ).first()
            
            if existing_module:
                print(f"✅ Modul 'Konsolidierung' existiert bereits (ID: {existing_module.id})")
                
                # Update falls nötig
                existing_module.title = "Konsolidierung Meistern"
                existing_module.description = "Verstehe Price Action & Price Acceptance wie ein Profi. Lance's Kernprinzip: Mit richtiger Konsolidierung können Trends unendlich weitergehen."
                existing_module.icon = "📊"
                existing_module.content_type = "html"
                existing_module.template_file = "konsolidierung.html"
                existing_module.is_published = True
                existing_module.is_lead_magnet = False
                existing_module.required_subscription_levels = ['elite', 'elite_pro']
                existing_module.estimated_duration = 50
                existing_module.difficulty_level = "advanced"
                existing_module.sort_order = 25
                
                db.session.commit()
                print("✅ Modul aktualisiert!")
                return True
            
            # Erstelle neues Modul
            new_module = LearningModule(
                category_id=subcategory.category_id,  # Wichtig: category_id von subcategory ableiten
                subcategory_id=subcategory.id,
                title="Konsolidierung Meistern",
                slug="konsolidierung",
                description="Verstehe Price Action & Price Acceptance wie ein Profi. Lance's Kernprinzip: Mit richtiger Konsolidierung können Trends unendlich weitergehen.",
                icon="📊",
                content_type="html",
                template_file="konsolidierung.html",
                is_published=True,
                is_lead_magnet=False,
                required_subscription_levels=['elite', 'elite_pro'],
                estimated_duration=50,  # Minuten
                difficulty_level="advanced",
                sort_order=25
            )
            
            db.session.add(new_module)
            db.session.commit()
            
            print("✅ Konsolidierungs-Modul erfolgreich registriert!")
            print(f"   - ID: {new_module.id}")
            print(f"   - Slug: {new_module.slug}")
            print(f"   - Kategorie: {subcategory.name}")
            print(f"   - Schwierigkeit: {new_module.difficulty_level}")
            print(f"   - Dauer: {new_module.estimated_duration} Min")
            print(f"   - Subscription: {new_module.required_subscription_levels}")
            print(f"   - URL: /module/konsolidierung")
            
            return True
            
        except Exception as e:
            print(f"❌ Fehler beim Registrieren des Moduls: {str(e)}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    print("=" * 60)
    print("Migration: Konsolidierung Modul registrieren")
    print("=" * 60)
    
    success = register_konsolidierung_module()
    
    if success:
        print("\n✅ Migration erfolgreich abgeschlossen!")
        print("\n📚 Nächste Schritte:")
        print("   1. Screenshots kopieren: cp 'Lance Kurs für System III/Consolidation/*.png' static/screenshots/")
        print("   2. Lokal testen: python app.py")
        print("   3. Route aufrufen: http://localhost:5000/module/konsolidierung")
        print("   4. Git commit: git add . && git commit -m 'feat: Add Konsolidierung module'")
        print("   5. Railway push: git push origin main")
    else:
        print("\n❌ Migration fehlgeschlagen!")
        sys.exit(1)

