"""
Test-Script für KGV/PEG Trading Modul
Prüft Template, Navigation und Datenbank-Registrierung
"""

import os
import sys

def test_template_exists():
    """Prüft ob das Template existiert"""
    template_path = "templates/kgv-peg-trading-lernseite.html"
    
    if os.path.exists(template_path):
        print("[OK] Template existiert: kgv-peg-trading-lernseite.html")
        
        # Prüfe Navigation
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Prüfe auf Navigation-Include
            if "{% include '_navigation.html' %}" in content:
                print("[OK] Navigation ist eingebunden")
            else:
                print("[FAIL] Navigation fehlt!")
                return False
            
            # Prüfe auf kritische Elemente
            checks = [
                ("Quiz-Container", "quiz-container" in content),
                ("Chart.js", "chart.js" in content),
                ("Progress-Tracking", "progressFill" in content),
                ("Responsive Design", "@media" in content),
                ("Interactive Sections", "toggleSection" in content)
            ]
            
            for name, check in checks:
                if check:
                    print(f"[OK] {name} vorhanden")
                else:
                    print(f"[FAIL] {name} fehlt!")
                    
        return True
    else:
        print(f"[FAIL] Template nicht gefunden: {template_path}")
        return False

def test_navigation_template():
    """Prüft ob _navigation.html existiert"""
    nav_path = "templates/_navigation.html"
    
    if os.path.exists(nav_path):
        print("[OK] Navigation-Template existiert: _navigation.html")
        return True
    else:
        print(f"[FAIL] Navigation-Template nicht gefunden: {nav_path}")
        return False

def test_database_module():
    """Prüft ob das Modul in der Datenbank registriert ist"""
    try:
        from app import app, db, LearningModule
        
        with app.app_context():
            module = LearningModule.query.filter_by(slug='kgv-peg-trading').first()
            
            if module:
                print(f"[OK] Modul in Datenbank gefunden:")
                print(f"   ID: {module.id}")
                print(f"   Titel: {module.title}")
                print(f"   Template: {module.template_file}")
                print(f"   Published: {module.is_published}")
                print(f"   Subscription: {module.required_subscription_levels}")
                return True
            else:
                print("[INFO] Modul noch nicht in Datenbank registriert")
                print("[INFO] Fuehre aus: python migrations/register_kgv_peg_modul.py")
                return False
                
    except Exception as e:
        print(f"[FAIL] Fehler beim Datenbankcheck: {e}")
        return False

def test_migration_script():
    """Prüft ob das Migrations-Script existiert"""
    migration_path = "migrations/register_kgv_peg_modul.py"
    
    if os.path.exists(migration_path):
        print("[OK] Migrations-Script existiert: register_kgv_peg_modul.py")
        return True
    else:
        print(f"[FAIL] Migrations-Script nicht gefunden: {migration_path}")
        return False

def run_all_tests():
    """Führt alle Tests aus"""
    print("=" * 60)
    print("KGV/PEG Trading Modul - Validierung")
    print("=" * 60)
    print()
    
    tests = [
        ("Template Check", test_template_exists),
        ("Navigation Check", test_navigation_template),
        ("Migration Script Check", test_migration_script),
        ("Database Check", test_database_module),
    ]
    
    results = []
    
    for name, test_func in tests:
        print(f"\n[TEST] {name}:")
        print("-" * 60)
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Fehler: {e}")
            results.append((name, False))
    
    # Zusammenfassung
    print("\n" + "=" * 60)
    print("Zusammenfassung")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "[OK] PASS" if result else "[FAIL] FAIL"
        print(f"{status}: {name}")
    
    print(f"\nErgebnis: {passed}/{total} Tests bestanden")
    
    if passed == total:
        print("\n[OK] Alle Tests erfolgreich!")
        print("\nNaechste Schritte:")
        print("1. Falls noch nicht registriert: python migrations/register_kgv_peg_modul.py")
        print("2. App starten: python app.py")
        print("3. Testen: http://localhost:5000/module/kgv-peg-trading")
    else:
        print("\n[WARNUNG] Einige Tests fehlgeschlagen. Bitte Fehler beheben.")
    
    return passed == total

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)

