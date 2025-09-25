#!/usr/bin/env python3
"""
Prüfe Magic Line Module in der Database
"""

from app import app, LearningModule

def check_magic_line_modules():
    with app.app_context():
        print("🔍 MAGIC LINE MODULE CHECK")
        print("=" * 40)
        
        # Alle Magic Line Module finden
        magic_modules = LearningModule.query.filter(
            LearningModule.title.contains('Magic Line')
        ).all()
        
        print(f"📊 Gefundene Magic Line Module: {len(magic_modules)}")
        print()
        
        for i, module in enumerate(magic_modules, 1):
            print(f"🎯 Modul {i}:")
            print(f"   Titel: {module.title}")
            print(f"   Slug: {module.slug}")
            print(f"   Content-Type: {module.content_type}")
            print(f"   Template: {module.template_file}")
            print(f"   External URL: {module.external_url}")
            print(f"   Published: {module.is_published}")
            print(f"   Required Levels: {module.required_subscription_levels}")
            print()
        
        # Prüfe HTML-Template
        try:
            import os
            template_path = os.path.join('templates', 'magic_line.html')
            if os.path.exists(template_path):
                print("✅ magic_line.html Template existiert")
            else:
                print("❌ magic_line.html Template NICHT gefunden")
        except Exception as e:
            print(f"⚠️  Template-Check Fehler: {e}")

if __name__ == '__main__':
    check_magic_line_modules()

