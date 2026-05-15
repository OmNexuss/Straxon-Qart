"use client";
import React from 'react';
import '@/styles/dashboard.css';

const DashboardShell = ({ children }) => {
  return (
    <div className="dashboard-shell">
      {children}
    </div>
  );
};

export const IntelligenceCard = ({ score, status }) => (
  <div className="bento-card intelligence-core">
    <div className="scan-line"></div>
    <div className="card-title" style={{ color: '#00d4ff' }}>
      <span className="pulse-dot"></span> Intelligence Depth
    </div>
    <div className="intelligence-content">
      <div className="score-display">
        <span className="score-value">{score}%</span>
        <span className="score-label">Analyzed</span>
      </div>
      <div className="depth-bar-container">
        <div className="depth-bar-progress" style={{ width: `${score}%` }}></div>
      </div>
      <div className="depth-status">{status}</div>
    </div>
    <style jsx>{`
      .score-display {
        display: flex;
        flex-direction: column;
        margin-bottom: 1rem;
      }
      .score-value {
        font-size: 3rem;
        font-weight: 900;
        color: #fff;
        line-height: 1;
      }
      .score-label {
        font-size: 0.7rem;
        opacity: 0.5;
        letter-spacing: 1px;
      }
      .depth-bar-container {
        height: 8px;
        background: rgba(255,255,255,0.05);
        border-radius: 4px;
        overflow: hidden;
        margin-bottom: 1rem;
        position: relative;
      }
      .depth-bar-progress {
        height: 100%;
        background: linear-gradient(90deg, #00d4ff, #d4af37);
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.5);
        transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
      }
      .depth-status {
        font-size: 0.8rem;
        opacity: 0.7;
        font-style: italic;
      }
      .pulse-dot {
        width: 6px;
        height: 6px;
        background: #00d4ff;
        border-radius: 50%;
        box-shadow: 0 0 10px #00d4ff;
        animation: pulse 2s infinite;
      }
      @keyframes pulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.5); opacity: 0.5; }
        100% { transform: scale(1); opacity: 1; }
      }
    `}</style>
  </div>
);

export const TimelineCard = ({ goals }) => (
  <div className="bento-card timeline-q">
    <div className="card-title">Q1-Q4 Strategic Roadmap</div>
    <div className="timeline-grid">
      {['Q1', 'Q2', 'Q3', 'Q4'].map((q, i) => (
        <div key={q} className={`q-slot ${i === 1 ? 'active' : ''}`}>
          <div className="q-label">{q}</div>
          <div className="q-goal">{goals[i] || 'Planning...'}</div>
        </div>
      ))}
    </div>
    <style jsx>{`
      .timeline-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        height: 100%;
      }
      .q-slot {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 1rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
      }
      .q-slot.active {
        border-color: rgba(212, 175, 55, 0.4);
        background: rgba(212, 175, 55, 0.05);
      }
      .q-label {
        font-size: 0.7rem;
        font-weight: 800;
        opacity: 0.4;
        margin-bottom: 0.3rem;
      }
      .q-goal {
        font-size: 0.9rem;
        font-weight: 500;
      }
    `}</style>
  </div>
);

export const JarvisInsightCard = ({ insight }) => (
  <div className="bento-card jarvis-insight">
    <div className="card-title" style={{ color: '#d4af37' }}>Jarvis Intelligence Center</div>
    <div className="insight-content">
      <div className="ai-icon">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#d4af37" strokeWidth="1.5">
          <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
        </svg>
      </div>
      <p className="insight-text">{insight}</p>
      <div className="action-row">
        <button className="action-btn">Action Plan</button>
        <button className="action-btn outline">Dismiss</button>
      </div>
    </div>
    <style jsx>{`
      .insight-content {
        display: flex;
        flex-direction: column;
        height: 100%;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 1rem;
      }
      .ai-icon {
        margin-bottom: 1.5rem;
        filter: drop-shadow(0 0 10px rgba(212, 175, 55, 0.3));
      }
      .insight-text {
        font-size: 1.25rem;
        font-weight: 300;
        line-height: 1.6;
        margin-bottom: 2rem;
        color: rgba(255,255,255,0.9);
      }
      .action-row {
        display: flex;
        gap: 1rem;
      }
      .action-btn {
        background: #d4af37;
        color: #000;
        border: none;
        padding: 0.7rem 1.5rem;
        border-radius: 8px;
        font-weight: 700;
        cursor: pointer;
        transition: 0.3s;
      }
      .action-btn.outline {
        background: transparent;
        border: 1px solid rgba(255,255,255,0.1);
        color: #fff;
      }
      .action-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(212, 175, 55, 0.2);
      }
    `}</style>
  </div>
);

export default DashboardShell;
