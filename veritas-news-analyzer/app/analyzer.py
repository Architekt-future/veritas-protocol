import re
import math
from typing import Dict, List

class VeritasAnalyzer:
    def __init__(self, config: Dict):
        self.config = config
        # Домени для перевірки на абсурд
        self.absurdity_map = {
            "tech": ["квантовий", "5g", "резонанс", "алгоритм", "мережа", "антена", "репітер"],
            "kitchen": ["борщ", "зажарка", "буряк", "сметана", "каструля", "часник", "цибуля"]
        }

    def analyze(self, text: str) -> Dict:
        if not text or len(text.strip()) < 10:
            return {"error": "Too short"}

        words = re.findall(r'\w+', text)
        
        # 1. Покращений Shout Factor (ігноруємо короткі абревіатури)
        caps_words = [w for w in words if w.isupper() and len(w) > 4 and not any(d.isdigit() for d in w)]
        shout_factor = len(caps_words) / (len(words) + 1)

        # 2. Семантична перевірка (Борщовий запобіжник)
        sanity_index = self._check_sanity(text.lower())

        # 3. Базова ентропія (спрощено, основна математика в core.py)
        # Тут ми лише готуємо дані для core
        return {
            "shout_factor": round(shout_factor, 4),
            "sanity_index": sanity_index,
            "word_count": len(words)
        }

    def _check_sanity(self, text: str) -> float:
        has_tech = any(w in text for w in self.absurdity_map["tech"])
        has_kitchen = any(w in text for w in self.absurdity_map["kitchen"])
        
        # Якщо в одному тексті і 5G, і зажарка - це марення
        if has_tech and has_kitchen:
            return 0.1 # Обвал довіри
        return 1.0
