#!/usr/bin/env python3
"""
Migration: Subscriptions für Demo-Benutzer erstellen
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import alles aus app.py (nutzt die richtige db-Instanz)
from app import app, db, User, Subscription, SubscriptionType
from datetime import datetime, timedelta

def create_demo_subscriptions():
    """Erstellt Subscriptions für Demo-Benutzer"""
    with app.app_context():
        print("\n" + "="*60)
        print("[MIGRATION] Erstelle Subscriptions für Demo-Benutzer")
        print("="*60)
        
        # Demo-User Subscriptions
        demo_subscriptions = {
            'admin': SubscriptionType.ELITE,
            'didi': SubscriptionType.ELITE,
            'premium': SubscriptionType.PREMIUM,
            'test': SubscriptionType.PREMIUM
        }
        
        created_count = 0
        
        for username, subscription_type in demo_subscriptions.items():
            user = User.query.filter_by(username=username).first()
            
            if not user:
                print(f"   [WARNING] User '{username}' nicht gefunden")
                continue
            
            # Prüfe ob bereits Subscription existiert
            existing_sub = Subscription.query.filter_by(user_id=user.id, is_active=True).first()
            
            if existing_sub:
                print(f"   [SKIP] {username} hat bereits Subscription: {existing_sub.subscription_type.value}")
                continue
            
            # Erstelle neue Subscription (1 Jahr gültig)
            subscription = Subscription(
                user_id=user.id,
                subscription_type=subscription_type,
                starts_at=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(days=365),
                is_active=True,
                is_trial=False
            )
            
            db.session.add(subscription)
            created_count += 1
            print(f"   [CREATED] {username} -> {subscription_type.value}")
        
        db.session.commit()
        
        print("="*60)
        print(f"[SUCCESS] {created_count} Subscriptions erstellt")
        print("="*60 + "\n")
        
        return created_count

if __name__ == '__main__':
    create_demo_subscriptions()

