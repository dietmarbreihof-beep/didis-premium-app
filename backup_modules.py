#!/usr/bin/env python3
"""
Backup-Script für Module und Kategorien
Exportiert alle Daten aus der Datenbank in JSON-Format
"""

import json
from datetime import datetime
from app import app, db, LearningModule, ModuleCategory, ModuleSubcategory

def backup_modules():
    """Exportiert alle Module und Kategorien in JSON"""
    with app.app_context():
        backup_data = {
            'backup_date': datetime.utcnow().isoformat(),
            'categories': [],
            'subcategories': [],
            'modules': []
        }
        
        # Kategorien exportieren
        categories = ModuleCategory.query.order_by(ModuleCategory.sort_order).all()
        for cat in categories:
            backup_data['categories'].append({
                'id': cat.id,
                'name': cat.name,
                'slug': cat.slug,
                'icon': cat.icon,
                'description': cat.description,
                'sort_order': cat.sort_order,
                'is_active': cat.is_active
            })
        
        # Unterkategorien exportieren
        subcategories = ModuleSubcategory.query.order_by(ModuleSubcategory.sort_order).all()
        for subcat in subcategories:
            backup_data['subcategories'].append({
                'id': subcat.id,
                'category_id': subcat.category_id,
                'name': subcat.name,
                'slug': subcat.slug,
                'description': subcat.description,
                'icon': subcat.icon,
                'sort_order': subcat.sort_order,
                'is_active': subcat.is_active
            })
        
        # Module exportieren
        modules = LearningModule.query.order_by(LearningModule.sort_order).all()
        for mod in modules:
            backup_data['modules'].append({
                'id': mod.id,
                'category_id': mod.category_id,
                'subcategory_id': mod.subcategory_id,
                'title': mod.title,
                'slug': mod.slug,
                'description': mod.description,
                'icon': mod.icon,
                'template_file': mod.template_file,
                'content_type': mod.content_type,
                'external_url': mod.external_url,
                'is_published': mod.is_published,
                'is_lead_magnet': mod.is_lead_magnet,
                'required_subscription_levels': mod.required_subscription_levels,
                'estimated_duration': mod.estimated_duration,
                'difficulty_level': mod.difficulty_level,
                'sort_order': mod.sort_order
            })
        
        # In Datei speichern
        filename = f"backup_modules_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, ensure_ascii=False, indent=2)
        
        print(f"[OK] Backup erstellt: {filename}")
        print(f"   - {len(backup_data['categories'])} Kategorien")
        print(f"   - {len(backup_data['subcategories'])} Unterkategorien")
        print(f"   - {len(backup_data['modules'])} Module")
        
        return filename

if __name__ == '__main__':
    backup_modules()

