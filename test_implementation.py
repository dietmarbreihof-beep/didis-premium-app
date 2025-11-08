#!/usr/bin/env python3
"""
Test-Script für die Implementierung
Prüft ob alle Änderungen korrekt funktionieren
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, LearningModule, ModuleCategory

def test_secret_key():
    """Test: Secret Key ist persistent"""
    print("\n[TEST] Secret Key Persistenz...")
    secret_key_file = os.path.join(os.path.dirname(__file__), '.secret_key')
    
    if not os.path.exists(secret_key_file):
        print("   [FAIL] .secret_key Datei nicht gefunden")
        return False
    
    with open(secret_key_file, 'r') as f:
        stored_key = f.read().strip()
    
    if len(stored_key) < 32:
        print(f"   [FAIL] Secret Key zu kurz: {len(stored_key)} Zeichen")
        return False
    
    if app.secret_key == stored_key:
        print(f"   [OK] Secret Key persistent ({len(stored_key)} Zeichen)")
        return True
    else:
        print("   [WARNING] Secret Key stimmt nicht mit gespeichertem überein")
        return False

def test_demo_users():
    """Test: Demo-Benutzer in Datenbank"""
    print("\n[TEST] Demo-Benutzer in Datenbank...")
    with app.app_context():
        demo_users = ['admin', 'didi', 'premium', 'test']
        found_users = []
        
        for username in demo_users:
            user = User.query.filter_by(username=username).first()
            if user:
                found_users.append(username)
                # Prüfe ob Passwort gehasht ist
                if user.password_hash.startswith('scrypt:') or user.password_hash.startswith('pbkdf2:'):
                    print(f"   [OK] {username} - Passwort gehasht")
                else:
                    print(f"   [WARNING] {username} - Passwort möglicherweise nicht gehasht")
            else:
                print(f"   [FAIL] {username} - Nicht in Datenbank")
        
        if len(found_users) == len(demo_users):
            print(f"   [OK] Alle {len(demo_users)} Demo-Benutzer gefunden")
            return True
        else:
            print(f"   [FAIL] Nur {len(found_users)}/{len(demo_users)} gefunden")
            return False

def test_module_persistence():
    """Test: Module in Datenbank"""
    print("\n[TEST] Modul-Persistenz...")
    with app.app_context():
        module_count = LearningModule.query.count()
        category_count = ModuleCategory.query.count()
        
        print(f"   [INFO] {category_count} Kategorien gefunden")
        print(f"   [INFO] {module_count} Module gefunden")
        
        if module_count > 0 and category_count > 0:
            print(f"   [OK] Datenbank enthält Module und Kategorien")
            return True
        else:
            print(f"   [WARNING] Datenbank könnte leer sein")
            return False

def test_csrf_protection():
    """Test: CSRF-Schutz aktiviert"""
    print("\n[TEST] CSRF-Schutz...")
    
    try:
        from flask_wtf.csrf import CSRFProtect
        print("   [OK] Flask-WTF installiert")
        
        # Prüfe ob CSRF in app.extensions registriert ist
        if 'csrf' in app.extensions:
            print("   [OK] CSRF-Schutz aktiviert")
            return True
        else:
            print("   [WARNING] CSRF möglicherweise nicht aktiviert")
            return False
    except ImportError:
        print("   [FAIL] Flask-WTF nicht installiert")
        return False

def test_session_config():
    """Test: Session-Konfiguration"""
    print("\n[TEST] Session-Konfiguration...")
    
    configs_to_check = {
        'SESSION_COOKIE_HTTPONLY': True,
        'SESSION_COOKIE_SAMESITE': 'Lax',
        'SESSION_REFRESH_EACH_REQUEST': True
    }
    
    all_ok = True
    for config_key, expected_value in configs_to_check.items():
        actual_value = app.config.get(config_key)
        if actual_value == expected_value:
            print(f"   [OK] {config_key} = {actual_value}")
        else:
            print(f"   [WARNING] {config_key} = {actual_value} (erwartet: {expected_value})")
            all_ok = False
    
    # SESSION_COOKIE_SECURE kann je nach Umgebung unterschiedlich sein
    secure_value = app.config.get('SESSION_COOKIE_SECURE')
    print(f"   [INFO] SESSION_COOKIE_SECURE = {secure_value}")
    
    return all_ok

def test_backup_exists():
    """Test: Backup wurde erstellt"""
    print("\n[TEST] Backup-Datei...")
    
    import glob
    backup_files = glob.glob('backup_modules_*.json')
    
    if backup_files:
        latest_backup = max(backup_files, key=os.path.getmtime)
        file_size = os.path.getsize(latest_backup)
        print(f"   [OK] Backup gefunden: {latest_backup} ({file_size} Bytes)")
        return True
    else:
        print("   [WARNING] Kein Backup gefunden")
        return False

def run_all_tests():
    """Führt alle Tests aus"""
    print("="*60)
    print("TESTING IMPLEMENTATION - App Skalierbarkeit & Persistenz")
    print("="*60)
    
    tests = [
        ("Secret Key Persistenz", test_secret_key),
        ("Demo-Benutzer", test_demo_users),
        ("Modul-Persistenz", test_module_persistence),
        ("CSRF-Schutz", test_csrf_protection),
        ("Session-Konfiguration", test_session_config),
        ("Backup", test_backup_exists)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   [ERROR] {test_name} fehlgeschlagen: {e}")
            results.append((test_name, False))
    
    print("\n" + "="*60)
    print("TEST-ZUSAMMENFASSUNG")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "[OK]" if result else "[FAIL]"
        print(f"   {status} {test_name}")
    
    print("="*60)
    print(f"ERGEBNIS: {passed}/{total} Tests bestanden")
    print("="*60 + "\n")
    
    if passed == total:
        print("[SUCCESS] Alle Tests bestanden!")
        return 0
    else:
        print(f"[WARNING] {total - passed} Test(s) fehlgeschlagen")
        return 1

if __name__ == '__main__':
    sys.exit(run_all_tests())




