import { NextResponse } from 'next/server';
import { getProfile, logNewsClick, addScore } from '@/lib/db';

// POST /api/v1/straxon/news/click
// Haber tıklamasını kaydet ve kullanıcıya +15 Zeka Derinliği puanı ver
export async function POST(request) {
  try {
    const { profile_id, news_id, email } = await request.json();

    if (!profile_id || !email) {
      return NextResponse.json(
        { error: 'profile_id ve email zorunludur' },
        { status: 400 }
      );
    }

    // Tıklama logla
    if (news_id) {
      await logNewsClick(profile_id, news_id);
    }

    // +15 puan ekle ve logla
    const newScore = await addScore(email, 15, 'News article clicked');

    return NextResponse.json({
      status: 'success',
      score_added: 15,
      new_intelligence_score: newScore,
    });
  } catch (err) {
    console.error('News click error:', err);
    return NextResponse.json(
      { error: 'Sunucu hatası', detail: err.message },
      { status: 500 }
    );
  }
}
