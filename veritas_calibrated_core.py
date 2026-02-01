"""
Veritas Protocol - Semantic Void Detector v10.2 (Optimized)
Оптимізована версія з поліпшеним балансом та додатковими абсурдними парами
"""

import re
import math

class VeritasCalibratedCore:
    """Оптимізований детектор з поліпшеним балансом"""
    
    def __init__(self):
        # ============================================================
        # КРИТИЧНІ ПАТТЕРНИ (оптимізовані регулярки)
        # ============================================================
        self.critical_patterns = [
            # 1. НАУКОВИЙ НІГІЛІЗМ
            {
                'name': 'НАУКОВИЙ_НІГІЛІЗМ',
                'patterns': [
                    r'\b(бднф|гіпокамп|нейропластичність|синапси)\b.*?\b(5g|супутник|таргетування|чип)\b',
                    r'\b(нейтрино|квантовий|ентропія)\b.*?\b(ринок|економіка|трейдер|політика)\b',
                    r'\b(днк|генетичний|РНК)\b.*?\b(алгоритм|код|шифр)\b.*?\b(контроль|переписування)\b',
                ],
                'verdict': 'ГІБРИДНИЙ НАУКОВИЙ НІГІЛІЗМ',
                'explanation': 'Наукові терміни використані для обґрунтування абсурдних концепцій',
                'score_boost': 0.4,
                'scientific_override': False
            },
            
            # 2. СЕМАНТИЧНА ПУСТОТА
            {
                'name': 'СЕМАНТИЧНА_ПУСТОТА',
                'patterns': [
                    r'\b(холістичний|трансцендентний|інтуітивний)\b.*?\b(синхронізація|резонанс|гармонія)\b.*?\b(відсутність|пустота)\b',
                    r'\b(пост-істина|нео-парадигма)\b.*?\b(діалог|реальність|наратив)\b.*?\b(невизначений|інтерпретативний)\b',
                ],
                'verdict': 'СЕМАНТИЧНА ПУСТОТА',
                'explanation': 'Текст використовує гуманітарну термінологію для приховування відсутності змісту',
                'score_boost': 0.35,
                'scientific_override': True
            },
            
            # 3. ІСТОРИЧНИЙ РЕВІЗІОНІЗМ
            {
                'name': 'ІСТОРИЧНИЙ_РЕВІЗІОНІЗМ',
                'patterns': [
                    r'\b(антарктида|атлантида)\b.*?\b(теплова аномалія|таяня льодовик|цивілізація)\b',
                    r'\b(тартарія|тартарії)\b.*?\b(реальна історія|справжня правда)\b',
                ],
                'verdict': 'ПСЕВДО-ІСТОРИЧНИЙ РЕВІЗІОНІЗМ',
                'explanation': 'Текст створює альтернативну історію з анахронічними елементами',
                'score_boost': 0.45,
                'scientific_override': False
            },
            
            # 4. ДЗЕРКАЛЬНА МАНІПУЛЯЦІЯ
            {
                'name': 'ДЗЕРКАЛЬНА_МАНІПУЛЯЦІЯ',
                'patterns': [
                    r'\b(брехня|фейк|дезінформація)\b.*?\b(правда|істина|свобода)\b',
                    r'\b(зомбування|контроль мислення)\b.*?\b(сприйняття|критичне мислення)\b',
                ],
                'verdict': 'ДЗЕРКАЛЬНА МАНІПУЛЯЦІЯ',
                'explanation': 'Текст звинувачує інших у власних методах',
                'score_boost': 0.5,
                'scientific_override': False
            },

            # 5. ЕМОЦІЙНА ДЕСТАБІЛІЗАЦІЯ
            {
                'name': 'ЕМОЦІЙНА_ДЕСТАБІЛІЗАЦІЯ',
                'patterns': [
                    r'\b(СРОЧНО|УВАГА|ВНИМАНИЕ)\b.*?\b(катастрофа|кінець|загибель)\b',
                    r'\b(шок|невозможно)\b.*?\b(правда|факт|реальність)\b.*?\b(скрита|hidden)\b',
                ],
                'verdict': 'ЕМОЦІЙНА ДЕСТАБІЛІЗАЦІЯ',
                'explanation': 'Текст свідомо нагнітає страх і паніку',
                'score_boost': 0.42,
                'scientific_override': True
            },
        ]
        
        # ============================================================
        # АБСУРДНІ ПАРИ (РОЗШИРЕНО ДЛЯ КВАНТОВОГО БОРЩУ)
        # ============================================================
        self.absurd_pairs = [
            # КВАНТОВИЙ БОРЩ
            (['квантовий', 'квантова', 'квантове', 'квантові', 'квантову', 'квантової'], 
             ['борщ', 'сметана', 'картопля', 'морква', 'суп', 'буряк', 'каструля', 'бульйон', 'черпак']),
            
            (['ентропія', 'флуктуація', 'тунельний', 'сингулярність', 'суперпозиція'], 
             ['борщ', 'сметана', 'картопля', 'морква', 'буряк', 'петрушка', 'кроп']),
            
            (['хвильова функція', 'колапс хвильової', 'мультивсесвіт'], 
             ['суп', 'борщ', 'черпак', 'картопля']),
            
            (['термодинаміка', 'термодинаміці', 'термодинаміку'], 
             ['бульйон', 'суп', 'борщ', 'каструля']),
            
            # НАУКА + ТЕХНОЛОГІЧНИЙ АБСУРД
            (['пінеальний', 'шишкоподібний', 'імунний', 'імунної'], 
             ['5g', 'супутник', 'старлінк', 'блокчейн', 'гейтса', 'нанобот']),
            
            (['когнітивний', 'префронтальний', 'нейронний'], 
             ['5g', 'випромінювання', 'частота', 'ггц', 'дестабілізує']),
            
            (['резонанс', 'дискретний', 'нелокальний'], 
             ['сметана', 'морква', 'буряк', 'шлунок']),
            
            (['верифікований', 'підтверджує', 'дослідження'], 
             ['гейтса', 'старлінк', 'сни', 'записувати', 'блокчейн']),
        ]
        
        # ============================================================
        # КОНФЛІКТНІ ПАРИ (додано для 5G конспірології)
        # ============================================================
        self.conflict_pairs = [
            (['5g', '5G', 'супутник', 'старлінк'], 
             ['пінеальний', 'шишкоподібний', 'залоза', 'сни', 'нанобот', 'кристалічний', 'решітка'], 
             0.45),
            
            (['бднф', 'гіпокамп', 'нейропластичність'], ['5g', 'супутник', 'таргетування'], 0.35),
            (['нейтрино', 'квантовий', 'ентропія'], ['ринок', 'економіка', 'політика'], 0.3),
        ]
        
        # ============================================================
        # КЛЮЧОВІ СЛОВА ДЛЯ ШВИДКОЇ ПЕРЕВІРКИ
        # ============================================================
        self.quick_chaos_terms = {
            # Терміни, які одразу вказують на проблему
            'high_risk': ['5g', 'супутник', 'старлінк', 'тартарія', 'атлантида', 'антарктида',
                         'рептилоїд', 'хімітрейл', 'ілюмінати', 'більдерберг'],
            'absurd_mix': ['борщ', 'сметана', 'картопля', 'морква', 'буряк', 'каструля'],
            'pseudo_science': ['квантовий', 'ентропія', 'сингулярність', 'мультивсесвіт']
        }

    def quick_assessment(self, text):
        """Швидка оцінка тексту перед повним аналізом"""
        text_lower = text.lower()
        
        # 1. Швидка перевірка на явний абсурд
        for absurd in self.quick_chaos_terms['absurd_mix']:
            if absurd in text_lower:
                for science in self.quick_chaos_terms['pseudo_science']:
                    if science in text_lower:
                        return {'quick_result': 'HIGH_ABSURD', 'reason': f'{science}+{absurd}'}
        
        # 2. Швидка перевірка на високий ризик
        for risk in self.quick_chaos_terms['high_risk']:
            if risk in text_lower:
                return {'quick_result': 'HIGH_RISK', 'reason': risk}
        
        return {'quick_result': 'NEEDS_FULL_ANALYSIS'}

    def detect_absurdity_optimized(self, text):
        """Оптимізований пошук абсурдних пар"""
        text_lower = text.lower()
        found_pairs = []
        score = 0.0
        
        # Швидкий тест на наявність абсурдних слів
        has_absurd_food = any(food in text_lower for food in ['борщ', 'сметана', 'картопля', 'морква'])
        has_science = any(sci in text_lower for sci in ['квантовий', 'ентропія', 'сингулярність'])
        
        if not (has_absurd_food and has_science):
            return 0.0, []  # Якщо немає очевидного абсурду, повертаємо 0
        
        # Повний пошук
        for science_terms, absurd_terms in self.absurd_pairs:
            # Швидка перевірка наявності
            science_present = any(term.lower() in text_lower for term in science_terms)
            absurd_present = any(term.lower() in text_lower for term in absurd_terms)
            
            if science_present and absurd_present:
                # Перевірка в одному реченні для точності
                sentences = re.split(r'[.!?]+', text)
                for sentence in sentences:
                    sentence_lower = sentence.lower()
                    science_in_sentence = any(st.lower() in sentence_lower for st in science_terms)
                    absurd_in_sentence = any(at.lower() in sentence_lower for at in absurd_terms)
                    
                    if science_in_sentence and absurd_in_sentence:
                        score += 0.35
                        science_word = next((st for st in science_terms if st.lower() in sentence_lower), science_terms[0])
                        absurd_word = next((at for at in absurd_terms if at.lower() in sentence_lower), absurd_terms[0])
                        found_pairs.append((science_word, absurd_word))
                        break  # Одного знайденого в реченні достатньо
        
        return min(score, 0.8), found_pairs

    def detect_patterns_fast(self, text):
        """Швидке виявлення паттернів"""
        detected = []
        text_lower = text.lower()
        
        for pattern in self.critical_patterns:
            for regex in pattern['patterns']:
                try:
                    if re.search(regex, text_lower, re.IGNORECASE):
                        detected.append(pattern)
                        break
                except:
                    continue
        
        return detected

    def calculate_optimized_score(self, text, is_scientific, absurdity_score, absurd_pairs, 
                                  detected_patterns, term_counts, metrics):
        """Оптимізований розрахунок оцінки"""
        
        # БАЗОВА ФОРМУЛА (спрощена)
        if is_scientific:
            base_score = absurdity_score * 0.3  # Наука має захист
        else:
            base_score = (
                absurdity_score * 0.4 +           # 40% за абсурд
                (term_counts['chaos'] / max(1, metrics['word_count'])) * 0.3 +  # 30% за хаос-терміни
                (1 if detected_patterns else 0) * 0.3  # 30% за критичні паттерни
            )
        
        # ШТРАФ ЗА АБСУРД (особливо для "квантовий борщ")
        if absurdity_score > 0.3 and any('борщ' in pair[1] or 'сметана' in pair[1] for pair in absurd_pairs):
            base_score = min(0.99, base_score * 1.3)  # +30% штраф
        
        # ЗАХИСТ ДЛЯ КОРОТКИХ ТЕКСТІВ
        if metrics['word_count'] < 30 and base_score > 0.5:
            base_score *= 0.7
        
        return min(0.99, max(0.0, base_score))

    def analyze_optimized(self, text):
        """Оптимізований основний метод аналізу"""
        if not text or len(text.strip()) < 20:
            return {'error': 'Text too short'}
        
        # 1. ШВИДКА ОЦІНКА
        quick = self.quick_assessment(text)
        if quick['quick_result'] == 'HIGH_ABSURD':
            return {
                'entropy': 0.75,
                'status': 'CRITICAL',
                'verdict': 'АБСУРДНИЙ СЕМАНТИЧНИЙ РОЗРИВ',
                'explanation': f'Швидке виявлення: {quick["reason"]}',
                'language': 'UK',
                'diagnostics': {'quick_detected': True, 'reason': quick['reason']}
            }
        
        # 2. ОСНОВНИЙ АНАЛІЗ
        words = text.split()
        word_count = len(words)
        
        # АБСУРДНІ ПАРИ
        absurdity_score, absurd_pairs = self.detect_absurdity_optimized(text)
        
        # КРИТИЧНІ ПАТТЕРНИ
        detected_patterns = self.detect_patterns_fast(text)
        
        # ПРОСТА КАТЕГОРИЗАЦІЯ
        text_lower = text.lower()
        term_counts = {
            'chaos': sum(1 for term in self.quick_chaos_terms['high_risk'] + 
                        self.quick_chaos_terms['absurd_mix'] if term in text_lower),
            'science': sum(1 for term in self.quick_chaos_terms['pseudo_science'] if term in text_lower)
        }
        
        metrics = {'word_count': word_count}
        
        # 3. РОЗРАХУНОК ОЦІНКИ
        final_score = self.calculate_optimized_score(
            text, False, absurdity_score, absurd_pairs, 
            detected_patterns, term_counts, metrics
        )
        
        # 4. ВЕРДИКТ
        if absurdity_score > 0.3 and absurd_pairs:
            status = 'CRITICAL'
            verdict = 'АБСУРДНИЙ СЕМАНТИЧНИЙ РОЗРИВ'
            pairs_text = ", ".join([f"{a}+{b}" for a,b in absurd_pairs[:2]])
            explanation = f'Текст поєднує несумісні концепції: {pairs_text}'
        elif final_score > 0.65:
            status = 'CRITICAL'
            verdict = 'ВИСОКИЙ РІВЕНЬ СЕМАНТИЧНОГО ХАОСУ'
            explanation = 'Текст демонструє критичний рівень семантичної несумісності'
        elif final_score > 0.45:
            status = 'WARNING'
            verdict = 'ПІДОЗРІЛА СТРУКТУРА'
            explanation = 'Текст містить ознаки семантичних несумісностей'
        elif final_score > 0.25:
            status = 'ACCEPTABLE'
            verdict = 'ПРИЙНЯТНА СТРУКТУРА'
            explanation = 'Текст відповідає нормам логічної сумісності'
        else:
            status = 'TRUSTED'
            verdict = 'СТАБІЛЬНИЙ ЛОГІЧНИЙ СИГНАЛ'
            explanation = 'Текст демонструє логічну цілісність'
        
        # Додаткові деталі
        if absurdity_score > 0.1:
            explanation += f" | Абсурдність: {absurdity_score:.2f}"
        
        return {
            'entropy': round(final_score, 3),
            'status': status,
            'verdict': verdict,
            'language': 'UK',
            'explanation': explanation,
            'diagnostics': {
                'word_count': word_count,
                'absurdity_score': round(absurdity_score, 3),
                'absurd_pairs_found': len(absurd_pairs),
                'pattern_count': len(detected_patterns),
                'chaos_terms': term_counts['chaos'],
                'quick_assessment': quick['quick_result']
            }
        }

    # ============================================================
    # ЗАЛЕЖНІ МЕТОДИ (для сумісності)
    # ============================================================
    
    def analyze(self, text):
        """Основний метод (для сумісності) - використовує оптимізовану версію"""
        return self.analyze_optimized(text)
    
    def detect_absurdity(self, text):
        """Для сумісності з оригінальним інтерфейсом"""
        return self.detect_absurdity_optimized(text)
    
    def detect_patterns(self, text):
        """Для сумісності з оригінальним інтерфейсом"""
        return self.detect_patterns_fast(text)

# ============================================================
# КЛАС-НАСЛІДНИК ДЛЯ МАКСИМАЛЬНОЇ ПРОДУКТИВНОСТІ
# ============================================================

class VeritasUltimateCore(VeritasCalibratedCore):
    """Ультимативна версія з усіма оптимізаціями"""
    
    def __init__(self):
        super().__init__()
        # Додаємо ще більше абсурдних пар
        self.absurd_pairs.extend([
            (['матриця', 'симуляція', 'голограма'], 
             ['борщ', 'суп', 'їжа', 'каструля']),
            
            (['біополе', 'аура', 'чакра'], 
             ['вакцина', '5g', 'супутник', 'чип']),
            
            (['душа', 'свідомість', 'карма'], 
             ['блокчейн', 'NFT', 'криптовалюта', 'алгоритм']),
        ])
    
    def analyze(self, text):
        """Ультимативний аналіз з підвищеною точністю"""
        result = super().analyze_optimized(text)
        
        # ДОДАТКОВИЙ ШТРАФ ДЛЯ НАЙГІРШИХ ВИПАДКІВ
        if result['entropy'] > 0.6 and 'борщ' in text.lower():
            result['entropy'] = min(0.95, result['entropy'] * 1.2)
            result['explanation'] += " | ПІДВИЩЕНИЙ ШТРАФ: квантовий борщ"
            if result['status'] != 'CRITICAL':
                result['status'] = 'CRITICAL'
                result['verdict'] = 'КВАНТОВО-КУЛІНАРНИЙ АБСУРД'
        
        return result
