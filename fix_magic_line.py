#!/usr/bin/env python3
"""
Repariere Magic Line Modul - Konvertiere von Streamlit zu HTML
"""

from app import app, LearningModule, db

def fix_magic_line_module():
    with app.app_context():
        print("🔧 MAGIC LINE MODUL REPARATUR")
        print("=" * 40)
        
        # Finde das Streamlit-Modul
        streamlit_module = LearningModule.query.filter_by(
            slug='magic-line-strategie-streamlit'
        ).first()
        
        if streamlit_module:
            print(f"✅ Streamlit-Modul gefunden: {streamlit_module.title}")
            
            # Konvertiere zu HTML-Modul
            print("🔄 Konvertiere zu HTML-Modul...")
            
            streamlit_module.content_type = 'html'
            streamlit_module.template_file = 'magic_line.html'
            streamlit_module.external_url = ''
            streamlit_module.slug = 'magic-line'  # Besserer Slug
            
            # Beschreibung aktualisieren
            streamlit_module.description = 'Meistere die Kunst des perfekten Ein- und Ausstiegs mit Didis bewährter Magic Line Strategie'
            
            db.session.commit()
            
            print("✅ Modul erfolgreich konvertiert!")
            print(f"   Neuer Content-Type: {streamlit_module.content_type}")
            print(f"   Template: {streamlit_module.template_file}")
            print(f"   Slug: {streamlit_module.slug}")
            
            # Test-URL
            print(f"\n🌐 Jetzt erreichbar unter: http://localhost:5000/module/{streamlit_module.slug}")
            
        else:
            print("❌ Streamlit-Modul nicht gefunden")
            
            # Erstelle neues HTML-Modul
            print("🆕 Erstelle neues HTML Magic Line Modul...")
            
            # Finde Technische Analyse Kategorie
            from app import ModuleCategory
            tech_analysis = ModuleCategory.query.filter_by(slug='technische-analyse').first()
            
            if tech_analysis:
                magic_line_module = LearningModule(
                    category_id=tech_analysis.id,
                    title='Magic Line Strategie',
                    slug='magic-line',
                    description='Meistere die Kunst des perfekten Ein- und Ausstiegs mit Didis bewährter Magic Line Strategie',
                    icon='🎯',
                    template_file='magic_line.html',
                    content_type='html',
                    is_published=True,
                    required_subscription_levels=['premium', 'elite'],
                    estimated_duration=120,
                    difficulty_level='advanced',
                    sort_order=1
                )
                
                db.session.add(magic_line_module)
                db.session.commit()
                
                print("✅ Neues HTML-Modul erstellt!")
                print(f"🌐 Erreichbar unter: http://localhost:5000/module/{magic_line_module.slug}")
            else:
                print("❌ Technische Analyse Kategorie nicht gefunden")

if __name__ == '__main__':
    fix_magic_line_module()

