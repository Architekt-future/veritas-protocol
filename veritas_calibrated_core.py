"""
Veritas Protocol - Calibrated Core Engine
Synthesized from veritas_core.py + app/core.py
Optimized for: Academic < 0.4, Wikipedia 0.5-0.65, Propaganda 0.85+
"""

import math
import re
from typing import Dict, Optional


class VeritasCalibratedEngine:
    """
    Комбінований движок аналізу інформаційної ентропії
    Синтез Shannon entropy + markers + sanity checks
    """
    
    def __init__(self):
        # Калібровані пороги
        self.thresholds = {
            'trusted': 0.35,      # Academic papers, pure logic
            'acceptable': 0.55,   # Wikipedia, structured content
            'suspicious': 0.75,   # Emotional rhetoric
            'critical': 0.85      # Propaganda, chaos
        }
        
        # Маркери шуму (емоційна риторика)
        self.noise_markers = {
            'uk': {
                'етично', 'необхідно', 'важливо', 'неприпустимо', 'історично',
                'фундаментально', 'занепокоєння', 'перемога', 'збитки', 'довіра',
                'шокуюча', 'паніка', 'приховували', 'потрясла', 'сенсація', 'терміново',
                'критично', 'безпрецедентно', 'катастрофа'
            },
            'en': {
                'ethically', 'necessarily', 'important', 'unacceptable', 'historically',
                'fundamentally', 'concern', 'victory', 'losses', 'trust',
                'shocking', 'panic', 'hidden', 'sensational', 'must', 'urgent',
                'unprecedented', 'catastrophic', 'critical'
            }
        }
        
        # Маркери сигналу (логічні зв'язки)
        self.signal_markers = {
            'uk': {
                'якщо', 'тоді', 'тому', 'внаслідок', 'дорівнює', 'факт',
                'ресурс', 'чип', 'наказ', 'координати', 'результат',
                'даних', 'показник', 'вимір', 'кількість', 'дослідження',
                'статистичний', 'кореляція', 'регресія', 'аналіз', 'респондентів',
                'відсоток', 'індекс', 'коефіцієнт', 'середній', 'медіана',
                'гіпотеза', 'метод', 'експеримент', 'вибірка'
            },
            'en': {
                'if', 'then', 'therefore', 'consequently', 'equals', 'fact',
                'resource', 'chip', 'order', 'coordinates', 'result',
                'data', 'metric', 'measurement', 'quantity', 'research',
                'statistical', 'correlation', 'regression', 'analysis', 'study',
                'rate', 'inflation', 'percentage', 'indicates', 'shows',
                'index', 'coefficient', 'average', 'median', 'respondents',
                'hypothesis', 'method', 'experiment', 'sample'
            }
        }
        
        # Маркери хаосу (конспірологія)
        self.chaos_markers = {
            'uk': {
                'рептилоїди', 'таємний', 'змова', 'плоска', 'контролюють',
                'масони', 'чіпування', 'підземелля', 'на слонах', 'ілюмінати',
                'глобалісти', 'світова змова', 'заговір'
            },
            'en': {
                'lizard', 'reptilian', 'magic', 'conspiracy', 'secret',
                'freemasons', 'microchip', 'underground', 'flat earth',
                'illuminati', 'globalists', 'new world order'
            }
        }
        
        # Sanity check: несумісні кластери (борщовий колапс)
        self.incompatible_clusters = [
            {'квантовий', 'борщ', 'зажарка', '5G', 'quantum', 'soup'},
            {'магія', 'криптовалюта', 'сметана', 'magic', 'crypto', 'blockchain'}
        ]

    def detect_language(self, text: str) -> str:
        """Визначення мови тексту"""
        ukrainian_chars = re.findall(r'[їієґ]', text.lower())
        return 'uk' if len(ukrainian_chars) > 3 else 'en'

    def _shannon_entropy(self, text: str) -> float:
        """
        Розрахунок ентропії Шеннона
        Вимірює інформаційну випадковість на рівні символів
        """
        if not text:
            return 0.0
        
        # Частоти символів
        char_freq = {}
        for char in text:
            char_freq[char] = char_freq.get(char, 0) + 1
        
        # Shannon entropy: H = -Σ(p_i * log2(p_i))
        entropy = 0.0
        text_len = len(text)
        
        for count in char_freq.values():
            p = count / text_len
            if p > 0:
                entropy -= p * math.log2(p)
        
        # Нормалізація до 0-1 (max entropy для ASCII ≈ 8 bits)
        normalized = min(1.0, entropy / 8.0)
        
        return normalized

    def _calculate_complexity(self, text: str) -> float:
        """
        Linguistic complexity (vocabulary diversity)
        Низька різноманітність = висока складність (repetitive)
        """
        words = re.findall(r'\w+', text.lower())
        if not words:
            return 1.0
        
        unique_words = len(set(words))
        total_words = len(words)
        
        # Vocabulary diversity ratio
        diversity = unique_words / total_words
        
        # Інвертуємо: низька різноманітність = висока складність
        # Але для академічних текстів це нормально (спеціалізована термінологія)
        complexity = 1.0 - diversity
        
        # Корекція: якщо текст довгий і repetitive - це може бути ознака структурованості
        # а не маніпуляції (академічні тексти часто повторюють терміни)
        if total_words > 500 and complexity > 0.6:
            complexity *= 0.7  # Пом'якшення для довгих текстів
        
        return complexity

    def _count_markers(self, words: list, lang: str) -> Dict:
        """Підрахунок маркерів шуму/сигналу/хаосу"""
        noise_count = sum(1 for w in words if w in self.noise_markers.get(lang, set()))
        signal_count = sum(1 for w in words if w in self.signal_markers.get(lang, set()))
        chaos_count = sum(1 for w in words if w in self.chaos_markers.get(lang, set()))
        
        return {
            'noise': noise_count,
            'signal': signal_count,
            'chaos': chaos_count
        }

    def _check_sanity(self, words: list) -> float:
        """
        Sanity check: виявлення несумісних концептів
        Returns: 0.0 (sane) to 1.0 (insane)
        """
        word_set = set(words)
        
        for cluster in self.incompatible_clusters:
            matches = cluster & word_set
            if len(matches) >= 2:
                # Знайдено 2+ несумісні концепти
                return 0.9  # Високий sanity penalty
        
        return 0.0  # Все нормально

    def _calculate_number_density(self, text: str, word_count: int) -> float:
        """
        Number density: наявність цифр/статистики
        Високий number density знижує ентропію (факти, дані)
        """
        if word_count == 0:
            return 0.0
        
        numbers = re.findall(r'\d+\.?\d*', text)
        return len(numbers) / (word_count + 1)

    def _calculate_shout_factor(self, text: str, word_count: int) -> float:
        """
        Shout factor: КАПС, знаки оклику
        Високий shout factor підвищує ентропію (емоційна маніпуляція)
        """
        if word_count == 0:
            return 0.0
        
        # CAPS words (>5 chars щоб не чіпати абревіатури)
        caps_words = len([w for w in text.split() if w.isupper() and len(w) > 5])
        
        # Exclamations
        exclamations = text.count('!')
        questions = text.count('?')
        
        shout = (exclamations * 2 + caps_words * 3 + questions) / (word_count + 1)
        
        return min(shout, 1.0)

    def analyze(self, text: str) -> Dict:
        """
        ГОЛОВНИЙ МЕТОД АНАЛІЗУ
        
        Синтезує всі фактори:
        - Shannon entropy (mathematical)
        - Complexity (linguistic)
        - Markers (pattern detection)
        - Sanity (conceptual coherence)
        - Number density (factuality)
        - Shout factor (emotional manipulation)
        
        Returns comprehensive analysis
        """
        if not text or len(text.strip()) < 10:
            return {'error': 'Text too short'}
        
        # Базова обробка
        lang = self.detect_language(text)
        words = re.findall(r'\w+', text.lower())
        word_count = len(words)
        
        # 1. Shannon entropy (0-1)
        shannon = self._shannon_entropy(text)
        
        # 2. Complexity (0-1)
        complexity = self._calculate_complexity(text)
        
        # 3. Markers
        markers = self._count_markers(words, lang)
        
        # 4. Sanity check
        sanity_penalty = self._check_sanity(words)
        
        # 5. Number density (knowledge-reducing factor)
        number_density = self._calculate_number_density(text, word_count)
        
        # 6. Shout factor (entropy-increasing factor)
        shout_factor = self._calculate_shout_factor(text, word_count)
        
        # === INSTANT CHAOS CHECK ===
        if markers['chaos'] > 0:
            return {
                'entropy': 0.99,
                'status': 'CRITICAL',
                'verdict': 'КОНСПІРОЛОГІЯ / CHAOS DETECTED',
                'language': lang.upper(),
                'diagnostics': {
                    'chaos_markers': markers['chaos'],
                    'shannon_entropy': round(shannon, 3),
                    'word_count': word_count
                }
            }
        
        # === СИНТЕЗ ЕНТРОПІЇ ===
        
        # Base: Shannon (0.6 weight) + Complexity (0.4 weight)
        # Але для академічних текстів complexity не є проблемою
        base_entropy = (shannon * 0.6) + (complexity * 0.4)
        
        # Marker ratio (noise vs signal)
        if markers['signal'] + markers['noise'] > 0:
            marker_ratio = markers['noise'] / (markers['signal'] + markers['noise'] + 1)
            # Змішуємо з base
            base_entropy = (base_entropy * 0.7) + (marker_ratio * 0.3)
        
        # Number density: більше цифр = менше ентропії
        base_entropy *= (1.0 - number_density * 0.25)
        
        # Shout factor: більше крику = більше ентропії
        base_entropy += shout_factor * 0.15
        
        # Sanity penalty
        base_entropy += sanity_penalty * 0.3
        
        # Фінальне обмеження
        final_entropy = min(0.99, max(0.0, base_entropy))
        
        # === КАЛІБРУВАННЯ РЕЗУЛЬТАТУ ===
        # Спеціальна корекція для академічних текстів
        if (markers['signal'] > markers['noise'] * 2 and 
            number_density > 0.05 and 
            shout_factor < 0.1):
            # Це схоже на академічний текст
            final_entropy *= 0.75  # Знижуємо ентропію на 25%
        
        # === ВИЗНАЧЕННЯ СТАТУСУ ===
        if final_entropy < self.thresholds['trusted']:
            status = 'TRUSTED'
            verdict = 'СТАБІЛЬНИЙ ЛОГІЧНИЙ СИГНАЛ'
        elif final_entropy < self.thresholds['acceptable']:
            status = 'ACCEPTABLE'
            verdict = 'ПРИЙНЯТНА СТРУКТУРОВАНА ІНФОРМАЦІЯ'
        elif final_entropy < self.thresholds['suspicious']:
            status = 'SUSPICIOUS'
            verdict = 'ПІДОЗРІЛА ЕМОЦІЙНА РИТОРИКА'
        elif final_entropy < self.thresholds['critical']:
            status = 'WARNING'
            verdict = 'ВИСОКИЙ РІВЕНЬ МАНІПУЛЯЦІЇ'
        else:
            status = 'CRITICAL'
            verdict = 'КРИТИЧНИЙ ІНФОРМАЦІЙНИЙ ХАОС'
        
        return {
            'entropy': round(final_entropy, 3),
            'status': status,
            'verdict': verdict,
            'language': lang.upper(),
            'diagnostics': {
                'shannon_entropy': round(shannon, 3),
                'complexity': round(complexity, 3),
                'noise_markers': markers['noise'],
                'signal_markers': markers['signal'],
                'chaos_markers': markers['chaos'],
                'number_density': round(number_density, 3),
                'shout_factor': round(shout_factor, 3),
                'sanity_penalty': round(sanity_penalty, 3),
                'word_count': word_count,
                'char_count': len(text)
            }
        }


# Standalone testing
if __name__ == "__main__":
    engine = VeritasCalibratedEngine()
    
    # Test 1: Academic text
    academic = """
    У дослідженні взяли участь 2,847 респондентів віком від 18 до 65 років.
    Статистичний аналіз показав кореляцію 0.73 (p<0.01) між змінними A та B.
    Методологія дослідження базувалася на регресійному аналізі з контролем 
    додаткових факторів. Результати вказують на значущий зв'язок між показниками.
    """
    
    result1 = engine.analyze(academic)
    print(f"Academic text: entropy={result1['entropy']}, status={result1['status']}")
    
    # Test 2: Propaganda
    propaganda = """
    ІСТОРИЧНО ВАЖЛИВО!!! Етично неприпустимо ігнорувати цю КРИТИЧНУ ситуацію!
    Необхідно ТЕРМІНОВО діяти! Паніка і занепокоєння зростають! КАТАСТРОФА!!!
    """
    
    result2 = engine.analyze(propaganda)
    print(f"Propaganda: entropy={result2['entropy']}, status={result2['status']}")
    
    # Test 3: Conspiracy
    conspiracy = """
    Рептилоїди через масонську змову контролюють світову економіку.
    Таємні сили планують чіпування населення через 5G мережі.
    """
    
    result3 = engine.analyze(conspiracy)
    print(f"Conspiracy: entropy={result3['entropy']}, status={result3['status']}")
