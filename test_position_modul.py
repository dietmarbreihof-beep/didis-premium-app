#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Test: Position vergrößern Modul
Prüft ob das Modul korrekt installiert ist
"""

import sys
import os

# Füge Parent-Directory zum Python-Path hinzu
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, LearningModule
import json

def test_position_vergroessern_module():
    """Testet ob das Position-Vergrößern-Modul verfügbar ist"""
    
    with app.app_context():
        print("=" * 60)
        print("🧪 Test: Position vergrößern Modul")
        print("=" * 60)
        
        # 1. Prüfe ob Template existiert
        print("\n[1/4] Template-Datei prüfen...")
        template_path = os.path.join('templates', 'position-vergroessern.html')
        if os.path.exists(template_path):
            print(f"  ✅ Template gefunden: {template_path}")
            # Prüfe Dateigröße
            size = os.path.getsize(template_path)
            print(f"     Größe: {size:,} Bytes ({size/1024:.1f} KB)")
        else:
            print(f"  ❌ Template NICHT gefunden: {template_path}")
            return False
        
        # 2. Prüfe ob Modul in Datenbank existiert
        print("\n[2/4] Datenbank-Eintrag prüfen...")
        try:
            module = LearningModule.query.filter_by(slug='position-vergroessern').first()
            if module:
                print(f"  ✅ Modul in DB gefunden: {module.title}")
                print(f"     ID: {module.id}")
                print(f"     Icon: {module.icon}")
                print(f"     Kategorie ID: {module.category_id}")
                print(f"     Published: {module.is_published}")
                print(f"     Lead Magnet: {module.is_lead_magnet}")
                print(f"     Template: {module.template_file}")
                print(f"     Duration: {module.estimated_duration} min")
                print(f"     Difficulty: {module.difficulty_level}")
                
                # Subscription Levels
                try:
                    levels = json.loads(module.required_subscription_levels) if isinstance(module.required_subscription_levels, str) else module.required_subscription_levels
                    print(f"     Required Subscription: {', '.join(levels)}")
                except:
                    print(f"     Required Subscription: {module.required_subscription_levels}")
            else:
                print("  ❌ Modul NICHT in Datenbank gefunden!")
                print("     Führe aus: python migrations/register_position_vergroessern.py")
                return False
        except Exception as e:
            print(f"  ❌ Fehler beim DB-Zugriff: {str(e)}")
            return False
        
        # 3. Prüfe ob Route existiert
        print("\n[3/4] Flask-Route prüfen...")
        routes = [str(rule) for rule in app.url_map.iter_rules()]
        if '/position-vergroessern' in routes:
            print("  ✅ Route gefunden: /position-vergroessern")
        else:
            print("  ❌ Route NICHT gefunden!")
            print("     Prüfe app.py um Zeile 1028-1048")
            return False
        
        # 4. Test-URL ausgeben
        print("\n[4/4] URLs zum Testen...")
        print("  🌐 Direkte Route:")
        print("     http://localhost:5000/position-vergroessern")
        print("\n  🌐 Modul-System Route:")
        print("     http://localhost:5000/module/position-vergroessern")
        print("\n  📚 Modul-Übersicht:")
        print("     http://localhost:5000/modules")
        
        # 5. Erfolgsmeldung
        print("\n" + "=" * 60)
        print("✅ ALLE TESTS BESTANDEN!")
        print("=" * 60)
        print("\n💡 Nächste Schritte:")
        print("   1. Starte die App: python app.py")
        print("   2. Login als Premium-User:")
        print("      Username: premium | Password: premium")
        print("      ODER: admin | admin (voller Zugriff)")
        print("   3. Navigiere zu: http://localhost:5000/position-vergroessern")
        print("\n📖 Vollständige Anleitung: POSITION_VERGROESSERN_SETUP.md")
        print()
        
        return True

if __name__ == '__main__':
    print("\n🚀 Starte Test-Suite...\n")
    success = test_position_vergroessern_module()
    
    if not success:
        print("\n" + "=" * 60)
        print("❌ TESTS FEHLGESCHLAGEN!")
        print("=" * 60)
        print("\n💡 Behebung:")
        print("   1. Führe Migration aus:")
        print("      python migrations/register_position_vergroessern.py")
        print("   2. Führe diesen Test erneut aus:")
        print("      python test_position_modul.py")
        print()
        sys.exit(1)
    
    sys.exit(0)


