import re
import math
from typing import Dict, List

class VeritasAnalyzer:
    def __init__(self, config: Dict):
        self.config = config
        # Додаємо словник несумісних категорій для відлову "борщового абсурду"
        self.absurdity_clusters = {
            "tech_absurd": ["квантовий", "5G", "резонанс", "алгоритм", "мережа"],
            "kitchen_absurd": ["борщ", "зажарка", "буряк", "сметана", "каструля", "часник"]
        }

    def analyze(self, text: str) -> Dict:
        if not text or len(text.strip()) < 10:
            return self._empty_result()

        words = re.findall(r'\w+', text.lower())
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 2]

        # Базові метрики
        entropy = self._calculate_entropy(text)
        laminar_flow = self._calculate_laminar_flow(words, sentences)
        
        # НОВЕ: Перевірка на здоровий глузд (Sanity Check)
        sanity_score = self._check_semantic_sanity(words)
        
        # Коригуємо ентропію: якщо текст абсурдний, ентропія злітає вгору, 
        # навіть якщо структура ідеальна
        adjusted_entropy = entropy
        if sanity_score < 0.5:
            adjusted_entropy = max(entropy, 0.85) # Штраф за борщ

        return {
            "entropy_index": round(adjusted_entropy, 3),
            "laminar_flow": round(laminar_flow, 3),
            "sanity_index": round(sanity_score, 3),
            "status": self._get_status(adjusted_entropy, sanity_score),
            "metrics": {
                "word_count": len(words),
                "sentence_count": len(sentences),
                "avg_sentence_len": len(words) / len(sentences) if sentences else 0
            }
        }

    def _calculate_entropy(self, text: str) -> float:
        # Твоя існуюча логіка розрахунку ентропії (спрощено для прикладу)
        # В ідеалі тут залишається твій LAC-алгоритм
        if len(text) < 100: return 0.999
        return 0.2 # Тимчасова заглушка, твій оригінальний код тут мав би бути
    
    def _calculate_laminar_flow(self, words: List[str], sentences: List[str]) -> float:
        # Розрахунок структурної зв'язності
        if not sentences: return 0
        return min(1.0, len(sentences) / (len(words) / 10))

    def _check_semantic_sanity(self, words: List[str]) -> float:
        """
        Виявляє 'Квантовий Борщ'. Якщо в тексті забагато слів з несумісних світів,
        індекс довіри падає.
        """
        has_tech = any(w in self.absurdity_clusters["tech_absurd"] for w in words)
        has_kitchen = any(w in self.absurdity_clusters["kitchen_absurd"] for w in words)
        
        # Якщо є і технології, і кухня в одному короткому тексті — це підозріло
        if has_tech and has_kitchen:
            return 0.15  # Критичний рівень абсурду
        return 1.0

    def _get_status(self, entropy: float, sanity: float) -> str:
        if sanity < 0.5:
            return "LOGICAL_MIRAGE (ABSURD)"
        if entropy < 0.3:
            return "TRUSTED"
        if entropy < 0.7:
            return "UNCERTAIN"
        return "CRITICAL"

    def _empty_result(self) -> Dict:
        return {"entropy_index": 1.0, "status": "EMPTY", "metrics": {}}

