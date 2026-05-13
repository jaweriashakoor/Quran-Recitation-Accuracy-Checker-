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
    text = re.sub(r'و(?=\s|$)', 'و', text)  # keep waw normalised
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def word_accuracy(original, spoken):
    """Return accuracy % between two Arabic words (0-100)."""
    orig_n   = normalize_arabic(original)
    spoken_n = normalize_arabic(spoken)
    if orig_n == spoken_n:
        return 100
    if not orig_n or not spoken_n:
        return 0

    # Substring bonus: if one is contained in the other (slow speech / partial)
    if orig_n in spoken_n or spoken_n in orig_n:
        shorter = min(len(orig_n), len(spoken_n))
        longer  = max(len(orig_n), len(spoken_n))
        bonus   = shorter / longer
        ratio   = difflib.SequenceMatcher(None, orig_n, spoken_n).ratio()
        return round(max(ratio, bonus) * 100)

    ratio = difflib.SequenceMatcher(None, orig_n, spoken_n).ratio()
    return round(ratio * 100)


def score_transcription(transcribed_words, ayahs_to_search):
    """
    Find the best-matching ayah window for a given list of transcribed words.
    Returns (best_score, best_ayah_indices).
    """
    best_score        = -1
    best_ayah_indices = []

    # Single-ayah scan
    for i, ayah in enumerate(ayahs_to_search):
        ayah_words = normalize_arabic(ayah['text']).split()
        score = difflib.SequenceMatcher(None, transcribed_words, ayah_words).ratio()

        # Partial-match boost: if user only spoke part of a long ayah, 
        # also try matching the transcription against the first N words of the ayah.
        if len(transcribed_words) < len(ayah_words):
            partial_words = ayah_words[:len(transcribed_words) + 3]
            partial_score = difflib.SequenceMatcher(None, transcribed_words, partial_words).ratio()
            # Weight partial score slightly lower so full matches still win
            score = max(score, partial_score * 0.92)

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

    return best_score, best_ayah_indices


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
        surah_number        (int, required)
        transcribed_text    (str, required)  — best / primary transcript
        alternatives        (list[str], opt) — other recognition candidates
        verse_from          (int | null)
        verse_to            (int | null)

    When multiple alternatives are supplied the backend picks whichever
    transcription scores highest against the Quran text, so quiet /
    noisy recordings that produce uncertain transcripts still get the
    best possible match.
    """
    try:
        body             = request.json
        surah_number     = body.get('surah_number')
        transcribed_text = (body.get('transcribed_text') or '').strip()
        alternatives     = body.get('alternatives', [])   # ← NEW
        verse_from       = body.get('verse_from')
        verse_to         = body.get('verse_to')

        if not surah_number or not transcribed_text:
            return jsonify({'success': False, 'error': 'Missing surah_number or transcribed_text'})

        raw = fetch_surah_from_api(surah_number)
        if not raw:
            return jsonify({'success': False, 'error': 'Failed to fetch surah for analysis'})

        all_ayahs     = raw['ayahs']
        surah_name    = raw['name']
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

        # ── Build candidate list: primary + all alternatives ──
        candidates = [transcribed_text] + [a.strip() for a in alternatives if a.strip()]

        # ── Score every candidate and keep the best ──
        best_overall_score    = -1
        best_overall_indices  = []
        best_candidate_text   = transcribed_text

        for candidate in candidates:
            norm_words = normalize_arabic(candidate).split()
            if not norm_words:
                continue
            score, indices = score_transcription(norm_words, ayahs_to_search)
            if score > best_overall_score:
                best_overall_score   = score
                best_overall_indices = indices
                best_candidate_text  = candidate

        # ── Build matched content using the winning candidate ──
        matched_ayahs        = [ayahs_to_search[i] for i in best_overall_indices]
        matched_ayah_numbers = [a['numberInSurah'] for a in matched_ayahs]
        combined_original    = ' '.join(a['text'] for a in matched_ayahs)

        orig_words   = combined_original.split()
        spoken_words = best_candidate_text.split()

        # ── Word-by-word comparison ──
        # Use SequenceMatcher to align words intelligently (handles insertions/deletions)
        matcher = difflib.SequenceMatcher(None,
            [normalize_arabic(w) for w in orig_words],
            [normalize_arabic(w) for w in spoken_words]
        )

        word_comparisons = []
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                for k in range(i2 - i1):
                    word_comparisons.append({
                        'original': orig_words[i1 + k],
                        'spoken':   spoken_words[j1 + k],
                        'accuracy': 100,
                    })
            elif tag == 'replace':
                orig_chunk   = orig_words[i1:i2]
                spoken_chunk = spoken_words[j1:j2]
                max_len      = max(len(orig_chunk), len(spoken_chunk))
                for k in range(max_len):
                    ow = orig_chunk[k]   if k < len(orig_chunk)   else None
                    sw = spoken_chunk[k] if k < len(spoken_chunk) else None
                    if ow and sw:
                        acc = word_accuracy(ow, sw)
                    elif ow:
                        acc, sw = 0, '---'
                    else:
                        acc, ow = 0, '---'
                    word_comparisons.append({'original': ow, 'spoken': sw, 'accuracy': acc})
            elif tag == 'delete':
                for k in range(i1, i2):
                    word_comparisons.append({'original': orig_words[k], 'spoken': '---', 'accuracy': 0})
            elif tag == 'insert':
                for k in range(j1, j2):
                    word_comparisons.append({'original': '---', 'spoken': spoken_words[k], 'accuracy': 0})

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
                'confidence':       round(best_overall_score * 100),
                'rangeUsed':        bool(verse_from and verse_to),
                'candidateUsed':    best_candidate_text,        # ← which transcript won
                'totalCandidates':  len(candidates),
            },
            'accuracy': {
                'overall':         overall_accuracy,
                'originalText':    combined_original,
                'spokenText':      best_candidate_text,
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