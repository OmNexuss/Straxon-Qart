// ─────────────────────────────────────────────────────────────────────────────
// Supabase REST API — Server-side only (API Route'larda kullanılır)
// Python backend/core/database.py'nin Next.js karşılığı
// ─────────────────────────────────────────────────────────────────────────────

function getHeaders() {
  const key = process.env.SUPABASE_KEY;
  return {
    apikey: key,
    Authorization: `Bearer ${key}`,
    'Content-Type': 'application/json',
    Prefer: 'return=representation',
  };
}

function supabaseUrl(path) {
  return `${process.env.SUPABASE_URL}/rest/v1/${path}`;
}

export async function getProfile(email) {
  const res = await fetch(
    supabaseUrl(`profiles?email=eq.${encodeURIComponent(email)}`),
    { headers: getHeaders() }
  );
  const data = await res.json();
  return Array.isArray(data) ? (data[0] || null) : null;
}

export async function createOrUpdateProfile(profileData) {
  const { email, full_name, github_username, score_increase = 0 } = profileData;
  const existing = await getProfile(email);

  if (existing) {
    const newScore = (existing.intelligence_score || 0) + score_increase;
    await fetch(
      supabaseUrl(`profiles?email=eq.${encodeURIComponent(email)}`),
      {
        method: 'PATCH',
        headers: getHeaders(),
        body: JSON.stringify({
          intelligence_score: newScore,
          github_username,
          jarvis_mood: 'Analyzing',
        }),
      }
    );
    return { status: 'updated', score: newScore };
  } else {
    await fetch(supabaseUrl('profiles'), {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({
        email,
        full_name,
        github_username,
        intelligence_score: 20,
        jarvis_mood: 'Analyzing',
      }),
    });
    return { status: 'created', score: 20 };
  }
}

export async function logIntelligence(email, amount, reason) {
  const profile = await getProfile(email);
  if (!profile) return;
  await fetch(supabaseUrl('intelligence_logs'), {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify({
      profile_id: profile.id,
      change_amount: amount,
      reason,
    }),
  });
}
