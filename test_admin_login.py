#!/usr/bin/env python3
"""Test ob admin/admin Login funktioniert"""

from app import app, db, User

with app.app_context():
    admin = User.query.filter_by(username='admin').first()
    
    if not admin:
        print("[FAIL] Admin-User nicht gefunden!")
        print(f"Verfuegbare User: {[u.username for u in User.query.all()]}")
    else:
        print(f"[OK] Admin-User gefunden: {admin.username}")
        print(f"     Email: {admin.email}")
        print(f"     Aktiv: {admin.is_active}")
        
        # Teste Passwort
        password_ok = admin.check_password('admin')
        print(f"     Passwort-Test 'admin': {'OK' if password_ok else 'FALSCH'}")
        
        if password_ok:
            print("\n[SUCCESS] admin/admin Login sollte funktionieren!")
        else:
            print("\n[FAIL] Passwort stimmt nicht!")

