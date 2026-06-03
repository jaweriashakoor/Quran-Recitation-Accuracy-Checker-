from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import difflib
import re
import os
import tempfile
import subprocess

app = Flask(__name__, static_folder='.')
CORS(app)

QURAN_API_BASE = "https://api.alquran.cloud/v1"

_whisper_model = None
_surah_cache   = {}


def get_whisper_model():
    global _whisper_model
    if _whisper_model is None:
        import whisper
        print("Loading Whisper 'small' model...")
        _whisper_model = whisper.load_model("small")
        print("Whisper model ready.")
    return _whisper_model


# ═══════════════════════════════════════════════════════════
#  ARABIC NORMALISATION
# ═══════════════════════════════════════════════════════════

_TASHKEEL = re.compile(
    r'[\u0610-\u061A\u064B-\u065F\u0670'
    r'\u06D6-\u06DC\u06DF-\u06E4\u06E7\u06E8\u06EA-\u06ED]'
)

def normalize_arabic(text: str) -> str:
    if not text:
        return ""
    text = _TASHKEEL.sub('', text)
    text = re.sub(r'[آأإٱ]',         'ا',  text)
    text = re.sub(r'ة',               'ه',  text)
    text = re.sub(r'ى',               'ي',  text)
    text = re.sub(r'ؤ',               'و',  text)
    text = re.sub(r'ئ',               'ي',  text)
    text = re.sub(r'ء',               'ا',  text)
    text = re.sub(r'\u0640',          '',   text)
    text = re.sub(r'[\uFEF5-\uFEFC]', 'لا', text)
    text = re.sub(r'(.)\1+',          r'\1',text)
    text = re.sub(r'\s+',             ' ',  text)
    return text.strip()


# ═══════════════════════════════════════════════════════════
#  PHONETIC MAPPING
#  Acoustically similar Arabic letters → same code.
#  This forgives common Whisper mishearings like:
#    ز↔ج  ص↔س↔ث  ض↔ذ↔ظ↔د  ط↔ت  ح↔ه
# ═══════════════════════════════════════════════════════════

_PHONETIC_MAP = str.maketrans({
    'ص':'s','س':'s','ث':'s',
    'ض':'d','ذ':'d','ظ':'d','د':'d',
    'ط':'t','ت':'t',
    'ح':'h','ه':'h',
    'خ':'x',
    'ع':'a','ا':'a',
    'و':'w','ي':'y','ى':'y',
    'ز':'z','ج':'z',
    'ق':'q','ك':'k','غ':'g',
    'ن':'n','م':'m',
    'ر':'r','ل':'l',
    'ب':'b','ف':'f',
    'ش':'c','ة':'h',
})

def phonetic_arabic(word: str) -> str:
    return normalize_arabic(word).translate(_PHONETIC_MAP)


# ═══════════════════════════════════════════════════════════
#  HALLUCINATION BLOCKLIST — YouTube phrases Whisper invents
#  when it hears silence. Only blocks short (<=5 word) results.
# ═══════════════════════════════════════════════════════════

_HALLUCINATIONS_NORM = {
    normalize_arabic(p) for p in [
        "اشتركوا في القناة",
        "اشترك في القناة",
        "لا تنسى الاشتراك",
        "لا تنسوا الاشتراك",
        "اشتركوا بالقناة",
        "تابعونا",
        "للمزيد من الفيديوهات",
        "شكرا للمشاهدة",
        "شكرا على المشاهدة",
    ]
}

def is_hallucination(transcript: str) -> bool:
    if len(transcript.split()) > 5:
        return False   # long text = real speech, never block
    norm = normalize_arabic(transcript)
    for h in _HALLUCINATIONS_NORM:
        if norm == h or norm in h or h in norm:
            return True
    return False


# ═══════════════════════════════════════════════════════════
#  PREFIX STRIPPING
# ═══════════════════════════════════════════════════════════

_PREFIXES = ['وال','فال','بال','كال','لل','ال','و','ف','ب','ك','ل']

def strip_prefix(word: str) -> str:
    for p in _PREFIXES:
        if word.startswith(p) and len(word) > len(p) + 1:
            return word[len(p):]
    return word


# ═══════════════════════════════════════════════════════════
#  WORD ACCURACY  (multi-strategy, best wins)
# ═══════════════════════════════════════════════════════════

def word_accuracy(original: str, spoken: str) -> int:
    on = normalize_arabic(original)
    sn = normalize_arabic(spoken)
    if not on or not sn:
        return 0
    if on == sn:
        return 100

    scores = []
    os_ = strip_prefix(on)
    ss_ = strip_prefix(sn)
    if os_ and ss_ and os_ == ss_:
        return 95

    op = phonetic_arabic(on)
    sp = phonetic_arabic(sn)
    if op == sp and op:
        scores.append(97)
    elif op and sp:
        scores.append(difflib.SequenceMatcher(None, op, sp).ratio() * 100)

    ops = phonetic_arabic(os_)
    sps = phonetic_arabic(ss_)
    if ops and sps:
        if ops == sps:
            scores.append(93)
        else:
            scores.append(difflib.SequenceMatcher(None, ops, sps).ratio() * 95)

    scores.append(difflib.SequenceMatcher(None, on, sn).ratio() * 100)
    if os_ and ss_:
        scores.append(difflib.SequenceMatcher(None, os_, ss_).ratio() * 100)
    if on in sn or sn in on:
        scores.append((min(len(on),len(sn)) / max(len(on),len(sn))) * 100)

    best = max(scores) if scores else 0
    if best >= 60:
        best = min(100, best * 1.12)
    return round(best)


# ═══════════════════════════════════════════════════════════
#  VERSE-AWARE SCORING
#  When user has selected a verse range, we score the
#  transcription directly against those specific ayahs
#  using both normalised AND phonetic comparison.
# ═══════════════════════════════════════════════════════════

def score_transcription(transcribed_words, ayahs_to_search):
    best_score        = -1.0
    best_ayah_indices = []

    t_phon = [phonetic_arabic(w) for w in transcribed_words]

    def best_ratio(an, ap):
        r1 = difflib.SequenceMatcher(None, transcribed_words, an, autojunk=False).ratio()
        r2 = difflib.SequenceMatcher(None, t_phon,            ap, autojunk=False).ratio()
        return max(r1, r2)

    for i, ayah in enumerate(ayahs_to_search):
        aw = normalize_arabic(ayah['text']).split()
        ap = [phonetic_arabic(w) for w in aw]
        score = best_ratio(aw, ap)
        if len(transcribed_words) < len(aw):
            score = max(score,
                        best_ratio(aw[:len(transcribed_words)+4],
                                   ap[:len(t_phon)+4]) * 0.94)
        if score > best_score:
            best_score, best_ayah_indices = score, [i]

    for window in range(2, min(6, len(ayahs_to_search)+1)):
        for i in range(len(ayahs_to_search)-window+1):
            cn, cp = [], []
            for j in range(i, i+window):
                wn = normalize_arabic(ayahs_to_search[j]['text']).split()
                cn += wn
                cp += [phonetic_arabic(w) for w in wn]
            score = best_ratio(cn, cp)
            if score > best_score:
                best_score, best_ayah_indices = score, list(range(i, i+window))

    return best_score, best_ayah_indices


# ═══════════════════════════════════════════════════════════
#  FORCED-DECODE: re-run Whisper with the expected verse
#  as a decode prompt so it stays on-track.
#  This is the KEY improvement — Whisper is guided to
#  transcribe what was actually said vs the expected text.
# ═══════════════════════════════════════════════════════════

def transcribe_with_context(wav_path: str, expected_text: str = None) -> str:
    """
    Transcribe audio. If expected_text is provided (the ayah the user
    should be reciting), we run Whisper TWICE:
      Pass 1 — blind transcription (no prompt)
      Pass 2 — guided transcription using expected_text as decode_options prompt
    We pick whichever output scores higher against the expected text.
    """
    model = get_whisper_model()

    base_options = dict(
        language='ar',
        task='transcribe',
        beam_size=5,
        best_of=5,
        temperature=0.0,
        no_speech_threshold=0.6,
        logprob_threshold=-1.0,
        compression_ratio_threshold=2.4,
        condition_on_previous_text=False,
        fp16=False,
        verbose=False,
    )

    # Pass 1: blind
    result1 = model.transcribe(wav_path, **base_options)
    t1 = clean_transcript(result1.get('text', ''))

    if not expected_text:
        return t1

    # Pass 2: guided — use normalised expected verse as prompt
    # This keeps Whisper focused on Quranic vocabulary
    prompt = normalize_arabic(expected_text)
    guided_options = {**base_options, 'initial_prompt': prompt}
    try:
        result2 = model.transcribe(wav_path, **guided_options)
        t2 = clean_transcript(result2.get('text', ''))
    except Exception:
        return t1

    if not t2 or is_hallucination(t2):
        return t1
    if not t1 or is_hallucination(t1):
        return t2

    # Pick whichever transcript scores higher against the expected verse
    exp_norm  = normalize_arabic(expected_text).split()
    exp_phon  = [phonetic_arabic(w) for w in exp_norm]

    def score_vs_expected(t):
        tw = normalize_arabic(t).split()
        tp = [phonetic_arabic(w) for w in tw]
        r1 = difflib.SequenceMatcher(None, tw, exp_norm, autojunk=False).ratio()
        r2 = difflib.SequenceMatcher(None, tp, exp_phon, autojunk=False).ratio()
        return max(r1, r2)

    s1 = score_vs_expected(t1)
    s2 = score_vs_expected(t2)
    return t2 if s2 > s1 else t1


def clean_transcript(text: str) -> str:
    text = (text or '').strip()
    text = re.sub(r'[^\u0600-\u06FF\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# ═══════════════════════════════════════════════════════════
#  AUDIO CONVERSION
# ═══════════════════════════════════════════════════════════

def convert_to_wav(input_path: str) -> str:
    wav_path = input_path + "_conv.wav"
    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-ar", "16000", "-ac", "1",
        "-c:a", "pcm_s16le",
        "-af", "highpass=f=80,lowpass=f=8000,afftdn=nf=-25,dynaudnorm=p=0.9:m=30",
        wav_path, "-loglevel", "error"
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=30)
        if r.returncode == 0 and os.path.exists(wav_path):
            return wav_path
    except Exception:
        pass
    return input_path


def fetch_surah_from_api(surah_number):
    if surah_number in _surah_cache:
        return _surah_cache[surah_number]
    resp = requests.get(
        f"{QURAN_API_BASE}/surah/{surah_number}/quran-uthmani", timeout=15)
    data = resp.json()
    if data.get('code') != 200:
        return None
    _surah_cache[surah_number] = data['data']
    return data['data']


# ═══════════════════════════════════════════════════════════
#  ROUTES
# ═══════════════════════════════════════════════════════════

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/api/surahs')
def get_surahs():
    try:
        resp = requests.get(f"{QURAN_API_BASE}/surah", timeout=10)
        data = resp.json()
        if data.get('code') == 200:
            surahs = [{
                'number':                 s['number'],
                'name':                   s['name'],
                'englishName':            s['englishName'],
                'englishNameTranslation': s['englishNameTranslation'],
                'numberOfAyahs':          s['numberOfAyahs'],
                'revelationType':         s['revelationType'],
            } for s in data['data']]
            return jsonify({'success': True, 'surahs': surahs})
        return jsonify({'success': False, 'error': 'Failed to fetch surah list'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/surah/<int:surah_number>')
def get_surah(surah_number):
    try:
        raw = fetch_surah_from_api(surah_number)
        if not raw:
            return jsonify({'success': False, 'error': 'Failed to fetch surah'})
        ayahs = [{'number': a['numberInSurah'], 'text': a['text'],
                  'key': f"{surah_number}:{a['numberInSurah']}"}
                 for a in raw['ayahs']]
        return jsonify({'success': True, 'surah': {
            'number': raw['number'], 'name': raw['name'],
            'englishName': raw['englishName'],
            'numberOfAyahs': raw['numberOfAyahs'], 'ayahs': ayahs,
        }})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/transcribe', methods=['POST'])
def transcribe_audio():
    """
    Accepts: multipart/form-data with:
      audio        — audio blob
      expected_text (optional) — the ayah text the user should be reciting.
                    When provided, Whisper runs a second guided pass and
                    the better transcript is returned.
    """
    tmp_path = wav_path = None
    try:
        if 'audio' not in request.files:
            return jsonify({'success': False, 'error': 'No audio file provided'})

        audio_file    = request.files['audio']
        expected_text = request.form.get('expected_text', '').strip() or None
        content_type  = audio_file.content_type or ''

        if   'ogg'  in content_type:                           ext = '.ogg'
        elif 'mp4'  in content_type or 'mpeg' in content_type: ext = '.mp4'
        elif 'wav'  in content_type:                           ext = '.wav'
        else:                                                  ext = '.webm'

        with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
            tmp_path = tmp.name
            audio_file.save(tmp_path)

        wav_path   = convert_to_wav(tmp_path)
        transcript = transcribe_with_context(wav_path, expected_text)

        if not transcript:
            return jsonify({
                'success': False,
                'error': 'No speech detected. Please speak clearly and try again.'
            })

        if is_hallucination(transcript):
            return jsonify({
                'success': False,
                'error': 'Could not detect clear recitation. Please speak louder and closer to the microphone.'
            })

        return jsonify({
            'success':          True,
            'transcribed_text': transcript,
            'alternatives':     [],
            'language':         'ar',
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

    finally:
        for p in [wav_path, tmp_path]:
            if p and os.path.exists(p):
                try: os.unlink(p)
                except: pass


@app.route('/api/analyze', methods=['POST'])
def analyze_recitation():
    try:
        body             = request.json
        surah_number     = body.get('surah_number')
        transcribed_text = (body.get('transcribed_text') or '').strip()
        alternatives     = body.get('alternatives', [])
        verse_from       = body.get('verse_from')
        verse_to         = body.get('verse_to')

        if not surah_number or not transcribed_text:
            return jsonify({'success': False, 'error': 'Missing required fields'})

        raw = fetch_surah_from_api(surah_number)
        if not raw:
            return jsonify({'success': False, 'error': 'Failed to fetch surah'})

        all_ayahs     = raw['ayahs']
        surah_name    = raw['name']
        surah_english = raw['englishName']

        if verse_from and verse_to:
            ayahs_to_search = [a for a in all_ayahs
                               if verse_from <= a['numberInSurah'] <= verse_to]
            if not ayahs_to_search:
                return jsonify({'success': False, 'error': 'No ayahs in range'})
        else:
            ayahs_to_search = all_ayahs

        candidates = [transcribed_text] + [a.strip() for a in alternatives if a.strip()]

        best_score   = -1.0
        best_indices = []
        best_text    = transcribed_text

        for candidate in candidates:
            nw = normalize_arabic(candidate).split()
            if not nw:
                continue
            score, indices = score_transcription(nw, ayahs_to_search)
            if score > best_score:
                best_score, best_indices, best_text = score, indices, candidate

        matched_ayahs = [ayahs_to_search[i] for i in best_indices]
        ayah_numbers  = [a['numberInSurah'] for a in matched_ayahs]
        combined_orig = ' '.join(a['text'] for a in matched_ayahs)

        orig_words   = combined_orig.split()
        spoken_words = best_text.split()

        norm_orig   = [normalize_arabic(w) for w in orig_words]
        norm_spoken = [normalize_arabic(w) for w in spoken_words]
        phon_orig   = [phonetic_arabic(w) for w in norm_orig]
        phon_spoken = [phonetic_arabic(w) for w in norm_spoken]

        matcher = difflib.SequenceMatcher(None, phon_orig, phon_spoken, autojunk=False)

        word_comparisons = []
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                for k in range(i2-i1):
                    acc = word_accuracy(orig_words[i1+k], spoken_words[j1+k])
                    word_comparisons.append({
                        'original': orig_words[i1+k],
                        'spoken':   spoken_words[j1+k],
                        'accuracy': acc,
                    })
            elif tag == 'replace':
                oc = orig_words[i1:i2]
                sc = spoken_words[j1:j2]
                for k in range(max(len(oc), len(sc))):
                    ow = oc[k] if k < len(oc) else None
                    sw = sc[k] if k < len(sc) else None
                    if ow and sw:   acc = word_accuracy(ow, sw)
                    elif ow:        acc, sw = 0, '---'
                    else:           acc, ow = 0, '---'
                    word_comparisons.append({'original': ow, 'spoken': sw, 'accuracy': acc})
            elif tag == 'delete':
                for k in range(i1, i2):
                    word_comparisons.append({
                        'original': orig_words[k], 'spoken': '---', 'accuracy': 0})
            elif tag == 'insert':
                for k in range(j1, j2):
                    word_comparisons.append({
                        'original': '---', 'spoken': spoken_words[k], 'accuracy': 0})

        overall = (round(sum(w['accuracy'] for w in word_comparisons) / len(word_comparisons))
                   if word_comparisons else 0)

        return jsonify({
            'success': True,
            'match': {
                'surahName':        surah_name,
                'surahEnglishName': surah_english,
                'surahNumber':      surah_number,
                'ayahNumbers':      ayah_numbers,
                'confidence':       round(best_score * 100),
                'rangeUsed':        bool(verse_from and verse_to),
                'candidateUsed':    best_text,
                'totalCandidates':  len(candidates),
            },
            'accuracy': {
                'overall':         overall,
                'originalText':    combined_orig,
                'spokenText':      best_text,
                'wordComparisons': word_comparisons,
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    print("=" * 52)
    print("  Quran Recitation Accuracy Checker — Whisper")
    print("  Open http://localhost:5000 in your browser")
    print("=" * 52)
    get_whisper_model()
    app.run(debug=True, port=5000)