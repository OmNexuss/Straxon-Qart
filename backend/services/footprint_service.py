from core.database import db

async def calculate_competence_score(profile_id: str) -> dict:
    """
    Kullanıcının Digital Footprint ve şirket içi (Straxon) görev tamamlama verilerine göre 
    Competence Score (Yetkinlik Puanı) hesaplar.
    
    Phase 1:
      - GitHub commit sayıları
      - Tamamlanan user_tasks
    """
    competence_score = 0
    details = {
        "github_commits_score": 0,
        "internal_tasks_score": 0,
        "total_competence_score": 0
    }
    
    try:
        # 1. Internal Tasks (Tamamlanmış Görevler)
        tasks = await db.get_user_tasks(profile_id)
        completed_tasks = [t for t in tasks if t.get("is_completed")]
        
        # Her tamamlanan görev 10 puan (Örnek ağırlık)
        details["internal_tasks_score"] = len(completed_tasks) * 10
        competence_score += details["internal_tasks_score"]
        
        # 2. External Footprints (Phase 1: GitHub Commits)
        # TODO: db.get_digital_footprint() eklendiğinde doğrudan oradan çağrılabilir.
        # Şimdilik DB'den github profilini çekip varsa basit bir puan eklenebilir
        # ya da db_schema.sql'de tanımlı 'digital_footprints' tablosundan okuma yapılabilir.
        
        # Bu fonksiyonun database.py'de eklendiğini varsayarak (get_digital_footprints):
        footprints = await db.get_digital_footprints(profile_id)
        
        github_commits = 0
        for fp in footprints:
            if fp.get("platform") == "github":
                summary = fp.get("data_summary", {})
                github_commits = summary.get("total_commits", 0)
        
        # Her GitHub commit'i için 2 puan (Örnek ağırlık)
        details["github_commits_score"] = github_commits * 2
        competence_score += details["github_commits_score"]
        
        details["total_competence_score"] = competence_score
        return details

    except Exception as e:
        print(f"[FootprintService] Competence Score hesaplama hatası: {e}")
        return details
