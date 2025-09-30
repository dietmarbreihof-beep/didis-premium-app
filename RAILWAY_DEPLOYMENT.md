
# Trading-Playbook Masterclass - Railway Deployment

## 1. Template-Datei hochladen
- Kopiere `templates/trading_playbook_masterclass.html` in dein Railway-Repository
- Stelle sicher, dass das Template im `templates/` Ordner liegt

## 2. Route-Code hinzufügen
Füge folgende Route in deine `app.py` ein:

```python
@app.route('/trading-playbook-masterclass')
def trading_playbook_masterclass():
    # [Route-Code aus lokaler app.py kopieren]
    # ...
```

## 3. Kategorie-Definition aktualisieren
In der `find_or_create_category_for_module` Funktion:

```python
'elite-system-iii': {'name': '5. Elite - System III', 'icon': '👑', 'order': 5}
```

## 4. Trading-Tools aktualisieren
Füge in der `trading_tools()` Route hinzu:

```python
{
    'title': 'Trading-Playbook Masterclass',
    'description': 'Die ultimative Masterclass über Metalearning und den Trading-Prozess.',
    'icon': '👑',
    'url': '/trading-playbook-masterclass',
    'status': 'available',
    'required_subscription': ['elite'],
    'estimated_time': '120 min',
    'difficulty': 'Expert',
    'category': 'Elite - System III'
}
```

## 5. Deployment ausführen
```bash
# Im Railway-Repository
python deploy_masterclass.py
```

## 6. Testen
- URL aufrufen: `https://your-app.railway.app/trading-playbook-masterclass`
- Admin-Login: Modul sollte unter "5. Elite - System III" erscheinen
- Funktionalität: Quiz und interaktive Elemente testen

## 7. Überprüfen
- Navigation: Modul in Hauptnavigation sichtbar
- Zugriff: Nur Elite-Member haben Zugriff
- Mobile: Responsive Design funktioniert
