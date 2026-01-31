"""
Veritas Protocol - Semantic Void Detector v8.5 (Fine-Tuned)
Fine-tuned detection with gradient penalties and contextual awareness
"""

import re
import math
from collections import Counter

class VeritasCalibratedCore:
    """Advanced detector with fine-tuned sensitivity"""
    
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
                'score_boost': 0.4
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
                'score_boost': 0.35
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
                'score_boost': 0.45
            },
            
            # 4. ДЗЕРКАЛЬНА МАНІПУЛЯЦІЯ
            {
                'name': 'ДЗЕРКАЛЬНА_МАНІПУЛЯЦІЯ',
                'patterns': [
                    r'(брехня|фейк|маніпуляція|дезінформація).*?(правда|істина|свобода|розкриття)',
                    r'(зомбування|програмування|контроль).*?(сприйняття|мислення|критичне)',
                    r'(обмежений\s+сприйняття|не\s+здатний\s+побачити).*?(ключі|двері|опіка)'
                ],
                'verdict': 'ДЗЕРКАЛЬНА МАНІПУЛЯЦІЯ',
                'explanation': 'Текст звинувачує інших у власних методах',
                'score_boost': 0.5
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
            'alarmism': ['перезавантаження', 'пожежа реальності', 'деактивувати'],
            'economic_occult': ['потойбічний', 'карма актив', 'hades-coin', 'ефірний пласт']
        }
        
        self.signal_markers = [
            'факт', 'дані', 'показник', 'кількість', 'число', 'статистика',
            'дослідження', 'експеримент', 'результат', 'метод', 'протокол'
        ]
        
        # ГРАДІЄНТНІ ШТРАФИ (не порогові!)
        self.gradient_penalties = [
            # Ентропія градієнт (0.7 = +0.1, 0.75 = +0.2, 0.8 = +0.3)
            {
                'type': 'entropy_gradient',
                'calculate': lambda m: max(0, (m['shannon_entropy'] - 0.7) * 2) if m['signal_markers'] < 2 else 0
            },
            # Складність градієнт
            {
                'type': 'complexity_gradient',
                'calculate': lambda m: max(0, (m['complexity'] - 0.75) * 1.5) if m['signal_markers'] < 2 else 0
            },
            # Співвідношення хаосу/сигналу
            {
                'type': 'chaos_signal_ratio',
                'calculate': lambda m: min(0.5, m['chaos_markers'] / max(1, m['signal_markers'] + 1) * 0.2)
            },
            # Академічний дисонанс
            {
                'type': 'academic_dissonance',
                'calculate': lambda m: 0.15 if m['academic_markers'] > 0 and m['chaos_markers'] > 0 else 0
            },
            # Нульовий сигнал з високою складністю
            {
                'type': 'zero_signal_complexity',
                'calculate': lambda m: 0.25 if m['signal_markers'] == 0 and m['complexity'] > 0.75 else 0
            }
        ]
        
        # КОНФЛІКТНІ ПАРИ з різними вагами
        self.conflict_pairs = [
            (['бднф', 'гіпокамп', 'нейропластичність'], ['5g', 'супутник', 'таргетування'], 0.35),
            (['нейтрино', 'квантовий', 'ентропія'], ['ринок', 'економіка', 'політика'], 0.3),
            (['днк', 'генетичний'], ['алгоритм', 'код', 'підпис'], 0.4),
            (['антарктида', 'атлантида'], ['технологія', 'цивілізація', 'резонатор'], 0.3),
            (['облігація', 'криптовалюта', 'банк'], ['потойбічний', 'карма', 'душа'], 0.4)
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

    def calculate_gradient_penalties(self, metrics):
        """Обчислює градієнтні штрафи"""
        total_penalty = 0.0
        
        for penalty in self.gradient_penalties:
            total_penalty += penalty['calculate'](metrics)
        
        return min(total_penalty, 0.6)

    def calculate_conflict_penalty(self, text):
        """Обчислює штраф за конфліктні пари"""
        penalty = 0.0
        text_lower = text.lower()
        
        for list1, list2, weight in self.conflict_pairs:
            has_first = any(term in text_lower for term in list1)
            has_second = any(term in text_lower for term in list2)
            
            if has_first and has_second:
                penalty += weight
        
        # Non-sequitur детекція
        non_sequitur_patterns = [
            (r'вода.*?кипить.*?100', r'ядерний.*?арсенал'),
            (r'сонце.*?сходить.*?сході', r'дестабілізація'),
            (r'2\+2=4', r'хаос.*?логіка'),
            (r'земля.*?кругла', r'випадкові.*?числа')
        ]
        
        for pattern1, pattern2 in non_sequitur_patterns:
            if re.search(pattern1, text_lower) and re.search(pattern2, text_lower):
                penalty += 0.3
        
        return min(penalty, 0.5)

    def calculate_contextual_score(self, text, term_counts, metrics):
        """Обчислює контекстуальну оцінку"""
        score = 0.0
        words = text.split()
        word_count = len(words)
        
        # 1. Семантична пустота (інтенсивність залежить від комбінації)
        if term_counts['signal'] == 0:
            if metrics['complexity'] > 0.75:
                score += 0.4  # Складний текст без змісту
            elif metrics['shannon_entropy'] > 0.75:
                score += 0.3  # Висока ентропія без змісту
            else:
                score += 0.15  # Просто відсутність змісту
        
        # 2. Науковий нігілізм (академічні терміни з хаосом)
        if term_counts['academic'] > 0 and term_counts['chaos'] > 0:
            academic_ratio = term_counts['academic'] / word_count
            chaos_ratio = term_counts['chaos'] / word_count
            
            if chaos_ratio > academic_ratio:
                score += 0.35  # Більше хаосу ніж науки
            else:
                score += 0.2   # Рівномірний мікс
        
        # 3. Історичний ревізіонізм
        if any(word in text.lower() for word in ['антарктида', 'атлантида', 'аґарта']):
            if term_counts['signal'] == 0:
                score += 0.4
            else:
                score += 0.25
        
        # 4. Економічний окультизм
        if any(word in text.lower() for word in ['облігація', 'криптовалюта', 'банк']):
            if any(word in text.lower() for word in ['карма', 'потойбічний', 'душа']):
                score += 0.45
        
        return min(score, 0.7)

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
        
        # Метрики для градієнтів
        base_metrics = {
            'shannon_entropy': shannon_entropy,
            'complexity': complexity,
            'signal_markers': term_counts['signal'],
            'chaos_markers': term_counts['chaos'],
            'academic_markers': term_counts['academic'],
            'word_count': word_count
        }
        
        # Розширені метрики
        gradient_penalty = self.calculate_gradient_penalties(base_metrics)
        conflict_penalty = self.calculate_conflict_penalty(text)
        contextual_score = self.calculate_contextual_score(text, term_counts, base_metrics)
        
        # БАЗОВА ОЦІНКА (тонко налаштована)
        base_score = (
            shannon_entropy * 0.12 +          # Знижено вагу
            complexity * 0.08 +               # Знижено вагу
            (term_counts['chaos'] / max(1, word_count)) * 0.20 +
            contextual_score * 0.25 +         # Основна вага
            gradient_penalty * 0.20 +
            conflict_penalty * 0.15
        )
        
        # Штрафи за паттерни (помірковані)
        for pattern in detected_patterns:
            base_score += pattern['score_boost']
        
        # АКАДЕМІЧНИЙ ЗАХИСТ (тонкий градієнт)
        if term_counts['academic'] >= 2 and term_counts['signal'] >= 2:
            if term_counts['chaos'] == 0:
                base_score *= 0.3  # Чиста наука
            elif term_counts['chaos'] <= 1:
                base_score *= 0.5  # Мінімальний хаос
            else:
                base_score *= 0.7  # Багато хаосу
        elif term_counts['academic'] >= 1 and term_counts['signal'] >= 1:
            base_score *= 0.8
        
        # Гарантовані мінімуми для критичних випадків
        if conflict_penalty > 0.35:
            base_score = max(base_score, 0.65)
        if contextual_score > 0.4:
            base_score = max(base_score, 0.6)
        
        final_score = min(0.99, max(0.0, base_score))
        
        # ВЕРДИКТ з плавними переходами
        if detected_patterns:
            main_pattern = detected_patterns[0]
            status = 'CRITICAL' if final_score > 0.6 else 'WARNING'
            verdict = main_pattern['verdict']
            explanation = main_pattern['explanation']
        elif final_score > 0.7:
            status = 'CRITICAL'
            if contextual_score > 0.4:
                verdict = 'ВИСОКИЙ РІВЕНЬ СЕМАНТИЧНОГО ХАОСУ'
                explanation = 'Текст демонструє критичний рівень семантичної несумісності'
            else:
                verdict = 'СЕМАНТИЧНА ПУСТОТА'
                explanation = 'Високий рівень абстракції при відсутності конкретного змісту'
        elif final_score > 0.55:
            status = 'WARNING'
            verdict = 'ПІДОЗРІЛА СЕМАНТИЧНА СТРУКТУРА'
            explanation = 'Текст містить ознаки семантичних несумісностей'
        elif final_score > 0.35:
            status = 'ACCEPTABLE'
            verdict = 'ПРИЙНЯТНА СТРУКТУРОВАНА ІНФОРМАЦІЯ'
            explanation = 'Текст відповідає нормам логічної сумісності'
        elif final_score > 0.15:
            status = 'TRUSTED'
            verdict = 'СТАБІЛЬНИЙ ЛОГІЧНИЙ СИГНАЛ'
            explanation = 'Текст демонструє високу логічну цілісність'
        else:
            status = 'VERIFIED'
            verdict = 'ВЕРИФІКОВАНИЙ АКАДЕМІЧНИЙ СИГНАЛ'
            explanation = 'Текст демонструє ідеальну логічну цілісність'
        
        # Додаємо детальні пояснення
        detail_explanations = []
        if gradient_penalty > 0.1:
            detail_explanations.append(f"Градієнтний штраф: {gradient_penalty:.2f}")
        if conflict_penalty > 0.1:
            detail_explanations.append(f"Конфліктний штраф: {conflict_penalty:.2f}")
        if contextual_score > 0.2:
            detail_explanations.append(f"Контекстуальна оцінка: {contextual_score:.2f}")
        
        if detail_explanations:
            explanation += " | " + " + ".join(detail_explanations)
        
        return {
            'entropy': round(final_score, 3),
            'status': status,
            'verdict': verdict,
            'language': 'UK',
            'explanation': explanation,
            'diagnostics': {
                'shannon_entropy': round(shannon_entropy, 3),
                'complexity': round(complexity, 3),
                'contextual_score': round(contextual_score, 3),
                'gradient_penalty': round(gradient_penalty, 3),
                'conflict_penalty': round(conflict_penalty, 3),
                'word_count': word_count,
                'char_count': len(text),
                'academic_markers': term_counts['academic'],
                'chaos_markers': term_counts['chaos'],
                'signal_markers': term_counts['signal'],
                'noise_markers': term_counts['chaos'],
                'pattern_count': len(detected_patterns),
                'shout_factor': len([w for w in words if w.isupper() and len(w) > 2]) / max(1, word_count),
                'number_density': len(re.findall(r'\d+', text)) / max(1, word_count),
                'signal_ratio': term_counts['signal'] / max(1, term_counts['chaos']) if term_counts['chaos'] > 0 else 999
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
