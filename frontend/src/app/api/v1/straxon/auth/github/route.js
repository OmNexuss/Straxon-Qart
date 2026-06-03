import { NextResponse } from 'next/server';

// GET /api/v1/straxon/auth/github
// GitHub OAuth akışını başlatır — kullanıcıyı GitHub login sayfasına yönlendirir
export async function GET() {
  const clientId = process.env.GITHUB_CLIENT_ID;
  const frontendUrl = process.env.FRONTEND_URL || 'https://straxon-qart.vercel.app';
  const redirectUri =
    process.env.GITHUB_REDIRECT_URI ||
    `${frontendUrl}/api/v1/straxon/auth/github/callback`;

  const githubAuthUrl =
    `https://github.com/login/oauth/authorize` +
    `?client_id=${clientId}` +
    `&redirect_uri=${encodeURIComponent(redirectUri)}` +
    `&scope=repo,user`;

  return NextResponse.redirect(githubAuthUrl);
}
