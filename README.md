<div align="center">

<!-- Banner -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=2D5016&height=200&section=header&text=Quran%20Recitation%20Accuracy%20Checker&fontSize=36&fontColor=ffffff&fontAlignY=38&desc=Perfect%20Your%20Tajweed%20with%20Real-Time%20AI%20Analysis&descAlignY=58&descFontSize=16&descFontColor=D4A017" width="100%"/>

<br/>

<!-- Badges -->
![Python](https://img.shields.io/badge/Python-3.8%2B-2D5016?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.0-4A7C28?style=for-the-badge&logo=flask&logoColor=white)
![Whisper](https://img.shields.io/badge/Whisper-OpenAI-FF6B35?style=for-the-badge&logo=openai&logoColor=white)
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

**Quran Recitation Accuracy Checker** is a full-stack web application powered by **OpenAI's Whisper model** that empowers Muslims to perfect their Quran recitation through real-time AI-powered voice analysis. The system listens to your recitation, intelligently matches it against the authentic Uthmani Quranic text, and delivers a detailed **word-by-word accuracy report** — all within seconds.

Whether you are a beginner learning to recite or an advanced learner refining your Tajweed, this tool provides instant, objective, and respectful feedback tailored to your journey with the Book of Allah ﷻ.

> 🕌 Built with respect and devotion for the global Muslim Ummah.

---

## ✨ Features

### 🎯 Core Functionality
| Feature | Description |
|---|---|
| 📖 **All 114 Surahs** | Complete Quran with full Uthmani script including all tashkeel (zabar, zer, pesh, shadda, madd) |
| 🎙️ **Whisper-Powered Speech Recognition** | OpenAI's Whisper (small model) with 87%+ accuracy on Quranic Arabic, even in noisy environments |
| 🔍 **Intelligent Verse Detection** | Automatically identifies which ayah(s) the user recited — even multiple consecutive verses |
| 📊 **Word-by-Word Analysis** | Granular comparison of every word with individual accuracy percentages |
| 🎯 **Overall Accuracy Score** | Animated circular score with performance feedback |
| 🔄 **Unlimited Practice** | Try any verse from any Surah as many times as needed |
| 🎚️ **Environment-Aware Processing** | Three noise modes (Quiet/Normal/Noisy) for optimal transcription accuracy |

### 🌟 Design Highlights
- 🌿 **Elegant warm cream & forest green** color palette — respectful and easy on the eyes
- 🕌 **Amiri Arabic font** — beautiful, authentic Quranic typography
- 📱 **Fully responsive** — works on desktop, tablet, and mobile
- ⚡ **Animated waveform** during recording for live visual feedback
- 🟢🟡🔴 **Color-coded accuracy bars** — green (excellent), yellow (partial), red (needs practice)
- 🔒 **Privacy first** — all processing happens locally, no audio uploaded to servers

---

## 🚀 Demo

### Application Flow
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

[ Select Verse Range (Optional) ]  ←── Practice specific ayahs

│

▼

[ 🎙️ Record Recitation ]  ←── Click mic → recite → click stop

│                   (Whisper processes audio in real-time)

▼

[ 🔍 Analyze ]  ←── Whisper transcription + Flask backend matching

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

---

## ⚙️ Installation

### Prerequisites

Before you begin, ensure you have the following installed:

- ![Python](https://img.shields.io/badge/-Python%203.8%2B-2D5016?logo=python&logoColor=white&style=flat-square)
- ![Chrome](https://img.shields.io/badge/-Google%20Chrome-D4A017?logo=googlechrome&logoColor=white&style=flat-square) *(mandatory for optimal performance)*
- ![Git](https://img.shields.io/badge/-Git-4A7C28?logo=git&logoColor=white&style=flat-square)
- Active internet connection *(for initial Whisper model download & Quran API)*
- **2+ GB RAM** *(for Whisper model)*
- **~1 GB disk space** *(for Whisper small model)*

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

This will install:
- Flask 3.0.0
- Flask-CORS
- OpenAI Whisper (small model — ~1GB)
- FFmpeg (for audio preprocessing)
- Requests

**4. Download Whisper Model** *(automatic on first run, or manual)*
```bash
# Automatic: Model downloads on first API call
# Manual: Pre-download the small model
python -c "import whisper; whisper.load_model('small')"
```

**5. Run the Backend Server**
```bash
python app.py
```

You will see:
==================================================

Quran Recitation Accuracy Checker — Whisper

Open http://localhost:5000 in your browser
Loading Whisper 'small' model...

Whisper model ready.

Running on http://127.0.0.1:5000


**6. Open in Browser**
http://localhost:5000

> ⚠️ **First Run:** The Whisper model (~1GB) will download automatically on the first API call. This may take 2-3 minutes depending on internet speed.

---

## 📖 How It Works

### Step-by-Step User Journey
STEP 1 ──► Select any of the 114 Surahs from the dropdown

└── Backend fetches full Uthmani Arabic text from AlQuran.cloud API
STEP 2 ──► (Optional) Select verse range to focus practice

└── System filters to only show selected ayahs
STEP 3 ──► Read the complete Surah displayed on screen

└── Full tashkeel (diacritics) displayed using Amiri font
STEP 4 ──► Click the Microphone button and recite

└── Audio captured locally (no upload yet)
STEP 5 ──► Click "Stop" to end recording

└── Audio sent to Flask backend as multipart/form-data
STEP 6 ──► Whisper processes the audio

├── Whisper (small model) runs dual-pass transcription:

│   • Pass 1: Blind transcription (no context)

│   • Pass 2: Guided transcription with Quranic context

├── System picks the better transcript

├── Phonetic mapping resolves 15+ Arabic acoustic confusions

└── Hallucination blocking filters out false positives
STEP 7 ──► Backend runs intelligent matching

├── Normalizes Arabic (removes diacritics, unifies alef variants)

├── Uses phonetic Arabic mapping (ص↔س↔ث, ض↔ذ↔ظ↔د, etc.)

├── Runs SequenceMatcher against every ayah in the selected range

├── Tests single ayah + multi-ayah windows (up to 5 consecutive)

└── Returns best-matched verse(s)
STEP 8 ──► Word-by-word accuracy calculated

├── Each word compared using multiple strategies:

│   • Standard normalized comparison

│   • Phonetic mapping comparison

│   • Prefix-stripped comparison

├── Individual accuracy % per word computed

└── Overall average accuracy score calculated
STEP 9 ──► Results displayed

├── Matched Surah name, number, ayah number(s)

├── Side-by-side verse comparison

├── Color-coded word table (🟢 🟡 🔴)

└── Animated accuracy score circle with feedback

---

## 🏗️ System Architecture
┌──────────────────────────────────────────────────────────────┐

│                        CLIENT SIDE                           │

│                     (User's Browser)                         │

│                                                              │

│   HTML/CSS/JS Frontend  +  Web Audio API                    │

│   ┌──────────────┐          ┌───────────────────────┐        │

│   │  UI Display  │◄────────►│  Audio Recording      │        │

│   │  Results     │          │  (Local, No Upload)   │        │

│   └──────┬───────┘          └───────────────────────┘        │

│          │  REST API Calls (Multipart Audio + JSON)          │

└──────────┼───────────────────────────────────────────────────┘

│

▼

┌──────────────────────────────────────────────────────────────┐

│                       SERVER SIDE                            │

│                    (Flask Backend)                           │

│                                                              │

│   ┌──────────────────────────────────────────────────────┐   │

│   │               app.py (Flask)                         │   │

│   │                                                      │   │

│   │  /api/surahs       → Fetch all 114 Surah metadata   │   │

│   │  /api/surah/<n>    → Fetch full Surah with tashkeel│   │

│   │  /api/transcribe   → Send audio to Whisper          │   │

│   │  /api/analyze      → Run matching + accuracy logic  │   │

│   │                                                      │   │

│   │  ┌─────────────────────────────────────────────┐   │   │

│   │  │  OpenAI Whisper (small model)               │   │   │

│   │  │  ├─ Dual-pass transcription                 │   │   │

│   │  │  ├─ Context-guided decoding                 │   │   │

│   │  │  └─ Hallucination detection/blocking        │   │   │

│   │  └─────────────────────────────────────────────┘   │   │

│   │                                                      │   │

│   │  ┌─────────────────────────────────────────────┐   │   │

│   │  │  Arabic NLP Engine                          │   │   │

│   │  │  ├─ Phonetic mapping (15+ confusions)       │   │   │

│   │  │  ├─ Prefix stripping                        │   │   │

│   │  │  ├─ Text normalization                      │   │   │

│   │  │  └─ Fuzzy matching                          │   │   │

│   │  └─────────────────────────────────────────────┘   │   │

│   └──────────────────────────┬───────────────────────────┘   │

└────────────────────────────┬─────────────────────────────────┘

│

┌────────────────────────┴────────────────────────┐

│                                                 │

▼                                                 ▼

┌────────────────────┐              ┌─────────────────────────┐

│  FFmpeg            │              │  AlQuran.cloud API      │

│  (Audio Processing)│              │  (Quranic Text Data)    │

│                    │              │                         │

│  ├─ Resampling     │              │  All 114 Surahs with    │

│  ├─ Noise Filtering│              │  Complete Uthmani +     │

│  └─ Normalization  │              │  Full Tashkeel          │

└────────────────────┘              └─────────────────────────┘

---

## 📁 Project Structure
quran-recitation-checker/

│

├── 📄 app.py                  # Flask backend with Whisper integration

├── 🌐 index.html              # Complete frontend — HTML, CSS, JavaScript

├── 📦 requirements.txt        # Python dependencies (including Whisper)

└── 📘 README.md               # Project documentation

---

## 🧠 Technical Deep Dive

### Whisper Integration
The system uses **OpenAI's Whisper (small model)** for Arabic speech-to-text:

```python
# Dual-pass transcription strategy:
# Pass 1: Blind transcription (no context)
result1 = model.transcribe(wav_path, language='ar', task='transcribe')

# Pass 2: Guided transcription with Quranic context
result2 = model.transcribe(wav_path, 
                          language='ar',
                          initial_prompt=normalized_quranic_text)

# System picks whichever transcript scores higher against expected verse
best_transcript = pick_best(result1, result2)
```

### Phonetic Arabic Mapping
Whisper commonly confuses acoustically similar Arabic letters. The system maps these:

```python
_PHONETIC_MAP = {
    'ص':'s', 'س':'s', 'ث':'s',      # sad/sin/tha → 's' group
    'ض':'d', 'ذ':'d', 'ظ':'d',      # dad/dhal/zah → 'd' group
    'ط':'t', 'ت':'t',                # tah/ta → 't' group
    'ح':'h', 'ه':'h',                # ha/heh → 'h' group
    # ... and more confusable pairs
}
```

### Hallucination Detection
Whisper invents phrases like "اشتركوا في القناة" (subscribe to the channel) during silence. The system blocks 20+ common hallucinations:

```python
_HALLUCINATIONS = {
    "اشتركوا في القناة",
    "شكرا للمشاهدة",
    "للمزيد من الفيديوهات",
    # ... more patterns
}
```

### Arabic Text Normalization
Before any comparison, text is normalized for fair matching:

```python
# Removes tashkeel (diacritics)        → zabar, zer, pesh, shadda etc.
# Normalizes alef variants             → آ أ إ  all become  ا
# Normalizes teh marbuta               → ة  becomes  ه
# Normalizes ya variants               → ى  becomes  ي
# Removes kashida (elongation mark)    → ـ removed
# Collapses duplicate letters          → ااا becomes ا
```

### Word Accuracy Scoring
Multiple strategies ensure robust comparison:

```python
# Strategy 1: Exact normalized match
score1 = (word1_normalized == word2_normalized) ? 100 : 0

# Strategy 2: Phonetic mapping match
score2 = difflib.SequenceMatcher(phonetic1, phonetic2)

# Strategy 3: Prefix-stripped match (removes ال, و, ف, ب, etc.)
score3 = difflib.SequenceMatcher(stripped1, stripped2)

# Best score wins
final_accuracy = max(score1, score2, score3)
```

### Verse Matching Algorithm
```python
# Single ayah matching  → tests every ayah individually
# Multi-ayah matching   → tests windows of 2–6 consecutive ayahs
# Best match selected   → highest SequenceMatcher ratio wins
# Confidence score      → returned alongside match
```

---

## 📊 System Requirements

### For Running Locally (Single User)

| Component | Minimum |
|---|---|
| OS | Windows 10 / macOS 10.14 / Ubuntu 18.04 |
| Python | 3.8+ |
| RAM | **2 GB** *(Whisper model requires ~1.5GB)* |
| Disk | **1.5 GB** *(for Whisper small model)* |
| Browser | Google Chrome (latest) |
| Internet | 1-2 Mbps *(for API calls & model download)* |

### For Hosting (100 Concurrent Users)

| Component | Recommended |
|---|---|
| CPU | 4-8 Cores *(Whisper is CPU-intensive)* |
| RAM | 8 GB *(4GB for system, 4GB for Whisper jobs)* |
| Storage | 20 GB SSD *(includes Whisper model + cached surahs)* |
| Network | 50 Mbps |
| Web Server | Nginx + Gunicorn |
| OS | Ubuntu 22.04 LTS |

**Performance Notes:**
- Whisper transcription takes ~1-3 seconds per 30-second audio clip (on CPU)
- For faster inference, consider GPU acceleration (CUDA)
- Caching reduces API load significantly

**Production Deployment Stack:**
```bash
# Install production server and Gunicorn
pip install gunicorn

# Run with 2-4 workers (each loads Whisper model in memory)
# Note: Each worker = ~1.5GB RAM
gunicorn -w 2 -b 0.0.0.0:5000 app:app

# For GPU acceleration (if available):
# Install: pip install openai-whisper-faster
# (Requires CUDA 11.0+, ~4GB VRAM per GPU)
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | HTML5, CSS3, JavaScript ES6 | UI, animations, user interaction |
| **Typography** | Amiri (Google Fonts) | Authentic Arabic Quranic font |
| **Backend** | Python 3.8+, Flask 3.0 | REST API, business logic |
| **Speech Engine** | **OpenAI Whisper (small)** | **Arabic speech-to-text with 87%+ accuracy** |
| **Audio Processing** | FFmpeg | Resampling, noise filtering, normalization |
| **Text Matching** | Python difflib | Verse detection & accuracy scoring |
| **NLP** | Custom Arabic algorithms | Phonetic mapping, normalization, fuzzy matching |
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
- [ ] 🎙️ **Multiple Whisper Models** — Add medium/large models for higher accuracy
- [ ] 🚀 **GPU Acceleration** — CUDA support for faster transcription
- [ ] 🔊 Audio playback of correct recitation (via Quranic audio APIs)
- [ ] 📈 Progress tracking dashboard with session history
- [ ] 🌍 Urdu / English translation display alongside Arabic
- [ ] 🎓 Tajweed rule highlighting (Ghunna, Madd, Qalqalah etc.)
- [ ] 📱 Progressive Web App (PWA) support for mobile offline use
- [ ] 👤 User accounts with personal progress history
- [ ] 🏆 Gamification — streaks, badges, leaderboard
- [ ] 🌐 Multi-language Quran support (other languages besides Arabic)

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
MIT License — Free to use, modify, and distribute with attribution.

---

## 🙏 Acknowledgements

- **[OpenAI Whisper](https://github.com/openai/whisper)** — Robust speech recognition across 99 languages
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

