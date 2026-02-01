"""
Veritas Protocol - FINAL FIXED VERSION v11.4
Проста логіка: наука = VERIFIED, абсурд = CRITICAL
"""

import re
import math

class VeritasCalibratedCore:
    """FINAL VERSION - SIMPLE & EFFECTIVE"""
    
    def __init__(self):
        # КЛЮЧОВІ ФРАЗИ ДЛЯ НАУКИ (якщо є хоча б одна - це наука)
        self.SCIENCE_PHRASES = [
            'другий закон термодинаміки',
            'ентропія не може зменшуватися',
            'ізольована система',
            'теплова смерть Всесвіту',
            'статистична фізика',
            'розподіл мікростанів',
            'спонтанні процеси',
            'зростання ентропії',
        ]
        
        # АБСУРД (якщо є хоча б один - це абсурд)
        self.ABSURD_PATTERNS = [
            # Наука + Їжа
            (r'квантовий.*?(борщ|суп|їжа|сметана|картопля)', 0.95),
            (r'(ентропія|термодинаміка).*?(борщ|суп|їжа)', 0.9),
            
            # Бізнес-езотерика
            (r'(бізнес|ринок|менеджмент).*?(чакра|аура|енергія)', 0.9),
            (r'(маркетинг|стратегія).*?(вібрація|карма)', 0.85),
            
            # Цифровий містицизм
            (r'(AI|алгоритм|блокчейн).*?(душа|карма|просвітлення)', 0.9),
            
            # Псевдонаука
            (r'нанодискретизація', 0.8),
            (r'квантова суперпозиція нейронів', 0.85),
            (r'супутникові масиви.*?несвідоме', 0.8),
            
            # Істерія (точні фрази)
            (r'НЕГАЙНО ПОШИРЮЙТЕ', 0.9),
            (r'ЗРАДА.*?НАЦІОНАЛЬНИХ', 0.85),
            (r'ВИЙДІТЬ НА ВУЛИЦІ', 0.9),
            (r'ПРИХОВУЮТЬ ПРАВДУ', 0.8),
        ]
        
        # СЛОВА-ІНДИКАТОРИ АБСУРДУ
        self.ABSURD_WORDS = [
            'чакра', 'аура', 'карма', 'енергетичний', 'вібраційний',
            'рептилоїд', 'ілюмінат', 'масон', 'змова',
            'нанодискретизація', 'пост-біологічний', 'мета-фізичний',
        ]

    def analyze(self, text):
        """НАЙПРОСТІША ЛОГІКА ЗА 4 КРОКИ"""
        if not text or len(text.strip()) < 20:
            return {'error': 'Text too short'}
        
        text_lower = text.lower()
        words = text.split()
        word_count = len(words)
        
        # КРОК 1: ЧИ ЦЕ НАУКА? (ПЕРШОЧЕРГОВО!)
        is_science = False
        for phrase in self.SCIENCE_PHRASES:
            if phrase in text_lower:
                is_science = True
                break
        
        # Додаткова перевірка для науки
        if not is_science:
            science_words = ['термодинаміка', 'ентропія', 'фізика', 'статистичний', 'енергія']
            science_count = sum(1 for word in science_words if word in text_lower)
            absurd_count = sum(1 for word in self.ABSURD_WORDS if word in text_lower)
            
            if science_count >= 2 and absurd_count == 0:
                is_science = True
        
        if is_science:
            return self._science_result(text, word_count)
        
        # КРОК 2: ЧИ ЦЕ АБСУРД?
        absurd_score = 0.0
        found_patterns = []
        
        # 1. Пошук паттернів абсурду
        for pattern, weight in self.ABSURD_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                absurd_score = max(absurd_score, weight)
                found_patterns.append(pattern[:30])
        
        # 2. Пошук слів абсурду
        for word in self.ABSURD_WORDS:
            if word in text_lower:
                absurd_score = max(absurd_score, 0.7)
                found_patterns.append(word)
                break
        
        # 3. Істерія
        hysteria = self._check_hysteria(text)
        if hysteria > 0:
            absurd_score = max(absurd_score, hysteria)
            found_patterns.append("Істерія")
        
        # КРОК 3: ФІНАЛЬНА ОЦІНКА
        if absurd_score > 0:
            final_score = absurd_score
        else:
            # Якщо немає абсурду - низький бал
            final_score = 0.1
        
        # КРОК 4: РОЗРАХУНОК ІНДЕКСІВ
        chaos_index = final_score * 100
        influence_index = final_score * 100 * (1 + hysteria * 0.3)
        
        # КРОК 5: ВЕРДИКТ
        if final_score > 0.7:
            status = 'CRITICAL'
            verdict = 'АБСУРД'
            explanation = 'Текст містить логічні порушення'
        elif final_score > 0.4:
            status = 'WARNING'
            verdict = 'ПІДОЗРІЛИЙ ТЕКСТ'
            explanation = 'Текст має ознаки нелогічності'
        elif final_score > 0.1:
            status = 'ACCEPTABLE'
            verdict = 'НОРМАЛЬНИЙ ТЕКСТ'
            explanation = 'Текст відповідає нормам'
        else:
            status = 'VERIFIED'
            verdict = 'ВЕРИФІКОВАНИЙ'
            explanation = 'Текст логічно цілісний'
        
        # Деталі
        if found_patterns:
            explanation += f" | Знайдено: {', '.join(set(found_patterns[:3]))}"
        
        return {
            'entropy': round(final_score, 3),
            'status': status,
            'verdict': verdict,
            'language': 'UK',
            'explanation': explanation,
            'diagnostics': {
                'absurd_score': round(absurd_score, 3),
                'hysteria_score': round(hysteria, 3),
                'word_count': word_count,
                'char_count': len(text),
                'chaos_index': round(chaos_index, 2),
                'influence_index': round(influence_index, 2),
                'is_science': False,
            }
        }
    
    def _science_result(self, text, word_count):
        """Результат для наукового тексту"""
        return {
            'entropy': 0.05,
            'status': 'VERIFIED',
            'verdict': 'НАУКОВИЙ СТАНДАРТ',
            'language': 'UK',
            'explanation': 'Текст демонструє наукову цілісність',
            'diagnostics': {
                'absurd_score': 0.0,
                'hysteria_score': 0.0,
                'word_count': word_count,
                'char_count': len(text),
                'chaos_index': 0.0,
                'influence_index': 5.25,
                'is_science': True,
            }
        }
    
    def _check_hysteria(self, text):
        """Перевірка на істерію"""
        score = 0.0
        
        # КАПС-слова
        caps = [w for w in text.split() if w.isupper() and len(w) > 2]
        if len(caps) >= 2:
            score += 0.6
        
        # Оклички
        if text.count('!') >= 3:
            score += 0.4
        
        # Паникерські слова
        panic_words = ['зрада', 'ганьба', 'скандал', 'негайно', 'пізно']
        for word in panic_words:
            if word in text.lower():
                score += 0.3
                break
        
        return min(1.0, score)
