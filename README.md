<div align="center">

<!-- Banner -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=2D5016&height=200&section=header&text=Quran%20Recitation%20Accuracy%20Checker&fontSize=36&fontColor=ffffff&fontAlignY=38&desc=Perfect%20Your%20Tajweed%20with%20Real-Time%20AI%20Analysis&descAlignY=58&descFontSize=16&descFontColor=D4A017" width="100%"/>

<br/>

<!-- Badges -->
![Python](https://img.shields.io/badge/Python-3.8%2B-2D5016?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.0-4A7C28?style=for-the-badge&logo=flask&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-Frontend-D4A017?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-Styled-B8860B?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-2D5016?style=for-the-badge&logo=javascript&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-4A7C28?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-D4A017?style=for-the-badge)

<br/>

<h3>
  <em>"And recite the Quran with measured recitation."</em><br/>
  <small>— Surah Al-Muzzammil 73:4</small>
</h3>

<br/>

[✨ Features](#-features) • [🚀 Demo](#-demo) • [⚙️ Installation](#%EF%B8%8F-installation) • [📖 How It Works](#-how-it-works) • [🏗️ Architecture](#%EF%B8%8F-system-architecture) • [📊 System Requirements](#-system-requirements) • [🤝 Contributing](#-contributing)

</div>

---

## 📌 Overview

**Quran Recitation Accuracy Checker** is a full-stack web application that empowers Muslims to perfect their Quran recitation through real-time AI-powered voice analysis. The system listens to your recitation, intelligently matches it against the authentic Uthmani Quranic text, and delivers a detailed **word-by-word accuracy report** — all within seconds.

Whether you are a beginner learning to recite or an advanced learner refining your Tajweed, this tool provides instant, objective, and respectful feedback tailored to your journey with the Book of Allah ﷻ.

> 🕌 Built with respect and devotion for the global Muslim Ummah.

---

## ✨ Features

### 🎯 Core Functionality
| Feature | Description |
|---|---|
| 📖 **All 114 Surahs** | Complete Quran with full Uthmani script including all tashkeel (zabar, zer, pesh, shadda, madd) |
| 🎙️ **Live Voice Recording** | Real-time Arabic speech recognition using Chrome's Web Speech API |
| 🔍 **Intelligent Verse Detection** | Automatically identifies which ayah(s) the user recited — even multiple consecutive verses |
| 📊 **Word-by-Word Analysis** | Granular comparison of every word with individual accuracy percentages |
| 🎯 **Overall Accuracy Score** | Animated circular score with performance feedback |
| 🔄 **Unlimited Practice** | Try any verse from any Surah as many times as needed |

### 🌟 Design Highlights
- 🌿 **Elegant warm cream & forest green** color palette — respectful and easy on the eyes
- 🕌 **Amiri Arabic font** — beautiful, authentic Quranic typography
- 📱 **Fully responsive** — works on desktop, tablet, and mobile
- ⚡ **Animated waveform** during recording for live visual feedback
- 🟢🟡🔴 **Color-coded accuracy bars** — green (excellent), yellow (partial), red (needs practice)
- 🔒 **Privacy first** — no audio ever leaves the user's device

---

## 🚀 Demo

### Application Flow

```
┌─────────────────────────────────────────────────────────┐
│  بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ                    │
│                                                         │
│     Welcome To Quran Recitation Accuracy Checker        │
└─────────────────────────────────────────────────────────┘
           │
           ▼
    [ Select Surah ]  ←── Dropdown with all 114 Surahs
           │
           ▼
    [ Full Arabic Text ]  ←── Complete Uthmani script, scrollable
           │
           ▼
    [ 🎙️ Record Recitation ]  ←── Click mic → recite → click stop
           │
           ▼
    [ 🔍 Analyze ]  ←── System processes in real-time
           │
           ▼
┌─────────────────────────────────────────────────────────┐
│  System Match:  Surah Al-Fatiha · Surah 1 · Ayah 2-4   │
│  Accuracy Score:  87%  ████████░░                       │
│                                                         │
│  Word-by-Word:                                          │
│  ٱلْحَمْدُ   →  الحمد    ✅ 100%                        │
│  لِلَّهِ    →  لله       ✅ 95%                         │
│  رَبِّ      →  رب        🟡 60%                         │
└─────────────────────────────────────────────────────────┘
```

---

## ⚙️ Installation

### Prerequisites

Before you begin, ensure you have the following installed:

- ![Python](https://img.shields.io/badge/-Python%203.8%2B-2D5016?logo=python&logoColor=white&style=flat-square)
- ![Chrome](https://img.shields.io/badge/-Google%20Chrome-D4A017?logo=googlechrome&logoColor=white&style=flat-square) *(mandatory for Arabic speech recognition)*
- ![Git](https://img.shields.io/badge/-Git-4A7C28?logo=git&logoColor=white&style=flat-square)
- Active internet connection *(for Quran API & speech recognition)*

---

### 🔧 Step-by-Step Setup

**1. Clone the Repository**
```bash
git clone https://github.com/YOUR_USERNAME/quran-recitation-checker.git
cd quran-recitation-checker
```

**2. Create a Virtual Environment** *(recommended)*
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the Backend Server**
```bash
python app.py
```

You will see:
```
Starting Quran Recitation Accuracy Checker...
Open http://localhost:5000 in your browser
 * Running on http://127.0.0.1:5000
```

**5. Open in Browser**
```
http://localhost:5000
```

> ⚠️ **Important:** Always use **Google Chrome**. Other browsers do not fully support the Arabic Web Speech API.

---

## 📖 How It Works

### Step-by-Step User Journey

```
STEP 1 ──► Select any of the 114 Surahs from the dropdown
              └── Backend fetches full Uthmani Arabic text from AlQuran.cloud API

STEP 2 ──► Read the complete Surah displayed on screen
              └── Full tashkeel (diacritics) displayed using Amiri font

STEP 3 ──► Click the Microphone button and recite
              └── Chrome Web Speech API (ar-SA) transcribes voice → Arabic text live

STEP 4 ──► Click "Analyze Recitation"
              └── Transcribed text sent to Flask backend via REST API

STEP 5 ──► Backend runs matching algorithm
              ├── Normalizes Arabic (removes diacritics, unifies alef variants)
              ├── Runs SequenceMatcher against every ayah in the Surah
              ├── Tests single ayah + multi-ayah windows (up to 5 consecutive)
              └── Returns best-matched verse(s)

STEP 6 ──► Word-by-word accuracy calculated
              ├── Each word pair compared via character-level similarity
              ├── Individual accuracy % per word
              └── Overall average accuracy score computed

STEP 7 ──► Results displayed
              ├── Matched Surah name, number, ayah number(s)
              ├── Side-by-side verse comparison
              ├── Color-coded word table (🟢 🟡 🔴)
              └── Animated accuracy score circle
```

---

## 🏗️ System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        CLIENT SIDE                           │
│                     (User's Browser)                         │
│                                                              │
│   HTML/CSS/JS Frontend  +  Chrome Web Speech API (ar-SA)    │
│   ┌──────────────┐          ┌───────────────────────┐        │
│   │  UI Display  │◄────────►│  Voice → Arabic Text  │        │
│   │  Results     │          │  (Local, No Upload)   │        │
│   └──────┬───────┘          └───────────────────────┘        │
│          │  REST API Calls (JSON)                            │
└──────────┼───────────────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────────────┐
│                       SERVER SIDE                            │
│                    (Flask Backend)                           │
│                                                              │
│   ┌─────────────────────────────────────────────────────┐   │
│   │               app.py (Flask)                        │   │
│   │                                                     │   │
│   │  /api/surahs      → Fetch all 114 Surah metadata   │   │
│   │  /api/surah/<n>   → Fetch full Surah with tashkeel │   │
│   │  /api/analyze     → Run matching + accuracy logic  │   │
│   │                                                     │   │
│   │  Arabic Normalizer  +  SequenceMatcher Algorithm   │   │
│   └────────────────────────┬────────────────────────────┘   │
└────────────────────────────┼─────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                    EXTERNAL API                              │
│               AlQuran.cloud REST API                         │
│                                                              │
│   Endpoint: api.alquran.cloud/v1/surah/{n}/quran-uthmani    │
│   Returns:  Full Uthmani Arabic text with tashkeel          │
│   Coverage: All 114 Surahs · 6,236 Ayahs                   │
└──────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
quran-recitation-checker/
│
├── 📄 app.py                  # Flask backend — all API routes & analysis logic
├── 🌐 index.html              # Complete frontend — HTML, CSS, JavaScript
├── 📦 requirements.txt        # Python dependencies
└── 📘 README.md               # Project documentation
```

---

## 🧠 Technical Deep Dive

### Arabic Text Normalization
Before any comparison, the system normalizes Arabic text to ensure fair matching:

```python
# Removes tashkeel (diacritics)        → zabar, zer, pesh, shadda etc.
# Normalizes alef variants             → آ أ إ  all become  ا
# Normalizes teh marbuta               → ة  becomes  ه
# Normalizes ya variants               → ى  becomes  ي
```

### Verse Matching Algorithm
```python
# Single ayah matching  → tests every ayah individually
# Multi-ayah matching   → tests windows of 2–5 consecutive ayahs
# Best match selected   → highest SequenceMatcher ratio wins
# Confidence score      → returned alongside match
```

### Word Accuracy Scoring
```python
# Per word:   SequenceMatcher(original_word, spoken_word).ratio() × 100
# Overall:    average of all individual word scores
# Color code: ≥70% Green · 30–69% Yellow · <30% Red
```

---

## 📊 System Requirements

### For Running Locally (Single User)

| Component | Minimum |
|---|---|
| OS | Windows 10 / macOS 10.14 / Ubuntu 18.04 |
| Python | 3.8+ |
| RAM | 2 GB |
| Browser | Google Chrome (latest) |
| Internet | 1 Mbps |

### For Hosting (100 Concurrent Users)

| Component | Recommended |
|---|---|
| CPU | 4 Cores |
| RAM | 4 GB |
| Storage | 20 GB SSD |
| Network | 50 Mbps |
| Web Server | Nginx + Gunicorn |
| OS | Ubuntu 22.04 LTS |

**Production Deployment Stack:**
```bash
# Install production server
pip install gunicorn

# Run with 4 workers (handles ~100 concurrent users)
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | HTML5, CSS3, JavaScript ES6 | UI, animations, user interaction |
| **Typography** | Amiri (Google Fonts) | Authentic Arabic Quranic font |
| **Backend** | Python 3.8+, Flask 3.0 | REST API, business logic |
| **Speech Engine** | Web Speech API (ar-SA) | Voice-to-Arabic-text transcription |
| **Text Matching** | Python difflib | Verse detection & accuracy scoring |
| **Quran Data** | AlQuran.cloud API | 114 Surahs, Uthmani script + tashkeel |
| **Cross-Origin** | Flask-CORS | Frontend-backend communication |

---

## 🤝 Contributing

Contributions are welcome and appreciated! Here's how you can help:

```bash
# 1. Fork the repository
# 2. Create your feature branch
git checkout -b feature/amazing-feature

# 3. Commit your changes
git commit -m "Add: amazing feature description"

# 4. Push to the branch
git push origin feature/amazing-feature

# 5. Open a Pull Request
```

### 💡 Ideas for Future Contributions
- [ ] 🔊 Audio playback of correct recitation (via Quranic audio APIs)
- [ ] 📈 Progress tracking dashboard with session history
- [ ] 🌍 Urdu / English translation display alongside Arabic
- [ ] 🎓 Tajweed rule highlighting (Ghunna, Madd, Qalqalah etc.)
- [ ] 📱 Progressive Web App (PWA) support for mobile offline use
- [ ] 👤 User accounts with personal progress history
- [ ] 🏆 Gamification — streaks, badges, leaderboard

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

```
MIT License — Free to use, modify, and distribute with attribution.
```

---

## 🙏 Acknowledgements

- **[AlQuran.cloud](https://alquran.cloud)** — Free, open Quran API with full Uthmani script
- **[Google Fonts — Amiri](https://fonts.google.com/specimen/Amiri)** — Beautiful Arabic typeface
- **[Quran.com](https://quran.com)** — Inspiration for Quranic app standards
- All contributors and users who help improve this tool for the Ummah

---

<div align="center">

### ⭐ If this project helped you, please give it a star!

*"Whoever recites a letter from the Book of Allah will receive a good deed, and a good deed is multiplied tenfold."*
— Prophet Muhammad ﷺ (Tirmidhi)

<br/>

Made with ❤️ and devotion for the Muslim Ummah

<img src="https://capsule-render.vercel.app/api?type=waving&color=2D5016&height=100&section=footer" width="100%"/>

</div>
