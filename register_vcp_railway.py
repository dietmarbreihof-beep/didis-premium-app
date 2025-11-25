"""
Railway Migration Script: VCP-Pattern Modul
Registriert das VCP-Pattern Modul auf Railway Production

Verwendung:
    railway run python register_vcp_railway.py
"""

import os
import sys

# Railway Produktions-DB URL verwenden
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    print("[ERROR] DATABASE_URL nicht gefunden!")
    print("[INFO] Verwende lokale Datenbank...")

# App importieren
from app import app, db, LearningModule, ModuleCategory, ModuleSubcategory
from datetime import datetime

def register_vcp_railway():
    """Registriert VCP-Pattern Modul auf Railway"""
    
    with app.app_context():
        print("\n" + "="*70)
        print("[RAILWAY] VCP-PATTERN MODUL REGISTRIERUNG")
        print("="*70 + "\n")
        
        # Check if module exists
        existing = LearningModule.query.filter_by(slug='vcp-pattern').first()
        
        if existing:
            print(f"[INFO] Modul existiert bereits (ID: {existing.id})")
            print("[UPDATE] Aktualisiere Modul...")
            module = existing
        else:
            print("[NEW] Erstelle neues Modul...")
            module = LearningModule()
        
        # Get category
        category = ModuleCategory.query.filter_by(slug='elite-system-iii').first()
        if not category:
            print("[ERROR] Kategorie 'elite-system-iii' nicht gefunden!")
            print("[INFO] Erstelle Kategorie...")
            category = ModuleCategory(
                name='System III - Elite Trading',
                slug='elite-system-iii',
                description='Fortgeschrittene Trading-Strategien nach Mark Minervini und Lance Breitstein',
                icon='crown',
                sort_order=3,
                is_published=True
            )
            db.session.add(category)
            db.session.flush()
        
        print(f"[OK] Kategorie: {category.name} (ID: {category.id})")
        
        # Get/Create subcategory
        subcategory = ModuleSubcategory.query.filter_by(
            category_id=category.id,
            slug='chartmuster-setups'
        ).first()
        
        if not subcategory:
            print("[INFO] Erstelle Unterkategorie...")
            subcategory = ModuleSubcategory(
                category_id=category.id,
                name='Chartmuster & Setups',
                slug='chartmuster-setups',
                description='Professionelle Chartmuster-Erkennung für explosive Trades',
                sort_order=1
            )
            db.session.add(subcategory)
            db.session.flush()
        
        print(f"[OK] Unterkategorie: {subcategory.name} (ID: {subcategory.id})")
        
        # Set module details
        module.category_id = category.id
        module.subcategory_id = subcategory.id
        module.title = 'VCP-Pattern: Mark Minervinis Signatur-Strategie'
        module.slug = 'vcp-pattern'
        module.description = '''Das Volatility Contraction Pattern (VCP) ist Mark Minervinis Signatur-Chartmuster 
für explosionsartige Kursausbrüche. Die Methodik brachte ihm 1997 und 2021 den U.S. Investing Championship 
Titel ein und ermöglichte eine 33.554% Rendite über fünf Jahre. Lerne die technische Anatomie, 
SEPA-Methodik, Trend Template mit 8 Kriterien und die 7 lebensverändernden Trading-Regeln.'''
        
        module.icon = 'chart'
        module.content_type = 'html'
        module.template_file = 'vcp-pattern.html'
        module.is_published = True
        module.is_lead_magnet = False
        module.required_subscription_levels = ['elite', 'elite_pro']
        module.estimated_duration = 90
        module.difficulty_level = 'advanced'
        module.sort_order = 10
        module.meta_keywords = 'VCP Pattern, Mark Minervini, Volatility Contraction, SEPA Methodik, Stage 2, Trend Template, Trading Strategie, Chartmuster, Ausbruch Trading'
        
        if not existing:
            module.created_at = datetime.utcnow()
        module.updated_at = datetime.utcnow()
        
        if not existing:
            db.session.add(module)
        
        try:
            db.session.commit()
            print("\n" + "="*70)
            print("[SUCCESS] MODUL ERFOLGREICH REGISTRIERT!")
            print("="*70)
            print(f"\n[DETAILS]")
            print(f"   Modul-ID: {module.id}")
            print(f"   Titel: {module.title}")
            print(f"   Slug: {module.slug}")
            print(f"   Route: /vcp-pattern")
            print(f"   Kategorie: {category.name}")
            print(f"   Unterkategorie: {subcategory.name}")
            print(f"   Subscription: {', '.join(module.required_subscription_levels)}")
            print(f"   Published: {'Ja' if module.is_published else 'Nein'}")
            print(f"\n[URL] https://didis-premium-app-production.up.railway.app/vcp-pattern")
            print("\n" + "="*70)
            
        except Exception as e:
            db.session.rollback()
            print(f"\n[ERROR] Fehler beim Speichern: {str(e)}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
        
        # Verify
        verify = LearningModule.query.filter_by(slug='vcp-pattern').first()
        if verify:
            print("\n[VERIFY] Modul erfolgreich verifiziert!")
            print(f"   Kategorie: {verify.category.name}")
            print(f"   Unterkategorie: {verify.subcategory.name}")
        else:
            print("\n[ERROR] Verifikation fehlgeschlagen!")
            sys.exit(1)
        
        print("\n[DONE] Migration abgeschlossen!")
        print("="*70 + "\n")

if __name__ == '__main__':
    try:
        register_vcp_railway()
    except KeyboardInterrupt:
        print("\n[WARN] Abgebrochen.")
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


