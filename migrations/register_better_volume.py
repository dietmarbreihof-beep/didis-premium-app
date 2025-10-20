#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Migration: Register Better Volume Indicator Modul
Erstellt: 2025-10-20
"""

import sys
import os
import io

# Windows encoding fix
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, LearningModule, ModuleCategory
from datetime import datetime

def register_better_volume_module():
    """Registriert das Better Volume Indicator Modul in der Datenbank"""
    
    with app.app_context():
        print("\n" + "="*70)
        print("📊 REGISTRIERUNG: BETTER VOLUME INDICATOR MODUL")
        print("="*70)
        
        try:
            # Hole oder erstelle "Neue Module" Kategorie
            neue_module_cat = ModuleCategory.query.filter_by(slug='neue-module').first()
            
            if not neue_module_cat:
                print("\n⚠️ 'Neue Module' Kategorie nicht gefunden - erstelle sie...")
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
                print("   ✅ Kategorie erstellt")
            
            # Prüfe ob Modul bereits existiert
            existing = LearningModule.query.filter_by(template_file='better-volume-lernseite.html').first()
            
            if existing:
                print("\n⚠️ Modul existiert bereits:")
                print(f"   📌 ID: {existing.id}")
                print(f"   📝 Titel: {existing.title}")
                print(f"   📁 Kategorie: {existing.category.name}")
                print(f"   📄 Template: {existing.template_file}")
                print("\n💡 Aktualisiere Modul-Daten...")
                
                # Update existing module
                existing.title = "Better Volume Indicator Masterclass"
                existing.slug = "better-volume-indicator"
                existing.description = "Erkenne Marktwendepunkte wie die Profis. Lerne die 4 essentiellen Volume-Signale: Climax Up/Down, High Volume Churn und Low Volume. Interaktive 8-Slide-Präsentation mit Quiz und praktischen Beispielen."
                existing.icon = "📊"
                existing.difficulty_level = "beginner"
                existing.estimated_duration = 30
                existing.is_published = True
                existing.is_lead_magnet = True
                existing.required_subscription_levels = []
                
                print("   ✅ Modul aktualisiert!")
                
            else:
                print("\n📝 Erstelle neues Modul...")
                
                # Erstelle neues Modul
                new_module = LearningModule(
                    title="Better Volume Indicator Masterclass",
                    slug="better-volume-indicator",
                    description="Erkenne Marktwendepunkte wie die Profis. Lerne die 4 essentiellen Volume-Signale: Climax Up/Down, High Volume Churn und Low Volume. Interaktive 8-Slide-Präsentation mit Quiz und praktischen Beispielen.",
                    icon="📊",
                    template_file="better-volume-lernseite.html",
                    category_id=neue_module_cat.id,
                    difficulty_level="beginner",
                    estimated_duration=30,
                    sort_order=1,
                    is_published=True,
                    is_lead_magnet=True,
                    required_subscription_levels=[],
                    content_type="html",
                    created_at=datetime.now()
                )
                
                db.session.add(new_module)
                print("   ✅ Neues Modul erstellt!")
            
            db.session.commit()
            
            # Zeige finales Modul
            final_module = LearningModule.query.filter_by(template_file='better-volume-lernseite.html').first()
            
            print("\n" + "="*70)
            print("✅ MODUL ERFOLGREICH REGISTRIERT")
            print("="*70)
            print(f"📌 ID:              {final_module.id}")
            print(f"📝 Titel:           {final_module.title}")
            print(f"🔗 Slug:            {final_module.slug}")
            print(f"📁 Kategorie:       {final_module.category.name}")
            print(f"📄 Template:        {final_module.template_file}")
            print(f"🎯 Schwierigkeit:   {final_module.difficulty_level}")
            print(f"⏱️  Geschätzte Zeit: {final_module.estimated_duration} Minuten")
            print(f"✅ Veröffentlicht:  {final_module.is_published}")
            print(f"🎁 Lead Magnet:     {final_module.is_lead_magnet}")
            print("="*70)
            
            print("\n🎯 MODUL-FEATURES:")
            print("   📊 8 interaktive Slides über Volume-Analyse")
            print("   🧠 7 Quiz-Sektionen mit sofortiger Auswertung")
            print("   📈 4 Volume-Signal-Typen (Climax Up/Down, Churn, Low Volume)")
            print("   🖼️  4 praktische Chart-Screenshots")
            print("   📋 Übersichtstabelle für alle Marktphasen")
            print("   ⚙️  Technisches Setup & Einstellungen")
            print("   💾 Progress-Tracking via LocalStorage")
            print("   🎨 Premium Design mit Gold/Dunkelgrau Standards")
            
            print("\n🌐 VERFÜGBAR UNTER:")
            print(f"   Local:   http://localhost:5000/module/{final_module.slug}")
            print(f"   Railway: https://your-app.railway.app/module/{final_module.slug}")
            
            print("\n💡 NÄCHSTE SCHRITTE:")
            print("   1. Öffne das Admin-Panel: /admin/modules")
            print("   2. Verschiebe Modul in passende Kategorie (z.B. 'Trading-Psychologie' oder 'Lead Magnets')")
            print("   3. Passe bei Bedarf Sortierung und weitere Details an")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Migration fehlgeschlagen: {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == '__main__':
    try:
        success = register_better_volume_module()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️ Migration durch Benutzer abgebrochen")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unerwarteter Fehler: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

