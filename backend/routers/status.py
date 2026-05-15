from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    return {
        "platform": "OmNexus Ecosystem",
        "status": "online",
        "message": "OmNexus Core API is operational."
    }

@router.get("/api/v1/straxon/status")
async def straxon_status():
    return {"product": "STRAXON QART", "status": "Phase 1", "jarvis": "Online"}
