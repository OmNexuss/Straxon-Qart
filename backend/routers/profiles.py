from fastapi import APIRouter, HTTPException
from models.schemas import WaitlistEntry
from core.database import db
from services.email_service import email_service
from services.roadmap import roadmap_service

router = APIRouter(prefix="/api/v1/straxon")

@router.post("/waitlist")
async def join_waitlist(entry: WaitlistEntry):
    try:
        # Waitlist'e ekle ve aynı zamanda profil oluştur
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
    
    # GitHub verilerini analiz et ve profil objesine ekle
    roadmap_analysis = await roadmap_service.analyze_profile(github_username)
    profile_dict["roadmap_match"] = roadmap_analysis
    
    return profile_dict
