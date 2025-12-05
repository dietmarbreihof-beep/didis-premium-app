#!/usr/bin/env python3
"""
Migration Script: Registriere "Einfluss der persönlichen Beziehung zum Geld" Modul
Erstellt: November 2025
Beschreibung: Trading-Psychologie Modul basierend auf Dr. Jonathan Katz & Lance Breitstein

Verwendung:
    python migrations/register_einfluss_geld_beziehung.py

Das Modul wird in der Kategorie "Trading-Psychologie" registriert.
"""

import sys
import os

# Füge das Projektverzeichnis zum Python-Pfad hinzu
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, ModuleCategory, ModuleSubcategory, LearningModule

def register_module():
    """Registriert das 'Einfluss der persönlichen Beziehung zum Geld' Modul in der Datenbank."""
    
    with app.app_context():
        # Prüfe ob Modul bereits existiert
        existing_module = LearningModule.query.filter_by(slug='einfluss-geld-beziehung').first()
        
        if existing_module:
            print(f"✅ Modul bereits vorhanden: {existing_module.title}")
            print(f"   Template: {existing_module.template_file}")
            print(f"   Kategorie: {existing_module.subcategory.name if existing_module.subcategory else 'Keine'}")
            return existing_module
        
        # Finde oder erstelle die passende Kategorie
        # Suche nach "Trading-Psychologie" oder "Psychologie"
        category = ModuleCategory.query.filter(
            ModuleCategory.name.ilike('%psychologie%')
        ).first()
        
        if not category:
            category = ModuleCategory.query.filter(
                ModuleCategory.slug.ilike('%psychologie%')
            ).first()
        
        if not category:
            # Erstelle neue Kategorie wenn keine passende gefunden
            category = ModuleCategory.query.filter_by(slug='neue-module').first()
            if not category:
                category = ModuleCategory(
                    name='🆕 Neue Module',
                    slug='neue-module',
                    description='Neu hinzugefügte Module zur Kategorisierung',
                    sort_order=999
                )
                db.session.add(category)
                db.session.flush()
                print(f"📁 Kategorie erstellt: {category.name}")
        
        # Finde oder erstelle Unterkategorie
        subcategory = None
        if category:
            # Suche nach bestehender Unterkategorie "Grundlagen" oder "Psychologie"
            subcategory = ModuleSubcategory.query.filter(
                ModuleSubcategory.category_id == category.id,
                ModuleSubcategory.name.ilike('%grundlagen%')
            ).first()
            
            if not subcategory:
                subcategory = ModuleSubcategory.query.filter(
                    ModuleSubcategory.category_id == category.id,
                    ModuleSubcategory.name.ilike('%psychologie%')
                ).first()
            
            if not subcategory:
                # Erstelle neue Unterkategorie
                subcategory = ModuleSubcategory(
                    name='Trading-Psychologie',
                    slug='trading-psychologie',
                    category_id=category.id,
                    description='Psychologische Aspekte des Tradings',
                    sort_order=1
                )
                db.session.add(subcategory)
                db.session.flush()
                print(f"📂 Unterkategorie erstellt: {subcategory.name}")
        
        # Erstelle das Modul
        new_module = LearningModule(
            category_id=category.id,
            title='Einfluss der persönlichen Beziehung zum Geld',
            slug='einfluss-geld-beziehung',
            description='Wie deine Kindheit und deine Erfahrungen dein Trading-Verhalten prägen. Mit Dr. Jonathan Katz & Lance Breitstein. Lerne, wie deine Beziehung zu Geld deine Risikotoleranz, dein Overtrading und dein FOMO beeinflusst.',
            content_type='html',
            template_file='einfluss-geld-beziehung.html',
            icon='🧠',
            difficulty='Anfänger',
            duration_minutes=50,
            subscription_required='premium',
            subcategory_id=subcategory.id if subcategory else None,
            sort_order=10,
            is_published=True,
            view_count=0
        )
        
        db.session.add(new_module)
        db.session.commit()
        
        print(f"✅ Modul erfolgreich registriert!")
        print(f"   Titel: {new_module.title}")
        print(f"   Slug: {new_module.slug}")
        print(f"   Template: {new_module.template_file}")
        print(f"   Subscription: {new_module.subscription_required}")
        print(f"   URL: /einfluss-geld-beziehung")
        
        return new_module

def main():
    print("=" * 60)
    print("📚 Migration: Einfluss der persönlichen Beziehung zum Geld")
    print("=" * 60)
    
    try:
        module = register_module()
        print("\n✅ Migration erfolgreich abgeschlossen!")
    except Exception as e:
        print(f"\n❌ Fehler bei der Migration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()



