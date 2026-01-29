import json
import math
import re
from collections import Counter

# --- ЯДРО ВБУДОВАНЕ ---
class VeritasCalibratedCore:
    def __init__(self):
        self.chaos_markers = ['рептилоїд', 'масон', 'змова', 'чипування', 'таємний світовий уряд', 'терміново репост', 'шок контент', 'влада приховує', 'паніка']
        self.semantic_categories = {
            'science': ['квантовий', 'синхрофазотрон', 'вакуумний', 'парадигма', 'ентропія', 'транзакція', 'резонанс', 'дискретний'],
            'domestic': ['борщ', 'огірок', 'каструля', 'ложка', 'суп', 'кріп', 'хата', 'вечеря'],
            'esoteric': ['астральний', 'метафізика', 'енергетика', 'всесвіт', 'вібрації', 'карма', 'потік']
        }

    def evaluate_integrity(self, text):
        if not text or len(text) < 10:
            return {"entropy_score": 0.5, "status": "NEED_MORE_DATA"}
        
        # 1. Шеннон
        words = re.findall(r'[а-яіїєґa-z]{3,}', text.lower())
        if not words: return {"entropy_score": 0.5, "status": "NO_WORDS"}
        total_words = len(words)
        counts = Counter(words)
        entropy = -sum((c/total_words)*math.log2(c/total_words) for c in counts.values())
        shannon = min(entropy / (math.log2(total_words + 1) * 0.90), 1.0)
        
        # 2. Дрейф (Борщ)
        found_cats = {cat for cat, kws in self.semantic_categories.items() if any(w in text.lower() for w in kws)}
        drift = 0.4 * (len(found_cats) - 1) if len(found_cats) > 1 else 0
        
        # 3. Штрафи
        chaos_hits = sum(1 for m in self.chaos_markers if m in text.lower())
        shout_factor = len(re.findall(r'[А-ЯІЇЄҐ]{4,}', text)) / (len(text.split()) + 1)
        
        final_score = round(min(max((shannon * 0.4) + (drift * 0.4) + (chaos_hits * 0.2) + (shout_factor * 0.3), 0.2), 1.0), 3)
        return {
            "entropy_score": final_score,
            "status": "TRUSTED" if final_score < 0.45 else "NEUTRAL" if final_score < 0.75 else "CRITICAL",
            "verdict": "АНАЛІЗ ЗАВЕРШЕНО",
            "stats": {"words": total_words, "drift": drift}
        }

# --- ГОЛОВНА ФУНКЦІЯ ДЛЯ VERCEL ---
engine = VeritasCalibratedCore()

def handler(request):
    # Дозволяємо CORS вручну
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-type': 'application/json'
    }

    if request.method == 'OPTIONS':
        return 200, headers, ""

    try:
        # Для GET запитів (статус)
        if request.method == 'GET':
            return 200, headers, json.dumps({"status": "online", "engine": "ready"})

        # Для POST (аналіз)
        payload = json.loads(request.body)
        text = payload.get('text', '')
        result = engine.evaluate_integrity(text)
        return 200, headers, json.dumps(result)

    except Exception as e:
        return 500, headers, json.dumps({"error": str(e)})
