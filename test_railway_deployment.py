# -*- coding: utf-8 -*-
"""
Test Railway Deployment - Didis Trading Academy
"""
import requests
import time
from datetime import datetime

def test_railway_deployment():
    base_url = "https://didis-premium-app-production.up.railway.app"
    
    print("=" * 60)
    print("TEST RAILWAY DEPLOYMENT")
    print("=" * 60)
    print(f"Zeit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"URL: {base_url}")
    
    # Test endpoints
    test_urls = [
        ("/", "Hauptseite"),
        ("/modules", "Module Übersicht"),
        ("/module/expected-value", "Expected Value Modul"),
        ("/module/tirone-quadrant-lines", "Tirone Levels Modul"),
        ("/login", "Login Seite")
    ]
    
    results = {}
    
    for endpoint, description in test_urls:
        url = f"{base_url}{endpoint}"
        try:
            print(f"\nTeste {description}: {endpoint}")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"[OK] {description}: OK (200)")
                results[endpoint] = True
            elif response.status_code in [301, 302, 307]:
                print(f"[REDIRECT] {description}: Redirect ({response.status_code})")
                results[endpoint] = True
            else:
                print(f"[ERROR] {description}: Error {response.status_code}")
                results[endpoint] = False
                
        except requests.exceptions.Timeout:
            print(f"[TIMEOUT] {description}: Timeout")
            results[endpoint] = False
        except Exception as e:
            print(f"[ERROR] {description}: {str(e)}")
            results[endpoint] = False
    
    # Summary
    successful = sum(results.values())
    total = len(results)
    
    print("\n" + "=" * 60)
    print("ERGEBNISSE")
    print("=" * 60)
    print(f"Erfolgreich: {successful}/{total}")
    
    if successful == total:
        print("[SUCCESS] ALLE TESTS ERFOLGREICH!")
        print("\n[LINKS] PRODUKTIONS-LINKS:")
        print(f"   Hauptseite: {base_url}/")
        print(f"   Module: {base_url}/modules")
        print(f"   Expected Value: {base_url}/module/expected-value")
        print(f"   Tirone Levels: {base_url}/module/tirone-quadrant-lines")
        print(f"   Admin: {base_url}/admin/modules")
        print("\n[LOGIN] LOGIN-DATEN:")
        print("   Username: admin")
        print("   Password: admin")
        return True
    else:
        print("[WARNING] EINIGE TESTS FEHLGESCHLAGEN")
        return False

if __name__ == "__main__":
    test_railway_deployment()
