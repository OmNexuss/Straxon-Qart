<div align="center">
  <img src="https://raw.githubusercontent.com/OmNexuss/Straxon-Qart/master/frontend/public/logo.png" alt="Straxon Qart Logo" width="140" style="border-radius: 24px; box-shadow: 0 8px 24px rgba(0,0,0,0.15); margin-bottom: 20px;"/>
  
  <h1>🚀 Straxon Qart</h1>
  
  <p><b>Agentic AI-Powered Multi-Dimensional Developer Mentor & Heuristic Roadmap Engine</b></p>
  
  <p>
    <a href="#core-features">Özellikler</a> •
    <a href="#architecture">Mimari</a> •
    <a href="#getting-started">Kurulum</a> •
    <a href="#contributing">Katkıda Bulunma</a>
  </p>
</div>

<br/>

**Straxon Qart**, sadece bir kod analiz aracı değil; geliştiricilerin GitHub geçmişlerini derinlemesine inceleyen, onları tek bir kalıba sığdırmak yerine **hibrit geliştirici kimlikleri** ile tanımlayan (örn: *DevSecOps Specialist*, *Cloud Native AI Engineer*) ve **9 farklı bilişim disiplini** üzerinden kişiselleştirilmiş teknik öğrenme rotaları (roadmap) çıkartan yeni nesil, yapay zeka destekli proaktif bir kariyer mentorudur.

---

## ✨ Neden Straxon Qart? (Core Features)

### 🧭 1. Universal IT Matrix (9-Disiplinli Evrensel Bilişim Matrisi)

Sistemimiz, yazılım dünyasını yalnızca "Frontend" ve "Backend" olarak sınırlamaz. Modern ekosistemin tüm renklerini kapsayan 9 temel disiplinde analiz yapar:

- 🌐 **Backend & Web Systems**
- 🎨 **Frontend & UI/UX**
- ⚙️ **DevOps & SRE**
- 🤖 **AI & Machine Learning**
- 🛡️ **Cyber Security**
- 🔗 **Blockchain & Web3**
- 📟 **Embedded Systems & IoT**
- 📱 **Mobile Development**
- 🎮 **Game Development**

### 🧬 2. Dynamic Hybrid Title Synthesis

Bir yazılımcı sadece tek bir şey olmak zorunda değildir. Straxon Qart, GitHub repolarınızdaki yetenek izlerini okur ve en güçlü olduğunuz alanları birleştirerek size **Sentez Unvanlar** atar.
*Örnek:* Algoritma, hem bulut mimarisi hem de yapay zeka alanında projeler geliştirdiğinizi tespit ederse, sizi klasik bir etiket yerine **"Cloud Native AI Engineer ☁️🤖"** olarak taçlandırır.

### 🎯 3. Heuristic Milestone Engine

Eksiklerinizi bulmak hiç bu kadar akıllıca olmamıştı. Repolarınız taranır, teknoloji yığınlarınız analiz edilir ve size özel bir "Öğrenme Haritası" çıkartılır.
*Örnek:* Projelerinizde yapay zeka modelleri (AI) eğitiyor ancak veri temizleme/manipülasyon (Pandas) tarafında zayıf görünüyorsanız, sistem sizi doğrudan hedefe yönlendirir: **"Priority: Data Manipulation (Pandas/NumPy)"** ve anında ilgili eğitim kaynaklarına bağlanmanızı sağlar.

### 🍱 4. Premium Bento-Box Dashboard

Verilerinizi okumak bir zevk olmalı. Next.js kullanılarak inşa edilen panelimiz; koyu tema (dark mode), glassmorphism (buzlu cam efekti), mikro-animasyonlar ve bento-box grid yerleşimi ile donatılmıştır. Kullanıcılar, radar grafikleri, yetenek yüzdeleri ve akıllı görev kartları üzerinden kariyer gelişimlerini premium bir deneyimle takip ederler.

### 🧠 5. Intelligence Depth Algorithm (News/Articles)

Kullanıcının 1-3 aylık periyotlar içindeki okuma alışkanlıklarını analiz eden özel bir algoritma ile çalışır. Kullanıcı, en yüksek yetenek skoru elde ettiği **ilk 3 disiplindeki** en az 20 güncel sektörel haberi veya makaleyi düzenli olarak okuduğunda, Intelligence Depth (Zeka Derinliği) skoru sistem tarafından *tek seferlik* artırılır ve profiline işlenir.

### 👣 6. Digital Footprint & Competence Score

Kullanıcının tamamladığı şirket içi hedefleri (`user_tasks`) ile **GitHub** gibi harici platformlardaki aktivitelerini (Phase 1: Commit geçmişi) harmanlayarak, gerçeğe en yakın **Yetkinlik Puanını (Competence Score)** hesaplar.

---

## 🏗️ Architecture & Tech Stack (Teknoloji Yığını)

Projemiz, modern ve yüksek performanslı araçlarla inşa edilmiştir.

### 💻 Frontend (Client)

- **Next.js 14** (App Router, Server Components ile ultra hızlı SSR/SSG deneyimi)
- **React.js** (Dinamik UI bileşenleri)
- **CSS3 / Vanilla CSS** (Özel Bento-box grid tasarımları, Glassmorphism, Micro-animations)
- **Chart.js / Recharts** (Dinamik yetenek radarları ve istatistik grafikleri)

### ⚙️ Backend (Core Engine & API)

- **FastAPI** (Python 3 tabanlı, asenkron, yüksek performanslı API)
- **httpx** (Asenkron ve non-blocking GitHub API çağrıları)
- **Heuristic Core** (Veri ve iş mantığının mükemmel izolasyonunu sağlayan modüler mimari)
- **Jarvis & News Services** (AI destekli mentor bildirimleri ve sektörel haber akışları)

### 🗄️ Database & Auth

- **Supabase** (PostgreSQL altyapısı)
- **Row Level Security (RLS)**
- **Magic Link / OAuth** (Güvenli ve hızlı kimlik doğrulama)

---

## 🚀 Getting Started (Kurulum ve Çalıştırma)

Straxon Qart'ı kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları sırasıyla izleyin.

### 1. Repoyu Klonlayın

```bash
git clone https://github.com/OmNexuss/Straxon-Qart.git
cd Straxon-Qart
```

### 2. Backend'i Başlatın (FastAPI)

```bash
cd backend
python -m venv venv

# Windows için sanal ortamı aktif etme:
venv\Scripts\activate

# Mac/Linux için sanal ortamı aktif etme:
# source venv/bin/activate

# Gereksinimleri yükleyin
pip install -r requirements.txt

# Çevresel değişkenleri ayarlayın
cp .env.example .env
# .env dosyasını gerekli API anahtarları ile doldurun.

# Sunucuyu başlatın
uvicorn main:app --reload
```

*Tebrikler! Backend `http://localhost:8000` adresinde çalışıyor. API dökümantasyonuna `http://localhost:8000/docs` adresinden ulaşabilirsiniz.*

### 3. Frontend'i Başlatın (Next.js)

Yeni bir terminal penceresi açın:

```bash
cd frontend

# Bağımlılıkları yükleyin
npm install

# Çevresel değişkenleri ayarlayın
# .env.local dosyasındaki Supabase URL ve Key'leri kendi projenize göre düzenleyin.

# Geliştirme sunucusunu başlatın
npm run dev
```

*Frontend uygulamanız `http://localhost:3000` adresinde hazır.*

---

## 🧪 Testing (Testler)

Heuristik motorun, 9 farklı disiplin matrisinin tüm kombinasyonlarında doğru kararlar aldığından emin olmak için kapsamlı testlerimiz mevcuttur.

Testleri çalıştırmak için `backend` klasöründe:

```bash
# Tüm testleri çalıştırmak için
python -m unittest discover tests/

# Veya özel roadmap test scripti için:
python ../scratch/test_roadmap.py
```

---


**© 2026 <a href="https://github.com/OmNexuss"> OmNexus.</a> Tüm Hakları Saklıdır.**
