# STRAXON QART 🛡️ - Strategic Command Center

**STRAXON QART**, profesyoneller için tasarlanmış, OmNexus ekosisteminin proaktif "Stratejik Komuta Merkezi"dir. Sadece bir hedef takip aracı değil, kullanıcının dijital ayak izini analiz eden ve kariyer yolculuğunu Jarvis zekasıyla optimize eden bir platformdur.

---

## 🌌 Vizyon: Proaktif Jarvis
STRAXON QART'ın kalbinde yatan Jarvis, kullanıcının teknik gelişimini (GitHub, StackOverflow vb.) ve kariyer platformlarındaki (LinkedIn, Upwork) varlığını analiz ederek şu yetenekleri sunar:

- **Zeka Derinliği (Intelligence Depth):** Kullanıcının dijital dünyadaki verilerine dayanarak oluşturulan %0-100 arası dinamik gelişim metriği.
- **Mentorluk Modülü:** roadmap.sh verileriyle entegre, kişiselleştirilmiş teknik kariyer rotaları.
- **Stratejik Haber Merkezi:** Kullanıcının Q1-Q4 hedefleriyle ilgili dünyadaki teknolojik gelişmeleri süzüp sunan proaktif analiz motoru.

---

## 🛠️ Teknoloji Yığını

### Frontend (Modern & Responsive)
- **Next.js 14+**: App Router mimarisi.
- **Premium UI**: Vanilla CSS ile oluşturulmuş Dark Mode, Glassmorphism ve Bento-Grid tasarımı.
- **PWA Ready**: Mobil öncelikli stratejik yönetim deneyimi.

### Backend (Modüler & Ölçeklenebilir)
- **FastAPI (Python)**: Yüksek performanslı asenkron API.
- **Modüler Mimari**: `core/`, `routers/`, `models/` ve `services/` ayrımıyla temiz kod yapısı.
- **Supabase**: PostgreSQL veritabanı ve güvenli kimlik doğrulama.
- **Resend**: Proaktif e-posta bilgilendirme sistemi.
- **GitHub OAuth**: Tek tıkla teknik profil entegrasyonu.

---

## 📁 Proje Yapısı

```text
backend/
├── core/           # Yapılandırma ve veritabanı bağlantıları
├── models/         # Pydantic veri şemaları
├── routers/        # API uç noktaları (Auth, Profiles, Status)
├── services/       # İş mantığı ve dış servisler (Email, Scrapers)
└── main.py         # Uygulama giriş noktası

frontend/
├── src/app/        # Next.js App Router sayfaları
├── src/components/ # Yeniden kullanılabilir UI bileşenleri
└── public/         # Logo ve statik varlıklar
```

---

## 🚀 Hızlı Başlangıç

### 1. Depoyu Klonlayın
```bash
git clone https://github.com/OmNexuss/Straxon-Qart.git
cd Straxon-Qart
```

### 2. Backend Kurulumu
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
# .env.example dosyasını .env yaparak doldurun
python main.py
```

### 3. Frontend Kurulumu
```bash
cd ../frontend
npm install
npm run dev
```

---

## 🛡️ Güvenlik ve Katkıda Bulunma
Bu proje [OmNexus](https://github.com/OmNexuss) bünyesinde geliştirilmektedir. Güvenlik nedeniyle API anahtarlarınızı `.env` dosyalarında saklayın ve asla commit etmeyin.

**© 2026 OmNexus Global Ecosystem. Tüm hakları saklıdır.**
