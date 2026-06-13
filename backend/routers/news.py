from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from core.database import db
from services.news_service import news_service

router = APIRouter(prefix="/api/v1/straxon")


class NewsClickRequest(BaseModel):
    profile_id: str
    news_id: str
    email: str


@router.get("/news")
async def get_news(
    background_tasks: BackgroundTasks,
    disciplines: str = "",
    limit: int = 20
):
    """
    Haberleri getir ve arka planda yeni haberleri asenkron olarak çek/güncelle.
    disciplines: Virgülle ayrılmış disiplin listesi (örn. "Backend Engineer,AI & ML Engineer")
    """
    discipline_list = [d.strip() for d in disciplines.split(",") if d.strip()] if disciplines else []

    # Arka planda haber kazıma (dashboard her yüklendiğinde asenkron tetiklenir)
    background_tasks.add_task(_scrape_in_background, discipline_list)

    # Mevcut haberleri filtreli veya filtresiz getir
    tags = news_service.get_tags_for_disciplines(discipline_list) if discipline_list else None
    news_items = await db.get_news(tags=tags, limit=limit)

    return {"news": news_items, "count": len(news_items)}


@router.post("/news/click")
async def record_news_click(payload: NewsClickRequest):
    """
    Haber tıklamasını kaydet ve kullanıcıya +15 Zeka Derinliği puanı ver.
    """
    profile = await db.get_profile(payload.email)
    if not profile:
        raise HTTPException(status_code=404, detail="Profil bulunamadı")

    await db.log_news_click(payload.profile_id, payload.news_id)
    new_score = await db.add_score(payload.email, 15, "News article clicked")

    return {
        "status": "success",
        "score_added": 15,
        "new_intelligence_score": new_score
    }


async def _scrape_in_background(disciplines: list):
    """Arka planda çalışan haber kazıma görevi."""
    try:
        count = await news_service.scrape_and_save(disciplines if disciplines else None)
        print(f"[NewsService] Arka planda {count} yeni haber kaydedildi.")
    except Exception as e:
        print(f"[NewsService] Arka plan kazıma hatası: {e}")
