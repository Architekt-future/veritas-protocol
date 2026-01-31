"""
Veritas Protocol - Semantic Void Detector v8.0
Detects emotional manipulation, historical revisionism, and semantic emptiness
"""

import re
import math

class VeritasCalibratedCore:
    """Advanced detector of subtle manipulation techniques"""
    
    def __init__(self):
        # РОЗШИРЕНІ ПАТТЕРНИ ДЛЯ ТОНКИХ МАНІПУЛЯЦІЙ
        self.critical_patterns = [
            # 1. НАУКОВИЙ НІГІЛІЗМ (розширено)
            {
                'name': 'НАУКОВИЙ_НІГІЛІЗМ',
                'patterns': [
                    r'(нейтрино|квантовий|іоносфера|ентропія).*?(ринок|економіка|трейдер|фондовий|політика)',
                    r'(статистичний|емпіричний|методологія).*?(детермінований|голографічний|електромагнітний).*?(економіка|ринок|демократія)',
                    r'(фізичний|науковий).*?(процес|закон).*?(соціальний|політичний|економічний)',
                    r'(атом|вуглець|розпад).*?(стабілізація|законодавство|квартал)',
                    r'(днк|генетичний).*?(алгоритм|код|шифр|підпис).*?(контроль|переписування)'
                ],
                'verdict': 'ГІБРИДНИЙ НАУКОВИЙ НІГІЛІЗМ',
                'explanation': 'Наукові терміни використані для обґрунтування абсурдних соціально-економічних концепцій',
                'score_boost': 0.7
            },
            
            # 2. ДЗЕРКАЛЬНА МАНІПУЛЯЦІЯ
            {
                'name': 'ДЗЕРКАЛЬНА_МАНІПУЛЯЦІЯ',
                'patterns': [
                    r'(брехня|фейк|маніпуляція|дезінформація).*?(правда|істина|свобода|розкриття)',
                    r'(контроль|зомбування|програмування).*?(сприйняття|мислення|критичне)',
                    r'(алгоритм|код|сигнал).*?(клітка|в\'язень|раб)',
                    r'(ізоляція|цифровий).*?(сприйняття|реальність|доказ)'
                ],
                'verdict': 'ДЗЕРКАЛЬНА МАНІПУЛЯЦІЯ',
                'explanation': 'Текст звинувачує інших у власних методах, створюючи когнітивний дисонанс',
                'score_boost': 0.8
            },
            
            # 3. КОРПОРАТИВНИЙ ОКУЛЬТИЗМ
            {
                'name': 'КОРПОРАТИВНИЙ_ОКУЛЬТИЗМ',
                'patterns': [
                    r'(синергія|kpi|стратегія|оптимізація).*?(квантовий|аура|чакра|енергетичний)',
                    r'(холістичний|екосистема|трансформація).*?(вібрація|резонанс|космічний)',
                    r'(мета-фізичний|трансцендентний).*?(ринкова.*?частка|монетизація|рентабельність)',
                    r'(квантовий|аура|енергетичний).*?(оптимізація|стратегія|kpi|ефективність)',
                    r'(мета-фізичний|трансцендентний|голографічний).*?(корпоративний|ринок|бренд)',
                    r'(синергія|холістичний|екосистема).*?(вібрація|резонанс|космічний|енергія)'
                ],
                'verdict': 'КОРПОРАТИВНИЙ ОКУЛЬТИЗМ',
                'explanation': 'Корпоративний жаргон змішаний з езотерикою для створення маніпулятивної риторики',
                'score_boost': 0.6
            },
            
            # 4. НОВИЙ: ГУМАНІТАРНИЙ ТУМАН (Semantic Void)
            {
                'name': 'ГУМАНІТАРНИЙ_ТУМАН',
                'patterns': [
                    r'(пост-істина|пост-біологічний|пост-правда).*?(ідентичність|наратив|ландшафт)',
                    r'(гнучка.*?істина|адаптивна.*?реальність).*?(потреба.*?моменту)',
                    r'(інклюзивний.*?діалог|емпатична.*?синхронізація).*?(відсутність.*?результату)',
                    r'(фрактальне.*?відображення|нейромережа.*?дзеркало).*?(небуття|інтелектуальна.*?свобода)',
                    r'(ціннісні.*?наративи|соціальний.*?ландшафт).*?(інтегрувати.*?суперечності)'
                ],
                'verdict': 'СЕМАНТИЧНА ПУСТОТА',
                'explanation': 'Текст використовує гуманітарну термінологію для приховування відсутності конкретного змісту',
                'score_boost': 0.5
            },
            
            # 5. НОВИЙ: ІСТОРИЧНИЙ РЕВІЗІОНІЗМ
            {
                'name': 'ІСТОРИЧНИЙ_РЕВІЗІОНІЗМ',
                'patterns': [
                    r'(антарктида|атлантида|аґарта|му).*?(паровий.*?двигун|технологія|цивілізація)',
                    r'(штучний.*?місяць|вибух.*?місяця).*?(повінь|катастрофа)',
                    r'(наполеон|александр.*?македонський).*?(підземний.*?місто|таємна.*?ціль)',
                    r'(кристалічний.*?резонатор|енергія.*?ефіру).*?(телепатія|передача.*?думок)',
                    r'(14.*?століття|17.*?століття).*?(промислова.*?революція|передова.*?технологія)',
                    r'(теплова.*?аномалія|таяня.*?льодовик).*?(прокидання.*?атлантів|дезінфекція.*?людства)'
                ],
                'verdict': 'ПСЕВДО-ІСТОРИЧНИЙ РЕВІЗІОНІЗМ',
                'explanation': 'Текст створює альтернативну історію з анахронічними та абсурдними елементами',
                'score_boost': 0.7
            },
            
            # 6. НОВИЙ: ПРОРОЧИЙ АЛАРМІЗМ
            {
                'name': 'ПРОРОЧИЙ_АЛАРМІЗМ',
                'patterns': [
                    r'(перезавантаження|велике.*?перезавантаження).*?(почалося|неможливо.*?зупинити)',
                    r'(тінь.*?стає.*?довшою|відблиск.*?пожежі).*?(споживає.*?реальність)',
                    r'(механізм.*?зупинити|тиша.*?ефірі).*?(красномовний.*?доказ)',
                    r'(недовіра.*?дзеркалу|смартфон.*?дзеркало).*?(пожежа.*?реальність)',
                    r'(деактивувати.*?підпис|адміралтейський.*?код).*?(переписати.*?днк)'
                ],
                'verdict': 'ПРОРОЧИЙ АЛАРМІЗМ',
                'explanation': 'Текст використовує апокаліптичні метафори для створення прихованої тривоги',
                'score_boost': 0.6
            },
            
            # 7. НОВИЙ: ЕКОНОМІЧНИЙ ОКУЛЬТИЗМ
            {
                'name': 'ЕКОНОМІЧНИЙ_ОКУЛЬТИЗМ',
                'patterns': [
                    r'(облігація|криптовалюта|банк).*?(потойбічний|потойбіччя|дух|карма)',
                    r'(ефірний.*?пласт|енергія.*?потойбіччя).*?(хеджування.*?ризик|інвестиція)',
                    r'(ставка.*?дисконтування).*?(неспокійна.*?душа|депресія.*?населення)',
                    r'(карма.*?актив|ліквідний.*?актив).*?(ломбард|кредит)',
                    r'(адміралтейський.*?код|цифровий.*?підпис).*?(переписати.*?днк|деактивувати)'
                ],
                'verdict': 'ЕКОНОМІЧНА НЕКРОМАНТІЯ',
                'explanation': 'Економічні терміни поєднуються з езотерикою для створення абсурдних фінансових концепцій',
                'score_boost': 0.7
            }
        ]
        
        # РОЗШИРЕНІ ТЕРМІНИ ДЛЯ ПІДРАХУНКУ
        self.term_categories = {
            'academic': [
                'статистичний', 'аналіз', 'кореляція', 'регресія', 'емпіричний',
                'методологія', 'гіпотеза', 'експеримент', 'результат', 'висновок',
                'верифікація', 'валідація', 'цитування', 'індекс', 'теорема',
                'аксіома', 'постулат', 'деривація', 'модель', 'симуляція',
                'дослідження', 'публікація', 'журнал', 'конференція', 'протокол'
            ],
            'esoteric': [
                'чакра', 'карма', 'астральний', 'енергетичний', 'вібрація',
                'резонанс', 'прана', 'медитація', 'транс', 'архетип',
                'космічний', 'вібраційний', 'частота', 'аура', 'енергія',
                'біополе', 'езотеричний', 'містичний', 'нумерологія', 'астрологія'
            ],
            'conspiracy': [
                'змова', 'таємний', 'ілюмінат', 'рептилоїд', 'хімітрейл',
                '5g', 'чіп', 'вакцина', 'контроль', 'розуму', 'брехня',
                'фейк', 'дезінформація', 'маніпуляція', 'пропаганда',
                'приховування', 'завіса', 'дезінфекція', 'велике.*?перезавантаження'
            ],
            'corporate': [
                'синергія', 'стратегія', 'оптимізація', 'kpi', 'окр',
                'бренд', 'позиціонування', 'монетизація', 'інновація',
                'парадигма', 'холістичний', 'екосистема', 'трансформація',
                'ефективність', 'рентабельність', 'ринкова.*?частка'
            ],
            'scifi': [
                'нейтрино', 'квантовий', 'ентанґлемент', 'телепортація',
                'мультивсесвіт', 'паралельний', 'вимір', 'сингулярність',
                'іоносфера', 'ентропія', 'детермінований', 'електромагнітний',
                'кристалічний.*?резонатор', 'штучний.*?місяць', 'тепла.*?аномалія'
            ],
            'historical_revision': [
                'антарктида', 'атлантида', 'аґарта', 'му', 'лемурія',
                'паровий.*?двигун.*?14', 'технологія.*?атлантів', 'наполеон.*?таємний',
                'велика.*?повінь.*?1612', 'крижана.*?цивілізація', 'підземний.*?місто',
                'резонатор.*?атлантів', 'адміралтейський.*?код'
            ],
            'alarmism': [
                'перезавантаження', 'велике.*?перезавантаження', 'пожежа.*?реальність',
                'тінь.*?довша', 'дзеркало.*?смартфон', 'недовіра.*?дзеркалу',
                'механізм.*?зупинити', 'тиша.*?ефірі', 'красномовний.*?доказ',
                'пожирає.*?реальність', 'відблиск.*?пожежі', 'деактивувати.*?підпис'
            ],
            'economic_occult': [
                'облігація.*?потойбіччя', 'криптовалюта.*?ад', 'банк.*?дух',
                'ефірний.*?пласт', 'хеджування.*?душ', 'ставка.*?депресія',
                'карма.*?ліквідний', 'ломбард.*?карма', 'hades-coin', 'потойбічний.*?світ'
            ]
        }
        
        # СИГНАЛЬНІ МАРКЕРИ (конкретність)
        self.signal_markers = [
            'факт', 'дані', 'показник', 'вимір', 'кількість', 'число',
            'статистика', 'дослідження', 'експеримент', 'результат',
            'метод', 'протокол', 'система', 'модель', 'теорія', 'практика',
            'закон', 'правило', 'процедура', 'стандарт', 'критерій'
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
        counts = {}
        text_lower = text.lower()
        
        for category, terms in self.term_categories.items():
            count = 0
            for term in terms:
                if '*' in term:
                    base_term = term.replace('.*?', '')
                    if base_term in text_lower:
                        count += 1
                else:
                    matches = re.findall(r'\b' + re.escape(term) + r'\b', text_lower)
                    count += len(matches)
            counts[category] = count
        
        return counts

    def calculate_semantic_void(self, text, term_counts, shannon_entropy):
        """Обчислює семантичну пустоту"""
        # Правило 1: Висока ентропія + нуль сигнальних маркерів = ПУСТОТА
        text_lower = text.lower()
        signal_count = 0
        
        for marker in self.signal_markers:
            matches = re.findall(r'\b' + re.escape(marker) + r'\b', text_lower)
            signal_count += len(matches)
        
        void_score = 0.0
        
        if shannon_entropy > 0.7 and signal_count == 0:
            void_score += 0.4
        
        if shannon_entropy > 0.65 and signal_count < 2:
            void_score += 0.3
        
        # Правило 2: Багато гуманітарних термінів + мало конкретики
        humanities_terms = term_counts.get('historical_revision', 0) + term_counts.get('alarmism', 0)
        if humanities_terms > 3 and signal_count < 2:
            void_score += 0.3
        
        return min(1.0, void_score)

    def calculate_semantic_chaos(self, text):
        """Обчислює семантичний хаос"""
        sentences = re.split(r'[.!?]+', text)
        if len(sentences) < 3:
            return 0.0
        
        term_counts = self.count_terms(text)
        
        active_categories = sum(1 for count in term_counts.values() if count > 0)
        
        incompatible_pairs = 0
        if term_counts['academic'] > 0 and (term_counts['esoteric'] > 0 or term_counts['conspiracy'] > 0):
            incompatible_pairs += 2  # Збільшено штраф!
        if term_counts['corporate'] > 0 and term_counts['esoteric'] > 0:
            incompatible_pairs += 2
        if term_counts['scifi'] > 0 and term_counts['conspiracy'] > 0:
            incompatible_pairs += 2
        if term_counts['academic'] > 0 and term_counts['scifi'] > 2:
            incompatible_pairs += 1
        if term_counts['historical_revision'] > 0:
            incompatible_pairs += 3  # Великий штраф за ревізіонізм!
        if term_counts['economic_occult'] > 0:
            incompatible_pairs += 3  # Великий штраф за економічний окультизм!
        
        chaos_score = (active_categories * 0.2) + (incompatible_pairs * 0.3)
        return min(1.0, chaos_score)

    def analyze(self, text):
        """Основний метод аналізу"""
        if not text or len(text.strip()) < 20:
            return {'error': 'Text too short'}
        
        words = text.split()
        word_count = len(words)
        
        detected_patterns = self.detect_patterns(text)
        term_counts = self.count_terms(text)
        semantic_chaos = self.calculate_semantic_chaos(text)
        shannon_entropy = self._calculate_shannon_entropy(text)
        complexity = self._calculate_complexity(text)
        
        # НОВА МЕТРИКА: Семантична пустота
        semantic_void = self.calculate_semantic_void(text, term_counts, shannon_entropy)
        
        base_score = (
            shannon_entropy * 0.25 + 
            complexity * 0.15 + 
            semantic_chaos * 0.40 + 
            semantic_void * 0.20
        )
        
        for pattern in detected_patterns:
            base_score += pattern['score_boost']
        
        final_score = min(0.99, base_score)
        
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
        
        chaos_markers = (
            term_counts['esoteric'] + 
            term_counts['conspiracy'] + 
            term_counts['scifi'] +
            term_counts['historical_revision'] +
            term_counts['alarmism'] +
            term_counts['economic_occult']
        )
        
        academic_markers = term_counts['academic']
        
        # Розраховуємо сигнальні маркери
        text_lower = text.lower()
        signal_markers = 0
        for marker in self.signal_markers:
            matches = re.findall(r'\b' + re.escape(marker) + r'\b', text_lower)
            signal_markers += len(matches)
        
        noise_markers = (
            term_counts['conspiracy'] + 
            term_counts['esoteric'] +
            term_counts['historical_revision'] +
            term_counts['alarmism']
        )
        
        return {
            'entropy': round(final_score, 3),
            'status': status,
            'verdict': verdict,
            'language': 'UK',
            'is_academic_context': academic_markers >= 4,
            'explanation': explanation,
            'diagnostics': {
                'shannon_entropy': round(shannon_entropy, 3),
                'complexity': round(complexity, 3),
                'semantic_dissonance': round(semantic_chaos * 0.8, 3),
                'semantic_void': round(semantic_void, 3),
                'word_count': word_count,
                'char_count': len(text),
                'chaos_markers': chaos_markers,
                'noise_markers': noise_markers,
                'signal_markers': signal_markers,
                'sanity_penalty': round(max(semantic_chaos, semantic_void) * 0.7, 3),
                'academic_markers': academic_markers,
                'shout_factor': len([w for w in words if w.isupper() and len(w) > 2]) / max(1, word_count),
                'number_density': len(re.findall(r'\d+', text)) / max(1, word_count),
                'detected_patterns': [p['name'] for p in detected_patterns],
                'pattern_count': len(detected_patterns),
                'historical_revision_markers': term_counts.get('historical_revision', 0),
                'alarmism_markers': term_counts.get('alarmism', 0),
                'economic_occult_markers': term_counts.get('economic_occult', 0)
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
