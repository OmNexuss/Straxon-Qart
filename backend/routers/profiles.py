from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.schemas import WaitlistEntry
from core.database import db
from services.email_service import email_service
from services.roadmap import roadmap_service
from services.jarvis_service import jarvis_service
from services.news_service import news_service

router = APIRouter(prefix="/api/v1/straxon")


class TaskStatusUpdate(BaseModel):
    task_id: str
    is_completed: bool


class TaskCreateRequest(BaseModel):
    profile_id: str
    task_type: str = "custom"
    title: str
    description: str = None
    metadata: dict = None


@router.post("/waitlist")
async def join_waitlist(entry: WaitlistEntry):
    try:
        await db.create_or_update_profile({
            "email": entry.email,
            "full_name": entry.name,
            "score_increase": 0
        })
        email_service.send_waitlist_welcome(entry.name, entry.email)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/profile/{email}")
async def get_user_profile(email: str):
    profile = await db.get_profile(email)
    if not profile:
        raise HTTPException(status_code=404, detail="Profil bulunamadı")

    profile_dict = dict(profile)
    github_username = profile_dict.get("github_username")
    profile_id = profile_dict.get("id")

    # 1. Roadmap analizi (GitHub)
    roadmap_analysis = await roadmap_service.analyze_profile(github_username)
    profile_dict["roadmap_match"] = roadmap_analysis

    # 2. Kullanıcıya ait görevleri getir
    tasks = await db.get_user_tasks(profile_id) if profile_id else []
    profile_dict["tasks"] = tasks

    # 3. Jarvis için: disipline göre ilgili haberleri getir
    primary_discipline = roadmap_analysis.get("primary_discipline")
    disciplines = [primary_discipline] if primary_discipline else []
    news_tags = news_service.get_tags_for_disciplines(disciplines)
    recent_news = await db.get_news(tags=news_tags if news_tags else None, limit=5)

    # 4. Jarvis tavsiyesi üret (Gemini AI)
    jarvis_insight = await jarvis_service.generate_insight(
        github_username=github_username or "",
        synthesis_title=roadmap_analysis.get("synthesis_title"),
        primary_discipline=primary_discipline,
        primary_score=roadmap_analysis.get("primary_score", 0),
        primary_milestone=roadmap_analysis.get("primary_milestone"),
        secondary_milestone=roadmap_analysis.get("secondary_milestone"),
        recent_news=recent_news,
        intelligence_score=profile_dict.get("intelligence_score", 0),
    )
    profile_dict["jarvis_insight"] = jarvis_insight

    # 5. Otomatik görev oluşturma: eğer kullanıcının henüz görevi yoksa kilometre taşlarından oluştur
    if not tasks and profile_id and roadmap_analysis.get("github_connected"):
        await _seed_tasks_from_milestones(
            profile_id,
            roadmap_analysis.get("primary_milestone"),
            roadmap_analysis.get("secondary_milestone"),
            roadmap_analysis.get("synthesis_title"),
            primary_discipline,
        )
        # Güncel görevleri tekrar al
        profile_dict["tasks"] = await db.get_user_tasks(profile_id)

    return profile_dict


@router.patch("/tasks/status")
async def update_task_status(payload: TaskStatusUpdate):
    """Görev tamamlama durumunu güncelle."""
    result = await db.update_task_status(payload.task_id, payload.is_completed)
    if not result:
        raise HTTPException(status_code=404, detail="Görev bulunamadı")
    return {"status": "updated", "task": result}


@router.post("/tasks")
async def create_task(payload: TaskCreateRequest):
    """Kullanıcı için yeni görev oluştur."""
    task = await db.create_user_task(
        profile_id=payload.profile_id,
        task_type=payload.task_type,
        title=payload.title,
        description=payload.description,
        metadata=payload.metadata,
    )
    return {"status": "created", "task": task}


async def _seed_tasks_from_milestones(
    profile_id: str,
    primary_milestone: dict,
    secondary_milestone: dict,
    synthesis_title: str,
    primary_discipline: str,
):
    """
    GitHub analizi tamamlandıktan sonra kilometre taşlarını otomatik olarak
    kullanıcının görev listesine ekle (yalnızca ilk kez).
    """
    if primary_milestone:
        await db.create_user_task(
            profile_id=profile_id,
            task_type="milestone",
            title=primary_milestone.get("title", "Birincil Hedef"),
            description=primary_milestone.get("why_needed"),
            metadata={
                "discipline": primary_milestone.get("discipline"),
                "anchor_url": primary_milestone.get("anchor_url"),
                "action_steps": primary_milestone.get("action_steps", []),
                "color": primary_milestone.get("color"),
                "emoji": primary_milestone.get("emoji"),
                "label": "Birincil Hedef",
            },
        )
    if secondary_milestone:
        await db.create_user_task(
            profile_id=profile_id,
            task_type="milestone",
            title=secondary_milestone.get("title", "İkincil Hedef"),
            description=secondary_milestone.get("why_needed"),
            metadata={
                "discipline": secondary_milestone.get("discipline"),
                "anchor_url": secondary_milestone.get("anchor_url"),
                "action_steps": secondary_milestone.get("action_steps", []),
                "color": secondary_milestone.get("color"),
                "emoji": secondary_milestone.get("emoji"),
                "label": "İkincil Hedef",
            },
        )
