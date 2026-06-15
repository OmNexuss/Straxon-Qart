from datetime import datetime, timezone, timedelta
from core.database import db

async def analyze_intelligence_depth(profile_id: str, email: str):
    """
    Arka planda çalışarak Intelligence Depth analizini yapar.
    Sadece yeterli veri varsa ve koşullar sağlanıyorsa (3 ayda en az 20 okuma) bir kez +15 puan verir.
    """
    try:
        # Profil bilgilerini al
        profile = await db.get_profile(email)
        if not profile:
            return
        
        # Eğer zaten ödül verildiyse loglardan kontrol et
        has_awarded = await db.has_intelligence_depth_log(profile["id"])
        if has_awarded:
            print(f"[Analytics] Profil {profile_id} zaten Intelligence Depth ödülünü almış. Atlanıyor.")
            return

        top_skills_data = await db.get_top_skills(profile_id, limit=3)
        top_skills = [skill.get("skill_name") for skill in top_skills_data]
        
        if not top_skills:
            print(f"[Analytics] Profil {profile_id} için skill matrix bulunamadı. Atlanıyor.")
            return

        # 2. Son 3 aydaki haber tıklamalarını getir.
        three_months_ago = datetime.now(timezone.utc) - timedelta(days=90)
        since_iso = three_months_ago.isoformat()
        
        recent_clicks = await db.get_recent_news_clicks(profile_id, since_iso)
        
        # Tags ile top_skills uyuşmasını kontrol et
        matching_articles_count = 0
        for click in recent_clicks:
            news = click.get("news_feed", {})
            tags = news.get("tags", [])
            # Eğer haberin etiketlerinden herhangi biri top_skills içinde varsa say
            if any(skill in tags for skill in top_skills):
                matching_articles_count += 1

        print(f"[Analytics] Profil {profile_id}: {matching_articles_count} eşleşen haber okundu (Hedef: 20)")
        
        if matching_articles_count >= 20:
            print(f"[Analytics] Profil {profile_id} için koşullar sağlandı, +15 Intelligence Depth ekleniyor.")
            await db.add_score(email, 15, "Intelligence Depth Analysis: Consistent Reading Pattern (Top 3 Skills)")

    except Exception as e:
        print(f"[AnalyticsService] Analiz hatası: {e}")

