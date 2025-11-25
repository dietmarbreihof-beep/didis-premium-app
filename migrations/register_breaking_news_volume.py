#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Migration Script: Breaking News Volume Modul registrieren
Basierend auf professioneller Volume-Analyse-Methode
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, LearningModule, ModuleSubcategory

def register_breaking_news_volume_module():
    """Registriert das Breaking News Volume-Modul in der Datenbank"""
    
    with app.app_context():
        try:
            # Finde die Subcategory "Intraday-Setups" unter System III
            subcategory = ModuleSubcategory.query.filter_by(
                slug='intraday-setups'
            ).first()
            
            # Fallback: Technische Analyse oder Chart-Patterns
            if not subcategory:
                subcategory = ModuleSubcategory.query.filter_by(
                    slug='technische-analyse'
                ).first()
            
            # Falls noch immer keine Kategorie gefunden
            if not subcategory:
                print("⚠️ Keine passende Subcategory gefunden. Bitte manuell zuordnen.")
                return False
            
            # Prüfe ob Modul bereits existiert
            existing_module = LearningModule.query.filter_by(
                slug='breaking-news-volume'
            ).first()
            
            if existing_module:
                print(f"✅ Modul 'Breaking News Volume' existiert bereits (ID: {existing_module.id})")
                
                # Update falls nötig
                existing_module.title = "Breaking News Volume"
                existing_module.description = "Erkenne die besten Headlines durch Volumen-Analyse. Lerne die 3 Faktoren für Volume-Analyse und wie du Monster-Setups in Echtzeit identifizierst."
                existing_module.icon = "📰"
                existing_module.content_type = "html"
                existing_module.template_file = "breaking-news-volume.html"
                existing_module.is_published = True
                existing_module.is_lead_magnet = False
                existing_module.required_subscription_levels = ['elite', 'elite_pro']
                existing_module.estimated_duration = 45
                existing_module.difficulty_level = "advanced"
                existing_module.sort_order = 26
                
                db.session.commit()
                print("✅ Modul aktualisiert!")
                return True
            
            # Erstelle neues Modul
            new_module = LearningModule(
                category_id=subcategory.category_id,
                subcategory_id=subcategory.id,
                title="Breaking News Volume",
                slug="breaking-news-volume",
                description="Erkenne die besten Headlines durch Volumen-Analyse. Lerne die 3 Faktoren für Volume-Analyse und wie du Monster-Setups in Echtzeit identifizierst.",
                icon="📰",
                content_type="html",
                template_file="breaking-news-volume.html",
                is_published=True,
                is_lead_magnet=False,
                required_subscription_levels=['elite', 'elite_pro'],
                estimated_duration=45,  # Minuten
                difficulty_level="advanced",
                sort_order=26
            )
            
            db.session.add(new_module)
            db.session.commit()
            
            print("✅ Breaking News Volume-Modul erfolgreich registriert!")
            print(f"   - ID: {new_module.id}")
            print(f"   - Slug: {new_module.slug}")
            print(f"   - Kategorie: {subcategory.name}")
            print(f"   - Schwierigkeit: {new_module.difficulty_level}")
            print(f"   - Dauer: {new_module.estimated_duration} Min")
            print(f"   - Subscription: {new_module.required_subscription_levels}")
            print(f"   - URL: /module/breaking-news-volume")
            
            return True
            
        except Exception as e:
            print(f"❌ Fehler beim Registrieren des Moduls: {str(e)}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    print("=" * 60)
    print("Migration: Breaking News Volume Modul registrieren")
    print("=" * 60)
    
    success = register_breaking_news_volume_module()
    
    if success:
        print("\n✅ Migration erfolgreich abgeschlossen!")
        print("\n📚 Nächste Schritte:")
        print("   1. Lokal testen: python app.py")
        print("   2. Route aufrufen: http://localhost:5000/module/breaking-news-volume")
        print("   3. Git commit: git add . && git commit -m 'feat: Add Breaking News Volume module'")
        print("   4. Railway push: git push origin main")
    else:
        print("\n❌ Migration fehlgeschlagen!")
        sys.exit(1)




