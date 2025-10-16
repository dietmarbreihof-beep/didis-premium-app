#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Initialisiere das Volumen-Analyse Modul in der Datenbank
Wird beim Railway Deployment automatisch ausgeführt
"""

from app import app, db
from app import ModuleCategory, ModuleSubcategory, LearningModule
from datetime import datetime
import sqlite3

def init_volume_module():
    """Initialisiere Volumen-Analyse Modul"""
    with app.app_context():
        try:
            # 1. Prüfe/Repariere Schema
            conn = sqlite3.connect('didis_academy.db')
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(module_subcategories)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'description' not in columns:
                cursor.execute("ALTER TABLE module_subcategories ADD COLUMN description TEXT")
                conn.commit()
            conn.close()
            
            # 2. Finde/Erstelle Kategorie
            tech_category = ModuleCategory.query.filter(
                ModuleCategory.name.like("%Technische%")
            ).first()
            
            if not tech_category:
                tech_category = ModuleCategory(
                    name="2. Technische Analyse",
                    slug="technische-analyse",
                    icon="📊",
                    description="Chartanalyse, Indikatoren und technische Handelsstrategien",
                    sort_order=2,
                    is_active=True
                )
                db.session.add(tech_category)
                db.session.commit()
            
            # 3. Finde/Erstelle Unterkategorie
            indicators_sub = ModuleSubcategory.query.filter_by(
                category_id=tech_category.id
            ).filter(ModuleSubcategory.name.like("%Indikator%")).first()
            
            if not indicators_sub:
                max_order = db.session.query(db.func.max(ModuleSubcategory.sort_order))\
                    .filter_by(category_id=tech_category.id).scalar() or 0
                
                indicators_sub = ModuleSubcategory(
                    category_id=tech_category.id,
                    name="2.2 Indikatoren",
                    slug="indikatoren",
                    icon="📈",
                    sort_order=max_order + 1,
                    is_active=True
                )
                db.session.add(indicators_sub)
                db.session.commit()
            
            # 4. Erstelle/Aktualisiere Modul
            existing = LearningModule.query.filter_by(slug="volume-analyse-grundlagen").first()
            
            if existing:
                # Aktualisiere wenn schon vorhanden
                existing.category_id = tech_category.id
                existing.subcategory_id = indicators_sub.id
                existing.title = "Volumen-Analyse Grundlagen"
                existing.description = "Lerne die wichtigste Trading-Variable nach Preis und Zeit. Mit Breaking News, Continuation Plays und Kapitulation."
                existing.icon = "📊"
                existing.template_file = "volume-analyse-grundlagen.html"
                existing.content_type = "html"
                existing.is_published = True
                existing.is_lead_magnet = False
                existing.estimated_duration = 45
                existing.difficulty_level = "beginner"
                existing.updated_at = datetime.utcnow()
            else:
                # Neu erstellen
                max_order = db.session.query(db.func.max(LearningModule.sort_order))\
                    .filter_by(subcategory_id=indicators_sub.id).scalar() or 0
                
                volume_module = LearningModule(
                    category_id=tech_category.id,
                    subcategory_id=indicators_sub.id,
                    title="Volumen-Analyse Grundlagen",
                    slug="volume-analyse-grundlagen",
                    description="Lerne die wichtigste Trading-Variable nach Preis und Zeit. Mit Breaking News, Continuation Plays und Kapitulation.",
                    icon="📊",
                    template_file="volume-analyse-grundlagen.html",
                    content_type="html",
                    is_published=True,
                    is_lead_magnet=False,
                    required_subscription_levels=[],
                    sort_order=max_order + 1,
                    estimated_duration=45,
                    difficulty_level="beginner",
                    view_count=0
                )
                db.session.add(volume_module)
            
            db.session.commit()
            return True
            
        except Exception as e:
            print(f"Error initializing volume module: {e}")
            return False

if __name__ == "__main__":
    print("Initializing Volume Analysis Module...")
    if init_volume_module():
        print("✓ Success!")
    else:
        print("✗ Failed!")




