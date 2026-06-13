import httpx
import json
from typing import Dict, Any, List, Optional
from core.config import settings


class JarvisService:
    """
    Google Gemini API'sini kullanan proaktif Jarvis zeka servisi.
    Kullanıcının GitHub analiz sonuçlarını ve güncel teknoloji haberlerini
    harmanlayarak kişiselleştirilmiş Türkçe tavsiyeler üretir.
    """

    GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

    @classmethod
    async def _call_gemini(cls, prompt: str) -> Optional[str]:
        """Gemini API'ye istek gönder ve yanıtı döndür."""
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            return None

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 512,
                "responseMimeType": "application/json"
            }
        }

        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                resp = await client.post(
                    f"{cls.GEMINI_URL}?key={api_key}",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                if resp.status_code != 200:
                    return None
                data = resp.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return text
        except Exception as e:
            print(f"[JarvisService] Gemini API hatası: {e}")
            return None

    @classmethod
    async def generate_insight(
        cls,
        github_username: str,
        synthesis_title: str,
        primary_discipline: str,
        primary_score: int,
        primary_milestone: Optional[Dict],
        secondary_milestone: Optional[Dict],
        recent_news: List[Dict],
        intelligence_score: int,
    ) -> str:
        """
        Kullanıcının profiline göre proaktif Türkçe Jarvis tavsiyesi üret.
        Gemini API yanıt vermezse fallback mesaj döner.
        """
        # Haberleri prompt için özetle
        news_context = ""
        if recent_news:
            headlines = [f"- {n.get('title', '')}" for n in recent_news[:5]]
            news_context = "Son teknoloji haberleri:\n" + "\n".join(headlines)

        milestone_context = ""
        if primary_milestone:
            milestone_context = f"Birincil hedef: {primary_milestone.get('title', '')} — {primary_milestone.get('why_needed', '')}"

        prompt = f"""Sen Straxon-Qart platformunun yapay zeka asistanı Jarvis'sin.
Kullanıcıya ait bilgiler:
- GitHub: @{github_username}
- Geliştirici Kimliği: {synthesis_title or primary_discipline}
- Ana Disiplin Skoru: %{primary_score}
- Zeka Derinliği: %{intelligence_score}
- {milestone_context}
{news_context}

Bu bilgilere dayanarak kullanıcıya özgün, motive edici, kısa (2-3 cümle) ve Türkçe bir proaktif kariyer tavsiyesi üret.
Tavsiyeyi JSON formatında döndür: {{"insight": "tavsiye metni buraya"}}"""

        result = await cls._call_gemini(prompt)
        if result:
            try:
                parsed = json.loads(result)
                return parsed.get("insight", result)
            except json.JSONDecodeError:
                # JSON parse edilemezse düz metin olarak döndür
                return result.strip()

        # Gemini API çalışmıyor veya anahtar yoksa fallback
        if synthesis_title and primary_discipline:
            return (
                f"Hoş geldin @{github_username}. Jarvis seni \"{synthesis_title}\" olarak tanımladı. "
                f"Zeka Derinliğin %{intelligence_score}. "
                f"{'Birincil hedefin: ' + primary_milestone['title'] + '. Roadmap üzerindeki bu konuya odaklan.' if primary_milestone else 'GitHub profilini zenginleştirerek analizimi derinleştirmeme yardımcı ol.'}"
            )
        return (
            f"Henüz bir teknik platform bağlanmadı. Jarvis'in seni analiz edebilmesi için "
            "GitHub hesabını bağla ve profilini oluştur."
        )

    @classmethod
    async def tag_news_for_user(
        cls,
        news_titles: List[str],
        primary_discipline: str,
    ) -> List[int]:
        """
        Verilen haber başlıklarından kullanıcının ana disipliniyle ilgili olanların
        indekslerini döndür. Gemini API ile filtreleme yapar.
        """
        if not news_titles:
            return []

        numbered = "\n".join(f"{i}. {t}" for i, t in enumerate(news_titles))
        prompt = f"""Aşağıdaki haber başlıklarından "{primary_discipline}" disipliniyle ilgili olanların numaralarını seç.
{numbered}
Yanıtı JSON formatında ver: {{"relevant_indices": [0, 2, 5]}}"""

        result = await cls._call_gemini(prompt)
        if result:
            try:
                parsed = json.loads(result)
                indices = parsed.get("relevant_indices", [])
                return [i for i in indices if isinstance(i, int) and 0 <= i < len(news_titles)]
            except Exception:
                pass

        # Fallback: tüm haberleri ilgili kabul et
        return list(range(len(news_titles)))


jarvis_service = JarvisService()
