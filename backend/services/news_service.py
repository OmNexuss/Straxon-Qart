import httpx
import asyncio
from typing import List, Dict, Any
from core.database import db


class NewsService:
    """
    Dev.to API ve HackerNews (Algolia) API'lerinden teknoloji haberlerini
    asenkron olarak çekip Supabase'e kaydeden servis.
    """

    DEVTO_API = "https://dev.to/api/articles"
    HN_API = "https://hn.algolia.com/api/v1/search"

    # Disiplin → Etiket / Arama terimi eşleştirme haritası
    DISCIPLINE_TAGS: Dict[str, List[str]] = {
        "Backend Engineer":           ["backend", "api", "fastapi", "django", "go", "rust", "database"],
        "Frontend Engineer":          ["frontend", "react", "nextjs", "typescript", "css", "webdev"],
        "DevOps Engineer":            ["devops", "kubernetes", "docker", "terraform", "cicd", "cloud"],
        "AI & ML Engineer":           ["machinelearning", "deeplearning", "ai", "llm", "python", "datascience"],
        "Cyber Security Specialist":  ["security", "cybersecurity", "hacking", "ctf", "cryptography"],
        "Blockchain & Web3 Developer":["blockchain", "web3", "solidity", "ethereum", "defi"],
        "Mobile Developer":           ["android", "ios", "flutter", "kotlin", "swift", "reactnative"],
        "Game Developer":             ["gamedev", "unity", "godot", "unrealengine", "opengl"],
        "Embedded & IoT Engineer":    ["embedded", "iot", "arduino", "raspberrypi", "firmware"],
    }

    @classmethod
    async def fetch_devto(cls, tags: List[str], per_tag: int = 5) -> List[Dict[str, Any]]:
        """Dev.to'dan verilen etiketlere göre makale çek."""
        articles = []
        async with httpx.AsyncClient(timeout=10.0) as client:
            tasks = []
            for tag in tags[:3]:  # fazla istek atmamak için etiket sınırı
                tasks.append(
                    client.get(cls.DEVTO_API, params={"tag": tag, "per_page": per_tag, "top": 1})
                )
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            for tag, resp in zip(tags[:3], responses):
                if isinstance(resp, Exception) or resp.status_code != 200:
                    continue
                for item in resp.json():
                    articles.append({
                        "title": item.get("title", ""),
                        "url": item.get("url", ""),
                        "source": "devto",
                        "summary": item.get("description") or item.get("readable_publish_date", ""),
                        "tags": [tag] + (item.get("tag_list") or [])[:4],
                        "published_at": item.get("published_at"),
                    })
        return articles

    @classmethod
    async def fetch_hackernews(cls, query: str, hits_per_page: int = 5) -> List[Dict[str, Any]]:
        """HackerNews Algolia API'sinden haber çek."""
        articles = []
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                resp = await client.get(
                    cls.HN_API,
                    params={"query": query, "tags": "story", "hitsPerPage": hits_per_page}
                )
                if resp.status_code != 200:
                    return []
                for hit in resp.json().get("hits", []):
                    url = hit.get("url")
                    title = hit.get("title")
                    if not url or not title:
                        continue
                    articles.append({
                        "title": title,
                        "url": url,
                        "source": "hackernews",
                        "summary": f"HackerNews · {hit.get('points', 0)} puan · {hit.get('num_comments', 0)} yorum",
                        "tags": [query],
                        "published_at": hit.get("created_at"),
                    })
            except Exception:
                pass
        return articles

    @classmethod
    async def scrape_and_save(cls, disciplines: List[str] = None) -> int:
        """
        Verilen disiplinlere (veya tüm disiplinlere) göre haberleri çek,
        Supabase'e kaydet. Kaydedilen haber sayısını döndür.
        """
        if not disciplines:
            disciplines = list(cls.DISCIPLINE_TAGS.keys())

        all_articles: List[Dict] = []
        seen_urls = set()

        for discipline in disciplines:
            tags = cls.DISCIPLINE_TAGS.get(discipline, [])
            if not tags:
                continue

            # Dev.to
            devto_articles = await cls.fetch_devto(tags[:2])
            # HackerNews (birincil etiketi kullan)
            hn_articles = await cls.fetch_hackernews(tags[0])

            for article in devto_articles + hn_articles:
                url = article.get("url", "")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    all_articles.append(article)

        saved = await db.save_news_bulk(all_articles)
        return saved

    @classmethod
    def get_tags_for_disciplines(cls, disciplines: List[str]) -> List[str]:
        """Verilen disiplinler için ilgili etiketleri döndür."""
        tags = set()
        for d in disciplines:
            tags.update(cls.DISCIPLINE_TAGS.get(d, []))
        return list(tags)


news_service = NewsService()
