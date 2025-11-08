#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scannt templates-Ordner nach Dateien ohne entsprechende Routes in app.py
"""

import os
import re

# Templates die ignoriert werden sollten (System-Templates)
SYSTEM_TEMPLATES = {
    'base.html', 'home.html', 'login.html', 'register.html', 'index.html',
    'modules_overview.html', 'module_detail.html', 'admin_modules.html',
    '_navigation.html', 'module_default.html', 'upgrade_required.html',
    'Banner5.html', 'app.py'  # app.py ist keine Template
}

SYSTEM_FOLDERS = {'admin', 'auth', 'errors', 'account', 'module', 'static', 'Screenshots', 'templates', 'Growth Inflation Quadrant'}

def scan_templates():
    """Scannt templates-Ordner nach HTML-Dateien"""
    templates = []
    templates_dir = 'templates'
    
    for filename in os.listdir(templates_dir):
        # Ignoriere System-Ordner
        if filename in SYSTEM_FOLDERS:
            continue
            
        # Ignoriere System-Templates
        if filename in SYSTEM_TEMPLATES:
            continue
            
        # Nur HTML-Dateien
        if filename.endswith('.html'):
            templates.append(filename)
    
    return sorted(templates)

def get_existing_routes():
    """Liest app.py und extrahiert alle existierenden Routes"""
    routes = set()
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Finde alle @app.route Deklarationen
            pattern = r"@app\.route\('([^']+)'\)"
            matches = re.findall(pattern, content)
            
            for match in matches:
                # Entferne Parameter wie <slug>
                route = re.sub(r'<[^>]+>', '', match)
                route = route.strip('/')
                routes.add(route)
    
    except Exception as e:
        print(f"Fehler beim Lesen von app.py: {e}")
    
    return routes

def template_to_slug(filename):
    """Konvertiert Template-Namen zu URL-Slug"""
    # Entferne .html
    slug = filename.replace('.html', '')
    
    # Spezielle Mappings
    mappings = {
        'marktampel_allokation_standalone': 'marktampel-allokation',
        'better-volume-lernseite': 'better-volume-indicator',
        'kgv-peg-trading-lernseite-debugged': 'kgv-peg-trading',
        'Position_Sizing_Kelly': 'position-sizing-kelly',
        'boersencrash_maerz_2025': 'boersencrash-maerz-2025',
        'tirone_quadrant_lines': 'tirone-quadrant-lines',
        'daily_report_card_lernseite': 'daily-report-card',
        'avwap_pinch': 'avwap-pinch',
        'ev_calculator': 'ev-calculator',
        'trading_tools': 'trading-tools',
        'trading_playbook_system_iii': 'trading-playbook-system-iii',
        'trading_playbook_masterclass': 'trading-playbook-masterclass',
        'position_sizing_abcd_calculator': 'position-sizing-abcd-calculator',
        'bridgewater_quadranten_complete': 'bridgewater-quadranten',
        'expected_value': 'expected-value',
        'magic_line': 'magic-line',
        'Playbook': 'playbook'
    }
    
    if slug in mappings:
        return mappings[slug]
    
    # Konvertiere Underscores zu Hyphens
    slug = slug.replace('_', '-')
    
    return slug.lower()

def main():
    print("=" * 80)
    print("TEMPLATE-SCAN: Fehlende Routes identifizieren")
    print("=" * 80)
    
    # 1. Templates scannen
    templates = scan_templates()
    print(f"\nGefundene Templates: {len(templates)}")
    
    # 2. Existierende Routes laden
    routes = get_existing_routes()
    print(f"Existierende Routes: {len(routes)}")
    
    # 3. Fehlende Routes identifizieren
    missing = []
    existing_mapped = []
    
    for template in templates:
        expected_slug = template_to_slug(template)
        
        # Prüfe ob Route existiert
        route_exists = False
        for route in routes:
            if expected_slug in route or route in expected_slug:
                route_exists = True
                existing_mapped.append((template, route))
                break
        
        if not route_exists:
            missing.append((template, expected_slug))
    
    # 4. Ergebnisse ausgeben
    print("\n" + "=" * 80)
    print(f"BEREITS INTEGRIERT: {len(existing_mapped)} Templates")
    print("=" * 80)
    for template, route in sorted(existing_mapped):
        print(f"  [OK] {template:50} -> /{route}")
    
    print("\n" + "=" * 80)
    print(f"FEHLENDE ROUTES: {len(missing)} Templates")
    print("=" * 80)
    
    if missing:
        for template, slug in sorted(missing):
            print(f"  [MISSING] {template:50} -> /{slug}")
        
        print("\n" + "=" * 80)
        print("NEXT STEPS:")
        print("=" * 80)
        print("1. Fuer jedes fehlende Template eine Route erstellen")
        print("2. Route NACH Zeile 1330 einfuegen (sichere Zone!)")
        print("3. Premium-Pattern verwenden (siehe meinecursorrules.md)")
        print("4. Migration erstellen fuer DB-Registrierung")
        print("5. Lokaler Test: python app.py")
        print("6. Git commit & push")
        
        print(f"\nGeschaetzte Arbeit: {len(missing)} Routes x 15 Zeilen = ~{len(missing) * 15} Zeilen Code")
    else:
        print("\nALLE TEMPLATES HABEN ROUTES! Keine Arbeit noetig.")
    
    print("\n" + "=" * 80)

if __name__ == '__main__':
    main()

