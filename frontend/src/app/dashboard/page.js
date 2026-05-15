"use client";
import React, { useState, useEffect } from 'react';
import DashboardShell, { IntelligenceCard, TimelineCard, JarvisInsightCard } from '@/components/Dashboard/Shell';
import OmNexusSignature from '@/components/OmNexusSignature';

export default function DashboardPage() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const fetchProfile = async () => {
      const params = new URLSearchParams(window.location.search);
      const email = params.get('email');
      
      if (email) {
        try {
          const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || '/_/backend';
          const res = await fetch(`${backendUrl}/api/v1/straxon/profile/${email}`);
          const data = await res.json();
          if (res.ok) setProfile(data);
        } catch (err) {
          console.error("Profil yüklenemedi:", err);
        }
      }
      setLoading(false);
    };

    fetchProfile();
  }, []);

  const goals = [
    profile?.current_q_goal || "Technical Infrastructure",
    "Jarvis Core Engine",
    "Market Integration",
    "Deep Analysis"
  ];

  const insight = profile?.github_username 
    ? `Hoş geldin @${profile.github_username}. Teknik ayak izin analiz edildi. Şu anki zeka derinliğin %${profile.intelligence_score}. Q1 hedeflerin için Go ve Python odaklı projeler geliştirmeye devam et.`
    : "Henüz bir teknik platform bağlanmadı. Jarvis'in sizi analiz edebilmesi için lütfen GitHub hesabınızı bağlayın.";

  if (loading) return <div style={{ background: '#0a0a0c', minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#d4af37' }}>STRAXON QART Yükleniyor...</div>;

  return (
    <DashboardShell>
      {/* 1. Intelligence Depth Hub */}
      <IntelligenceCard 
        score={profile?.intelligence_score || 0} 
        status={profile?.jarvis_mood || "Initializing..."} 
      />

      {/* 2. Timeline Card */}
      <TimelineCard goals={goals} />

      {/* 3. Jarvis Insight Card */}
      <JarvisInsightCard insight={insight} />

      {/* 4. Integration Matrix (Placeholder) */}
      <div className="bento-card integration-matrix">
        <div className="card-title">Integration Matrix</div>
        <div className="matrix-grid">
          {['GitHub', 'LinkedIn', 'StackOverflow', 'GitLab'].map(item => (
            <div key={item} className="matrix-item">
              <div className="status-dot online"></div>
              {item}
            </div>
          ))}
        </div>
        <style jsx>{`
          .matrix-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
          }
          .matrix-item {
            background: rgba(255,255,255,0.02);
            padding: 0.8rem;
            border-radius: 12px;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.8rem;
          }
          .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
          }
          .status-dot.online {
            background: #00ff88;
            box-shadow: 0 0 5px #00ff88;
          }
        `}</style>
      </div>

      {/* 5. Roadmap Mentor (Placeholder) */}
      <div className="bento-card roadmap-mentor">
        <div className="card-title">Career Roadmap Match</div>
        <div className="roadmap-content">
          <div className="match-score">65%</div>
          <div className="match-label">Backend Engineer Path Match</div>
        </div>
        <style jsx>{`
          .roadmap-content {
            display: flex;
            align-items: center;
            gap: 1rem;
            height: 100%;
          }
          .match-score {
            font-size: 2rem;
            font-weight: 900;
            color: #d4af37;
          }
          .match-label {
            font-size: 0.9rem;
            opacity: 0.7;
          }
        `}</style>
      </div>

      {/* 6. News Feed (Placeholder) */}
      <div className="bento-card news-feed">
        <div className="card-title">Strategic News Feed</div>
        <div className="news-list">
          <div className="news-item">Go 1.22 Release: New features for Cloud Native</div>
          <div className="news-item">The Rise of Agentic AI in DevOps</div>
        </div>
        <style jsx>{`
          .news-list {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
          }
          .news-item {
            font-size: 0.85rem;
            padding: 0.5rem;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            opacity: 0.8;
          }
        `}</style>
      </div>

      <div style={{ 
        position: 'fixed', 
        bottom: '2rem', 
        left: '50%', 
        transform: 'translateX(-50%)',
        zIndex: 100 
      }}>
        <OmNexusSignature />
      </div>
    </DashboardShell>
  );
}
