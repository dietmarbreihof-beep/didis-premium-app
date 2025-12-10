# 🚀 Cursor Shortcuts für Didis Premium Trading Academy

## 📋 Was sind Cursor Shortcuts?

**Cursor Shortcuts** sind vorgefertigte Prompt-Templates, die du einfach in den Cursor Chat kopierst, um häufige Aufgaben schnell zu erledigen. Sie folgen alle Best Practices und Projekt-Standards.

### 🎯 **Verwendung:**
1. Kopiere den Shortcut-Text (nach dem `→`) aus diesem Dokument
2. Füge ihn in den Cursor Chat ein
3. Passe optional die Parameter an (z.B. Modul-Name, Datei-Pfad)
4. Cursor führt die Aufgabe automatisch aus

### 💡 **Vorteile:**
- ✅ Schneller als manuelles Tippen
- ✅ Folgt automatisch allen Projekt-Standards
- ✅ Konsistente Ergebnisse
- ✅ Weniger Fehler durch vorgefertigte Patterns

### 📖 **Beispiele:**
- `@new-module-page` → Erstellt sofort eine vollständige Modul-Seite mit Design-System
- `@register-module` → Registriert ein Modul in der Datenbank
- `@fix-du-anrede` → Korrigiert alle "Sie"-Anreden zu "Du"

---

---

## 🎨 DESIGN & STYLING

### @design-system
→ Verwende das Gold-Premium-Design-System: Primärfarben #1a1a1a/#2d2d2d, Akzentfarben #b8860b/#daa520/#f4e97b, Border-Radius 12px, Schatten 0 4px 20px rgba(0,0,0,0.1), Inter Font, immer "Du"-Anrede, Glasmorphismus-Effekte, Gold-Hover-Transitions 0.3s ease

### @fix-page-display
→ Analysiere die HTML-Seite und korrigiere: 1) CSS-Wrapper-Div für Klassenanwendung, 2) HTML-Strukturfehler, 3) Persönliche "Du"-Anrede (nie "Sie"), 4) Browser-Kompatibilität (-webkit-Präfixe), 5) Accessibility (aria-labels, title), 6) Responsive Design (Mobile/Tablet)

### @premium-card
→ Erstelle eine Premium-Karte: weißer Hintergrund, padding 30px, border-radius 12px, box-shadow 0 4px 20px rgba(0,0,0,0.1), border-left 4px solid #daa520, hover: translateY(-2px) + stärkerer Schatten, smooth transition 0.3s ease

### @gold-button
→ Erstelle einen Gold-Premium-Button: background linear-gradient(135deg, #daa520 0%, #b8860b 100%), color white, padding 15px 40px, border-radius 12px, font-weight 700, hover: transform scale(1.05) + box-shadow 0 8px 30px rgba(184,134,11,0.4), transition 0.3s ease

---

## 📄 HTML-SEITEN

### @new-module-page
→ Erstelle eine neue HTML-Modul-Seite basierend auf dem Design-System: 1) extends "base.html", 2) Wrapper-Div mit Klasse für CSS-Scoping, 3) Hero-Header mit Primär-Verlauf, 4) Content-Cards mit Gold-Akzenten, 5) Responsive Grid-Layout, 6) Navigation-Include am Ende, 7) JavaScript für Interaktivität, 8) "Du"-Anrede durchgängig

### @fix-du-anrede
→ Korrigiere ALLE "Sie/Ihr/Ihnen/Ihrem" zu "du/dein/dir/deinem" in dieser Datei. Verwende konsequent die persönliche "Du"-Anrede gemäß Cursor Rules. Prüfe auch Platzhalter-Texte und Beschreibungen.

### @add-navigation
→ Füge die einheitliche Navigation hinzu: {% include '_navigation.html' %} vor {% endblock %}, stelle sicher dass Prev/Next-Module korrekt verlinkt sind

---

## 🗄️ DATENBANK & MODULE

### @register-module
→ Registriere ein neues Modul in der Datenbank: 1) Füge Eintrag in database.py zur MODULES-Liste hinzu mit korrekter category/subcategory/order, 2) Erstelle HTML-Template mit Design-System, 3) Teste Route mit /module/slug, 4) Füge zu Navigation hinzu

### @create-migration
→ Erstelle ein Migrations-Script in migrations/: 1) Import app und db, 2) with app.app_context(), 3) Prüfe ob Modul existiert, 4) Erstelle/Update Module-Eintrag, 5) db.session.commit(), 6) Fehlerbehandlung mit try/except

### @fix-database
→ Analysiere Datenbank-Probleme: 1) Prüfe didis_academy.db Existenz, 2) Verifiziere Module-Einträge, 3) Checke Fremdschlüssel-Constraints, 4) Teste User-Subscription-Links, 5) Führe init_db.py bei Bedarf aus

---

## 📊 TRADING-FEATURES

### @avwap-implementation
→ Implementiere AVWAP-Feature: 1) yfinance für Daten, 2) Pandas für Berechnungen, 3) Plotly für interaktive Charts, 4) Support/Resistance-Level markieren, 5) Gold-Design für Chart-Theme, 6) Responsive Canvas

### @portfolio-analyzer
→ Erstelle Portfolio-Analyzer: 1) Input-Slider mit Gold-Design, 2) Pie-Chart mit Plotly, 3) Asset-Allocation-Berechnung, 4) Regime-basierte Empfehlungen, 5) Live-Update bei Slider-Änderung, 6) Balance-Validierung (100%)

### @market-regime
→ Implementiere Marktregime-Analyse: 1) 4 Regime (Goldilocks/Reflation/Inflation/Deflation), 2) Asset-Klassen-Empfehlungen, 3) Farbcodierung (Grün=Preferred, Gelb=Neutral, Rot=Avoid), 4) Sector-Performance-Tabelle, 5) Dynamic Updates

---

## 📚 LERNMODULE

### @progressive-disclosure
→ Erstelle Progressive-Disclosure-Modul: 1) Session-State für current_step, 2) Jeder Schritt nur sichtbar wenn current_step >= X, 3) Next-Button nur bei current_step == X, 4) Bereits abgeschlossene Schritte bleiben sichtbar, 5) Quiz nach jedem Schritt, 6) Key Takeaways am Ende
→ Füge Quiz hinzu: 1) st.expander für kompakte Darstellung, 2) st.radio für Multiple-Choice, 3) Eindeutige keys (quiz_X_Y), 4) Score-Berechnung, 5) Instant-Feedback mit st.success/warning, 6) Motivierende Emojis (🎉/👍/📖)

### @interactive-charts
→ Erstelle interaktive Trading-Charts: 1) Plotly für Interaktivität, 2) Candlestick oder Line-Chart, 3) AVWAP-Overlays, 4) Support/Resistance-Linien, 5) Hover-Tooltips, 6) Gold-Color-Theme, 7) Responsive sizing

---

## 🚀 DEPLOYMENT & GIT

### @git-push-railway
→ Synchronisiere mit Railway: 1) cd ins Projektverzeichnis, 2) git add [geänderte Dateien], 3) git commit -m "Beschreibung", 4) git push origin main, 5) Warte 3-5 Minuten für Deployment

### @fix-deployment
→ Debugge Railway-Deployment: 1) Prüfe railway.toml Konfiguration, 2) Checke requirements.txt Dependencies, 3) Verifiziere Procfile, 4) Teste lokalen Build, 5) Prüfe Railway-Logs, 6) Environment-Variables checken

### @commit-message
→ Erstelle strukturierte Commit-Message: Fix/Feature/Refactor: [Kurzbeschreibung] - [Details zu Änderungen 1-3], Beispiel: "Fix: Marktampel-Seite - CSS-Wrapper, Du-Anrede, Safari-Support"

---

## 🔧 DEBUGGING & FIXES

### @debug-css
→ Debugge CSS-Probleme: 1) Prüfe CSS-Wrapper vorhanden?, 2) Verifiziere Klassenselektoren, 3) Checke Specificity-Konflikte, 4) Browser-DevTools für Applied Styles, 5) Responsive-Breakpoints testen

### @fix-javascript
→ Debugge JavaScript-Fehler: 1) Browser-Console öffnen, 2) Syntax-Fehler prüfen, 3) Variable-Scopes checken, 4) Event-Listener verifizieren, 5) Async/Await-Handling, 6) Console.log für Debugging

### @accessibility-check
→ Prüfe Accessibility: 1) Alt-Text für Bilder, 2) Aria-Labels für interaktive Elemente, 3) Keyboard-Navigation testen, 4) Farbkontraste (WCAG AA), 5) Screen-Reader-Test, 6) Focus-Indikatoren

---

## 📱 RESPONSIVE DESIGN

### @mobile-optimize
→ Optimiere für Mobile: 1) Media Query @media (max-width: 768px), 2) Touch-optimierte Tap-Bereiche (min 44px), 3) Flex-direction: column für Stacks, 4) Font-Größen anpassen, 5) Padding/Margin reduzieren, 6) Hamburger-Menü

### @tablet-layout
→ Optimiere für Tablet: 1) Grid-Columns von 3 auf 2 reduzieren, 2) Sidebar collapsible machen, 3) Font-Größen leicht anpassen, 4) Touch-Gesten unterstützen

---

## 🔐 SICHERHEIT

### @security-audit
→ Führe Security-Audit durch: 1) Passwort-Hashing prüfen (werkzeug.security), 2) CSRF-Schutz aktivieren (Flask-WTF), 3) Session-Sicherheit (secure cookies), 4) SQL-Injection-Schutz (SQLAlchemy ORM), 5) Input-Validierung, 6) Environment-Variables für Secrets

### @password-security
→ Implementiere sichere Passwort-Verwaltung: 1) generate_password_hash() beim Registrieren, 2) check_password_hash() beim Login, 3) Min. 8 Zeichen Policy, 4) Passwort-Reset-Flow, 5) Rate-Limiting gegen Brute-Force

---

## 📊 ANALYTICS & TRACKING

### @add-analytics
→ Füge Analytics hinzu: 1) Page-View-Tracking, 2) User-Interaction-Events, 3) Module-Completion-Tracking, 4) Time-on-Page, 5) Database-Logging mit Timestamps

---

## 🎓 STREAMLIT-INTEGRATION

### @streamlit-module
→ Erstelle Streamlit-Modul: 1) st.set_page_config mit Custom-Theme, 2) Custom CSS für Gold-Design, 3) Session-State für Persistenz, 4) Interaktive Widgets, 5) Plotly-Charts, 6) Export-Funktionalität

---

## 💡 BEST PRACTICES

### @code-review
→ Führe Code-Review durch: 1) PEP 8 Konformität, 2) Type Hints vorhanden, 3) Docstrings für Funktionen, 4) Fehlerbehandlung mit try/except, 5) Deutsche Kommentare, 6) DRY-Prinzip (Don't Repeat Yourself)

### @performance-check
→ Optimiere Performance: 1) Lazy-Loading für Bilder, 2) CSS/JS minifizieren, 3) Database-Queries optimieren, 4) Caching implementieren, 5) Async-Loading für Heavy-Content

---

## 🆘 HÄUFIGE PROBLEME

### Problem: "Seite zerschossen"
→ @fix-page-display verwenden

### Problem: "Sie" statt "Du"
→ @fix-du-anrede verwenden

### Problem: "Modul nicht in Navigation"
→ @register-module verwenden

### Problem: "CSS wird nicht angewendet"
→ @debug-css verwenden + CSS-Wrapper prüfen

### Problem: "Railway-Deployment failed"
→ @fix-deployment verwenden

---

## 🔄 WORKFLOW-KOMBINATIONEN

### Neues Feature komplett implementieren:
1. @new-module-page
2. @register-module
3. @add-navigation
4. @git-push-railway

### Bestehende Seite fixen:
1. @fix-page-display
2. @fix-du-anrede
3. @accessibility-check
4. @git-push-railway

### Trading-Feature hinzufügen:
1. @avwap-implementation
2. @premium-card für UI
3. @interactive-charts
4. @mobile-optimize

---

## 📝 PROJEKT-SPEZIFISCHE SHORTCUTS

### @lance-kurs-module
→ Erstelle Lernmodul basierend auf Didis-Charts Kurs-Material aus "Lance Kurs für System III": 1) Extrahiere Konzepte aus .txt-Dateien, 2) Progressive Disclosure Pattern, 3) Interaktive Beispiele, 4) Quiz-Integration, 5) Key Takeaways, 6) PDF-Verlinkung

### @ev-calculator
→ Implementiere Expected Value Calculator: 1) Input-Felder für Win-Rate, Avg-Win, Avg-Loss, 2) Echtzeit-Berechnung, 3) Visualisierung mit Plotly, 4) Position-Sizing-Empfehlungen, 5) Trade-Journal-Integration

### @volume-analysis
→ Erstelle Volume-Analyse-Modul: 1) Kapitulation vs Continuation unterscheiden, 2) Breaking News Volume Pattern, 3) Interaktive Chart-Beispiele, 4) Checklist-Integration, 5) Didis-Charts Kriterien anwenden

### @momentum-burst
→ Implementiere Momentum Burst Setup-Modul: 1) Range Expansion Detection, 2) 3-5 Tage Timing-Regeln, 3) Profit-Erwartungen nach Preisklasse, 4) Mythen-Busting (52W High, 200MA, Fundamentals), 5) Trading-Checkliste, 6) Progressive Disclosure mit Quiz

---

## 🎯 TRADING-SPEZIFISCHE FEATURES

### @bollinger-bands
→ Implementiere Bollinger Bands Modul: 1) Measures of Overextension, 2) Didis-Charts Magnum Opus Checklist, 3) Interaktive BB-Visualisierung, 4) Entry/Exit-Signale, 5) Grade-System (A/B/C)

### @symmetry-analysis
→ Erstelle Symmetrie-Analyse-Tool: 1) Swing-High/Low-Erkennung, 2) Fibonacci-Retracements, 3) Pattern-Recognition, 4) QBTS-Beispiel visualisieren, 5) Didis-Charts Symmetrie-Regeln

### @position-sizing
→ Implementiere Position-Sizing-Calculator: 1) Grade-basiertes System, 2) Exponentielles Sizing, 3) Risk-Management-Rules, 4) Portfolio-Impact-Berechnung, 5) The Sizing Notecard Integration

---

## 📚 KURS-MATERIAL-INTEGRATION

### @daily-report-card
→ Erstelle Daily Report Card Feature: 1) Template-Integration, 2) Trading-Tagesbericht ausfüllbar, 3) Grade-Selbstbewertung, 4) Speicherung in Database, 5) Progress-Tracking über Zeit, 6) PDF-Export

### @monster-club-study
→ Analysiere Monsterkeulen-Fallstudie: 1) Chart-Beispiele einbinden, 2) Volume-Pattern erklärt, 3) Entry-Timing, 4) Risk-Management, 5) Interaktive Übungen

---

## 🔍 QUICK REFERENCE

**Design:** @design-system, @premium-card, @gold-button  
**HTML:** @new-module-page, @fix-du-anrede, @add-navigation  
**Trading:** @avwap-implementation, @ev-calculator, @volume-analysis  
**Git:** @git-push-railway, @commit-message  
**Debug:** @fix-page-display, @debug-css, @accessibility-check  
**Kurs:** @lance-kurs-module, @daily-report-card, @position-sizing

---

## 💾 VERWENDUNGS-BEISPIELE

**Beispiel 1: Neue Trading-Seite erstellen**
```
@new-module-page
Titel: "Bollinger Bands Mastery"
Kategorie: "Technische Analyse"
Features: Interactive Charts, Quiz, Key Takeaways
```

**Beispiel 1a: Risikomanagement Modul (Erfolgreich erstellt!)**
```
@new-module-page Risikomanagement
- HTML-Seite: templates/risikomanagement.html ✅
- Screenshot integriert: Gewinn_Verlust_Didis-Charts.jpg ✅
- Kategorie: 4. Risikomanagement ✅
- Lead-Magnet: Ja (für alle verfügbar) ✅
- Features: Interaktiver Loss-Recovery-Rechner, Key Takeaways, Progressive Disclosure
```

**Beispiel 1b: Bouncy Ball Setup (Neu erstellt!)**
```
@new-module-page Bouncy Ball Setup
- HTML-Seite: templates/bouncy-ball-setup.html ✅
- Screenshots: VVOS (3 Phasen), SMCI (2 Phasen), Ford (1 Chart) ✅
- Kategorie: Didis-Charts System III → Intraday-Setups ✅
- Premium Modul: Ja (Premium/Elite/Elite Pro) ✅
- Features: Progressive Disclosure, 4-Step-Learning, Quiz-System, Interactive Charts, Key Takeaways
- Schwierigkeit: Fortgeschritten ⭐
- Dauer: 45 Minuten
```

**Beispiel 1c: Momentum Burst (StockBee Guide)**
```
@new-module-page Momentum Burst
- HTML-Seite: templates/momentum-burst.html ✅
- Quelle: StockBee Guides/Momentum Burst/Momentum-Burst.txt ✅
- Kategorie: Trading-Setups → Momentum Trading ✅
- Premium Modul: Ja (Elite/Elite Pro) ✅
- Features: Progressive Disclosure (8 Sections), Quiz-System (5 Fragen), Trading-Checklisten, Mythen-Busting, Key Takeaways
- Schwierigkeit: Fortgeschritten ⭐⭐⭐
- Dauer: 60 Minuten
```

**Beispiel 1d: Eine Rally für jede Jahreszeit (Neu erstellt!)**
```
@new-module-page Eine Rally für jede Jahreszeit
- HTML-Seite: templates/eine-rally-fuer-jede-jahreszeit.html ✅
- Quelle: APP Didis-Chart/pages ✅
- Kategorie: Marktanalyse → Marktzyklen & Timing ✅
- Lead-Magnet: Ja (für alle verfügbar) ✅
- Features: Progressive Disclosure (6 Sections), Quiz-System (3 Fragen), Interaktive Saison-Karten, Key Takeaways
- Schwierigkeit: Anfänger ⭐
- Dauer: 20 Minuten
- Route: /eine-rally-fuer-jede-jahreszeit ✅
```

**Beispiel 1e: Wie man Trader wird (NEU - November 2025)**
```
@new-module-page Wie man Trader wird
- HTML-Seite: templates/wie-man-trader-wird.html ✅
- Quelle: StockBee Guides/How to get started/Wie_man_Trader_wird.txt ✅
- Kategorie: Trading-Psychologie → Grundlagen ✅
- Premium Modul: Ja (Premium/Elite/Elite Pro) ✅
- Features: Progressive Disclosure (7 Sections), Quiz-System (7 Fragen), Reflexions-Boxen, Checklisten, Key Takeaways
- Schwierigkeit: Anfänger ⭐
- Dauer: 45 Minuten
- Route: /wie-man-trader-wird ✅
- Kernthemen: Ziele definieren, Profit-Erwartungen, Zeit-Commitment (2-5 Jahre), Lernkosten, Kapitalanforderungen (300K+), OPM-Strategie, Zeitrahmen-Wahl
```

**Beispiel 1f: Dein Trading-Stil (NEU - November 2025)**
```
@new-module-page Dein Trading-Stil
- HTML-Seite: templates/dein-trading-stil.html ✅
- Quelle: StockBee Guides/How to get started/How to become a trader 2.txt ✅
- Kategorie: Trading-Psychologie → Grundlagen ✅
- Premium Modul: Ja (Premium/Elite/Elite Pro) ✅
- Features: Progressive Disclosure (6 Sections), Quiz-System (6 Fragen), Interaktive Style-Cards, Vergleichstabellen, Reflexions-Box
- Schwierigkeit: Anfänger ⭐
- Dauer: 35 Minuten
- Route: /dein-trading-stil ✅
- Kernthemen: Day-Trading vs Swing-Trading vs Position-Trading, 4 Entscheidungsfaktoren (Persönlichkeit/Lifestyle/Alter/Kapital), Volatilitätsrisiko, Position Sizing je Stil, Konsequenzen jedes Stils, Commitment-Entscheidung
```

**Beispiel 1g: Wie man Trader wird Teil 3 (NEU - November 2025)**
```
@new-module-page Wie man Trader wird Teil 3
- HTML-Seite: templates/wie-man-trader-wird-3.html ✅
- Quelle: StockBee Guides/How to get started/Wie_man_Trader_wird_3.txt ✅
- Kategorie: Trading-Psychologie → Grundlagen ✅
- Premium Modul: Ja (Premium/Elite/Elite Pro/Masterclass) ✅
- Features: Progressive Disclosure (6 Sections), Quiz-System (6 Fragen), Interaktive Setup-Cards, Trader-Vergleichstabelle, Vacuum-Learning-Anleitung, Checklisten
- Schwierigkeit: Anfänger ⭐
- Dauer: 40 Minuten
- Route: /wie-man-trader-wird-3 ✅
- Kernthemen: 
  • Alle erfolgreichen Trader machen dasselbe (nur mit verschiedenen Namen)
  • Day-Trading Setups: News Plays, Shorting Pumps, Breakouts/Pullbacks
  • Swing-Trading Setups: Breakouts ODER Pullbacks (VCP, TBA, TAZ = dasselbe)
  • Position-Trading: Growth Stocks, Value Stocks, Dividend Aristocrats
  • Vacuum-Learning System: 15-30 Tage intensives Sammeln = Expertise
  • Keine exotischen Techniken jagen
  • Einen Zeitrahmen wählen und DABEIBEIBEN
- Serie: Teil 3 von 3 (nach "Wie man Trader wird" und "Dein Trading-Stil")
```

**Beispiel 1h: Moving Averages - Qullamaggie's Strategie (NEU - November 2025)**
```
@new-module-page Moving Averages Qullamaggie
- HTML-Seite: templates/moving-averages-qullamaggie.html ✅
- Quelle: 2. Lance Breitstein/Moving Averages System/Moving Averages Qullamaggie´s Strategy.txt ✅
- Kategorie: Technische Analyse → Moving Averages ✅
- Premium Modul: Ja (Premium/Elite/Elite Pro/Masterclass) ✅
- Features: Progressive Disclosure (8 Sections), Quiz-System (5 Fragen), Zitat-Boxen, Vergleichstabellen, Screenshots, Key Takeaways
- Screenshots: ATEC_20MA_Surfing.png, 20SMA_Widerstand.png ✅
- Schwierigkeit: Fortgeschritten ⭐⭐
- Dauer: 45 Minuten
- Route: /moving-averages-qullamaggie ✅
- Kernthemen:
  • Was sind Moving Averages (SMA vs EMA)
  • Warum funktionieren sie? (Qullamaggie: "Maybe it's magic")
  • Die wichtigsten MAs: 10, 20, 50 SMA
  • MAs als Support & Resistance (mit Flip-Konzept)
  • Entry-Strategie: Stair-Step-Pattern
  • Exit-Strategie: Trailing mit 10/20 MA
  • Marktfilter: Wann traden, wann nicht
  • Market Wizards: Qullamaggie & Lance Breitstein
```

**Beispiel 1i: Breakout Trading Meistern (NEU - Dezember 2025)**
```
@new-module-page Breakout Trading Meistern
- HTML-Seite: templates/breakout-trading.html ✅
- Quelle: StockBee Guides/Breakout/How_to_Trade_Breakouts_part1and2.txt ✅
- Bild: Buch_Toby_Crabel.jpg (Opening Range Breakout Referenz) ✅
- Kategorie: Trading-Setups → Breakout Trading ✅
- Premium Modul: Ja (Premium/Elite/Elite Pro/Masterclass) ✅
- Features: Progressive Disclosure (8 Sections), Quiz-System (5 Fragen), Breakout-Typen-Grid, Mythen-Buster, Book Reference, Key Takeaways
- Schwierigkeit: Fortgeschritten ⭐⭐
- Dauer: 60 Minuten
- Route: /breakout-trading ✅
- Kernthemen:
  • Definition: Breakout = prozentuale Bewegung größer als letzte 2-5 Tage
  • 3 Breakout-Arten: Continuation (8-20%), Bottom Bounce (20-25%), Consolidation (40-100%)
  • Entry: NUR Tag 1 ist valide! (härteste Lektion)
  • Stop-Loss: Low of Day oder halbe Tagesrange
  • Mythen: Volumen nicht nötig, Widerstand nicht nötig
  • Haltedauer: 2-40 Tage (selbst bei 500% Moves)
  • Opening Range Breakout Technik (Toby Crabel Buch)
  • Realistische Profit-Erwartungen nach Aktienpreis
```

**Beispiel 2: Seite reparieren**
```
@fix-page-display
Datei: templates/marktampel_allokation.html
```

**Beispiel 3: Git Push**
```
@git-push-railway
Geänderte Dateien: SHORTCUTS.md (neu erstellt)
```

---

## 🎓 TIPPS

1. **Kombiniere Shortcuts:** Nutze mehrere Shortcuts nacheinander für komplexe Tasks
2. **Referenziere diese Datei:** Schreibe `@SHORTCUTS.md` im Chat für Quick-Access
3. **Customizen:** Füge eigene Shortcuts hinzu, die du häufig brauchst
4. **Versioniere:** Committe diese Datei zu Git, damit sie überall verfügbar ist

---

**Zuletzt aktualisiert:** 29. November 2025  
**Projekt:** Didis Premium Trading Academy  
**Version:** 1.0


