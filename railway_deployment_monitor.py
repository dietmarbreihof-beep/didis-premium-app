#!/usr/bin/env python3
"""
🚀 RAILWAY DEPLOYMENT MONITOR
Überwacht und testet das Railway-Deployment der Didis Trading Academy

Version: 1.0
"""

import requests
import time
import sys
from datetime import datetime
import json

class RailwayMonitor:
    def __init__(self):
        self.base_url = "https://didis-premium-app-production.up.railway.app"
        self.endpoints_to_test = [
            "/",
            "/modules", 
            "/module/expected-value",
            "/module/tirone-quadrant-lines",
            "/admin/modules"
        ]
        
    def test_endpoint(self, endpoint, description="", timeout=10):
        """Testet einen einzelnen Endpoint"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            print(f"🔍 Teste {description}: {endpoint}")
            response = requests.get(url, timeout=timeout)
            
            if response.status_code == 200:
                print(f"✅ {description}: OK ({response.status_code})")
                return True
            elif response.status_code in [301, 302]:
                print(f"🔄 {description}: Redirect ({response.status_code})")
                return True
            else:
                print(f"❌ {description}: Fehler {response.status_code}")
                return False
                
        except requests.exceptions.Timeout:
            print(f"⏰ {description}: Timeout nach {timeout}s")
            return False
        except requests.exceptions.ConnectionError:
            print(f"🔌 {description}: Verbindungsfehler")
            return False
        except Exception as e:
            print(f"💥 {description}: {str(e)}")
            return False
    
    def wait_for_deployment(self, max_wait=300, check_interval=30):
        """Wartet auf erfolgreiches Deployment"""
        print(f"\n⏳ WARTE AUF RAILWAY-DEPLOYMENT (max. {max_wait//60} min)")
        print("=" * 50)
        
        start_time = time.time()
        
        while (time.time() - start_time) < max_wait:
            elapsed = int(time.time() - start_time)
            print(f"\n⏱️  Zeit: {elapsed//60}:{elapsed%60:02d} | Teste Hauptseite...")
            
            if self.test_endpoint("/", "Hauptseite", timeout=15):
                print(f"🎉 DEPLOYMENT ERFOLGREICH! (nach {elapsed//60}:{elapsed%60:02d})")
                return True
            
            if elapsed < max_wait - check_interval:
                print(f"💤 Warte {check_interval}s bis zum nächsten Test...")
                time.sleep(check_interval)
            else:
                break
        
        print(f"⏰ TIMEOUT: Deployment nicht erfolgreich nach {max_wait//60} Minuten")
        return False
    
    def comprehensive_test(self):
        """Führt umfassende Tests durch"""
        print("\n🧪 UMFASSENDE TESTS")
        print("=" * 30)
        
        test_results = {}
        
        tests = [
            ("/", "Hauptseite"),
            ("/modules", "Module-Übersicht"),
            ("/module/expected-value", "Expected Value Modul"),
            ("/module/tirone-quadrant-lines", "Tirone Levels Modul"),
            ("/login", "Login-Seite")
        ]
        
        for endpoint, description in tests:
            result = self.test_endpoint(endpoint, description)
            test_results[endpoint] = result
        
        # Ergebnis-Zusammenfassung
        successful = sum(test_results.values())
        total = len(test_results)
        
        print(f"\n📊 TEST-ERGEBNISSE: {successful}/{total} erfolgreich")
        
        if successful == total:
            print("🎉 ALLE TESTS ERFOLGREICH!")
            return True
        else:
            print("⚠️  EINIGE TESTS FEHLGESCHLAGEN!")
            return False
    
    def check_modules_api(self):
        """Prüft die Module-API"""
        print("\n🔌 API-TESTS")
        print("=" * 20)
        
        # Test 1: Module-Liste abrufen
        try:
            response = requests.get(f"{self.base_url}/api/modules", timeout=10)
            if response.status_code == 200:
                modules = response.json()
                print(f"✅ Module-API: {len(modules)} Module gefunden")
                
                # Specific module checks
                expected_modules = ["expected-value", "tirone-quadrant-lines"]
                found_modules = [m.get('slug') for m in modules]
                
                for module_slug in expected_modules:
                    if module_slug in found_modules:
                        print(f"✅ Modul gefunden: {module_slug}")
                    else:
                        print(f"❌ Modul fehlt: {module_slug}")
                        
            else:
                print(f"❌ Module-API Fehler: {response.status_code}")
                
        except Exception as e:
            print(f"💥 API-Test Fehler: {str(e)}")

def main():
    """Hauptfunktion"""
    print("=" * 60)
    print("🚀 RAILWAY DEPLOYMENT MONITOR")
    print("=" * 60)
    print(f"⏰ Gestartet: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 URL: https://didis-premium-app-production.up.railway.app/")
    
    monitor = RailwayMonitor()
    
    # Schritt 1: Auf Deployment warten
    if not monitor.wait_for_deployment(max_wait=300):
        print("❌ Deployment-Überwachung fehlgeschlagen!")
        sys.exit(1)
    
    # Schritt 2: Umfassende Tests
    time.sleep(5)  # Kurz warten nach erfolgreichem Deployment
    if not monitor.comprehensive_test():
        print("⚠️  Nicht alle Tests erfolgreich!")
    
    # Schritt 3: API-Tests
    monitor.check_modules_api()
    
    # Erfolgsmeldung
    print("\n" + "=" * 60)
    print("✅ MONITORING ABGESCHLOSSEN")
    print("=" * 60)
    print("🔗 PRODUKTIONS-LINKS:")
    print("   🏠 Hauptseite: https://didis-premium-app-production.up.railway.app/")
    print("   📚 Module: https://didis-premium-app-production.up.railway.app/modules")
    print("   📊 Expected Value: https://didis-premium-app-production.up.railway.app/module/expected-value")
    print("   📈 Tirone Levels: https://didis-premium-app-production.up.railway.app/module/tirone-quadrant-lines")
    print("   👨‍💼 Admin: https://didis-premium-app-production.up.railway.app/admin/modules")
    
    print("\n🔐 LOGIN-DATEN:")
    print("   Username: admin")
    print("   Password: admin")

if __name__ == "__main__":
    main()









