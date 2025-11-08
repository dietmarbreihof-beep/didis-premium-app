#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sammel-Migration: Registriert alle 12 neuen Lernmodule
Erstellt: 8. November 2025
"""

import sys
import os

# Füge Parent-Directory zum Python-Path hinzu
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, LearningModule, ModuleCategory, ModuleSubcategory
from datetime import datetime
import json

def register_all_new_modules():
    """Registriert alle 12 neuen Lernmodule in der Datenbank"""
    
    with app.app_context():
        print("=" * 80)
        print("SAMMEL-MIGRATION: Alle neuen Module registrieren")
        print("=" * 80)
        
        # Modul-Definitionen
        modules = [
            {
                'title': '99% Noise vs. 0,1% Edge',
                'slug': 'noise-vs-edge',
                'description': 'Lerne die Kunst der Setup-Selektion. Die überwältigende Mehrheit der Marktbewegungen sind nur Noise - finde die 0,1% Edge-Setups, die wirklich profitabel sind.',
                'icon': '🎰',
                'template_file': 'noise-vs-edge.html',
                'category_name': 'Trading Konzepte',
                'estimated_duration': 30,
                'difficulty_level': 'intermediate',
                'required_subscription_levels': ["premium", "elite", "elite_pro", "masterclass"]
            },
            {
                'title': 'Defining Trend - Die Kunst der Trend-Erkennung',
                'slug': 'defining-trend',
                'description': 'Basierend auf Lance Breitstein\'s Trading-Philosophie: Lerne wie professionelle Trader Trends definieren, nutzen und davon profitieren. Mit VWAP, MAs, Prior Bars und Multi-Timeframe-Alignment.',
                'icon': '📈',
                'template_file': 'defining-trend.html',
                'category_name': 'Technische Analyse',
                'estimated_duration': 45,
                'difficulty_level': 'intermediate',
                'required_subscription_levels': ["premium", "elite", "elite_pro", "masterclass"]
            },
            {
                'title': 'Risikomanagement: Dein Überlebensguide',
                'slug': 'risikomanagement',
                'description': 'Die nicht verhandelbare Grundlage für langfristigen Trading-Erfolg. Verstehe Loss Limits, Position Sizing, die brutale Mathematik des Verlierens und die Psychologie des Risikomanagements.',
                'icon': '⚡',
                'template_file': 'risikomanagement.html',
                'category_name': 'Risikomanagement',
                'estimated_duration': 45,
                'difficulty_level': 'beginner',
                'required_subscription_levels': ["premium", "elite", "elite_pro", "masterclass"]
            },
            {
                'title': 'Daily Report Card',
                'slug': 'daily-report-card',
                'description': 'Tracke deine Trading-Performance systematisch. Tägliche Selbstreflexion und Auswertung für kontinuierliche Verbesserung.',
                'icon': '📊',
                'template_file': 'daily_report_card_lernseite.html',
                'category_name': 'Trading Tools',
                'estimated_duration': 25,
                'difficulty_level': 'beginner',
                'required_subscription_levels': ["premium", "elite", "elite_pro", "masterclass"]
            },
            {
                'title': 'Darwin Investing',
                'slug': 'darwin-investing',
                'description': 'Evolution-basierte Investmentstrategien. Wie natürliche Selektion im Markt funktioniert und wie du davon profitieren kannst.',
                'icon': '🦎',
                'template_file': 'darwin_investing.html',
                'category_name': 'Fundamentalanalyse',
                'estimated_duration': 40,
                'difficulty_level': 'advanced',
                'required_subscription_levels': ["premium", "elite", "elite_pro", "masterclass"]
            },
            {
                'title': 'Trading-Archetypen',
                'slug': 'trading-archetypen',
                'description': 'Finde deinen persönlichen Trading-Stil. Welcher Archetyp bist du? Scalper, Swing-Trader, Investor oder Hybrid?',
                'icon': '👤',
                'template_file': 'trading_archetypen.html',
                'category_name': 'Psychologie & Mindset',
                'estimated_duration': 30,
                'difficulty_level': 'beginner',
                'required_subscription_levels': ["premium", "elite", "elite_pro", "masterclass"]
            },
            {
                'title': 'Finde deinen Trading-Weg',
                'slug': 'finde-deinen-trading-weg',
                'description': 'Persönliche Strategie-Entwicklung. Ein strukturierter Ansatz, um DEINEN optimalen Trading-Stil zu finden.',
                'icon': '🧭',
                'template_file': 'finde_deinen_trading_weg.html',
                'category_name': 'Getting Started',
                'estimated_duration': 35,
                'difficulty_level': 'beginner',
                'required_subscription_levels': ["premium", "elite", "elite_pro", "masterclass"]
            },
            {
                'title': 'Die Wahrheit über die Lernkurve',
                'slug': 'die-wahrheit-lernkurve',
                'description': 'Realistische Erwartungen für Trading-Anfänger. Wie lange dauert es wirklich profitabel zu werden? Was sind die typischen Phasen?',
                'icon': '📚',
                'template_file': 'die_wahrheit_lernkurve.html',
                'category_name': 'Psychologie & Mindset',
                'estimated_duration': 30,
                'difficulty_level': 'beginner',
                'required_subscription_levels': ["premium", "elite", "elite_pro", "masterclass"]
            },
            {
                'title': 'Positioning & Risikomanagement',
                'slug': 'positioning-risikomanagement',
                'description': 'Fortgeschrittene Konzepte zu Position Sizing und Risk Management. Für erfahrene Trader die ihr Risikomanagement optimieren wollen.',
                'icon': '🎯',
                'template_file': 'positioning_risikomanagement.html',
                'category_name': 'Risikomanagement',
                'estimated_duration': 40,
                'difficulty_level': 'advanced',
                'required_subscription_levels': ["elite", "elite_pro", "masterclass"]
            },
            {
                'title': 'Meta-Learning Quiz',
                'slug': 'meta-learning-quiz',
                'description': 'Teste dein Trading-Wissen. Interaktives Quiz über alle wichtigen Trading-Konzepte mit sofortigem Feedback.',
                'icon': '🧠',
                'template_file': 'meta_learning_quiz.html',
                'category_name': 'Interaktive Quizzes',
                'estimated_duration': 20,
                'difficulty_level': 'intermediate',
                'required_subscription_levels': ["premium", "elite", "elite_pro", "masterclass"]
            },
            {
                'title': 'KGV & PEG Trading',
                'slug': 'kgv-peg-trading',
                'description': 'Fundamentalanalyse für Trader. Lerne wie du KGV (P/E Ratio) und PEG nutzt, um unterbewertete Aktien zu finden.',
                'icon': '💼',
                'template_file': 'kgv-peg-trading-lernseite-debugged.html',
                'category_name': 'Fundamentalanalyse',
                'estimated_duration': 35,
                'difficulty_level': 'intermediate',
                'required_subscription_levels': ["premium", "elite", "elite_pro", "masterclass"]
            },
            {
                'title': 'Poker vs. Trading - Denkweisen im Vergleich',
                'slug': 'poker-cards-comparison',
                'description': 'Kostenloser Einblick: Was haben Poker und Trading gemeinsam? Lerne die wichtigsten mentalen Konzepte aus beiden Welten.',
                'icon': '🃏',
                'template_file': 'poker-cards-comparison.html',
                'category_name': 'Lead-Magnets',
                'estimated_duration': 15,
                'difficulty_level': 'beginner',
                'required_subscription_levels': [],  # Lead-Magnet - kostenlos!
                'is_lead_magnet': True
            }
        ]
        
        registered_count = 0
        updated_count = 0
        
        for module_data in modules:
            try:
                # Prüfe ob Modul bereits existiert
                existing = LearningModule.query.filter_by(slug=module_data['slug']).first()
                
                if existing:
                    print(f"[UPDATE] {module_data['title']}")
                    # Update existierendes Modul
                    existing.title = module_data['title']
                    existing.description = module_data['description']
                    existing.icon = module_data['icon']
                    existing.template_file = module_data['template_file']
                    existing.estimated_duration = module_data['estimated_duration']
                    existing.difficulty_level = module_data['difficulty_level']
                    existing.required_subscription_levels = json.dumps(module_data['required_subscription_levels'])
                    if 'is_lead_magnet' in module_data:
                        existing.is_lead_magnet = module_data['is_lead_magnet']
                    existing.updated_at = datetime.utcnow()
                    updated_count += 1
                else:
                    # Finde oder erstelle Kategorie
                    category = ModuleCategory.query.filter_by(name=module_data['category_name']).first()
                    if not category:
                        print(f"[INFO] Kategorie '{module_data['category_name']}' nicht gefunden - nutze 'Neue Module'")
                        # Fallback: "Neue Module" Kategorie
                        category = ModuleCategory.query.filter_by(slug='neue-module').first()
                        if not category:
                            print("[ERROR] 'Neue Module' Kategorie fehlt! Führe zuerst app.py aus.")
                            continue
                    
                    # Erstelle neues Modul
                    print(f"[NEW] {module_data['title']}")
                    new_module = LearningModule(
                        category_id=category.id,
                        subcategory_id=None,
                        title=module_data['title'],
                        slug=module_data['slug'],
                        description=module_data['description'],
                        icon=module_data['icon'],
                        template_file=module_data['template_file'],
                        content_type='html',
                        is_published=False,  # Manual review erforderlich
                        is_lead_magnet=module_data.get('is_lead_magnet', False),
                        required_subscription_levels=json.dumps(module_data['required_subscription_levels']),
                        sort_order=100,
                        estimated_duration=module_data['estimated_duration'],
                        difficulty_level=module_data['difficulty_level'],
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    db.session.add(new_module)
                    registered_count += 1
                
                db.session.commit()
                
            except Exception as e:
                print(f"[ERROR] Fehler bei {module_data['slug']}: {str(e)}")
                db.session.rollback()
                continue
        
        print("\n" + "=" * 80)
        print("MIGRATION ABGESCHLOSSEN")
        print("=" * 80)
        print(f"Neue Module: {registered_count}")
        print(f"Aktualisierte Module: {updated_count}")
        print(f"\nNächste Schritte:")
        print("1. Gehe zu /admin/modules")
        print("2. Verschiebe Module aus '🆕 Neue Module' in richtige Kategorien")
        print("3. Setze is_published=True für veröffentlichung")
        print()
        
        return True

if __name__ == '__main__':
    print("\n🚀 Starte Sammel-Migration...\n")
    success = register_all_new_modules()
    
    if success:
        print("✅ ERFOLG! Alle Module registriert.")
    else:
        print("❌ FEHLER! Migration fehlgeschlagen.")
        sys.exit(1)

