#!/usr/bin/env python3
"""
Einfaches Migrations-Script für Didis Streamlit-Module
"""

import json
import sys
import os

# Flask-App importieren
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app, db, LearningModule, ModuleCategory, ModuleSubcategory

def migrate_didis_modules():
    """Migriert alle Didis Streamlit-Module"""
    
    with app.app_context():
        print("🔄 Starte Migration der Didis Streamlit-Module...")
        
        # Module-Daten
        modules_data = [
            {
                "title": "Trading mit Risiko",
                "slug": "trading-mit-risiko",
                "description": "Grundlagen des Risikomanagements im Trading",
                "category": "risikomanagement",
                "content_type": "streamlit",
                "external_url": "http://localhost:8501/(0.0)_💰_Trading_mit_Risiko",
                "required_subscription_levels": [],
                "is_lead_magnet": True,
                "estimated_duration": 45,
                "difficulty_level": "beginner",
                "icon": "💰",
                "sort_order": 1
            },
            {
                "title": "Marktampel & Allokation",
                "slug": "marktampel-allokation",
                "description": "Marktampel-System und Portfolio-Allokation",
                "category": "risikomanagement",
                "content_type": "streamlit",
                "external_url": "http://localhost:8501/(0.1)_Marktampel_Allokation",
                "required_subscription_levels": [],
                "is_lead_magnet": True,
                "estimated_duration": 30,
                "difficulty_level": "beginner",
                "icon": "🚦",
                "sort_order": 2
            },
            {
                "title": "Die 3 Trader-Archetypen",
                "slug": "drei-trader-archetypen",
                "description": "Verstehe die verschiedenen Trader-Typen und finde deinen Stil",
                "category": "trading-psychologie",
                "content_type": "streamlit",
                "external_url": "http://localhost:8501/(0.2)_Die_3_Trader_Archetypen",
                "required_subscription_levels": [],
                "is_lead_magnet": True,
                "estimated_duration": 40,
                "difficulty_level": "beginner",
                "icon": "👥",
                "sort_order": 3
            },
            {
                "title": "Winner identifizieren",
                "slug": "winner-identifizieren",
                "description": "Lerne wie du die besten Aktien für dein Portfolio findest",
                "category": "fundamentalanalyse",
                "content_type": "streamlit",
                "external_url": "http://localhost:8501/(1.0)_📘_Winner_identifizieren",
                "required_subscription_levels": [],
                "is_lead_magnet": True,
                "estimated_duration": 60,
                "difficulty_level": "intermediate",
                "icon": "📘",
                "sort_order": 4
            },
            {
                "title": "Magic Line Strategie",
                "slug": "magic-line-strategie",
                "description": "Die berühmte Magic Line Trading-Strategie",
                "category": "technische-analyse",
                "content_type": "streamlit",
                "external_url": "http://localhost:8501/(2.1.1)_🎯_Magic_Line_Strategie",
                "required_subscription_levels": ["premium", "elite"],
                "is_lead_magnet": False,
                "estimated_duration": 120,
                "difficulty_level": "advanced",
                "icon": "🎯",
                "sort_order": 12
            },
            {
                "title": "AVWAP Grundlagen",
                "slug": "avwap-grundlagen",
                "description": "Teil I: Die Grundlagen von AVWAP (Advanced Volume Weighted Average Price)",
                "category": "technische-analyse",
                "content_type": "streamlit",
                "external_url": "http://localhost:8501/(2.2)_Teil_I_AVWAP_Grundlagen",
                "required_subscription_levels": ["premium", "elite"],
                "is_lead_magnet": False,
                "estimated_duration": 75,
                "difficulty_level": "intermediate",
                "icon": "📊",
                "sort_order": 14
            },
            {
                "title": "AVWAP Anwenden",
                "slug": "avwap-anwenden",
                "description": "Teil II: AVWAP in der Praxis anwenden",
                "category": "technische-analyse",
                "content_type": "streamlit",
                "external_url": "http://localhost:8501/(2.2.1)_Teil_II_AVWAP_Anwenden",
                "required_subscription_levels": ["premium", "elite"],
                "is_lead_magnet": False,
                "estimated_duration": 90,
                "difficulty_level": "intermediate",
                "icon": "📊",
                "sort_order": 15
            },
            {
                "title": "AVWAP Entry & Exit Techniken",
                "slug": "avwap-entry-exit-techniken",
                "description": "Professionelle Entry- und Exit-Strategien mit AVWAP",
                "category": "technische-analyse",
                "content_type": "streamlit",
                "external_url": "http://localhost:8501/(2.2.2)_AVWAP_Entry_Exit_Techniken",
                "required_subscription_levels": ["premium", "elite"],
                "is_lead_magnet": False,
                "estimated_duration": 105,
                "difficulty_level": "advanced",
                "icon": "🎯",
                "sort_order": 16
            },
            {
                "title": "Trading Psychologie",
                "slug": "trading-psychologie",
                "description": "Die psychologischen Aspekte des Tradings",
                "category": "trading-psychologie",
                "content_type": "streamlit",
                "external_url": "http://localhost:8501/(7.0)_🧠_Psychologie",
                "required_subscription_levels": ["premium", "elite"],
                "is_lead_magnet": False,
                "estimated_duration": 75,
                "difficulty_level": "intermediate",
                "icon": "🧠",
                "sort_order": 24
            }
        ]
        
        migrated_count = 0
        errors = []
        
        for module_data in modules_data:
            try:
                # Prüfen ob bereits vorhanden
                existing = LearningModule.query.filter_by(slug=module_data['slug']).first()
                if existing:
                    print(f"⏭️  Modul bereits vorhanden: {module_data['title']}")
                    continue
                
                # Kategorie finden
                category = ModuleCategory.query.filter_by(slug=module_data['category']).first()
                if not category:
                    print(f"❌ Kategorie nicht gefunden: {module_data['category']}")
                    continue
                
                # Neues Modul erstellen
                module = LearningModule(
                    category_id=category.id,
                    title=module_data['title'],
                    slug=module_data['slug'],
                    description=module_data['description'],
                    icon=module_data['icon'],
                    content_type=module_data['content_type'],
                    external_url=module_data['external_url'],
                    is_published=module_data.get('is_published', True),
                    is_lead_magnet=module_data.get('is_lead_magnet', False),
                    required_subscription_levels=module_data.get('required_subscription_levels', ['premium', 'elite']),
                    estimated_duration=module_data.get('estimated_duration', 60),
                    difficulty_level=module_data.get('difficulty_level', 'intermediate'),
                    sort_order=module_data.get('sort_order', 100 + migrated_count)
                )
                
                db.session.add(module)
                db.session.commit()
                
                migrated_count += 1
                print(f"✅ Migriert: {module_data['title']}")
                
            except Exception as e:
                error_msg = f"Fehler bei {module_data['title']}: {str(e)}"
                errors.append(error_msg)
                print(f"❌ {error_msg}")
        
        # Zusammenfassung
        print("\n" + "="*50)
        print("📊 MIGRATIONS-ZUSAMMENFASSUNG")
        print("="*50)
        print(f"✅ Erfolgreich migriert: {migrated_count} Module")
        print(f"❌ Fehler: {len(errors)}")
        
        if errors:
            print("\n🚨 FEHLER:")
            for error in errors:
                print(f"   - {error}")
        
        print("\n🎯 NÄCHSTE SCHRITTE:")
        print("1. Flask-App starten: python app.py")
        print("2. Admin-Panel öffnen: http://localhost:5000/admin/modules")
        print("3. Module überprüfen und anpassen")
        print("4. Streamlit-Apps parallel starten (Port 8501)")

if __name__ == "__main__":
    migrate_didis_modules()
