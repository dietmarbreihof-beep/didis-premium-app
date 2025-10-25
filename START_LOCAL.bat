@echo off
echo ===============================================
echo Didis Trading Academy - Lokaler Start
echo ===============================================
echo.

cd "C:\Users\dietmar.breihof\OneDrive - Breihof-IT GmbH\Aktien\didis-premium-app"

echo [1/3] Starte Flask-App...
start "Didis Trading Academy" cmd /k "python app.py"

echo [2/3] Warte 8 Sekunden auf App-Start...
timeout /t 8 /nobreak >nul

echo [3/3] Oeffne Browser...
start http://localhost:5000/module/noise-vs-edge

echo.
echo ===============================================
echo App sollte jetzt laufen auf:
echo   http://localhost:5000/module/noise-vs-edge
echo.
echo Zum Beenden: Schliesse das Flask-App-Fenster
echo ===============================================
pause


