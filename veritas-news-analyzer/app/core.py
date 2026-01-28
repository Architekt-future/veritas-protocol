import math
import re
from typing import Dict

class VeritasEngine:
    def __init__(self, config: Dict):
        self.config = config
        # Базові константи для коригування
        self.entropy_threshold = 0.5
        # Список стоп-комбінацій (можна розширювати через config.yaml)
        self.incompatible_clusters = [
            {"квантовий", "борщ", "зажарка", "5G"}, # Борщовий колапс
            {"магія", "сметана", "криптовалюта"}    # Майбутні аномалії
        ]

    def calculate_veritas_score(self, text: str, sanity_index: float = 1.0) -> float:
        """
         sanity_index передається з analyzer.py після семантичного аналізу
        """
        if not text: return 1.0

        raw_entropy = self._shannon_entropy(text)
        complexity = self._calculate_complexity(text)
        
        # Основна формула: поєднуємо ентропію та складність
        # Veritas Score = (Entropy * 0.7) + (Complexity * 0.3)
        base_score = (raw_entropy * 0.7) + (complexity * 0.3)

        # НОВЕ: Вплив здорового глузду (Sanity Penalty)
        # Якщо sanity_index низький, ми експоненціально підвищуємо ентропію
        if sanity_index < 1.0:
            penalty = (1.0 - sanity_index) * 0.8
            base_score = min(0.999, base_score + penalty)

        return base_score

    def _shannon_entropy(self, data: str) -> float:
        """Розрахунок ентропії Шеннона для тексту"""
        if not data: return 0
        
        prob = [float(data.count(c)) / len(data) for c in dict.fromkeys(list(data))]
        entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])
        
        # Нормалізація до діапазону 0-1 (8 - макс для ASCII)
        return min(1.0, entropy / 8.0)

    def _calculate_complexity(self, text: str) -> float:
        """Оцінка складності структури (Linguistic Density)"""
        words = re.findall(r'\w+', text)
        if not words: return 1.0
        
        unique_words = len(set(words))
        # Чим більше унікальних слів на одиницю тексту, тим нижча ентропія (сигнал чистіший)
        density = unique_words / len(words)
        return 1.0 - density

                                
