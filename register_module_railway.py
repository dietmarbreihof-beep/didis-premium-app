#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Module Registration Script für Railway
Minimale Dependencies - kann direkt auf Railway ausgeführt werden
"""

import os
import sys

# Füge Parent-Directory zum Python-Path hinzu
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def register_trading_archetypen():
    """Registriert das Trading-Archetypen Modul"""
    try:
        from app import app, db, LearningModule, ModuleCategory
        from datetime import datetime
        import json

        with app.app_context():
            print("🚀 Starte Modul-Registrierung...")

            # 1. Prüfe ob Modul bereits existiert
            existing = LearningModule.query.filter_by(slug='trading-archetypen').first()
            if existing:
                print(f"✅ Modul existiert bereits!")
                print(f"   ID: {existing.id}")
                print(f"   Titel: {existing.title}")
                print(f"   Template: {existing.template_file}")
                print(f"   Published: {existing.is_published}")
                return True

            # 2. Finde oder erstelle Kategorie
            category = ModuleCategory.query.filter_by(slug='trading-strategien').first()

            if not category:
                print("📁 Erstelle Kategorie 'Trading-Strategien'...")
                category = ModuleCategory(
                    name='1. Trading-Strategien',
                    slug='trading-strategien',
                    icon='🎯',
                    description='Grundlegende und fortgeschrittene Trading-Methoden und -Strategien',
                    sort_order=1,
                    is_active=True
                )
                db.session.add(category)
                db.session.flush()
                print(f"✅ Kategorie erstellt: {category.name}")
            else:
                print(f"✅ Kategorie gefunden: {category.name}")

            # 3. Erstelle Modul
            print("📚 Erstelle Modul 'Trading-Archetypen'...")
            module = LearningModule(
                category_id=category.id,
                subcategory_id=None,
                title='Trading-Methoden Vertiefung',
                slug='trading-archetypen',
                description='Verstehe die drei Säulen erfolgreichen Tradings: Buy & Hold, Position Trading und Swing Trading. Lerne den Keulen-Kombi-Prozess und finde deinen systematischen Edge.',
                icon='🎯',
                template_file='trading_archetypen.html',
                content_type='html',
                is_published=True,
                is_lead_magnet=False,
                required_subscription_levels=json.dumps(["premium", "elite", "masterclass"]),
                estimated_duration=25,
                difficulty_level='intermediate',
                sort_order=100,
                view_count=0,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            db.session.add(module)
            db.session.commit()

            print("\n" + "="*60)
            print("✅ MODUL ERFOLGREICH REGISTRIERT!")
            print("="*60)
            print(f"ID:           {module.id}")
            print(f"Titel:        {module.title}")
            print(f"Slug:         {module.slug}")
            print(f"Template:     {module.template_file}")
            print(f"Kategorie:    {category.name}")
            print(f"Published:    {module.is_published}")
            print(f"Difficulty:   {module.difficulty_level}")
            print(f"Duration:     {module.estimated_duration} min")
            print("="*60)
            print(f"\n🌐 URL: /module/{module.slug}")
            print(f"🌐 Full URL: https://didis-premium-app-production.up.railway.app/module/{module.slug}\n")

            return True

    except Exception as e:
        print(f"\n❌ FEHLER: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = register_trading_archetypen()
    sys.exit(0 if success else 1)
