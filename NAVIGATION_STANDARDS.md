# 📍 Navigation-Standards für alle Module

## 🎯 Übersicht
Alle Module in der Didis Premium Trading Academy verwenden eine einheitliche Navigation, um eine konsistente Benutzererfahrung zu gewährleisten.

## 🔧 Implementierung

### Für Flask-Templates (Empfohlen)
```html
<!-- Am Ende des Moduls, vor dem schließenden Tag -->
{% include '_navigation.html' %}
```

### Für Standalone HTML-Dateien
```html
<!-- Navigation für standalone HTML -->
<div class="module-navigation">
    <a href="/">🏠 Startseite</a>
    <a href="/modules">📚 Alle Module</a>
    <a href="/admin/modules" id="admin-link" style="display: none;">🔧 Admin</a>
    <a href="https://didis-trading-club.streamlit.app/" target="_blank">🚀 Zur Hauptapp</a>
</div>

<div style="text-align: center; margin-top: 30px; color: #666; padding: 20px;">
    <p><strong>Didis Premium Trading Academy</strong></p>
    <p>📍 Heidelberg | 📊 30+ Jahre Börsenerfahrung</p>
</div>

<script>
// Admin-Link nur für admin/didi anzeigen
fetch('/api/check-admin')
    .then(response => response.json())
    .then(data => {
        if (data.isAdmin) {
            document.getElementById('admin-link').style.display = 'inline-block';
        }
    })
    .catch(error => {
        console.log('Admin-Check nicht verfügbar:', error);
        // Fallback: Admin-Link ausblenden für standalone HTML
        document.getElementById('admin-link').style.display = 'none';
    });
</script>

<!-- CSS falls nicht in Template enthalten -->
<style>
.module-navigation {
    text-align: center;
    margin: 40px 0 20px 0;
    padding: 20px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.module-navigation a {
    color: #b8860b;
    text-decoration: none;
    margin: 0 15px;
    font-weight: 600;
    padding: 10px 15px;
    border-radius: 8px;
    transition: all 0.3s ease;
    display: inline-block;
}

.module-navigation a:hover {
    color: #daa520;
    background: #f7f7f7;
    transform: translateY(-2px);
}

@media (max-width: 768px) {
    .module-navigation a {
        display: block;
        margin: 5px 0;
    }
}
</style>
```

## 🚀 Navigation-Elemente

### Hauptnavigation (Alle Module)
- **🏠 Startseite** → `{{ url_for('home') }}` oder `/`
- **📚 Alle Module** → `{{ url_for('modules') }}` oder `/modules`
- **🚀 Zur Hauptapp** → `https://didis-trading-club.streamlit.app/` (neues Fenster)

### Admin-Navigation (Nur für admin/didi)
- **🔧 Admin** → `{{ url_for('admin_modules') }}` oder `/admin/modules`

## 🔒 Admin-Zugriffskontrolle

### In Flask-Templates
```html
{% if session.get('logged_in') and session.get('user', {}).get('username') in ['admin', 'didi'] %}
    <a href="{{ url_for('admin_modules') }}">🔧 Admin</a>
{% endif %}
```

### In JavaScript (Standalone HTML)
```javascript
fetch('/api/check-admin')
    .then(response => response.json())
    .then(data => {
        if (data.isAdmin) {
            document.getElementById('admin-link').style.display = 'inline-block';
        }
    });
```

## 📱 Responsive Design
Die Navigation passt sich automatisch an verschiedene Bildschirmgrößen an:
- **Desktop**: Horizontal angeordnete Links
- **Mobile**: Vertikal gestapelte Links

## 🎨 Styling-Standards

### Farben
- **Standard**: `#b8860b` (Gold-dunkel)
- **Hover**: `#daa520` (Gold-klassisch)
- **Background**: `white` mit Schatten

### Abstände
- **Margin**: `40px 0 20px 0`
- **Padding**: `20px` für Container, `10px 15px` für Links
- **Border-Radius**: `12px` für Container, `8px` für Links

## 📋 Checkliste für neue Module

- [ ] Navigation am Ende des Moduls eingefügt
- [ ] Admin-Link nur für berechtigte User sichtbar
- [ ] Responsive Design getestet
- [ ] Links funktionieren korrekt
- [ ] Styling konsistent mit anderen Modulen

## 🔄 Automatische Updates
Änderungen an der Navigation werden automatisch in allen Modulen übernommen, die `{% include '_navigation.html' %}` verwenden.

## 🛠️ Wartung
- **Navigation-Template**: `templates/_navigation.html`
- **API-Route**: `/api/check-admin` in `app.py`
- **Admin-Logik**: `session.get('user', {}).get('username') in ['admin', 'didi']`

## 📞 Support
Bei Problemen mit der Navigation wende dich an das Entwicklerteam oder prüfe die bestehenden Module als Referenz.


