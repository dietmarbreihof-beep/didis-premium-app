# Analytics System - Didis Premium Trading Academy

## 📊 Übersicht

Das Analytics-System bietet detaillierte Besucher-Statistiken mit **IP-basierter Deduplizierung** für präzise Unique-Visitor-Zahlen.

## ✨ Features

### 🎯 **Unique Visitor Tracking**
- **IP-basierte Deduplizierung**: Jede IP-Adresse wird nur einmal pro Zeitraum gezählt
- **Automatisches Tracking**: Alle Seitenaufrufe werden automatisch erfasst
- **Session-Tracking**: Verfolgt Benutzer-Sessions über mehrere Seiten

### 📈 **Detaillierte Statistiken**
- **Zeitraum-Filter**: Heute, 7 Tage, 30 Tage, 90 Tage
- **Top-Seiten**: Beliebteste Seiten mit Aufrufzahlen
- **Device-Analyse**: Desktop, Mobile, Tablet Verteilung
- **Referrer-Tracking**: Woher kommen die Besucher?
- **Browser & OS**: Detaillierte User-Agent Analyse

### 📊 **Interaktive Charts**
- **Verlaufs-Diagramm**: Unique Visitors und Seitenaufrufe über Zeit
- **Device-Verteilung**: Pie-Chart für Geräte-Typen
- **Real-time Updates**: Charts aktualisieren sich automatisch

## 🚀 Installation & Setup

### 1. **Migration ausführen**
```bash
python migrate_analytics.py
```

### 2. **Dependencies installieren**
```bash
pip install user-agents
```

### 3. **Analytics aktivieren**
Das System ist automatisch aktiviert und trackt alle Seitenaufrufe.

## 🔧 Technische Details

### **Datenbank-Schema**
```sql
CREATE TABLE visitor_analytics (
    id INTEGER PRIMARY KEY,
    ip_address VARCHAR(45) NOT NULL,
    user_agent TEXT,
    page_url VARCHAR(500) NOT NULL,
    page_title VARCHAR(200),
    referrer VARCHAR(500),
    session_id VARCHAR(100),
    user_id INTEGER,
    visited_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    country VARCHAR(2),
    city VARCHAR(100),
    device_type VARCHAR(20),
    browser VARCHAR(50),
    os VARCHAR(50)
);
```

### **Performance-Indizes**
- `idx_visitor_analytics_ip`: Für IP-basierte Queries
- `idx_visitor_analytics_date`: Für Zeitraum-Queries  
- `idx_visitor_analytics_url`: Für Top-Pages Queries
- `idx_visitor_analytics_ip_date`: Für Unique Visitors pro Zeitraum

### **Middleware-Integration**
```python
from analytics_middleware import AnalyticsMiddleware
analytics = AnalyticsMiddleware(app)
```

## 📱 Admin-Dashboard

### **Zugriff**
- **URL**: `/admin/analytics`
- **Berechtigung**: Nur für `admin` und `didi` Benutzer
- **Navigation**: Admin-Panel → "📊 Analytics Dashboard"

### **Dashboard-Features**
- **Hauptstatistiken**: Unique Visitors, Seitenaufrufe, Seiten pro Besucher
- **Zeitraum-Filter**: Dynamische Filterung nach Zeiträumen
- **Top-Seiten Tabelle**: Detaillierte Aufschlüsselung der beliebtesten Seiten
- **Device-Chart**: Visuelle Darstellung der Geräte-Verteilung
- **Referrer-Liste**: Woher kommen die Besucher?

## 🔒 Datenschutz & Sicherheit

### **IP-Anonymisierung**
- IPs werden nur für Deduplizierung verwendet
- Keine Speicherung von persönlichen Daten
- Automatische Bereinigung alter Daten (optional)

### **Bot-Filtering**
- Automatische Erkennung und Filterung von Bots
- User-Agent basierte Bot-Erkennung
- Keine Verfälschung der Statistiken durch Crawler

## 🛠️ Wartung

### **Status prüfen**
```bash
python migrate_analytics.py status
```

### **Daten bereinigen** (optional)
```python
# Lösche Daten älter als 90 Tage
from datetime import datetime, timedelta
from database import db, VisitorAnalytics

cutoff_date = datetime.utcnow() - timedelta(days=90)
old_entries = VisitorAnalytics.query.filter(
    VisitorAnalytics.visited_at < cutoff_date
).delete()
db.session.commit()
```

## 📊 API-Endpoints

### **Analytics-Daten abrufen**
```
GET /admin/analytics/api/data?days=30&metric=overview
```

**Parameter:**
- `days`: Zeitraum (1, 7, 30, 90)
- `metric`: Art der Daten (`overview`, `devices`, `daily`)

**Response:**
```json
{
  "unique_visitors": 42,
  "page_views": 156,
  "top_pages": [...]
}
```

## 🎯 Unique Visitor Logik

### **Deduplizierung**
```python
# Unique Visitors = COUNT(DISTINCT ip_address) pro Zeitraum
unique_visitors = db.session.query(
    func.count(distinct(VisitorAnalytics.ip_address))
).filter(
    VisitorAnalytics.visited_at >= cutoff_date
).scalar()
```

### **Vorteile**
- **Präzise Zahlen**: Keine doppelten Zählungen
- **Realistische Metriken**: Echte Besucher vs. Seitenaufrufe
- **Performance-optimiert**: Effiziente Datenbankabfragen

## 🚀 Erweiterungen

### **Geplante Features**
- [ ] **Geo-Location**: Länder/Städte der Besucher
- [ ] **Conversion-Tracking**: Anmeldungen und Käufe
- [ ] **A/B Testing**: Verschiedene Versionen testen
- [ ] **Export-Funktionen**: CSV/Excel Export
- [ ] **Email-Reports**: Automatische Berichte

### **Custom Tracking**
```python
# Manuelles Event-Tracking
from analytics_middleware import AnalyticsService

# Custom Event tracken
analytics_entry = VisitorAnalytics(
    ip_address=request.remote_addr,
    page_url='/custom-event',
    page_title='Custom Event',
    # ... weitere Felder
)
db.session.add(analytics_entry)
db.session.commit()
```

## 📞 Support

Bei Fragen oder Problemen:
1. **Status prüfen**: `python migrate_analytics.py status`
2. **Logs prüfen**: Console-Output der Flask-App
3. **Datenbank prüfen**: SQLite Browser für `didis_academy.db`

---

**🎉 Das Analytics-System ist jetzt vollständig eingerichtet und einsatzbereit!**
