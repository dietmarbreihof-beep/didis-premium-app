# Cursor Rules - Didis Premium Trading Academy

**WICHTIG:** Diese Rules beschreiben Änderungen durch Claude Code. Claude Code hat Vorrang für alle hier beschriebenen Funktionalitäten.

---

## 🚨 KRITISCHE REGELN - NIEMALS ÄNDERN

### 1. AUTO-SYNC IST PERMANENT DEAKTIVIERT

**Was wurde geändert:**
- `init_modules_on_startup()` (app.py:209-212) hat ein **Early Return** und ist deaktiviert
- `sync_modules_from_local()` wird NICHT mehr in Routes aufgerufen
- Grund: Auto-Sync hat User-erstellte Module überschrieben

**CURSOR DARF NICHT:**
- ❌ Auto-Sync reaktivieren
- ❌ Early Return in `init_modules_on_startup()` entfernen
- ❌ `sync_modules_from_local()` in Routes aufrufen (z.B. in home())
- ❌ Module programmatisch synchronisieren/überschreiben

**CURSOR MUSS:**
- ✅ Module-Verwaltung NUR über Admin-UI belassen
- ✅ Beim Hinzufügen neuer Module die Admin-UI oder `/admin/register-missing-modules` nutzen
- ✅ Kommentare über deaktivierten Auto-Sync beibehalten

**Betroffene Code-Bereiche:**
```python
# app.py:209-212
def init_modules_on_startup():
    """🚀 AUTO-SYNC DEAKTIVIERT - Module werden nur über Admin-UI verwaltet"""
    print("[INFO] Module Auto-Sync ist DEAKTIVIERT - Module werden über Admin-UI verwaltet")
    return True  # Early return - DO NOT REMOVE!
```

---

### 2. 4-TIER SUBSCRIPTION SYSTEM

**Was wurde geändert:**
- SubscriptionType Enum erweitert auf 4 Levels: `FREE, PREMIUM, ELITE, ELITE_PRO` (app.py:362-381)
- User Model hat neue Felder: `subscription_type`, `subscription_updated_at`, `subscription_updated_by` (app.py:399-402)
- Hierarchie-Logik implementiert mit `hierarchy()` und `can_access()` Methoden

**CURSOR DARF NICHT:**
- ❌ Subscription Levels reduzieren (z.B. zurück auf 3 Levels)
- ❌ User Model Felder `subscription_type`, `subscription_updated_at`, `subscription_updated_by` entfernen
- ❌ SubscriptionType Enum ändern oder umbenennen
- ❌ Hierarchie-Logik modifizieren ohne Rücksprache

**CURSOR MUSS:**
- ✅ Alle 4 Subscription Levels unterstützen bei neuen Features
- ✅ Bei Modul-Erstellung alle 4 Levels anbieten (free, premium, elite, elite_pro)
- ✅ `can_access_module()` Methode verwenden für Zugriffsprüfung
- ✅ Admin-Audit-Log nutzen bei Subscription-Änderungen

**Betroffene Code-Bereiche:**
```python
# app.py:362-381 - SubscriptionType Enum
class SubscriptionType(enum.Enum):
    FREE = "free"
    PREMIUM = "premium"
    ELITE = "elite"
    ELITE_PRO = "elite_pro"

# app.py:399-402 - User Model Felder
subscription_type = db.Column(db.Enum(SubscriptionType), default=SubscriptionType.FREE, nullable=False)
subscription_updated_at = db.Column(db.DateTime)
subscription_updated_by = db.Column(db.String(80))

# app.py:410-416 - Zugriffsprüfung
def can_access_module(self, module):
    """Check if user can access a specific module based on subscription"""
    if module.is_lead_magnet:
        return True
    if not module.required_subscription_levels:
        return True
    return self.subscription_type.value in module.required_subscription_levels
```

**Templates:**
```html
<!-- templates/admin/modules.html:624-649 - Alle 4 Checkboxen -->
<input type="checkbox" name="req_free"> 🆓 Free
<input type="checkbox" name="req_premium" checked> ⭐ Premium
<input type="checkbox" name="req_elite" checked> 💎 Elite
<input type="checkbox" name="req_elite_pro" checked> 👑 Elite Pro
```

---

### 3. FEHLENDE MODULE AUTO-DETECTION

**Was wurde geändert:**
- Neue Admin-Route: `/admin/register-missing-modules` (app.py:5437-5532)
- Scannt templates-Ordner nach unregistrierten .html Dateien
- Registriert fehlende Module automatisch in "🆕 Neue Module" Kategorie
- Button im Admin-Interface: "🔍 Fehlende Module finden" (templates/admin/modules.html:55-60)

**CURSOR DARF NICHT:**
- ❌ Route `/admin/register-missing-modules` löschen oder umbenennen
- ❌ "Neue Module" Kategorie (slug: `neue-module`) löschen oder ändern
- ❌ Auto-Detection Logik entfernen
- ❌ Button im Admin-Interface entfernen

**CURSOR MUSS:**
- ✅ Fehlende Module als `is_published=False` registrieren (wie implementiert)
- ✅ Auto-generierte Module in "Neue Module" Kategorie einordnen
- ✅ Templates-Ignorierung beibehalten (base.html, home.html, admin/*, auth/*, errors/*)
- ✅ Bei neuen System-Templates diese zur Ignorier-Liste hinzufügen

**Betroffene Code-Bereiche:**
```python
# app.py:5437-5532
@app.route('/admin/register-missing-modules')
@admin_required
def admin_register_missing_modules():
    """Scannt templates-Ordner und registriert fehlende Module in 'Neue Module' Kategorie"""
    # 1. Scan templates-Ordner
    # 2. Vergleich mit DB
    # 3. Registrierung in "Neue Module" Kategorie
    # 4. is_published=False für manuelle Review
```

**Ignore-Pattern:**
```python
# Diese Templates ignorieren (System-Templates):
if filename in ['base.html', 'home.html', 'modules_overview.html', '_navigation.html']:
    continue
# Auch ignorieren: admin/*, auth/*, errors/*
```

---

### 4. USER MANAGEMENT SYSTEM

**Was wurde geändert:**
- Komplettes User-Management-Interface: `/admin/users` (app.py:5188-5433)
- Neue Template: `templates/admin/users.html` (388 Zeilen)
- Admin Audit Log für alle User-Änderungen (AdminAuditLog Model app.py:418-433)
- Navigation erweitert in `templates/base.html` (User-Link im Admin-Bereich)

**CURSOR DARF NICHT:**
- ❌ Admin-Routes löschen: `/admin/users`, `/admin/users/<id>/subscription`, `/admin/users/<id>/toggle-status`, `/admin/users/<id>/delete`
- ❌ AdminAuditLog Model ändern oder entfernen
- ❌ Audit-Logging deaktivieren
- ❌ User-Management-Template löschen

**CURSOR MUSS:**
- ✅ Audit-Logging nutzen bei allen User-Änderungen (Beispiel unten)
- ✅ Subscription-Updates über Admin-Routes durchführen
- ✅ User-Status-Änderungen über `is_active` Boolean verwalten

**Audit-Log Beispiel:**
```python
# Bei User-Änderungen immer Audit-Log erstellen
audit_entry = AdminAuditLog(
    admin_username=session['username'],
    action_type='subscription_change',  # oder 'user_activate', 'user_deactivate', 'user_delete'
    target_user_id=user.id,
    target_username=user.username,
    old_value=old_subscription.value,
    new_value=new_subscription.value,
    ip_address=request.remote_addr
)
db.session.add(audit_entry)
```

---

## 📋 MODULE MANAGEMENT KONVENTIONEN

### Module Form Backend

**Subscription Levels Verarbeitung (app.py:2376-2386):**
```python
# Alle 4 Levels unterstützen:
required_levels = []
if not is_lead_magnet:
    if 'req_free' in request.form:
        required_levels.append('free')
    if 'req_premium' in request.form:
        required_levels.append('premium')
    if 'req_elite' in request.form:
        required_levels.append('elite')
    if 'req_elite_pro' in request.form:
        required_levels.append('elite_pro')
```

**CURSOR MUSS:**
- ✅ Bei neuen Modul-Features alle 4 Checkboxen unterstützen
- ✅ Default: premium, elite, elite_pro checked (wie in Template definiert)

---

## 🗄️ DATABASE KONVENTIONEN

### PostgreSQL in Production

**Was wurde geändert:**
- DATABASE_URL verwendet PostgreSQL auf Railway (app.py:69-78)
- Auto-Fix für `postgres://` → `postgresql://` implementiert
- Migration für `subscription_type` Felder erstellt

**CURSOR DARF NICHT:**
- ❌ DATABASE_URL Logik ändern
- ❌ Auto-Fix für postgres:// entfernen
- ❌ SQLite für Production nutzen

**CURSOR MUSS:**
- ✅ Neue Migrationen für Schema-Änderungen erstellen
- ✅ Bei neuen User-Feldern Migration bereitstellen
- ✅ PostgreSQL-Kompatibilität sicherstellen

---

## 🔒 SECURITY FEATURES

**Was NICHT geändert werden darf:**
- CSRF-Protection (app.py:47-52)
- Rate Limiting (app.py:54-64)
- Password Validation (app.py:307-355)
- Session Security Config (app.py:39-49)
- SECRET_KEY Validierung (app.py:17-37)

**CURSOR MUSS:**
- ✅ CSRF-Token in allen Forms nutzen
- ✅ Rate Limiting für Login-Routes beibehalten
- ✅ Password-Validierung bei Registrierung/Änderung nutzen

---

## 📝 GIT WORKFLOW

**Branch:**
- Production Branch: `claude/prepare-production-release-011CURveFMwP9fPGmGZ2NeWN`

**CURSOR MUSS:**
- ✅ Vor Commits prüfen ob Claude Code Änderungen auf diesem Branch sind
- ✅ Bei Merge-Konflikten: Claude Code Änderungen haben Vorrang
- ✅ Nicht auf `main` pushen ohne Review

**Commits die Claude Code gemacht hat (neueste zuerst):**
```
26a6bee - feat(admin): Auto-Detection fehlender Module mit Neue-Module-Kategorie
f220e59 - feat(modules): Robustes Modul-Management - Module bleiben persistent
8ded385 - feat(migration): Auto-Migration für User subscription_type Felder
388daed - feat(admin): Implementiere User-Verwaltung mit 4-Tier-Subscription-System
1c8c2cb - fix(change-password): Handle Demo-User ohne DB-ID
```

---

## ⚠️ KONFLIKT-PRÄVENTION

### Bei folgenden Änderungen CURSOR MUSS STOPPEN und User fragen:

1. **Module-Sync wiederherstellen** → Claude Code hat das bewusst deaktiviert
2. **Subscription Levels reduzieren** → 4-Tier System ist Production-Standard
3. **User Model Schema ändern** → Migration erforderlich + Claude Code Konsultation
4. **Admin-Routes löschen/ändern** → Core-Funktionalität von Claude Code
5. **Auto-Detection Logik modifizieren** → Kritische Funktion für Modul-Recovery

### Sichere Bereiche für Cursor-Entwicklung:

✅ **Templates/Frontend** (außer admin/users.html, admin/modules.html Subscription-Checkboxen)
✅ **Neue Features** (solange keine Core-Funktionen überschrieben werden)
✅ **Styling/CSS** (keine Einschränkungen)
✅ **Analytics** (VisitorAnalytics Model und Tracking)
✅ **Neue Routes** (außer /admin/* Namespace)

---

## 📚 WICHTIGE FILE-LOCATIONS

**Geänderte Files:**
- `app.py` (Zeilen: 209-212, 362-381, 399-402, 2376-2386, 5188-5532)
- `templates/admin/users.html` (NEU, 388 Zeilen)
- `templates/admin/modules.html` (Zeilen: 55-60, 624-649)
- `templates/base.html` (User-Link in Navigation)

**Kritische Funktionen:**
- `init_modules_on_startup()` - app.py:209
- `sync_modules_from_local()` - app.py:3938
- `admin_register_missing_modules()` - app.py:5437
- `SubscriptionType` Enum - app.py:362
- `User.can_access_module()` - app.py:410
- `AdminAuditLog` Model - app.py:418

---

## 🎯 SUMMARY FÜR CURSOR

**Claude Code hat implementiert:**
1. ✅ 4-Tier Subscription System (FREE, PREMIUM, ELITE, ELITE_PRO)
2. ✅ User Management mit Admin-UI
3. ✅ Persistentes Modul-Management (Auto-Sync DEAKTIVIERT)
4. ✅ Automatische Erkennung fehlender Module
5. ✅ Admin Audit Logging
6. ✅ PostgreSQL Migration

**Cursor muss beachten:**
- 🚫 Kein Auto-Sync reaktivieren
- 🚫 Keine Subscription Levels entfernen
- 🚫 Keine Admin-Routes löschen
- ✅ Bei Unsicherheit: User fragen
- ✅ Diese Rules befolgen

**Bei Fragen oder Konflikten:**
→ User konsultieren
→ Claude Code hat Vorrang für alle oben beschriebenen Features
