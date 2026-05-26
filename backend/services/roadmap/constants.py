import httpx
from typing import Dict, List, Any

# ─────────────────────────────────────────────────────────────────────────────
# 9-DİSİPLİNLİ EVRENSEL BİLİŞİM MATRİSİ
# Her disiplin: dil ağırlıkları, imza kelimeleri ve hücresel kilometre taşları
# ─────────────────────────────────────────────────────────────────────────────

DISCIPLINES = {

    # ──────────────────────────────────────────────────────────────
    # 1. BACKEND & WEB SYSTEMS
    # ──────────────────────────────────────────────────────────────
    "Backend Engineer": {
        "url": "https://roadmap.sh/backend",
        "emoji": "⚙️",
        "color": "#00d4ff",
        "lang_weights": {
            "Go": 0.9, "Python": 0.85, "Ruby": 0.8, "Java": 0.8,
            "C++": 0.7, "C#": 0.75, "PHP": 0.65,
            "JavaScript": 0.5, "TypeScript": 0.55, "Rust": 0.85
        },
        "repo_signatures": [
            "api", "backend", "server", "rest", "graphql", "grpc",
            "fastapi", "django", "flask", "spring", "express",
            "microservice", "endpoint", "controller", "route"
        ],
        "milestones": [
            {
                "title": "APIs & REST Basics",
                "anchor_url": "https://roadmap.sh/backend#apis",
                "signatures": ["api", "rest", "fastapi", "graphql", "grpc", "endpoint", "controller", "route"],
                "why_needed": "Backend mimarisinin temeli olan HTTP ve REST API tasarımlarını derinlemesine kavramanız gerekmektedir.",
                "action_steps": [
                    "HTTP metodlarını (GET, POST, PUT, DELETE) ve durum kodlarını öğrenin",
                    "FastAPI veya Express ile basit bir CRUD API geliştirin",
                    "Postman veya Swagger ile API uç noktalarınızı belgeleyin"
                ]
            },
            {
                "title": "Relational & NoSQL Databases",
                "anchor_url": "https://roadmap.sh/backend#relational-databases",
                "signatures": ["sql", "postgres", "mysql", "mongo", "db", "sqlite", "orm", "prisma", "sequelize", "sqlalchemy", "redis", "nosql"],
                "why_needed": "Veri kalıcılığını sağlamak için veritabanlarını ve ORM kavramlarını projelerinize entegre etmelisiniz.",
                "action_steps": [
                    "PostgreSQL ile temel SQL sorgularını (SELECT, INSERT, JOIN) öğrenin",
                    "SQLAlchemy veya Prisma ile ORM kullanımını deneyin",
                    "Veritabanı indeksleme ve ilişkisel veri modelleme mantığını kavrayın"
                ]
            },
            {
                "title": "Testing & QA Principles",
                "anchor_url": "https://roadmap.sh/backend#testing",
                "signatures": ["test", "pytest", "jest", "mocha", "cypress", "unittest", "spec", "assert"],
                "why_needed": "Profesyonel backend dünyasında kod kalitesini korumak için otomatik test yazımı şarttır.",
                "action_steps": [
                    "PyTest veya Go Testing paketiyle birim testleri yazın",
                    "Harici servisleri taklit etmek için Mocking kavramını öğrenin",
                    "Code coverage aracı ile test kapsama oranınızı ölçün"
                ]
            },
            {
                "title": "Docker & Containers",
                "anchor_url": "https://roadmap.sh/backend#containers",
                "signatures": ["docker", "container", "dockerfile", "kubernetes", "k8s", "compose"],
                "why_needed": "Uygulamalarınızı izole etmek ve ölçeklemek için Docker konteynerizasyon teknolojisini öğrenmelisiniz.",
                "action_steps": [
                    "Temel Docker CLI komutlarını öğrenin (run, build, ps)",
                    "Uygulamanız için optimize çok katmanlı (multi-stage) bir Dockerfile yazın",
                    "Docker Compose ile servislerinizi tek komutla ayağa kaldırın"
                ]
            },
            {
                "title": "CI/CD & Automation",
                "anchor_url": "https://roadmap.sh/backend#ci-cd",
                "signatures": ["github-actions", "jenkins", "ci", "cd", "pipeline", "workflow", "travis"],
                "why_needed": "Sürekli entegrasyon ve dağıtım otomasyonu ile güvenilir yazılım teslimat süreçleri kurmalısınız.",
                "action_steps": [
                    "GitHub Actions ile her push'ta testleri çalıştıran workflow oluşturun",
                    "Docker imajınızı otomatik build edip registry'e push edin",
                    "Lint ve kod kalitesi kontrol adımlarını pipeline'a ekleyin"
                ]
            },
            {
                "title": "Cloud & Scalability",
                "anchor_url": "https://roadmap.sh/backend#designing-for-scale",
                "signatures": ["aws", "gcp", "azure", "cloud", "s3", "ec2", "terraform", "lambda", "ecs"],
                "why_needed": "Uygulamalarınızı buluta taşımak ve ölçeklemek için AWS, GCP veya Azure araçlarını öğrenmelisiniz.",
                "action_steps": [
                    "AWS EC2 veya ECS üzerinde bir uygulamanızı canlıya alın",
                    "Serverless mimari için AWS Lambda işlevlerini inceleyin",
                    "Terraform ile kodla altyapı yönetimini (IaC) keşfedin"
                ]
            }
        ]
    },

    # ──────────────────────────────────────────────────────────────
    # 2. FRONTEND & UI/UX
    # ──────────────────────────────────────────────────────────────
    "Frontend Engineer": {
        "url": "https://roadmap.sh/frontend",
        "emoji": "🎨",
        "color": "#ff6b9d",
        "lang_weights": {
            "TypeScript": 0.95, "JavaScript": 0.9, "HTML": 0.8, "CSS": 0.8,
            "Vue": 0.7, "Svelte": 0.65
        },
        "repo_signatures": [
            "frontend", "ui", "ux", "react", "vue", "angular", "nextjs",
            "svelte", "nuxt", "gatsby", "tailwind", "sass", "css", "design"
        ],
        "milestones": [
            {
                "title": "HTML & CSS Fundamentals",
                "anchor_url": "https://roadmap.sh/frontend#html",
                "signatures": ["html", "css", "layout", "flexbox", "grid", "responsive", "semantic"],
                "why_needed": "Web geliştirmenin temeli olan HTML ve CSS'i iyi kavramak, her seviyede kaliteli arayüzler oluşturmanızı sağlar.",
                "action_steps": [
                    "Semantik HTML etiketlerini ve erişilebilirlik kurallarını öğrenin",
                    "CSS Flexbox ve Grid ile responsive layout oluşturun",
                    "Mobil öncelikli (mobile-first) tasarım prensiplerini uygulayın"
                ]
            },
            {
                "title": "JavaScript & TypeScript Core",
                "anchor_url": "https://roadmap.sh/frontend#javascript",
                "signatures": ["js", "typescript", "es6", "async", "promise", "dom", "event"],
                "why_needed": "Modern web uygulamaları için JavaScript'in async yapısını, DOM manipülasyonunu ve TypeScript'i kavramanız şarttır.",
                "action_steps": [
                    "ES6+ sözdizimini (arrow functions, destructuring, spread) öğrenin",
                    "Promise ve async/await ile asenkron veri çekmeyi deneyin",
                    "TypeScript ile tip güvenli kod yazmaya başlayın"
                ]
            },
            {
                "title": "Modern Frameworks (React/Next.js)",
                "anchor_url": "https://roadmap.sh/frontend#pick-a-framework",
                "signatures": ["react", "vue", "angular", "nextjs", "svelte", "nuxt", "gatsby"],
                "why_needed": "Büyük ölçekli ve sürdürülebilir web uygulamaları geliştirmek için React veya Next.js gibi modern bir framework şarttır.",
                "action_steps": [
                    "React state, props ve hooks (useState, useEffect) kavramlarını oturtun",
                    "Next.js App Router ve Server Components mimarisini öğrenin",
                    "Reusable component ve custom hooks yazarak kod tekrarını azaltın"
                ]
            },
            {
                "title": "CSS Frameworks & Design Systems",
                "anchor_url": "https://roadmap.sh/frontend#css-frameworks",
                "signatures": ["tailwind", "bootstrap", "material", "chakra", "styled-components", "storybook"],
                "why_needed": "Hızlı, tutarlı ve premium arayüzler üretmek için Tailwind CSS gibi modern bir framework ve design system kullanmalısınız.",
                "action_steps": [
                    "Tailwind CSS utility sınıflarını ve tema konfigürasyonunu öğrenin",
                    "Storybook ile component library oluşturmayı deneyin",
                    "Dark mode ve özel renk paletleri tasarlayın"
                ]
            },
            {
                "title": "Build Tools & Performance",
                "anchor_url": "https://roadmap.sh/frontend#build-tools",
                "signatures": ["webpack", "vite", "rollup", "esbuild", "bundler", "lazy", "performance", "lighthouse"],
                "why_needed": "Uygulamanızın hızını ve kullanıcı deneyimini optimize etmek için build araçlarını ve performans metriklerini kavramanız gerekir.",
                "action_steps": [
                    "Vite veya Webpack ile proje bundling ve code splitting öğrenin",
                    "Lighthouse ile Core Web Vitals metriklerinizi ölçün",
                    "Lazy loading ve image optimization tekniklerini uygulayın"
                ]
            }
        ]
    },

    # ──────────────────────────────────────────────────────────────
    # 3. DEVOPS & SRE
    # ──────────────────────────────────────────────────────────────
    "DevOps Engineer": {
        "url": "https://roadmap.sh/devops",
        "emoji": "☁️",
        "color": "#00ff88",
        "lang_weights": {
            "Go": 0.9, "Shell": 0.85, "HCL": 0.95, "Python": 0.7,
            "Bash": 0.85, "Ruby": 0.4
        },
        "repo_signatures": [
            "devops", "infrastructure", "terraform", "kubernetes", "k8s",
            "ansible", "jenkins", "ci-cd", "pipeline", "monitoring", "sre"
        ],
        "milestones": [
            {
                "title": "Linux & Shell Scripting",
                "anchor_url": "https://roadmap.sh/devops#operating-systems",
                "signatures": ["bash", "shell", "linux", "ubuntu", "script", "sh", "posix"],
                "why_needed": "Sistem yönetimi ve otomasyon için Linux işletim sistemini ve Shell betiklerini kavramanız şarttır.",
                "action_steps": [
                    "Temel Linux CLI komutlarını ve dosya izinlerini öğrenin",
                    "Tekrarlayan görevleri otomatikleştiren bir Bash betiği yazın",
                    "Cron job ile zamanlanmış görevleri deneyin"
                ]
            },
            {
                "title": "Containers & Orchestration",
                "anchor_url": "https://roadmap.sh/devops#containers",
                "signatures": ["docker", "container", "kubernetes", "k8s", "helm", "compose", "pod"],
                "why_needed": "Uygulamalarınızı konteynerize etmek ve yüksek erişilebilirlikte çalıştırmak için Kubernetes ve Docker'ı öğrenmelisiniz.",
                "action_steps": [
                    "Docker ve Docker Compose'u üretim benzeri bir senaryo için yapılandırın",
                    "Kubernetes'te Deployment ve Service kaynaklarını tanımlayın",
                    "Helm chart ile servis dağıtımını paketleyin"
                ]
            },
            {
                "title": "Infrastructure as Code",
                "anchor_url": "https://roadmap.sh/devops#infrastructure-as-code",
                "signatures": ["terraform", "ansible", "pulumi", "chef", "puppet", "vagrant", "tf"],
                "why_needed": "Altyapıyı tutarlı ve tekrarlanabilir şekilde yönetmek için IaC araçlarını (Terraform, Ansible) kullanmalısınız.",
                "action_steps": [
                    "Terraform HCL ile temel bir cloud kaynağı (EC2, VPC) tanımlayın",
                    "Ansible playbook ile sunucu konfigürasyon yönetimini öğrenin",
                    "Terraform state ve remote backend kavramlarını kavrayın"
                ]
            },
            {
                "title": "Monitoring & Observability",
                "anchor_url": "https://roadmap.sh/devops#monitoring",
                "signatures": ["prometheus", "grafana", "elastic", "kibana", "datadog", "monitoring", "alert", "log", "trace"],
                "why_needed": "Sistemlerin sağlığını ve performansını izlemek için Prometheus/Grafana veya ELK Stack gibi araçları kurmalısınız.",
                "action_steps": [
                    "Prometheus ile uygulama metriklerini toplayın ve Grafana'da görselleştirin",
                    "Structured logging ile uygulama loglarını merkezi bir sistemde toplayın",
                    "Alertmanager ile kritik anomaliler için bildirim kuralları oluşturun"
                ]
            }
        ]
    },

    # ──────────────────────────────────────────────────────────────
    # 4. MOBILE DEVELOPMENT
    # ──────────────────────────────────────────────────────────────
    "Mobile Developer": {
        "url": "https://roadmap.sh/android",
        "emoji": "📱",
        "color": "#a78bfa",
        "lang_weights": {
            "Kotlin": 0.95, "Swift": 0.95, "Dart": 0.90,
            "Java": 0.7, "Objective-C": 0.65
        },
        "repo_signatures": [
            "android", "ios", "mobile", "flutter", "react-native", "app",
            "swiftui", "compose", "jetpack", "xcode"
        ],
        "milestones": [
            {
                "title": "Core Language & UI Fundamentals",
                "anchor_url": "https://roadmap.sh/android#kotlin",
                "signatures": ["kotlin", "swift", "dart", "compose", "swiftui", "jetpack", "flutter"],
                "why_needed": "Mobil uygulama geliştirme için Kotlin/Swift dilinin temellerini ve modern deklaratif UI tasarımını kavramanız gerekir.",
                "action_steps": [
                    "Kotlin veya Swift dilinin OOP ve fonksiyonel özelliklerini öğrenin",
                    "Jetpack Compose veya SwiftUI ile responsive ekranlar tasarlayın",
                    "Flutter kullanıyorsanız widget ağacı ve state yönetimini kavrayın"
                ]
            },
            {
                "title": "State Management & Navigation",
                "anchor_url": "https://roadmap.sh/android#state-management",
                "signatures": ["viewmodel", "redux", "bloc", "provider", "riverpod", "navigation", "route", "nav"],
                "why_needed": "Karmaşık mobil uygulamalarda state yönetimi ve ekranlar arası navigasyonu doğru mimariyle kurmanız şarttır.",
                "action_steps": [
                    "ViewModel ve LiveData/StateFlow kullanarak reactive UI mimarisi kurun",
                    "Flutter'da BLoC veya Riverpod ile state yönetimini deneyin",
                    "Bottom Tab Navigation ve Deep Link yapılandırın"
                ]
            },
            {
                "title": "Networking & Local Storage",
                "anchor_url": "https://roadmap.sh/android#networking",
                "signatures": ["retrofit", "volley", "http", "sqlite", "room", "realm", "shared-preferences", "hive", "objectbox"],
                "why_needed": "API entegrasyonu ve yerel veri saklama için ağ kütüphaneleri ve yerel veritabanı çözümlerini uygulamanıza entegre etmelisiniz.",
                "action_steps": [
                    "Retrofit/Dio ile REST API çağrıları yapın ve JSON parse edin",
                    "Room Database veya Hive ile çevrimdışı veri saklama kurun",
                    "Network hata senaryolarını (timeout, retry) yönetin"
                ]
            },
            {
                "title": "App Store Deployment",
                "anchor_url": "https://roadmap.sh/android#release",
                "signatures": ["release", "publish", "fastlane", "signing", "certificate", "apk", "ipa", "store"],
                "why_needed": "Uygulamanızı Google Play veya App Store'a yayınlamak için imzalama, sürüm yönetimi ve dağıtım araçlarını öğrenmelisiniz.",
                "action_steps": [
                    "Keystore ile APK imzalama ve App Bundle oluşturma adımlarını öğrenin",
                    "Fastlane ile derleme ve yayınlama süreçlerini otomatikleştirin",
                    "Beta test için Firebase App Distribution veya TestFlight'ı kullanın"
                ]
            }
        ]
    },

    # ──────────────────────────────────────────────────────────────
    # 5. GAME DEVELOPMENT
    # ──────────────────────────────────────────────────────────────
    "Game Developer": {
        "url": "https://roadmap.sh/game-developer",
        "emoji": "🎮",
        "color": "#f59e0b",
        "lang_weights": {
            "C#": 0.95, "C++": 0.95, "GDScript": 0.98, "Lua": 0.90,
            "Python": 0.35, "JavaScript": 0.3
        },
        "repo_signatures": [
            "game", "unity", "unreal", "godot", "engine", "level",
            "sprite", "shader", "opengl", "webgl", "player", "scene"
        ],
        "milestones": [
            {
                "title": "Math & Physics for Games",
                "anchor_url": "https://roadmap.sh/game-developer#mathematics-physics",
                "signatures": ["math", "vector", "physics", "matrix", "trigonometry", "geometry", "collision"],
                "why_needed": "Oyun geliştirmenin temeli olan doğrusal cebir, vektör matematiği ve fizik motorlarını kavramanız gerekmektedir.",
                "action_steps": [
                    "Vektör matematiğini (dot/cross product) ve 2D/3D koordinat sistemlerini öğrenin",
                    "Çarpışma (collision) algılama ve fizik simülasyonunu kodlayın",
                    "Temel lineer cebir ve quaternion rotasyonlarını inceleyin"
                ]
            },
            {
                "title": "Game Engine Integration",
                "anchor_url": "https://roadmap.sh/game-developer#game-engines",
                "signatures": ["unity", "unreal", "godot", "prefab", "scene", "blueprint", "mono", "gdscript"],
                "why_needed": "Modern oyun geliştirme süreçleri Unity, Unreal veya Godot gibi motorlar üzerinde yürütülür; bu ortamları iyi kavramanız şarttır.",
                "action_steps": [
                    "Unity, Unreal veya Godot arasından bir motor seçin ve temel arayüzünü öğrenin",
                    "Basit bir 2D sahne oluşturup karakter hareketi scripti ekleyin",
                    "Prefab/Scene yapısı ve component mimarisini kavrayın"
                ]
            },
            {
                "title": "Game Design Patterns",
                "anchor_url": "https://roadmap.sh/game-developer#design-patterns",
                "signatures": ["pattern", "singleton", "state-machine", "object-pool", "pooling", "observer", "ecs"],
                "why_needed": "Performanslı ve temiz oyun kodu için Object Pooling, State Machine ve Entity Component System (ECS) kalıplarını öğrenmelisiniz.",
                "action_steps": [
                    "Mermi/efekt objeleri için Object Pooling uygulayın",
                    "Karakter durumlarını (koşma, zıplama, ölme) State Machine ile yönetin",
                    "ECS mimarisiyle veri odaklı oyun mantığını inceleyin"
                ]
            },
            {
                "title": "Graphics & Shaders",
                "anchor_url": "https://roadmap.sh/game-developer#graphics-programming",
                "signatures": ["shader", "opengl", "webgl", "directx", "vulkan", "hlsl", "glsl", "render", "three"],
                "why_needed": "Görsel kaliteyi artırmak için gölgelendirici (shader) yazımı ve grafik API'lerini kavramanız gerekmektedir.",
                "action_steps": [
                    "GLSL veya HLSL ile temel bir vertex/fragment shader yazın",
                    "Render pipeline aşamalarını (vertex, rasterization, fragment) öğrenin",
                    "Three.js veya OpenGL ile 3D bir sahne oluşturun"
                ]
            }
        ]
    },

    # ──────────────────────────────────────────────────────────────
    # 6. AI & MACHINE LEARNING
    # ──────────────────────────────────────────────────────────────
    "AI & ML Engineer": {
        "url": "https://roadmap.sh/ai-data-scientist",
        "emoji": "🧠",
        "color": "#c084fc",
        "lang_weights": {
            "Python": 0.95, "R": 0.95, "Julia": 0.75, "MATLAB": 0.70,
            "Scala": 0.65, "SQL": 0.5
        },
        "repo_signatures": [
            "ml", "machine-learning", "ai", "artificial-intelligence",
            "deep-learning", "neural", "nlp", "computer-vision",
            "tensorflow", "pytorch", "keras", "llm", "transformer", "model"
        ],
        "milestones": [
            {
                "title": "Math & Statistics Foundations",
                "anchor_url": "https://roadmap.sh/ai-data-scientist#mathematics",
                "signatures": ["math", "statistics", "probability", "linear-algebra", "calculus", "matrix", "regression", "stats"],
                "why_needed": "Makine öğrenmesi algoritmalarının temelini oluşturan matematik ve istatistik kavramlarını sağlam öğrenmeden model geliştirmek imkânsızdır.",
                "action_steps": [
                    "Lineer cebir (matris çarpımı, eigenvalue) kavramlarını öğrenin",
                    "Temel istatistik (dağılım, hipotez testi, korelasyon) konularını gözden geçirin",
                    "Gradient descent optimizasyon algoritmasını elle hesaplayın"
                ]
            },
            {
                "title": "Data Manipulation (Pandas/NumPy)",
                "anchor_url": "https://roadmap.sh/ai-data-scientist#data-wrangling",
                "signatures": ["pandas", "numpy", "dataframe", "dplyr", "tidyr", "data-cleaning", "etl", "csv", "dataset"],
                "why_needed": "Model eğitmeden önce veriyi temizlemek, dönüştürmek ve analiz etmek için Pandas ve NumPy kütüphanelerini etkin kullanmanız şarttır.",
                "action_steps": [
                    "Pandas DataFrame ile veri filtreleme, gruplama ve pivot işlemleri yapın",
                    "Eksik veri (NaN) yönetimi ve özellik mühendisliği tekniklerini öğrenin",
                    "NumPy ile matris işlemleri ve vektörleştirilmiş hesaplamalar gerçekleştirin"
                ]
            },
            {
                "title": "Data Visualization",
                "anchor_url": "https://roadmap.sh/ai-data-scientist#data-visualization",
                "signatures": ["matplotlib", "seaborn", "plotly", "tableau", "powerbi", "chart", "plot", "visualization", "dashboard"],
                "why_needed": "Verideki kalıpları keşfetmek ve bulguları aktarmak için etkili veri görselleştirme becerilerini geliştirmelisiniz.",
                "action_steps": [
                    "Matplotlib ve Seaborn ile histogram, scatter plot ve heatmap oluşturun",
                    "Plotly ile interaktif dashboard geliştirmeyi deneyin",
                    "Veri hikayeciliği (data storytelling) ilkelerini öğrenin"
                ]
            },
            {
                "title": "Machine Learning Algorithms",
                "anchor_url": "https://roadmap.sh/ai-data-scientist#machine-learning",
                "signatures": ["scikit-learn", "sklearn", "regression", "classification", "clustering", "svm", "xgboost", "random-forest"],
                "why_needed": "Gerçek problemleri çözmek için temel ML algoritmalarını (regresyon, sınıflandırma, kümeleme) kodlayıp değerlendirmeyi öğrenmelisiniz.",
                "action_steps": [
                    "Scikit-learn ile Linear Regression ve Random Forest modellerini eğitin",
                    "Cross-validation ve hiperparametre optimizasyonunu uygulayın",
                    "Model değerlendirme metriklerini (F1, AUC-ROC, RMSE) kavrayın"
                ]
            },
            {
                "title": "Deep Learning & Neural Networks",
                "anchor_url": "https://roadmap.sh/ai-data-scientist#deep-learning",
                "signatures": ["tensorflow", "pytorch", "keras", "neural", "cnn", "rnn", "transformer", "attention", "bert", "llm"],
                "why_needed": "Görüntü tanıma, NLP ve üretken AI gibi ileri seviye problemler için derin öğrenme mimarilerini kavramanız gerekmektedir.",
                "action_steps": [
                    "PyTorch ile basit bir yapay sinir ağı sıfırdan kodlayın",
                    "CNN ile görüntü sınıflandırması ve Transfer Learning uygulayın",
                    "Transformer mimarisini ve Attention mekanizmasını inceleyin"
                ]
            }
        ]
    },

    # ──────────────────────────────────────────────────────────────
    # 7. CYBER SECURITY
    # ──────────────────────────────────────────────────────────────
    "Cyber Security Specialist": {
        "url": "https://roadmap.sh/cyber-security",
        "emoji": "🛡️",
        "color": "#ef4444",
        "lang_weights": {
            "Python": 0.85, "C": 0.90, "C++": 0.85, "Assembly": 0.95,
            "Shell": 0.80, "Bash": 0.80, "Ruby": 0.5, "Go": 0.5
        },
        "repo_signatures": [
            "security", "cyber", "exploit", "malware", "penetration",
            "hacking", "reverse", "cryptography", "ctf", "pentest",
            "vulnerability", "forensics", "osint", "red-team", "blue-team"
        ],
        "milestones": [
            {
                "title": "Networking & Protocols",
                "anchor_url": "https://roadmap.sh/cyber-security#networking-knowledge",
                "signatures": ["network", "tcp", "udp", "http", "dns", "wireshark", "packet", "protocol", "firewall", "vpn"],
                "why_needed": "Siber güvenliğin temeli ağ protokollerini derinlemesine kavramaktır; güvenlik açıklarının büyük çoğunluğu ağ katmanında gizlidir.",
                "action_steps": [
                    "TCP/IP, UDP, DNS ve HTTP/HTTPS protokollerini inceleyin",
                    "Wireshark ile gerçek ağ trafiğini analiz edin",
                    "OSI ve TCP/IP modellerindeki her katmanın rolünü kavrayın"
                ]
            },
            {
                "title": "Linux & System Internals",
                "anchor_url": "https://roadmap.sh/cyber-security#os-knowledge",
                "signatures": ["linux", "bash", "kernel", "process", "privilege", "chmod", "sudo", "syscall"],
                "why_needed": "Güvenlik testleri ve exploit geliştirme için Linux işletim sistemi ve sistem programlama kavramlarını derinlemesine bilmelisiniz.",
                "action_steps": [
                    "Linux dosya izinleri, process yönetimi ve cron'u öğrenin",
                    "setuid, capabilities ve privilege escalation kavramlarını kavrayın",
                    "Sistem çağrıları (syscall) ve kernel-user space ayrımını inceleyin"
                ]
            },
            {
                "title": "Penetration Testing",
                "anchor_url": "https://roadmap.sh/cyber-security#penetration-testing",
                "signatures": ["pentest", "nmap", "metasploit", "burp", "sqlmap", "kali", "exploit", "payload", "ctf"],
                "why_needed": "Sistemlerdeki güvenlik açıklarını tespit edip raporlamak için sızma testi metodolojisini ve araçlarını öğrenmelisiniz.",
                "action_steps": [
                    "Nmap ile port tarama ve servis keşif tekniklerini öğrenin",
                    "Metasploit Framework kullanarak kontrollü bir ortamda exploit deneyin",
                    "HackTheBox veya TryHackMe üzerinde pratik CTF çözün"
                ]
            },
            {
                "title": "Cryptography & PKI",
                "anchor_url": "https://roadmap.sh/cyber-security#cryptography",
                "signatures": ["crypto", "cryptography", "encryption", "aes", "rsa", "hash", "sha", "tls", "ssl", "certificate", "pki"],
                "why_needed": "Güvenli iletişim ve veri koruma için kriptografi prensiplerini ve PKI altyapısını kavramanız gerekmektedir.",
                "action_steps": [
                    "Simetrik (AES) ve asimetrik (RSA) şifreleme yöntemlerini karşılaştırın",
                    "Hash fonksiyonlarını (SHA-256) ve HMAC'ı öğrenin",
                    "TLS/SSL sertifika zincirini ve PKI altyapısını inceleyin"
                ]
            },
            {
                "title": "Reverse Engineering",
                "anchor_url": "https://roadmap.sh/cyber-security#reverse-engineering",
                "signatures": ["reverse", "disassembly", "ghidra", "ida", "binary", "asm", "assembly", "malware-analysis", "decompile"],
                "why_needed": "Zararlı yazılımları analiz etmek ve güvenlik araştırması yapmak için tersine mühendislik becerilerini geliştirmelisiniz.",
                "action_steps": [
                    "Ghidra veya IDA Free ile bir binary dosyayı disassemble edin",
                    "Assembly dilinin temel komutlarını (mov, push, jmp) öğrenin",
                    "Basit bir malware örneğini sandbox ortamında analiz edin"
                ]
            }
        ]
    },

    # ──────────────────────────────────────────────────────────────
    # 8. BLOCKCHAIN & WEB3
    # ──────────────────────────────────────────────────────────────
    "Blockchain & Web3 Developer": {
        "url": "https://roadmap.sh/blockchain",
        "emoji": "⛓️",
        "color": "#fb923c",
        "lang_weights": {
            "Solidity": 0.98, "Rust": 0.90, "Go": 0.70,
            "TypeScript": 0.65, "JavaScript": 0.6, "Python": 0.5
        },
        "repo_signatures": [
            "blockchain", "web3", "solidity", "smart-contract", "ethereum",
            "solana", "dapp", "nft", "token", "defi", "dao", "crypto", "wallet"
        ],
        "milestones": [
            {
                "title": "Blockchain Fundamentals",
                "anchor_url": "https://roadmap.sh/blockchain#blockchain-basics",
                "signatures": ["blockchain", "block", "chain", "consensus", "hash", "merkle", "ledger", "distributed"],
                "why_needed": "Blok zinciri teknolojisinin temel prensiplerini (consensus, immutability, P2P ağlar) kavramadan üzerine uygulama geliştirmek mümkün değildir.",
                "action_steps": [
                    "Proof of Work ve Proof of Stake consensus mekanizmalarını öğrenin",
                    "Merkle Tree ve kriptografik hash fonksiyonlarını kavrayın",
                    "Bir blok zincirini sıfırdan Python ile simüle edin"
                ]
            },
            {
                "title": "Solidity & Smart Contracts",
                "anchor_url": "https://roadmap.sh/blockchain#smart-contracts",
                "signatures": ["solidity", "smart-contract", "contract", "pragma", "evm", "abi", "deploy", "hardhat", "truffle"],
                "why_needed": "Ethereum ve uyumlu ağlarda merkezi olmayan uygulamalar geliştirmek için Solidity ile akıllı sözleşme yazmayı öğrenmelisiniz.",
                "action_steps": [
                    "Solidity ile temel bir ERC-20 token akıllı sözleşmesi yazın",
                    "Hardhat ile akıllı sözleşmeleri test edin ve testnet'e deploy edin",
                    "Solidity güvenlik açıklarını (reentrancy, overflow) inceleyin"
                ]
            },
            {
                "title": "dApp Development",
                "anchor_url": "https://roadmap.sh/blockchain#dapps",
                "signatures": ["dapp", "ethers", "web3js", "metamask", "wagmi", "viem", "frontend-web3", "react-web3"],
                "why_needed": "Akıllı sözleşmeleri kullanıcıya açmak için Web3 kütüphanelerini ve cüzdan entegrasyonlarını içeren dApp geliştirmeli, tanımalısınız.",
                "action_steps": [
                    "Ethers.js veya Wagmi ile MetaMask bağlantısı kurun",
                    "React frontend ile akıllı sözleşme fonksiyonlarını çağırın",
                    "IPFS veya Arweave ile merkezi olmayan dosya depolama deneyin"
                ]
            },
            {
                "title": "DeFi & Protocol Design",
                "anchor_url": "https://roadmap.sh/blockchain#defi",
                "signatures": ["defi", "amm", "liquidity", "pool", "swap", "yield", "vault", "protocol", "uniswap", "aave"],
                "why_needed": "Merkeziyetsiz finans (DeFi) protokollerini anlamak ve tasarlamak için AMM, likidite havuzları ve tokenomics kavramlarını kavramanız gerekmektedir.",
                "action_steps": [
                    "Uniswap AMM mekanizmasını ve x*y=k formülünü inceleyin",
                    "Basit bir DeFi vault sözleşmesi yazın",
                    "Flash loan mekanizmasını ve kullanım senaryolarını öğrenin"
                ]
            }
        ]
    },

    # ──────────────────────────────────────────────────────────────
    # 9. EMBEDDED SYSTEMS & IoT
    # ──────────────────────────────────────────────────────────────
    "Embedded & IoT Engineer": {
        "url": "https://roadmap.sh/embedded",
        "emoji": "🤖",
        "color": "#4ade80",
        "lang_weights": {
            "C": 0.95, "C++": 0.90, "Assembly": 0.95, "Rust": 0.85,
            "Python": 0.45, "MicroPython": 0.9
        },
        "repo_signatures": [
            "embedded", "iot", "arduino", "raspberry", "mcu", "firmware",
            "hardware", "esp32", "esp8266", "driver", "microcontroller",
            "rtos", "bare-metal", "sensor", "gpio"
        ],
        "milestones": [
            {
                "title": "C/C++ for Embedded Systems",
                "anchor_url": "https://roadmap.sh/embedded#c-programming",
                "signatures": ["c", "c++", "pointer", "struct", "bit", "register", "volatile", "embedded-c"],
                "why_needed": "Gömülü sistemlerde bellek ve donanım kaynaklarını doğrudan yönetmek için C dilini ve low-level programlamayı derin biçimde öğrenmelisiniz.",
                "action_steps": [
                    "Pointer aritmetiği, bellek yönetimi (malloc/free) ve bit manipülasyonu öğrenin",
                    "volatile ve const anahtar kelimelerinin embedded C'deki önemini kavrayın",
                    "Memory-mapped I/O ve register erişimini öğrenin"
                ]
            },
            {
                "title": "Microcontroller & Peripheral Interfaces",
                "anchor_url": "https://roadmap.sh/embedded#microcontrollers",
                "signatures": ["arduino", "esp32", "stm32", "avr", "arm", "gpio", "uart", "spi", "i2c", "adc", "pwm"],
                "why_needed": "Sensörler ve harici modüllerle iletişim kurmak için UART, SPI, I2C gibi donanım iletişim protokollerini ve mikrodenetleyici çevre birimlerini kavramalısınız.",
                "action_steps": [
                    "Arduino/STM32 ile GPIO kullanarak LED ve buton projesi yapın",
                    "I2C protokolü ile bir sensörden (BMP280, MPU6050) veri okuyun",
                    "PWM ile motor hızı kontrolü veya LED parlaklık ayarı yapın"
                ]
            },
            {
                "title": "RTOS & Bare Metal",
                "anchor_url": "https://roadmap.sh/embedded#rtos",
                "signatures": ["rtos", "freertos", "zephyr", "bare-metal", "interrupt", "task", "scheduler", "semaphore", "mutex"],
                "why_needed": "Gerçek zamanlı ve çok görevli sistemler geliştirmek için RTOS kavramlarını (task, scheduler, mutex) ve interrupt yönetimini öğrenmelisiniz.",
                "action_steps": [
                    "FreeRTOS ile birden fazla görevi (task) paralel çalıştırın",
                    "Interrupt Service Routine (ISR) yazarak harici olayları yakalayın",
                    "Semaphore ve mutex kullanarak paylaşımlı kaynak yönetimi yapın"
                ]
            },
            {
                "title": "IoT Protocols & Connectivity",
                "anchor_url": "https://roadmap.sh/embedded#iot-protocols",
                "signatures": ["mqtt", "coap", "lorawan", "wifi", "bluetooth", "zigbee", "ble", "cloud-iot", "aws-iot"],
                "why_needed": "IoT cihazlarını buluta ve diğer cihazlara bağlamak için MQTT, LoRaWAN ve BLE gibi IoT iletişim protokollerini öğrenmelisiniz.",
                "action_steps": [
                    "MQTT protokolü ile Mosquitto broker üzerinden mesaj yayınlayın/alın",
                    "ESP32 ile Wi-Fi bağlantısı kurarak verileri cloud'a gönderin",
                    "AWS IoT Core veya Azure IoT Hub'a cihaz bağlantısı yapılandırın"
                ]
            }
        ]
    }
}

# ─────────────────────────────────────────────────────────────────────────────
# HİBRİT UNVAN MATRİSİ
# Birincil + İkincil disiplin kombinasyonuna göre dinamik unvan üretimi
# ─────────────────────────────────────────────────────────────────────────────

HYBRID_TITLES = {
    ("Backend Engineer",             "Frontend Engineer"):          ("Full-Stack Software Engineer", "🌟"),
    ("Frontend Engineer",            "Backend Engineer"):           ("Full-Stack Software Engineer", "🌟"),
    ("Backend Engineer",             "DevOps Engineer"):            ("Cloud Native Backend Engineer", "☁️"),
    ("DevOps Engineer",              "Backend Engineer"):           ("Platform & Site Reliability Engineer", "⚙️"),
    ("AI & ML Engineer",             "Backend Engineer"):           ("AI Platform & Data Engineer", "🧠"),
    ("Backend Engineer",             "AI & ML Engineer"):           ("AI-Powered Systems Developer", "🧠"),
    ("AI & ML Engineer",             "Cyber Security Specialist"):  ("AI-Powered Threat Analyst", "🛡️"),
    ("Cyber Security Specialist",    "AI & ML Engineer"):           ("AI-Powered Threat Analyst", "🛡️"),
    ("Cyber Security Specialist",    "DevOps Engineer"):            ("DevSecOps Specialist", "🛡️"),
    ("DevOps Engineer",              "Cyber Security Specialist"):  ("DevSecOps Specialist", "🛡️"),
    ("Blockchain & Web3 Developer",  "Backend Engineer"):           ("Decentralized Web3 Architect", "⛓️"),
    ("Backend Engineer",             "Blockchain & Web3 Developer"):("Web3 Infrastructure Engineer", "⛓️"),
    ("Blockchain & Web3 Developer",  "Frontend Engineer"):          ("dApp Full-Stack Developer", "⛓️"),
    ("Embedded & IoT Engineer",      "AI & ML Engineer"):           ("Edge AI & Robotics Developer", "🤖"),
    ("AI & ML Engineer",             "Embedded & IoT Engineer"):    ("Embedded Intelligence Engineer", "🤖"),
    ("Embedded & IoT Engineer",      "DevOps Engineer"):            ("Industrial IoT Platform Engineer", "🤖"),
    ("Game Developer",               "Backend Engineer"):           ("Multiplayer Systems Game Engineer", "🎮"),
    ("Backend Engineer",             "Game Developer"):             ("Game Server & Backend Architect", "🎮"),
    ("Game Developer",               "AI & ML Engineer"):           ("AI-Driven Game Developer", "🎮"),
    ("AI & ML Engineer",             "Game Developer"):             ("Procedural & Intelligent Game Systems Dev", "🎮"),
    ("Mobile Developer",             "Backend Engineer"):           ("Full-Stack Mobile Developer", "📱"),
    ("Mobile Developer",             "AI & ML Engineer"):           ("On-Device AI Mobile Engineer", "📱"),
    ("AI & ML Engineer",             "Mobile Developer"):           ("On-Device AI Mobile Engineer", "📱"),
    ("Frontend Engineer",            "AI & ML Engineer"):           ("AI-Augmented Frontend Engineer", "🎨"),
    ("Cyber Security Specialist",    "Blockchain & Web3 Developer"):("Smart Contract Security Auditor", "🛡️"),
    ("Blockchain & Web3 Developer",  "Cyber Security Specialist"):  ("Smart Contract Security Auditor", "🛡️"),
}

