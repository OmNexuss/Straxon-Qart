import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

class Settings:
    PROJECT_NAME: str = "OmNexus Core API"
    VERSION: str = "1.0.0"
    ROOT_PATH: str = os.getenv("ROOT_PATH", "")
    
    # API Keys & URLs
    RESEND_API_KEY: str = os.getenv("RESEND_API_KEY")
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")
    
    # GitHub OAuth
    GITHUB_CLIENT_ID: str = os.getenv("GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET: str = os.getenv("GITHUB_CLIENT_SECRET")
    
    # URLs
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8000")
    GITHUB_REDIRECT_URI: str = os.getenv("GITHUB_REDIRECT_URI", f"{BASE_URL}/api/v1/straxon/auth/github/callback")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # Email
    FROM_EMAIL: str = os.getenv("FROM_EMAIL", "onboarding@resend.dev")

settings = Settings()
