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

export async function addScore(email, amount, reason) {
  const profile = await getProfile(email);
  if (!profile) return null;
  const newScore = (profile.intelligence_score || 0) + amount;
  await fetch(
    supabaseUrl(`profiles?email=eq.${encodeURIComponent(email)}`),
    {
      method: 'PATCH',
      headers: getHeaders(),
      body: JSON.stringify({ intelligence_score: newScore }),
    }
  );
  await logIntelligence(email, amount, reason);
  return newScore;
}

// ─── News Feed ──────────────────────────────────────────────────────────────

export async function getNews({ tags, limit = 20 } = {}) {
  let path = `news_feed?order=created_at.desc&limit=${limit}`;
  if (tags && tags.length > 0) {
    const tagFilter = '{' + tags.join(',') + '}';
    path += `&tags=ov.${encodeURIComponent(tagFilter)}`;
  }
  const res = await fetch(supabaseUrl(path), { headers: getHeaders() });
  if (!res.ok) return [];
  return res.json();
}

export async function saveNewsBulk(newsList) {
  if (!newsList || newsList.length === 0) return 0;
  const headers = {
    ...getHeaders(),
    Prefer: 'resolution=ignore-duplicates,return=minimal',
  };
  let saved = 0;
  for (const item of newsList) {
    const res = await fetch(supabaseUrl('news_feed'), {
      method: 'POST',
      headers,
      body: JSON.stringify(item),
    });
    if (res.status === 201 || res.status === 200) saved++;
  }
  return saved;
}

export async function logNewsClick(profileId, newsId) {
  await fetch(supabaseUrl('news_click_logs'), {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify({ profile_id: profileId, news_id: newsId }),
  });
}

// ─── User Tasks ─────────────────────────────────────────────────────────────

export async function getUserTasks(profileId) {
  const res = await fetch(
    supabaseUrl(`user_tasks?profile_id=eq.${profileId}&order=created_at.asc`),
    { headers: getHeaders() }
  );
  if (!res.ok) return [];
  return res.json();
}

export async function createUserTask(profileId, taskType, title, description, metadata) {
  const res = await fetch(supabaseUrl('user_tasks'), {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify({
      profile_id: profileId,
      task_type: taskType || 'milestone',
      title,
      description,
      metadata: metadata || {},
    }),
  });
  const data = await res.json();
  return Array.isArray(data) ? data[0] : data;
}

export async function updateTaskStatus(taskId, isCompleted) {
  const patchBody = { is_completed: isCompleted };
  if (isCompleted) patchBody.completed_at = new Date().toISOString();
  else patchBody.completed_at = null;

  const res = await fetch(
    supabaseUrl(`user_tasks?id=eq.${taskId}`),
    {
      method: 'PATCH',
      headers: getHeaders(),
      body: JSON.stringify(patchBody),
    }
  );
  const data = await res.json();
  return Array.isArray(data) ? data[0] : data;
}

