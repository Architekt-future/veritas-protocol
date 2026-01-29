"""
Veritas Protocol - Veritas Calibrated Core (FIXED)
Synthesized from veritas_core.py + app/core.py
FIXED: Improved sanity check with substring matching for word variations
"""

import math
import re
from typing import Dict, Optional


class VeritasCalibratedCore:
    """
    Комбінований движок аналізу інформаційної ентропії
    Синтез Shannon entropy + markers + sanity checks
    FIXED: Substring matching для виявлення словоформ (борщ/борщу/борщем)
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
                'рептилоїд', 'таємн', 'змов', 'плоск', 'контролю',
                'масон', 'чіпува', 'підземелл', 'на слонах', 'ілюмінат',
                'глобаліст', 'світова змова', 'заговір'
            },
            'en': {
                'lizard', 'reptilian', 'magic', 'conspiracy', 'secret',
                'freemason', 'microchip', 'underground', 'flat earth',
                'illuminati', 'globalist', 'new world order'
            }
        }
        
        # FIXED: Розширені sanity кластери з stems для substring matching
        self.incompatible_clusters = [
            # Квантова кулінарія (борщовий колапс)
            {
                'квантов', 'борщ', 'зажарк', 'каструл', 'ложк',
                'quantum', 'soup', 'spoon', 'pot', 'kitchen',
                'синхрофазотрон', 'резонанс', 'вакуум',
                'огірк', 'кріп', 'їж', 'вечер', 'закипа'
            },
            
            # Езотерична фізика їжі
            {
                'астральн', 'карм', 'вібрац', 'метафізичн',
                'енерг', 'чакр', 'всесвіт', 'парадигм',
                'astral', 'karma', 'vibration', 'metaphysic',
                'energy', 'chakra', 'universe', 'paradigm'
            },
            
            # Наукова термінологія в побуті
            {
                'транзакц', 'дискретн', 'ентроп', 'модел',
                'фазотрон', 'реактор', 'квант',
                'побут', 'кухн', 'їж', 'готув'
            },
            
            # Крипто-магія
            {
                'магі', 'криптовалют', 'блокчейн', 'сметан',
                'magic', 'crypto', 'blockchain', 'cream'
            }
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
        complexity = 1.0 - diversity
        
        # Корекція для довгих академічних текстів
        if total_words > 500 and complexity > 0.6:
            complexity *= 0.7
        
        return complexity

    def _count_markers(self, words: list, lang: str) -> Dict:
        """Підрахунок маркерів шуму/сигналу/хаосу з substring matching"""
        noise_count = 0
        signal_count = 0
        chaos_count = 0
        
        # Для кожного слова перевіряємо чи містить маркер (substring)
        for word in words:
            word_lower = word.lower()
            
            # Noise markers
            for marker in self.noise_markers.get(lang, set()):
                if marker in word_lower:
                    noise_count += 1
                    break
            
            # Signal markers
            for marker in self.signal_markers.get(lang, set()):
                if marker in word_lower:
                    signal_count += 1
                    break
            
            # Chaos markers (substring match)
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
        """
        FIXED: Sanity check з substring matching
        Виявляє несумісні концепти навіть у різних словоформах
        
        Returns: 0.0 (sane) to 1.0 (insane)
        """
        words_lower = [w.lower() for w in words]
        
        for cluster in self.incompatible_clusters:
            match_count = 0
            matched_patterns = []
            
            for word in words_lower:
                for pattern in cluster:
                    # FIXED: Substring matching (pattern in word OR word in pattern)
                    if pattern in word or word in pattern:
                        match_count += 1
                        matched_patterns.append(f"{word}~{pattern}")
                        break  # Count each word only once per cluster
            
            # Якщо знайдено 2+ несумісні концепти
            if match_count >= 2:
                # Debug info (можна видалити в production)
                # print(f"SANITY VIOLATION: {match_count} matches - {matched_patterns[:5]}")
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
        
        Синтезує всі фактори з FIXED sanity check
        """
        if not text or len(text.strip()) < 10:
            return {'error': 'Text too short'}
        
        # Базова обробка
        lang = self.detect_language(text)
        words = re.findall(r'\w+', text.lower())
        word_count = len(words)
        
        # 1. Shannon entropy
        shannon = self._shannon_entropy(text)
        
        # 2. Complexity
        complexity = self._calculate_complexity(text)
        
        # 3. Markers (з substring matching)
        markers = self._count_markers(words, lang)
        
        # 4. FIXED: Sanity check (з substring matching)
        sanity_penalty = self._check_sanity(words)
        
        # 5. Number density
        number_density = self._calculate_number_density(text, word_count)
        
        # 6. Shout factor
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
                    'word_count': word_count,
                    'sanity_penalty': round(sanity_penalty, 3)
                }
            }
        
        # === СИНТЕЗ ЕНТРОПІЇ ===
        
        # Base: Shannon + Complexity
        base_entropy = (shannon * 0.6) + (complexity * 0.4)
        
        # Marker ratio
        if markers['signal'] + markers['noise'] > 0:
            marker_ratio = markers['noise'] / (markers['signal'] + markers['noise'] + 1)
            base_entropy = (base_entropy * 0.7) + (marker_ratio * 0.3)
        
        # Modifiers
        base_entropy *= (1.0 - number_density * 0.25)  # Numbers reduce entropy
        base_entropy += shout_factor * 0.15              # CAPS increase entropy
        base_entropy += sanity_penalty * 0.3             # FIXED: Sanity violations!
        
        # Bounds
        final_entropy = min(0.99, max(0.0, base_entropy))
        
        # Academic correction
        if (markers['signal'] > markers['noise'] * 2 and 
            number_density > 0.05 and 
            shout_factor < 0.1 and
            sanity_penalty == 0.0):  # Only if sane!
            final_entropy *= 0.75
        
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
                'sanity_violations': sanity_penalty > 0,
                'word_count': word_count,
                'char_count': len(text)
            }
        }

    def evaluate_integrity(self, text: str, source: Optional[str] = None):
        """Адаптер для сумісності з API"""
        result = self.analyze(text)
        
        if result.get('entropy') == 0.99:
            return {
                'node': source or 'Unknown',
                'status': 'CRITICAL',
                'new_reputation': 0.1,
                'intervention_required': True,
                'verdict': result['verdict'],
                'entropy': result['entropy']
            }
        
        status_map = {
            'TRUSTED': 'STABLE',
            'ACCEPTABLE': 'STABLE',
            'SUSPICIOUS': 'REJECTED',
            'WARNING': 'REJECTED',
            'CRITICAL': 'REJECTED'
        }
        
        base_reputation = 1.0 - result['entropy']
        
        return {
            'node': source or 'Unknown',
            'status': status_map.get(result['status'], 'STABLE'),
            'new_reputation': round(base_reputation, 2),
            'intervention_required': result['status'] in ['WARNING', 'CRITICAL'],
            'verdict': result['verdict'],
            'entropy': result['entropy'],
            'diagnostics': result.get('diagnostics', {})
        }


# Testing
if __name__ == "__main__":
    engine = VeritasCalibratedCore()
    
    # Test: Borsch quantum collapse (має виявити!)
    borsch = """
    Квантовий резонанс борщу виникає внаслідок дискретної транзакції 
    кропу крізь вакуумну каструлю. Синхрофазотрон ложки моделює парадигму 
    астральної вечері, де ентропія огірка стає метафізичним потоком вібрацій.
    """
    
    result = engine.analyze(borsch)
    print(f"Borsch Quantum: entropy={result['entropy']}, status={result['status']}")
    print(f"Sanity penalty: {result['diagnostics']['sanity_penalty']}")
    print(f"Sanity violations: {result['diagnostics']['sanity_violations']}")
