"""
Migrations-Script: Registrierung des Moduls "Die wichtigste Variable im Trading"

Dieses Modul erklärt, warum Breaking News die wichtigste Variable im Trading ist.

Kategorie: Trading-Konzepte → Grundlagen
Level: Premium/Elite
"""

import sys
import os

# Füge Projektverzeichnis zum Python-Path hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db, LearningModule, ModuleCategory, ModuleSubcategory

def register_wichtigste_variable():
    """Registriert das Modul 'Die wichtigste Variable im Trading' in der Datenbank"""
    
    with app.app_context():
        print("🚀 Starte Registrierung: Die wichtigste Variable im Trading")
        
        # Hole oder erstelle Hauptkategorie "Trading-Konzepte"
        category = ModuleCategory.query.filter_by(slug='trading-konzepte').first()
        if not category:
            print("📁 Erstelle neue Hauptkategorie: Trading-Konzepte")
            category = ModuleCategory(
                name='5. Trading Konzepte',
                slug='trading-konzepte',
                description='Fundamentale Trading-Konzepte und Frameworks',
                icon='🎯',
                sort_order=5
            )
            db.session.add(category)
            db.session.flush()
        
        # Hole oder erstelle Unterkategorie "Grundlagen" (oder direkte Kategorie-Zuordnung)
        subcategory = None
        # Optional: Falls Unterkategorien gewünscht sind
        # subcategory = ModuleSubcategory.query.filter_by(
        #     name='Grundlagen',
        #     category_id=category.id
        # ).first()
        
        # if not subcategory:
        #     print("📂 Erstelle neue Unterkategorie: Grundlagen")
        #     subcategory = ModuleSubcategory(
        #         name='Grundlagen',
        #         slug='grundlagen',
        #         description='Fundamentale Trading-Konzepte',
        #         category_id=category.id,
        #         sort_order=1
        #     )
        #     db.session.add(subcategory)
        #     db.session.flush()
        
        # Prüfe ob Modul bereits existiert
        existing_module = LearningModule.query.filter_by(
            slug='wichtigste-variable-trading'
        ).first()
        
        if existing_module:
            print(f"⚠️  Modul existiert bereits (ID: {existing_module.id})")
            print("📝 Aktualisiere Modul-Daten...")
            
            # Aktualisiere bestehende Daten
            existing_module.title = 'Die wichtigste Variable im Trading'
            existing_module.description = 'Breaking News als Fundament für erfolgreiche Trading-Strategien'
            existing_module.content = '''
            <p>Breaking News ist die wichtigste Variable im Trading. Sie bestimmt, ob eine Aktie trendet oder mean revertet.</p>
            <ul>
                <li>📈 <strong>MIT Breaking News:</strong> Bewegungen trenden weitaus wahrscheinlicher → Continuation-Strategien</li>
                <li>⚠️ <strong>OHNE Breaking News:</strong> Bewegungen mean revertieren → Mean Reversion-Strategien</li>
                <li>🎯 <strong>Best Expected Value:</strong> Früh bei Breaking News sein oder Mean Reversion bei Emotions-basierten Moves</li>
            </ul>
            '''
            existing_module.category_id = category.id
            existing_module.subcategory_id = subcategory.id if subcategory else None
            existing_module.level = 'premium'
            existing_module.duration_minutes = 30
            existing_module.sort_order = 10
            existing_module.is_published = True
            existing_module.is_interactive = True
            existing_module.template_file = 'wichtigste-variable-trading.html'
            existing_module.premium_required = True
            
            print("✅ Modul erfolgreich aktualisiert!")
        
        else:
            print("📄 Erstelle neues Modul...")
            
            # Erstelle neues Modul
            new_module = LearningModule(
                title='Die wichtigste Variable im Trading',
                slug='wichtigste-variable-trading',
                description='Breaking News als Fundament für erfolgreiche Trading-Strategien',
                content='''
                <p>Breaking News ist die wichtigste Variable im Trading. Sie bestimmt, ob eine Aktie trendet oder mean revertet.</p>
                <ul>
                    <li>📈 <strong>MIT Breaking News:</strong> Bewegungen trenden weitaus wahrscheinlicher → Continuation-Strategien</li>
                    <li>⚠️ <strong>OHNE Breaking News:</strong> Bewegungen mean revertieren → Mean Reversion-Strategien</li>
                    <li>🎯 <strong>Best Expected Value:</strong> Früh bei Breaking News sein oder Mean Reversion bei Emotions-basierten Moves</li>
                </ul>
                ''',
                category_id=category.id,
                subcategory_id=subcategory.id if subcategory else None,
                level='premium',
                duration_minutes=30,
                sort_order=10,
                is_published=True,
                is_interactive=True,
                template_file='wichtigste-variable-trading.html',
                premium_required=True
            )
            
            db.session.add(new_module)
            print("✅ Neues Modul erstellt!")
        
        # Änderungen speichern
        db.session.commit()
        
        print("\n" + "="*60)
        print("✨ ERFOLGREICH REGISTRIERT!")
        print("="*60)
        print(f"📌 Titel: Die wichtigste Variable im Trading")
        print(f"🔗 Slug: wichtigste-variable-trading")
        print(f"📁 Kategorie: {category.name}")
        print(f"📂 Unterkategorie: {subcategory.name if subcategory else 'Keine (direkte Kategorie)'}")
        print(f"💎 Level: Premium/Elite")
        print(f"⏱️  Dauer: ~30 Minuten")
        print(f"🎯 Route: /wichtigste-variable-trading")
        print(f"📄 Template: wichtigste-variable-trading.html")
        print("="*60)
        print("\n🎉 Das Modul ist jetzt verfügbar!")
        print("🌐 Teste es unter: http://localhost:5000/wichtigste-variable-trading")
        print("☁️  Railway URL: https://didis-premium-app-production.up.railway.app/wichtigste-variable-trading")

if __name__ == '__main__':
    try:
        register_wichtigste_variable()
    except Exception as e:
        print(f"\n❌ FEHLER bei der Registrierung: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

