"""
Veritas Protocol - Calibrated Core v12.0 STABLE
Balanced detection: protects science, catches real absurdity
"""

import re
import math


class VeritasCalibratedCore:
    """STABLE VERSION — правильний баланс між чутливістю і точністю"""
    
    def __init__(self):
        # ============================================================
        # АБСУРД-ПАТТЕРНИ (тільки явний абсурд!)
        # ============================================================
        self.absurd_patterns = [
            # Наука + Їжа
            (r'квантов(ий|а|е).*?(борщ|суп|їжа)', 0.9),
            (r'(ентропія|термодинаміка).*?(борщ|суп|рецепт)', 0.85),
            
            # Біологія + Техно-параноя
            (r'(днк|вакцина|імунітет).*?(5g|чип|контроль)', 0.85),
            (r'(мозок|нейрон).*?(програмування|зомбування)', 0.8),
            
            # Бізнес + Езотерика
            (r'(бізнес|маркетинг).*?(чакра|аура|карма)', 0.9),
            (r'квантов(ий|а).*?(бізнес|продажі)', 0.85),
            
            # Цифровий містицизм
            (r'(блокчейн|AI|алгоритм).*?(душа|карма|просвітлення)', 0.85),
            
            # Істерія
            (r'НЕГАЙНО.*?(ЗРАДА|КАТАСТРОФА)', 0.8),
            (r'СРОЧНО.*?(правда|загибель)', 0.75),
        ]
        
        # ============================================================
        # ЗАХИСТ НАУКИ
        # ============================================================
        self.science_keyphrases = [
            'другий закон термодинаміки',
            'ентропія не може зменшуватися',
            'ізольована система',
            'теплова смерть всесвіту',
            'статистична фізика',
            'second law of thermodynamics',
            'entropy increases',
            'isolated system',
            'heat death',
        ]
        
        self.science_terms = [
            'термодинаміка', 'ентропія', 'фізика', 'математика',
            'статистичний', 'дослідження', 'експеримент',
            'thermodynamics', 'entropy', 'physics', 'mathematics',
            'statistical', 'research', 'experiment', 'study'
        ]
        
        # ============================================================
        # СЛОВА-ВИНІВКИ (явні ознаки абсурду)
        # ============================================================
        self.absurd_keywords = [
            'чакра', 'аура', 'карма', 'рептилоїд', 'ілюмінат',
            'змова', 'езотеричний', 'містичний'
        ]

    def analyze(self, text: str) -> dict:
        """Головна функція аналізу"""
        
        if not text or len(text.strip()) < 20:
            return {'error': 'Text too short'}
        
        text_lower = text.lower()
        words = text.split()
        word_count = len(words)
        
        # ============================================================
        # КРОК 1: ЧИ ЦЕ НАУКА? (fast-path)
        # ============================================================
        for phrase in self.science_keyphrases:
            if phrase.lower() in text_lower:
                return self._create_science_result(word_count, len(text))
        
        # Додаткова перевірка: багато наукових термінів
        sci_count = sum(1 for term in self.science_terms if term in text_lower)
        has_absurd_kw = any(kw in text_lower for kw in self.absurd_keywords)
        
        if sci_count >= 3 and not has_absurd_kw:
            return self._create_science_result(word_count, len(text))
        
        # ============================================================
        # КРОК 2: ДЕТЕКЦІЯ АБСУРДУ
        # ============================================================
        absurd_score = 0.0
        found_patterns = []
        
        # Regex паттерни
        for pattern, weight in self.absurd_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                absurd_score = max(absurd_score, weight)
                found_patterns.append(pattern[:25])
        
        # Ключові слова абсурду
        found_kw = [kw for kw in self.absurd_keywords if kw in text_lower]
        if found_kw:
            absurd_score = max(absurd_score, 0.65)
            found_patterns.append(f"keywords: {','.join(found_kw[:2])}")
        
        # Істерія (КАПС + оклички)
        hysteria = self._calculate_hysteria(text)
        if hysteria > 0.5:
            absurd_score = max(absurd_score, 0.6 + hysteria * 0.3)
            found_patterns.append('Hysteria')
        
        # ============================================================
        # КРОК 3: ФІНАЛЬНА ОЦІНКА
        # ============================================================
        # Якщо нічого не знайдено — низький бал
        if absurd_score == 0.0 and hysteria < 0.3:
            final_score = 0.05 if word_count > 50 else 0.08
        else:
            # Є ознаки абсурду — підвищуємо
            final_score = min(0.99, absurd_score * 1.05)
        
        # ============================================================
        # КРОК 4: ВЕРДИКТ
        # ============================================================
        if final_score > 0.75:
            status = 'CRITICAL'
            verdict = 'АБСОЛЮТНИЙ АБСУРД'
            explanation = 'Текст містить критичні логічні порушення'
        elif final_score > 0.55:
            status = 'WARNING'
            verdict = 'ВИСОКИЙ РІВЕНЬ АБСУРДУ'
            explanation = 'Текст демонструє значні семантичні несумісності'
        elif final_score > 0.35:
            status = 'WARNING'
            verdict = 'ПІДОЗРІЛИЙ ДИСКУРС'
            explanation = 'Текст містить ознаки логічних несумісностей'
        elif final_score > 0.15:
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
        
        if found_patterns:
            explanation += f" | Знайдено: {', '.join(found_patterns[:2])}"
        
        # ============================================================
        # РЕЗУЛЬТАТ
        # ============================================================
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
                'chaos_index': round(final_score * 100, 2),
                'influence_index': round(final_score * 100 * (1 + hysteria * 0.5), 2),
                'sanity_penalty': round(absurd_score + hysteria * 0.3, 3),
                'is_science': False,
                'patterns_found': len(found_patterns)
            }
        }
    
    def _create_science_result(self, word_count, char_count):
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
                'char_count': char_count,
                'chaos_index': 0.0,
                'influence_index': 5.25,
                'sanity_penalty': 0.0,
                'is_science': True,
                'patterns_found': 0
            }
        }
    
    def _calculate_hysteria(self, text):
        """Детекція істерії"""
        score = 0.0
        
        # КАПС слова
        caps_words = [w for w in text.split() if w.isupper() and len(w) > 2]
        score += min(0.5, len(caps_words) / 4)
        
        # Оклички
        score += min(0.3, text.count('!') / 5)
        
        # Паникерські слова
        panic = ['зрада', 'ганьба', 'скандал', 'негайно', 'катастрофа', 
                'срочно', 'увага', 'шок', 'ужас']
        panic_count = sum(1 for w in panic if w in text.lower())
        score += min(0.4, panic_count / 3)
        
        return min(1.0, score)
