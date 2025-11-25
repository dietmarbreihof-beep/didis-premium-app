"""
Migration: KGV & PEG Trading Modul registrieren
Erstellt: 2025-01-25
Beschreibung: Registriert das KGV/PEG-Lernmodul ueber Yahoo, Palantir und Crocs
"""

import sys
import os

# Pfad zum Projekt-Root hinzufuegen
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db, LearningModule, ModuleSubcategory

def register_kgv_peg_modul():
    """Registriert das KGV/PEG Trading Modul in der Datenbank"""
    with app.app_context():
        print("[INFO] Suche Unterkategorie 'Fundamentalanalyse'...")
        
        # Suche nach der Fundamentalanalyse Unterkategorie
        subcategory = ModuleSubcategory.query.filter_by(slug='fundamentalanalyse').first()
        
        if not subcategory:
            print("[FAIL] Unterkategorie 'fundamentalanalyse' nicht gefunden!")
            print("[INFO] Bitte zuerst die Kategorie erstellen oder eine andere waehlen.")
            return False
        
        print(f"[OK] Unterkategorie gefunden: {subcategory.name}")
        
        # Pruefe ob Modul bereits existiert
        existing = LearningModule.query.filter_by(slug='kgv-peg-trading').first()
        if existing:
            print(f"[INFO] Modul 'kgv-peg-trading' existiert bereits (ID: {existing.id})")
            
            # Update des bestehenden Moduls
            existing.title = "KGV & PEG: Von Yahoo zu Palantir"
            existing.description = "Lerne, wie Marc Minervini mit Yahoo 7.800% Gewinn machte - und warum traditionelle Bewertungsmetriken bei revolutionaeren Unternehmen versagen. Mit Crocs als Warnung!"
            existing.icon = "[CHART]"
            existing.content_type = "html"
            existing.template_file = "kgv-peg-trading-lernseite.html"
            existing.is_published = True
            existing.is_lead_magnet = False
            existing.required_subscription_levels = ["premium", "elite", "elite_pro"]
            existing.estimated_duration = 45
            existing.difficulty_level = "intermediate"
            existing.sort_order = 20
            
            db.session.commit()
            print("[OK] Modul erfolgreich aktualisiert!")
            return True
        
        # Erstelle neues Modul
        print("[INFO] Erstelle neues Modul...")
        
        new_module = LearningModule(
            subcategory_id=subcategory.id,
            title="KGV & PEG: Von Yahoo zu Palantir",
            slug="kgv-peg-trading",
            description="Lerne, wie Marc Minervini mit Yahoo 7.800% Gewinn machte - und warum traditionelle Bewertungsmetriken bei revolutionaeren Unternehmen versagen. Mit Crocs als Warnung!",
            icon="[CHART]",
            content_type="html",
            template_file="kgv-peg-trading-lernseite.html",
            is_published=True,
            is_lead_magnet=False,  # Premium Content
            required_subscription_levels=["premium", "elite", "elite_pro"],
            estimated_duration=45,  # Minuten
            difficulty_level="intermediate",  # beginner, intermediate, advanced
            sort_order=20
        )
        
        db.session.add(new_module)
        db.session.commit()
        
        print(f"[OK] Modul erfolgreich registriert!")
        print(f"   ID: {new_module.id}")
        print(f"   Titel: {new_module.title}")
        print(f"   Slug: {new_module.slug}")
        print(f"   Template: {new_module.template_file}")
        print(f"   Unterkategorie: {subcategory.name}")
        print(f"   Published: {new_module.is_published}")
        print(f"   Subscription: {new_module.required_subscription_levels}")
        print(f"   Dauer: {new_module.estimated_duration} Min")
        print(f"   Schwierigkeit: {new_module.difficulty_level}")
        
        return True

if __name__ == '__main__':
    print("=" * 60)
    print("KGV & PEG Trading Modul - Migration")
    print("=" * 60)
    
    try:
        success = register_kgv_peg_modul()
        
        if success:
            print("\n" + "=" * 60)
            print("[OK] Migration erfolgreich abgeschlossen!")
            print("=" * 60)
            print("\nNaechste Schritte:")
            print("1. [OK] Template erstellt: templates/kgv-peg-trading-lernseite.html")
            print("2. [OK] Modul in Datenbank registriert")
            print("3. [INFO] Route in app.py hinzufuegen (optional fuer spezielle Route):")
            print("   @app.route('/kgv-peg-trading')")
            print("4. [TEST] Testen: http://localhost:5000/module/kgv-peg-trading")
            print("\n[INFO] Oder nutze die Standard-Route: /module/kgv-peg-trading")
        else:
            print("\n" + "=" * 60)
            print("[FAIL] Migration fehlgeschlagen!")
            print("=" * 60)
            sys.exit(1)
            
    except Exception as e:
        print(f"\n[FAIL] Fehler bei der Migration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
