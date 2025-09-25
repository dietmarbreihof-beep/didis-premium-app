#!/usr/bin/env python3
"""
Test Magic Line Modul Zugriff
"""

import requests

def test_magic_line():
    print("🧪 MAGIC LINE MODUL TEST")
    print("=" * 30)
    
    try:
        # Test ohne Login (sollte Redirect geben)
        response = requests.get('http://localhost:5000/module/magic-line', 
                              allow_redirects=False, timeout=5)
        
        print(f"📊 Status ohne Login: {response.status_code}")
        
        if response.status_code == 302:
            print("✅ Zugriffskontrolle funktioniert - Redirect zu Login/Upgrade")
        elif response.status_code == 200:
            print("⚠️  Modul öffentlich zugänglich (möglicherweise Lead-Magnet)")
        else:
            print(f"❌ Unerwarteter Status: {response.status_code}")
            
        # Zeige Location Header bei Redirect
        if 'Location' in response.headers:
            print(f"🔄 Redirect zu: {response.headers['Location']}")
            
    except Exception as e:
        print(f"❌ Fehler: {e}")
    
    print("\n🌐 Direkt-URL: http://localhost:5000/module/magic-line")
    print("🔑 Login als admin/admin für Zugriff")

if __name__ == '__main__':
    test_magic_line()

