#!/usr/bin/env python3
"""
Migration: Demo-Benutzer in Datenbank erstellen
Migriert hart-codierte Demo-Benutzer in die Datenbank mit gehashten Passwörtern
"""

import sys
import os
# Füge Parent-Directory zum Python-Path hinzu
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, User
from werkzeug.security import generate_password_hash

def create_demo_users():
    """Erstellt Demo-Benutzer in der Datenbank"""
    with app.app_context():
        print("\n" + "="*60)
        print("[MIGRATION] Erstelle Demo-Benutzer in Datenbank")
        print("="*60)
        
        demo_users = [
            {
                'username': 'admin',
                'email': 'admin@didis-academy.com',
                'password': 'admin',  # Wird gehasht
                'first_name': 'Admin',
                'last_name': 'User',
                'is_active': True,
                'email_verified': True
            },
            {
                'username': 'didi',
                'email': 'didi@didis-academy.com',
                'password': 'didi',  # Wird gehasht
                'first_name': 'Dietmar',
                'last_name': 'Breihof',
                'is_active': True,
                'email_verified': True
            },
            {
                'username': 'premium',
                'email': 'premium@didis-academy.com',
                'password': 'premium',  # Wird gehasht
                'first_name': 'Premium',
                'last_name': 'User',
                'is_active': True,
                'email_verified': True
            },
            {
                'username': 'test',
                'email': 'test@didis-academy.com',
                'password': 'test',  # Wird gehasht
                'first_name': 'Test',
                'last_name': 'User',
                'is_active': True,
                'email_verified': True
            }
        ]
        
        created_count = 0
        updated_count = 0
        
        for user_data in demo_users:
            # Prüfe ob User bereits existiert
            existing_user = User.query.filter_by(username=user_data['username']).first()
            
            if existing_user:
                # Update bestehendem User
                existing_user.set_password(user_data['password'])
                existing_user.email = user_data['email']
                existing_user.first_name = user_data['first_name']
                existing_user.last_name = user_data['last_name']
                existing_user.is_active = user_data['is_active']
                existing_user.email_verified = user_data['email_verified']
                updated_count += 1
                print(f"   [UPDATE] {user_data['username']}")
            else:
                # Erstelle neuen User
                user = User(
                    username=user_data['username'],
                    email=user_data['email'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    is_active=user_data['is_active'],
                    email_verified=user_data['email_verified']
                )
                user.set_password(user_data['password'])
                db.session.add(user)
                created_count += 1
                print(f"   [CREATED] {user_data['username']}")
        
        db.session.commit()
        
        print("="*60)
        print(f"[SUCCESS] Demo-Benutzer Migration abgeschlossen")
        print(f"          - {created_count} neu erstellt")
        print(f"          - {updated_count} aktualisiert")
        print("="*60 + "\n")
        
        print("[INFO] Passwörter wurden sicher gehasht und sind nicht mehr im Klartext!")
        print("[INFO] Demo-User können sich jetzt mit Username/Passwort anmelden")
        
        return created_count + updated_count

if __name__ == '__main__':
    create_demo_users()

