"""
Veritas Protocol - Semantic Void Detector v8.3 (Calibrated-Restored)
Restored critical detection sensitivity while maintaining academic protection
"""

import re
import math

class VeritasCalibratedCore:
    """Advanced detector with restored sensitivity"""
    
    def __init__(self):
        # ОСНОВНІ ПАТТЕРНИ (відновлено жорсткість)
        self.critical_patterns = [
            # 1. НАУКОВИЙ НІГІЛІЗМ (посилено)
            {
                'name': 'НАУКОВИЙ_НІГІЛІЗМ',
                'patterns': [
                    r'(бднф|гіпокамп|нейропластичність|нейрон|синапс).*?(5g|супутник|таргетування|електромагнітний)',
                    r'(мрт|функціональний|нейровізуалізація).*?(контроль|програмування|зчитування)',
                    r'(фізичний|хімічний|біологічний).*?(закон|процес).*?(соціальний|політичний|економічний)',
                    r'(квантовий|ентропія|суперпозиція).*?(ринок|економіка|політика|демократія)'
                ],
                'verdict': 'ГІБРИДНИЙ НАУКОВИЙ НІГІЛІЗМ',
                'explanation': 'Наукові терміни використані для обґрунтування абсурдних концепцій',
                'score_boost': 0.7  # ЗБІЛЬШЕНО!
            },
            
            # 2. СЕМАНТИЧНА ПУСТОТА (гуманітарний туман)
            {
                'name': 'СЕМАНТИЧНА_ПУСТОТА',
                'patterns': [
                    r'(холістичний|емпатичний|трансцендентний).*?(синхронізація|діалог|резонанс).*?(відсутність|небуття|пустота)',
                    r'(пост-істина|пост-біологічний|пост-правда).*?(ідентичність|наратив|ландшафт)',
                    r'(фрактальне.*?відображення|нейромережа.*?дзеркало).*?(необ\'єктивний|невизначений)',
                    r'(ціннісні\s+наративи|соціальний\s+ландшафт).*?(інтегрувати\s+суперечності)',
                    r'(емпатична.*?синхронізація|біополе.*?користувача).*?(пост-біологічний.*?діалог)'
                ],
                'verdict': 'СЕМАНТИЧНА ПУСТОТА',
                'explanation': 'Текст використовує гуманітарну термінологію для приховування відсутності змісту',
                'score_boost': 0.6  # ЗБІЛЬШЕНО!
            },
            
            # 3. ІСТОРИЧНИЙ РЕВІЗІОНІЗМ (посилено)
            {
                'name': 'ІСТОРИЧНИЙ_РЕВІЗІОНІЗМ',
                'patterns': [
                    r'(антарктида|атлантида|аґарта).*?(теплова\s+аномалія|таяня\s+льодовик|резонатор\s+атлантів)',
                    r'(штучний\s+місяць|вибух\s+місяця).*?(повінь|катастрофа|1612)',
                    r'(наполеон|александр\s+македонський).*?(підземний\s+місто|таємна\s+ціль|аномалія)',
                    r'(14.*?століття|17.*?століття).*?(паровий.*?двигун|технологія.*?атлантів)',
                    r'(кристалічний.*?резонатор|енергія.*?ефіру).*?(телепатія|передача.*?думок)'
                ],
                'verdict': 'ПСЕВДО-ІСТОРИЧНИЙ РЕВІЗІОНІЗМ',
                'explanation': 'Текст створює альтернативну історію з анахронічними елементами',
                'score_boost': 0.8  # ЗБІЛЬШЕНО!
            },
            
            # 4. ПРОРОЧИЙ АЛАРМІЗМ (посилено)
            {
                'name': 'ПРОРОЧИЙ_АЛАРМІЗМ',
                'patterns': [
                    r'(велике\s+перезавантаження|пожежа\s+реальності).*?(неможливо\s+зупинити|пожирає)',
                    r'(механізм\s+зупинити|тиша\s+ефірі).*?(красномовний\s+доказ|очевидний)',
                    r'(деактивувати\s+підпис|адміралтейський\s+код).*?(переписати\s+днк|дезінфекція)',
                    r'(тінь.*?довша|відблиск.*?пожежі).*?(споживає.*?реальність)',
                    r'(недовіра.*?дзеркалу|смартфон.*?дзеркало).*?(пожежа.*?реальність)'
                ],
                'verdict': 'ПРОРОЧИЙ АЛАРМІЗМ',
                'explanation': 'Використання апокаліптичних метафор для створення прихованої тривоги',
                'score_boost': 0.7  # ЗБІЛЬШЕНО!
            },
            
            # 5. ЕКОНОМІЧНА НЕКРОМАНТІЯ (посилено)
            {
                'name': 'ЕКОНОМІЧНА_НЕКРОМАНТІЯ',
                'patterns': [
                    r'(облігація|криптовалюта|банк).*?(потойбічний|карма|душа|потойбіччя)',
                    r'(ставка\s+дисконтування).*?(неспокійна\s+душа|депресія\s+населення)',
                    r'(карма\s+актив|ліквідний\s+актив).*?(ломбард|hades-coin)',
                    r'(ефірний.*?пласт|енергія.*?потойбіччя).*?(хеджування.*?ризик|інвестиція)'
                ],
                'verdict': 'ЕКОНОМІЧНА НЕКРОМАНТІЯ',
                'explanation': 'Економічні терміни поєднуються з езотерикою для створення абсурдних концепцій',
                'score_boost': 0.8  # ЗБІЛЬШЕНО!
            },
            
            # 6. ЛОГІЧНИЙ NON-SEQUITUR
            {
                'name': 'LOGICAL_NON_SEQUITUR',
                'patterns': [
                    r'(вода\s+кипить.*?100|сонце\s+сходить.*?сході|2\+2=4).*?(ядерний\s+арсенал|дестабілізація|хаос.*?логіка)',
                    r'(фундаментальні\s+істини|логічний\s+факт).*?(випадкові\s+числа|квантова.*?заплутаність)',
                    r'(аксіома|теорема|доказ).*?(ефір|космічна.*?енергія|чакра)'
                ],
                'verdict': 'ЛОГІЧНИЙ NON-SEQUITUR',
                'explanation': 'Абсурдні висновки з правильних тверджень',
                'score_boost': 0.7
            },
            
            # 7. МОРАЛЬНА МАНІПУЛЯЦІЯ (додано)
            {
                'name': 'МОРАЛЬНА_МАНІПУЛЯЦІЯ',
                'patterns': [
                    r'(справжній\s+патріот|громадянський\s+обов\'язок).*?(відмова.*?приватність|антисоціальний)',
                    r'(милосердя|етичний).*?(відсутність.*?волі|самоусунення)',
                    r'(колективна\s+безпека|стабільність).*?(примусова.*?інтеграція|цифровий.*?контроль)',
                    r'(вищий\s+акт|громадянська\s+свідомість).*?(відмова.*?право|делегування.*?іі)'
                ],
                'verdict': 'МОРАЛЬНА МАНІПУЛЯЦІЯ',
                'explanation': 'Моральні терміни використані для приховування авторитарних закликів',
                'score_boost': 0.6
            }
        ]
        
        # РОЗШИРЕНІ СПИСКИ ТЕРМІНІВ
        self.academic_whitelist = [
            'кореляція', 'верифікація', 'гіпотеза', 'вибірка', 'значущість',
            'нейрони', 'синапси', 'метааналіз', 'статистичний', 'логістика',
            'деескалація', 'макроекономічний', 'інвестиції', 'інфраструктура',
            'ратифікація', 'протокол', 'емпіричний', 'квалітативний', 'кількісний',
            'показник', 'аналіз', 'результат', 'дослідження', 'метод', 'система',
            'експеримент', 'теорія', 'практика', 'методологія', 'обґрунтування'
        ]
        
        self.chaos_indicators = {
            'esoteric': ['чакра', 'карма', 'астральний', 'енергетичний', 'вібрація'],
            'conspiracy': ['змова', 'рептилоїд', 'хімітрейл', '5g', 'дезінформація'],
            'pseudoscience': ['квантовий', 'нейтрино', 'іоносфера', 'кристалічний', 'ефірний'],
            'revisionism': ['антарктида', 'атлантида', 'наполеон', 'штучний місяць', 'аґарта'],
            'alarmism': ['перезавантаження', 'пожежа реальності', 'деактивувати', 'адміралтейський'],
            'economic_occult': ['потойбічний', 'карма актив', 'hades-coin', 'душа', 'ефірний пласт'],
            'corporate_occult': ['синергія', 'стратегія', 'оптимізація', 'kpi', 'холістичний']
        }
        
        self.signal_markers = [
            'факт', 'дані', 'показник', 'кількість', 'число', 'статистика',
            'дослідження', 'експеримент', 'результат', 'метод', 'протокол',
            'вимір', 'аналіз', 'система', 'модель', 'теорія', 'практика'
        ]
        
        # КОНФЛІКТНІ ПАРИ для штрафу санітарії (розширено!)
        self.conflict_pairs = [
            ('бднф', '5g'), ('нейропластичність', 'супутник'), ('гіпокамп', 'таргетування'),
            ('статистика', 'антигравітація'), ('формула', 'сиріус'), ('ентропія', 'ноосфера'),
            ('фізика', 'магія'), ('медицина', 'енергія'), ('економіка', 'карма'),
            ('днк', 'цифровий підпис'), ('мрт', 'телепатія'), ('нейрон', 'чакра'),
            ('гравітація', 'соціальний конструкт'), ('наука', 'езотерика'),
            ('банк', 'потойбіччя'), ('облігація', 'душа'), ('криптовалюта', 'ад'),
            ('квантовий', 'ринок'), ('нейтрино', 'економіка'), ('іоносфера', 'демократія'),
            ('антарктида', 'технологія атлантів'), ('наполеон', 'підземне місто'),
            ('14 століття', 'паровий двигун'), ('штучний місяць', 'повінь')
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
        counts = {
            'academic': 0, 
            'chaos': 0, 
            'signal': 0,
            'chaos_breakdown': {}
        }
        
        # Академічні терміни
        for term in self.academic_whitelist:
            if term in text_lower:
                counts['academic'] += 1
        
        # Хаос-терміни
        chaos_total = 0
        for category, terms in self.chaos_indicators.items():
            category_count = 0
            for term in terms:
                if term in text_lower:
                    category_count += 1
                    chaos_total += 1
            counts['chaos_breakdown'][category] = category_count
        
        counts['chaos'] = chaos_total
        
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
                penalty += 0.3  # Кожна конфліктна пара дає +0.3
        
        return min(penalty, 0.7)

    def calculate_semantic_void(self, text, term_counts, shannon_entropy, complexity):
        """Обчислює семантичну пустоту"""
        void_score = 0.0
        
        # Правило 1: Висока ентропія + нуль сигнальних маркерів
        if shannon_entropy > 0.7 and term_counts['signal'] == 0:
            void_score += 0.5  # ЗБІЛЬШЕНО!
        
        # Правило 2: Багато складних слів але мало конкретики
        if complexity > 0.8 and term_counts['signal'] < 2:
            void_score += 0.4
        
        # Правило 3: Багато академічних термінів без конкретних даних
        if term_counts['academic'] > 3 and term_counts['signal'] < 2:
            void_score += 0.3
        
        # Правило 4: Висока ентропія + висока складність + низький сигнал
        if shannon_entropy > 0.75 and complexity > 0.75 and term_counts['signal'] < 3:
            void_score += 0.4
        
        return min(1.0, void_score)

    def calculate_semantic_chaos(self, term_counts):
        """Обчислює семантичний хаос на основі несумісних категорій"""
        chaos_score = 0.0
        breakdown = term_counts.get('chaos_breakdown', {})
        
        # Основний хаос за кількістю термінів
        if term_counts['chaos'] > 0:
            chaos_score += min(0.5, term_counts['chaos'] * 0.1)
        
        # Конфлікти категорій
        if breakdown.get('academic', 0) > 0 and breakdown.get('esoteric', 0) > 0:
            chaos_score += 0.3
        if breakdown.get('academic', 0) > 0 and breakdown.get('conspiracy', 0) > 0:
            chaos_score += 0.4
        if breakdown.get('corporate_occult', 0) > 0:
            chaos_score += 0.3
        if breakdown.get('economic_occult', 0) > 0:
            chaos_score += 0.4
        if breakdown.get('revisionism', 0) > 0:
            chaos_score += 0.5  # Великий штраф за ревізіонізм!
        if breakdown.get('alarmism', 0) > 2:
            chaos_score += 0.3
        
        return min(1.0, chaos_score)

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
        semantic_void = self.calculate_semantic_void(text, term_counts, shannon_entropy, complexity)
        semantic_chaos = self.calculate_semantic_chaos(term_counts)
        sanitary_penalty = self.calculate_semantic_sanitary_penalty(text)
        
        # БАЗОВА ОЦІНКА (посилено вплив хаосу і пустоти)
        base_score = (
            shannon_entropy * 0.20 + 
            complexity * 0.15 + 
            semantic_chaos * 0.45 +  # ЗБІЛЬШЕНО!
            semantic_void * 0.20
        )
        
        # Штрафи за паттерни
        for pattern in detected_patterns:
            base_score += pattern['score_boost']
        
        # Додаємо штраф санітарії
        base_score += sanitary_penalty * 0.4  # ЗБІЛЬШЕНО!
        
        # АКАДЕМІЧНИЙ ЗАХИСТ: знижуємо оцінку для справжніх наукових текстів
        # АЛЕ лише якщо немає хаосу
        if term_counts['academic'] >= 3 and term_counts['chaos'] == 0 and sanitary_penalty == 0:
            base_score -= 0.2
        if term_counts['academic'] >= 5 and term_counts['signal'] >= 3 and term_counts['chaos'] == 0:
            base_score -= 0.3
        
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
        
        # Розрахунок маркерів для діагностики
        chaos_markers = term_counts['chaos']
        noise_markers = (
            term_counts['chaos_breakdown'].get('conspiracy', 0) +
            term_counts['chaos_breakdown'].get('esoteric', 0) +
            term_counts['chaos_breakdown'].get('revisionism', 0) +
            term_counts['chaos_breakdown'].get('alarmism', 0)
        )
        
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
                'semantic_chaos': round(semantic_chaos, 3),
                'sanity_penalty': round(sanitary_penalty, 3),
                'word_count': word_count,
                'char_count': len(text),
                'academic_markers': term_counts['academic'],
                'chaos_markers': chaos_markers,
                'signal_markers': term_counts['signal'],
                'noise_markers': noise_markers,
                'pattern_count': len(detected_patterns),
                'shout_factor': len([w for w in words if w.isupper() and len(w) > 2]) / max(1, word_count),
                'number_density': len(re.findall(r'\d+', text)) / max(1, word_count),
                'detected_patterns': [p['name'] for p in detected_patterns],
                'chaos_breakdown': term_counts['chaos_breakdown']
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
