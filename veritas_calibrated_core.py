import math
import re
from collections import Counter

class VeritasCalibratedCore:
    def __init__(self):
        # Маркери прямого хаосу та конспірології
        self.chaos_markers = [
            'рептилоїд', 'масон', 'змова', 'чипування', 'таємний світовий уряд',
            'терміново репост', 'шок контент', 'влада приховує', 'паніка'
        ]
        
        # Категорії для виявлення семантичного розриву (Квантового Борщу)
        self.semantic_categories = {
            'science': ['квантовий', 'синхрофазотрон', 'вакуумний', 'парадигма', 'ентропія', 'транзакція', 'резонанс', 'дискретний'],
            'domestic': ['борщ', 'огірок', 'каструля', 'ложка', 'суп', 'кріп', 'хата', 'вечеря'],
            'esoteric': ['астральний', 'метафізика', 'енергетика', 'всесвіт', 'вібрації', 'карма', 'потік']
        }

    def _calculate_shannon_entropy(self, text):
        words = re.findall(r'[а-яіїєґa-z]{3,}', text.lower())
        if not words:
            return 0
        
        total_words = len(words)
        counts = Counter(words)
        entropy = -sum((count / total_words) * math.log2(count / total_words) for count in counts.values())
        
        # Калібрування: нормалізація під живу мову (захист Вікіпедії)
        ideal_entropy = math.log2(total_words + 1) * 0.90
        return min(entropy / ideal_entropy, 1.0)

    def _calculate_semantic_drift(self, text):
        text_lower = text.lower()
        found_cats = set()
        
        for cat, keywords in self.semantic_categories.items():
            if any(word in text_lower for word in keywords):
                found_cats.add(cat)
        
        # Якщо в тексті змішано непоєднувані категорії (напр. Наука + Кулінарія)
        if len(found_cats) > 1:
            return 0.4 * (len(found_cats) - 1)
        return 0

    def evaluate_integrity(self, text):
        if not text or len(text) < 10:
            return {"entropy_score": 0.5, "status": "INSUFFICIENT_DATA"}

        # 1. Розрахунок базової ентропії
        shannon = self._calculate_shannon_entropy(text)
        
        # 2. Виявлення семантичного дрейфу (Квантовий Борщ)
        drift = self._calculate_semantic_drift(text)
        
        # 3. Пошук прямих маркерів хаосу
        chaos_hits = sum(1 for m in self.chaos_markers if m in text.lower())
        chaos_penalty = min(chaos_hits * 0.2, 0.5)
        
        # 4. Аналіз агресивності (Caps Lock та вигуки)
        shout_factor = len(re.findall(r'[А-ЯІЇЄҐ]{4,}', text)) / (len(text.split()) + 1)
        shout_penalty = min(shout_factor * 0.5, 0.3)

        # ФІНАЛЬНА ФОРМУЛА: Ентропія + Дрейф + Штрафи
        # Збільшуємо вагу дрейфу для виявлення абсурду
        final_score = (shannon * 0.4) + (drift * 0.4) + chaos_penalty + shout_penalty
        
        # Обмежуємо результат від 0 до 1
        final_score = round(min(max(final_score, 0.2), 1.0), 3)

        # Визначення статусу
        if final_score < 0.45:
            status = "TRUSTED / ACADEMIC"
            verdict = "СТАБІЛЬНИЙ ЛОГІЧНИЙ СИГНАЛ"
        elif final_score < 0.75:
            status = "MODERATE / NEUTRAL"
            verdict = "ПРИЙНЯТНА СТРУКТУРОВАНА ІНФОРМАЦІЯ"
        else:
            status = "CRITICAL / CHAOS"
            verdict = "КОНСПІРОЛОГІЯ / СЕМАНТИЧНИЙ ХАОС"

        return {
            "entropy_score": final_score,
            "shannon_raw": round(shannon, 3),
            "drift_score": round(drift, 3),
            "status": status,
            "verdict": verdict,
            "stats": {
                "words": len(text.split()),
                "chaos_markers": chaos_hits
            }
        }
