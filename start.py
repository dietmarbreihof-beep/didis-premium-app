#!/usr/bin/env python3
"""
Railway Startup Script
1. Führt Migrationen aus
2. Startet Gunicorn Server
"""

import sys
import os
import subprocess

def main():
    print("=" * 60)
    print("RAILWAY STARTUP: Starting Application")
    print("=" * 60)
    
    # Schritt 1: Migrationen ausführen
    print("\n[1/2] Running database migrations...")
    try:
        result = subprocess.run(
            [sys.executable, 'run_migrations.py'],
            check=True,
            capture_output=False
        )
        print("[OK] Migrations completed successfully\n")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Migrations failed with exit code {e.returncode}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Unexpected error during migrations: {e}")
        sys.exit(1)
    
    # Schritt 2: Gunicorn Server starten
    print("[2/2] Starting Gunicorn server...")
    port = os.environ.get('PORT', '8080')
    
    try:
        # exec ersetzt den Python-Prozess durch Gunicorn
        os.execvp('gunicorn', [
            'gunicorn',
            '--bind', f'0.0.0.0:{port}',
            '--workers', '2',
            'app:app'
        ])
    except Exception as e:
        print(f"[ERROR] Failed to start Gunicorn: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

