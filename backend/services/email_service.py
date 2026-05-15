import resend
from core.config import settings

resend.api_key = settings.RESEND_API_KEY

class EmailService:
    @staticmethod
    def send_waitlist_welcome(name: str, to_email: str):
        email_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #0a0a0c; color: #f0f0f2; padding: 40px;">
                <div style="max-width: 600px; margin: 0 auto; background: #1a1a1e; padding: 30px; border-radius: 12px; border: 1px solid #333;">
                    <h1 style="color: #d4af37; font-size: 24px;">STRAXON QART</h1>
                    <p style="font-size: 18px;">Stratejik Komuta Merkezine Hoş Geldiniz.</p>
                    <hr style="border: 0; border-top: 1px solid #333; margin: 20px 0;">
                    <p>Sayın {name},</p>
                    <p>STRAXON QART bekleme listesine katıldığınız için teşekkür ederiz.</p>
                    <p>Jarvis şu an sizin için teknik bir profil oluşturdu. GitHub hesabınızı bağlayarak Zeka Derinliğini artırabilirsiniz.</p>
                    <br>
                    <p><strong>STRAXON QART Operasyon Merkezi</strong></p>
                </div>
            </body>
        </html>
        """
        
        return resend.Emails.send({
            "from": settings.FROM_EMAIL,
            "to": to_email,
            "subject": "STRAXON QART: Profiliniz Oluşturuldu",
            "html": email_content,
        })

email_service = EmailService()
