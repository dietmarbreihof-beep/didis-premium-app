#!/usr/bin/env python3
"""
EINFACHES Database-Init Script
Erstellt nur die Tabellen, KEINE Migrations!
Wird einmal beim ersten Start ausgeführt
"""

from app import app, db

def init_tables():
    """Erstellt alle Tabellen falls sie nicht existieren"""
    with app.app_context():
        print("[DATABASE] Erstelle Tabellen falls nicht vorhanden...")
        db.create_all()
        print("[DATABASE] Tabellen bereit!")

if __name__ == '__main__':
    init_tables()

