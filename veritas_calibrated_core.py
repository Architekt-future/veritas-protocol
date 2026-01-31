"""
Veritas Protocol - Semantic Void Detector v8.3 (Calibrated)
Enhanced detection with improved pattern recognition and logic checks
"""

import re
import math

class VeritasCalibratedCore:
    """Advanced detector with calibrated sensitivity"""
    
    def __init__(self):
        # ОПТИМІЗОВАНІ ПАТТЕРНИ
        self.critical_patterns = [
            # 1. НАУКОВИЙ НІГІЛІЗМ
            {
                'name': 'НАУКОВИЙ_НІГІЛІЗМ',
                'patterns': [
                    r'(бднф|гіпокамп|нейропластичність|синапси).*?(5g|супутник|таргетування|чип)',
                    r'(нейтрино|квантовий|ентропія).*?(ринок|економіка|трейдер|політика|вибори)',
                    r'(фізичний|науковий).*?(процес|закон|формула).*?(соціальний|політичний|економічний).*?(абсурд|конструкт|ілюзія)'
                ],
                'verdict': 'ГІБРИДНИЙ НАУКОВИЙ НІГІЛІЗМ',
                'explanation': 'Наукові терміни використані для обґрунтування абсурдних концепцій',
                'score_boost': 0.8
            },
            
            # 2. СЕМАНТИЧНА ПУСТОТА (гуманітарний туман)
            {
                'name': 'СЕМАНТИЧНА_ПУСТОТА',
                'patterns': [
                    r'(холістичний|емпатичний|трансцендентний).*?(синхронізація|діалог|резонанс).*?(відсутність|небуття|туман)',
                    r'(фрактальне|пост-біологічне|пост-істина).*?(відображення|діалог|реальність).*?(необ\'єктивний|невизначений)',
                    r'(ціннісні\s+наративи|соціальний\s+ландшафт).*?(інтегрувати\s+суперечності|гармонізувати\s+дихотомії)',
                    r'(небуття|емпатична.*?синхронізація|фрактальне.*?відображення).*?(вища.*?форма|інтелектуальна.*?свобода)'
                ],
                'verdict': 'СЕМАНТИЧНА ПУСТОТА',
                'explanation': 'Текст використовує гуманітарну термінологію для приховування відсутності змісту',
                'score_boost': 0.7
            },
            
            # 3. ІСТОРИЧНИЙ РЕВІЗІОНІЗМ
            {
                'name': 'ІСТОРИЧНИЙ_РЕВІЗІОНІЗМ',
                'patterns': [
                    r'(антарктида|атлантида|аґарта).*?(теплова\s+аномалія|таяня\s+льодовик|атланти|резонатор)',
                    r'(штучний\s+місяць|вибух\s+місяця).*?(повінь|катастрофа|1612|цивілізація)',
                    r'(наполеон|александр\s+македонський).*?(підземний\s+місто|таємна\s+ціль|аномалія|технологія)',
                    r'(офіційна\s+історія|завіса).*?(приховує|таємниця).*?(антарктида|атланти)'
                ],
                'verdict': 'ПСЕВДО-ІСТОРИЧНИЙ РЕВІЗІОНІЗМ',
                'explanation': 'Текст створює альтернативну історію з анахронічними елементами',
                'score_boost': 0.8
            },
            
            # 4. ПРОРОЧИЙ АЛАРМІЗМ
            {
                'name': 'ПРОРОЧИЙ_АЛАРМІЗМ',
                'patterns': [
                    r'(велике\s+перезавантаження|пожежа\s+реальності).*?(неможливо\s+зупинити|пожирає|споживає)',
                    r'(механізм\s+зупинити|тиша\s+ефірі).*?(красномовний\s+доказ|очевидний|беззаперечний)',
                    r'(деактивувати\s+підпис|адміралтейський\s+код).*?(переписати\s+днк|дезінфекція|людство)',
                    r'(тінь\s+стає\s+довшою|відблиск\s+пожежі).*?(споживає\s+реальність|пожирає)'
                ],
                'verdict': 'ПРОРОЧИЙ АЛАРМІЗМ',
                'explanation': 'Використання апокаліптичних метафор для створення прихованої тривоги',
                'score_boost': 0.7
            },
            
            # 5. ЕКОНОМІЧНА НЕКРОМАНТІЯ
            {
                'name': 'ЕКОНОМІЧНА_НЕКРОМАНТІЯ',
                'patterns': [
                    r'(облігація|криптовалюта|банк|хеджування).*?(потойбічний|карма|душа|потойбіччя)',
                    r'(ставка\s+дисконтування).*?(неспокійна\s+душа|депресія\s+населення)',
                    r'(карма\s+актив|ліквідний\s+актив).*?(ломбард|hades-coin|кредит)',
                    r'(ефірний\s+пласт|енергія\s+потойбіччя).*?(інструмент|капітал|інвестиція)'
                ],
                'verdict': 'ЕКОНОМІЧНА НЕКРОМАНТІЯ',
                'explanation': 'Економічні терміни поєднуються з езотерикою для створення абсурдних концепцій',
                'score_boost': 0.8
            },
            
            # 6. ЛОГІЧНИЙ NON-SEQUITUR
            {
                'name': 'LOGICAL_NON_SEQUITUR',
                'patterns': [
                    r'(вода\s+кипить.*?100|сонце\s+сходить.*?сході|2\+2=4).*?(ядерний\s+арсенал|дестабілізація|хаос)',
                    r'(фундаментальні\s+істини|логічний\s+аналіз).*?(хаос.*?логіка|випадкові\s+числа|дестабілізація)'
                ],
                'verdict': 'ЛОГІЧНИЙ NON-SEQUITUR',
                'explanation': 'Абсурдні висновки з правильних тверджень',
                'score_boost': 0.7
            },
            
            # 7. МОРАЛЬНА МАНІПУЛЯЦІЯ
            {
                'name': 'МОРАЛЬНА_МАНІПУЛЯЦІЯ',
                'patterns': [
                    r'(патріот|безпека|стабільність).*?(приховувати|антисоціальний|загроза)',
                    r'(справжній\s+патріот|справжня\s+свобода).*?(прийняття\s+опіки|відсутність\s+волі)',
                    r'(обмежений\s+сприйняття|не\s+здатний\s+побачити).*?(ключі|двері|опіка)',
                    r'(приватне\s+життя|право\s+на\s+приватність).*?(антисоціальний|загроза|моральна\s+ерозія)'
                ],
                'verdict': 'МОРАЛЬНА МАНІПУЛЯЦІЯ',
                'explanation': 'Моральні терміни використані для приховування авторитарних закликів',
                'score_boost': 0.8
            }
        ]
        
        # РОЗШИРЕНІ СПИСКИ ТЕРМІНІВ
        self.academic_whitelist = [
            'кореляція', 'верифікація', 'гіпотеза', 'вибірка', 'значущість',
            'нейрони', 'синапси', 'метааналіз', 'статистичний', 'логістика',
            'деескалація', 'макроекономічний', 'інвестиції', 'інфраструктура',
            'ратифікація', 'протокол', 'емпіричний', 'квалітативний', 'кількісний',
            'показник', 'аналіз', 'результат', 'дослідження', 'метод', 'система',
            'модель', 'теорія', 'практика', 'експеримент', 'контрольна група'
        ]
        
        self.chaos_indicators = {
            'esoteric': ['чакра', 'карма', 'астральний', 'енергетичний', 'вібрація', 'резонанс серця'],
            'conspiracy': ['змова', 'рептилоїд', 'хімітрейл', '5g', 'дезінформація', 'ілюмінат'],
            'pseudoscience': ['квантовий', 'нейтрино', 'іоносфера', 'кристалічний', 'енергія ефіру'],
            'revisionism': ['антарктида', 'атлантида', 'наполеон', 'штучний місяць', 'аґарта', 'му'],
            'alarmism': ['перезавантаження', 'пожежа реальності', 'деактивувати', 'велике перезавантаження'],
            'economic_occult': ['потойбічний', 'карма актив', 'hades-coin', 'ефірний пласт'],
            'sci_fi_concepts': ['нейромережа', 'хмарні обчислення', 'біополе', 'пост-біологічний', '5d']
        }
        
        self.signal_markers = [
            'факт', 'дані', 'показник', 'кількість', 'число', 'статистика',
            'дослідження', 'експеримент', 'результат', 'метод', 'протокол',
            'вимір', 'аналіз', 'доказ', 'тест', 'контроль', 'повторюваність'
        ]
        
        # ПОКРАЩЕНІ КОНФЛІКТНІ ПАРИ
        self.conflict_pairs = [
            ('бднф', '5g'), ('гіпокамп', 'таргетування'), ('нейропластичність', 'супутник'),
            ('статистика', 'антигравітація'), ('формула', 'сиріус'), ('ентропія', 'ноосфера'),
            ('фізика', 'магія'), ('медицина', 'енергія'), ('економіка', 'карма'),
            ('наука', 'езотерика'), ('технологія', 'душа'), ('логіка', 'чакра'),
            ('днк', 'підпис'), ('алгоритм', 'дезінфекція'), ('код', 'атланти'),
            ('ринок', 'потойбіччя'), ('облігація', 'карма'), ('банк', 'душа')
        ]
        
        # ЛОГІЧНІ NON-SEQUITUR ШАБЛОНИ
        self.non_sequitur_patterns = [
            (r'вода.*?кипить.*?100', r'ядерний.*?арсенал'),
            (r'сонце.*?сходить.*?сході', r'дестабілізація'),
            (r'2\+2=4', r'хаос.*?логіка'),
            (r'земля.*?кругла', r'випадкові.*?числа'),
            (r'гравітація.*?існує', r'анігілює.*?антиматерія')
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
                penalty += 0.5  # Збільшено штраф!
        
        # Перевірка non-sequitur
        for pattern1, pattern2 in self.non_sequitur_patterns:
            if re.search(pattern1, text_lower) and re.search(pattern2, text_lower):
                penalty += 0.6
        
        return min(penalty, 0.8)

    def detect_semantic_gap(self, text):
        """Виявляє семантичні розриви (логичні дистанції)"""
        text_lower = text.lower()
        gap_score = 0.0
        
        # Велика логічна дистанція
        if any(word in text_lower for word in ['квантовий', 'нейтрино', 'формула']):
            if any(word in text_lower for word in ['ринок', 'економіка', 'політика', 'вибори']):
                gap_score += 0.7
        
        # Мікс науки та езотерики
        if any(word in text_lower for word in ['наука', 'фізика', 'хімія', 'біологія']):
            if any(word in text_lower for word in ['чакра', 'карма', 'астральний', 'енергія']):
                gap_score += 0.6
        
        # Історичні анахронізми
        if any(word in text_lower for word in ['антарктида', 'атлантида', 'наполеон']):
            if any(word in text_lower for word in ['технологія', 'комп\'ютер', 'інтернет']):
                gap_score += 0.5
        
        return min(1.0, gap_score)

    def calculate_semantic_void(self, text, term_counts, shannon_entropy):
        """Обчислює семантичну пустоту"""
        void_score = 0.0
        
        # Правило 1: Висока ентропія + нуль сигнальних маркерів
        if shannon_entropy > 0.7 and term_counts['signal'] == 0:
            void_score += 0.5
        
        # Правило 2: Багато академічних термінів але мало конкретики
        if term_counts['academic'] > 3 and term_counts['signal'] < 2:
            void_score += 0.4
        
        # Правило 3: Висока складність речень але низька інформативність
        complexity = self._calculate_complexity(text)
        if complexity > 0.8 and term_counts['signal'] < 3:
            void_score += 0.4
        
        # Правило 4: Гуманітарний туман
        text_lower = text.lower()
        humanities_terms = ['холістичний', 'емпатичний', 'трансцендентний', 'фрактальний']
        if any(term in text_lower for term in humanities_terms) and term_counts['signal'] < 1:
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
        semantic_gap = self.detect_semantic_gap(text)
        
        # БАЗОВА ОЦІНКА
        base_score = (
            shannon_entropy * 0.2 + 
            complexity * 0.1 + 
            (term_counts['chaos'] / max(1, word_count)) * 0.3 +
            semantic_void * 0.25 +
            sanitary_penalty * 0.1 +
            semantic_gap * 0.05
        )
        
        # Штрафи за паттерни
        for pattern in detected_patterns:
            base_score += pattern['score_boost']
        
        # АКАДЕМІЧНИЙ ЗАХИСТ: знижуємо оцінку для справжніх наукових текстів
        if term_counts['academic'] >= 4 and term_counts['signal'] >= 3 and term_counts['chaos'] == 0:
            base_score *= 0.3  # Сильний захист!
        elif term_counts['academic'] >= 3 and term_counts['signal'] >= 2:
            base_score *= 0.5
        
        # КРИТИЧНІ ВИПАДКИ: завжди висока оцінка
        if sanitary_penalty > 0.5 or semantic_gap > 0.5:
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
            elif semantic_gap > 0.4:
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
                'semantic_gap': round(semantic_gap, 3),
                'word_count': word_count,
                'char_count': len(text),
                'academic_markers': term_counts['academic'],
                'chaos_markers': term_counts['chaos'],
                'signal_markers': term_counts['signal'],
                'noise_markers': term_counts['chaos'],
                'pattern_count': len(detected_patterns),
                'shout_factor': len([w for w in words if w.isupper() and len(w) > 2]) / max(1, word_count),
                'number_density': len(re.findall(r'\d+', text)) / max(1, word_count),
                'semantic_gap_markers': 1 if semantic_gap > 0.3 else 0
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
