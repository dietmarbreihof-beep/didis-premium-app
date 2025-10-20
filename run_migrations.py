#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Führt alle ausstehenden Migrationen aus
Wird automatisch beim Railway-Deployment ausgeführt
"""

import sys
import os

def run_all_migrations():
    """Führt alle Migrationen aus"""
    print("=" * 60)
    print("RAILWAY DEPLOYMENT: Starte Migrations")
    print("=" * 60)
    
    # WICHTIG: Import erst HIER um zirkuläre Imports zu vermeiden
    from app import app, db
    
    # WICHTIG: Zuerst Tabellen erstellen falls sie nicht existieren
    with app.app_context():
        try:
            print("\n[DATABASE] Erstelle Tabellen falls nicht vorhanden...")
            db.create_all()
            print("[OK] Datenbank-Tabellen sind bereit!")
        except Exception as e:
            print(f"[ERROR] Fehler beim Erstellen der Tabellen: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    # Migrations NACH db.create_all() importieren
    from migrations.add_symmetrie_module import add_symmetrie_module
    from migrations.register_risikomanagement import register_risikomanagement_module
    from migrations.register_all_core_modules import register_all_core_modules
    
    migrations = [
        ('register_all_core_modules', register_all_core_modules),  # WICHTIG: Zuerst alle Core-Module!
        ('add_symmetrie_module', add_symmetrie_module),
        ('register_risikomanagement_module', register_risikomanagement_module),
        # Weitere Migrationen hier hinzufügen
    ]
    
    failed = []
    succeeded = []
    
    for name, migration_func in migrations:
        print(f"\n>>> Migration: {name}")
        try:
            result = migration_func()
            if result:
                succeeded.append(name)
                print(f"[OK] {name} erfolgreich")
            else:
                failed.append(name)
                print(f"[ERROR] {name} fehlgeschlagen")
        except Exception as e:
            failed.append(name)
            print(f"[ERROR] {name} fehlgeschlagen: {e}")
    
    print("\n" + "=" * 60)
    print(f"Migrations abgeschlossen: {len(succeeded)} erfolgreich, {len(failed)} fehlgeschlagen")
    print("=" * 60)
    
    if failed:
        print("\nFehlgeschlagene Migrationen:")
        for name in failed:
            print(f"  - {name}")
        return False
    
    return True

if __name__ == '__main__':
    success = run_all_migrations()
    sys.exit(0 if success else 1)





