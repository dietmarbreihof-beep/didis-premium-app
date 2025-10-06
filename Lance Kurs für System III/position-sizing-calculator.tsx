import React, { useState, useEffect } from 'react';
import { TrendingUp, DollarSign, Target, AlertTriangle, CheckCircle, Calculator } from 'lucide-react';

export default function PositionSizingCalculator() {
  const [depotwert, setDepotwert] = useState(100000);
  const [risikoProTrade, setRisikoProTrade] = useState(1);
  const [sizingMethode, setSizingMethode] = useState('exponential');
  const [selectedGrade, setSelectedGrade] = useState('A');
  const [showComparison, setShowComparison] = useState(false);
  const [activeTab, setActiveTab] = useState('beginner');

  const tradeGrades = {
    A: {
      name: 'A-Trade',
      color: '#38a169',
      winRate: 90,
      reward: 4,
      risk: 1,
      ev: 3.50,
      frequency: '2-3x pro Monat',
      beschreibung: 'Die absoluten Highlight-Trades des Jahres. Pocket Aces. Alles stimmt perfekt.',
      beispiele: 'QXO Entry bei $13.90, CELH Breakout, SMCI Stage 2 Setup'
    },
    B: {
      name: 'B-Trade',
      color: '#d69e2e',
      winRate: 70,
      reward: 2,
      risk: 1,
      ev: 1.10,
      frequency: 'Mehrmals pro Woche',
      beschreibung: 'Solide Setups mit gutem Risk-Reward. Die "Singles" im Trading.',
      beispiele: 'Stage 2 Continuation, Breakout über Resistance, Momentum-Plays'
    },
    C: {
      name: 'C-Trade',
      color: '#f4e97b',
      winRate: 55,
      reward: 1,
      risk: 1,
      ev: 0.10,
      frequency: 'Täglich',
      beschreibung: 'Durchschnittliche Trades. Leichter Edge, aber nichts Besonderes.',
      beispiele: 'Kleine Scalps, Range-Trades, Routine-Setups'
    },
    D: {
      name: 'D-Trade',
      color: '#e53e3e',
      winRate: 40,
      reward: 1,
      risk: 1,
      ev: -0.20,
      frequency: 'Ständig verfügbar',
      beschreibung: 'Mediocre 50/50 Trades oder negativer Expected Value. Vermeiden!',
      beispiele: 'FOMO-Trades, Breaking News ohne Setup, Übertrading'
    }
  };

  const calculatePositionSize = (grade, methode) => {
    const basisRisiko = (depotwert * risikoProTrade) / 100;
    
    const multipliers = {
      equal: { A: 1, B: 1, C: 1, D: 1 },
      linear: { A: 4, B: 3, C: 2, D: 1 },
      exponential: { A: 8, B: 4, C: 2, D: 1 },
      wild: { A: 27, B: 9, C: 3, D: 1 }
    };

    return basisRisiko * multipliers[methode][grade];
  };

  const calculateComparison = () => {
    const trades = [
      { grade: 'A', count: 2, ev: 3.50 },
      { grade: 'B', count: 8, ev: 1.10 },
      { grade: 'C', count: 24, ev: 0.10 },
      { grade: 'D', count: 66, ev: -0.20 }
    ];

    const methods = ['equal', 'linear', 'exponential', 'wild'];
    const results = {};

    methods.forEach(method => {
      let totalPL = 0;
      trades.forEach(({ grade, count, ev }) => {
        const size = calculatePositionSize(grade, method);
        totalPL += size * ev * count;
      });
      results[method] = totalPL;
    });

    return results;
  };

  const comparison = calculateComparison();
  const currentSize = calculatePositionSize(selectedGrade, sizingMethode);
  const grade = tradeGrades[selectedGrade];

  const methodNames = {
    equal: 'Gleiches Sizing',
    linear: 'Lineares Sizing',
    exponential: 'Exponentielles Sizing',
    wild: 'Exponentiell Wild'
  };

  const methodDescriptions = {
    equal: 'Für Anfänger - Lerne erst Dein System',
    linear: 'Für Beginner mit ersten Daten',
    exponential: 'Für Trader mit 4+ Jahren Erfahrung + robuste Daten',
    wild: 'Für Elite-Trader mit 8+ Jahren Erfahrung + tonnenweise Daten'
  };

  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)', padding: '40px 20px' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        
        {/* Hero Header */}
        <div style={{ 
          background: 'linear-gradient(135deg, #1a1a1a 0%, #b8860b 100%)', 
          borderRadius: '12px',
          padding: '40px',
          marginBottom: '40px',
          color: 'white',
          textAlign: 'center'
        }}>
          <h1 style={{ fontSize: '2.8em', marginBottom: '15px', fontWeight: 'bold' }}>
            🎯 Positionsgrößen-Kalkulator
          </h1>
          <p style={{ fontSize: '1.3em', opacity: 0.9, lineHeight: '1.6' }}>
            Wie Du durch intelligentes Bet-Sizing Deine Trading-Performance exponentiell steigerst
          </p>
        </div>

        {/* Tab Navigation */}
        <div style={{ display: 'flex', gap: '10px', marginBottom: '30px', flexWrap: 'wrap' }}>
          {['beginner', 'calculator', 'grades', 'comparison', 'poker'].map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              style={{
                flex: '1',
                minWidth: '150px',
                padding: '15px 25px',
                background: activeTab === tab ? 'linear-gradient(135deg, #b8860b, #daa520)' : '#2d2d2d',
                color: 'white',
                border: 'none',
                borderRadius: '12px',
                cursor: 'pointer',
                fontSize: '1.1em',
                fontWeight: activeTab === tab ? 'bold' : 'normal',
                transition: 'all 0.3s ease'
              }}
            >
              {tab === 'beginner' && '⚠️ START HIER'}
              {tab === 'calculator' && '🧮 Kalkulator'}
              {tab === 'grades' && '📊 Trade-Grades'}
              {tab === 'comparison' && '📈 Vergleich'}
              {tab === 'poker' && '♠️ Poker-Analogie'}
            </button>
          ))}
        </div>

        {/* Beginner Tab */}
        {activeTab === 'beginner' && (
          <div style={{ background: 'white', borderRadius: '12px', padding: '40px', boxShadow: '0 4px 20px rgba(0,0,0,0.1)' }}>
            <h2 style={{ fontSize: '2em', marginBottom: '30px', color: '#1a1a1a', textAlign: 'center' }}>
              ⚠️ WICHTIG: Lies das zuerst!
            </h2>

            <div style={{ background: '#e53e3e20', borderRadius: '12px', padding: '30px', marginBottom: '30px', borderLeft: '6px solid #e53e3e' }}>
              <h3 style={{ fontSize: '1.8em', marginBottom: '20px', color: '#e53e3e' }}>
                🚨 Exponentielles Bet-Sizing ist NICHT für Anfänger!
              </h3>
              <p style={{ fontSize: '1.2em', lineHeight: '1.8', color: '#1a1a1a' }}>
                Dieser Kalkulator und die gesamte Methodik basieren auf einem fundamentalen Prinzip: 
                <strong> Du musst Deine A-Trades von Deinen D-Trades unterscheiden können - IN ECHTZEIT, VOR dem Entry!</strong>
              </p>
            </div>

            <div style={{ marginBottom: '30px' }}>
              <h3 style={{ fontSize: '1.6em', marginBottom: '20px', color: '#1a1a1a' }}>
                🎯 Drei kritische Voraussetzungen
              </h3>
              
              <div style={{ display: 'grid', gap: '20px' }}>
                <div style={{ background: '#f7f7f7', borderRadius: '12px', padding: '25px', borderLeft: '6px solid #b8860b' }}>
                  <h4 style={{ fontSize: '1.3em', marginBottom: '15px', color: '#b8860b' }}>
                    1. Empirische Daten aus Deinem Journal
                  </h4>
                  <p style={{ fontSize: '1.1em', lineHeight: '1.6', marginBottom: '15px' }}>
                    <strong>Ohne Journal-Auswertung Deiner eigenen Setups fehlt Dir die empirische Grundlage für präzises Grading.</strong>
                  </p>
                  <p style={{ fontSize: '1.05em', lineHeight: '1.6', color: '#2d2d2d' }}>
                    Die Win-Rates in diesem Tool (90%, 70%, 55%, 40%) stammen aus Lance Breitsteins Beispiel-Fallstudie - 
                    <strong> nicht aus Deinen realen Trading-Daten!</strong> Du kannst nicht einfach raten, welche Win-Rate Deine Setups haben. 
                    Du musst es messen!
                  </p>
                  <div style={{ marginTop: '15px', padding: '15px', background: '#daa52020', borderRadius: '8px' }}>
                    <strong>Minimum:</strong> 30-50 Trades pro Grade bevor Du valide Schlüsse ziehen kannst. 
                    Besser: 100+ Trades für statistische Signifikanz.
                  </div>
                </div>

                <div style={{ background: '#f7f7f7', borderRadius: '12px', padding: '25px', borderLeft: '6px solid #b8860b' }}>
                  <h4 style={{ fontSize: '1.3em', marginBottom: '15px', color: '#b8860b' }}>
                    2. Entwickelte Trading-Strategie
                  </h4>
                  <p style={{ fontSize: '1.1em', lineHeight: '1.6', marginBottom: '15px' }}>
                    Du brauchst ein <strong>erprobtes Playbook</strong> mit definierten Setups:
                  </p>
                  <ul style={{ fontSize: '1.05em', lineHeight: '1.8', paddingLeft: '25px' }}>
                    <li>Stage 2 Breakout-Setup</li>
                    <li>Momentum-Plays mit Katalysator</li>
                    <li>Mean Reversion bei Support</li>
                    <li>Swing-Trades nach Konsolidierung</li>
                  </ul>
                  <p style={{ fontSize: '1.05em', lineHeight: '1.6', marginTop: '15px', color: '#2d2d2d' }}>
                    <strong>Wenn Du noch kein klares System hast:</strong> Fokussiere Dich ERST auf das Erlernen einer Strategie 
                    mit kleinen, gleichbleibenden Positionsgrößen. Bet-Sizing kommt später!
                  </p>
                </div>

                <div style={{ background: '#f7f7f7', borderRadius: '12px', padding: '25px', borderLeft: '6px solid #b8860b' }}>
                  <h4 style={{ fontSize: '1.3em', marginBottom: '15px', color: '#b8860b' }}>
                    3. Psychologische Stabilität
                  </h4>
                  <p style={{ fontSize: '1.1em', lineHeight: '1.6', marginBottom: '15px' }}>
                    Du musst in der Lage sein, <strong>größere Positionsgrößen zu handeln, ohne dass es Deine Psychologie verändert.</strong>
                  </p>
                  <p style={{ fontSize: '1.05em', lineHeight: '1.6', color: '#2d2d2d' }}>
                    Wenn Du bei 8x Deiner normalen Size nervös wirst und deshalb zu früh aussteigst oder 
                    Deine Entry-Regeln missachtest, zerstörst Du den gesamten Expected Value Vorteil. 
                    Die Positionsgröße darf Deine Ausführung NICHT beeinflussen.
                  </p>
                  <div style={{ marginTop: '15px', padding: '15px', background: '#e53e3e20', borderRadius: '8px' }}>
                    <strong>Warnung:</strong> Viele Trader ruinieren ihre Accounts, weil sie zu schnell skalieren, 
                    bevor sie psychologisch bereit sind!
                  </div>
                </div>
              </div>
            </div>

            <div style={{ background: 'linear-gradient(135deg, #f4e97b, #daa520)', padding: '30px', borderRadius: '12px', marginBottom: '30px' }}>
              <h3 style={{ fontSize: '1.6em', marginBottom: '20px', color: '#1a1a1a' }}>
                ✅ Der richtige Weg zum exponentiellen Sizing
              </h3>
              <div style={{ fontSize: '1.1em', lineHeight: '1.8', color: '#1a1a1a' }}>
                <p style={{ marginBottom: '15px' }}>
                  <strong>Phase 1 (Monate 1-6):</strong> Lerne Dein Setup. Trade mit kleiner, gleichbleibender Size. 
                  Führe detailliertes Journal. Ziel: Konsistenz entwickeln.
                </p>
                <p style={{ marginBottom: '15px' }}>
                  <strong>Phase 2 (Monate 7-12):</strong> Analysiere Dein Journal. Identifiziere Deine besten Setups. 
                  Beginne mit leichtem linearem Sizing (1x, 1.5x, 2x, 3x). Sammle mehr Daten.
                </p>
                <p style={{ marginBottom: '15px' }}>
                  <strong>Phase 3 (Jahr 2+):</strong> Mit 100+ Trades und bewiesener Konsistenz: 
                  Beginne vorsichtig mit exponentiellem Sizing. Steigere monatlich um 10%.
                </p>
                <p>
                  <strong>Phase 4 (Elite Level):</strong> Nach Jahren der Erfahrung und psychologischer Meisterschaft: 
                  Aggressive Skalierung bei A-Setups (1x, 3x, 9x, 27x).
                </p>
              </div>
            </div>

            <div style={{ background: '#38a16920', borderRadius: '12px', padding: '30px', borderLeft: '6px solid #38a169' }}>
              <h3 style={{ fontSize: '1.6em', marginBottom: '20px', color: '#38a169' }}>
                🚀 Dein nächster Schritt
              </h3>
              <p style={{ fontSize: '1.2em', lineHeight: '1.8', color: '#1a1a1a', marginBottom: '20px' }}>
                Wenn Du noch kein vollständiges Trade-Journal hast, starte JETZT damit:
              </p>
              <div style={{ background: 'white', padding: '20px', borderRadius: '8px' }}>
                <p style={{ fontSize: '1.1em', lineHeight: '1.6', marginBottom: '15px' }}>
                  <strong>Minimales Journal pro Trade:</strong>
                </p>
                <ul style={{ fontSize: '1.05em', lineHeight: '1.8', paddingLeft: '25px' }}>
                  <li>Datum & Ticker</li>
                  <li>Setup-Typ (z.B. "Stage 2 Breakout")</li>
                  <li><strong>Grade VOR Entry</strong> (A/B/C/D) - das ist kritisch!</li>
                  <li>Entry & Exit Preis</li>
                  <li>Ergebnis (Win/Loss/Breakeven)</li>
                  <li>P&L in Euro</li>
                  <li>Kurze Notiz: Warum dieser Grade? Was lief gut/schlecht?</li>
                </ul>
              </div>
              <p style={{ fontSize: '1.1em', lineHeight: '1.6', marginTop: '20px', color: '#1a1a1a' }}>
                Nach 50-100 Trades hast Du genug Daten, um Deine echten Win-Rates pro Grade zu berechnen. 
                Dann - und erst dann - kannst Du den Kalkulator mit Deinen realen Zahlen nutzen.
              </p>
            </div>

            <div style={{ marginTop: '30px', padding: '25px', background: '#2d2d2d', borderRadius: '12px', color: 'white', textAlign: 'center' }}>
              <p style={{ fontSize: '1.3em', lineHeight: '1.8' }}>
                <strong style={{ color: '#daa520' }}>Denk dran:</strong> Elite-Trader wurden nicht über Nacht zu Elite-Tradern. 
                Sie verbrachten Jahre damit, ihr Handwerk zu perfektionieren, bevor sie aggressiv skalieren konnten.
              </p>
              <p style={{ fontSize: '1.1em', marginTop: '15px', opacity: 0.9 }}>
                Sei geduldig mit Dir selbst. Fokussiere Dich auf Konsistenz vor Sizing.
              </p>
            </div>
          </div>
        )}

        {/* Calculator Tab */}
        {activeTab === 'calculator' && (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
            
            {/* Einstellungen */}
            <div style={{ background: 'white', borderRadius: '12px', padding: '30px', boxShadow: '0 4px 20px rgba(0,0,0,0.1)' }}>
              <h2 style={{ fontSize: '1.8em', marginBottom: '25px', color: '#1a1a1a' }}>
                <Calculator size={32} style={{ verticalAlign: 'middle', marginRight: '10px' }} />
                Deine Einstellungen
              </h2>

              <div style={{ marginBottom: '25px' }}>
                <label style={{ display: 'block', marginBottom: '10px', fontWeight: 'bold', color: '#1a1a1a' }}>
                  Depotwert (€)
                </label>
                <input
                  type="number"
                  value={depotwert}
                  onChange={(e) => setDepotwert(Number(e.target.value))}
                  style={{
                    width: '100%',
                    padding: '12px',
                    fontSize: '1.2em',
                    border: '2px solid #daa520',
                    borderRadius: '8px'
                  }}
                />
              </div>

              <div style={{ marginBottom: '25px' }}>
                <label style={{ display: 'block', marginBottom: '10px', fontWeight: 'bold', color: '#1a1a1a' }}>
                  Basis-Risiko pro D-Trade (%)
                </label>
                <input
                  type="range"
                  min="0.25"
                  max="3"
                  step="0.25"
                  value={risikoProTrade}
                  onChange={(e) => setRisikoProTrade(Number(e.target.value))}
                  style={{ width: '100%', marginBottom: '10px' }}
                />
                <div style={{ fontSize: '1.3em', fontWeight: 'bold', color: '#b8860b' }}>
                  {risikoProTrade}%
                </div>
              </div>

              <div style={{ marginBottom: '25px' }}>
                <label style={{ display: 'block', marginBottom: '10px', fontWeight: 'bold', color: '#1a1a1a' }}>
                  Sizing-Methode
                </label>
                {Object.entries(methodNames).map(([key, name]) => (
                  <div key={key} style={{ marginBottom: '10px' }}>
                    <label style={{ 
                      display: 'flex', 
                      flexDirection: 'column',
                      cursor: 'pointer', 
                      padding: '12px', 
                      background: sizingMethode === key ? '#f4e97b' : '#f7f7f7', 
                      borderRadius: '8px',
                      border: sizingMethode === key ? '2px solid #b8860b' : '2px solid transparent',
                      transition: 'all 0.3s ease'
                    }}>
                      <div style={{ display: 'flex', alignItems: 'center' }}>
                        <input
                          type="radio"
                          value={key}
                          checked={sizingMethode === key}
                          onChange={(e) => setSizingMethode(e.target.value)}
                          style={{ marginRight: '10px' }}
                        />
                        <span style={{ fontWeight: 'bold', fontSize: '1.05em' }}>{name}</span>
                      </div>
                      <div style={{ 
                        marginTop: '5px', 
                        marginLeft: '30px', 
                        fontSize: '0.9em', 
                        color: '#666',
                        fontStyle: 'italic'
                      }}>
                        {methodDescriptions[key]}
                      </div>
                    </label>
                  </div>
                ))}
              </div>

              <div>
                <label style={{ display: 'block', marginBottom: '10px', fontWeight: 'bold', color: '#1a1a1a' }}>
                  Trade-Grade auswählen
                </label>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                  {Object.entries(tradeGrades).map(([key, value]) => (
                    <button
                      key={key}
                      onClick={() => setSelectedGrade(key)}
                      style={{
                        padding: '15px',
                        background: selectedGrade === key ? value.color : '#f7f7f7',
                        color: selectedGrade === key ? 'white' : '#1a1a1a',
                        border: 'none',
                        borderRadius: '8px',
                        cursor: 'pointer',
                        fontWeight: 'bold',
                        fontSize: '1.2em',
                        transition: 'all 0.3s ease'
                      }}
                    >
                      {value.name}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Ergebnis */}
            <div style={{ background: grade.color, borderRadius: '12px', padding: '30px', color: 'white', boxShadow: '0 4px 20px rgba(0,0,0,0.1)' }}>
              <h2 style={{ fontSize: '1.8em', marginBottom: '25px' }}>
                {grade.name} Positionsgröße
              </h2>

              <div style={{ background: 'rgba(255,255,255,0.2)', borderRadius: '12px', padding: '25px', marginBottom: '25px', textAlign: 'center' }}>
                <div style={{ fontSize: '1.2em', marginBottom: '10px', opacity: 0.9 }}>
                  Empfohlenes Risiko
                </div>
                <div style={{ fontSize: '3em', fontWeight: 'bold' }}>
                  €{currentSize.toLocaleString('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                </div>
                <div style={{ fontSize: '1.1em', marginTop: '10px', opacity: 0.9 }}>
                  {((currentSize / depotwert) * 100).toFixed(2)}% des Depots
                </div>
              </div>

              <div style={{ background: 'rgba(255,255,255,0.2)', borderRadius: '12px', padding: '20px', marginBottom: '20px' }}>
                <h3 style={{ fontSize: '1.3em', marginBottom: '15px' }}>Trade-Charakteristika</h3>
                <div style={{ marginBottom: '10px' }}>
                  <strong>Win-Rate:</strong> {grade.winRate}%
                </div>
                <div style={{ marginBottom: '10px' }}>
                  <strong>Risk/Reward:</strong> 1:{grade.reward}
                </div>
                <div style={{ marginBottom: '10px' }}>
                  <strong>Expected Value:</strong> ${grade.ev}
                </div>
                <div style={{ marginBottom: '10px' }}>
                  <strong>Häufigkeit:</strong> {grade.frequency}
                </div>
              </div>

              <div style={{ background: 'rgba(255,255,255,0.2)', borderRadius: '12px', padding: '20px' }}>
                <p style={{ lineHeight: '1.6', fontSize: '1.05em' }}>
                  <strong>Beschreibung:</strong> {grade.beschreibung}
                </p>
                <p style={{ lineHeight: '1.6', fontSize: '1.05em', marginTop: '10px' }}>
                  <strong>Beispiele:</strong> {grade.beispiele}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Trade Grades Tab */}
        {activeTab === 'grades' && (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px' }}>
            {Object.entries(tradeGrades).map(([key, value]) => (
              <div
                key={key}
                style={{
                  background: 'white',
                  borderRadius: '12px',
                  padding: '25px',
                  borderLeft: `6px solid ${value.color}`,
                  boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
                  transition: 'transform 0.3s ease',
                  cursor: 'pointer'
                }}
                onMouseEnter={(e) => e.currentTarget.style.transform = 'translateY(-5px)'}
                onMouseLeave={(e) => e.currentTarget.style.transform = 'translateY(0)'}
              >
                <h3 style={{ fontSize: '1.6em', color: value.color, marginBottom: '15px', fontWeight: 'bold' }}>
                  {value.name}
                </h3>
                
                <div style={{ marginBottom: '15px', padding: '15px', background: '#f7f7f7', borderRadius: '8px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span><strong>Win-Rate:</strong></span>
                    <span style={{ color: value.color, fontWeight: 'bold' }}>{value.winRate}%</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span><strong>R:R:</strong></span>
                    <span style={{ color: value.color, fontWeight: 'bold' }}>1:{value.reward}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span><strong>EV:</strong></span>
                    <span style={{ color: value.color, fontWeight: 'bold' }}>${value.ev}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span><strong>Häufigkeit:</strong></span>
                    <span style={{ fontSize: '0.9em' }}>{value.frequency}</span>
                  </div>
                </div>

                <p style={{ fontSize: '1.05em', lineHeight: '1.6', color: '#2d2d2d', marginBottom: '15px' }}>
                  {value.beschreibung}
                </p>

                <div style={{ padding: '12px', background: `${value.color}15`, borderRadius: '8px' }}>
                  <strong style={{ color: value.color }}>Beispiele:</strong>
                  <div style={{ fontSize: '0.95em', marginTop: '8px', lineHeight: '1.5' }}>
                    {value.beispiele}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Comparison Tab */}
        {activeTab === 'comparison' && (
          <div style={{ background: 'white', borderRadius: '12px', padding: '40px', boxShadow: '0 4px 20px rgba(0,0,0,0.1)' }}>
            <h2 style={{ fontSize: '2em', marginBottom: '30px', color: '#1a1a1a', textAlign: 'center' }}>
              📊 Die Macht des Exponentiellen Sizings
            </h2>

            <div style={{ background: 'linear-gradient(135deg, #f4e97b, #daa520)', padding: '20px', borderRadius: '12px', marginBottom: '30px', borderLeft: '6px solid #b8860b' }}>
              <p style={{ fontSize: '1.1em', lineHeight: '1.6', color: '#1a1a1a' }}>
                <strong>Annahme:</strong> 100 Trades über ein Jahr: 2x A-Trades, 8x B-Trades, 24x C-Trades, 66x D-Trades<br/>
                <strong>Depotwert:</strong> €{depotwert.toLocaleString('de-DE')}<br/>
                <strong>Basis-Risiko (D-Trade):</strong> {risikoProTrade}%
              </p>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '20px', marginBottom: '30px' }}>
              {Object.entries(methodNames).map(([key, name]) => {
                const pl = comparison[key];
                const isPositive = pl > 0;
                const performance = ((pl / depotwert) * 100).toFixed(2);
                
                return (
                  <div
                    key={key}
                    style={{
                      background: isPositive ? '#38a16920' : '#e53e3e20',
                      borderRadius: '12px',
                      padding: '25px',
                      borderLeft: `6px solid ${isPositive ? '#38a169' : '#e53e3e'}`,
                      textAlign: 'center'
                    }}
                  >
                    <h3 style={{ fontSize: '1.3em', marginBottom: '15px', color: '#1a1a1a' }}>
                      {name}
                    </h3>
                    <div style={{ fontSize: '2.2em', fontWeight: 'bold', color: isPositive ? '#38a169' : '#e53e3e', marginBottom: '10px' }}>
                      {isPositive ? '+' : ''}€{pl.toLocaleString('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                    </div>
                    <div style={{ fontSize: '1.3em', color: isPositive ? '#38a169' : '#e53e3e', fontWeight: 'bold' }}>
                      {isPositive ? '+' : ''}{performance}%
                    </div>
                  </div>
                );
              })}
            </div>

            <div style={{ background: '#f7f7f7', borderRadius: '12px', padding: '30px' }}>
              <h3 style={{ fontSize: '1.5em', marginBottom: '20px', color: '#1a1a1a' }}>
                💡 Kernerkenntnisse
              </h3>
              <ul style={{ fontSize: '1.1em', lineHeight: '1.8', color: '#2d2d2d' }}>
                <li style={{ marginBottom: '15px' }}>
                  <strong>Gleiches Sizing:</strong> Bei konstanter Positionsgröße wirst Du zum Verlierer-Trader, selbst wenn Du gute Trades identifizieren kannst!
                </li>
                <li style={{ marginBottom: '15px' }}>
                  <strong>Lineares Sizing:</strong> Schon eine einfache Skalierung (1x, 2x, 3x, 4x) macht Dich profitabel.
                </li>
                <li style={{ marginBottom: '15px' }}>
                  <strong>Exponentielles Sizing:</strong> Die wahre Magie beginnt hier. Durch 1x, 2x, 4x, 8x vervielfachst Du Deine Performance dramatisch.
                </li>
                <li>
                  <strong>Exponentiell Wild:</strong> Elite-Trader setzen auf extreme Skalierung (1x, 3x, 9x, 27x) und machen 80%+ ihrer Jahresperformance mit weniger als 5% ihrer Trades!
                </li>
              </ul>
            </div>
          </div>
        )}

        {/* Poker Tab */}
        {activeTab === 'poker' && (
          <div style={{ background: 'white', borderRadius: '12px', padding: '40px', boxShadow: '0 4px 20px rgba(0,0,0,0.1)' }}>
            <h2 style={{ fontSize: '2em', marginBottom: '30px', color: '#1a1a1a', textAlign: 'center' }}>
              ♠️ Die Poker-Analogie: Warum Trade-Grades wie Poker-Hände sind
            </h2>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '30px', marginBottom: '30px' }}>
              <div style={{ background: 'linear-gradient(135deg, #e53e3e20, #e53e3e10)', borderRadius: '12px', padding: '25px', borderLeft: '6px solid #e53e3e' }}>
                <h3 style={{ fontSize: '1.5em', marginBottom: '20px', color: '#e53e3e' }}>
                  9-2 Hand (D-Trade)
                </h3>
                <div style={{ fontSize: '3em', textAlign: 'center', marginBottom: '15px' }}>
                  9♣ 2♥
                </div>
                <div style={{ fontSize: '1.2em', marginBottom: '10px' }}>
                  <strong>Win-Rate:</strong> 38.9%
                </div>
                <p style={{ fontSize: '1.05em', lineHeight: '1.6' }}>
                  Die schlechteste Starting Hand im Poker. Du spielst sie nur, wenn Du musst (Big Blind). Aber Du setzt niemals groß darauf!
                </p>
              </div>

              <div style={{ background: 'linear-gradient(135deg, #38a16920, #38a16910)', borderRadius: '12px', padding: '25px', borderLeft: '6px solid #38a169' }}>
                <h3 style={{ fontSize: '1.5em', marginBottom: '20px', color: '#38a169' }}>
                  Pocket Aces (A-Trade)
                </h3>
                <div style={{ fontSize: '3em', textAlign: 'center', marginBottom: '15px' }}>
                  A♥ A♠
                </div>
                <div style={{ fontSize: '1.2em', marginBottom: '10px' }}>
                  <strong>Win-Rate:</strong> 85.3%
                </div>
                <p style={{ fontSize: '1.05em', lineHeight: '1.6' }}>
                  Die stärkste Starting Hand! Kommt nur 1 von 221 Händen vor (0.45%). Wenn Du sie bekommst: GO ALL-IN!
                </p>
              </div>
            </div>

            <div style={{ background: 'linear-gradient(135deg, #f4e97b, #daa520)', padding: '25px', borderRadius: '12px', marginBottom: '30px' }}>
              <h3 style={{ fontSize: '1.5em', marginBottom: '20px', color: '#1a1a1a' }}>
                🎯 Die entscheidende Frage
              </h3>
              <p style={{ fontSize: '1.2em', lineHeight: '1.8', color: '#1a1a1a' }}>
                Stell Dir vor, Du sitzt am Pokertisch und bekommst abwechselnd 9-2 und Pocket Aces.<br/><br/>
                <strong>Würdest Du auf beide Hände gleich viel setzen?</strong><br/><br/>
                Natürlich nicht! Das wäre finanzieller Selbstmord.<br/><br/>
                Genau so ist es beim Trading: Wenn Du auf einen D-Trade und einen A-Trade die gleiche Positionsgröße setzt, verschenkst Du massiv Potential!
              </p>
            </div>

            <div style={{ background: '#f7f7f7', borderRadius: '12px', padding: '30px' }}>
              <h3 style={{ fontSize: '1.5em', marginBottom: '20px', color: '#1a1a1a' }}>
                📈 Trading = Professionelles Poker
              </h3>
              <div style={{ display: 'grid', gap: '20px' }}>
                <div style={{ padding: '20px', background: 'white', borderRadius: '8px', borderLeft: '4px solid #b8860b' }}>
                  <strong style={{ fontSize: '1.2em', color: '#b8860b' }}>Ähnlichkeit 1: Wahrscheinlichkeiten</strong>
                  <p style={{ marginTop: '10px', lineHeight: '1.6' }}>
                    Sowohl beim Poker als auch beim Trading geht es um das Spielen von Wahrscheinlichkeiten, nicht um Garantien.
                  </p>
                </div>
                
                <div style={{ padding: '20px', background: 'white', borderRadius: '8px', borderLeft: '4px solid #b8860b' }}>
                  <strong style={{ fontSize: '1.2em', color: '#b8860b' }}>Ähnlichkeit 2: Seltenheit der Premiumhände</strong>
                  <p style={{ marginTop: '10px', lineHeight: '1.6' }}>
                    Pocket Aces kommen nur 0.45% vor - genau wie A-Trades nur 2-3x pro Monat auftreten.
                  </p>
                </div>
                
                <div style={{ padding: '20px', background: 'white', borderRadius: '8px', borderLeft: '4px solid #b8860b' }}>
                  <strong style={{ fontSize: '1.2em', color: '#b8860b' }}>Ähnlichkeit 3: Bankroll Management</strong>
                  <p style={{ marginTop: '10px', lineHeight: '1.6' }}>
                    Professionelle Pokerspieler passen ihre Einsätze der Handstärke an - genau wie Du Deine Positionsgröße dem Trade-Grade anpassen solltest.
                  </p>
                </div>
                
                <div style={{ padding: '20px', background: 'white', borderRadius: '8px', borderLeft: '4px solid #b8860b' }}>
                  <strong style={{ fontSize: '1.2em', color: '#b8860b' }}>Die Lektion:</strong>
                  <p style={{ marginTop: '10px', lineHeight: '1.6' }}>
                    Elite-Trader, wie Elite-Pokerspieler, machen den Großteil ihres Geldes mit wenigen großen Händen/Trades. Sie erkennen die Pocket Aces, wenn sie kommen, und setzen massiv darauf!
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Footer mit Didis Signatur */}
        <div style={{ 
          marginTop: '40px', 
          padding: '30px', 
          background: 'linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%)', 
          borderRadius: '12px',
          color: 'white',
          textAlign: 'center'
        }}>
          <p style={{ fontSize: '1.2em', lineHeight: '1.8', marginBottom: '15px' }}>
            <strong style={{ color: '#daa520' }}>Denk dran:</strong> Elite-Trader machen 80%+ ihrer Jahresperformance mit weniger als 5% ihrer Trades!
          </p>
          <p style={{ fontSize: '1.05em', opacity: 0.9 }}>
            Die Kunst liegt darin, die Pocket Aces zu erkennen und dann die Ranch zu setzen.
          </p>
        </div>

      </div>
    </div>
  );
}