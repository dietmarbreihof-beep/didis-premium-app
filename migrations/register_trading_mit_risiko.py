#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migration Script: Trading mit Risiko - Lead-Magnet Modul
=========================================================

Registriert das "Trading mit Risiko" Modul in der Datenbank.

Features:
- Öffentlich zugänglich (Lead-Magnet)
- Progressive Disclosure mit 6 Sektionen
- Quiz-System mit 3 interaktiven Tests
- Gold-Premium Design-System
- Vollständige Navigation

Verwendung:
    python migrations/register_trading_mit_risiko.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from database import LearningModule, ModuleCategory, ModuleSubcategory

def register_trading_mit_risiko():
    """Registriere Trading mit Risiko Modul in der Datenbank"""
    
    with app.app_context():
        try:
            # 1. Prüfe ob Modul bereits existiert
            existing_module = LearningModule.query.filter_by(
                slug='trading-mit-risiko'
            ).first()
            
            if existing_module:
                print("✅ Modul 'trading-mit-risiko' existiert bereits in der Datenbank.")
                print(f"   Titel: {existing_module.title}")
                print(f"   Kategorie-ID: {existing_module.category_id}")
                return
            
            # 2. Finde oder erstelle Hauptkategorie "Lead-Magnets"
            lead_magnet_category = ModuleCategory.query.filter_by(
                name='Lead-Magnets'
            ).first()
            
            if not lead_magnet_category:
                # Erstelle Lead-Magnet Kategorie
                lead_magnet_category = ModuleCategory(
                    name='Lead-Magnets',
                    description='Öffentlich zugängliche Premium-Inhalte für Marketing',
                    order=99  # Am Ende der Liste
                )
                db.session.add(lead_magnet_category)
                db.session.flush()
                print(f"✅ Kategorie 'Lead-Magnets' erstellt (ID: {lead_magnet_category.id})")
            else:
                print(f"✅ Kategorie 'Lead-Magnets' gefunden (ID: {lead_magnet_category.id})")
            
            # 3. Finde oder erstelle Unterkategorie "Risikomanagement"
            risiko_subcategory = ModuleSubcategory.query.filter_by(
                category_id=lead_magnet_category.id,
                name='Risikomanagement'
            ).first()
            
            if not risiko_subcategory:
                # Erstelle Unterkategorie
                risiko_subcategory = ModuleSubcategory(
                    category_id=lead_magnet_category.id,
                    name='Risikomanagement',
                    description='Wie du mit kalkuliertem Risiko außergewöhnliche Renditen erzielst',
                    order=1
                )
                db.session.add(risiko_subcategory)
                db.session.flush()
                print(f"✅ Unterkategorie 'Risikomanagement' erstellt (ID: {risiko_subcategory.id})")
            else:
                print(f"✅ Unterkategorie 'Risikomanagement' gefunden (ID: {risiko_subcategory.id})")
            
            # 4. Erstelle Modul-Eintrag
            new_module = LearningModule(
                title='Trading mit Risiko: Der Schlüssel zum Reichtum',
                slug='trading-mit-risiko',
                description='Warum du mehr Risiko eingehen musst, um außergewöhnliche Renditen zu erzielen. Die unbequeme Wahrheit über Vermögensaufbau.',
                category_id=lead_magnet_category.id,
                subcategory_id=risiko_subcategory.id,
                template_file='trading-mit-risiko.html',
                required_subscription='free',  # Öffentlich zugänglich
                estimated_time=30,
                difficulty='Anfänger',
                is_published=True,
                sort_order=1
            )
            
            db.session.add(new_module)
            db.session.commit()
            
            print("\n" + "="*70)
            print("✅ MODUL ERFOLGREICH REGISTRIERT!")
            print("="*70)
            print(f"📝 Titel: {new_module.title}")
            print(f"🔗 Slug: {new_module.slug}")
            print(f"📂 Kategorie: {lead_magnet_category.name}")
            print(f"📁 Unterkategorie: {risiko_subcategory.name}")
            print(f"🎯 Template: {new_module.template_file}")
            print(f"💎 Subscription: {new_module.required_subscription} (Öffentlich)")
            print(f"⏱️  Dauer: {new_module.estimated_time} Minuten")
            print(f"⭐ Schwierigkeit: {new_module.difficulty}")
            print(f"✅ Veröffentlicht: {new_module.is_published}")
            print("\n🚀 Features:")
            print("   - Progressive Disclosure (6 Sektionen)")
            print("   - Quiz-System (3 interaktive Tests)")
            print("   - Gold-Premium Design-System")
            print("   - Vollständige Navigation")
            print("   - LocalStorage-basierte Fortschrittsspeicherung")
            print("\n📊 Zugriff:")
            print("   🌐 Route: /trading-mit-risiko")
            print("   🔓 Öffentlich: Ja (Lead-Magnet)")
            print("   🎯 Ziel: Marketing & Conversion")
            print("\n✅ Du kannst das Modul jetzt testen:")
            print("   👉 https://deine-app.railway.app/trading-mit-risiko")
            print("="*70)
            
        except Exception as e:
            print(f"\n❌ FEHLER beim Registrieren des Moduls:")
            print(f"   {str(e)}")
            db.session.rollback()
            import traceback
            traceback.print_exc()
            return False
        
        return True

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚀 MIGRATION: Trading mit Risiko Modul")
    print("="*70)
    print("\n📋 Dieses Script registriert das Lead-Magnet Modul in der Datenbank.\n")
    
    success = register_trading_mit_risiko()
    
    if success:
        print("\n✅ Migration erfolgreich abgeschlossen!")
    else:
        print("\n❌ Migration fehlgeschlagen!")
        sys.exit(1)

