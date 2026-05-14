import os
import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import resend
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Vercel routePrefix ile uyumluluk için
ROOT_PATH = os.getenv("ROOT_PATH", "")
app = FastAPI(title="OmNexus Core API", version="1.0.0", root_path=ROOT_PATH)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Yapılandırma
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
resend.api_key = RESEND_API_KEY
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
# Vercel'de veya yerelde çalışırken dinamik olması için
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
GITHUB_REDIRECT_URI = f"{BASE_URL}/api/v1/straxon/auth/github/callback"

class WaitlistEntry(BaseModel):
    name: str
    email: EmailStr

@app.get("/")
async def root():
    return {
        "platform": "OmNexus Ecosystem",
        "status": "online",
        "message": "OmNexus Core API is operational."
    }

# --- STRAXON WAITLIST ---
@app.post("/api/v1/straxon/waitlist")
async def join_waitlist(entry: WaitlistEntry):
    try:
        async with httpx.AsyncClient() as client:
            db_response = await client.post(
                f"{SUPABASE_URL}/rest/v1/waitlist",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                    "Content-Type": "application/json",
                    "Prefer": "return=representation"
                },
                json={
                    "name": entry.name,
                    "email": entry.email
                }
            )
            
            if db_response.status_code != 201:
                error_data = db_response.json()
                if "duplicate key" in str(error_data):
                    raise HTTPException(status_code=400, detail="Bu e-posta adresi zaten bekleme listesinde kayıtlı.")
                raise HTTPException(status_code=db_response.status_code, detail="Veritabanı hatası oluştu.")
            
            db_data = db_response.json()

        email_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #0a0a0c; color: #f0f0f2; padding: 40px;">
                <div style="max-width: 600px; margin: 0 auto; background: #1a1a1e; padding: 30px; border-radius: 12px; border: 1px solid #333;">
                    <h1 style="color: #d4af37; font-size: 24px;">STRAXON QART</h1>
                    <p style="font-size: 18px;">Stratejik Komuta Merkezine Hoş Geldiniz.</p>
                    <hr style="border: 0; border-top: 1px solid #333; margin: 20px 0;">
                    <p>Sayın {entry.name},</p>
                    <p>STRAXON QART bekleme listesine katıldığınız için teşekkür ederiz.</p>
                    <p>Sizi sadece bir kullanıcı listesine değil; verinin, stratejinin ve teknik itibarın tek bir merkezden yönetildiği bir ekosisteme davet ediyoruz.</p>
                    <p>Süreçle ilgili kritik güncellemeleri bu adres üzerinden paylaşacağız.</p>
                    <p>Sağlıcakla kalın.</p>
                    <br>
                    <p><strong>STRAXON QART Operasyon Merkezi</strong></p>
                    <p style="font-size: 12px; opacity: 0.5;">A Product of OmNexus</p>
                </div>
            </body>
        </html>
        """
        
        resend.Emails.send({
            "from": os.getenv("FROM_EMAIL", "onboarding@resend.dev"),
            "to": entry.email,
            "subject": "STRAXON QART: Stratejik Komuta Merkezine Hoş Geldiniz.",
            "html": email_content,
        })
        
        return {"status": "success", "db_id": db_data[0].get("id") if db_data else None}
    except HTTPException as he: raise he
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

# --- GITHUB OAUTH ---

@app.get("/api/v1/straxon/auth/github")
async def github_login():
    # GitHub'a yönlendir
    return RedirectResponse(
        f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&redirect_uri={GITHUB_REDIRECT_URI}&scope=repo,user"
    )

@app.get("/api/v1/straxon/auth/github/callback")
async def github_callback(code: str):
    # GitHub'dan gelen kod ile access_token al
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            params={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": GITHUB_REDIRECT_URI
            }
        )
        token_data = token_response.json()
        
        if "access_token" not in token_data:
            raise HTTPException(status_code=400, detail="GitHub yetkilendirmesi başarısız oldu.")
        
        access_token = token_data["access_token"]
        
        user_response = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"token {access_token}"}
        )
        user_data = user_response.json()
        
        # Frontend URL'i de ortam değişkeninden alalım
        FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
        return RedirectResponse(url=f"{FRONTEND_URL}?github_connected=true&username={user_data.get('login')}")

@app.get("/api/v1/straxon/status")
async def straxon_status():
    return {"product": "STRAXON QART", "status": "Phase 1", "jarvis": "Online"}
