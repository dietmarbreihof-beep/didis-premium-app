"""
Migration: Email Verification Tokens Tabelle hinzufügen
Datum: 2025-11-29
Beschreibung: Fügt die email_verification_tokens Tabelle für Email-Verifizierung und Passwort-Reset hinzu
"""
from app import app, db, EmailVerificationToken

def migrate():
    """Erstellt die email_verification_tokens Tabelle"""
    with app.app_context():
        print("\n" + "="*60)
        print("🔧 MIGRATION: Email Verification Tokens")
        print("="*60)
        
        try:
            # Prüfen ob Tabelle bereits existiert
            inspector = db.inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            if 'email_verification_tokens' in existing_tables:
                print("ℹ️  Tabelle 'email_verification_tokens' existiert bereits")
            else:
                # Tabelle erstellen
                db.create_all()
                print("✅ Tabelle 'email_verification_tokens' erfolgreich erstellt")
            
            # Zeige Tabellenstruktur
            if 'email_verification_tokens' in inspector.get_table_names():
                columns = inspector.get_columns('email_verification_tokens')
                print("\n📋 Tabellenstruktur:")
                for col in columns:
                    print(f"   - {col['name']}: {col['type']}")
            
            print("="*60)
            print("✅ Migration erfolgreich abgeschlossen\n")
            return True
            
        except Exception as e:
            print(f"❌ Fehler bei der Migration: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = migrate()
    if not success:
        exit(1)

