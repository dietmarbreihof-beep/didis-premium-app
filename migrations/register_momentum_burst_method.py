"""
Migration Script: Momentum Burst Method Modul
Registriert das Momentum Burst Method Modul in der Datenbank
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, LearningModule, ModuleCategory, ModuleSubcategory
from datetime import datetime

def register_momentum_burst_method():
    """Registriert das Momentum Burst Method Modul"""
    
    with app.app_context():
        try:
            # Prüfe ob Modul bereits existiert
            existing = LearningModule.query.filter_by(slug='momentum-burst-method').first()
            if existing:
                print("[OK] Momentum Burst Method Modul existiert bereits")
                print(f"  - ID: {existing.id}")
                print(f"  - Kategorie: {existing.category.name if existing.category else 'N/A'}")
                print(f"  - Published: {existing.is_published}")
                return existing
            
            # Finde oder erstelle Hauptkategorie "Trading-Methoden"
            main_category = ModuleCategory.query.filter_by(slug='trading-methoden').first()
            if not main_category:
                main_category = ModuleCategory(
                    name='Trading-Methoden',
                    slug='trading-methoden',
                    description='Bewaehrte Trading-Strategien und Setups',
                    icon='TARGET',
                    sort_order=5
                )
                db.session.add(main_category)
                db.session.flush()
                print("[OK] Hauptkategorie 'Trading-Methoden' erstellt")
            
            # Finde oder erstelle Unterkategorie "Momentum Trading"
            subcategory = ModuleSubcategory.query.filter_by(
                category_id=main_category.id,
                slug='momentum-trading'
            ).first()
            
            if not subcategory:
                subcategory = ModuleSubcategory(
                    category_id=main_category.id,
                    name='Momentum Trading',
                    slug='momentum-trading',
                    description='Momentum Burst, Breakout-Strategien, Range Expansion',
                    icon='ROCKET',
                    sort_order=1
                )
                db.session.add(subcategory)
                db.session.flush()
                print("[OK] Unterkategorie 'Momentum Trading' erstellt")
            
            # Erstelle das Modul
            module = LearningModule(
                category_id=main_category.id,
                subcategory_id=subcategory.id,
                title='Momentum Burst Method - Die 4% Breakout Strategie',
                slug='momentum-burst-method',
                description='StockBees bewaehrte Momentum Burst Methode: 4% Scanner, 2LYNCH Kriterien, und wie Du systematisch 8-40% in 3-5 Tagen handelst. Inklusive TC2000 Formeln und praktischen Beispielen.',
                icon='ROCKET',
                content_type='html',
                template_file='momentum-burst-method.html',
                is_published=True,
                is_lead_magnet=False,
                required_subscription_levels=['premium', 'elite', 'elite_pro'],
                estimated_duration=90,  # 90 Minuten (sehr umfangreich)
                difficulty_level='intermediate',
                sort_order=1,
                view_count=0
            )
            
            db.session.add(module)
            db.session.commit()
            
            print("\n" + "="*70)
            print("[SUCCESS] MOMENTUM BURST METHOD MODUL ERFOLGREICH REGISTRIERT")
            print("="*70)
            print(f"Modul ID: {module.id}")
            print(f"Titel: {module.title}")
            print(f"Slug: {module.slug}")
            print(f"Kategorie: {main_category.name}")
            print(f"Unterkategorie: {subcategory.name}")
            print(f"Template: {module.template_file}")
            print(f"Subscription: {', '.join(module.required_subscription_levels)}")
            print(f"Dauer: {module.estimated_duration} Minuten")
            print(f"Schwierigkeit: {module.difficulty_level}")
            print(f"Published: {module.is_published}")
            print("="*70)
            print(f"\n[WEB] Modul erreichbar unter: /momentum-burst-method")
            print(f"[ADMIN] Sichtbar in Admin: /admin/modules")
            print(f"[USER] Sichtbar fuer Premium+ User in: /modules")
            print("\n")
            
            return module
            
        except Exception as e:
            print(f"\n[ERROR] FEHLER beim Registrieren des Moduls:")
            print(f"   {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return None

def unregister_momentum_burst_method():
    """Entfernt das Momentum Burst Method Modul (fuer Testing)"""
    
    with app.app_context():
        try:
            module = LearningModule.query.filter_by(slug='momentum-burst-method').first()
            if module:
                db.session.delete(module)
                db.session.commit()
                print("[OK] Momentum Burst Method Modul entfernt")
            else:
                print("[INFO] Momentum Burst Method Modul nicht gefunden")
                
        except Exception as e:
            print(f"[ERROR] Fehler beim Entfernen: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Momentum Burst Method Modul Migration')
    parser.add_argument('--unregister', action='store_true', 
                       help='Entfernt das Modul (für Testing)')
    
    args = parser.parse_args()
    
    if args.unregister:
        unregister_momentum_burst_method()
    else:
        register_momentum_burst_method()

