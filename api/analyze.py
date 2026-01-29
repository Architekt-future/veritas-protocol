import json
import http.server
import urllib.parse
import sys
import os
import math
import re
from collections import Counter

# --- ТУТ ТЕПЕР ЖИВЕ ЯДРО (Вбудоване для 100% стабільності) ---
class VeritasCalibratedCore:
    def __init__(self):
        self.chaos_markers = [
            'рептилоїд', 'масон', 'змова', 'чипування', 'таємний світовий уряд',
            'терміново репост', 'шок контент', 'влада приховує', 'паніка'
        ]
        self.semantic_categories = {
            'science': ['квантовий', 'синхрофазотрон', 'вакуумний', 'парадигма', 'ентропія', 'транзакція', 'резонанс', 'дискретний'],
            'domestic': ['борщ', 'огірок', 'каструля', 'ложка', 'суп', 'кріп', 'хата', 'вечеря'],
            'esoteric': ['астральний', 'метафізика', 'енергетика', 'всесвіт', 'вібрації', 'карма', 'потік']
        }

    def _calculate_shannon_entropy(self, text):
        words = re.findall(r'[а-яіїєґa-z]{3,}', text.lower())
        if not words: return 0
        total_words = len(words)
        counts = Counter(words)
        entropy = -sum((count / total_words) * math.log2(count / total_words) for count in counts.values())
        ideal_entropy = math.log2(total_words + 1) * 0.90
        return min(entropy / ideal_entropy, 1.0)

    def _calculate_semantic_drift(self, text):
        text_lower = text.lower()
        found_cats = set()
        for cat, keywords in self.semantic_categories.items():
            if any(word in text_lower for word in keywords):
                found_cats.add(cat)
        return 0.4 * (len(found_cats) - 1) if len(found_cats) > 1 else 0

    def evaluate_integrity(self, text):
        if not text or len(text) < 10:
            return {"entropy_score": 0.5, "status": "INSUFFICIENT_DATA"}
        shannon = self._calculate_shannon_entropy(text)
        drift = self._calculate_semantic_drift(text)
        chaos_hits = sum(1 for m in self.chaos_markers if m in text.lower())
        chaos_penalty = min(chaos_hits * 0.2, 0.5)
        shout_factor = len(re.findall(r'[А-ЯІЇЄҐ]{4,}', text)) / (len(text.split()) + 1)
        shout_penalty = min(shout_factor * 0.5, 0.3)
        final_score = round(min(max((shannon * 0.4) + (drift * 0.4) + chaos_penalty + shout_penalty, 0.2), 1.0), 3)
        
        status = "TRUSTED" if final_score < 0.45 else "NEUTRAL" if final_score < 0.75 else "CRITICAL / CHAOS"
        return {
            "entropy_score": final_score,
            "shannon_raw": round(shannon, 3),
            "drift_score": round(drift, 3),
            "status": status,
            "verdict": "АНАЛІЗ ЗАВЕРШЕНО",
            "stats": {"words": len(text.split()), "chaos_markers": chaos_hits}
        }

# --- СЕРВЕРНА ЧАСТИНА (HANDLER) ---
engine = VeritasCalibratedCore()

class handler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "online",
            "engine_ready": engine is not None
        }).encode())

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        try:
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            text = data.get('text', '')
            
            result = engine.evaluate_integrity(text)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
