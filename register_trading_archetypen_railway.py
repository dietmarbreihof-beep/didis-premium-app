"""
Railway Migration Script: Trading-Archetypen Modul
Registriert das Trading-Archetypen Modul auf Railway Production

Verwendung:
    railway run python register_trading_archetypen_railway.py
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

def register_trading_archetypen_railway():
    """Registriert Trading-Archetypen Modul auf Railway"""
    
    with app.app_context():
        print("\n" + "="*70)
        print("[RAILWAY] TRADING-ARCHETYPEN MODUL REGISTRIERUNG")
        print("="*70 + "\n")
        
        # Check if module exists
        existing = LearningModule.query.filter_by(slug='trading_archetypen').first()
        
        if existing:
            print(f"[INFO] Modul existiert bereits (ID: {existing.id})")
            print("[UPDATE] Aktualisiere Modul...")
            module = existing
        else:
            print("[NEW] Erstelle neues Modul...")
            module = LearningModule()
        
        # Get or create category
        category = ModuleCategory.query.filter_by(slug='trading-strategien').first()
        if not category:
            print("[ERROR] Kategorie 'trading-strategien' nicht gefunden!")
            print("[INFO] Erstelle Kategorie...")
            category = ModuleCategory(
                name='1. Trading-Strategien',
                slug='trading-strategien',
                description='Grundlegende und fortgeschrittene Trading-Methoden und -Strategien',
                icon='🎯',
                sort_order=1,
                is_published=True
            )
            db.session.add(category)
            db.session.flush()
        
        print(f"[OK] Kategorie: {category.name} (ID: {category.id})")
        
        # No subcategory for this module
        print("[INFO] Keine Unterkategorie - Modul wird direkt unter Kategorie eingefügt")
        
        # Set module details
        module.category_id = category.id
        module.subcategory_id = None
        module.title = 'Trading-Methoden Vertiefung'
        module.slug = 'trading_archetypen'
        module.description = '''Verstehe die drei Säulen erfolgreichen Tradings: Buy & Hold, Position Trading und Swing Trading. 
Lerne den Keulen-Kombi-Prozess und finde deinen systematischen Edge. Dieses Modul vertieft die Grundlagen der 
verschiedenen Trading-Archetypen und hilft dir, deinen persönlichen Trading-Stil zu entwickeln.'''
        
        module.icon = '🎯'
        module.content_type = 'html'
        module.template_file = 'trading_archetypen.html'
        module.is_published = True
        module.is_lead_magnet = False
        module.required_subscription_levels = ['premium', 'elite', 'masterclass']
        module.estimated_duration = 25
        module.difficulty_level = 'intermediate'
        module.sort_order = 100
        module.meta_keywords = 'Trading Archetypen, Buy and Hold, Position Trading, Swing Trading, Trading Strategien, Keulen-Kombi-Prozess, Trading Methoden'
        
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
            print(f"   Route: /module/trading_archetypen")
            print(f"   Direkte Route: /trading-archetypen")
            print(f"   Kategorie: {category.name}")
            print(f"   Template: {module.template_file}")
            print(f"   Subscription: {', '.join(module.required_subscription_levels)}")
            print(f"   Published: {'Ja' if module.is_published else 'Nein'}")
            print(f"\n[URLs]")
            print(f"   https://didis-premium-app-production.up.railway.app/module/trading_archetypen")
            print(f"   https://didis-premium-app-production.up.railway.app/trading-archetypen")
            print("\n" + "="*70)
            
        except Exception as e:
            db.session.rollback()
            print(f"\n[ERROR] Fehler beim Speichern: {str(e)}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
        
        # Verify
        verify = LearningModule.query.filter_by(slug='trading_archetypen').first()
        if verify:
            print("\n[VERIFY] Modul erfolgreich verifiziert!")
            print(f"   Kategorie: {verify.category.name}")
            if verify.subcategory:
                print(f"   Unterkategorie: {verify.subcategory.name}")
        else:
            print("\n[ERROR] Verifikation fehlgeschlagen!")
            sys.exit(1)
        
        print("\n[DONE] Migration abgeschlossen!")
        print("="*70 + "\n")

if __name__ == '__main__':
    try:
        register_trading_archetypen_railway()
    except KeyboardInterrupt:
        print("\n[WARN] Abgebrochen.")
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)



