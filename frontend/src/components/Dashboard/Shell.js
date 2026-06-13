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
  </div>
);

export const TimelineCard = ({ goals }) => (
  <div className="bento-card timeline-q">
    <div className="card-title">Q1-Q4 Strategic Roadmap</div>
    <div className="timeline-grid">
      {['Q1', 'Q2', 'Q3', 'Q4'].map((q, i) => (
        <div key={q} className={`q-slot${i === 1 ? ' active' : ''}`}>
          <div className="q-label">{q}</div>
          <div className="q-goal">{goals[i] || 'Planning...'}</div>
        </div>
      ))}
    </div>
  </div>
);

export const JarvisInsightCard = ({ insight }) => (
  <div className="bento-card jarvis-insight">
    <div className="card-title" style={{ color: '#d4af37' }}>Jarvis Intelligence Center</div>
    <div className="insight-content">
      <div className="ai-icon">
        <svg width="42" height="42" viewBox="0 0 24 24" fill="none" stroke="#d4af37" strokeWidth="1.5">
          <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
        </svg>
      </div>
      <p className="insight-text">{insight}</p>
      <div className="action-row">
        <button className="action-btn">Action Plan</button>
        <button className="action-btn outline">Dismiss</button>
      </div>
    </div>
  </div>
);

export default DashboardShell;
