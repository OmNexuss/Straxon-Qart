import { NextResponse } from 'next/server';
import { getProfile, getUserTasks, createUserTask, getNews } from '@/lib/db';
import { analyzeProfile } from '@/lib/roadmap';

// GET /api/v1/straxon/profile/[email]
// Kullanıcı profilini Supabase'den çeker + GitHub roadmap analizi + Jarvis + Tasks
export async function GET(request, { params }) {
  try {
    const resolvedParams = await params;
    const email = decodeURIComponent(resolvedParams.email);
    const profile = await getProfile(email);

    if (!profile) {
      return NextResponse.json(
        { error: 'Profil bulunamadı' },
        { status: 404 }
      );
    }

    // 1. Roadmap analizi (GitHub)
    const roadmapAnalysis = await analyzeProfile(profile.github_username);

    // 2. Kullanıcı görevleri
    let tasks = await getUserTasks(profile.id);

    // 3. Görev tohumlama: GitHub bağlıysa ve hiç görev yoksa kilometre taşlarından oluştur
    if (tasks.length === 0 && roadmapAnalysis?.github_connected) {
      const { primary_milestone, secondary_milestone } = roadmapAnalysis;
      if (primary_milestone) {
        await createUserTask(
          profile.id, 'milestone',
          primary_milestone.title,
          primary_milestone.why_needed,
          {
            discipline: primary_milestone.discipline,
            anchor_url: primary_milestone.anchor_url,
            action_steps: primary_milestone.action_steps || [],
            color: primary_milestone.color,
            emoji: primary_milestone.emoji,
            label: 'Birincil Hedef',
          }
        );
      }
      if (secondary_milestone) {
        await createUserTask(
          profile.id, 'milestone',
          secondary_milestone.title,
          secondary_milestone.why_needed,
          {
            discipline: secondary_milestone.discipline,
            anchor_url: secondary_milestone.anchor_url,
            action_steps: secondary_milestone.action_steps || [],
            color: secondary_milestone.color,
            emoji: secondary_milestone.emoji,
            label: 'İkincil Hedef',
          }
        );
      }
      tasks = await getUserTasks(profile.id);
    }

    // 4. Jarvis tavsiyesi — Gemini API (server-side)
    let jarvisInsight = null;
    const geminiApiKey = process.env.GEMINI_API_KEY;
    if (geminiApiKey && profile.github_username && roadmapAnalysis?.github_connected) {
      // Son haberleri (disipline göre) getir
      const primaryDiscipline = roadmapAnalysis.primary_discipline || '';
      const recentNews = await getNews({ limit: 5 });
      const newsHeadlines = recentNews.map(n => n.title).join('\n- ');

      const milestoneCtx = roadmapAnalysis.primary_milestone
        ? `Birincil hedef: "${roadmapAnalysis.primary_milestone.title}"`
        : '';

      const prompt = `Sen Straxon-Qart platformunun yapay zeka asistanı Jarvis'sin.
Kullanıcı: @${profile.github_username}
Kimlik: ${roadmapAnalysis.synthesis_title || primaryDiscipline}
Ana disiplin skoru: %${roadmapAnalysis.primary_score || 0}
Zeka derinliği: %${profile.intelligence_score || 0}
${milestoneCtx}
${newsHeadlines ? `Son teknoloji haberleri:\n- ${newsHeadlines}` : ''}

Bu bilgilere dayanarak 2-3 cümlelik, motive edici, özgün Türkçe bir kariyer tavsiyesi üret.
JSON: {"insight": "metin"}`;

      try {
        const gemRes = await fetch(
          `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${geminiApiKey}`,
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              contents: [{ parts: [{ text: prompt }] }],
              generationConfig: {
                temperature: 0.7,
                maxOutputTokens: 256,
                responseMimeType: 'application/json',
              },
            }),
          }
        );
        if (gemRes.ok) {
          const gemData = await gemRes.json();
          const text = gemData?.candidates?.[0]?.content?.parts?.[0]?.text;
          if (text) {
            const parsed = JSON.parse(text);
            jarvisInsight = parsed.insight || text;
          }
        }
      } catch (_) {
        // Gemini API hatası — fallback kullanılacak
      }
    }

    return NextResponse.json({
      ...profile,
      roadmap_match: roadmapAnalysis,
      tasks,
      jarvis_insight: jarvisInsight,
    });
  } catch (err) {
    console.error('Profile fetch error:', err);
    return NextResponse.json(
      { error: 'Sunucu hatası', detail: err.message },
      { status: 500 }
    );
  }
}
