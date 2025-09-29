#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SYNC MODULES TO RAILWAY.APP
Automatisches Script zur Synchronisation aller Module zur Railway.app Produktion

Version: 1.0
Author: AI Assistant for Didis Trading Academy
"""

import os
import sys
import subprocess
import json
from datetime import datetime
from pathlib import Path

# Windows encoding fix
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def run_command(command, description=""):
    """Führt ein Kommando aus und gibt das Ergebnis zurück"""
    print(f"\n🔄 {description}")
    print(f"   Kommando: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print(f"✅ Erfolgreich: {description}")
            if result.stdout:
                print(f"   Output: {result.stdout.strip()}")
            return True, result.stdout
        else:
            print(f"❌ Fehler bei: {description}")
            print(f"   Error: {result.stderr}")
            return False, result.stderr
    except Exception as e:
        print(f"❌ Exception bei {description}: {str(e)}")
        return False, str(e)

def validate_module_config():
    """Validiert die Module-Konfiguration"""
    config_file = "didis_streamlit_modules_config.json"
    
    if not os.path.exists(config_file):
        print(f"❌ Module-Konfiguration nicht gefunden: {config_file}")
        return False
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        modules = config.get('modules', [])
        print(f"✅ {len(modules)} Module in Konfiguration gefunden")
        
        # Statistiken
        html_modules = len([m for m in modules if m.get('content_type') == 'html'])
        streamlit_modules = len([m for m in modules if m.get('content_type') == 'streamlit'])
        lead_magnets = len([m for m in modules if m.get('is_lead_magnet', False)])
        
        print(f"   📄 HTML-Module: {html_modules}")
        print(f"   ⚡ Streamlit-Module: {streamlit_modules}")
        print(f"   🧲 Lead-Magnete: {lead_magnets}")
        
        return True
        
    except Exception as e:
        print(f"❌ Fehler beim Lesen der Konfiguration: {str(e)}")
        return False

def check_git_status():
    """Prüft Git-Status und zeigt Änderungen"""
    print("\n📊 AKTUELLER GIT-STATUS")
    print("=" * 50)
    
    # Status anzeigen
    success, output = run_command("git status --porcelain", "Git-Status prüfen")
    if not success:
        return False
    
    if not output.strip():
        print("✅ Keine ausstehenden Änderungen")
        return True
    
    print("📝 Ausstehende Änderungen:")
    for line in output.strip().split('\n'):
        status = line[:2]
        file = line[3:]
        
        status_symbol = {
            'M ': '📝 Modifiziert:',
            ' M': '📝 Modifiziert:',
            'A ': '➕ Hinzugefügt:',
            'D ': '🗑️  Gelöscht:',
            '??': '❓ Unbekannt:',
            'MM': '📝 Modifiziert:'
        }.get(status, f'📄 {status}:')
        
        print(f"   {status_symbol} {file}")
    
    return True

def sync_to_railway():
    """Hauptfunktion: Synchronisation zu Railway"""
    print("\n" + "=" * 60)
    print("🚀 SYNC MODULES TO RAILWAY.APP")
    print("=" * 60)
    print(f"⏰ Gestartet: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Arbeitsverzeichnis: {os.getcwd()}")
    
    # 1. Module-Konfiguration validieren
    print("\n📋 SCHRITT 1: MODULE-KONFIGURATION VALIDIEREN")
    if not validate_module_config():
        print("❌ Module-Validierung fehlgeschlagen!")
        return False
    
    # 2. Git-Status prüfen
    print("\n📋 SCHRITT 2: GIT-STATUS PRÜFEN")
    if not check_git_status():
        print("❌ Git-Status-Check fehlgeschlagen!")
        return False
    
    # 3. Wichtige Dateien zum Staging hinzufügen
    print("\n📋 SCHRITT 3: DATEIEN HINZUFÜGEN")
    files_to_add = [
        "app.py",
        "didis_streamlit_modules_config.json", 
        "templates/expected_value.html",
        "templates/tirone_quadrant_lines.html",
        "templates/Screenshots/Tirone.png"
    ]
    
    for file in files_to_add:
        if os.path.exists(file):
            success, _ = run_command(f'git add "{file}"', f"Hinzufügen: {file}")
            if not success:
                print(f"⚠️  Warnung: Konnte {file} nicht hinzufügen")
        else:
            print(f"⚠️  Warnung: Datei nicht gefunden: {file}")
    
    # 4. Commit erstellen
    print("\n📋 SCHRITT 4: COMMIT ERSTELLEN")
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    commit_message = f"🚀 Module-Sync zu Railway - {timestamp}\\n\\n✨ Neue Features:\\n- Updated module configuration\\n- New Tirone Quadrant Lines module\\n- Enhanced Expected Value calculator\\n- Improved module structure"
    
    success, _ = run_command(f'git commit -m "{commit_message}"', "Git Commit erstellen")
    if not success:
        print("❌ Commit fehlgeschlagen!")
        return False
    
    # 5. Push zu Railway
    print("\n📋 SCHRITT 5: PUSH ZU RAILWAY")
    success, _ = run_command("git push origin main", "Push zu Railway")
    if not success:
        print("❌ Push zu Railway fehlgeschlagen!")
        return False
    
    # 6. Deployment-Status prüfen
    print("\n📋 SCHRITT 6: DEPLOYMENT-STATUS")
    print("🎯 Railway Auto-Deployment läuft...")
    print("📱 Produktions-URL: https://didis-premium-app-production.up.railway.app/")
    print("⏱️  Deployment-Zeit: ca. 2-3 Minuten")
    
    # 7. Erfolgsmeldung
    print("\n" + "=" * 60)
    print("✅ SYNC ERFOLGREICH ABGESCHLOSSEN!")
    print("=" * 60)
    print("📊 Zusammenfassung:")
    print("   ✅ Module-Konfiguration validiert")
    print("   ✅ Git-Changes committed")
    print("   ✅ Push zu Railway erfolgreich")
    print("   🚀 Auto-Deployment gestartet")
    
    print("\n🔗 NÄCHSTE SCHRITTE:")
    print("1. ⏳ 2-3 Minuten warten (Railway Deployment)")
    print("2. 🌐 Produktions-App testen:")
    print("   https://didis-premium-app-production.up.railway.app/")
    print("3. 🔐 Mit Admin-Account einloggen:")
    print("   Username: admin | Password: admin")
    print("4. 📚 Module-Übersicht überprüfen:")
    print("   https://didis-premium-app-production.up.railway.app/modules")
    print("5. 🆕 Neue Module testen (Expected Value, Tirone Levels)")
    
    return True

def main():
    """Main function"""
    try:
        if sync_to_railway():
            print("\n🎉 SYNC ZU RAILWAY ERFOLGREICH! 🎉")
            sys.exit(0)
        else:
            print("\n💥 SYNC FEHLGESCHLAGEN!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Sync durch Benutzer abgebrochen")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unerwarteter Fehler: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
