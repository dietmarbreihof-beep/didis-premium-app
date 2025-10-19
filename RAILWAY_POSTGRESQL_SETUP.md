# 🚀 PostgreSQL auf Railway einrichten

## ⚠️ Warum PostgreSQL statt SQLite?

**Problem mit SQLite auf Railway:**
- Railway Container haben **kein persistentes Dateisystem**
- Bei jedem Deployment wird die SQLite-Datei **gelöscht**
- Alle manuell hinzugefügten Module sind **weg** nach dem nächsten Deploy
- Alle User-Registrierungen **verloren**

**Lösung: PostgreSQL**
- ✅ Persistenter Storage - Daten bleiben bei Deployments
- ✅ Besser für Multi-User
- ✅ Production-ready
- ✅ Kostenlos bei Railway

---

## 📋 Setup-Schritte (5 Minuten)

### **1. PostgreSQL-Service hinzufügen**

1. Gehe zu deinem Railway-Projekt: https://railway.app/dashboard

2. Klicke auf **"+ New"** → **"Database"** → **"Add PostgreSQL"**

3. Railway erstellt automatisch:
   - PostgreSQL-Datenbank
   - Connection String in `DATABASE_URL`

### **2. DATABASE_URL mit deiner App verknüpfen**

1. Klicke auf dein **Flask-App-Service**

2. Gehe zu **"Variables"** Tab

3. Klicke auf **"+ New Variable"** → **"Add Reference"**

4. Wähle:
   - **Service:** PostgreSQL
   - **Variable:** `DATABASE_URL`

5. **Speichern!**

### **3. App neu deployen**

Dein nächster `git push origin main` wird:
1. PostgreSQL-Treiber installieren (psycopg2-binary)
2. Automatisch PostgreSQL statt SQLite nutzen
3. Migrations ausführen → Risikomanagement-Modul wird registriert
4. Daten bleiben **permanent** erhalten!

---

## ✅ Verifikation

Nach dem Deployment:

1. **Railway Logs prüfen:**
   ```
   [DATABASE] Nutze PostgreSQL auf Railway
   ```

2. **Module prüfen:**
   ```
   https://didis-premium-app-production.up.railway.app/modules
   ```
   → Risikomanagement-Modul sollte da sein!

3. **Admin-Panel prüfen:**
   ```
   https://didis-premium-app-production.up.railway.app/admin/modules
   ```
   → Alle Module sichtbar!

---

## 🎯 Was passiert jetzt?

### **Lokal (auf deinem PC):**
```
[DATABASE] Nutze lokales SQLite: didis_academy.db
```
→ Du entwickelst weiter mit SQLite (einfacher!)

### **Auf Railway (Production):**
```
[DATABASE] Nutze PostgreSQL auf Railway
```
→ Production nutzt PostgreSQL (sicher!)

### **Bei jedem Deployment:**
1. ✅ PostgreSQL-Datenbank bleibt erhalten
2. ✅ `run_migrations.py` läuft automatisch
3. ✅ Risikomanagement-Modul wird registriert (falls noch nicht da)
4. ✅ Alle anderen Module auch!

---

## 🔧 Falls etwas schief geht

### **"Migration failed" in Logs:**

Führe manuell aus als Admin:
```
https://didis-premium-app-production.up.railway.app/admin/auto-register-modules
```

Das scannt alle HTML-Templates und registriert sie!

### **"Connection refused" Error:**

1. Prüfe ob `DATABASE_URL` Variable gesetzt ist
2. Prüfe ob PostgreSQL-Service läuft
3. Neu-deployen: `git commit --allow-empty -m "Trigger deploy" && git push`

### **Module verschwinden immer noch:**

Das passiert NICHT mehr mit PostgreSQL! Datenbank ist persistent.

---

## 💾 Backup & Restore (Optional)

### **PostgreSQL Backup erstellen:**

Railway bietet automatische Backups, aber du kannst auch manuell:

```bash
# In Railway Console
pg_dump $DATABASE_URL > backup.sql
```

### **Lokale SQLite → PostgreSQL migrieren:**

Falls du Daten von SQLite übertragen willst:

1. Exportiere Daten lokal
2. Importiere in Railway PostgreSQL
3. Oder: Nutze `/admin/auto-register-modules` um alle Module neu zu registrieren

---

## 📊 Kosten

**Railway PostgreSQL:**
- ✅ **$5/Monat** (Hobby Plan)
- ✅ 500 MB Storage
- ✅ Völlig ausreichend für deine App

**Was du bekommst:**
- Persistente Datenbank
- Automatische Backups
- Production-ready Setup
- Keine Daten-Verluste mehr!

---

## 🎉 Nächste Schritte

Nach PostgreSQL-Setup:

1. ✅ Teste `/modules` - Risikomanagement sollte da sein
2. ✅ Teste Modul-Hinzufügen - bleibt nach Deployment
3. ✅ Teste User-Registrierung - User bleiben erhalten
4. ✅ Entwickle weiter - alles funktioniert!

---

**Erstellt:** 19. Oktober 2025  
**Status:** ✅ Ready to Deploy

