from pydantic import BaseModel, EmailStr

class WaitlistEntry(BaseModel):
    name: str
    email: EmailStr

class ProfileUpdate(BaseModel):
    email: EmailStr
    full_name: str | None = None
    github_username: str | None = None
    score_increase: int = 0
