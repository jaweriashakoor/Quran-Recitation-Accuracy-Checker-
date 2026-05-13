from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import json
import difflib
import re
import os
import tempfile
import base64

app = Flask(__name__, static_folder='.')
CORS(app)

QURAN_API_BASE = "https://api.alquran.cloud/v1"

def normalize_arabic(text):
    """Remove diacritics and normalize Arabic text for comparison."""
    if not text:
        return ""
    # Remove tashkeel (diacritics)
    tashkeel = re.compile(r'[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06DC\u06DF-\u06E4\u06E7\u06E8\u06EA-\u06ED]')
    text = tashkeel.sub('', text)
    # Normalize alef variants
    text = re.sub(r'[آأإ]', 'ا', text)
    # Normalize teh marbuta
    text = re.sub(r'ة', 'ه', text)
    # Normalize ya variants
    text = re.sub(r'ى', 'ي', text)
    text = text.strip()
    return text

def word_accuracy(original, spoken):
    """Compare two Arabic words and return accuracy percentage."""
    orig_norm = normalize_arabic(original)
    spoken_norm = normalize_arabic(spoken)
    if orig_norm == spoken_norm:
        return 100
    if not orig_norm or not spoken_norm:
        return 0
    ratio = difflib.SequenceMatcher(None, orig_norm, spoken_norm).ratio()
    return round(ratio * 100)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/surahs', methods=['GET'])
def get_surahs():
    """Get list of all 114 surahs."""
    try:
        resp = requests.get(f"{QURAN_API_BASE}/surah", timeout=10)
        data = resp.json()
        if data.get('code') == 200:
            surahs = []
            for s in data['data']:
                surahs.append({
                    'number': s['number'],
                    'name': s['name'],
                    'englishName': s['englishName'],
                    'englishNameTranslation': s['englishNameTranslation'],
                    'numberOfAyahs': s['numberOfAyahs'],
                    'revelationType': s['revelationType']
                })
            return jsonify({'success': True, 'surahs': surahs})
        return jsonify({'success': False, 'error': 'Failed to fetch surahs'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/surah/<int:surah_number>', methods=['GET'])
def get_surah(surah_number):
    """Get complete surah with Arabic text and tashkeel."""
    try:
        # Use uthmani script for proper tashkeel
        resp = requests.get(f"{QURAN_API_BASE}/surah/{surah_number}/quran-uthmani", timeout=15)
        data = resp.json()
        if data.get('code') == 200:
            surah_data = data['data']
            ayahs = []
            for ayah in surah_data['ayahs']:
                ayahs.append({
                    'number': ayah['numberInSurah'],
                    'text': ayah['text'],
                    'key': f"{surah_number}:{ayah['numberInSurah']}"
                })
            return jsonify({
                'success': True,
                'surah': {
                    'number': surah_data['number'],
                    'name': surah_data['name'],
                    'englishName': surah_data['englishName'],
                    'numberOfAyahs': surah_data['numberOfAyahs'],
                    'ayahs': ayahs
                }
            })
        return jsonify({'success': False, 'error': 'Failed to fetch surah'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/analyze', methods=['POST'])
def analyze_recitation():
    """
    Analyze user's recitation against the selected surah.
    Expects JSON: { surah_number, transcribed_text }
    """
    try:
        body = request.json
        surah_number = body.get('surah_number')
        transcribed_text = body.get('transcribed_text', '').strip()

        if not surah_number or not transcribed_text:
            return jsonify({'success': False, 'error': 'Missing surah_number or transcribed_text'})

        # Fetch surah
        resp = requests.get(f"{QURAN_API_BASE}/surah/{surah_number}/quran-uthmani", timeout=15)
        data = resp.json()
        if data.get('code') != 200:
            return jsonify({'success': False, 'error': 'Failed to fetch surah for analysis'})

        ayahs = data['data']['ayahs']
        surah_name = data['data']['name']
        surah_english = data['data']['englishName']

        # Normalize transcribed text
        transcribed_words = normalize_arabic(transcribed_text).split()

        # Find best matching ayah(s)
        best_score = -1
        best_ayah_indices = []
        best_match_info = None

        # Single ayah matching
        for i, ayah in enumerate(ayahs):
            ayah_text_norm = normalize_arabic(ayah['text'])
            ayah_words = ayah_text_norm.split()
            score = difflib.SequenceMatcher(None, transcribed_words, ayah_words).ratio()
            if score > best_score:
                best_score = score
                best_ayah_indices = [i]

        # Multi-ayah matching (consecutive)
        for window in range(2, min(6, len(ayahs)+1)):
            for i in range(len(ayahs) - window + 1):
                combined = ' '.join(normalize_arabic(ayahs[j]['text']) for j in range(i, i+window))
                combined_words = combined.split()
                score = difflib.SequenceMatcher(None, transcribed_words, combined_words).ratio()
                if score > best_score:
                    best_score = score
                    best_ayah_indices = list(range(i, i+window))

        # Build result
        matched_ayahs = [ayahs[i] for i in best_ayah_indices]
        matched_ayah_numbers = [a['numberInSurah'] for a in matched_ayahs]

        # Combine matched ayah text
        combined_original = ' '.join(a['text'] for a in matched_ayahs)
        combined_original_words = combined_original.split()
        transcribed_text_words = transcribed_text.split()

        # Word-by-word comparison
        word_comparisons = []
        max_len = max(len(combined_original_words), len(transcribed_text_words))
        for idx in range(max_len):
            orig_word = combined_original_words[idx] if idx < len(combined_original_words) else None
            spoken_word = transcribed_text_words[idx] if idx < len(transcribed_text_words) else None
            if orig_word and spoken_word:
                acc = word_accuracy(orig_word, spoken_word)
            elif orig_word and not spoken_word:
                acc = 0
                spoken_word = "---"
            else:
                acc = 0
                orig_word = "---"
            word_comparisons.append({
                'original': orig_word,
                'spoken': spoken_word,
                'accuracy': acc
            })

        # Overall accuracy
        if word_comparisons:
            overall_accuracy = round(sum(w['accuracy'] for w in word_comparisons) / len(word_comparisons))
        else:
            overall_accuracy = 0

        return jsonify({
            'success': True,
            'match': {
                'surahName': surah_name,
                'surahEnglishName': surah_english,
                'surahNumber': surah_number,
                'ayahNumbers': matched_ayah_numbers,
                'confidence': round(best_score * 100)
            },
            'accuracy': {
                'overall': overall_accuracy,
                'originalText': combined_original,
                'spokenText': transcribed_text,
                'wordComparisons': word_comparisons
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print("Starting Quran Recitation Accuracy Checker...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)