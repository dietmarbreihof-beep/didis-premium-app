#!/bin/bash
# Railway Startup Script
# Führt Migrationen aus, dann startet den Server

set -e  # Bei Fehler abbrechen

echo "========================================="
echo "RAILWAY STARTUP: Starting Application"
echo "========================================="

# Schritt 1: Migrationen ausführen
echo ""
echo "[1/2] Running database migrations..."
python run_migrations.py

if [ $? -eq 0 ]; then
    echo "[OK] Migrations completed successfully"
else
    echo "[ERROR] Migrations failed!"
    exit 1
fi

# Schritt 2: Server starten
echo ""
echo "[2/2] Starting Gunicorn server..."
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 app:app

