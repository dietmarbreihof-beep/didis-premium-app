"""
Migration: Registriere "S-Kurven & Unternehmenslebenszyklus" Modul
Erstellt: 29. Dezember 2025
Beschreibung: Alex Sacerdotes S-Kurven-Investitionsmodell kombiniert mit Damodarans Corporate Lifecycle
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, ModuleCategory, ModuleSubcategory, LearningModule

def register_module():
    """Registriert das S-Kurven & Lifecycle Modul in der Datenbank"""
    
    with app.app_context():
        # Prüfe ob Modul bereits existiert
        existing = LearningModule.query.filter_by(slug='s-kurven-lifecycle').first()
        if existing:
            print(f"✅ Modul 's-kurven-lifecycle' existiert bereits (ID: {existing.id})")
            return
        
        # Finde oder erstelle die Kategorie "Fundamentalanalyse"
        category = ModuleCategory.query.filter_by(slug='fundamentalanalyse').first()
        if not category:
            # Erstelle Kategorie falls nicht vorhanden
            category = ModuleCategory(
                name='Fundamentalanalyse',
                slug='fundamentalanalyse',
                description='Bewertung von Unternehmen und Märkten',
                icon='📊',
                sort_order=6
            )
            db.session.add(category)
            db.session.commit()
            print(f"✅ Kategorie 'Fundamentalanalyse' erstellt (ID: {category.id})")
        
        # Finde oder erstelle die Unterkategorie "Bewertungsmodelle"
        subcategory = ModuleSubcategory.query.filter_by(slug='bewertungsmodelle').first()
        if not subcategory:
            subcategory = ModuleSubcategory(
                name='Bewertungsmodelle',
                slug='bewertungsmodelle',
                description='Professionelle Modelle zur Unternehmensbewertung und Investment-Timing',
                category_id=category.id,
                sort_order=1
            )
            db.session.add(subcategory)
            db.session.commit()
            print(f"✅ Unterkategorie 'Bewertungsmodelle' erstellt (ID: {subcategory.id})")
        
        # Erstelle das neue Modul
        new_module = LearningModule(
            title='S-Kurven & Unternehmenslebenszyklus',
            slug='s-kurven-lifecycle',
            description='Meistere das Investment-Timing: Alex Sacerdotes S-Kurven-Philosophie kombiniert mit Prof. Damodarans Corporate Lifecycle Theorie. Lerne den optimalen Einstiegszeitpunkt zu erkennen.',
            content='S-Kurven-Investitionsmodell von Alex Sacerdote (Whale Rock Capital) und Aswath Damodarans Corporate Lifecycle: Die Konvergenz von Wachstumstheorie und fundamentaler Bewertung für überlegene Investmententscheidungen.',
            template_file='s-kurven-lifecycle.html',
            subcategory_id=subcategory.id,
            difficulty='Fortgeschritten',
            estimated_time=60,
            is_published=True,
            is_premium=True,
            required_subscription='premium',
            sort_order=1
        )
        
        db.session.add(new_module)
        db.session.commit()
        
        print(f"✅ Modul 'S-Kurven & Unternehmenslebenszyklus' erfolgreich registriert!")
        print(f"   - ID: {new_module.id}")
        print(f"   - Slug: {new_module.slug}")
        print(f"   - Kategorie: {category.name}")
        print(f"   - Unterkategorie: {subcategory.name}")
        print(f"   - Template: {new_module.template_file}")
        print(f"   - Premium: Ja (ab Premium)")
        print(f"   - Route: /s-kurven-lifecycle")
        print(f"")
        print(f"📚 Kernthemen:")
        print(f"   • S-Kurve der Technologie-Adoption (Alex Sacerdote, Whale Rock Capital)")
        print(f"   • Corporate Lifecycle (Prof. Aswath Damodaran, NYU Stern)")
        print(f"   • Inflektionspunkt = Sweet Spot für Investment")
        print(f"   • Die 6 Lebenszyklus-Phasen von Unternehmen")
        print(f"   • Synthese: Zwei Modelle, ein optimaler Einstiegszeitpunkt")
        print(f"   • Investment-Checkliste für den Sweet Spot")

if __name__ == '__main__':
    register_module()

