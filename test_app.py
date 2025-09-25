#!/usr/bin/env python3
"""
Test-Script für Didis Trading Academy
Führt systematische Tests der App-Funktionalität durch
"""

import requests
import time
from datetime import datetime

def test_app_functionality():
    """Testet die wichtigsten App-Funktionen"""
    base_url = "http://localhost:5000"
    
    print("🧪 DIDIS TRADING ACADEMY - FUNKTIONS-TEST")
    print("=" * 50)
    print(f"⏰ Test-Zeit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Test-URL: {base_url}")
    print()
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Homepage
    print("📄 Test 1: Homepage-Zugriff")
    tests_total += 1
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("   ✅ Homepage erreichbar (Status: 200)")
            if "Didis Trading Academy" in response.text:
                print("   ✅ Titel korrekt gefunden")
                tests_passed += 1
            else:
                print("   ⚠️  Titel nicht gefunden")
        else:
            print(f"   ❌ Fehler: Status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Verbindungsfehler: {e}")
    
    # Test 2: Login-Seite
    print("\n🔑 Test 2: Login-Seite")
    tests_total += 1
    try:
        response = requests.get(f"{base_url}/login", timeout=5)
        if response.status_code == 200:
            print("   ✅ Login-Seite erreichbar")
            if "Anmeldung" in response.text:
                print("   ✅ Login-Formular vorhanden")
                tests_passed += 1
            else:
                print("   ⚠️  Login-Formular nicht gefunden")
        else:
            print(f"   ❌ Fehler: Status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
    
    # Test 3: Registrierungs-Seite
    print("\n📝 Test 3: Registrierungs-Seite")
    tests_total += 1
    try:
        response = requests.get(f"{base_url}/register", timeout=5)
        if response.status_code == 200:
            print("   ✅ Registrierungs-Seite erreichbar")
            if "Registrierung" in response.text:
                print("   ✅ Registrierungs-Formular vorhanden")
                tests_passed += 1
            else:
                print("   ⚠️  Registrierungs-Formular nicht gefunden")
        else:
            print(f"   ❌ Fehler: Status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
    
    # Test 4: Module-Übersicht
    print("\n📚 Test 4: Module-Übersicht")
    tests_total += 1
    try:
        response = requests.get(f"{base_url}/modules", timeout=5)
        if response.status_code == 200:
            print("   ✅ Module-Seite erreichbar")
            if "Module" in response.text:
                print("   ✅ Module-Inhalt vorhanden")
                tests_passed += 1
            else:
                print("   ⚠️  Module-Inhalt nicht gefunden")
        else:
            print(f"   ❌ Fehler: Status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
    
    # Test 5: Admin-Panel (ohne Login)
    print("\n🔧 Test 5: Admin-Panel (Zugriffskontrolle)")
    tests_total += 1
    try:
        response = requests.get(f"{base_url}/admin/modules", timeout=5)
        if response.status_code == 302:  # Redirect zu Login
            print("   ✅ Admin-Panel geschützt (Redirect)")
            tests_passed += 1
        elif response.status_code == 200:
            print("   ⚠️  Admin-Panel ohne Login erreichbar")
        else:
            print(f"   ❌ Unerwarteter Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Fehler: {e}")
    
    # Ergebnis
    print("\n" + "=" * 50)
    print("📊 TEST-ERGEBNIS:")
    print(f"   ✅ Erfolgreich: {tests_passed}/{tests_total}")
    print(f"   📈 Erfolgsrate: {(tests_passed/tests_total)*100:.1f}%")
    
    if tests_passed == tests_total:
        print("\n🎉 ALLE TESTS BESTANDEN!")
        print("✅ Die App ist funktionsfähig und bereit für den Einsatz!")
    elif tests_passed >= tests_total * 0.8:
        print("\n👍 MEISTE TESTS BESTANDEN!")
        print("✅ Die App funktioniert größtenteils korrekt.")
    else:
        print("\n⚠️  EINIGE TESTS FEHLGESCHLAGEN!")
        print("🔧 Bitte prüfen Sie die Fehler-Meldungen.")
    
    print("\n🚀 NÄCHSTE SCHRITTE:")
    print("1. Browser öffnen: http://localhost:5000")
    print("2. Demo-Login: admin/admin")
    print("3. Registrierung testen")
    print("4. Module durchsuchen")
    print("5. Admin-Panel testen")

if __name__ == '__main__':
    test_app_functionality()

