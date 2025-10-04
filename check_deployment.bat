@echo off
title Git Push & Railway Deployment Status
color 0A

echo.
echo ========================================
echo    GIT PUSH ^& RAILWAY STATUS CHECK
echo ========================================
echo.

cd /d "%~dp0"

echo 🔍 Pruefe Git Status...
git status --porcelain > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git nicht verfuegbar oder nicht in Git Repository
    pause
    exit /b 1
)

echo.
echo 📦 GIT STATUS:
echo --------------
git status -b

echo.
echo 📝 LETZTER COMMIT:
echo ------------------
git log -1 --format="Hash: %%h | %%s | %%an | %%ar"

echo.
echo 🚂 RAILWAY STATUS:
echo ------------------
echo Pruefe Railway App...

python -c "
import requests
try:
    response = requests.get('https://didis-premium-app-production.up.railway.app/', timeout=10)
    if response.status_code == 200:
        print('✅ Railway App ist ONLINE (%s)' % response.elapsed.total_seconds())
        print('🌐 URL: https://didis-premium-app-production.up.railway.app/')
    else:
        print('⚠️  Railway App antwortet mit Status:', response.status_code)
except Exception as e:
    print('❌ Railway App nicht erreichbar:', str(e))
    print('💡 Deployment läuft möglicherweise noch...')
"

echo.
echo ========================================
echo 💡 TIPPS:
echo - Wenn Git "ahead" zeigt: git push origin main
echo - Wenn Railway offline: Warte 2-3 Minuten nach Push
echo - Analytics Dashboard: /admin/analytics
echo ========================================
echo.

pause
