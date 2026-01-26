"""
Veritas News Analyzer - Multilingual Support (v2.0 - Calibrated)
Покращена підтримка української та англійської мов
"""

from typing import Dict, Set
import re


class LanguageDetector:
    """Визначає мову тексту та адаптує маркери"""
    
    # Маркери ентропії для різних мов
    NOISE_MARKERS = {
        'uk': {
            "етично", "необхідно", "важливо", "неприпустимо", "історично",
            "фундаментально", "занепокоєння", "перемога", "збитки", "довіра",
            "безпрецедентно", "викликає", "критично", "надзвичайно",
            "шокуюча", "паніка", "приховували", "потрясла", "сенсація"
        },
        'en': {
            "ethically", "necessarily", "important", "unacceptable", "historically",
            "fundamentally", "concern", "victory", "losses", "trust",
            "unprecedented", "raises", "critical", "extremely",
            "shocking", "panic", "hidden", "sensational", "must"
        }
    }
    
    # Розширені signal markers (включаючи наукові терміни)
    SIGNAL_MARKERS = {
        'uk': {
            "якщо", "тоді", "тому", "внаслідок", "дорівнює", "факт",
            "ресурс", "чип", "наказ", "координати", "результат",
            "даних", "показник", "вимір", "кількість",
            # Наукові терміни
            "дослідження", "статистичний", "кореляція", "регресія",
            "аналіз", "респондентів", "вимірювання", "модель",
            "відсотків", "відсотки", "коефіцієнт"
        },
        'en': {
            "if", "then", "therefore", "consequently", "equals", "fact",
            "resource", "chip", "order", "coordinates", "result",
            "data", "metric", "measurement", "quantity",
            # Наукові терміни
            "research", "statistical", "correlation", "regression",
            "analysis", "respondents", "measured", "model",
            "percent", "percentage", "coefficient", "study",
            "indicates", "shows", "demonstrates", "calculated",
            # Економічні терміни
            "rate", "rates", "inflation", "eurozone", "bank",
            "points", "increase", "marking", "predict"
        }
    }
    
    CHAOS_MARKERS = {
        'uk': {
            "рептилоїди", "таємний", "змова", "плоска", "контролюють",
            "масони", "чіпування", "підземелля", "слонах"
        },
        'en': {
            "lizard", "reptilian", "magic", "conspiracy", "secret",
            "freemasons", "microchip", "underground", "flat earth"
        }
    }
    
    # Характерні букви для визначення мови
    UKRAINIAN_CHARS = set('їієґ')
    
    def detect_language(self, text: str) -> str:
        """
        Визначає мову тексту (uk або en)
        
        Args:
            text: Текст для аналізу
            
        Returns:
            'uk' або 'en'
        """
        text_lower = text.lower()
        
        # Перевірка на українські символи
        if any(char in text_lower for char in self.UKRAINIAN_CHARS):
            return 'uk'
        
        # Підрахунок Ukrainian vs English маркерів
        uk_score = sum(1 for marker in self.NOISE_MARKERS['uk'] if marker in text_lower)
        en_score = sum(1 for marker in self.NOISE_MARKERS['en'] if marker in text_lower)
        
        return 'uk' if uk_score > en_score else 'en'
    
    def get_markers(self, language: str = None, text: str = None) -> Dict[str, Set[str]]:
        """
        Повертає маркери для визначеної мови
        
        Args:
            language: 'uk' або 'en' (опціонально)
            text: Текст для автовизначення мови (якщо language не вказано)
            
        Returns:
            Dict з noise_markers, signal_markers, chaos_markers
        """
        if language is None and text is not None:
            language = self.detect_language(text)
        elif language is None:
            language = 'en'  # Default
        
        return {
            'noise_markers': self.NOISE_MARKERS.get(language, self.NOISE_MARKERS['en']),
            'signal_markers': self.SIGNAL_MARKERS.get(language, self.SIGNAL_MARKERS['en']),
            'chaos_markers': self.CHAOS_MARKERS.get(language, self.CHAOS_MARKERS['en'])
        }


class MultilingualVeritasCore:
    """
    Veritas Core з підтримкою множини мов (v2.0 - Calibrated)
    """
    
    def __init__(self, config: Dict = None):
        self.detector = LanguageDetector()
        self.reputation_registry = {
            "Unknown_Source": 0.5
        }
        
        # Налаштування thresholds (можна перевизначити через config)
        self.config = config or {}
        self.thresholds = self.config.get('thresholds', {
            'critical': 0.7,      # Було 0.6 - зробили суворіше
            'warning': 0.4,       # Було 0.4 - залишили
            'trusted': 0.2        # Новий поріг для TRUSTED
        })
        
        self.slashing = self.config.get('slashing', {
            'penalty_multiplier': 0.35,  # Було 0.4 - трохи м'якше
            'reward_bonus': 0.05
        })
    
    def _count_numbers(self, text: str) -> float:
        """
        Рахує числа в тексті як ознаку фактичності
        
        Args:
            text: Текст для аналізу
            
        Returns:
            float: Частка чисел відносно слів
        """
        numbers = re.findall(r'\d+\.?\d*', text)
        words = text.split()
        return len(numbers) / (len(words) + 1)
    
    def _count_caps_and_shouts(self, text: str) -> float:
        """
        Рахує КАПСЛОК та вигуки як ознаку маніпуляції
        
        Args:
            text: Текст для аналізу
            
        Returns:
            float: Shout factor
        """
        words = text.split()
        if not words:
            return 0.0
        
        # Вигуки
        exclamations = text.count('!')
        
        # КАПСЛОК слова (довжина > 2)
        caps_words = sum(1 for w in words if w.isupper() and len(w) > 2)
        
        # Питання (надмірна кількість)
        questions = text.count('?')
        
        shout_factor = (exclamations * 2 + caps_words * 3 + questions) / (len(words) + 1)
        return min(shout_factor, 1.0)
    
    def _calculate_entropy_coefficient(self, text: str, language: str = None) -> float:
        """
        Розрахунок ентропії з покращеною логікою (v2.0)
        
        Args:
            text: Текст для аналізу
            language: Мова ('uk' або 'en'), якщо None - автовизначення
            
        Returns:
            float: Індекс ентропії (0.0 - 1.0)
        """
        words = text.lower().replace(",", "").replace(".", "").split()
        if not words:
            return 1.0
        
        # Отримуємо маркери для відповідної мови
        markers = self.detector.get_markers(language=language, text=text)
        
        # 1. Перевірка на абсолютний хаос
        chaos_count = sum(1 for w in words if any(m in w for m in markers['chaos_markers']))
        if chaos_count > 0:
            return 0.99  # Максимальна ентропія
        
        # 2. Підрахунок шуму та сигналу
        noise_count = sum(1 for w in words if any(m in w for m in markers['noise_markers']))
        signal_count = sum(1 for w in words if any(m in w for m in markers['signal_markers']))
        
        # 3. Number Factor (цифри знижують ентропію)
        number_factor = self._count_numbers(text)
        
        # 4. Shout Factor (капслок і вигуки підвищують ентропію)
        shout_factor = self._count_caps_and_shouts(text)
        
        # 5. Базова ентропія
        base_entropy = (noise_count + 1) / (signal_count + noise_count + 1)
        
        # 6. Фінальна формула з урахуванням всіх факторів
        # - Цифри знижують ентропію
        # - Вигуки та КАПСЛОК підвищують ентропію
        final_entropy = base_entropy * (1 - number_factor * 0.3) + shout_factor * 0.4
        
        return round(min(max(final_entropy, 0.0), 0.999), 3)
    
    def evaluate_integrity(self, text: str, source: str, language: str = None) -> Dict:
        """
        Оцінка цілісності новини (v2.0)
        
        Args:
            text: Текст новини
            source: Джерело
            language: Мова (опціонально, автовизначення)
            
        Returns:
            Dict з результатами аналізу
        """
        # Визначаємо мову
        detected_lang = self.detector.detect_language(text) if language is None else language
        
        # Розрахунок ентропії
        entropy_score = self._calculate_entropy_coefficient(text, detected_lang)
        
        # Dynamic Slashing (з оновленими параметрами)
        penalty = 0.0
        if entropy_score > self.thresholds['warning']:
            penalty = round(entropy_score * self.slashing['penalty_multiplier'], 2)
        elif entropy_score < self.thresholds['trusted']:
            penalty = -self.slashing['reward_bonus']
        
        # Оновлення репутації
        current_rep = self.reputation_registry.get(source, 0.5)
        updated_rep = max(0.0, min(1.0, current_rep - penalty))
        self.reputation_registry[source] = round(updated_rep, 2)
        
        # Визначення статусу (з оновленими thresholds)
        status = self._get_status(entropy_score, updated_rep)
        
        return {
            "source": source,
            "language": detected_lang,
            "entropy_index": entropy_score,
            "reputation": updated_rep,
            "status": status,
            "verdict": self._get_verdict(entropy_score, detected_lang),
            "intervention_required": entropy_score >= self.thresholds['critical'] or updated_rep < 0.3,
            # Додаткова діагностика
            "diagnostics": {
                "number_factor": round(self._count_numbers(text), 3),
                "shout_factor": round(self._count_caps_and_shouts(text), 3)
            }
        }
    
    def _get_status(self, entropy: float, reputation: float) -> str:
        """Визначає статус на основі ентропії та репутації"""
        # Якщо ентропія критична - одразу CRITICAL
        if entropy >= self.thresholds['critical']:
            return "CRITICAL"
        
        # Інакше дивимось на репутацію
        if reputation >= 0.70:
            return "TRUSTED"
        elif reputation >= 0.50:
            return "SUCCESS"
        elif reputation >= 0.30:
            return "WARNING"
        else:
            return "CRITICAL"
    
    def _get_verdict(self, entropy: float, language: str) -> str:
        """Повертає вердикт мовою користувача"""
        verdicts = {
            'uk': {
                'excellent': "СТАБІЛЬНИЙ ЛОГІЧНИЙ СИГНАЛ",
                'good': "ПРИЙНЯТНА ЯКІСТЬ ІНФОРМАЦІЇ",
                'medium': "ПІДОЗРА НА РИТОРИЧНИЙ ШУМ",
                'high': "ВИСОКИЙ РІВЕНЬ МАНІПУЛЯЦІЇ",
                'critical': "КРИТИЧНА МАНІПУЛЯЦІЯ / ТОКСИЧНИЙ КОНТЕНТ"
            },
            'en': {
                'excellent': "STABLE LOGICAL SIGNAL",
                'good': "ACCEPTABLE INFORMATION QUALITY",
                'medium': "SUSPECTED RHETORICAL NOISE",
                'high': "HIGH LEVEL OF MANIPULATION",
                'critical': "CRITICAL MANIPULATION / TOXIC CONTENT"
            }
        }
        
        if entropy >= self.thresholds['critical']:
            level = 'critical'
        elif entropy >= 0.5:
            level = 'high'
        elif entropy >= self.thresholds['warning']:
            level = 'medium'
        elif entropy >= self.thresholds['trusted']:
            level = 'good'
        else:
            level = 'excellent'
        
        return verdicts.get(language, verdicts['en'])[level]


# Тестування
if __name__ == "__main__":
    analyzer = MultilingualVeritasCore()
    
    print("=== Тест 1: Наукова стаття ===")
    science_text = """У дослідженні взяли участь 2,847 респондентів віком від 18 до 65 років. 
    Статистичний аналіз показав кореляцію 0.73 (p<0.01) між змінними A та B."""
    result = analyzer.evaluate_integrity(science_text, "Science_Journal")
    print(f"Entropy: {result['entropy_index']}")
    print(f"Verdict: {result['verdict']}")
    print(f"Diagnostics: {result['diagnostics']}\n")
    
    print("=== Тест 2: BBC News ===")
    bbc_text = """The European Central Bank raised interest rates by 0.25 percentage points to 4.5%, 
    marking the tenth consecutive increase. Inflation in the eurozone reached 5.3% in March."""
    result = analyzer.evaluate_integrity(bbc_text, "BBC")
    print(f"Entropy: {result['entropy_index']}")
    print(f"Verdict: {result['verdict']}")
    print(f"Diagnostics: {result['diagnostics']}\n")
    
    print("=== Тест 3: Конспірологія ===")
    conspiracy = "Рептилоїди через масонську змову КОНТРОЛЮЮТЬ світ!!!"
    result = analyzer.evaluate_integrity(conspiracy, "Conspiracy")
    print(f"Entropy: {result['entropy_index']}")
    print(f"Verdict: {result['verdict']}")
    print(f"Diagnostics: {result['diagnostics']}")
