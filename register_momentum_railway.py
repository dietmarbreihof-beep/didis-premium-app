"""
Railway Deployment Script: Momentum Burst Method Modul
Registriert das Modul direkt auf Railway nach dem Deployment
"""

import os
import sys

# Railway Umgebung
RAILWAY_DB_URL = os.environ.get('DATABASE_URL', '')

if RAILWAY_DB_URL:
    print("[RAILWAY] Verwende Railway PostgreSQL Datenbank")
else:
    print("[LOCAL] Verwende lokale SQLite Datenbank")

from app import app, db, LearningModule, ModuleCategory, ModuleSubcategory
from datetime import datetime

def register_momentum_burst_on_railway():
    """Registriert Momentum Burst Method Modul auf Railway"""
    
    with app.app_context():
        try:
            # Prüfe ob Modul bereits existiert
            existing = LearningModule.query.filter_by(slug='momentum-burst-method').first()
            if existing:
                print(f"[OK] Momentum Burst Modul existiert bereits (ID: {existing.id})")
                return existing
            
            # Finde oder erstelle Hauptkategorie
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
            else:
                print(f"[OK] Kategorie gefunden: {main_category.name}")
            
            # Finde oder erstelle Unterkategorie
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
            else:
                print(f"[OK] Unterkategorie gefunden: {subcategory.name}")
            
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
                estimated_duration=90,
                difficulty_level='intermediate',
                sort_order=1,
                view_count=0
            )
            
            db.session.add(module)
            db.session.commit()
            
            print("\n" + "="*70)
            print("[SUCCESS] MOMENTUM BURST METHOD MODUL REGISTRIERT")
            print("="*70)
            print(f"Modul ID: {module.id}")
            print(f"Slug: {module.slug}")
            print(f"URL: /momentum-burst-method")
            print(f"Template: {module.template_file}")
            print(f"Subscription: {', '.join(module.required_subscription_levels)}")
            print("="*70)
            
            return module
            
        except Exception as e:
            print(f"\n[ERROR] Fehler beim Registrieren:")
            print(f"   {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return None

if __name__ == '__main__':
    print("\n[START] Railway Momentum Burst Modul Registration")
    print(f"[INFO] Database: {'Railway' if RAILWAY_DB_URL else 'Local'}")
    register_momentum_burst_on_railway()
    print("[DONE] Registration abgeschlossen\n")


