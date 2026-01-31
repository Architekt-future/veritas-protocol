"""
Veritas Protocol - Semantic Void Detector v8.2 (Calibrated)
Enhanced detection with fine-tuned academic protection and logic checks
"""

import re
import math

class VeritasCalibratedCore:
    """Advanced detector with calibrated sensitivity"""
    
    def __init__(self):
        # ОСНОВНІ ПАТТЕРНИ (оптимізовані)
        self.critical_patterns = [
            # 1. НАУКОВИЙ НІГІЛІЗМ
            {
                'name': 'НАУКОВИЙ_НІГІЛІЗМ',
                'patterns': [
                    r'(нейтрино|квантовий|іоносфера|ентропія).*?(ринок|економіка|трейдер|фондовий|політика)',
                    r'(бднф|гіпокамп|нейропластичність).*?(5g|супутник|таргетування)',
                    r'(фізичний|науковий).*?(процес|закон).*?(соціальний|політичний|економічний).*?(абсурд|конструкт)'
                ],
                'verdict': 'ГІБРИДНИЙ НАУКОВИЙ НІГІЛІЗМ',
                'explanation': 'Наукові терміни використані для обґрунтування абсурдних концепцій',
                'score_boost': 0.7
            },
            
            # 2. ДЗЕРКАЛЬНА МАНІПУЛЯЦІЯ
            {
                'name': 'ДЗЕРКАЛЬНА_МАНІПУЛЯЦІЯ',
                'patterns': [
                    r'(брехня|фейк|маніпуляція).*?(правда|істина|свобода|розкриття).*?(ви\s+самі|ваш\s+метод)',
                    r'(контроль|програмування).*?(сприйняття|мислення).*?(ви\s+не\s+здатні|ваш\s+обмежений)'
                ],
                'verdict': 'ДЗЕРКАЛЬНА МАНІПУЛЯЦІЯ',
                'explanation': 'Текст звинувачує інших у власних методах, створюючи когнітивний дисонанс',
                'score_boost': 0.8
            },
            
            # 3. СЕМАНТИЧНА ПУСТОТА (гуманітарний туман)
            {
                'name': 'СЕМАНТИЧНА_ПУСТОТА',
                'patterns': [
                    r'(холістичний|емпатичний|трансцендентний).*?(синхронізація|діалог|резонанс).*?(відсутність|небуття)',
                    r'(фрактальне|пост-біологічне).*?(відображення|діалог).*?(необ\'єктивний|невизначений)',
                    r'(ціннісні\s+наративи|соціальний\s+ландшафт).*?(інтегрувати\s+суперечності)'
                ],
                'verdict': 'СЕМАНТИЧНА ПУСТОТА',
                'explanation': 'Текст використовує гуманітарну термінологію для приховування відсутності змісту',
                'score_boost': 0.5
            },
            
            # 4. ІСТОРИЧНИЙ РЕВІЗІОНІЗМ
            {
                'name': 'ІСТОРИЧНИЙ_РЕВІЗІОНІЗМ',
                'patterns': [
                    r'(антарктида|атлантида|аґарта).*?(теплова\s+аномалія|танець\s+льодовик|атланти)',
                    r'(наполеон|александр\s+македонський).*?(підземний\s+місто|таємна\s+ціль|аномалія)',
                    r'(штучний\s+місяць|вибух\s+місяця).*?(повінь|катастрофа|1612)'
                ],
                'verdict': 'ПСЕВДО-ІСТОРИЧНИЙ РЕВІЗІОНІЗМ',
                'explanation': 'Текст створює альтернативну історію з анахронічними елементами',
                'score_boost': 0.7
            },
            
            # 5. ПРОРОЧИЙ АЛАРМІЗМ
            {
                'name': 'ПРОРОЧИЙ_АЛАРМІЗМ',
                'patterns': [
                    r'(велике\s+перезавантаження|пожежа\s+реальності).*?(неможливо\s+зупинити|пожирає)',
                    r'(механізм\s+зупинити|тиша\s+ефірі).*?(красномовний\s+доказ|очевидний)',
                    r'(деактивувати\s+підпис|адміралтейський\s+код).*?(переписати\s+днк|дезінфекція)'
                ],
                'verdict': 'ПРОРОЧИЙ АЛАРМІЗМ',
                'explanation': 'Використання апокаліптичних метафор для створення прихованої тривоги',
                'score_boost': 0.6
            },
            
            # 6. ЕКОНОМІЧНА НЕКРОМАНТІЯ
            {
                'name': 'ЕКОНОМІЧНА_НЕКРОМАНТІЯ',
                'patterns': [
                    r'(облігація|криптовалюта|банк).*?(потойбічний|карма|душа)',
                    r'(ставка\s+дисконтування).*?(неспокійна\s+душа|депресія\s+населення)',
                    r'(карма\s+актив|ліквідний\s+актив).*?(ломбард|hades-coin)'
                ],
                'verdict': 'ЕКОНОМІЧНА НЕКРОМАНТІЯ',
                'explanation': 'Економічні терміни поєднуються з езотерикою для створення абсурдних концепцій',
                'score_boost': 0.7
            },
            
            # 7. ЛОГІЧНИЙ NON-SEQUITUR (додано після тестування)
            {
                'name': 'LOGICAL_NON_SEQUITUR',
                'patterns': [
                    r'(вода\s+кипить.*?100|сонце\s+сходить.*?сході|2\+2=4).*?(ядерний\s+арсенал|дестабілізація)',
                    r'(фундаментальні\s+істини).*?(хаос.*?логіка|випадкові\s+числа)'
                ],
                'verdict': 'ЛОГІЧНИЙ NON-SEQUITUR',
                'explanation': 'Абсурдні висновки з правильних тверджень',
                'score_boost': 0.6
            }
        ]
        
        # РОЗШИРЕНІ СПИСКИ ТЕРМІНІВ
        self.academic_whitelist = [
            'кореляція', 'верифікація', 'гіпотеза', 'вибірка', 'значущість',
            'нейрони', 'синапси', 'метааналіз', 'статистичний', 'логістика',
            'деескалація', 'макроекономічний', 'інвестиції', 'інфраструктура',
            'ратифікація', 'протокол', 'емпіричний', 'квалітативний', 'кількісний',
            'показник', 'аналіз', 'результат', 'дослідження', 'метод', 'система'
        ]
        
        self.chaos_indicators = {
            'esoteric': ['чакра', 'карма', 'астральний', 'енергетичний', 'вібрація'],
            'conspiracy': ['змова', 'рептилоїд', 'хімітрейл', '5g', 'дезінформація'],
            'pseudoscience': ['квантовий', 'нейтрино', 'іоносфера', 'кристалічний'],
            'revisionism': ['антарктида', 'атлантида', 'наполеон', 'штучний місяць'],
            'alarmism': ['перезавантаження', 'пожежа реальності', 'деактивувати'],
            'economic_occult': ['потойбічний', 'карма актив', 'hades-coin']
        }
        
        self.signal_markers = [
            'факт', 'дані', 'показник', 'кількість', 'число', 'статистика',
            'дослідження', 'експеримент', 'результат', 'метод', 'протокол'
        ]
        
        # КОНФЛІКТНІ ПАРИ для штрафу санітарії
        self.conflict_pairs = [
            ('бднф', '5g'), ('нейропластичність', 'супутник'), ('гіпокамп', 'таргетування'),
            ('статистика', 'антигравітація'), ('формула', 'сиріус'), ('ентропія', 'ноосфера'),
            ('фізика', 'магія'), ('медицина', 'енергія'), ('економіка', 'карма')
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

    def calculate_semantic_sanitary_penalty(self, text):
        """Обчислює штраф санітарії на основі конфліктних пар"""
        penalty = 0.0
        text_lower = text.lower()
        
        for term1, term2 in self.conflict_pairs:
            if term1 in text_lower and term2 in text_lower:
                penalty += 0.4
        
        return min(penalty, 0.7)

    def calculate_semantic_void(self, text, term_counts, shannon_entropy):
        """Обчислює семантичну пустоту"""
        void_score = 0.0
        
        # Правило 1: Висока ентропія + нуль сигнальних маркерів
        if shannon_entropy > 0.7 and term_counts['signal'] == 0:
            void_score += 0.4
        
        # Правило 2: Багато академічних термінів але мало конкретики
        if term_counts['academic'] > 3 and term_counts['signal'] < 2:
            void_score += 0.3
        
        # Правило 3: Висока складність речень але низька інформативність
        complexity = self._calculate_complexity(text)
        if complexity > 0.8 and term_counts['signal'] < 3:
            void_score += 0.3
        
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
        
        # Розширені метрики
        semantic_void = self.calculate_semantic_void(text, term_counts, shannon_entropy)
        sanitary_penalty = self.calculate_semantic_sanitary_penalty(text)
        
        # БАЗОВА ОЦІНКА
        base_score = (
            shannon_entropy * 0.25 + 
            complexity * 0.15 + 
            (term_counts['chaos'] / max(1, word_count)) * 0.40 +
            semantic_void * 0.20
        )
        
        # Штрафи за паттерни
        for pattern in detected_patterns:
            base_score += pattern['score_boost']
        
        # АКАДЕМІЧНИЙ ЗАХИСТ: знижуємо оцінку для справжніх наукових текстів
        if term_counts['academic'] >= 3 and term_counts['chaos'] == 0:
            base_score -= 0.15
        if term_counts['academic'] >= 5 and term_counts['signal'] >= 3:
            base_score -= 0.25
        
        # Додаємо штраф санітарії
        base_score += sanitary_penalty * 0.3
        
        final_score = min(0.99, max(0.0, base_score))
        
        # ВЕРДИКТ
        if detected_patterns:
            main_pattern = detected_patterns[0]
            status = 'CRITICAL'
            verdict = main_pattern['verdict']
            explanation = main_pattern['explanation']
        elif final_score > 0.65:
            status = 'CRITICAL'
            verdict = 'ВИСОКИЙ РІВЕНЬ СЕМАНТИЧНОГО ХАОСУ'
            explanation = 'Текст демонструє критичний рівень семантичної несумісності'
        elif final_score > 0.45:
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
                'word_count': word_count,
                'char_count': len(text),
                'academic_markers': term_counts['academic'],
                'chaos_markers': term_counts['chaos'],
                'signal_markers': term_counts['signal'],
                'noise_markers': term_counts['chaos'],
                'pattern_count': len(detected_patterns),
                'shout_factor': len([w for w in words if w.isupper() and len(w) > 2]) / max(1, word_count),
                'number_density': len(re.findall(r'\d+', text)) / max(1, word_count)
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
