"""
Migration: Registriere "Deine Trader-Reise" Modul
Erstellt: 15. Dezember 2025
Beschreibung: Die 4 Stufen zum profitablen Trading - Von Stage 1 bis Stage 4
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, ModuleCategory, ModuleSubcategory, LearningModule

def register_module():
    """Registriert das Traders Journey Modul in der Datenbank"""
    
    with app.app_context():
        # Prüfe ob Modul bereits existiert
        existing = LearningModule.query.filter_by(slug='traders-journey').first()
        if existing:
            print(f"✅ Modul 'traders-journey' existiert bereits (ID: {existing.id})")
            return
        
        # Finde oder erstelle die Kategorie "Trading-Psychologie"
        category = ModuleCategory.query.filter_by(slug='trading-psychologie').first()
        if not category:
            # Erstelle Kategorie falls nicht vorhanden
            category = ModuleCategory(
                name='Trading-Psychologie',
                slug='trading-psychologie',
                description='Psychologische Aspekte des Tradings',
                icon='🧠',
                sort_order=5
            )
            db.session.add(category)
            db.session.commit()
            print(f"✅ Kategorie 'Trading-Psychologie' erstellt (ID: {category.id})")
        
        # Finde oder erstelle die Unterkategorie "Trader-Entwicklung"
        subcategory = ModuleSubcategory.query.filter_by(slug='trader-entwicklung').first()
        if not subcategory:
            subcategory = ModuleSubcategory(
                name='Trader-Entwicklung',
                slug='trader-entwicklung',
                description='Die Reise vom Anfänger zum profitablen Trader',
                category_id=category.id,
                sort_order=1
            )
            db.session.add(subcategory)
            db.session.commit()
            print(f"✅ Unterkategorie 'Trader-Entwicklung' erstellt (ID: {subcategory.id})")
        
        # Erstelle das neue Modul
        new_module = LearningModule(
            title='Deine Trader-Reise',
            slug='traders-journey',
            description='Die 4 Stufen zum profitablen Trading: Von der Unprofitable Phase über Boom-and-Bust zur Consistency und Performance Phase. Lerne, wo du stehst und wie du aufsteigst.',
            content='Die Evolution eines profitablen Traders mit Equity-Kurven-Analyse',
            template_file='traders-journey.html',
            subcategory_id=subcategory.id,
            difficulty='Anfänger',
            estimated_time=45,
            is_published=True,
            is_premium=True,
            required_subscription='premium',
            sort_order=1
        )
        
        db.session.add(new_module)
        db.session.commit()
        
        print(f"✅ Modul 'Deine Trader-Reise' erfolgreich registriert!")
        print(f"   - ID: {new_module.id}")
        print(f"   - Slug: {new_module.slug}")
        print(f"   - Kategorie: {category.name}")
        print(f"   - Unterkategorie: {subcategory.name}")
        print(f"   - Template: {new_module.template_file}")
        print(f"   - Premium: Ja (ab Premium)")
        print(f"   - Route: /traders-journey")

if __name__ == '__main__':
    register_module()
