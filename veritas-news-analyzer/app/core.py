import math
import re
from typing import Dict

class VeritasEngine:
    def __init__(self, config: Dict = None):
        self.config = config or {}
        # Пороги для статусів
        self.thresholds = {
            "trusted": 0.3,
            "warning": 0.6,
            "critical": 0.85
        }

    def calculate_veritas_score(self, metrics: Dict) -> float:
        """
        Головна формула Veritas Protocol v3.5
        Приймає метрики з analyzer.py та вираховує фінальний індекс ентропії.
        """
        # Отримуємо дані з аналізатора
        shout = metrics.get('shout_factor', 0)
        sanity = metrics.get('sanity_index', 1.0)
        complexity = metrics.get('complexity', 0.5)
        
        # 1. Розрахунок базової ентропії на основі лінгвістичної складності
        # Чим вища складність (unique words), тим нижча базова ентропія
        base_score = 1.0 - complexity
        
        # 2. Вплив Shout Factor (тепер він м'який, бо відфільтрований в analyzer.py)
        # Додає максимум 0.3 до ентропії
        shout_impact = shout * 0.3
        
        # 3. Фінальна збірка
        final_score = (base_score * 0.7) + shout_impact
        
        # 4. СЕМАНТИЧНИЙ ШТРАФ (Захист від "Квантового борщу")
        # Якщо sanity_index низький, ми примусово виводимо результат у червону зону
        if sanity < 0.5:
            # Експоненціальне зростання ентропії при порушенні логіки
            final_score = max(final_score, 0.92)
            
        return round(min(0.999, final_score), 4)

    def get_status(self, score: float) -> str:
        """Повертає статус на основі фінального результату"""
        if score < self.thresholds["trusted"]:
            return "STABLE LOGICAL SIGNAL (TRUSTED)"
        if score < self.thresholds["warning"]:
            return "ACCEPTABLE QUALITY (SUCCESS)"
        if score < self.thresholds["critical"]:
            return "RHETORICAL NOISE (WARNING)"
        return "LOGICAL MIRAGE (CRITICAL)"
