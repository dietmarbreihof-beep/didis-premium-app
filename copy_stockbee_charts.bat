@echo off
echo ===================================================
echo StockBee Charts zu static/screenshots kopieren
echo ===================================================

REM Erstelle Zielverzeichnis falls nicht vorhanden
if not exist "static\screenshots\StockBee Guides" mkdir "static\screenshots\StockBee Guides"

REM Kopiere Chart-Beispiele
echo Kopiere Chart-Beispiele...

if exist "StockBee Guides\1_Chart_Beispiel.png" (
    copy "StockBee Guides\1_Chart_Beispiel.png" "static\screenshots\StockBee Guides\"
    echo [OK] 1_Chart_Beispiel.png
) else (
    echo [SKIP] 1_Chart_Beispiel.png nicht gefunden
)

if exist "StockBee Guides\2_Chart_Beispiel_GRWG.png" (
    copy "StockBee Guides\2_Chart_Beispiel_GRWG.png" "static\screenshots\StockBee Guides\"
    echo [OK] 2_Chart_Beispiel_GRWG.png
) else (
    echo [SKIP] 2_Chart_Beispiel_GRWG.png nicht gefunden
)

if exist "StockBee Guides\3_Chart_Beispiel_FSLY.png" (
    copy "StockBee Guides\3_Chart_Beispiel_FSLY.png" "static\screenshots\StockBee Guides\"
    echo [OK] 3_Chart_Beispiel_FSLY.png
) else (
    echo [SKIP] 3_Chart_Beispiel_FSLY.png nicht gefunden
)

if exist "StockBee Guides\Buch_Next_Superstock.png" (
    copy "StockBee Guides\Buch_Next_Superstock.png" "static\screenshots\StockBee Guides\"
    echo [OK] Buch_Next_Superstock.png
) else (
    echo [SKIP] Buch_Next_Superstock.png nicht gefunden
)

if exist "StockBee Guides\1. Episodic Pivots (EP) Guide_Screenshot.png" (
    copy "StockBee Guides\1. Episodic Pivots (EP) Guide_Screenshot.png" "static\screenshots\StockBee Guides\"
    echo [OK] 1. Episodic Pivots (EP) Guide_Screenshot.png
) else (
    echo [SKIP] Episodic Pivots Screenshot nicht gefunden
)

echo.
echo ===================================================
echo Kopieren abgeschlossen!
echo ===================================================
echo.
echo Dateien sind jetzt verfuegbar unter:
echo   static/screenshots/StockBee Guides/
echo.
echo Naechste Schritte:
echo 1. python migrations/register_momentum_burst.py
echo 2. Teste lokal: http://localhost:5000/module/momentum-burst
echo 3. Git Add + Commit + Push
echo.
pause

