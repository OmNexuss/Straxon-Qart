import { NextResponse } from 'next/server';
import { createOrUpdateProfile } from '@/lib/db';

export async function POST(request) {
  try {
    const { name, email } = await request.json();

    if (!email || !name) {
      return NextResponse.json(
        { error: 'Name and email are required' },
        { status: 400 }
      );
    }

    // 1. Waitlist'e ekle ve aynı zamanda profil oluştur (+0 Zeka Puanı)
    await createOrUpdateProfile({
      email,
      full_name: name,
      score_increase: 0,
    });

    // 2. Resend API ile hoş geldiniz e-postası gönder
    const resendApiKey = process.env.RESEND_API_KEY;
    const fromEmail = process.env.FROM_EMAIL || 'onboarding@resend.dev';

    if (resendApiKey) {
      const emailContent = `
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #0a0a0c; color: #f0f0f2; padding: 40px;">
                <div style="max-width: 600px; margin: 0 auto; background: #1a1a1e; padding: 30px; border-radius: 12px; border: 1px solid #333;">
                    <h1 style="color: #d4af37; font-size: 24px;">STRAXON QART</h1>
                    <p style="font-size: 18px;">Stratejik Komuta Merkezine Hoş Geldiniz.</p>
                    <hr style="border: 0; border-top: 1px solid #333; margin: 20px 0;">
                    <p>Sayın ${name},</p>
                    <p>STRAXON QART bekleme listesine katıldığınız için teşekkür ederiz.</p>
                    <p>Jarvis şu an sizin için teknik bir profil oluşturdu. GitHub hesabınızı bağlayarak Zeka Derinliğini artırabilirsiniz.</p>
                    <br>
                    <p><strong>STRAXON QART Operasyon Merkezi</strong></p>
                </div>
            </body>
        </html>
      `;

      try {
        await fetch('https://api.resend.com/emails', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${resendApiKey}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            from: fromEmail,
            to: email,
            subject: 'STRAXON QART: Profiliniz Oluşturuldu',
            html: emailContent,
          }),
        });
      } catch (emailErr) {
        console.error('Error sending welcome email via Resend:', emailErr);
        // E-posta gönderimi başarısız olsa bile waitlist kaydını bozmamak için hata fırlatmıyoruz
      }
    }

    return NextResponse.json({ status: 'success' });
  } catch (err) {
    console.error('Waitlist join error:', err);
    return NextResponse.json(
      { error: 'Sunucu hatası', detail: err.message },
      { status: 500 }
    );
  }
}
