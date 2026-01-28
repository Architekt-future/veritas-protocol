import re
import math
from typing import Dict, List

class VeritasAnalyzer:
    def __init__(self, config: Dict):
        self.config = config
        # Домени для перевірки на абсурд (Борщовий запобіжник)
        self.absurdity_map = {
            "tech": ["квантовий", "5g", "резонанс", "алгоритм", "мережа", "антена", "репітер"],
            "kitchen": ["борщ", "зажарка", "буряк", "сметана", "каструля", "часник", "цибуля"]
        }

    def analyze(self, text: str) -> Dict:
        if not text or len(text.strip()) < 10:
            return {"error": "Text too short"}

        words = re.findall(r'\w+', text)
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 2]

        # 1. Покращений Shout Factor (ігноруємо короткі абревіатури AI, DNA тощо)
        # Рахуємо як крик тільки довгі слова CAPS
        caps_words = [w for w in words if w.isupper() and len(w) > 4 and not any(d.isdigit() for d in w)]
        shout_factor = len(caps_words) / (len(words) + 1)

        # 2. Семантична перевірка (Sanity Check)
        sanity_index = self._check_sanity(text.lower())

        # 3. Розрахунок складності (Linguistic Complexity)
        unique_words = len(set([w.lower() for w in words]))
        complexity = unique_words / len(words) if words else 0

        # Повертаємо повний набір метрик для Engine
        return {
            "shout_factor": round(shout_factor, 4),
            "sanity_index": sanity_index,
            "complexity": round(complexity, 4),
            "word_count": len(words),
            "sentence_count": len(sentences),
            "avg_sentence_len": len(words) / len(sentences) if sentences else 0
        }

    def _check_sanity(self, text: str) -> float:
        """Шукає несумісні терміни в одному контексті"""
        has_tech = any(w in text for w in self.absurdity_map["tech"])
        has_kitchen = any(w in text for w in self.absurdity_map["kitchen"])
        
        if has_tech and has_kitchen:
            return 0.1  # Обвал довіри (Абсурд виявлено)
        return 1.0
