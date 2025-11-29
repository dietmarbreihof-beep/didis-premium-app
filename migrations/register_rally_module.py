"""
Migrations-Script: Registrierung des Moduls "Eine Rally für jede Jahreszeit"

Dieses Modul erklärt saisonale Börsenperformance und widerlegt den Mythos der "Sommer-Rally".

Kategorie: Marktanalyse → Marktzyklen & Timing
Level: FREE (Lead-Magnet)
"""

import sys
import os

# Füge Projektverzeichnis zum Python-Path hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db, LearningModule, ModuleCategory, ModuleSubcategory

def register_rally_module():
    """Registriert das Modul 'Eine Rally für jede Jahreszeit' in der Datenbank"""
    
    with app.app_context():
        print("🚀 Starte Registrierung: Eine Rally für jede Jahreszeit")
        
        # Hole oder erstelle Hauptkategorie "Marktanalyse"
        category = ModuleCategory.query.filter_by(name='Marktanalyse').first()
        if not category:
            print("📁 Erstelle neue Hauptkategorie: Marktanalyse")
            category = ModuleCategory(
                name='Marktanalyse',
                description='Verstehe Märkte, Trends und makroökonomische Zusammenhänge',
                icon='📊',
                sort_order=3
            )
            db.session.add(category)
            db.session.flush()
        
        # Hole oder erstelle Unterkategorie "Marktzyklen & Timing"
        subcategory = ModuleSubcategory.query.filter_by(
            name='Marktzyklen & Timing',
            category_id=category.id
        ).first()
        
        if not subcategory:
            print("📂 Erstelle neue Unterkategorie: Marktzyklen & Timing")
            subcategory = ModuleSubcategory(
                name='Marktzyklen & Timing',
                description='Saisonale Muster, Marktzyklen und optimales Timing',
                category_id=category.id,
                sort_order=2
            )
            db.session.add(subcategory)
            db.session.flush()
        
        # Prüfe ob Modul bereits existiert
        existing_module = LearningModule.query.filter_by(
            slug='eine-rally-fuer-jede-jahreszeit'
        ).first()
        
        if existing_module:
            print(f"⚠️  Modul existiert bereits (ID: {existing_module.id})")
            print("📝 Aktualisiere Modul-Daten...")
            
            # Aktualisiere bestehende Daten
            existing_module.title = 'Eine Rally für jede Jahreszeit'
            existing_module.description = 'Warum die Börse nicht nur im Sommer steigt - Fakten über saisonale Performance'
            existing_module.content = '''
            <p>Viele Anleger glauben an die "Sommer-Rally" als beste Zeit für Aktiengewinne. 
            Doch die Daten zeigen ein anderes Bild!</p>
            <ul>
                <li>❄️ <strong>Winter:</strong> 13,0% durchschnittliche Performance (Beste Saison)</li>
                <li>🌸 <strong>Frühling:</strong> 11,7% (Zweitbeste Saison)</li>
                <li>🍂 <strong>Herbst:</strong> 11,2% (Drittbeste Saison)</li>
                <li>☀️ <strong>Sommer:</strong> 9,4% (Schwächste Saison!)</li>
            </ul>
            <p>Lerne, wie du saisonale Muster richtig interpretierst und nutzt.</p>
            '''
            existing_module.category_id = category.id
            existing_module.subcategory_id = subcategory.id
            existing_module.level = 'free'
            existing_module.duration_minutes = 20
            existing_module.sort_order = 20
            existing_module.is_published = True
            existing_module.is_interactive = True
            existing_module.template_file = 'eine-rally-fuer-jede-jahreszeit.html'
            existing_module.premium_required = False
            
            print("✅ Modul erfolgreich aktualisiert!")
        
        else:
            print("📄 Erstelle neues Modul...")
            
            # Erstelle neues Modul
            new_module = LearningModule(
                title='Eine Rally für jede Jahreszeit',
                slug='eine-rally-fuer-jede-jahreszeit',
                description='Warum die Börse nicht nur im Sommer steigt - Fakten über saisonale Performance',
                content='''
                <p>Viele Anleger glauben an die "Sommer-Rally" als beste Zeit für Aktiengewinne. 
                Doch die Daten zeigen ein anderes Bild!</p>
                <ul>
                    <li>❄️ <strong>Winter:</strong> 13,0% durchschnittliche Performance (Beste Saison)</li>
                    <li>🌸 <strong>Frühling:</strong> 11,7% (Zweitbeste Saison)</li>
                    <li>🍂 <strong>Herbst:</strong> 11,2% (Drittbeste Saison)</li>
                    <li>☀️ <strong>Sommer:</strong> 9,4% (Schwächste Saison!)</li>
                </ul>
                <p>Lerne, wie du saisonale Muster richtig interpretierst und nutzt.</p>
                ''',
                category_id=category.id,
                subcategory_id=subcategory.id,
                level='free',
                duration_minutes=20,
                sort_order=20,
                is_published=True,
                is_interactive=True,
                template_file='eine-rally-fuer-jede-jahreszeit.html',
                premium_required=False
            )
            
            db.session.add(new_module)
            print("✅ Neues Modul erstellt!")
        
        # Änderungen speichern
        db.session.commit()
        
        print("\n" + "="*60)
        print("✨ ERFOLGREICH REGISTRIERT!")
        print("="*60)
        print(f"📌 Titel: Eine Rally für jede Jahreszeit")
        print(f"🔗 Slug: eine-rally-fuer-jede-jahreszeit")
        print(f"📁 Kategorie: {category.name}")
        print(f"📂 Unterkategorie: {subcategory.name}")
        print(f"💎 Level: FREE (Lead-Magnet)")
        print(f"⏱️  Dauer: ~20 Minuten")
        print(f"🎯 Route: /eine-rally-fuer-jede-jahreszeit")
        print(f"📄 Template: eine-rally-fuer-jede-jahreszeit.html")
        print("="*60)
        print("\n🎉 Das Modul ist jetzt verfügbar!")
        print("🌐 Teste es unter: http://localhost:5000/eine-rally-fuer-jede-jahreszeit")
        print("☁️  Railway URL: https://didis-premium-app-production.up.railway.app/eine-rally-fuer-jede-jahreszeit")

if __name__ == '__main__':
    try:
        register_rally_module()
    except Exception as e:
        print(f"\n❌ FEHLER bei der Registrierung: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

