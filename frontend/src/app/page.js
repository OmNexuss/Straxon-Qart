"use client";
import { useState, useEffect } from 'react';
import OmNexusSignature from '@/components/OmNexusSignature';

export default function Home() {
  const [formData, setFormData] = useState({ name: '', email: '' });
  const [status, setStatus] = useState({ type: '', message: '' });
  const [loading, setLoading] = useState(false);
  const [githubUser, setGithubUser] = useState(null);

  // URL'den GitHub bağlantı durumunu kontrol et
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const connected = params.get('github_connected');
    const username = params.get('username');
    if (connected === 'true' && username) {
      setGithubUser(username);
      // URL'deki parametreleri temizle
      window.history.replaceState({}, document.title, "/");
    }
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setStatus({ type: '', message: '' });

    try {
      // Vercel'deki routePrefix'e uygun olarak güncellendi
      const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || '/_/backend';
      const res = await fetch(`${backendUrl}/api/v1/straxon/waitlist`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await res.json();

      if (res.ok) {
        setStatus({ type: 'success', message: 'Kaydınız başarıyla alındı. OmNexus ekosistemine hoş geldiniz.' });
        setFormData({ name: '', email: '' });
      } else {
        setStatus({ type: 'error', message: data.detail || 'Bir hata oluştu.' });
      }
    } catch (err) {
      setStatus({ type: 'error', message: 'Sunucuya bağlanılamadı. Lütfen API\'nin çalıştığından emin olun.' });
    } finally {
      setLoading(false);
    }
  };

  const handleGithubConnect = () => {
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || '/_/backend';
    window.location.href = `${backendUrl}/api/v1/straxon/auth/github`;
  };

  return (
    <div style={{ 
      minHeight: '100vh', 
      display: 'flex', 
      flexDirection: 'column', 
      alignItems: 'center', 
      justifyContent: 'center',
      padding: '2rem',
      background: 'radial-gradient(circle at center, #1a1a1e 0%, #0a0a0c 100%)'
    }}>
      
      {/* Logo Area */}
      <div className="animate-fade" style={{ textAlign: 'center', marginBottom: '2.5rem' }}>
        <div style={{ 
          width: '100px', 
          height: '100px', 
          margin: '0 auto 1rem',
          position: 'relative',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}>
          <div style={{
            position: 'absolute',
            width: '100%',
            height: '100%',
            background: 'url("/logo.png") center/contain no-repeat',
            zIndex: 2,
            filter: 'drop-shadow(0 0 15px rgba(212, 175, 55, 0.3))'
          }}></div>
          <div style={{ 
            width: '100%', 
            height: '100%', 
            border: '2px solid #d4af37', 
            borderRadius: '50%', 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            color: '#d4af37',
            fontSize: '1.5rem',
            fontWeight: 'bold',
            opacity: 0.8
          }}>SQ</div>
        </div>
        <h1 style={{ fontSize: '1.8rem', fontWeight: '900', letterSpacing: '4px', color: '#fff' }}>STRAXON QART</h1>
        <p style={{ fontSize: '0.8rem', letterSpacing: '2px', opacity: 0.6, color: '#d4af37' }}>STRATEGIC COMMAND CENTER</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '2rem', width: '100%', maxWidth: '900px' }}>
        
        {/* Waitlist Form */}
        <div className="glass-panel animate-fade" style={{ padding: '2.5rem', textAlign: 'center' }}>
          <h2 style={{ fontSize: '1.3rem', marginBottom: '1.5rem' }}>Bekleme Listesi</h2>
          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <input 
              type="text" 
              placeholder="Tam İsminiz" 
              required
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)', padding: '0.8rem', borderRadius: '8px', color: '#fff', outline: 'none' }}
            />
            <input 
              type="email" 
              placeholder="E-posta Adresiniz" 
              required
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)', padding: '0.8rem', borderRadius: '8px', color: '#fff', outline: 'none' }}
            />
            <button 
              type="submit"
              disabled={loading}
              style={{ background: 'linear-gradient(135deg, #d4af37 0%, #b8860b 100%)', color: '#000', padding: '0.8rem', borderRadius: '8px', border: 'none', fontWeight: '800', cursor: 'pointer', transition: 'all 0.3s ease', opacity: loading ? 0.7 : 1 }}
            >
              {loading ? 'İŞLENİYOR...' : 'ERİŞİM TALEBİ GÖNDER'}
            </button>
          </form>
          {status.message && (
            <div style={{ marginTop: '1.5rem', padding: '0.8rem', borderRadius: '8px', background: status.type === 'success' ? 'rgba(0, 255, 136, 0.1)' : 'rgba(255, 68, 68, 0.1)', color: status.type === 'success' ? '#00ff88' : '#ff4444', fontSize: '0.85rem' }}>
              {status.message}
            </div>
          )}
        </div>

        {/* Jarvis & GitHub Section */}
        <div className="glass-panel animate-fade" style={{ padding: '2.5rem', textAlign: 'center', animationDelay: '0.2s', border: '1px solid rgba(0, 212, 255, 0.2)' }}>
          <h2 style={{ fontSize: '1.3rem', marginBottom: '1.5rem', color: '#00d4ff' }}>Jarvis Teknik Analiz</h2>
          
          {githubUser ? (
            <div style={{ padding: '1rem', background: 'rgba(0, 212, 255, 0.05)', borderRadius: '12px', textAlign: 'left' }}>
              <p style={{ fontSize: '0.9rem', marginBottom: '1rem' }}>Sistem Bağlandı: <span style={{ fontWeight: 'bold', color: '#00d4ff' }}>@{githubUser}</span></p>
              <p style={{ fontSize: '0.85rem', opacity: 0.7, lineHeight: '1.5' }}>
                Jarvis şu an teknik ayak izinizi analiz ediyor. Çok yakında roadmap.sh üzerinden size özel kariyer rotanızı burada görebileceksiniz.
              </p>
            </div>
          ) : (
            <>
              <p style={{ opacity: 0.7, marginBottom: '2rem', fontSize: '0.9rem', lineHeight: '1.6' }}>
                Jarvis'in sizi analiz etmesi ve yol haritası (roadmap.sh) önermesi için teknik dünyanızı bağlayın.
              </p>
              <button 
                onClick={handleGithubConnect}
                style={{ 
                  background: '#24292e', 
                  color: '#fff', 
                  padding: '0.8rem 1.5rem', 
                  borderRadius: '8px', 
                  border: '1px solid #444', 
                  fontWeight: '600', 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: '10px', 
                  margin: '0 auto',
                  cursor: 'pointer'
                }}
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.042-1.416-4.042-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
                GitHub ile Bağlan
              </button>
            </>
          )}
        </div>

      </div>

      <OmNexusSignature />
    </div>
  );
}
