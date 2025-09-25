#!/usr/bin/env python3
"""
Migrations-Script für Lernmodule
Migriert Streamlit-Apps und HTML-Templates in die Didis Premium Trading Academy
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Flask-App importieren
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app, db, LearningModule, ModuleCategory, ModuleSubcategory

class ModuleMigrator:
    def __init__(self):
        self.migrated_count = 0
        self.errors = []
        
    def migrate_streamlit_modules(self, streamlit_dir, category_slug="technische-analyse"):
        """
        Migriert Streamlit-Module aus einem Verzeichnis
        
        Args:
            streamlit_dir (str): Pfad zum Streamlit-Module-Verzeichnis
            category_slug (str): Ziel-Kategorie in der Flask-App
        """
        print(f"🔄 Migriere Streamlit-Module aus: {streamlit_dir}")
        
        streamlit_path = Path(streamlit_dir)
        if not streamlit_path.exists():
            print(f"❌ Verzeichnis nicht gefunden: {streamlit_dir}")
            return
            
        # Kategorie finden
        category = ModuleCategory.query.filter_by(slug=category_slug).first()
        if not category:
            print(f"❌ Kategorie nicht gefunden: {category_slug}")
            return
            
        # Streamlit-Dateien finden
        streamlit_files = list(streamlit_path.glob("*.py"))
        
        for file_path in streamlit_files:
            try:
                self._migrate_single_streamlit(file_path, category)
            except Exception as e:
                error_msg = f"Fehler bei {file_path.name}: {str(e)}"
                self.errors.append(error_msg)
                print(f"❌ {error_msg}")
                
        print(f"✅ {self.migrated_count} Streamlit-Module migriert")
        
    def _migrate_single_streamlit(self, file_path, category):
        """Migriert eine einzelne Streamlit-Datei"""
        file_name = file_path.stem
        
        # Modul-Info aus Dateiname extrahieren
        title = file_name.replace("_", " ").replace("-", " ").title()
        slug = file_name.lower().replace("_", "-")
        
        # Prüfen ob bereits vorhanden
        existing = LearningModule.query.filter_by(slug=slug).first()
        if existing:
            print(f"⏭️  Modul bereits vorhanden: {title}")
            return
            
        # Streamlit-URL generieren (angenommen Port 8501)
        streamlit_url = f"http://localhost:8501/{file_name}"
        
        # Neues Modul erstellen
        module = LearningModule(
            category_id=category.id,
            title=title,
            slug=slug,
            description=f"Interaktives Lernmodul: {title}",
            icon="📊",
            content_type="streamlit",
            external_url=streamlit_url,
            is_published=True,
            required_subscription_levels=['premium', 'elite'],
            estimated_duration=60,
            difficulty_level='intermediate',
            sort_order=100 + self.migrated_count
        )
        
        db.session.add(module)
        db.session.commit()
        
        self.migrated_count += 1
        print(f"✅ Migriert: {title} -> {streamlit_url}")
        
    def migrate_html_modules(self, html_dir, category_slug="technische-analyse"):
        """
        Migriert HTML-Templates aus einem Verzeichnis
        
        Args:
            html_dir (str): Pfad zum HTML-Templates-Verzeichnis
            category_slug (str): Ziel-Kategorie in der Flask-App
        """
        print(f"🔄 Migriere HTML-Module aus: {html_dir}")
        
        html_path = Path(html_dir)
        if not html_path.exists():
            print(f"❌ Verzeichnis nicht gefunden: {html_dir}")
            return
            
        # Kategorie finden
        category = ModuleCategory.query.filter_by(slug=category_slug).first()
        if not category:
            print(f"❌ Kategorie nicht gefunden: {category_slug}")
            return
            
        # HTML-Dateien finden
        html_files = list(html_path.glob("*.html"))
        
        for file_path in html_files:
            try:
                self._migrate_single_html(file_path, category)
            except Exception as e:
                error_msg = f"Fehler bei {file_path.name}: {str(e)}"
                self.errors.append(error_msg)
                print(f"❌ {error_msg}")
                
        print(f"✅ {self.migrated_count} HTML-Module migriert")
        
    def _migrate_single_html(self, file_path, category):
        """Migriert eine einzelne HTML-Datei"""
        file_name = file_path.stem
        
        # Modul-Info aus Dateiname extrahieren
        title = file_name.replace("_", " ").replace("-", " ").title()
        slug = file_name.lower().replace("_", "-")
        
        # Prüfen ob bereits vorhanden
        existing = LearningModule.query.filter_by(slug=slug).first()
        if existing:
            print(f"⏭️  Modul bereits vorhanden: {title}")
            return
            
        # HTML-Template in templates/ kopieren
        templates_dir = Path("templates")
        templates_dir.mkdir(exist_ok=True)
        
        target_path = templates_dir / file_path.name
        if not target_path.exists():
            import shutil
            shutil.copy2(file_path, target_path)
            print(f"📁 Template kopiert: {file_path.name}")
        
        # Neues Modul erstellen
        module = LearningModule(
            category_id=category.id,
            title=title,
            slug=slug,
            description=f"HTML-Lernmodul: {title}",
            icon="📄",
            content_type="html",
            template_file=file_path.name,
            is_published=True,
            required_subscription_levels=['premium', 'elite'],
            estimated_duration=45,
            difficulty_level='intermediate',
            sort_order=100 + self.migrated_count
        )
        
        db.session.add(module)
        db.session.commit()
        
        self.migrated_count += 1
        print(f"✅ Migriert: {title} -> {file_path.name}")
        
    def migrate_from_config(self, config_file):
        """
        Migriert Module basierend auf einer JSON-Konfigurationsdatei
        
        config_file Format:
        {
            "modules": [
                {
                    "title": "Modul-Titel",
                    "slug": "modul-slug",
                    "description": "Beschreibung",
                    "category": "technische-analyse",
                    "content_type": "streamlit|html",
                    "external_url": "http://localhost:8501/app",
                    "template_file": "template.html",
                    "required_subscription_levels": ["premium", "elite"],
                    "is_lead_magnet": false
                }
            ]
        }
        """
        print(f"🔄 Migriere Module aus Konfiguration: {config_file}")
        
        config_path = Path(config_file)
        if not config_path.exists():
            print(f"❌ Konfigurationsdatei nicht gefunden: {config_file}")
            return
            
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        for module_data in config.get('modules', []):
            try:
                self._migrate_from_config_data(module_data)
            except Exception as e:
                error_msg = f"Fehler bei {module_data.get('title', 'Unbekannt')}: {str(e)}"
                self.errors.append(error_msg)
                print(f"❌ {error_msg}")
                
        print(f"✅ {self.migrated_count} Module aus Konfiguration migriert")
        
    def _migrate_from_config_data(self, module_data):
        """Migriert ein Modul basierend auf Konfigurationsdaten"""
        slug = module_data['slug']
        
        # Prüfen ob bereits vorhanden
        existing = LearningModule.query.filter_by(slug=slug).first()
        if existing:
            print(f"⏭️  Modul bereits vorhanden: {module_data['title']}")
            return
            
        # Kategorie finden
        category = ModuleCategory.query.filter_by(slug=module_data['category']).first()
        if not category:
            print(f"❌ Kategorie nicht gefunden: {module_data['category']}")
            return
            
        # Neues Modul erstellen
        module = LearningModule(
            category_id=category.id,
            title=module_data['title'],
            slug=slug,
            description=module_data.get('description', ''),
            icon=module_data.get('icon', '📊'),
            content_type=module_data.get('content_type', 'html'),
            external_url=module_data.get('external_url'),
            template_file=module_data.get('template_file'),
            is_published=module_data.get('is_published', True),
            is_lead_magnet=module_data.get('is_lead_magnet', False),
            required_subscription_levels=module_data.get('required_subscription_levels', ['premium', 'elite']),
            estimated_duration=module_data.get('estimated_duration', 60),
            difficulty_level=module_data.get('difficulty_level', 'intermediate'),
            sort_order=module_data.get('sort_order', 100 + self.migrated_count)
        )
        
        db.session.add(module)
        db.session.commit()
        
        self.migrated_count += 1
        print(f"✅ Migriert: {module_data['title']}")
        
    def print_summary(self):
        """Zeigt Migrations-Zusammenfassung"""
        print("\n" + "="*50)
        print("📊 MIGRATIONS-ZUSAMMENFASSUNG")
        print("="*50)
        print(f"✅ Erfolgreich migriert: {self.migrated_count} Module")
        print(f"❌ Fehler: {len(self.errors)}")
        
        if self.errors:
            print("\n🚨 FEHLER:")
            for error in self.errors:
                print(f"   - {error}")
                
        print("\n🎯 NÄCHSTE SCHRITTE:")
        print("1. Flask-App starten: python app.py")
        print("2. Admin-Panel öffnen: http://localhost:5000/admin/modules")
        print("3. Module überprüfen und anpassen")
        print("4. Bei Streamlit-Modulen: Streamlit-Apps parallel starten")

def main():
    """Hauptfunktion für CLI-Nutzung"""
    migrator = ModuleMigrator()
    
    if len(sys.argv) < 2:
        print("""
🚀 Didis Premium Trading Academy - Modul-Migration

Verwendung:
    python migrate_modules.py streamlit <verzeichnis> [kategorie]
    python migrate_modules.py html <verzeichnis> [kategorie]  
    python migrate_modules.py config <config.json>

Beispiele:
    python migrate_modules.py streamlit ./streamlit_modules technische-analyse
    python migrate_modules.py html ./html_templates fundamentalanalyse
    python migrate_modules.py config modules_config.json

Verfügbare Kategorien:
    - fundamentalanalyse
    - technische-analyse  
    - risikomanagement
    - trading-psychologie
        """)
        return
        
    command = sys.argv[1]
    
    with app.app_context():
        if command == "streamlit":
            streamlit_dir = sys.argv[2] if len(sys.argv) > 2 else "./streamlit_modules"
            category = sys.argv[3] if len(sys.argv) > 3 else "technische-analyse"
            migrator.migrate_streamlit_modules(streamlit_dir, category)
            
        elif command == "html":
            html_dir = sys.argv[2] if len(sys.argv) > 2 else "./html_templates"
            category = sys.argv[3] if len(sys.argv) > 3 else "technische-analyse"
            migrator.migrate_html_modules(html_dir, category)
            
        elif command == "config":
            config_file = sys.argv[2] if len(sys.argv) > 2 else "modules_config.json"
            migrator.migrate_from_config(config_file)
            
        else:
            print(f"❌ Unbekannter Befehl: {command}")
            return
            
        migrator.print_summary()

if __name__ == "__main__":
    main()
