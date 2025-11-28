#!/usr/bin/env python3
"""
Löscht das alte momentum-burst-method Modul aus der Datenbank
"""

from app import app, db, LearningModule

def delete_old_momentum_module():
    """Lösche momentum-burst-method aus der Datenbank"""
    with app.app_context():
        try:
            # Finde das alte Modul
            old_module = LearningModule.query.filter_by(slug='momentum-burst-method').first()
            
            if old_module:
                print(f"[OK] Gefunden: '{old_module.title}' (Slug: {old_module.slug})")
                print(f"  ID: {old_module.id}")
                print(f"  Template: {old_module.template_file}")
                print(f"  Kategorie: {old_module.category_id}")
                
                # Loesche das Modul
                db.session.delete(old_module)
                db.session.commit()
                
                print(f"\n[SUCCESS] Modul 'momentum-burst-method' wurde erfolgreich geloescht!")
                print(f"   Das konsolidierte Modul 'momentum-burst' bleibt aktiv.")
            else:
                print("[WARNING] Modul 'momentum-burst-method' nicht in Datenbank gefunden.")
                print("   Moeglicherweise bereits geloescht oder nie registriert.")
                
        except Exception as e:
            print(f"[ERROR] Fehler beim Loeschen: {e}")
            db.session.rollback()

if __name__ == '__main__':
    print("Loesche altes momentum-burst-method Modul aus Datenbank...\n")
    delete_old_momentum_module()

