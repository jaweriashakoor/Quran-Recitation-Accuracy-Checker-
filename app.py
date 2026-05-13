from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import difflib
import re
import os

app = Flask(__name__, static_folder='.')
CORS(app)

QURAN_API_BASE = "https://api.alquran.cloud/v1"

# ── In-memory cache so we don't hammer the Quran API ──
_surah_cache = {}


def normalize_arabic(text):
    """Remove diacritics and normalize Arabic text for fair comparison."""
    if not text:
        return ""
    # Remove tashkeel (diacritics / harakat)
    tashkeel = re.compile(
        r'[\u0610-\u061A\u064B-\u065F\u0670'
        r'\u06D6-\u06DC\u06DF-\u06E4\u06E7\u06E8\u06EA-\u06ED]'
    )
    text = tashkeel.sub('', text)
    text = re.sub(r'[آأإ]', 'ا', text)   # alef variants → plain alef
    text = re.sub(r'ة', 'ه', text)        # teh marbuta → heh
    text = re.sub(r'ى', 'ي', text)        # alef maqsura → ya
    return text.strip()


def word_accuracy(original, spoken):
    """Return accuracy % between two Arabic words (0-100)."""
    orig_n   = normalize_arabic(original)
    spoken_n = normalize_arabic(spoken)
    if orig_n == spoken_n:
        return 100
    if not orig_n or not spoken_n:
        return 0
    ratio = difflib.SequenceMatcher(None, orig_n, spoken_n).ratio()
    return round(ratio * 100)


def fetch_surah_from_api(surah_number):
    """Fetch a surah from AlQuran.cloud with caching."""
    if surah_number in _surah_cache:
        return _surah_cache[surah_number]

    resp = requests.get(
        f"{QURAN_API_BASE}/surah/{surah_number}/quran-uthmani",
        timeout=15
    )
    data = resp.json()
    if data.get('code') != 200:
        return None

    _surah_cache[surah_number] = data['data']
    return data['data']


# ────────────────────────────────────────────────────────────
# ROUTES
# ────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/api/surahs', methods=['GET'])
def get_surahs():
    """Return metadata for all 114 surahs."""
    try:
        resp = requests.get(f"{QURAN_API_BASE}/surah", timeout=10)
        data = resp.json()
        if data.get('code') == 200:
            surahs = [
                {
                    'number':                  s['number'],
                    'name':                    s['name'],
                    'englishName':             s['englishName'],
                    'englishNameTranslation':  s['englishNameTranslation'],
                    'numberOfAyahs':           s['numberOfAyahs'],
                    'revelationType':          s['revelationType'],
                }
                for s in data['data']
            ]
            return jsonify({'success': True, 'surahs': surahs})
        return jsonify({'success': False, 'error': 'Failed to fetch surah list'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/surah/<int:surah_number>', methods=['GET'])
def get_surah(surah_number):
    """Return complete surah with full Uthmani Arabic text and tashkeel."""
    try:
        raw = fetch_surah_from_api(surah_number)
        if not raw:
            return jsonify({'success': False, 'error': 'Failed to fetch surah'})

        ayahs = [
            {
                'number': a['numberInSurah'],
                'text':   a['text'],
                'key':    f"{surah_number}:{a['numberInSurah']}",
            }
            for a in raw['ayahs']
        ]

        return jsonify({
            'success': True,
            'surah': {
                'number':        raw['number'],
                'name':          raw['name'],
                'englishName':   raw['englishName'],
                'numberOfAyahs': raw['numberOfAyahs'],
                'ayahs':         ayahs,
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/analyze', methods=['POST'])
def analyze_recitation():
    """
    Compare transcribed recitation against the selected surah.

    Body JSON:
        surah_number     (int, required)
        transcribed_text (str, required)
        verse_from       (int | null, optional) — start of verse range
        verse_to         (int | null, optional) — end of verse range

    When verse_from / verse_to are provided the matching is restricted
    to those ayahs only; otherwise the whole surah is searched.
    """
    try:
        body             = request.json
        surah_number     = body.get('surah_number')
        transcribed_text = (body.get('transcribed_text') or '').strip()
        verse_from       = body.get('verse_from')   # may be None
        verse_to         = body.get('verse_to')     # may be None

        if not surah_number or not transcribed_text:
            return jsonify({'success': False, 'error': 'Missing surah_number or transcribed_text'})

        raw = fetch_surah_from_api(surah_number)
        if not raw:
            return jsonify({'success': False, 'error': 'Failed to fetch surah for analysis'})

        all_ayahs    = raw['ayahs']
        surah_name   = raw['name']
        surah_english = raw['englishName']

        # ── Filter ayahs to the selected range (if any) ──
        if verse_from and verse_to:
            ayahs_to_search = [
                a for a in all_ayahs
                if verse_from <= a['numberInSurah'] <= verse_to
            ]
            if not ayahs_to_search:
                return jsonify({'success': False, 'error': 'No ayahs found in the specified range'})
        else:
            ayahs_to_search = all_ayahs

        # ── Normalize user's transcription ──
        transcribed_words = normalize_arabic(transcribed_text).split()

        # ── Find best-matching ayah or window of ayahs ──
        best_score        = -1
        best_ayah_indices = []   # indices into ayahs_to_search

        # Single-ayah scan
        for i, ayah in enumerate(ayahs_to_search):
            ayah_words = normalize_arabic(ayah['text']).split()
            score = difflib.SequenceMatcher(None, transcribed_words, ayah_words).ratio()
            if score > best_score:
                best_score        = score
                best_ayah_indices = [i]

        # Multi-ayah windows (2 to min 6)
        max_window = min(6, len(ayahs_to_search) + 1)
        for window in range(2, max_window):
            for i in range(len(ayahs_to_search) - window + 1):
                combined_norm = ' '.join(
                    normalize_arabic(ayahs_to_search[j]['text'])
                    for j in range(i, i + window)
                )
                combined_words = combined_norm.split()
                score = difflib.SequenceMatcher(None, transcribed_words, combined_words).ratio()
                if score > best_score:
                    best_score        = score
                    best_ayah_indices = list(range(i, i + window))

        # ── Build matched content ──
        matched_ayahs       = [ayahs_to_search[i] for i in best_ayah_indices]
        matched_ayah_numbers = [a['numberInSurah'] for a in matched_ayahs]
        combined_original   = ' '.join(a['text'] for a in matched_ayahs)

        orig_words   = combined_original.split()
        spoken_words = transcribed_text.split()

        # ── Word-by-word comparison ──
        max_len = max(len(orig_words), len(spoken_words))
        word_comparisons = []
        for idx in range(max_len):
            orig_w   = orig_words[idx]   if idx < len(orig_words)   else None
            spoken_w = spoken_words[idx] if idx < len(spoken_words) else None

            if orig_w and spoken_w:
                acc = word_accuracy(orig_w, spoken_w)
            elif orig_w:
                acc      = 0
                spoken_w = '---'
            else:
                acc    = 0
                orig_w = '---'

            word_comparisons.append({
                'original': orig_w,
                'spoken':   spoken_w,
                'accuracy': acc,
            })

        overall_accuracy = (
            round(sum(w['accuracy'] for w in word_comparisons) / len(word_comparisons))
            if word_comparisons else 0
        )

        return jsonify({
            'success': True,
            'match': {
                'surahName':        surah_name,
                'surahEnglishName': surah_english,
                'surahNumber':      surah_number,
                'ayahNumbers':      matched_ayah_numbers,
                'confidence':       round(best_score * 100),
                'rangeUsed':        bool(verse_from and verse_to),
            },
            'accuracy': {
                'overall':         overall_accuracy,
                'originalText':    combined_original,
                'spokenText':      transcribed_text,
                'wordComparisons': word_comparisons,
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    print("=" * 50)
    print("  Quran Recitation Accuracy Checker")
    print("  Open http://localhost:5000 in Chrome")
    print("=" * 50)
    app.run(debug=True, port=5000)