import httpx
from core.config import settings

class SupabaseService:
    def __init__(self):
        self.url = settings.SUPABASE_URL
        self.key = settings.SUPABASE_KEY
        self.headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }

    async def get_profile(self, email: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.url}/rest/v1/profiles?email=eq.{email}",
                headers=self.headers
            )
            data = response.json()
            return data[0] if data else None

    async def create_or_update_profile(self, profile_data: dict):
        email = profile_data.get("email")
        existing = await self.get_profile(email)
        
        async with httpx.AsyncClient() as client:
            if existing:
                # Güncelleme (Puanı artır)
                new_score = existing.get("intelligence_score", 0) + profile_data.get("score_increase", 0)
                await client.patch(
                    f"{self.url}/rest/v1/profiles?email=eq.{email}",
                    headers=self.headers,
                    json={
                        "intelligence_score": new_score,
                        "github_username": profile_data.get("github_username"),
                        "jarvis_mood": "Analyzing"
                    }
                )
                return {"status": "updated", "score": new_score}
            else:
                # Yeni Kayıt
                response = await client.post(
                    f"{self.url}/rest/v1/profiles",
                    headers=self.headers,
                    json={
                        "email": email,
                        "full_name": profile_data.get("full_name"),
                        "github_username": profile_data.get("github_username"),
                        "intelligence_score": 20, # İlk bağlantı ödülü
                        "jarvis_mood": "Analyzing"
                    }
                )
                return {"status": "created", "score": 20}

    async def log_intelligence(self, email: str, amount: int, reason: str):
        profile = await self.get_profile(email)
        if profile:
            async with httpx.AsyncClient() as client:
                await client.post(
                    f"{self.url}/rest/v1/intelligence_logs",
                    headers=self.headers,
                    json={
                        "profile_id": profile["id"],
                        "change_amount": amount,
                        "reason": reason
                    }
                )

db = SupabaseService()
