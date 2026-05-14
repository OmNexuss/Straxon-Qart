# STRAXON QART 🛡️

**STRAXON QART**, OmNexus ekosisteminin stratejik komuta merkezidir. Modern bir arayüz, güçlü bir backend ve gelişmiş iletişim araçlarıyla donatılmış, profesyonel bir yönetim ve strateji platformudur.

## 🚀 Özellikler

- **Vakur Tasarım**: Ciddi, premium ve kullanıcı odaklı karanlık mod arayüzü.
- **Stratejik Yönetim**: Proje ve iş süreçlerini takip etmek için optimize edilmiş araçlar.
- **AI Destekli Altyapı**: Gelecekteki "Jarvis" entegrasyonu için hazır mimari.
- **Proaktif İletişim**: Resend entegrasyonu ile otomatik ve güvenli bilgilendirme.

## 🛠️ Teknoloji Yığını

### Frontend
- **Framework**: [Next.js](https://nextjs.org/) (App Router)
- **Styling**: Vanilla CSS (Modern & Responsive)
- **State Management**: Zustand / React Context

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Database**: [Supabase](https://supabase.com/) (PostgreSQL)
- **Email Service**: [Resend](https://resend.com/)
- **Authentication**: GitHub OAuth / Supabase Auth

## 📦 Kurulum

### Gereksinimler
- Node.js (v18+)
- Python (v3.9+)
- Git

### 1. Depoyu Klonlayın
```bash
git clone https://github.com/OmNexuss/Straxon-Qart.git
cd Straxon-Qart
```

### 2. Backend Kurulumu
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows için: venv\Scripts\activate
pip install -r requirements.txt
# .env.example dosyasını .env olarak kopyalayın ve bilgileri doldurun
cp .env.example .env
python main.py
```

### 3. Frontend Kurulumu
```bash
cd ../frontend
npm install
# .env dosyasını oluşturun ve Supabase bilgilerini girin
npm run dev
```

## 🔒 Güvenlik Notu
Bu projedeki hassas bilgiler (`.env` dosyaları) `.gitignore` ile korunmaktadır. Kendi kurulumunuzda gerekli API anahtarlarını temin etmeniz gerekmektedir.

## 📄 Lisans
Bu proje [OmNexus](https://github.com/OmNexuss) bünyesinde geliştirilmiştir. Tüm hakları saklıdır.
