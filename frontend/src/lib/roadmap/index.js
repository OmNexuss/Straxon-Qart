// ─────────────────────────────────────────────────────────────────────────────
// ROADMAP SERVICE  (index.js)
// Python backend/services/roadmap/service.py → RoadmapService.analyze_profile()
// Bu dosya Next.js tarafından @/lib/roadmap import'larında otomatik çözümlenir.
// ─────────────────────────────────────────────────────────────────────────────

import { DISCIPLINES, HYBRID_TITLES } from "./constants";

// ─────────────────────────────────────────────────────────────────────────────
// HELPER FUNCTIONS
// ─────────────────────────────────────────────────────────────────────────────

function getTitle(primary, pScore, secondary, sScore) {
  const key = `${primary}|${secondary}`;
  if (HYBRID_TITLES[key] && sScore >= 35) {
    const [title, emoji] = HYBRID_TITLES[key];
    return [title, emoji];
  }
  const emoji = DISCIPLINES[primary]?.emoji || "⚡";
  return [primary, emoji];
}

function findMilestone(disciplineName, repoCorpus) {
  const data = DISCIPLINES[disciplineName];
  if (!data) return null;

  for (const ms of data.milestones) {
    const hasEvidence = repoCorpus.some((corpus) =>
      ms.signatures.some((sig) => corpus.includes(sig))
    );
    if (!hasEvidence) {
      return {
        discipline: disciplineName,
        title: ms.title,
        anchor_url: ms.anchor_url,
        why_needed: ms.why_needed,
        action_steps: ms.action_steps,
        roadmap_url: data.url,
        emoji: data.emoji,
        color: data.color,
      };
    }
  }

  // Tüm konular mevcut → son konuyu ileri seviye olarak öner
  const last = data.milestones[data.milestones.length - 1];
  return {
    discipline: disciplineName,
    title: last.title,
    anchor_url: last.anchor_url,
    why_needed:
      "Tebrikler! Bu disiplindeki temel ve orta düzey konuların tümü projelerinizde tespit edildi. Sıradaki hedef ileri seviye konuları derinleştirmektir.",
    action_steps: last.action_steps,
    roadmap_url: data.url,
    emoji: data.emoji,
    color: data.color,
  };
}

// ─────────────────────────────────────────────────────────────────────────────
// FALLBACK HELPERS
// ─────────────────────────────────────────────────────────────────────────────

function _fallback(username) {
  return {
    github_connected: true,
    synthesis_title: "Analiz Bekleniyor",
    synthesis_emoji: "⏳",
    compatibilities: [],
    primary_milestone: {
      discipline: "General",
      title: "GitHub Profilinizi Güncelleyin",
      anchor_url: "https://roadmap.sh",
      why_needed:
        "GitHub API rate limit veya erişim sorunu nedeniyle depolarınız analiz edilemedi.",
      action_steps: [
        "GitHub profilinizin herkese açık (public) olduğundan emin olun",
        "Depolarınıza açıklama ve topic etiketleri ekleyin",
      ],
      roadmap_url: "https://roadmap.sh",
      emoji: "⏳",
      color: "#6b7280",
    },
    secondary_milestone: null,
    language_distribution: {},
  };
}

function _noRepos() {
  return {
    github_connected: true,
    synthesis_title: "İlk Depoyu Oluşturun",
    synthesis_emoji: "🚀",
    compatibilities: [],
    primary_milestone: {
      discipline: "General",
      title: "İlk Projenizi Yayınlayın",
      anchor_url: "https://roadmap.sh",
      why_needed:
        "GitHub profilinizde henüz depo bulunamadı. Jarvis sizi analiz edebilmek için en az birkaç projeye ihtiyaç duyuyor.",
      action_steps: [
        "Lokal bir proje klasörünü 'git init' ile Git deposuna dönüştürün",
        "Deponuzu public olarak GitHub'a push edin",
        "README.md ekleyerek ne yaptığınızı açıklayın",
      ],
      roadmap_url: "https://roadmap.sh",
      emoji: "🚀",
      color: "#d4af37",
    },
    secondary_milestone: null,
    language_distribution: {},
  };
}

function _error(err) {
  return {
    github_connected: true,
    synthesis_title: "Analiz Hatası",
    synthesis_emoji: "⚠️",
    compatibilities: [],
    primary_milestone: {
      discipline: "Error",
      title: "Beklenmeyen Hata",
      anchor_url: "https://roadmap.sh",
      why_needed: `Analiz sırasında bir hata oluştu: ${err}`,
      action_steps: [
        "Daha sonra tekrar deneyin",
        "GitHub bağlantınızın aktif olduğundan emin olun",
      ],
      roadmap_url: "https://roadmap.sh",
      emoji: "⚠️",
      color: "#ef4444",
    },
    secondary_milestone: null,
    language_distribution: {},
  };
}

// ─────────────────────────────────────────────────────────────────────────────
// MAIN ANALYZE FUNCTION
// ─────────────────────────────────────────────────────────────────────────────

export async function analyzeProfile(githubUsername) {
  if (!githubUsername) {
    return {
      github_connected: false,
      synthesis_title: "Henüz Analiz Edilmedi",
      synthesis_emoji: "⚡",
      compatibilities: [],
      primary_milestone: null,
      secondary_milestone: null,
      language_distribution: {},
    };
  }

  try {
    const url = `https://api.github.com/users/${githubUsername}/repos?sort=updated&per_page=30`;
    const res = await fetch(url, {
      headers: { "User-Agent": "Straxon-Qart-OmNexus" },
      next: { revalidate: 300 }, // 5 dk cache
    });

    if (!res.ok) return _fallback(githubUsername);

    const repos = await res.json();
    if (!repos || repos.length === 0) return _noRepos();

    // 1. Dil Dağılım Analizi
    const langCounts = {};
    for (const repo of repos) {
      if (repo.language) {
        langCounts[repo.language] = (langCounts[repo.language] || 0) + 1;
      }
    }
    const total = Object.values(langCounts).reduce((a, b) => a + b, 0);
    const langDist = {};
    if (total > 0) {
      for (const [lang, cnt] of Object.entries(langCounts).sort((a, b) => b[1] - a[1])) {
        langDist[lang] = Math.round((cnt / total) * 100);
      }
    }

    // Repo corpus
    const repoCorpus = repos.map((repo) => {
      const name = (repo.name || "").toLowerCase();
      const desc = (repo.description || "").toLowerCase();
      const topics = (repo.topics || []).join(" ").toLowerCase();
      return `${name} ${desc} ${topics}`;
    });

    // 2. Her Disiplin için Skor
    const disciplineScores = {};
    for (const [discipline, data] of Object.entries(DISCIPLINES)) {
      let langScore = 0;
      for (const [lang, weight] of Object.entries(data.lang_weights)) {
        langScore += ((langDist[lang] || 0) / 100) * weight;
      }
      let sigHits = 0;
      for (const corpus of repoCorpus) {
        for (const sig of data.repo_signatures) {
          if (corpus.includes(sig)) sigHits++;
        }
      }
      const sigBonus = Math.min(sigHits * 3, 30);
      disciplineScores[discipline] = Math.min(100, Math.round(langScore * 100 + sigBonus));
    }

    // 3. Sıralama
    const ranked = Object.entries(disciplineScores).sort((a, b) => b[1] - a[1]);
    const [primaryName, primaryScore] = ranked[0];
    const [secondaryName, secondaryScore] = ranked[1] || [null, 0];

    // 4. Uyumluluk Listesi
    const compatibilities = ranked
      .filter(([, score]) => score >= 5)
      .map(([name, score]) => ({
        role: name,
        emoji: DISCIPLINES[name].emoji,
        color: DISCIPLINES[name].color,
        score,
        url: DISCIPLINES[name].url,
      }));

    // 5. Sentez Unvanı
    const [synthesisTitle, synthesisEmoji] = getTitle(
      primaryName, primaryScore, secondaryName, secondaryScore
    );

    // 6. Kilometre Taşları
    const primaryMilestone = findMilestone(primaryName, repoCorpus);
    let secondaryMilestone = null;
    if (secondaryName && secondaryScore >= 35) {
      secondaryMilestone = findMilestone(secondaryName, repoCorpus);
    }

    return {
      github_connected: true,
      synthesis_title: synthesisTitle,
      synthesis_emoji: synthesisEmoji,
      compatibilities,
      primary_discipline: primaryName,
      primary_score: primaryScore,
      secondary_discipline: secondaryName,
      secondary_score: secondaryScore,
      primary_milestone: primaryMilestone,
      secondary_milestone: secondaryMilestone,
      language_distribution: langDist,
    };
  } catch (e) {
    return _error(String(e));
  }
}
