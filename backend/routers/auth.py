import httpx
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from core.config import settings
from core.database import db

router = APIRouter(prefix="/api/v1/straxon/auth")

@router.get("/github")
async def github_login():
    return RedirectResponse(
        f"https://github.com/login/oauth/authorize?client_id={settings.GITHUB_CLIENT_ID}&redirect_uri={settings.GITHUB_REDIRECT_URI}&scope=repo,user"
    )

@router.get("/github/callback")
async def github_callback(code: str):
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            params={
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": settings.GITHUB_REDIRECT_URI
            }
        )
        token_data = token_response.json()
        access_token = token_data.get("access_token")
        
        user_response = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"token {access_token}"}
        )
        user_data = user_response.json()
        email = user_data.get("email") or f"{user_data.get('login')}@github.com"
        
        # Profili Güncelle ve +20 Puan Ver
        await db.create_or_update_profile({
            "email": email,
            "full_name": user_data.get("name"),
            "github_username": user_data.get("login"),
            "score_increase": 20
        })
        
        await db.log_intelligence(email, 20, "GitHub Integration connected")
        
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/dashboard?github_connected=true&username={user_data.get('login')}&email={email}")
