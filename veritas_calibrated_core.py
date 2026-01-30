"""
Veritas Protocol - Veritas Calibrated Core (FIXED v2)
FIXED: Class name changed to VeritasCalibratedEngine to match api/analyze.py import
FIXED: Substring matching for sanity check
"""

import math
import re
from typing import Dict, Optional


class VeritasCalibratedEngine:  # ← FIXED CLASS NAME!
    """
    Комбінований движок аналізу інформаційної ентропії
    FIXED: Substring matching для виявлення словоформ
    """
    
    def __init__(self):
        self.thresholds = {
            'trusted': 0.35,
            'acceptable': 0.55,
            'suspicious': 0.75,
            'critical': 0.85
        }
        
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
        
        self.chaos_markers = {
            'uk': {
                'рептилоїд', 'таємн', 'змов', 'плоск', 'контролю',
                'масон', 'чіпува', 'підземелл', 'ілюмінат', 'глобаліст'
            },
            'en': {
                'lizard', 'reptilian', 'conspiracy', 'secret',
                'freemason', 'microchip', 'underground', 'flat earth',
                'illuminati', 'globalist'
            }
        }
        
        # FIXED: Розширені кластери з substring matching
        self.incompatible_clusters = [
            {
                'квантов', 'борщ', 'зажарк', 'каструл', 'ложк',
                'quantum', 'soup', 'spoon', 'pot', 'kitchen',
                'синхрофазотрон', 'резонанс', 'вакуум',
                'огірк', 'кріп', 'їж', 'вечер', 'закипа'
            },
            {
                'астральн', 'карм', 'вібрац', 'метафізичн',
                'енерг', 'чакр', 'всесвіт', 'парадигм',
                'astral', 'karma', 'vibration', 'metaphysic'
            },
            {
                'транзакц', 'дискретн', 'ентроп', 'модел',
                'фазотрон', 'квант', 'побут', 'кухн', 'готув'
            },
            {
                'магі', 'криптовалют', 'блокчейн', 'сметан',
                'magic', 'crypto', 'blockchain', 'cream'
            }
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
        
        normalized = min(1.0, entropy / 8.0)
        return normalized

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
        
        return {
            'noise': noise_count,
            'signal': signal_count,
            'chaos': chaos_count
        }

    def _check_sanity(self, words: list) -> float:
        """FIXED: Substring matching для виявлення словоформ"""
        words_lower = [w.lower() for w in words]
        
        for cluster in self.incompatible_clusters:
            match_count = 0
            
            for word in words_lower:
                for pattern in cluster:
                    if pattern in word or word in pattern:
                        match_count += 1
                        break
            
            if match_count >= 2:
                return 0.9
        
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
        """ГОЛОВНИЙ МЕТОД АНАЛІЗУ"""
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
        
        if markers['chaos'] > 0:
            return {
                'entropy': 0.99,
                'status': 'CRITICAL',
                'verdict': 'КОНСПІРОЛОГІЯ / CHAOS DETECTED',
                'language': lang.upper(),
                'diagnostics': {
                    'chaos_markers': markers['chaos'],
                    'shannon_entropy': round(shannon, 3),
                    'sanity_penalty': round(sanity_penalty, 3),
                    'word_count': word_count
                }
            }
        
        base_entropy = (shannon * 0.6) + (complexity * 0.4)
        
        if markers['signal'] + markers['noise'] > 0:
            marker_ratio = markers['noise'] / (markers['signal'] + markers['noise'] + 1)
            base_entropy = (base_entropy * 0.7) + (marker_ratio * 0.3)
        
        base_entropy *= (1.0 - number_density * 0.25)
        base_entropy += shout_factor * 0.15
        base_entropy += sanity_penalty * 0.3
        
        final_entropy = min(0.99, max(0.0, base_entropy))
        
        if (markers['signal'] > markers['noise'] * 2 and 
            number_density > 0.05 and 
            shout_factor < 0.1 and
            sanity_penalty == 0.0):
            final_entropy *= 0.75
        
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
                'sanity_violations': sanity_penalty > 0,
                'word_count': word_count,
                'char_count': len(text)
            }
        }
