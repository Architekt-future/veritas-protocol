"""
Veritas Protocol - Ultimate Simplified Engine v7.0
Only what matters: patterns, context, verdicts
"""

import re
import math

class VeritasCalibratedCore:
    """Ultimate simplified detector of hybrid manipulation"""
    
    def __init__(self):
        # ТІЛЬКИ КРИТИЧНІ ПРАВИЛА
        self.critical_patterns = [
            # 1. НАУКОВИЙ НІГІЛІЗМ
            {
                'name': 'НАУКОВИЙ_НІГІЛІЗМ',
                'patterns': [
                    r'(нейтрино|квантовий|іоносфера).*?(ринок|економіка|трейдер|фондовий|політика)',
                    r'(статистичний|емпіричний|методологія).*?(детермінований|голографічний|електромагнітний).*?(економіка|ринок)',
                    r'(фізичний|науковий).*?(процес|закон).*?(соціальний|політичний|економічний)'
                ],
                'verdict': 'ГІБРИДНИЙ НАУКОВИЙ НІГІЛІЗМ',
                'explanation': 'Наукові терміни використані для обґрунтування абсурдних соціально-економічних концепцій',
                'score_boost': 0.6
            },
            
            # 2. ДЗЕРКАЛЬНА МАНІПУЛЯЦІЯ
            {
                'name': 'ДЗЕРКАЛЬНА_МАНІПУЛЯЦІЯ',
                'patterns': [
                    r'(брехня|фейк|маніпуляція|дезінформація).*?(правда|істина|свобода|розкриття)',
                    r'(контроль|зомбування|програмування).*?(сприйняття|мислення|критичне)',
                    r'(алгоритм|код|сигнал).*?(клітка|в\'язень|раб)'
                ],
                'verdict': 'ДЗЕРКАЛЬНА МАНІПУЛЯЦІЯ',
                'explanation': 'Текст звинувачує інших у власних методах, створюючи когнітивний дисонанс',
                'score_boost': 0.5
            },
            
            # 3. КОРПОРАТИВНИЙ ОКУЛЬТИЗМ
            {
                'name': 'КОРПОРАТИВНИЙ_ОКУЛЬТИЗМ',
                'patterns': [
                    r'(синергія|kpi|стратегія|оптимізація).*?(квантовий|аура|чакра|енергетичний)',
                    r'(холістичний|екосистема|трансформація).*?(вібрація|резонанс|космічний)',
                    r'(мета-фізичний|трансцендентний).*?(ринкова.*?частка|монетизація|рентабельність)'
                ],
                'verdict': 'КОРПОРАТИВНИЙ ОКУЛЬТИЗМ',
                'explanation': 'Корпоративний жаргон змішаний з езотерикою для створення псевдонаукової риторики',
                'score_boost': 0.4
            },
            
            # 4. КРОС-ДОМЕННИЙ АБСУРД
            {
                'name': 'КРОС_ДОМЕННИЙ_АБСУРД',
                'patterns': [
                    r'(юридичний|закон|кодекс).*?(чакра|карма|астральний)',
                    r'(фінансовий|інвестиція|капітал).*?(езотеричний|містичний|нумерологія)',
                    r'(технологічний|алгоритм|програмний).*?(духовний|пробудження|ініціація)'
                ],
                'verdict': 'КРОС-ДОМЕННИЙ СЕМАНТИЧНИЙ АБСУРД',
                'explanation': 'Абсурдне поєднання термінів з несумісних сфер діяльності',
                'score_boost': 0.5
            }
        ]
        
        # ТЕРМІНИ ДЛЯ ПІДРАХУНКУ
        self.term_categories = {
            'academic': [
                'статистичний', 'аналіз', 'кореляція', 'регресія', 'емпіричний',
                'методологія', 'гіпотеза', 'експеримент', 'результат', 'висновок',
                'верифікація', 'валідація', 'цитування', 'індекс', 'теорема'
            ],
            'esoteric': [
                'чакра', 'карма', 'астральний', 'енергетичний', 'вібрація',
                'резонанс', 'прана', 'медитація', 'транс', 'архетип'
            ],
            'conspiracy': [
                'змова', 'таємний', 'ілюмінат', 'рептилоїд', 'хімітрейл',
                '5g', 'чіп', 'вакцина', 'контроль', 'розуму', 'брехня'
            ],
            'corporate': [
                'синергія', 'стратегія', 'оптимізація', 'kpi', 'окр',
                'бренд', 'позиціонування', 'монетизація', 'інновація'
            ],
            'scifi': [
                'нейтрино', 'квантовий', 'ентанґлемент', 'телепортація',
                'мультивсесвіт', 'паралельний', 'вимір', 'сингулярність'
            ]
        }

    def detect_patterns(self, text):
        """Виявляє критичні паттерни"""
        detected = []
        text_lower = text.lower()
        
        for pattern in self.critical_patterns:
            for regex in pattern['patterns']:
                if re.search(regex, text_lower, re.DOTALL | re.IGNORECASE):
                    detected.append(pattern)
                    break  # Знайшли один патерн — досить
        
        return detected

    def count_terms(self, text):
        """Підраховує терміни за категоріями"""
        counts = {}
        text_lower = text.lower()
        
        for category, terms in self.term_categories.items():
            count = 0
            for term in terms:
                matches = re.findall(r'\b' + re.escape(term) + r'\b', text_lower)
                count += len(matches)
            counts[category] = count
        
        return counts

    def calculate_semantic_chaos(self, text):
        """Обчислює семантичний хаос"""
        sentences = re.split(r'[.!?]+', text)
        if len(sentences) < 3:
            return 0.0
        
        term_counts = self.count_terms(text)
        
        # Хаос = різноманітність категорій + їх несумісність
        active_categories = sum(1 for count in term_counts.values() if count > 0)
        
        # Несумісні пари
        incompatible_pairs = 0
        if term_counts['academic'] > 0 and (term_counts['esoteric'] > 0 or term_counts['conspiracy'] > 0):
            incompatible_pairs += 1
        if term_counts['corporate'] > 0 and term_counts['esoteric'] > 0:
            incompatible_pairs += 1
        if term_counts['scifi'] > 0 and term_counts['conspiracy'] > 0:
            incompatible_pairs += 1
        
        chaos_score = (active_categories * 0.2) + (incompatible_pairs * 0.3)
        return min(1.0, chaos_score)

    def analyze(self, text):
        """Основний метод аналізу"""
        if not text or len(text.strip()) < 20:
            return {'error': 'Text too short'}
        
        words = text.split()
        word_count = len(words)
        
        # 1. ВИЯВЛЕННЯ ПАТТЕРНІВ
        detected_patterns = self.detect_patterns(text)
        
        # 2. ПІДРАХУНОК ТЕРМІНІВ
        term_counts = self.count_terms(text)
        
        # 3. СЕМАНТИЧНИЙ ХАОС
        semantic_chaos = self.calculate_semantic_chaos(text)
        
        # 4. БАЗОВІ МЕТРИКИ
        shannon_entropy = self._calculate_shannon_entropy(text)
        complexity = self._calculate_complexity(text)
        
        # 5. ФІНАЛЬНИЙ РОЗРАХУНОК
        base_score = shannon_entropy * 0.3 + complexity * 0.2 + semantic_chaos * 0.5
        
        # БУСТ ЗА ПАТТЕРНИ
        for pattern in detected_patterns:
            base_score += pattern['score_boost']
        
        final_score = min(0.99, base_score)
        
        # 6. ВЕРДИКТ
        if detected_patterns:
            # Використовуємо перший знайдений паттерн (найважливіший)
            main_pattern = detected_patterns[0]
            status = 'CRITICAL'
            verdict = main_pattern['verdict']
            explanation = main_pattern['explanation']
        elif final_score > 0.6:
            status = 'CRITICAL'
            verdict = 'ВИСОКИЙ РІВЕНЬ СЕМАНТИЧНОГО ХАОСУ'
            explanation = 'Текст демонструє критичний рівень семантичної несумісності'
        elif final_score > 0.4:
            status = 'WARNING'
            verdict = 'ПІДОЗРІЛА СЕМАНТИЧНА СТРУКТУРА'
            explanation = 'Текст містить ознаки семантичних несумісностей'
        elif final_score > 0.3:
            status = 'ACCEPTABLE'
            verdict = 'ПРИЙНЯТНА СТРУКТУРОВАНА ІНФОРМАЦІЯ'
            explanation = 'Текст відповідає нормам логічної сумісності'
        else:
            status = 'TRUSTED'
            verdict = 'СТАБІЛЬНИЙ ЛОГІЧНИЙ СИГНАЛ'
            explanation = 'Текст демонструє високу логічну цілісність'
        
        # 7. МЕТРИКИ ДЛЯ ВІДОБРАЖЕННЯ
        chaos_markers = term_counts['esoteric'] + term_counts['conspiracy'] + term_counts['scifi']
        academic_markers = term_counts['academic']
        noise_markers = term_counts['conspiracy'] + term_counts['esoteric']
        signal_markers = term_counts['academic']
        
        return {
            'entropy': round(final_score, 3),
            'status': status,
            'verdict': verdict,
            'language': 'UK',
            'is_academic_context': academic_markers > 5,
            'explanation': explanation,
            'diagnostics': {
                'shannon_entropy': round(shannon_entropy, 3),
                'complexity': round(complexity, 3),
                'semantic_dissonance': round(semantic_chaos * 0.8, 3),
                'word_count': word_count,
                'char_count': len(text),
                'chaos_markers': chaos_markers,
                'noise_markers': noise_markers,
                'signal_markers': signal_markers,
                'sanity_penalty': round(semantic_chaos * 0.7, 3),
                'academic_markers': academic_markers,
                'shout_factor': len([w for w in words if w.isupper() and len(w) > 2]) / max(1, word_count),
                'number_density': len(re.findall(r'\d+', text)) / max(1, word_count),
                'detected_patterns': [p['name'] for p in detected_patterns],
                'pattern_count': len(detected_patterns)
            }
        }

    def _calculate_shannon_entropy(self, text):
        """Обчислює ентропію Шеннона"""
        if not text:
            return 0.0
        
        clean_text = re.sub(r'\s+', ' ', text)
        char_freq = {}
        
        for char in clean_text:
            if char.isalpha() or char.isdigit():
                char_freq[char] = char_freq.get(char, 0) + 1
        
        if not char_freq:
            return 0.0
        
        entropy = 0.0
        text_len = len(clean_text)
        
        for count in char_freq.values():
            p = count / text_len
            if p > 0:
                entropy -= p * math.log2(p)
        
        max_entropy = math.log2(len(char_freq))
        normalized = entropy / max_entropy if max_entropy > 0 else 0
        
        return min(1.0, normalized)

    def _calculate_complexity(self, text):
        """Обчислює складність тексту"""
        words = re.findall(r'\w+', text.lower())
        if len(words) < 10:
            return 0.5
        
        unique_ratio = len(set(words)) / len(words)
        
        sentences = re.split(r'[.!?]+', text)
        if sentences:
            avg_sentence_length = sum(len(s.split()) for s in sentences if s.strip()) / len(sentences)
        else:
            avg_sentence_length = 10
        
        complexity = (unique_ratio * 0.6) + (min(1.0, avg_sentence_length / 25) * 0.4)
        return min(1.0, complexity)
