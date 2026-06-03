import { NextResponse } from 'next/server';
import { getProfile } from '@/lib/db';
import { analyzeProfile } from '@/lib/roadmap';

// GET /api/v1/straxon/profile/[email]
// Kullanıcı profilini Supabase'den çeker + GitHub roadmap analizi ekler
export async function GET(request, { params }) {
  try {
    const email = decodeURIComponent(params.email);
    const profile = await getProfile(email);

    if (!profile) {
      return NextResponse.json(
        { error: 'Profil bulunamadı' },
        { status: 404 }
      );
    }

    const roadmapAnalysis = await analyzeProfile(profile.github_username);

    return NextResponse.json({
      ...profile,
      roadmap_match: roadmapAnalysis,
    });
  } catch (err) {
    console.error('Profile fetch error:', err);
    return NextResponse.json(
      { error: 'Sunucu hatası', detail: err.message },
      { status: 500 }
    );
  }
}
