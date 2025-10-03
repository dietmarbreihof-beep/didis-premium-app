# 🚀 Didis Trading Academy - App starten

## Schritt-für-Schritt Anleitung

### 1. Terminal/Eingabeaufforderung öffnen
- Windows: `Win + R` → `cmd` → Enter
- Oder PowerShell: `Win + X` → Windows PowerShell

### 2. Zum App-Verzeichnis wechseln
```bash
cd "C:\Users\dietmar.breihof\OneDrive - Breihof-IT GmbH\Aktien\didis-premium-app"
```

### 3. App starten
```bash
python app.py
```

**ODER** (falls das nicht funktioniert):
```bash
python -m flask run --host=127.0.0.1 --port=5000 --debug
```

### 4. App aufrufen
- Öffnen Sie Ihren Browser
- Gehen Sie zu: **http://localhost:5000**

## 🌟 Ihre neue Börsencrash-Seite

Die neue Seite ist erreichbar unter:
**http://localhost:5000/boersencrash-maerz-2025**

## ✨ Features der Seite

### 📊 **Interaktive Lernseite**
- Hero-Section mit Crash-Statistiken
- 5 aufklappbare Themenbereiche
- Interaktive Timeline der Ereignisse
- VIX Fear-Gauge Visualisierung
- Sektor-Performance-Analyse

### 🧠 **10-Fragen Quiz**
- Multiple-Choice Format
- Sofortige Antwort-Erklärungen
- Detailliertes Ergebnis-Feedback
- Fortschritts-Tracking

### 🎯 **Pädagogische Struktur**
1. **Marktüberblick** - Crash-Verlauf und Timing
2. **Trump's Zollpolitik** - Politische Auslöser
3. **Sentiment-Indikatoren** - Angst-Messungen  
4. **Sektor-Performance** - Gewinner vs. Verlierer
5. **Quiz** - Wissenstest mit 10 Fragen
6. **Erholung & Lektionen** - Trading-Erkenntnisse

### 🎨 **Design-Features**
- Responsive Design für alle Geräte
- Gold-Akzent Farbschema (professionell)
- Smooth Animationen und Übergänge
- Glasmorphismus-Effekte bei Statistik-Karten
- Hover-Effekte und Interaktivität

## 📱 **Navigation**
- **Hauptnavigation** im Footer
- **Modul-Navigation** zwischen Lerneinheiten
- **Admin-Zugang** für Benutzer "admin" und "didi"
- **Link zur Hauptapp** (Streamlit)

## 🔧 **Falls Probleme auftreten**

### Problem: "No module named 'app'"
**Lösung:** Sie sind im falschen Verzeichnis
```bash
cd "C:\Users\dietmar.breihof\OneDrive - Breihof-IT GmbH\Aktien\didis-premium-app"
```

### Problem: "flask command not found"
**Lösung:** Nutzen Sie Python direkt:
```bash
python app.py
```

### Problem: Port bereits belegt
**Lösung:** Anderen Port nutzen:
```bash
python -c "from app import app; app.run(port=5001)"
```
Dann aufrufen unter: http://localhost:5001

## 📁 **Dateien erstellt/geändert**
- ✅ `templates/boersencrash_maerz_2025.html` - Neue Lernseite
- ✅ `app.py` - Route hinzugefügt (`/boersencrash-maerz-2025`)
- ✅ Navigation und Footer integriert
- ✅ 10 Quiz-Fragen implementiert
- ✅ Responsive Design und Animationen

## 🎯 **Kategorie-Zuordnung**
Die Seite gehört zur Kategorie: **"0. Grundlagen / Crash Beispiele"**

Viel Spaß beim Testen der neuen interaktiven Lernseite! 🎉






