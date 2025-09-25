#!/usr/bin/env python3
"""
Test der Registrierungs-Funktionalität
"""

import requests
from datetime import datetime

def test_registration():
    """Testet die User-Registrierung"""
    base_url = "http://localhost:5000"
    
    print("🧪 REGISTRIERUNGS-TEST")
    print("=" * 40)
    print(f"⏰ Test-Zeit: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    # Test-Daten
    test_user = {
        'first_name': 'Test',
        'last_name': 'User',
        'email': f'test{datetime.now().strftime("%H%M%S")}@example.com',
        'username': f'testuser{datetime.now().strftime("%H%M%S")}',
        'password': 'testpassword123'
    }
    
    print(f"📝 Teste Registrierung für: {test_user['username']}")
    print(f"📧 E-Mail: {test_user['email']}")
    
    try:
        # POST-Request an Registrierung
        response = requests.post(
            f"{base_url}/register",
            data=test_user,
            allow_redirects=False,
            timeout=10
        )
        
        print(f"\n📊 Response Status: {response.status_code}")
        
        if response.status_code == 302:
            # Redirect nach Login = Erfolg
            print("✅ Registrierung erfolgreich!")
            print("✅ Redirect zu Login-Seite")
            
            # Teste Login mit neuen Daten
            print(f"\n🔑 Teste Login mit neuen Daten...")
            login_response = requests.post(
                f"{base_url}/login",
                data={
                    'email_or_username': test_user['username'],
                    'password': test_user['password']
                },
                allow_redirects=False,
                timeout=10
            )
            
            if login_response.status_code == 302:
                print("✅ Login erfolgreich!")
                print("🎉 REGISTRIERUNG UND LOGIN FUNKTIONIEREN!")
            else:
                print(f"⚠️  Login-Status: {login_response.status_code}")
                
        elif response.status_code == 200:
            # Seite neu geladen = Fehler
            if "Fehler" in response.text:
                print("❌ Registrierung fehlgeschlagen")
                if "bereits registriert" in response.text:
                    print("   Grund: E-Mail bereits registriert")
                elif "bereits vergeben" in response.text:
                    print("   Grund: Username bereits vergeben")
                else:
                    print("   Grund: Unbekannter Fehler")
            else:
                print("⚠️  Unerwartete Response")
        else:
            print(f"❌ Unerwarteter Status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Fehler beim Test: {e}")
    
    print("\n" + "=" * 40)

if __name__ == '__main__':
    test_registration()

