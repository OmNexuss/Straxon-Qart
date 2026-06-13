import { NextResponse } from 'next/server';
import { getNews, saveNewsBulk } from '@/lib/db';

// Disiplin → Haber etiketi haritası (frontend kopyası)
const DISCIPLINE_TAGS = {
  'Backend Engineer':           ['backend', 'api', 'fastapi', 'django', 'go', 'rust', 'database'],
  'Frontend Engineer':          ['frontend', 'react', 'nextjs', 'typescript', 'css', 'webdev'],
  'DevOps Engineer':            ['devops', 'kubernetes', 'docker', 'terraform', 'cicd', 'cloud'],
  'AI & ML Engineer':           ['machinelearning', 'deeplearning', 'ai', 'llm', 'python', 'datascience'],
  'Cyber Security Specialist':  ['security', 'cybersecurity', 'hacking', 'ctf', 'cryptography'],
  'Blockchain & Web3 Developer':['blockchain', 'web3', 'solidity', 'ethereum', 'defi'],
  'Mobile Developer':           ['android', 'ios', 'flutter', 'kotlin', 'swift', 'reactnative'],
  'Game Developer':             ['gamedev', 'unity', 'godot', 'unrealengine', 'opengl'],
  'Embedded & IoT Engineer':    ['embedded', 'iot', 'arduino', 'raspberrypi', 'firmware'],
};

function getTagsForDisciplines(disciplines) {
  const tags = new Set();
  for (const d of disciplines) {
    (DISCIPLINE_TAGS[d] || []).forEach(t => tags.add(t));
  }
  return [...tags];
}

// GET /api/v1/straxon/news?disciplines=...&limit=20
export async function GET(request) {
  try {
    const { searchParams } = new URL(request.url);
    const disciplineStr = searchParams.get('disciplines') || '';
    const limit = parseInt(searchParams.get('limit') || '20', 10);

    const disciplineList = disciplineStr
      ? disciplineStr.split(',').map(d => d.trim()).filter(Boolean)
      : [];

    const tags = disciplineList.length > 0
      ? getTagsForDisciplines(disciplineList)
      : null;

    // 1. Mevcut haberleri getir
    let newsItems = await getNews({ tags, limit });

    // 2. Eğer veritabanı boşsa ilk seferlik senkron olarak kazıma yap
    if (newsItems.length === 0) {
      console.log('[NewsRoute] Database is empty, scraping news synchronously...');
      await scrapeInBackground(disciplineList).catch(e =>
        console.error('[NewsRoute] Sync Scrape error:', e)
      );
      newsItems = await getNews({ tags, limit });
    } else {
      // Değilse arka planda (fire-and-forget) haber kazı
      scrapeInBackground(disciplineList).catch(e =>
        console.error('[NewsRoute] Scrape error:', e)
      );
    }

    return NextResponse.json({ news: newsItems, count: newsItems.length });
  } catch (err) {
    console.error('News fetch error:', err);
    return NextResponse.json({ news: [], count: 0, error: err.message }, { status: 500 });
  }
}

// ─── Arka Plan Haber Kazıyıcı (Dev.to + HackerNews) ─────────────────────────
async function scrapeInBackground(disciplines) {
  const tags = disciplines.length > 0
    ? getTagsForDisciplines(disciplines)
    : Object.values(DISCIPLINE_TAGS).flat();

  const uniqueTags = [...new Set(tags)].slice(0, 8); // fazla istek önle
  const articles = [];
  const seenUrls = new Set();

  await Promise.allSettled(
    uniqueTags.slice(0, 4).map(async (tag) => {
      // Dev.to
      try {
        const r = await fetch(
          `https://dev.to/api/articles?tag=${tag}&per_page=4&top=1`,
          { signal: AbortSignal.timeout(8000) }
        );
        if (r.ok) {
          const items = await r.json();
          for (const item of items) {
            if (item.url && !seenUrls.has(item.url)) {
              seenUrls.add(item.url);
              articles.push({
                title: item.title,
                url: item.url,
                source: 'devto',
                summary: item.description || '',
                tags: [tag, ...(item.tag_list || []).slice(0, 3)],
                published_at: item.published_at,
              });
            }
          }
        }
      } catch (_) {}

      // HackerNews
      try {
        const r = await fetch(
          `https://hn.algolia.com/api/v1/search?query=${encodeURIComponent(tag)}&tags=story&hitsPerPage=3`,
          { signal: AbortSignal.timeout(8000) }
        );
        if (r.ok) {
          const data = await r.json();
          for (const hit of (data.hits || [])) {
            if (hit.url && !seenUrls.has(hit.url)) {
              seenUrls.add(hit.url);
              articles.push({
                title: hit.title,
                url: hit.url,
                source: 'hackernews',
                summary: `${hit.points || 0} puan · ${hit.num_comments || 0} yorum`,
                tags: [tag],
                published_at: hit.created_at,
              });
            }
          }
        }
      } catch (_) {}
    })
  );

  if (articles.length > 0) {
    await saveNewsBulk(articles);
  }
}
