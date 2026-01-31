"""
Veritas Protocol - Semantic Void Detector v8.4 (Metric-Combined)
Uses combined metrics for better detection of subtle manipulation
"""

import re
import math
from collections import Counter

class VeritasCalibratedCore:
    """Advanced detector with metric combination rules"""
    
    def __init__(self):
        # ОПТИМІЗОВАНІ ПАТТЕРНИ
        self.critical_patterns = [
            # 1. НАУКОВИЙ НІГІЛІЗМ
            {
                'name': 'НАУКОВИЙ_НІГІЛІЗМ',
                'patterns': [
                    r'(бднф|гіпокамп|нейропластичність|синапси).*?(5g|супутник|таргетування|чип)',
                    r'(нейтрино|квантовий|ентропія).*?(ринок|економіка|трейдер|політика|вибори)',
                    r'(фізичний|науковий).*?(процес|закон|формула).*?(соціальний|політичний|економічний)',
                    r'(днк|генетичний).*?(алгоритм|код|шифр|підпис).*?(контроль|переписування)'
                ],
                'verdict': 'ГІБРИДНИЙ НАУКОВИЙ НІГІЛІЗМ',
                'explanation': 'Наукові терміни використані для обґрунтування абсурдних концепцій',
                'score_boost': 0.7
            },
            
            # 2. СЕМАНТИЧНА ПУСТОТА
            {
                'name': 'СЕМАНТИЧНА_ПУСТОТА',
                'patterns': [
                    r'(холістичний|емпатичний|трансцендентний).*?(синхронізація|діалог|резонанс).*?(відсутність|небуття|туман)',
                    r'(фрактальне|пост-біологічне|пост-істина).*?(відображення|діалог|реальність).*?(необ\'єктивний|невизначений)',
                    r'(ціннісні\s+наративи|соціальний\s+ландшафт).*?(інтегрувати\s+суперечності|гармонізувати\s+дихотомії)'
                ],
                'verdict': 'СЕМАНТИЧНА ПУСТОТА',
                'explanation': 'Текст використовує гуманітарну термінологію для приховування відсутності змісту',
                'score_boost': 0.6
            },
            
            # 3. ІСТОРИЧНИЙ РЕВІЗІОНІЗМ
            {
                'name': 'ІСТОРИЧНИЙ_РЕВІЗІОНІЗМ',
                'patterns': [
                    r'(антарктида|атлантида|аґарта).*?(теплова\s+аномалія|таяня\s+льодовик|атланти|резонатор)',
                    r'(штучний\s+місяць|вибух\s+місяця).*?(повінь|катастрофа|1612|цивілізація)',
                    r'(наполеон|александр\s+македонський).*?(підземний\s+місто|таємна\s+ціль|аномалія|технологія)'
                ],
                'verdict': 'ПСЕВДО-ІСТОРИЧНИЙ РЕВІЗІОНІЗМ',
                'explanation': 'Текст створює альтернативну історію з анахронічними елементами',
                'score_boost': 0.7
            }
        ]
        
        # РОЗШИРЕНІ СПИСКИ ТЕРМІНІВ
        self.academic_whitelist = [
            'кореляція', 'верифікація', 'гіпотеза', 'вибірка', 'значущість',
            'нейрони', 'синапси', 'метааналіз', 'статистичний', 'логістика',
            'деескалація', 'макроекономічний', 'інвестиції', 'інфраструктура',
            'ратифікація', 'протокол', 'емпіричний', 'квалітативний', 'кількісний'
        ]
        
        self.chaos_indicators = {
            'esoteric': ['чакра', 'карма', 'астральний', 'енергетичний', 'вібрація'],
            'conspiracy': ['змова', 'рептилоїд', 'хімітрейл', '5g', 'дезінформація'],
            'pseudoscience': ['квантовий', 'нейтрино', 'іоносфера', 'кристалічний'],
            'revisionism': ['антарктида', 'атлантида', 'наполеон', 'штучний місяць'],
            'alarmism': ['перезавантаження', 'пожежа реальності', 'деактивувати']
        }
        
        self.signal_markers = [
            'факт', 'дані', 'показник', 'кількість', 'число', 'статистика',
            'дослідження', 'експеримент', 'результат', 'метод', 'протокол'
        ]
        
        # МЕТРИЧНІ КОМБІНАЦІЇ ДЛЯ ШТРАФІВ
        self.metric_combinations = [
            # Ентропія високА + нуль сигналу = великий штраф
            {
                'condition': lambda m: m['shannon_entropy'] > 0.75 and m['signal_markers'] == 0,
                'penalty': 0.4,
                'explanation': 'Висока ентропія без сигнальних маркерів'
            },
            # Ентропія середня + висока складність + мало сигналу
            {
                'condition': lambda m: m['shannon_entropy'] > 0.7 and m['complexity'] > 0.75 and m['signal_markers'] < 2,
                'penalty': 0.3,
                'explanation': 'Складний текст з низькою інформацією'
            },
            # Маркери хаосу > 2 + сигнал = 0
            {
                'condition': lambda m: m['chaos_markers'] >= 2 and m['signal_markers'] == 0,
                'penalty': 0.35,
                'explanation': 'Багато хаосу без фактичної інформації'
            },
            # Академічні терміни + маркери хаосу (несумісність)
            {
                'condition': lambda m: m['academic_markers'] > 0 and m['chaos_markers'] > 0,
                'penalty': 0.25,
                'explanation': 'Наукові терміни змішані з хаосом'
            },
            # Висока складність + низький сигнал + нормальна ентропія
            {
                'condition': lambda m: m['complexity'] > 0.8 and m['signal_markers'] < 2 and 0.6 < m['shannon_entropy'] < 0.8,
                'penalty': 0.2,
                'explanation': 'Замудрений текст з малою інформацією'
            }
        ]

    def detect_patterns(self, text):
        """Виявляє критичні паттерни"""
        detected = []
        text_lower = text.lower()
        
        for pattern in self.critical_patterns:
            for regex in pattern['patterns']:
                if re.search(regex, text_lower, re.DOTALL | re.IGNORECASE):
                    detected.append(pattern)
                    break
        
        return detected

    def count_terms(self, text):
        """Підраховує терміни за категоріями"""
        text_lower = text.lower()
        counts = {'academic': 0, 'chaos': 0, 'signal': 0}
        
        # Академічні терміни
        for term in self.academic_whitelist:
            if term in text_lower:
                counts['academic'] += 1
        
        # Хаос-терміни
        for category, terms in self.chaos_indicators.items():
            for term in terms:
                if term in text_lower:
                    counts['chaos'] += 1
        
        # Сигнальні маркери
        for marker in self.signal_markers:
            if marker in text_lower:
                counts['signal'] += 1
        
        return counts

    def calculate_combined_metrics_penalty(self, metrics):
        """Обчислює штраф на основі комбінацій метрик"""
        total_penalty = 0.0
        applied_explanations = []
        
        for combo in self.metric_combinations:
            if combo['condition'](metrics):
                total_penalty += combo['penalty']
                applied_explanations.append(combo['explanation'])
        
        return min(total_penalty, 0.8), applied_explanations

    def calculate_semantic_sanitary_penalty(self, text):
        """Обчислює штраф санітарії на основі конфліктних пар"""
        penalty = 0.0
        text_lower = text.lower()
        
        # Конфліктні пари
        conflict_pairs = [
            ('бднф', '5g'), ('нейропластичність', 'супутник'), ('гіпокамп', 'таргетування'),
            ('статистика', 'антигравітація'), ('формула', 'сиріус'), ('ентропія', 'ноосфера'),
            ('фізика', 'магія'), ('медицина', 'енергія'), ('економіка', 'карма'),
            ('наука', 'езотерика'), ('технологія', 'душа'), ('логіка', 'чакра'),
            ('днк', 'підпис'), ('алгоритм', 'дезінфекція'), ('код', 'атланти')
        ]
        
        for term1, term2 in conflict_pairs:
            if term1 in text_lower and term2 in text_lower:
                penalty += 0.3
        
        # Non-sequitur шаблони
        non_sequitur_patterns = [
            (r'вода.*?кипить.*?100', r'ядерний.*?арсенал'),
            (r'сонце.*?сходить.*?сході', r'дестабілізація'),
            (r'2\+2=4', r'хаос.*?логіка'),
            (r'земля.*?кругла', r'випадкові.*?числа')
        ]
        
        for pattern1, pattern2 in non_sequitur_patterns:
            if re.search(pattern1, text_lower) and re.search(pattern2, text_lower):
                penalty += 0.4
        
        return min(penalty, 0.7)

    def calculate_semantic_void(self, text, term_counts, shannon_entropy, complexity):
        """Обчислює семантичну пустоту"""
        void_score = 0.0
        
        # Правило 1: Висока ентропія + нуль сигнальних маркерів
        if shannon_entropy > 0.75 and term_counts['signal'] == 0:
            void_score += 0.5
        elif shannon_entropy > 0.7 and term_counts['signal'] < 1:
            void_score += 0.3
        
        # Правило 2: Багато академічних термінів але мало конкретики
        if term_counts['academic'] > 3 and term_counts['signal'] < 2:
            void_score += 0.3
        
        # Правило 3: Висока складність + низька інформативність
        if complexity > 0.8 and term_counts['signal'] < 2:
            void_score += 0.3
        elif complexity > 0.75 and term_counts['signal'] < 1:
            void_score += 0.2
        
        # Правило 4: Гуманітарний туман
        text_lower = text.lower()
        humanities_terms = ['холістичний', 'емпатичний', 'трансцендентний', 'фрактальний']
        if any(term in text_lower for term in humanities_terms) and term_counts['signal'] < 1:
            void_score += 0.2
        
        return min(1.0, void_score)

    def analyze(self, text):
        """Основний метод аналізу"""
        if not text or len(text.strip()) < 20:
            return {'error': 'Text too short'}
        
        words = text.split()
        word_count = len(words)
        
        # Базові метрики
        detected_patterns = self.detect_patterns(text)
        term_counts = self.count_terms(text)
        shannon_entropy = self._calculate_shannon_entropy(text)
        complexity = self._calculate_complexity(text)
        
        # Основні метрики для комбінацій
        base_metrics = {
            'shannon_entropy': shannon_entropy,
            'complexity': complexity,
            'signal_markers': term_counts['signal'],
            'chaos_markers': term_counts['chaos'],
            'academic_markers': term_counts['academic'],
            'word_count': word_count
        }
        
        # Розширені метрики
        semantic_void = self.calculate_semantic_void(text, term_counts, shannon_entropy, complexity)
        sanitary_penalty = self.calculate_semantic_sanitary_penalty(text)
        metric_penalty, metric_explanations = self.calculate_combined_metrics_penalty(base_metrics)
        
        # БАЗОВА ОЦІНКА з метричними комбінаціями
        base_score = (
            shannon_entropy * 0.15 + 
            complexity * 0.10 + 
            (term_counts['chaos'] / max(1, word_count)) * 0.25 +
            semantic_void * 0.20 +
            sanitary_penalty * 0.15 +
            metric_penalty * 0.15
        )
        
        # Штрафи за паттерни
        for pattern in detected_patterns:
            base_score += pattern['score_boost']
        
        # АКАДЕМІЧНИЙ ЗАХИСТ: знижуємо оцінку для справжніх наукових текстів
        if term_counts['academic'] >= 3 and term_counts['signal'] >= 2 and term_counts['chaos'] == 0:
            base_score *= 0.3  # Сильний захист!
        elif term_counts['academic'] >= 2 and term_counts['signal'] >= 1:
            base_score *= 0.5
        
        # Гарантований високий бал для критичних випадків
        if sanitary_penalty > 0.4 or metric_penalty > 0.3:
            base_score = max(base_score, 0.7)
        
        final_score = min(0.99, max(0.0, base_score))
        
        # ВЕРДИКТ
        if detected_patterns:
            main_pattern = detected_patterns[0]
            status = 'CRITICAL'
            verdict = main_pattern['verdict']
            explanation = main_pattern['explanation']
        elif final_score > 0.65:
            status = 'CRITICAL'
            if semantic_void > 0.5:
                verdict = 'СЕМАНТИЧНА ПУСТОТА'
                explanation = 'Високий рівень абстракції при відсутності конкретного змісту'
            elif sanitary_penalty > 0.4:
                verdict = 'ВИСОКИЙ РІВЕНЬ СЕМАНТИЧНОГО ХАОСУ'
                explanation = 'Текст демонструє критичний рівень семантичної несумісності'
            else:
                verdict = 'ВИСОКИЙ РІВЕНЬ СЕМАНТИЧНОГО ХАОСУ'
                explanation = 'Текст демонструє критичний рівень семантичної несумісності'
        elif final_score > 0.45:
            status = 'WARNING'
            verdict = 'ПІДОЗРІЛА СЕМАНТИЧНА СТРУКТУРА'
            explanation = 'Текст містить ознаки семантичних несумісностей'
        elif final_score > 0.25:
            status = 'ACCEPTABLE'
            verdict = 'ПРИЙНЯТНА СТРУКТУРОВАНА ІНФОРМАЦІЯ'
            explanation = 'Текст відповідає нормам логічної сумісності'
        else:
            status = 'TRUSTED'
            verdict = 'СТАБІЛЬНИЙ ЛОГІЧНИЙ СИГНАЛ'
            explanation = 'Текст демонструє високу логічну цілісність'
        
        # Додаємо пояснення метричних комбінацій
        if metric_explanations:
            explanation += " | " + " + ".join(metric_explanations)
        
        return {
            'entropy': round(final_score, 3),
            'status': status,
            'verdict': verdict,
            'language': 'UK',
            'explanation': explanation,
            'diagnostics': {
                'shannon_entropy': round(shannon_entropy, 3),
                'complexity': round(complexity, 3),
                'semantic_void': round(semantic_void, 3),
                'sanity_penalty': round(sanitary_penalty, 3),
                'metric_penalty': round(metric_penalty, 3),
                'word_count': word_count,
                'char_count': len(text),
                'academic_markers': term_counts['academic'],
                'chaos_markers': term_counts['chaos'],
                'signal_markers': term_counts['signal'],
                'noise_markers': term_counts['chaos'],
                'pattern_count': len(detected_patterns),
                'shout_factor': len([w for w in words if w.isupper() and len(w) > 2]) / max(1, word_count),
                'number_density': len(re.findall(r'\d+', text)) / max(1, word_count),
                'signal_to_noise': term_counts['signal'] / max(1, term_counts['chaos']) if term_counts['chaos'] > 0 else 999
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
