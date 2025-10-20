#!/usr/bin/env python3
"""
Database Init + Auto-Register Templates
1. Erstellt Tabellen
2. Registriert automatisch alle HTML-Templates als Module
"""

from app import app, db
from pathlib import Path
import re

def init_tables():
    """Erstellt alle Tabellen falls sie nicht existieren"""
    with app.app_context():
        print("[DATABASE] Erstelle Tabellen falls nicht vorhanden...")
        db.create_all()
        print("[DATABASE] Tabellen bereit!")

def auto_register_templates():
    """Registriert automatisch alle HTML-Templates als Module"""
    from app import LearningModule, ModuleCategory
    
    with app.app_context():
        # Prüfe ob schon Module existieren
        existing_count = LearningModule.query.count()
        if existing_count > 0:
            print(f"[INFO] {existing_count} Module bereits in Datenbank - überspringe Auto-Register")
            return
        
        print("[INFO] Keine Module gefunden - starte Auto-Register...")
        
        # Scanne templates/ Ordner
        templates_dir = Path(__file__).parent / 'templates'
        html_files = list(templates_dir.glob('*.html'))
        
        # Filtere unwichtige Templates
        exclude = ['base.html', 'home.html', 'modules_overview.html', 'module_default.html', 
                   'upgrade_required.html', '_navigation.html']
        
        registered = 0
        for html_file in html_files:
            if html_file.name in exclude:
                continue
            
            try:
                # Erstelle Slug aus Dateinamen
                slug = html_file.stem  # z.B. "risikomanagement" aus "risikomanagement.html"
                
                # Prüfe ob bereits existiert
                if LearningModule.query.filter_by(slug=slug).first():
                    continue
                
                # Lese Template um Titel zu extrahieren (optional)
                content = html_file.read_text(encoding='utf-8')
                
                # Versuche Titel zu extrahieren
                title_match = re.search(r'<title>(.*?)</title>', content)
                if title_match:
                    title = title_match.group(1).replace(' - Didis Trading Academy', '').strip()
                else:
                    title = slug.replace('-', ' ').title()
                
                # Standard-Kategorie finden oder erstellen
                category = ModuleCategory.query.first()
                if not category:
                    category = ModuleCategory(
                        name='Uncategorized',
                        slug='uncategorized',
                        icon='📁',
                        sort_order=999,
                        is_active=True
                    )
                    db.session.add(category)
                    db.session.flush()
                
                # Modul erstellen (unveröffentlicht!)
                module = LearningModule(
                    category_id=category.id,
                    title=title,
                    slug=slug,
                    description=f'Auto-registriert aus {html_file.name}',
                    icon='📄',
                    template_file=html_file.name,
                    content_type='html',
                    is_published=False,  # Unveröffentlicht bis Admin es aktiviert!
                    is_lead_magnet=False,
                    required_subscription_levels='["premium", "elite", "masterclass"]',
                    sort_order=999,
                    estimated_duration=30,
                    difficulty_level='beginner'
                )
                db.session.add(module)
                registered += 1
                
            except Exception as e:
                print(f"[WARN] Fehler bei {html_file.name}: {e}")
                continue
        
        db.session.commit()
        print(f"[SUCCESS] {registered} Templates automatisch registriert!")

if __name__ == '__main__':
    init_tables()
    auto_register_templates()

