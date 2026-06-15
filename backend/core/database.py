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

    # ─── Profil Fonksiyonları ─────────────────────────────────────
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
                response = await client.post(
                    f"{self.url}/rest/v1/profiles",
                    headers=self.headers,
                    json={
                        "email": email,
                        "full_name": profile_data.get("full_name"),
                        "github_username": profile_data.get("github_username"),
                        "intelligence_score": 20,
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

    async def has_intelligence_depth_log(self, profile_id: str) -> bool:
        """Kullanıcının daha önce Intelligence Depth ödülü alıp almadığını loglardan kontrol et."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.url}/rest/v1/intelligence_logs?profile_id=eq.{profile_id}&reason=eq.Intelligence Depth Analysis: Consistent Reading Pattern (Top 3 Skills)",
                headers=self.headers
            )
            if response.status_code == 200:
                data = response.json()
                return len(data) > 0
            return False

    async def add_score(self, email: str, amount: int, reason: str):
        """Kullanıcının puanını artır ve logla."""
        profile = await self.get_profile(email)
        if not profile:
            return
        new_score = profile.get("intelligence_score", 0) + amount
        async with httpx.AsyncClient() as client:
            await client.patch(
                f"{self.url}/rest/v1/profiles?email=eq.{email}",
                headers=self.headers,
                json={"intelligence_score": new_score}
            )
        await self.log_intelligence(email, amount, reason)
        return new_score

    # ─── News Feed Fonksiyonları ──────────────────────────────────
    async def save_news_bulk(self, news_list: list) -> int:
        """Haberleri toplu olarak kaydet, zaten olanları atla (url UNIQUE)."""
        if not news_list:
            return 0
        saved = 0
        async with httpx.AsyncClient() as client:
            for item in news_list:
                resp = await client.post(
                    f"{self.url}/rest/v1/news_feed",
                    headers={**self.headers, "Prefer": "resolution=ignore-duplicates,return=minimal"},
                    json=item
                )
                if resp.status_code in (201, 200):
                    saved += 1
        return saved

    async def get_news(self, tags: list = None, limit: int = 20) -> list:
        """Haberleri getir; opsiyonel olarak disiplin etiketlerine göre filtrele."""
        async with httpx.AsyncClient() as client:
            url = f"{self.url}/rest/v1/news_feed?order=created_at.desc&limit={limit}"
            if tags:
                # Supabase array overlap: tags && '{tag1,tag2}'
                tag_filter = "{" + ",".join(tags) + "}"
                url += f"&tags=ov.{tag_filter}"
            response = await client.get(url, headers=self.headers)
            return response.json() if response.status_code == 200 else []

    async def log_news_click(self, profile_id: str, news_id: str):
        """Haber tıklamasını logla (gün içinde birden fazla tıklama engeli için kontrol dışında tutuldu)."""
        async with httpx.AsyncClient() as client:
            await client.post(
                f"{self.url}/rest/v1/news_click_logs",
                headers=self.headers,
                json={"profile_id": profile_id, "news_id": news_id}
            )

    async def get_top_skills(self, profile_id: str, limit: int = 3) -> list:
        """Kullanıcının en yüksek puanlı yeteneklerini getirir."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.url}/rest/v1/universal_skill_matrices?profile_id=eq.{profile_id}&order=score.desc&limit={limit}",
                headers=self.headers
            )
            return response.json() if response.status_code == 200 else []

    async def get_recent_news_clicks(self, profile_id: str, since_iso: str) -> list:
        """Belirtilen tarihten sonraki haber tıklama loglarını, haber detaylarıyla birlikte getirir."""
        async with httpx.AsyncClient() as client:
            # Supabase join syntax: select=*,news_feed(*)
            url = f"{self.url}/rest/v1/news_click_logs?profile_id=eq.{profile_id}&clicked_at=gte.{since_iso}&select=*,news_feed(*)"
            response = await client.get(url, headers=self.headers)
            return response.json() if response.status_code == 200 else []

    # ─── User Tasks Fonksiyonları ─────────────────────────────────
    async def get_user_tasks(self, profile_id: str) -> list:
        """Kullanıcıya ait tüm görevleri getir."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.url}/rest/v1/user_tasks?profile_id=eq.{profile_id}&order=created_at.asc",
                headers=self.headers
            )
            return response.json() if response.status_code == 200 else []

    async def create_user_task(self, profile_id: str, task_type: str, title: str, description: str = None, metadata: dict = None) -> dict:
        """Yeni görev oluştur."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.url}/rest/v1/user_tasks",
                headers=self.headers,
                json={
                    "profile_id": profile_id,
                    "task_type": task_type,
                    "title": title,
                    "description": description,
                    "metadata": metadata or {}
                }
            )
            data = response.json()
            return data[0] if isinstance(data, list) and data else data

    async def update_task_status(self, task_id: str, is_completed: bool) -> dict:
        """Görev tamamlama durumunu güncelle."""
        from datetime import datetime, timezone
        patch_data = {"is_completed": is_completed}
        if is_completed:
            patch_data["completed_at"] = datetime.now(timezone.utc).isoformat()
        else:
            patch_data["completed_at"] = None
        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"{self.url}/rest/v1/user_tasks?id=eq.{task_id}",
                headers=self.headers,
                json=patch_data
            )
            data = response.json()
            return data[0] if isinstance(data, list) and data else data

    # ─── Digital Footprints Fonksiyonları ────────────────────────
    async def save_digital_footprint(self, profile_id: str, platform: str, username: str, data_summary: dict):
        """Dijital ayak izi kaydı oluştur veya güncelle."""
        from datetime import datetime, timezone
        async with httpx.AsyncClient() as client:
            # Mevcut kaydı kontrol et
            resp = await client.get(
                f"{self.url}/rest/v1/digital_footprints?profile_id=eq.{profile_id}&platform=eq.{platform}",
                headers=self.headers
            )
            existing = resp.json()
            payload = {
                "profile_id": profile_id,
                "platform": platform,
                "username": username,
                "data_summary": data_summary,
                "last_synced_at": datetime.now(timezone.utc).isoformat()
            }
            if existing:
                await client.patch(
                    f"{self.url}/rest/v1/digital_footprints?profile_id=eq.{profile_id}&platform=eq.{platform}",
                    headers=self.headers,
                    json=payload
                )
            else:
                await client.post(
                    f"{self.url}/rest/v1/digital_footprints",
                    headers=self.headers,
                    json=payload
                )

    async def get_digital_footprints(self, profile_id: str) -> list:
        """Kullanıcının dijital ayak izi verilerini getirir."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.url}/rest/v1/digital_footprints?profile_id=eq.{profile_id}",
                headers=self.headers
            )
            return response.json() if response.status_code == 200 else []

db = SupabaseService()
