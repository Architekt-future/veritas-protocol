"""
Veritas Protocol - Calibrated Core Engine (FIXED v3)
Inspired by Orpheus LAC principles:
- Weighted scoring (not binary)
- Density-based detection (not count)
- Configurable thresholds
- Academic context awareness
"""

import math
import re
from typing import Dict, Optional

class VeritasCalibratedCore:
    """Calibrated entropy analysis with weighted scoring"""

    def __init__(self):
        # Configurable thresholds
        self.thresholds = {
            'trusted': 0.35,
            'acceptable': 0.55,
            'suspicious': 0.75,
            'critical': 0.85
        }

        # Configurable weights (Orpheus style)
        self.weights = {
            'shannon': 0.25,
            'complexity': 0.15,
            'noise_signal_ratio': 0.20,
            'chaos_density': 0.15,
            'sanity_violation': 0.15,
            'shout_factor': 0.10
        }

        # Configurable chaos threshold
        self.chaos_density_threshold = 0.05  # 5% of text

        self.noise_markers = {
            'uk': {
                'етично', 'необхідно', 'важливо', 'неприпустимо', 'історично',
                'фундаментально', 'занепокоєння', 'перемога', 'збитки', 'довіра',
                'шокуюча', 'паніка', 'приховували', 'потрясла', 'сенсація', 'терміново'
            },
            'en': {
                'ethically', 'necessarily', 'important', 'unacceptable', 'historically',
                'fundamentally', 'concern', 'victory', 'losses', 'trust',
                'shocking', 'panic', 'hidden', 'sensational', 'must', 'urgent'
            }
        }

        self.signal_markers = {
            'uk': {
                'якщо', 'тоді', 'тому', 'внаслідок', 'дорівнює', 'факт',
                'даних', 'показник', 'вимір', 'кількість', 'дослідження',
                'статистичний', 'кореляція', 'регресія', 'аналіз', 'респондентів',
                'метод', 'експеримент', 'гіпотеза', 'вибірка'
            },
            'en': {
                'if', 'then', 'therefore', 'consequently', 'equals', 'fact',
                'data', 'metric', 'measurement', 'quantity', 'research',
                'statistical', 'correlation', 'regression', 'analysis', 'study',
                'method', 'experiment', 'hypothesis', 'sample', 'respondents'
            }
        }

        # Academic indicators - РОЗШИРЕНО
        self.academic_markers = {
            'uk': {
                'дослідження', 'аналіз', 'метод', 'експеримент', 'гіпотеза',
                'респондент', 'статистичн', 'кореляц', 'регрес', 'вибірк',
                'науков', 'публікац', 'журнал', 'конференц', 'протокол',
                'архітектур', 'систем', 'алгоритм', 'модель', 'теорі',
                'практичн', 'результат', 'висновок', 'апроксимаці', 'синтез',
                'верифікац', 'калібровка', 'детермінізм', 'ентропі', 'вердикт',
                'категорі', 'таксономі', 'епістемолог', 'семантичн'
            },
            'en': {
                'research', 'study', 'analysis', 'method', 'experiment',
                'hypothesis', 'respondent', 'statistical', 'correlation',
                'regression', 'sample', 'scientific', 'publication', 'journal',
                'conference', 'protocol', 'architecture', 'system', 'algorithm',
                'model', 'theory', 'practice', 'result', 'conclusion',
                'approximation', 'synthesis', 'verification', 'calibration',
                'determinism', 'entropy', 'verdict', 'category', 'taxonomy',
                'epistemological', 'semantic'
            }
        }

        # FIXED: Only REAL conspiracy/pseudoscience
        self.chaos_markers = {
            'uk': {
                'рептилоїд', 'масон', 'чіпува', 'плоскоземель', 'плоск', 
                'ілюмінат', 'глобаліст', 'світова змова', 'заговір', 'інопланетн',
                'нібіру', 'анунак', 'хаос', 'дезорієнтац', 'маніпуляц'
            },
            'en': {
                'lizard', 'reptilian', 'freemason', 'flat earth', 'illuminati',
                'globalist', 'new world order', 'microchip implant', 'alien',
                'nibiru', 'annunaki', 'chaos', 'disorientation', 'manipulation'
            }
        }

        # РОЗШИРЕНО: More incompatible clusters
        self.incompatible_clusters = [
            {'квантов', 'борщ', 'каструл', 'зажарк', 'ложк', 'кухн', 'буряк', 'сметан', 'суп'},
            {'рептилоїд', 'масон', 'змов', 'контролю', 'таємн', 'прибулець'},
            {'астральн', 'карм', 'чакр', 'вібрац', 'енерг', 'біопол', 'мультивсесвіт'},
            {'глобальн', 'дестабілізац', 'когнітив', 'поле', 'резонанс', 'нелокальн'},
            {'планк', 'гейзенберг', 'вакуум', 'флуктуац', 'тунель', 'ефект', 'шлунок'}
        ]

    def detect_language(self, text: str) -> str:
        ukrainian_chars = re.findall(r'[їієґ]', text.lower())
        return 'uk' if len(ukrainian_chars) > 3 else 'en'

    def _shannon_entropy(self, text: str) -> float:
        if not text:
            return 0.0
        char_freq = {}
        for char in text:
            char_freq[char] = char_freq.get(char, 0) + 1
        entropy = 0.0
        text_len = len(text)
        for count in char_freq.values():
            p = count / text_len
            if p > 0:
                entropy -= p * math.log2(p)
        return min(1.0, entropy / 8.0)

    def _calculate_complexity(self, text: str) -> float:
        words = re.findall(r'\w+', text.lower())
        if not words:
            return 1.0
        unique_words = len(set(words))
        total_words = len(words)
        diversity = unique_words / total_words
        complexity = 1.0 - diversity
        if total_words > 500 and complexity > 0.6:
            complexity *= 0.7
        return complexity

    def _count_markers(self, words: list, lang: str) -> Dict:
        noise_count = 0
        signal_count = 0
        chaos_count = 0
        academic_count = 0

        for word in words:
            word_lower = word.lower()
            for marker in self.noise_markers.get(lang, set()):
                if marker in word_lower:
                    noise_count += 1
                    break
            for marker in self.signal_markers.get(lang, set()):
                if marker in word_lower:
                    signal_count += 1
                    break
            for marker in self.chaos_markers.get(lang, set()):
                if marker in word_lower or word_lower in marker:
                    chaos_count += 1
                    break
            for marker in self.academic_markers.get(lang, set()):
                if marker in word_lower:
                    academic_count += 1
                    break

        return {
            'noise': noise_count,
            'signal': signal_count,
            'chaos': chaos_count,
            'academic': academic_count
        }

    def _check_sanity(self, words: list) -> float:
        words_lower = [w.lower() for w in words]
        for cluster in self.incompatible_clusters:
            match_count = 0
            for word in words_lower:
                for pattern in cluster:
                    if pattern in word or word in pattern:
                        match_count += 1
                        break
            if match_count >= 2:
                return 0.9  # HIGH sanity penalty for obvious nonsense
        return 0.0

    def _calculate_number_density(self, text: str, word_count: int) -> float:
        if word_count == 0:
            return 0.0
        numbers = re.findall(r'\d+\.?\d*', text)
        return len(numbers) / (word_count + 1)

    def _calculate_shout_factor(self, text: str, word_count: int) -> float:
        if word_count == 0:
            return 0.0
        caps_words = len([w for w in text.split() if w.isupper() and len(w) > 5])
        exclamations = text.count('!')
        questions = text.count('?')
        shout = (exclamations * 2 + caps_words * 3 + questions) / (word_count + 1)
        return min(shout, 1.0)

    def analyze(self, text: str) -> Dict:
        """MAIN ANALYSIS (FIXED with Orpheus principles)"""
        if not text or len(text.strip()) < 10:
            return {'error': 'Text too short'}

        lang = self.detect_language(text)
        words = re.findall(r'\w+', text.lower())
        word_count = len(words)

        shannon = self._shannon_entropy(text)
        complexity = self._calculate_complexity(text)
        markers = self._count_markers(words, lang)
        sanity_penalty = self._check_sanity(words)
        number_density = self._calculate_number_density(text, word_count)
        shout_factor = self._calculate_shout_factor(text, word_count)

        # FIXED: Density-based chaos
        chaos_density = markers['chaos'] / word_count if word_count > 0 else 0

        # Academic context - ПОЛІПШЕНА логіка
        academic_density = markers['academic'] / word_count if word_count > 0 else 0
        # Визначаємо академічність за кількома критеріями
        is_academic = False
        if academic_density > 0.01:  # Знижений поріг з 0.03 до 0.01
            is_academic = True
        elif markers['academic'] > 8:  # Або якщо багато академічних слів
            is_academic = True
        elif markers['signal'] > 50 and complexity < 0.6:  # Багато сигнальних слів + низька складність
            is_academic = True

        # Noise/signal ratio
        if markers['signal'] + markers['noise'] > 0:
            noise_signal_ratio = markers['noise'] / (markers['signal'] + markers['noise'] + 1)
        else:
            noise_signal_ratio = 0.5

        # === WEIGHTED SCORING (Orpheus) ===
        components = {
            'shannon': shannon,
            'complexity': complexity,
            'noise_signal_ratio': noise_signal_ratio,
            'chaos_density': chaos_density,
            'sanity_violation': sanity_penalty,
            'shout_factor': shout_factor
        }

        base_entropy = sum(components[key] * self.weights[key] for key in components.keys())
        base_entropy *= (1.0 - number_density * 0.25)

        # Academic correction
        if is_academic:
            base_entropy *= 0.6

        final_entropy = min(0.99, max(0.0, base_entropy))

        # Verdict
        if final_entropy < self.thresholds['trusted']:
            status, verdict = 'TRUSTED', 'СТАБІЛЬНИЙ ЛОГІЧНИЙ СИГНАЛ'
        elif final_entropy < self.thresholds['acceptable']:
            status, verdict = 'ACCEPTABLE', 'ПРИЙНЯТНА СТРУКТУРОВАНА ІНФОРМАЦІЯ'
        elif final_entropy < self.thresholds['suspicious']:
            status, verdict = 'SUSPICIOUS', 'ПІДОЗРІЛА ЕМОЦІЙНА РИТОРИКА'
        elif final_entropy < self.thresholds['critical']:
            status, verdict = 'WARNING', 'ВИСОКИЙ РІВЕНЬ МАНІПУЛЯЦІЇ'
        else:
            status, verdict = 'CRITICAL', 'КРИТИЧНИЙ ІНФОРМАЦІЙНИЙ ХАОС'

        # УЗГОДЖЕНІ КЛЮЧІ для diagnostics (важливо для фронтенду)
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
                'chaos_density': round(chaos_density, 4),
                'academic_markers': markers['academic'],
                'academic_density': round(academic_density, 4),
                'is_academic_context': is_academic,
                'number_density': round(number_density, 3),
                'shout_factor': round(shout_factor, 3),
                'sanity_penalty': round(sanity_penalty, 3),
                'sanity_violations': sanity_penalty > 0,
                'word_count': word_count,
                'char_count': len(text)
            }
        }
