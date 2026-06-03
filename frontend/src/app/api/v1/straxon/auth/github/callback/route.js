import { NextResponse } from 'next/server';
import { createOrUpdateProfile, logIntelligence } from '@/lib/db';

// GET /api/v1/straxon/auth/github/callback
// GitHub OAuth callback — code'u token'a çevirir, profili günceller, dashboard'a yönlendirir
export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const code = searchParams.get('code');
  const frontendUrl = process.env.FRONTEND_URL || 'https://straxon-qart.vercel.app';

  if (!code) {
    return NextResponse.redirect(`${frontendUrl}/?error=github_no_code`);
  }

  try {
    // 1. Code → Access Token
    const tokenRes = await fetch('https://github.com/login/oauth/access_token', {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        client_id: process.env.GITHUB_CLIENT_ID,
        client_secret: process.env.GITHUB_CLIENT_SECRET,
        code,
        redirect_uri: process.env.GITHUB_REDIRECT_URI,
      }),
    });

    const tokenData = await tokenRes.json();
    const accessToken = tokenData.access_token;

    if (!accessToken) {
      return NextResponse.redirect(`${frontendUrl}/?error=github_token_failed`);
    }

    // 2. GitHub Kullanıcı Bilgileri
    const userRes = await fetch('https://api.github.com/user', {
      headers: {
        Authorization: `token ${accessToken}`,
        'User-Agent': 'Straxon-Qart-OmNexus',
      },
    });

    const userData = await userRes.json();
    const email = userData.email || `${userData.login}@github.com`;

    // 3. Profili Güncelle / Oluştur (+20 Zeka Puanı)
    await createOrUpdateProfile({
      email,
      full_name: userData.name,
      github_username: userData.login,
      score_increase: 20,
    });

    // 4. Intelligence Log
    await logIntelligence(email, 20, 'GitHub Integration connected');

    // 5. Dashboard'a yönlendir
    return NextResponse.redirect(
      `${frontendUrl}/dashboard?github_connected=true&username=${userData.login}&email=${encodeURIComponent(email)}`
    );
  } catch (err) {
    console.error('GitHub OAuth callback error:', err);
    return NextResponse.redirect(`${frontendUrl}/?error=github_callback_failed`);
  }
}
