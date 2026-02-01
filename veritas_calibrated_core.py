"""
Veritas Protocol - Semantic Void Detector v11.3 (ULTRA SIMPLE & STRICT)
Найпростіша версія з максимальними штрафами за абсурд
"""

import re
import math

class VeritasCalibratedCore:
    """ULTRA SIMPLE VERSION - PROTECTS SCIENCE, DESTROYS ABSURDITY"""
    
    def __init__(self):
        # ============================================================
        # КРИТИЧНІ АБСУРД-ПАТТЕРНИ (МАКСИМАЛЬНІ ШТРАФИ!)
        # ============================================================
        self.critical_absurdity = [
            # Наука + Їжа = АБСОЛЮТНИЙ АБСУРД (1.0!)
            (r'квантов(ий|а|е|і|ого|ої|ому|ій).*?(борщ|суп|їжа|сметана|картопля|буряк|каструля)', 1.0),
            (r'(ентропія|термодинаміка|фізика).*?(борщ|суп|їжа|рецепт|кухня)', 0.9),
            
            # Біологія + Техно-параноя
            (r'(днк|генетичний|імунітет|вакцина).*?(5g|чип|супутник|частота|гц|радіо)', 0.9),
            (r'(нейрон|мозок|синапс).*?(програмування|контроль|зомбування)', 0.85),
            
            # Бізнес + Езотерика (КОРПОРАТИВНИЙ БРЕД!)
            (r'(бізнес|ринок|менеджмент|стратегія).*?(чакра|аура|енергія|вібрація|карма)', 1.0),
            (r'(квантовий|квантова).*?(маркетинг|бізнес|продажі|лідерство)', 0.95),
            (r'(холістичний|синергетичний).*?(маркетинг|менеджмент|розвиток)', 0.8),
            
            # Цифровий містицизм
            (r'(блокчейн|AI|штучний інтелект|алгоритм).*?(душа|свідомість|карма|просвітлення)', 0.9),
            (r'(NFT|метаверс|Web3).*?(енергія|чакра|астрал)', 0.95),
            
            # Істерія (ЕМОЦІЙНИЙ ТЕРОР!)
            (r'(НЕГАЙНО|ЗРАДА|ГАНЬБА|СКАНДАЛ|КАТАСТРОФА).*?(правда|істина|факт)', 0.95),
            (r'ви не готові|ви не знаєте|ви не розумієте.*?(правда|реальність)', 0.85),
            (r'(СРОЧНО|УВАГА|ВНИМАНИЕ).*?(катастрофа|кінець|загибель)', 0.9),
            
            # Псевдонауковий бред
            (r'(нанодискретизація|супутникові масиви низької орбіти)', 0.8),
            (r'(квантова суперпозиція нейронів|пост-біологічне суспільство)', 0.9),
            (r'(чакри|вібраційний фон|ефірний кокон|провідники прани)', 0.85),
            (r'(мета-фізичні протоколи|квантове вирівнювання аури)', 1.0),
            (r'(світловий вузол у глобальній матриці|езотеричні цикли)', 0.95),
        ]
        
        # ============================================================
        # ЗАХИСТ НАУКИ (автоматичний VERIFIED)
        # ============================================================
        self.science_protection = [
            r'другий закон термодинаміки',
            r'ентропія.*?(зростання|зменшуватися|не може)',
            r'ізольована система',
            r'теплова смерть.*?всесвіту',
            r'статистична фізика',
            r'згідно з.*?дослідженням',
            r'результати.*?показують',
            r'статистично значущий',
            r'p.*?value.*?<.*?\d',
            r'коефіцієнт кореляції',
        ]
        
        # ============================================================
        # НАУКОВІ ФОРМУЛИ (захист)
        # ============================================================
        self.science_formulas = [
            '=', '≠', '≈', '~', '→', '⇒', '∈', '∑', '∫', '∂',
            '∆', 'π', '∞', '√', '≈', '≡', 'α', 'β', 'γ', 'δ'
        ]
        
        # ============================================================
        # НАУКОВІ ТЕРМІНИ
        # ============================================================
        self.science_terms = [
            'термодинаміка', 'ентропія', 'енергія', 'фізика', 'математика',
            'статистичний', 'кореляція', 'регресія', 'вибірка', 'гіпотеза',
            'теорія', 'експеримент', 'дослідження', 'аналіз', 'методологія',
            'верифікація', 'валідація', 'реплікація', 'контрольна група'
        ]

    def analyze(self, text):
        """УЛЬТРА-ПРОСТА ЛОГІКА"""
        if not text or len(text.strip()) < 20:
            return {'error': 'Text too short'}
        
        text_lower = text.lower()
        words = text.split()
        word_count = len(words)
        
        # ============================================================
        # КРОК 1: ПЕРЕВІРКА НА НАУКУ (ПЕРШОЧЕРГОВО!)
        # ============================================================
        is_science = self._is_pure_science(text)
        if is_science:
            return self._create_science_result(text, word_count)
        
        # ============================================================
        # КРОК 2: ДЕТЕКЦІЯ АБСУРДУ (МАКСИМАЛЬНІ ШТРАФИ!)
        # ============================================================
        absurd_score = 0.0
        absurd_details = []
        
        # 1. Регулярні вирази для абсурду
        for pattern, weight in self.critical_absurdity:
            if re.search(pattern, text_lower, re.IGNORECASE):
                absurd_score = max(absurd_score, weight)
                # Беремо перші 20 символів знайденого патерну
                match = re.search(pattern, text_lower[:100], re.IGNORECASE)
                if match:
                    absurd_details.append(f"{pattern[:30]}...")
        
        # 2. Істерія (капс + оклички)
        hysteria_score = self._calculate_hysteria(text)
        if hysteria_score > 0.5:
            absurd_score = max(absurd_score, 0.7 + hysteria_score * 0.3)
            absurd_details.append("Істерія")
        
        # 3. Псевдоінтелектуальний бред (довгі "розумні" слова без змісту)
        pseudo_score = self._calculate_pseudo_intellectual(text)
        if pseudo_score > 0.6:
            absurd_score = max(absurd_score, pseudo_score)
            absurd_details.append("Псевдоінтелектуальний стиль")
        
        # ============================================================
        # КРОК 3: ФІНАЛЬНА ОЦІНКА
        # ============================================================
        final_score = absurd_score
        
        # Автоматичне підвищення для очевидного абсурду
        if absurd_score > 0.7:
            final_score = min(0.99, absurd_score * 1.1)
        
        # ============================================================
        # КРОК 4: РОЗРАХУНОК ІНДЕКСІВ (ОБОВ'ЯЗКОВО!)
        # ============================================================
        chaos_index = final_score * 100 * (1 + len(absurd_details) * 0.5)
        influence_index = final_score * 100 * (1 + hysteria_score * 0.8)
        sanity_penalty = round(absurd_score + hysteria_score * 0.5, 3)
        
        # ============================================================
        # КРОК 5: ВЕРДИКТ (ДУЖЕ ЖОРСТКО!)
        # ============================================================
        if final_score > 0.8:
            status = 'CRITICAL'
            verdict = 'АБСОЛЮТНИЙ АБСУРД'
            explanation = 'Текст містить критичні логічні порушення'
        elif final_score > 0.6:
            status = 'CRITICAL'
            verdict = 'ВИСОКИЙ РІВЕНЬ АБСУРДУ'
            explanation = 'Текст демонструє значні семантичні несумісності'
        elif final_score > 0.4:
            status = 'WARNING'
            verdict = 'ПІДОЗРІЛИЙ ДИСКУРС'
            explanation = 'Текст містить ознаки логічних несумісностей'
        elif final_score > 0.2:
            status = 'ACCEPTABLE'
            verdict = 'ПРИЙНЯТНА ІНФОРМАЦІЯ'
            explanation = 'Текст відповідає нормам логічної сумісності'
        elif final_score > 0.05:
            status = 'TRUSTED'
            verdict = 'СТАБІЛЬНИЙ СИГНАЛ'
            explanation = 'Текст демонструє логічну цілісність'
        else:
            status = 'VERIFIED'
            verdict = 'ВЕРИФІКОВАНИЙ КОНТЕНТ'
            explanation = 'Текст демонструє ідеальну логічну цілісність'
        
        # Деталізація
        if absurd_details:
            details = ", ".join(absurd_details[:3])
            explanation += f" | Абсурд: {details}"
        
        if hysteria_score > 0.3:
            explanation += f" | Істерія: {hysteria_score:.1f}"
        
        # ============================================================
        # КРОК 6: ПОВЕРТАЄМО РЕЗУЛЬТАТ З УСІМА ІНДЕКСАМИ!
        # ============================================================
        return {
            'entropy': round(final_score, 3),
            'status': status,
            'verdict': verdict,
            'language': 'UK',
            'explanation': explanation,
            'diagnostics': {
                'absurd_score': round(absurd_score, 3),
                'hysteria_score': round(hysteria_score, 3),
                'pseudo_score': round(pseudo_score, 3),
                'word_count': word_count,
                'char_count': len(text),
                'chaos_index': round(chaos_index, 2),
                'influence_index': round(influence_index, 2),
                'sanity_penalty': sanity_penalty,
                'is_science': False,
                'absurd_patterns': len(absurd_details)
            }
        }
    
    def _is_pure_science(self, text):
        """Перевіряє, чи текст є чистою наукою"""
        text_lower = text.lower()
        
        # 1. Має бути хоча б одна наукова формула або 3 наукових терміни
        has_formula = any(formula in text for formula in self.science_formulas)
        science_terms_count = sum(1 for term in self.science_terms if term in text_lower)
        
        if not has_formula and science_terms_count < 3:
            return False
        
        # 2. Має бути хоча б один захисний патерн
        has_protection = any(re.search(pattern, text_lower, re.IGNORECASE) 
                           for pattern in self.science_protection)
        
        # 3. Не повинно бути абсурду
        has_absurd = any(re.search(pattern, text_lower, re.IGNORECASE) 
                        for pattern, _ in self.critical_absurdity)
        
        # 4. Не повинно бути істерії
        hysteria = self._calculate_hysteria(text)
        
        return (has_protection or (has_formula and science_terms_count >= 3)) and not has_absurd and hysteria < 0.3
    
    def _create_science_result(self, text, word_count):
        """Створює результат для наукового тексту"""
        return {
            'entropy': 0.05,
            'status': 'VERIFIED',
            'verdict': 'НАУКОВИЙ СТАНДАРТ',
            'language': 'UK',
            'explanation': 'Текст демонструє наукову цілісність без ознак абсурду',
            'diagnostics': {
                'absurd_score': 0.0,
                'hysteria_score': 0.0,
                'pseudo_score': 0.0,
                'word_count': word_count,
                'char_count': len(text),
                'chaos_index': 0.0,
                'influence_index': round(0.05 * 100 * (1 + 0.05), 2),
                'sanity_penalty': 0.0,
                'is_science': True,
                'absurd_patterns': 0
            }
        }
    
    def _calculate_hysteria(self, text):
        """Розраховує рівень істерії"""
        score = 0.0
        
        # 1. КАПС-ЛОКАУТ
        caps_words = [w for w in text.split() if w.isupper() and len(w) > 2]
        score += min(0.5, len(caps_words) / 3)
        
        # 2. Окличні речення
        excl_count = text.count('!')
        score += min(0.3, excl_count / 4)
        
        # 3. Ключові слова істерії
        hysteria_words = ['зрада', 'ганьба', 'скандал', 'негайно', 'пізно', 
                         'катастрофа', 'шок', 'ужас', 'паника', 'знищення']
        hysteria_count = sum(1 for word in hysteria_words if word in text.lower())
        score += min(0.4, hysteria_count / 2)
        
        # 4. Довжина речень (короткі = істерія)
        sentences = re.split(r'[.!?]+', text)
        if sentences:
            avg_len = sum(len(s.split()) for s in sentences if s.strip()) / len(sentences)
            if avg_len < 8:  # Дуже короткі речення
                score += 0.2
        
        return min(1.0, score)
    
    def _calculate_pseudo_intellectual(self, text):
        """Розраховує рівень псевдоінтелектуального бреду"""
        text_lower = text.lower()
        score = 0.0
        
        # "Розумні" слова без змісту
        pseudo_words = [
            'парадигма', 'дискурс', 'наратив', 'конструкт', 'семіозис',
            'трансгресивний', 'деконструкція', 'постмодерн', 'метанаратив',
            'симулякр', 'гіперреальність', 'детеріторіалізація',
            'синергетичний', 'холістичний', 'мета-фізичний'
        ]
        
        found_words = sum(1 for word in pseudo_words if word in text_lower)
        
        # Якщо багато "розумних" слів, але мало реального змісту
        if found_words >= 3:
            score = 0.4 + (found_words - 3) * 0.15
        
        # Дуже довгі речення з багатьма абстракціями
        sentences = re.split(r'[.!?]+', text)
        long_complex = 0
        for sentence in sentences:
            words_in_sentence = sentence.split()
            if len(words_in_sentence) > 25:  # Дуже довге речення
                # Рахуємо абстрактні слова
                abstract = sum(1 for word in pseudo_words if word in sentence.lower())
                if abstract >= 2:
                    long_complex += 1
        
        if long_complex >= 2:
            score = max(score, 0.7)
        
        return min(1.0, score)
