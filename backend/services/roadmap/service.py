import httpx
from typing import Dict, List, Any
from .constants import DISCIPLINES, HYBRID_TITLES

class RoadmapService:
    @staticmethod
    async def analyze_profile(github_username: str) -> Dict[str, Any]:
        """
        Kullanıcının GitHub repolarını çeker, 9 evrensel bilişim disiplininde
        yatkınlık skorları hesaplar, hibrit unvan üretir ve kişiselleştirilmiş
        kilometre taşları belirler.
        """
        if not github_username:
            return {
                "github_connected": False,
                "synthesis_title": "Henüz Analiz Edilmedi",
                "synthesis_emoji": "⚡",
                "compatibilities": [],
                "primary_milestone": None,
                "secondary_milestone": None,
                "language_distribution": {}
            }

        try:
            async with httpx.AsyncClient() as client:
                url = f"https://api.github.com/users/{github_username}/repos?sort=updated&per_page=30"
                headers = {"User-Agent": "Straxon-Qart-OmNexus"}
                response = await client.get(url, headers=headers, timeout=10.0)

                if response.status_code != 200:
                    return RoadmapService._fallback(github_username)

                repos = response.json()
                if not repos:
                    return RoadmapService._no_repos_result()

                # 1. Dil Dağılım Analizi
                lang_counts = {}
                for repo in repos:
                    lang = repo.get("language")
                    if lang:
                        lang_counts[lang] = lang_counts.get(lang, 0) + 1

                total = sum(lang_counts.values())
                lang_distribution = {
                    lang: round((cnt / total) * 100)
                    for lang, cnt in sorted(lang_counts.items(), key=lambda x: -x[1])
                } if total > 0 else {}

                # Repo corpus (isim + açıklama + topic) — küçük harf, tek metin
                repo_corpus = []
                for repo in repos:
                    name = (repo.get("name") or "").lower()
                    desc = (repo.get("description") or "").lower()
                    topics = " ".join(repo.get("topics") or []).lower()
                    repo_corpus.append(f"{name} {desc} {topics}")

                # 2. Her Disiplin için Skor Hesaplama
                discipline_scores = {}
                for discipline, data in DISCIPLINES.items():
                    # Dil puanı
                    lang_score = sum(
                        (lang_distribution.get(lang, 0) / 100.0) * weight
                        for lang, weight in data["lang_weights"].items()
                    )
                    # Repo imza puanı (0-30 arası bonus)
                    sig_hits = sum(
                        1 for corpus in repo_corpus
                        for sig in data["repo_signatures"]
                        if sig in corpus
                    )
                    sig_bonus = min(sig_hits * 3, 30)
                    raw = lang_score * 100 + sig_bonus
                    discipline_scores[discipline] = min(100, round(raw))

                # 3. Sıralama
                ranked = sorted(discipline_scores.items(), key=lambda x: -x[1])
                primary_name, primary_score = ranked[0]
                secondary_name, secondary_score = ranked[1] if len(ranked) > 1 else (None, 0)

                # 4. Uyumluluk Listesi (tüm disiplinler, skora göre sıralı, >=5 puan olanlar)
                compatibilities = [
                    {
                        "role": name,
                        "emoji": DISCIPLINES[name]["emoji"],
                        "color": DISCIPLINES[name]["color"],
                        "score": score,
                        "url": DISCIPLINES[name]["url"]
                    }
                    for name, score in ranked if score >= 5
                ]

                # 5. Sentez Unvanı (Hibrit Motor)
                synthesis_title, synthesis_emoji = RoadmapService._get_title(
                    primary_name, primary_score, secondary_name, secondary_score
                )

                # 6. Birincil Kilometre Taşı
                primary_milestone = RoadmapService._find_milestone(
                    primary_name, repo_corpus
                )

                # 7. İkincil Kilometre Taşı (eğer ikincil rota yeterince güçlüyse)
                secondary_milestone = None
                if secondary_name and secondary_score >= 35:
                    secondary_milestone = RoadmapService._find_milestone(
                        secondary_name, repo_corpus
                    )

                return {
                    "github_connected": True,
                    "synthesis_title": synthesis_title,
                    "synthesis_emoji": synthesis_emoji,
                    "compatibilities": compatibilities,
                    "primary_discipline": primary_name,
                    "primary_score": primary_score,
                    "secondary_discipline": secondary_name,
                    "secondary_score": secondary_score,
                    "primary_milestone": primary_milestone,
                    "secondary_milestone": secondary_milestone,
                    "language_distribution": lang_distribution
                }

        except Exception as e:
            return RoadmapService._error_result(str(e))

    @staticmethod
    def _get_title(primary: str, p_score: int, secondary: str, s_score: int):
        # Hibrit unvan tablosundan bak
        key = (primary, secondary)
        if key in HYBRID_TITLES and s_score >= 35:
            title, emoji = HYBRID_TITLES[key]
            return title, emoji
        # Varsayılan tekil unvan
        emoji = DISCIPLINES.get(primary, {}).get("emoji", "⚡")
        label = primary.replace("Engineer", "Uzmanı").replace("Developer", "Geliştirici").replace("Specialist", "Uzmanı")
        return label, emoji

    @staticmethod
    def _find_milestone(discipline_name: str, repo_corpus: List[str]) -> Dict:
        data = DISCIPLINES.get(discipline_name)
        if not data:
            return None
        for ms in data["milestones"]:
            has_evidence = any(
                sig in corpus
                for corpus in repo_corpus
                for sig in ms["signatures"]
            )
            if not has_evidence:
                return {
                    "discipline": discipline_name,
                    "title": ms["title"],
                    "anchor_url": ms["anchor_url"],
                    "why_needed": ms["why_needed"],
                    "action_steps": ms["action_steps"],
                    "roadmap_url": data["url"],
                    "emoji": data["emoji"],
                    "color": data["color"]
                }
        # Tüm konular mevcut → son konuyu ileri seviye olarak öner
        last = data["milestones"][-1]
        return {
            "discipline": discipline_name,
            "title": last["title"],
            "anchor_url": last["anchor_url"],
            "why_needed": "Tebrikler! Bu disiplindeki temel ve orta düzey konuların tümü projelerinizde tespit edildi. Sıradaki hedef ileri seviye konuları derinleştirmektir.",
            "action_steps": last["action_steps"],
            "roadmap_url": data["url"],
            "emoji": data["emoji"],
            "color": data["color"]
        }

    @staticmethod
    def _fallback(username: str) -> Dict:
        return {
            "github_connected": True,
            "synthesis_title": "Analiz Bekleniyor",
            "synthesis_emoji": "⏳",
            "compatibilities": [],
            "primary_milestone": {
                "discipline": "General",
                "title": "GitHub Profilinizi Güncelleyin",
                "anchor_url": "https://roadmap.sh",
                "why_needed": "GitHub API rate limit veya erişim sorunu nedeniyle depolarınız analiz edilemedi. Kısa süre sonra tekrar deneyin.",
                "action_steps": [
                    "GitHub profilinizin herkese açık (public) olduğundan emin olun",
                    "Depolarınıza açıklama ve topic etiketleri ekleyin"
                ],
                "roadmap_url": "https://roadmap.sh",
                "emoji": "⏳",
                "color": "#6b7280"
            },
            "secondary_milestone": None,
            "language_distribution": {}
        }

    @staticmethod
    def _no_repos_result() -> Dict:
        return {
            "github_connected": True,
            "synthesis_title": "İlk Depoyu Oluşturun",
            "synthesis_emoji": "🚀",
            "compatibilities": [],
            "primary_milestone": {
                "discipline": "General",
                "title": "İlk Projenizi Yayınlayın",
                "anchor_url": "https://roadmap.sh",
                "why_needed": "GitHub profilinizde henüz depo bulunamadı. Jarvis sizi analiz edebilmek için en az birkaç projeye ihtiyaç duyuyor.",
                "action_steps": [
                    "Lokal bir proje klasörünü 'git init' ile Git deposuna dönüştürün",
                    "Deponuzu public olarak GitHub'a push edin",
                    "README.md ekleyerek ne yaptığınızı açıklayın"
                ],
                "roadmap_url": "https://roadmap.sh",
                "emoji": "🚀",
                "color": "#d4af37"
            },
            "secondary_milestone": None,
            "language_distribution": {}
        }

    @staticmethod
    def _error_result(err: str) -> Dict:
        return {
            "github_connected": True,
            "synthesis_title": "Analiz Hatası",
            "synthesis_emoji": "⚠️",
            "compatibilities": [],
            "primary_milestone": {
                "discipline": "Error",
                "title": "Beklenmeyen Hata",
                "anchor_url": "https://roadmap.sh",
                "why_needed": f"Analiz sırasında bir hata oluştu: {err}",
                "action_steps": ["Daha sonra tekrar deneyin", "GitHub bağlantınızın aktif olduğundan emin olun"],
                "roadmap_url": "https://roadmap.sh",
                "emoji": "⚠️",
                "color": "#ef4444"
            },
            "secondary_milestone": None,
            "language_distribution": {}
        }


roadmap_service = RoadmapService()
