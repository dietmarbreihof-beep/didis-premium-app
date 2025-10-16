#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migration: Registriert das Defining Trend Modul
Datum: 2025-10-16
Zweck: Fügt das neue interaktive Defining Trend Modul zur Datenbank hinzu
"""

import sys
import os
import io

# Windows encoding fix
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Füge Parent-Directory zum Python-Path hinzu
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, LearningModule, ModuleCategory

def register_defining_trend():
    """📦 Registriert das Defining Trend Modul in der Datenbank"""
    
    with app.app_context():
        print("\n" + "="*70)
        print("📈 REGISTRIERUNG: DEFINING TREND MODUL")
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
            existing = LearningModule.query.filter_by(template_file='defining-trend.html').first()
            
            if existing:
                print("\n⚠️ Modul existiert bereits:")
                print(f"   📌 ID: {existing.id}")
                print(f"   📝 Titel: {existing.title}")
                print(f"   📁 Kategorie: {existing.category.name}")
                print(f"   📄 Template: {existing.template_file}")
                print("\n💡 Aktualisiere Modul-Daten...")
                
                # Update existing module
                existing.title = "Defining Trend - Die Kunst der Trend-Erkennung"
                existing.slug = "defining-trend"
                existing.description = "Lerne von Lance Breitenstein, wie du Trends richtig definierst, erkennst und nutzt. Mit interaktivem Quiz, Homework Assignments und echten Trading-Beispielen."
                existing.icon = "📈"
                existing.difficulty_level = "intermediate"
                existing.estimated_duration = 45
                existing.is_published = True
                existing.required_subscription_levels = ["premium", "elite"]
                
                print("   ✅ Modul aktualisiert!")
                
            else:
                print("\n📝 Erstelle neues Modul...")
                
                # Erstelle neues Modul
                new_module = LearningModule(
                    title="Defining Trend - Die Kunst der Trend-Erkennung",
                    slug="defining-trend",
                    description="Lerne von Lance Breitenstein, wie du Trends richtig definierst, erkennst und nutzt. Mit interaktivem Quiz, Homework Assignments und echten Trading-Beispielen.",
                    icon="📈",
                    template_file="defining-trend.html",
                    category_id=neue_module_cat.id,
                    difficulty_level="intermediate",
                    estimated_duration=45,
                    sort_order=1,
                    is_published=True,
                    required_subscription_levels=["premium", "elite"],
                    content_type="html",
                    created_at=datetime.now()
                )
                
                db.session.add(new_module)
                print("   ✅ Neues Modul erstellt!")
            
            db.session.commit()
            
            # Zeige finales Modul
            final_module = LearningModule.query.filter_by(template_file='defining-trend.html').first()
            
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
            print(f"💎 Subscription:    {', '.join(final_module.required_subscription_levels)}")
            print("="*70)
            
            print("\n🎯 MODUL-FEATURES:")
            print("   📈 7 interaktive Sektionen über Trend-Definition")
            print("   🧠 6-Fragen Quiz mit sofortiger Auswertung")
            print("   📝 4 Homework Assignments mit Progress Tracking")
            print("   📋 12 Key Takeaways aus Lance's Material")
            print("   💾 Persistenter Progress via LocalStorage")
            print("   🎨 Premium Design nach Gold/Dunkelgrau Standards")
            
            print("\n🌐 VERFÜGBAR UNTER:")
            print(f"   Local:   http://localhost:5000/module/{final_module.slug}")
            print(f"   Railway: https://your-app.railway.app/module/{final_module.slug}")
            
            print("\n💡 NÄCHSTE SCHRITTE:")
            print("   1. Öffne das Admin-Panel: /admin/modules")
            print("   2. Verschiebe Modul in passende Kategorie (z.B. 'Trading-Psychologie' oder 'Technische Analyse')")
            print("   3. Passe bei Bedarf Sortierung und weitere Details an")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Migration fehlgeschlagen: {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == '__main__':
    from datetime import datetime
    
    try:
        success = register_defining_trend()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️ Migration durch Benutzer abgebrochen")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unerwarteter Fehler: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

