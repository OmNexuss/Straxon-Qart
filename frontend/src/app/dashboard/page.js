"use client";
import React, { useState, useEffect } from 'react';
import DashboardShell, { IntelligenceCard, TimelineCard, JarvisInsightCard } from '@/components/Dashboard/Shell';
import OmNexusSignature from '@/components/OmNexusSignature';

// ─── Dinamik Q1-Q4 hedefleri — Sentez unvanına göre ──────────────────────────
function getDynamicGoals(synthesisTitle, primaryDiscipline) {
  const d = primaryDiscipline || "";
  if (d.includes("Backend"))     return ["API Design & REST","Relational Databases","Docker Containers","CI/CD & Cloud Deploy"];
  if (d.includes("Frontend"))    return ["HTML/CSS & Core JS","React State & Hooks","Next.js SSR / RSC","Build Tools & Perf"];
  if (d.includes("DevOps"))      return ["Linux Shell Mastery","Containers & K8s","Terraform IaC","Monitoring & Alerts"];
  if (d.includes("AI & ML"))     return ["Math & Statistics","Pandas / NumPy ETL","ML Algorithms","Deep Learning / LLMs"];
  if (d.includes("Cyber"))       return ["Networking & Protocols","Linux Internals","Penetration Testing","Cryptography & PKI"];
  if (d.includes("Blockchain"))  return ["Blockchain Fundamentals","Solidity & Smart Contracts","dApp Development","DeFi Protocol Design"];
  if (d.includes("Embedded"))    return ["C/C++ Low-Level","MCU & Peripherals","RTOS & Interrupts","IoT Protocols & Cloud"];
  if (d.includes("Mobile"))      return ["Core Language & UI","State Management","Networking & Local DB","App Store Deployment"];
  if (d.includes("Game"))        return ["Math & Physics Systems","Game Engine Integration","Design Patterns (ECS)","Shaders & Graphics API"];
  // Full-Stack ve diğer hibrit unvanlar
  if (synthesisTitle?.includes("Full-Stack")) return ["API Design & DB","React / Next.js UI","Docker Containers","Production Deploy"];
  if (synthesisTitle?.includes("DevSecOps"))  return ["Linux & Networking","Container Security","Pentest Automation","SIEM & Monitoring"];
  if (synthesisTitle?.includes("Web3"))       return ["Solidity Contracts","Backend APIs","dApp Frontend","DeFi & Audit"];
  if (synthesisTitle?.includes("Edge AI"))    return ["Embedded C/C++","MCU & RTOS","On-Device ML","IoT Cloud Pipeline"];
  return ["Technical Infrastructure","Jarvis Core Engine","Market Integration","Deep Analysis"];
}

// ─── Uyumluluk Çubuğu ────────────────────────────────────────────────────────
function CompatibilityBar({ role, emoji, color, score, url }) {
  return (
    <a href={url} target="_blank" rel="noopener noreferrer"
      style={{ textDecoration: "none", color: "inherit", display: "block" }}>
      <div style={{
        display: "flex", alignItems: "center", gap: "0.6rem",
        padding: "0.45rem 0.2rem",
        borderRadius: "8px",
        transition: "background 0.2s",
        cursor: "pointer"
      }}
        onMouseOver={e => e.currentTarget.style.background = "rgba(255,255,255,0.03)"}
        onMouseOut={e => e.currentTarget.style.background = "transparent"}
      >
        <span style={{ fontSize: "0.8rem", width: "18px", textAlign: "center" }}>{emoji}</span>
        <span style={{ fontSize: "0.72rem", opacity: 0.75, width: "160px", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>{role}</span>
        <div style={{ flex: 1, height: "5px", background: "rgba(255,255,255,0.05)", borderRadius: "3px", overflow: "hidden" }}>
          <div style={{
            width: `${score}%`, height: "100%",
            background: `linear-gradient(90deg, ${color}, ${color}88)`,
            boxShadow: `0 0 8px ${color}55`,
            borderRadius: "3px",
            transition: "width 1.2s cubic-bezier(0.4,0,0.2,1)"
          }} />
        </div>
        <span style={{ fontSize: "0.7rem", fontWeight: "700", color, minWidth: "30px", textAlign: "right" }}>{score}%</span>
      </div>
    </a>
  );
}

// ─── Milestone Kartı ──────────────────────────────────────────────────────────
function MilestoneCard({ milestone, label }) {
  if (!milestone) return null;
  const { title, anchor_url, why_needed, action_steps, emoji, color } = milestone;
  return (
    <div style={{
      background: `rgba(${hexToRgb(color)}, 0.04)`,
      border: `1px solid ${color}30`,
      borderRadius: "16px",
      padding: "1.1rem",
      position: "relative",
      flex: 1
    }}>
      {/* Label badge */}
      <div style={{
        position: "absolute", top: "-10px", left: "12px",
        background: color, color: "#000",
        fontSize: "0.6rem", fontWeight: "900",
        padding: "2px 10px", borderRadius: "8px",
        letterSpacing: "1px", textTransform: "uppercase"
      }}>
        {label}
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", marginTop: "0.4rem", marginBottom: "0.5rem" }}>
        <span style={{ fontSize: "1.1rem" }}>{emoji}</span>
        <h3 style={{ fontSize: "0.9rem", fontWeight: "900", color, margin: 0, lineHeight: 1.2 }}>{title}</h3>
      </div>
      <p style={{ fontSize: "0.75rem", opacity: 0.8, lineHeight: "1.5", marginBottom: "0.8rem", color: "#f0f0f2" }}>
        {why_needed}
      </p>
      <div style={{ display: "flex", flexDirection: "column", gap: "0.35rem", marginBottom: "0.9rem" }}>
        {(action_steps || []).map((step, i) => (
          <div key={i} style={{ display: "flex", gap: "7px", alignItems: "flex-start", fontSize: "0.72rem" }}>
            <span style={{ color, fontWeight: "900", marginTop: "1px" }}>✓</span>
            <span style={{ opacity: 0.9 }}>{step}</span>
          </div>
        ))}
      </div>
      <a href={anchor_url} target="_blank" rel="noopener noreferrer" style={{
        display: "block", textAlign: "center",
        background: `linear-gradient(135deg, ${color}, ${color}88)`,
        color: "#000", textDecoration: "none",
        padding: "0.55rem", borderRadius: "8px",
        fontWeight: "900", fontSize: "0.72rem",
        letterSpacing: "0.8px",
        transition: "all 0.3s"
      }}
        onMouseOver={e => e.currentTarget.style.transform = "translateY(-1px)"}
        onMouseOut={e => e.currentTarget.style.transform = "translateY(0)"}
      >
        YOL HARİTASINDA AÇ ➔
      </a>
    </div>
  );
}

// hex rengi rgb parçalarına ayır (rgba için)
function hexToRgb(hex) {
  hex = hex?.replace("#", "") || "212,175,55";
  if (hex.length === 3) hex = hex.split("").map(c => c + c).join("");
  const num = parseInt(hex, 16);
  return `${(num >> 16) & 255}, ${(num >> 8) & 255}, ${num & 255}`;
}

// ─────────────────────────────────────────────────────────────────────────────
// DASHBOARD SAYFASI
// ─────────────────────────────────────────────────────────────────────────────
export default function DashboardPage() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProfile = async () => {
      const params = new URLSearchParams(window.location.search);
      const email = params.get("email");
      const username = params.get("username");

      if (username) setProfile({ github_username: username, email, intelligence_score: 20 });

      if (email) {
        try {
          const res = await fetch(`/api/v1/straxon/profile/${email}`);
          const data = await res.json();
          if (res.ok && data && !data.error) setProfile(data);
        } catch (err) {
          console.error("Profil yüklenemedi:", err);
        }
      }
      setLoading(false);
    };
    fetchProfile();
  }, []);

  const rm = profile?.roadmap_match || {};
  const synthesisTitle     = rm.synthesis_title || null;
  const synthesisEmoji     = rm.synthesis_emoji || "⚡";
  const compatibilities    = rm.compatibilities || [];
  const primaryDiscipline  = rm.primary_discipline || null;
  const primaryMilestone   = rm.primary_milestone || null;
  const secondaryMilestone = rm.secondary_milestone || null;

  const goals = getDynamicGoals(synthesisTitle, primaryDiscipline);

  const insight = profile?.github_username
    ? `Hoş geldin @${profile.github_username}. ${synthesisTitle ? `Jarvis seni "${synthesisTitle}" olarak tanımladı.` : ""} Şu anki zeka derinliğin %${profile.intelligence_score || 0}. Aşağıdaki kilometre taşlarına odaklan.`
    : "Henüz bir teknik platform bağlanmadı. Jarvis'in seni analiz edebilmesi için GitHub hesabını bağla.";

  if (loading) return (
    <div style={{ background: "#0a0a0c", minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", color: "#d4af37", letterSpacing: "3px", fontSize: "0.85rem" }}>
      STRAXON QART — Yükleniyor...
    </div>
  );

  return (
    <DashboardShell>
      {/* 1. Intelligence Depth */}
      <IntelligenceCard score={profile?.intelligence_score || 0} status={profile?.jarvis_mood || "Initializing..."} />

      {/* 2. Q1-Q4 Strategic Timeline */}
      <TimelineCard goals={goals} />

      {/* 3. Jarvis Insight */}
      <JarvisInsightCard insight={insight} />

      {/* 4. Integration Matrix */}
      <div className="bento-card integration-matrix">
        <div className="card-title">Integration Matrix</div>
        <div style={{ display: "flex", flexDirection: "column", gap: "0.8rem" }}>
          {["GitHub", "LinkedIn", "StackOverflow", "GitLab"].map(item => {
            const isGh = item === "GitHub";
            const active = isGh && profile?.github_username;
            return (
              <div key={item} style={{
                background: "rgba(255,255,255,0.02)",
                padding: "0.8rem", borderRadius: "12px",
                display: "flex", alignItems: "center", gap: "0.5rem",
                fontSize: "0.82rem", opacity: active || !isGh ? 1 : 0.35,
                border: "1px solid rgba(255,255,255,0.04)"
              }}>
                <div style={{
                  width: "8px", height: "8px", borderRadius: "50%",
                  background: active || !isGh ? "#00ff88" : "#ef4444",
                  boxShadow: `0 0 5px ${active || !isGh ? "#00ff88" : "#ef4444"}`
                }} />
                {item}
                {active && (
                  <span style={{ fontSize: "0.65rem", color: "#00d4ff", marginLeft: "auto" }}>
                    @{profile.github_username}
                  </span>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* 5. UNIVERSAL DEVELOPER SYNTHESIS — Ana Bento Kartı */}
      <div className="bento-card roadmap-mentor" style={{
        border: rm.github_connected ? "1px solid rgba(212,175,55,0.25)" : "1px solid rgba(255,255,255,0.05)"
      }}>
        {rm.github_connected ? (
          <div style={{ display: "flex", flexDirection: "column", height: "100%", gap: "0.8rem" }}>

            {/* ── Sentez Unvanı Rozeti ── */}
            <div style={{
              display: "flex", alignItems: "center", justifyContent: "space-between",
              background: "rgba(212,175,55,0.04)",
              border: "1px solid rgba(212,175,55,0.15)",
              borderRadius: "14px", padding: "0.8rem 1.1rem"
            }}>
              <div>
                <div style={{ fontSize: "0.65rem", opacity: 0.45, letterSpacing: "1.5px", textTransform: "uppercase", marginBottom: "2px" }}>
                  Geliştirici Kimliği
                </div>
                <div style={{ fontSize: "1.1rem", fontWeight: "900", color: "#fff", display: "flex", alignItems: "center", gap: "0.4rem" }}>
                  <span>{synthesisEmoji}</span>
                  <span>{synthesisTitle || primaryDiscipline || "Analiz Ediliyor..."}</span>
                </div>
              </div>
              <div style={{ textAlign: "right" }}>
                <div style={{ fontSize: "1.5rem", fontWeight: "900", color: "#d4af37" }}>
                  {rm.primary_score || 0}%
                </div>
                <div style={{ fontSize: "0.6rem", opacity: 0.45, letterSpacing: "1px" }}>ANA UYUM</div>
              </div>
            </div>

            {/* ── 9 Disiplinli Yetenek Matrisi ── */}
            <div style={{
              background: "rgba(255,255,255,0.01)",
              border: "1px solid rgba(255,255,255,0.04)",
              borderRadius: "14px", padding: "0.8rem 0.9rem"
            }}>
              <div style={{ fontSize: "0.65rem", opacity: 0.4, letterSpacing: "1.5px", textTransform: "uppercase", marginBottom: "0.5rem" }}>
                🌐 Evrensel Yetenek Matrisi
              </div>
              {compatibilities.length > 0 ? (
                compatibilities.map(c => (
                  <CompatibilityBar key={c.role} {...c} />
                ))
              ) : (
                <p style={{ fontSize: "0.75rem", opacity: 0.5 }}>Veri analiz ediliyor...</p>
              )}
            </div>

            {/* ── Kilometre Taşları ── */}
            <div style={{ fontSize: "0.65rem", opacity: 0.4, letterSpacing: "1.5px", textTransform: "uppercase" }}>
              🎯 Kişisel Kilometre Taşları
            </div>
            <div style={{ display: "flex", gap: "0.8rem", flex: 1 }}>
              <MilestoneCard milestone={primaryMilestone} label="Birincil Hedef" />
              {secondaryMilestone && (
                <MilestoneCard milestone={secondaryMilestone} label="İkincil Hedef" />
              )}
            </div>

          </div>
        ) : (
          /* ── GitHub Bağlı Değil ── */
          <div style={{ display: "flex", flexDirection: "column", height: "100%", justifyContent: "center", alignItems: "center", gap: "1.2rem", textAlign: "center", padding: "1.5rem" }}>
            <div className="card-title" style={{ color: "#d4af37" }}>🎯 Career Roadmap Mentor</div>
            <div style={{
              width: "56px", height: "56px", borderRadius: "50%",
              background: "rgba(255,255,255,0.02)", display: "flex",
              alignItems: "center", justifyContent: "center",
              border: "1px solid rgba(255,255,255,0.06)", fontSize: "1.8rem"
            }}>🌐</div>
            <p style={{ fontSize: "0.82rem", opacity: 0.65, lineHeight: "1.6", maxWidth: "300px" }}>
              9 bilişim disiplininde kişisel yetenek haritanı ve spesifik kilometre taşlarını görmek için GitHub hesabını bağla.
            </p>
            <button onClick={() => {
              window.location.href = '/api/v1/straxon/auth/github';
            }} style={{
              background: "#24292e", color: "#fff",
              padding: "0.7rem 1.4rem", borderRadius: "10px",
              border: "1px solid #444", fontWeight: "700", fontSize: "0.8rem",
              display: "flex", alignItems: "center", gap: "8px",
              margin: "0 auto", cursor: "pointer", transition: "all 0.3s"
            }}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.042-1.416-4.042-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
              </svg>
              GitHub ile Bağlan
            </button>
          </div>
        )}
      </div>

      {/* 6. News Feed */}
      <div className="bento-card news-feed">
        <div className="card-title">Strategic News Feed</div>
        <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
          {["Go 1.22 Release: New features for Cloud Native", "The Rise of Agentic AI in DevOps", "Solidity 0.8.25: EVM updates & gas optimizations"].map((item, i) => (
            <div key={i} style={{ fontSize: "0.82rem", padding: "0.5rem 0.2rem", borderBottom: "1px solid rgba(255,255,255,0.05)", opacity: 0.8 }}>
              {item}
            </div>
          ))}
        </div>
      </div>

      <div style={{ gridColumn: "1 / -1", display: "flex", justifyContent: "center", marginTop: "2rem", paddingBottom: "1rem", opacity: 0.8 }}>
        <OmNexusSignature />
      </div>
    </DashboardShell>
  );
}
