"""
Migration: VCP-Pattern Modul
Registriert Mark Minervinis VCP (Volatility Contraction Pattern) als Elite-Content Modul

Ausführung:
    python migrations/register_vcp_pattern.py
"""

import sys
import os

# Add parent directory to path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db, LearningModule, ModuleCategory, ModuleSubcategory
from datetime import datetime

def register_vcp_module():
    """Registriert das VCP-Pattern Modul in der Datenbank"""
    
    with app.app_context():
        print("\n" + "="*60)
        print("VCP-PATTERN MODUL REGISTRIERUNG")
        print("="*60 + "\n")
        
        # 1. Prüfe ob Modul bereits existiert
        existing_module = LearningModule.query.filter_by(slug='vcp-pattern').first()
        if existing_module:
            print("[INFO] Modul 'vcp-pattern' existiert bereits!")
            print(f"   ID: {existing_module.id}")
            print(f"   Titel: {existing_module.title}")
            print(f"   Kategorie: {existing_module.category.name if existing_module.category else 'Keine'}")
            print(f"   Subcategory: {existing_module.subcategory.name if existing_module.subcategory else 'Keine'}")
            
            response = input("\n[?] Modul aktualisieren? (j/n): ").strip().lower()
            if response != 'j':
                print("[X] Abgebrochen.")
                return
            
            module = existing_module
            print("\n[UPDATE] Aktualisiere bestehendes Modul...")
        else:
            module = LearningModule()
            print("[NEW] Erstelle neues Modul...")
        
        # 2. Hauptkategorie finden - Technische Analyse oder Neue Module
        # HINWEIS: elite-system-iii wurde entfernt, Module landen in neue-module
        print("\n[SEARCH] Suche Hauptkategorie 'Technische Analyse'...")
        category = ModuleCategory.query.filter_by(slug='technische-analyse').first()
        
        if not category:
            print("   [INFO] Technische Analyse nicht gefunden. Suche 'Neue Module'...")
            category = ModuleCategory.query.filter_by(slug='neue-module').first()
            
        if not category:
            print("   [INFO] Erstelle Kategorie 'Neue Module'...")
            category = ModuleCategory(
                name='🆕 Neue Module',
                slug='neue-module',
                description='Automatisch erkannte Module - Bitte in die richtige Kategorie verschieben',
                icon='🆕',
                sort_order=999,
                is_published=True
            )
            db.session.add(category)
            db.session.flush()
            print(f"   [OK] Kategorie erstellt (ID: {category.id})")
        else:
            print(f"   [OK] Kategorie gefunden (ID: {category.id})")
        
        # 3. Unterkategorie finden/erstellen
        print("\n[SEARCH] Suche Unterkategorie 'Chartmuster & Setups'...")
        subcategory = ModuleSubcategory.query.filter_by(
            category_id=category.id,
            slug='chartmuster-setups'
        ).first()
        
        if not subcategory:
            print("   [INFO] Unterkategorie nicht gefunden. Erstelle neue Unterkategorie...")
            subcategory = ModuleSubcategory(
                category_id=category.id,
                name='Chartmuster & Setups',
                slug='chartmuster-setups',
                description='Professionelle Chartmuster-Erkennung für explosive Trades',
                sort_order=1
            )
            db.session.add(subcategory)
            db.session.flush()
            print(f"   [OK] Unterkategorie erstellt (ID: {subcategory.id})")
        else:
            print(f"   [OK] Unterkategorie gefunden (ID: {subcategory.id})")
        
        # 4. Modul-Details setzen
        print("\n[CONFIG] Setze Modul-Details...")
        
        module.category_id = category.id
        module.subcategory_id = subcategory.id
        module.title = 'VCP-Pattern: Mark Minervinis Signatur-Strategie'
        module.slug = 'vcp-pattern'
        module.description = '''Das Volatility Contraction Pattern (VCP) ist Mark Minervinis Signatur-Chartmuster 
für explosionsartige Kursausbrüche. Die Methodik brachte ihm 1997 und 2021 den U.S. Investing Championship 
Titel ein und ermöglichte eine 33.554% Rendite über fünf Jahre. Lerne die technische Anatomie, 
SEPA-Methodik, Trend Template mit 8 Kriterien und die 7 lebensverändernden Trading-Regeln.'''
        
        module.icon = '📈'
        module.content_type = 'html'
        module.template_file = 'vcp-pattern.html'
        module.is_published = True
        module.is_lead_magnet = False  # Elite Content
        
        # Elite-Level erforderlich
        module.required_subscription_levels = ['elite', 'elite_pro']
        
        module.estimated_duration = 90  # 90 Minuten (umfangreiches Modul)
        module.difficulty_level = 'advanced'  # Fortgeschritten
        module.sort_order = 10
        
        # SEO & Marketing
        module.meta_keywords = 'VCP Pattern, Mark Minervini, Volatility Contraction, SEPA Methodik, Stage 2, Trend Template, Trading Strategie, Chartmuster, Ausbruch Trading'
        
        # Aktualisiere Timestamps
        if not existing_module:
            module.created_at = datetime.utcnow()
        module.updated_at = datetime.utcnow()
        
        # 5. Speichern
        if not existing_module:
            db.session.add(module)
        
        try:
            db.session.commit()
            print("\n" + "="*60)
            print("[SUCCESS] MODUL ERFOLGREICH REGISTRIERT!")
            print("="*60)
            print(f"\n[DETAILS]")
            print(f"   Modul-ID: {module.id}")
            print(f"   Titel: {module.title}")
            print(f"   Slug: {module.slug}")
            print(f"   Route: /vcp-pattern")
            print(f"   Kategorie: {category.name}")
            print(f"   Unterkategorie: {subcategory.name}")
            print(f"   Subscription: {', '.join(module.required_subscription_levels)}")
            print(f"   Dauer: {module.estimated_duration} Minuten")
            print(f"   Schwierigkeit: {module.difficulty_level}")
            print(f"   Published: {'Ja' if module.is_published else 'Nein'}")
            print(f"\n[URL] https://didis-premium-app-production.up.railway.app/vcp-pattern")
            print("\n" + "="*60)
            
        except Exception as e:
            db.session.rollback()
            print(f"\n[ERROR] FEHLER beim Speichern: {str(e)}")
            import traceback
            traceback.print_exc()
            return
        
        # 6. Verifikation
        print("\n[VERIFY] Verifikation...")
        verification = LearningModule.query.filter_by(slug='vcp-pattern').first()
        if verification:
            print("   [OK] Modul in Datenbank verifiziert")
            print(f"   [OK] Kategorie verknuepft: {verification.category.name}")
            print(f"   [OK] Unterkategorie verknuepft: {verification.subcategory.name}")
        else:
            print("   [ERROR] Verifikation fehlgeschlagen!")
            return
        
        print("\n" + "="*60)
        print("[DONE] MIGRATION ERFOLGREICH ABGESCHLOSSEN!")
        print("="*60)
        print("\n[NEXT STEPS]")
        print("   1. [OK] Template erstellt: templates/vcp-pattern.html")
        print("   2. [OK] Route hinzugefuegt: /vcp-pattern")
        print("   3. [OK] Modul registriert in Datenbank")
        print("   4. [TODO] Deploy zu Railway")
        print("   5. [TODO] Teste: https://didis-premium-app-production.up.railway.app/vcp-pattern")
        print("\n[TIP] Modul ist sichtbar unter /modules -> System III - Elite Trading")

if __name__ == '__main__':
    try:
        register_vcp_module()
    except KeyboardInterrupt:
        print("\n\n[WARN] Abgebrochen durch Benutzer.")
    except Exception as e:
        print(f"\n[ERROR] FEHLER: {str(e)}")
        import traceback
        traceback.print_exc()

