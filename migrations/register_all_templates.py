#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migration: Registriert ALLE HTML-Templates aus dem templates-Ordner
Datum: 2025-10-12
Zweck: Initiale Bulk-Registrierung aller Templates in die Datenbank
"""

import sys
import os

# Füge Parent-Directory zum Python-Path hinzu
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from pathlib import Path

def register_all_templates():
    """📦 Registriert alle HTML-Templates in der Datenbank"""
    
    with app.app_context():
        print("\n" + "="*70)
        print("📦 BULK-REGISTRIERUNG ALLER TEMPLATES")
        print("="*70)
        
        from app import auto_register_modules, sync_modules_from_local
        
        try:
            # 1. Stelle sicher dass alle Kategorien existieren
            print("\n1️⃣ Synchronisiere Kategorien...")
            sync_modules_from_local()
            db.session.commit()
            print("   ✅ Kategorien synchronisiert")
            
            # 2. Registriere alle Templates
            print("\n2️⃣ Scanne alle HTML-Templates...")
            
            templates_dir = Path("templates")
            
            # Ausgeschlossene Dateien
            excluded_patterns = [
                'base.html', 'home.html', 'login.html', 'register.html',
                'modules_overview.html', 'upgrade_required.html', 'module_default.html',
                '_navigation.html', 'Banner5.html', 'app.py'
            ]
            
            excluded_dirs = ['admin', 'auth', 'errors', 'account', 'templates', 'static']
            
            # Finde alle HTML-Templates
            all_templates = []
            for html_file in templates_dir.glob("*.html"):
                if any(pattern in html_file.name for pattern in excluded_patterns):
                    continue
                if any(excluded_dir in str(html_file) for excluded_dir in excluded_dirs):
                    continue
                all_templates.append(html_file.name)
            
            print(f"   📄 {len(all_templates)} Templates gefunden:")
            for template in sorted(all_templates):
                print(f"      • {template}")
            
            # 3. Führe Auto-Registrierung durch
            print("\n3️⃣ Registriere Templates in Datenbank...")
            print("   (Dies kann einen Moment dauern...)")
            
            # Import der benötigten Funktionen
            from app import (
                LearningModule, ModuleCategory, 
                extract_module_metadata, create_auto_module
            )
            
            registered_count = 0
            skipped_count = 0
            error_count = 0
            
            # Hole "Neue Module" Kategorie
            neue_module_cat = ModuleCategory.query.filter_by(slug='neue-module').first()
            
            if not neue_module_cat:
                print("   ⚠️ 'Neue Module' Kategorie nicht gefunden - erstelle sie...")
                neue_module_cat = ModuleCategory(
                    name='🆕 Neue Module',
                    slug='neue-module',
                    icon='🆕',
                    description='Automatisch erkannte Module - Bitte in die richtige Kategorie verschieben',
                    sort_order=999,
                    is_active=True
                )
                db.session.add(neue_module_cat)
                db.session.flush()
            
            # Registriere jedes Template
            for html_file in templates_dir.glob("*.html"):
                if any(pattern in html_file.name for pattern in excluded_patterns):
                    continue
                if any(excluded_dir in str(html_file) for excluded_dir in excluded_dirs):
                    continue
                
                try:
                    # Prüfe ob bereits registriert
                    existing = LearningModule.query.filter_by(template_file=html_file.name).first()
                    
                    if existing:
                        print(f"   ⏭️  Übersprungen (existiert): {html_file.name}")
                        skipped_count += 1
                        continue
                    
                    # Extrahiere Metadaten
                    module_info = extract_module_metadata(html_file)
                    
                    # Speichere Kategorie-Vorschlag
                    suggested_category = module_info.get('category', 'technische-analyse')
                    module_info['description'] += f" [Vorschlag: {suggested_category}]"
                    
                    # Erstelle Modul in "Neue Module" Kategorie
                    create_auto_module(html_file, module_info, neue_module_cat)
                    registered_count += 1
                    
                    print(f"   ✅ Registriert: {module_info['title']}")
                    
                except Exception as e:
                    print(f"   ❌ Fehler bei {html_file.name}: {str(e)}")
                    error_count += 1
            
            db.session.commit()
            
            # 4. Zusammenfassung
            print("\n" + "="*70)
            print("📊 ZUSAMMENFASSUNG")
            print("="*70)
            print(f"   ✅ Neu registriert:  {registered_count}")
            print(f"   ⏭️  Übersprungen:     {skipped_count}")
            print(f"   ❌ Fehler:           {error_count}")
            print(f"   📦 Gesamt Templates: {len(all_templates)}")
            print("="*70)
            
            if registered_count > 0:
                print("\n🎯 NÄCHSTE SCHRITTE:")
                print("   1. Öffne das Admin-Panel: http://localhost:5000/admin/modules")
                print("   2. Gehe zur Kategorie '🆕 Neue Module'")
                print("   3. Verschiebe Module in die richtigen Kategorien")
                print("   4. Passe Titel, Beschreibungen und Icons an")
                print("   5. Veröffentliche die Module (is_published = True)")
            
            print("\n✅ Migration erfolgreich abgeschlossen!")
            return True
            
        except Exception as e:
            print(f"\n❌ Migration fehlgeschlagen: {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == '__main__':
    try:
        success = register_all_templates()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️ Migration durch Benutzer abgebrochen")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unerwarteter Fehler: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

