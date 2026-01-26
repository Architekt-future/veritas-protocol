"""
Veritas News Analyzer - Multilingual Support
Підтримка української та англійської мов
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
            "безпрецедентно", "викликає", "критично", "надзвичайно"
        },
        'en': {
            "ethically", "necessarily", "important", "unacceptable", "historically",
            "fundamentally", "concern", "victory", "losses", "trust",
            "unprecedented", "raises", "critical", "extremely"
        }
    }
    
    SIGNAL_MARKERS = {
        'uk': {
            "якщо", "тоді", "тому", "внаслідок", "дорівнює", "факт",
            "ресурс", "чип", "наказ", "координати", "результат",
            "даних", "показник", "вимір", "кількість"
        },
        'en': {
            "if", "then", "therefore", "consequently", "equals", "fact",
            "resource", "chip", "order", "coordinates", "result",
            "data", "metric", "measurement", "quantity"
        }
    }
    
    CHAOS_MARKERS = {
        'uk': {
            "рептилоїди", "таємний", "змова", "плоска", "контролюють",
            "масони", "чіпування", "підземелля"
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
    Veritas Core з підтримкою множини мов
    """
    
    def __init__(self):
        self.detector = LanguageDetector()
        self.reputation_registry = {
            "Unknown_Source": 0.5
        }
    
    def _calculate_entropy_coefficient(self, text: str, language: str = None) -> float:
        """
        Розрахунок ентропії з автовизначенням мови
        
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
        
        # Перевірка на абсолютний хаос
        if any(w in markers['chaos_markers'] for w in words):
            return 0.99
        
        # Підрахунок шуму та сигналу
        noise_count = sum(1 for w in words if w in markers['noise_markers'])
        signal_count = sum(1 for w in words if w in markers['signal_markers'])
        
        laminar_index = (signal_count + 1) / (noise_count + signal_count + 1)
        return round(1.0 - laminar_index, 3)
    
    def evaluate_integrity(self, text: str, source: str, language: str = None) -> Dict:
        """
        Оцінка цілісності новини
        
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
        
        # Dynamic Slashing
        penalty = 0.0
        if entropy_score > 0.4:
            penalty = round(entropy_score * 0.4, 2)
        elif entropy_score < 0.2:
            penalty = -0.05
        
        # Оновлення репутації
        current_rep = self.reputation_registry.get(source, 0.5)
        updated_rep = max(0.0, min(1.0, current_rep - penalty))
        self.reputation_registry[source] = round(updated_rep, 2)
        
        # Визначення статусу
        status = self._get_status(updated_rep)
        
        return {
            "source": source,
            "language": detected_lang,
            "entropy_index": entropy_score,
            "reputation": updated_rep,
            "status": status,
            "verdict": self._get_verdict(entropy_score, detected_lang),
            "intervention_required": updated_rep < 0.3
        }
    
    def _get_status(self, reputation: float) -> str:
        """Визначає статус на основі репутації"""
        if reputation >= 0.85:
            return "TRUSTED"
        elif reputation >= 0.60:
            return "MONITORED"
        elif reputation >= 0.40:
            return "WARNING"
        else:
            return "REJECTED"
    
    def _get_verdict(self, entropy: float, language: str) -> str:
        """Повертає вердикт мовою користувача"""
        verdicts = {
            'uk': {
                'low': "Високоякісний логічний сигнал",
                'medium': "Помірна кількість риторики",
                'high': "Високий рівень демагогії",
                'chaos': "Виявлено конспірологічний контент"
            },
            'en': {
                'low': "High-quality logical signal",
                'medium': "Moderate amount of rhetoric",
                'high': "High level of demagoguery",
                'chaos': "Conspiracy content detected"
            }
        }
        
        if entropy >= 0.99:
            level = 'chaos'
        elif entropy > 0.6:
            level = 'high'
        elif entropy > 0.3:
            level = 'medium'
        else:
            level = 'low'
        
        return verdicts.get(language, verdicts['en'])[level]


# Тестування
if __name__ == "__main__":
    analyzer = MultilingualVeritasCore()
    
    # Тест українською
    uk_text = "Історично необхідно етично занепокоїтися через фундаментальну втрату довіри."
    uk_result = analyzer.evaluate_integrity(uk_text, "TestSource_UK")
    
    print("=== Ukrainian Test ===")
    print(f"Language: {uk_result['language']}")
    print(f"Entropy: {uk_result['entropy_index']}")
    print(f"Verdict: {uk_result['verdict']}")
    print(f"Status: {uk_result['status']}\n")
    
    # Тест англійською
    en_text = "If chips are blocked, then the result equals zero."
    en_result = analyzer.evaluate_integrity(en_text, "TestSource_EN")
    
    print("=== English Test ===")
    print(f"Language: {en_result['language']}")
    print(f"Entropy: {en_result['entropy_index']}")
    print(f"Verdict: {en_result['verdict']}")
    print(f"Status: {en_result['status']}\n")
    
    # Тест конспірології
    conspiracy_text = "Рептилоїди таємно контролюють світ через масонську змову."
    con_result = analyzer.evaluate_integrity(conspiracy_text, "Conspiracy_Source")
    
    print("=== Conspiracy Test ===")
    print(f"Language: {con_result['language']}")
    print(f"Entropy: {con_result['entropy_index']}")
    print(f"Verdict: {con_result['verdict']}")
    print(f"Status: {con_result['status']}")
