# Trading-Archetypen Modul - Installationsanleitung

## Übersicht
Dieses Dokument beschreibt die Installation des neuen Moduls "Trading-Methoden Vertiefung" (Trading-Archetypen).

## Erstellte Dateien
- **Template:** `templates/trading_archetypen.html`
- **Migrationsskript:** `migrations/add_trading_archetypen_module.py`

## Option 1: Automatische Installation via Migrationsskript

**Voraussetzungen:**
- Flask-App läuft
- Alle Dependencies aus `requirements.txt` installiert

**Ausführung:**
```bash
python3 migrations/add_trading_archetypen_module.py
```

Das Skript:
- Prüft, ob das Modul bereits existiert
- Erstellt die Kategorie "Trading-Strategien" falls nicht vorhanden
- Registriert das Modul in der Datenbank

## Option 2: Manuelle Installation über Admin-Interface

Falls das Migrationsskript nicht ausgeführt werden kann, können Sie das Modul manuell über das Admin-Interface hinzufügen:

### Schritt 1: Admin-Bereich öffnen
1. Navigieren Sie zu `/admin/modules`
2. Melden Sie sich als Administrator an

### Schritt 2: Modul hinzufügen
Klicken Sie auf "Neues Modul hinzufügen" und verwenden Sie folgende Daten:

**Moduldetails:**
- **Titel:** Trading-Methoden Vertiefung
- **Slug:** `trading-archetypen`
- **Beschreibung:** Verstehe die drei Säulen erfolgreichen Tradings: Buy & Hold, Position Trading und Swing Trading. Lerne den Keulen-Kombi-Prozess und finde deinen systematischen Edge.
- **Icon:** 🎯
- **Template-Datei:** `trading_archetypen.html`
- **Content Type:** html
- **Kategorie:** Trading-Strategien (oder Technische Analyse)
- **Unterkategorie:** (leer lassen)

**Einstellungen:**
- **Published:** ✓ Ja
- **Lead Magnet:** ✗ Nein
- **Erforderliche Subscription-Level:** premium, elite, masterclass
- **Geschätzte Dauer:** 25 Minuten
- **Schwierigkeitsgrad:** intermediate
- **Sort Order:** 100

### Schritt 3: Kategorie erstellen (falls nicht vorhanden)
Falls die Kategorie "Trading-Strategien" noch nicht existiert:

**Kategorie-Details:**
- **Name:** 1. Trading-Strategien
- **Slug:** `trading-strategien`
- **Icon:** 🎯
- **Beschreibung:** Grundlegende und fortgeschrittene Trading-Methoden und -Strategien
- **Sort Order:** 1
- **Aktiv:** ✓ Ja

## Option 3: SQL-Import (für fortgeschrittene Benutzer)

Falls direkter Datenbank-Zugriff besteht, kann das Modul auch via SQL hinzugefügt werden:

```sql
-- Kategorie erstellen (falls nicht vorhanden)
INSERT INTO module_category (name, slug, icon, description, sort_order, is_active)
VALUES ('1. Trading-Strategien', 'trading-strategien', '🎯',
        'Grundlegende und fortgeschrittene Trading-Methoden und -Strategien',
        1, 1);

-- Modul hinzufügen
INSERT INTO learning_module (
    category_id,
    title,
    slug,
    description,
    icon,
    template_file,
    content_type,
    is_published,
    is_lead_magnet,
    required_subscription_levels,
    estimated_duration,
    difficulty_level,
    sort_order,
    created_at,
    updated_at
)
SELECT
    mc.id,
    'Trading-Methoden Vertiefung',
    'trading-archetypen',
    'Verstehe die drei Säulen erfolgreichen Tradings: Buy & Hold, Position Trading und Swing Trading. Lerne den Keulen-Kombi-Prozess und finde deinen systematischen Edge.',
    '🎯',
    'trading_archetypen.html',
    'html',
    1,
    0,
    '["premium", "elite", "masterclass"]',
    25,
    'intermediate',
    100,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
FROM module_category mc
WHERE mc.slug = 'trading-strategien'
LIMIT 1;
```

## Modulinhalt

Das Modul behandelt folgende Themen:

### 1. Buy & Hold (Der geduldige Investor)
- Haltedauer: 5-10 Jahre
- Kleine Positionen (1-3% Depotgewicht)
- Long-term Compounder Growth Stocks
- Magic Line Verkaufssystem

### 2. Position Trading (Der strategische Jäger)
- Haltedauer: 3-9 Monate
- Mittlere Positionen (3-5% Depotgewicht)
- Stage 2 Trades nach Stan Weinstein
- Low-Risk Entry Points

### 3. Swing Trading (Der taktische Sprinter)
- Haltedauer: 2-14 Tage
- Keulen-Positionen (5-15% Depotgewicht)
- High Momentum Breakouts
- Keulen-Kombi-Prozess

### Zusätzliche Themen:
- Marktzyklen verstehen
- Risk Management Regeln
- Die 1%-Regel
- Chance-Risiko-Verhältnis
- Direkter Methodenvergleich

## Technische Details

**Template:** `trading_archetypen.html`
- Standalone HTML-Datei
- Verwendet didis-CHARTS Corporate Identity
- Responsive Design
- Interaktive Elemente
- Animationen und Hover-Effekte

**Design-Features:**
- Gradient-Hintergründe
- Vergleichstabellen
- Info-Cards
- Highlight-Boxen
- Risk-Warnings
- Progress-Tracking

## Verifizierung

Nach der Installation können Sie das Modul testen:

1. **Admin-Bereich:** `/admin/modules` - Modul sollte in der Liste erscheinen
2. **Modulübersicht:** `/modules` - Modul sollte sichtbar sein
3. **Direkter Zugriff:** `/module/trading-archetypen` - Modul sollte laden

## Support

Bei Fragen oder Problemen:
- Prüfen Sie die Log-Dateien der Flask-App
- Stellen Sie sicher, dass alle Dependencies installiert sind
- Überprüfen Sie die Dateirechte für das Template

## Änderungshistorie

- **2025-10-25:** Initiale Erstellung des Moduls
  - HTML-Template erstellt
  - Migrationsskript erstellt
  - Dokumentation erstellt
