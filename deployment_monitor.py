# deployment_monitor.py - Git Push & Railway Deployment Monitor
"""
Einfaches Tool um Git Push Status und Railway Deployment zu überwachen.
Zeigt dir genau an, wann alles fertig deployed ist.
"""

import subprocess
import time
import requests
import sys
from datetime import datetime

def get_git_status():
    """Prüft den Git Status"""
    try:
        # Prüfe ob es uncommitted changes gibt
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, cwd='.')
        uncommitted = len(result.stdout.strip()) > 0
        
        # Prüfe ob lokaler Branch ahead/behind ist
        result = subprocess.run(['git', 'status', '-b', '--porcelain'], 
                              capture_output=True, text=True, cwd='.')
        
        status_line = result.stdout.split('\n')[0] if result.stdout else ""
        
        ahead = 'ahead' in status_line
        behind = 'behind' in status_line
        up_to_date = not ahead and not behind and not uncommitted
        
        return {
            'uncommitted_changes': uncommitted,
            'ahead_of_remote': ahead,
            'behind_remote': behind,
            'up_to_date': up_to_date,
            'status_line': status_line
        }
    except Exception as e:
        return {'error': str(e)}

def get_latest_commit():
    """Holt den letzten Commit Hash und Message"""
    try:
        # Letzter lokaler Commit
        result = subprocess.run(['git', 'log', '-1', '--format=%H|%s|%an|%ar'], 
                              capture_output=True, text=True, cwd='.')
        if result.stdout:
            hash_msg, subject, author, date = result.stdout.strip().split('|', 3)
            return {
                'hash': hash_msg[:8],
                'message': subject,
                'author': author,
                'date': date
            }
    except Exception as e:
        return {'error': str(e)}
    return None

def check_railway_deployment():
    """Prüft ob Railway App erreichbar ist (einfacher Health Check)"""
    try:
        # Ersetze mit deiner Railway App URL
        app_url = "https://didis-premium-app-production.up.railway.app"
        
        response = requests.get(f"{app_url}/", timeout=10)
        
        return {
            'status_code': response.status_code,
            'response_time': response.elapsed.total_seconds(),
            'accessible': response.status_code == 200,
            'url': app_url
        }
    except requests.exceptions.RequestException as e:
        return {
            'error': str(e),
            'accessible': False
        }

def print_status_header():
    """Druckt den Status-Header"""
    print("\n" + "="*60)
    print("GIT PUSH & RAILWAY DEPLOYMENT MONITOR")
    print("="*60)
    print(f"Zeit: {datetime.now().strftime('%H:%M:%S')}")

def print_git_status(git_status, latest_commit):
    """Druckt Git Status"""
    print("\nGIT STATUS:")
    print("-" * 30)
    
    if 'error' in git_status:
        print(f"[ERROR] Git Fehler: {git_status['error']}")
        return
    
    if git_status['up_to_date']:
        print("[OK] Git: Alles synchronisiert")
    else:
        if git_status['uncommitted_changes']:
            print("[WARNING] Git: Uncommitted changes vorhanden")
        if git_status['ahead_of_remote']:
            print("[PUSH] Git: Lokale Commits müssen gepusht werden")
        if git_status['behind_remote']:
            print("[PULL] Git: Remote Commits müssen gepullt werden")
    
    if latest_commit and not 'error' in latest_commit:
        print(f"Letzter Commit: {latest_commit['hash']} - {latest_commit['message']}")
        print(f"Autor: {latest_commit['author']} ({latest_commit['date']})")

def print_railway_status(railway_status):
    """Druckt Railway Status"""
    print("\nRAILWAY DEPLOYMENT:")
    print("-" * 30)
    
    if 'error' in railway_status:
        print(f"[ERROR] Railway nicht erreichbar: {railway_status['error']}")
        print("Mögliche Gründe:")
        print("   - Deployment läuft noch")
        print("   - App ist offline")
        print("   - Netzwerkproblem")
    else:
        if railway_status['accessible']:
            print(f"[OK] Railway: App ist online ({railway_status['response_time']:.2f}s)")
            print(f"URL: {railway_status['url']}")
        else:
            print(f"[ERROR] Railway: App nicht erreichbar (Status: {railway_status.get('status_code', 'N/A')})")

def monitor_deployment():
    """Hauptfunktion für Deployment-Monitoring"""
    print("Starte Deployment-Monitoring...")
    print("Drücke Ctrl+C zum Beenden")
    
    try:
        while True:
            print_status_header()
            
            # Git Status prüfen
            git_status = get_git_status()
            latest_commit = get_latest_commit()
            print_git_status(git_status, latest_commit)
            
            # Railway Status prüfen
            railway_status = check_railway_deployment()
            print_railway_status(railway_status)
            
            # Zusammenfassung
            print("\nSTATUS ZUSAMMENFASSUNG:")
            print("-" * 30)
            
            git_ok = git_status.get('up_to_date', False)
            railway_ok = railway_status.get('accessible', False)
            
            if git_ok and railway_ok:
                print("*** ALLES BEREIT! ***")
                print("[OK] Git: Synchronisiert")
                print("[OK] Railway: Online")
                print("\nDeine Änderungen sind live!")
                break
            elif git_ok:
                print("[WAIT] Git synchronisiert, warte auf Railway...")
                print("Railway Deployment läuft noch...")
            else:
                print("[ACTION] Git Push erforderlich")
            
            print(f"\nNächste Prüfung in 10 Sekunden...")
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\n\nMonitoring beendet.")
        print("Du kannst jederzeit 'python deployment_monitor.py' ausführen")

def quick_status():
    """Schneller Status-Check ohne Loop"""
    print_status_header()
    
    git_status = get_git_status()
    latest_commit = get_latest_commit()
    print_git_status(git_status, latest_commit)
    
    railway_status = check_railway_deployment()
    print_railway_status(railway_status)
    
    # Kurze Zusammenfassung
    git_ok = git_status.get('up_to_date', False)
    railway_ok = railway_status.get('accessible', False)
    
    print("\nQUICK STATUS:")
    if git_ok and railway_ok:
        print("*** Alles online und synchronisiert! ***")
    elif git_ok:
        print("[WAIT] Git OK, Railway möglicherweise noch am deployen...")
    else:
        print("[ACTION] Git Push oder Pull erforderlich")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'quick':
        quick_status()
    else:
        print("DEPLOYMENT MONITOR")
        print("=" * 40)
        print("Dieses Tool überwacht Git Push und Railway Deployment Status.")
        print()
        print("Optionen:")
        print("  python deployment_monitor.py       # Kontinuierliches Monitoring")
        print("  python deployment_monitor.py quick # Einmaliger Status-Check")
        print()
        
        choice = input("Monitoring starten? (j/n): ").lower().strip()
        if choice == 'j':
            monitor_deployment()
        else:
            print("Bis später!")
