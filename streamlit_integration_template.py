#!/usr/bin/env python3
"""
Streamlit-Integration Template für Didis Premium Trading Academy
Zeigt wie Streamlit-Apps in die Flask-App integriert werden können
"""

import streamlit as st
import requests
import json
from datetime import datetime

# Konfiguration
FLASK_APP_URL = "http://localhost:5000"
STREAMLIT_APP_NAME = "avwap_strategie"  # Name der Streamlit-App

def check_user_access():
    """Prüft ob User Zugriff auf das Modul hat"""
    try:
        # Session-Info aus Flask-App abrufen (vereinfacht)
        # In der Praxis würde man JWT-Tokens oder Session-Cookies verwenden
        response = requests.get(f"{FLASK_APP_URL}/api/user/session")
        if response.status_code == 200:
            user_data = response.json()
            return user_data.get('has_access', False)
    except:
        pass
    return False

def show_access_denied():
    """Zeigt Zugriff-verweigert-Seite"""
    st.error("🔒 Zugriff verweigert")
    st.markdown("""
    ### Für dieses Modul benötigen Sie ein Premium-Abonnement
    
    **Verfügbare Abonnements:**
    - 🥉 **Premium**: 30-Minuten-Depot + alle Premium-Module
    - 🥇 **Elite**: 5-Minuten-Depot + VIP-Module + persönliche Betreuung
    
    [Jetzt upgraden](http://localhost:5000/upgrade)
    """)
    
    st.markdown("---")
    st.markdown("**Oder testen Sie mit einem Demo-Account:**")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Demo Premium", type="secondary"):
            st.info("Demo-Login: premium/premium")
            
    with col2:
        if st.button("Demo Elite", type="secondary"):
            st.info("Demo-Login: elite/elite")

def main():
    """Hauptfunktion der Streamlit-App"""
    
    # Page Config
    st.set_page_config(
        page_title="AVWAP Trading Strategie",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0;">📊 AVWAP Trading Strategie</h1>
        <p style="color: white; margin: 0.5rem 0 0 0; font-size: 18px;">Advanced Volume Weighted Average Price</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Zugriff prüfen (vereinfacht - in der Praxis über Session/JWT)
    user_has_access = st.session_state.get('user_has_access', True)  # Für Demo
    
    if not user_has_access:
        show_access_denied()
        return
    
    # Sidebar mit Navigation
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        
        # Zurück zur Hauptseite
        if st.button("🏠 Zurück zur Academy", type="secondary"):
            st.markdown(f"[Zurück zur Academy]({FLASK_APP_URL})")
        
        st.markdown("---")
        
        # Modul-Progress (vereinfacht)
        st.markdown("### 📊 Fortschritt")
        progress = st.progress(0.3)
        st.caption("30% abgeschlossen")
        
        # Kapitel-Navigation
        st.markdown("### 📚 Kapitel")
        chapters = [
            "1. AVWAP Grundlagen",
            "2. Support & Resistance", 
            "3. Entry & Exit Strategien",
            "4. Live Trading Beispiele",
            "5. Quiz & Zertifikat"
        ]
        
        for i, chapter in enumerate(chapters):
            if st.button(chapter, key=f"chapter_{i}"):
                st.session_state.current_chapter = i
                st.rerun()
    
    # Hauptinhalt
    current_chapter = st.session_state.get('current_chapter', 0)
    
    if current_chapter == 0:
        show_avwap_basics()
    elif current_chapter == 1:
        show_support_resistance()
    elif current_chapter == 2:
        show_entry_exit_strategies()
    elif current_chapter == 3:
        show_live_examples()
    elif current_chapter == 4:
        show_quiz_certificate()
    
    # Footer mit Academy-Branding
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>📚 Teil der <strong>Didis Premium Trading Academy</strong></p>
        <p>🎯 Professionelle Trading-Ausbildung für nachhaltigen Erfolg</p>
    </div>
    """, unsafe_allow_html=True)

def show_avwap_basics():
    """Zeigt AVWAP Grundlagen"""
    st.markdown("## 📊 Kapitel 1: AVWAP Grundlagen")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Was ist AVWAP?
        
        **AVWAP (Advanced Volume Weighted Average Price)** ist ein dynamischer 
        Support/Resistance-Indikator, der das durchschnittliche Handelsvolumen 
        über einen bestimmten Zeitraum berücksichtigt.
        
        **Vorteile von AVWAP:**
        - ✅ Dynamische Support/Resistance-Level
        - ✅ Institutionelle Benchmark
        - ✅ Objektive Marktbewertung
        - ✅ Weniger subjektiv als traditionelle S&R
        """)
        
        # Interaktives Beispiel
        st.markdown("### 🎯 Interaktives Beispiel")
        
        # Simulierte AVWAP-Berechnung
        price_range = st.slider("Preisbereich", 100, 200, 150)
        volume = st.slider("Volumen", 1000, 10000, 5000)
        
        # Einfache AVWAP-Simulation
        avwap = price_range * (1 + volume/10000)
        
        st.metric("AVWAP", f"${avwap:.2f}")
        
        if avwap > price_range:
            st.success("📈 AVWAP über aktuellem Preis - Bullish Signal")
        else:
            st.warning("📉 AVWAP unter aktuellem Preis - Bearish Signal")
    
    with col2:
        st.markdown("### 📈 Live Chart")
        
        # Platzhalter für Chart
        st.markdown("""
        <div style="height: 300px; background: #f0f2f6; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #666;">
            📊 Live AVWAP Chart<br>
            <small>(Integration mit TradingView/Plotly)</small>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🎯 Key Takeaways")
        st.markdown("""
        - AVWAP ist ein **dynamischer** Indikator
        - Berücksichtigt **Volumen** und **Zeit**
        - Wird von **Institutionen** als Benchmark genutzt
        - Weniger **subjektiv** als traditionelle S&R
        """)

def show_support_resistance():
    """Zeigt Support & Resistance mit AVWAP"""
    st.markdown("## 📈 Kapitel 2: Support & Resistance")
    
    st.markdown("""
    ### AVWAP als dynamischer Support/Resistance
    
    **Traditionelle S&R vs. AVWAP:**
    
    | Aspekt | Traditionell | AVWAP |
    |--------|-------------|-------|
    | **Art** | Statisch | Dynamisch |
    | **Berechnung** | Subjektiv | Objektiv |
    | **Volumen** | Ignoriert | Berücksichtigt |
    | **Institutionen** | Weniger relevant | Benchmark |
    """)
    
    # Interaktive S&R-Demo
    st.markdown("### 🎮 Interaktive Demo")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📊 Aktueller Preis:**")
        current_price = st.number_input("Preis", value=150.0, step=0.1)
    
    with col2:
        st.markdown("**📈 AVWAP:**")
        avwap_price = st.number_input("AVWAP", value=148.5, step=0.1)
    
    with col3:
        st.markdown("**🎯 Signal:**")
        if current_price > avwap_price:
            st.success("🟢 BULLISH")
            st.caption("Preis über AVWAP")
        else:
            st.error("🔴 BEARISH") 
            st.caption("Preis unter AVWAP")
    
    # Trading-Strategie
    st.markdown("### 💡 Trading-Strategie")
    
    if current_price > avwap_price:
        st.info("""
        **🟢 Bullish Setup:**
        - AVWAP als Support nutzen
        - Bei Rückkehr zu AVWAP kaufen
        - Stop-Loss unter AVWAP
        """)
    else:
        st.warning("""
        **🔴 Bearish Setup:**
        - AVWAP als Resistance nutzen
        - Bei Annäherung an AVWAP verkaufen
        - Stop-Loss über AVWAP
        """)

def show_entry_exit_strategies():
    """Zeigt Entry & Exit Strategien"""
    st.markdown("## 🎯 Kapitel 3: Entry & Exit Strategien")
    
    st.markdown("### 📋 AVWAP Trading Checklist")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **✅ Entry-Kriterien:**
        - [ ] AVWAP-Trend bestätigt
        - [ ] Volumen steigt
        - [ ] Preis bricht AVWAP
        - [ ] Risiko/Reward > 1:2
        - [ ] Stop-Loss definiert
        """)
    
    with col2:
        st.markdown("""
        **✅ Exit-Kriterien:**
        - [ ] Gewinnziel erreicht
        - [ ] AVWAP-Trend bricht
        - [ ] Volumen nimmt ab
        - [ ] Stop-Loss getriggert
        - [ ] Zeitlimit erreicht
        """)
    
    # Position Sizing Calculator
    st.markdown("### 🧮 Position Sizing Calculator")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        account_size = st.number_input("Account-Größe ($)", value=10000, step=1000)
    
    with col2:
        risk_percent = st.slider("Risiko pro Trade (%)", 1, 5, 2)
    
    with col3:
        stop_distance = st.number_input("Stop-Distance ($)", value=2.0, step=0.1)
    
    # Berechnung
    risk_amount = account_size * (risk_percent / 100)
    position_size = risk_amount / stop_distance
    
    st.metric("Position Size", f"${position_size:.0f}")
    st.caption(f"Risiko: ${risk_amount:.0f} ({risk_percent}%)")

def show_live_examples():
    """Zeigt Live Trading Beispiele"""
    st.markdown("## 📊 Kapitel 4: Live Trading Beispiele")
    
    # Beispiel-Trades
    trades = [
        {
            "symbol": "AAPL",
            "direction": "LONG",
            "entry": 150.25,
            "exit": 155.80,
            "avwap": 149.50,
            "profit": "+3.7%",
            "status": "WIN"
        },
        {
            "symbol": "TSLA", 
            "direction": "SHORT",
            "entry": 245.30,
            "exit": 238.90,
            "avwap": 246.20,
            "profit": "+2.6%",
            "status": "WIN"
        },
        {
            "symbol": "NVDA",
            "direction": "LONG", 
            "entry": 420.15,
            "exit": 415.80,
            "avwap": 418.50,
            "profit": "-1.0%",
            "status": "LOSS"
        }
    ]
    
    for trade in trades:
        with st.expander(f"{trade['symbol']} - {trade['direction']} - {trade['profit']}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Entry", f"${trade['entry']}")
                st.metric("Exit", f"${trade['exit']}")
            
            with col2:
                st.metric("AVWAP", f"${trade['avwap']}")
                st.metric("Profit", trade['profit'])
            
            with col3:
                if trade['status'] == "WIN":
                    st.success("✅ WIN")
                else:
                    st.error("❌ LOSS")
                
                st.caption(f"Richtung: {trade['direction']}")

def show_quiz_certificate():
    """Zeigt Quiz und Zertifikat"""
    st.markdown("## 🧠 Kapitel 5: Quiz & Zertifikat")
    
    # Quiz
    st.markdown("### 📝 AVWAP Quiz")
    
    questions = [
        {
            "question": "Was bedeutet AVWAP?",
            "options": [
                "Average Volume Weighted Average Price",
                "Advanced Volume Weighted Average Price", 
                "Accelerated Volume Weighted Average Price"
            ],
            "correct": 1
        },
        {
            "question": "AVWAP ist ein...",
            "options": [
                "Statischer Indikator",
                "Dynamischer Indikator",
                "Oszillator"
            ],
            "correct": 1
        }
    ]
    
    score = 0
    total = len(questions)
    
    for i, q in enumerate(questions):
        st.markdown(f"**{i+1}. {q['question']}**")
        answer = st.radio("", q['options'], key=f"q{i}")
        
        if answer == q['options'][q['correct']]:
            score += 1
            st.success("✅ Richtig!")
        else:
            st.error("❌ Falsch!")
    
    # Ergebnis
    st.markdown("---")
    percentage = (score / total) * 100
    
    if percentage >= 80:
        st.success(f"🎉 Bestanden! Score: {score}/{total} ({percentage:.0f}%)")
        
        if st.button("📜 Zertifikat herunterladen", type="primary"):
            st.balloons()
            st.success("Zertifikat wird generiert...")
    else:
        st.warning(f"📚 Wiederholen Sie das Modul. Score: {score}/{total} ({percentage:.0f}%)")

if __name__ == "__main__":
    main()
