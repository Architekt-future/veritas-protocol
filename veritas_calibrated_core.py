"""
Veritas Protocol - FINAL WORKING VERSION v11.6
З усіма маркерами категорій для правильної класифікації
"""

import re
import math

class VeritasCalibratedCore:
    def __init__(self):
        # ============================================================
        # МАРКЕРИ КАТЕГОРІЙ (НАЙВАЖЛИВІШЕ!)
        # ============================================================
        
        # НАУКОВІ МАРКЕРИ (захищаємо!)
        self.SCIENCE_MARKERS = [
            'термодинаміка', 'ентропія', 'енергія', 'фізика', 'математика',
            'статистичний', 'кореляція', 'регресія', 'вибірка', 'гіпотеза',
            'теорія', 'експеримент', 'дослідження', 'аналіз', 'методологія',
            'верифікація', 'валідація', 'реплікація', 'контрольна група',
            'ізольована система', 'теплова смерть', 'статистична фізика'
        ]
        
        # ЕЗОТЕРИЧНІ МАРКЕРИ (абсурд!)
        self.ESOTERIC_MARKERS = [
            'чакра', 'аура', 'карма', 'енергетичний', 'вібраційний',
            'рептилоїд', 'ілюмінат', 'масон', 'оккультний', 'містичний',
            'потойбічний', 'астральний', 'третій око', 'кундаліні'
        ]
        
        # ПСЕВДОНАУКОВІ МАРКЕРИ (абсурд!)
        self.PSEUDO_SCIENCE_MARKERS = [
            'квантовий', 'нейтрино', 'іоносфера', 'торсійний', 'ефір',
            'антигравітація', 'скалярне поле', 'тесла', 'безкоштовна енергія',
            'нанодискретизація', 'пост-біологічний', 'мета-фізичний'
        ]
        
        # БІЗНЕС-ЕЗОТЕРИКА (абсурд!)
        self.BUSINESS_ESOTERIC = [
            'холістичний', 'синергетичний', 'стратегія', 'ринок', 'менеджмент',
            'маркетинг', 'бізнес', 'корпоративний', 'оптимізація', 'ресурси'
        ]
        
        # ІСТЕРІЯ МАРКЕРИ
        self.HYSTERIA_MARKERS = [
            'зрада', 'ганьба', 'скандал', 'негайно', 'пізно', 'катастрофа',
            'шок', 'ужас', 'паніка', 'знищення', 'крах', 'кримінальний'
        ]

        # ============================================================
        # КРИТИЧНІ ПАТТЕРНИ АБСУРДУ (ВИСОКІ ШТРАФИ!)
        # ============================================================
        self.CRITICAL_ABSURD_PATTERNS = [
            # Наука + Їжа = АБСУРД
            (r'квантовий.*?(борщ|суп|їжа|сметана|картопля)', 1.0),
            (r'ентропія.*?(борщ|суп|їжа)', 0.95),
            (r'термодинаміка.*?(їжа|кухня|рецепт)', 0.9),
            
            # Бізнес + Езотерика = АБСУРД
            (r'(бізнес|ринок|менеджмент).*?(чакра|аура|енергія)', 0.95),
            (r'(маркетинг|стратегія).*?(вібрація|карма)', 0.9),
            
            # Цифровий містицизм = АБСУРД
            (r'(AI|алгоритм|блокчейн).*?(душа|карма|просвітлення)', 0.9),
            
            # Псевдонаука = АБСУРД
            (r'нанодискретизація.*?синаптичний', 0.85),
            (r'квантова суперпозиція.*?нейрон', 0.9),
        ]
        
        # ============================================================
        # НАУКОВІ ФРАЗИ (автоматичний VERIFIED)
        # ============================================================
        self.SCIENCE_PHRASES = [
            'другий закон термодинаміки',
            'ентропія не може зменшуватися',
            'ізольована система',
            'теплова смерть Всесвіту',
            'статистична фізика',
            'розподіл мікростанів системи',
            'спонтанні процеси',
            'зростання ентропії',
        ]

    def analyze(self, text):
        """ОСТАТОЧНА ЛОГІКА З УРАХУВАННЯМ МАРКЕРІВ"""
        if len(text.strip()) < 20:
            return {'error': 'Text too short'}
        
        text_lower = text.lower()
        words = text.split()
        word_count = len(words)
        
        # ============================================================
        # КРОК 1: ПОРАХУВАТИ МАРКЕРИ КАТЕГОРІЙ
        # ============================================================
        
        # Наукові маркери
        science_count = sum(1 for marker in self.SCIENCE_MARKERS if marker in text_lower)
        
        # Езотеричні маркери (АБСУРД!)
        esoteric_count = sum(1 for marker in self.ESOTERIC_MARKERS if marker in text_lower)
        
        # Псевдонаукові маркери (АБСУРД!)
        pseudo_count = sum(1 for marker in self.PSEUDO_SCIENCE_MARKERS if marker in text_lower)
        
        # Бізнес-езотерика (АБСУРД!)
        business_eso_count = 0
        business_words = [w for w in self.BUSINESS_ESOTERIC if w in text_lower]
        esoteric_words = [w for w in self.ESOTERIC_MARKERS if w in text_lower]
        if business_words and esoteric_words:
            business_eso_count = len(business_words) + len(esoteric_words)
        
        # Істерія маркери
        hysteria_count = sum(1 for marker in self.HYSTERIA_MARKERS if marker in text_lower)
        
        # ============================================================
        # КРОК 2: ПЕРЕВІРКА НА НАУКУ (ЗА МАРКЕРАМИ!)
        # ============================================================
        
        # УМОВА 1: Є наукові маркери
        # УМОВА 2: Немає езотеричних маркерів
        # УМОВА 3: Немає псевдонаукових маркерів в комбінації з езотеричними
        if (science_count >= 2 and 
            esoteric_count == 0 and 
            not (pseudo_count >= 2 and esoteric_count > 0)):
            
            # Додаткова перевірка: є наукові фрази
            has_science_phrase = any(phrase in text_lower for phrase in self.SCIENCE_PHRASES)
            
            if has_science_phrase or science_count >= 3:
                return self._create_result(
                    score=0.05,
                    status='VERIFIED',
                    verdict='НАУКОВИЙ СТАНДАРТ',
                    explanation='Текст демонструє наукову цілісність',
                    is_science=True,
                    text=text,
                    word_count=word_count,
                    science_count=science_count,
                    esoteric_count=esoteric_count,
                    pseudo_count=pseudo_count,
                    hysteria_count=hysteria_count
                )
        
        # ============================================================
        # КРОК 3: ДЕТЕКЦІЯ АБСУРДУ
        # ============================================================
        
        absurd_score = 0.0
        absurd_reasons = []
        
        # 1. КРИТИЧНІ ПАТТЕРНИ АБСУРДУ
        for pattern, weight in self.CRITICAL_ABSURD_PATTERNS:
            if re.search(pattern, text_lower):
                absurd_score = max(absurd_score, weight)
                absurd_reasons.append(f"Паттерн: {pattern[:20]}...")
        
        # 2. ЕЗОТЕРИКА = АБСУРД
        if esoteric_count > 0:
            absurd_score = max(absurd_score, 0.7 + esoteric_count * 0.1)
            absurd_reasons.append(f"Езотерика: {esoteric_count} маркерів")
        
        # 3. ПСЕВДОНАУКА + ЕЗОТЕРИКА = МЕГА-АБСУРД
        if pseudo_count > 0 and esoteric_count > 0:
            absurd_score = max(absurd_score, 0.9)
            absurd_reasons.append(f"Псевдонаука+Езотерика")
        
        # 4. БІЗНЕС-ЕЗОТЕРИКА = АБСУРД
        if business_eso_count > 0:
            absurd_score = max(absurd_score, 0.8 + business_eso_count * 0.05)
            absurd_reasons.append(f"Бізнес-езотерика")
        
        # 5. ІСТЕРІЯ
        if hysteria_count > 0:
            absurd_score = max(absurd_score, 0.6 + hysteria_count * 0.15)
            absurd_reasons.append(f"Істерія: {hysteria_count} маркерів")
        
        # 6. КАПС-ІСТЕРІЯ
        caps_score = self._check_caps_hysteria(text)
        if caps_score > 0:
            absurd_score = max(absurd_score, caps_score)
            absurd_reasons.append("КАПС-істерія")
        
        # ============================================================
        # КРОК 4: ФІНАЛЬНА ОЦІНКА
        # ============================================================
        
        if absurd_score > 0.7:
            final_score = min(0.99, absurd_score)
            status = 'CRITICAL'
            verdict = 'АБСУРД'
            explanation = 'Текст містить критичні логічні порушення'
        elif absurd_score > 0.4:
            final_score = absurd_score
            status = 'WARNING'
            verdict = 'ПІДОЗРІЛИЙ'
            explanation = 'Текст має ознаки нелогічності'
        else:
            # Нормальний текст
            final_score = 0.1 if len(text) < 100 else 0.05
            status = 'VERIFIED'
            verdict = 'НОРМАЛЬНИЙ ТЕКСТ'
            explanation = 'Текст відповідає нормам'
        
        # Додаємо причини
        if absurd_reasons:
            explanation += f" | Причини: {', '.join(absurd_reasons[:3])}"
        
        # ============================================================
        # КРОК 5: РОЗРАХУНОК ІНДЕКСІВ
        # ============================================================
        
        # Індекс хаосу
        chaos_index = final_score * 100 * (1 + (esoteric_count + pseudo_count) * 0.2)
        
        # Індекс впливу
        influence_index = final_score * 100 * (1 + hysteria_count * 0.3)
        
        # Штраф логіки
        sanity_penalty = round(absurd_score + (esoteric_count + pseudo_count) * 0.1, 3)
        
        return self._create_result(
            score=final_score,
            status=status,
            verdict=verdict,
            explanation=explanation,
            is_science=False,
            text=text,
            word_count=word_count,
            science_count=science_count,
            esoteric_count=esoteric_count,
            pseudo_count=pseudo_count,
            hysteria_count=hysteria_count,
            chaos_index=chaos_index,
            influence_index=influence_index,
            sanity_penalty=sanity_penalty
        )
    
    def _check_caps_hysteria(self, text):
        """Перевірка на КАПС-істерію"""
        score = 0.0
        
        # КАПС-слова
        caps_words = [w for w in text.split() if w.isupper() and len(w) > 2]
        if len(caps_words) >= 2:
            score += 0.6
        
        # Оклички
        if text.count('!') >= 3:
            score += 0.4
        
        return min(1.0, score)
    
    def _create_result(self, score, status, verdict, explanation, is_science, text, 
                      word_count, science_count, esoteric_count, pseudo_count, hysteria_count,
                      chaos_index=None, influence_index=None, sanity_penalty=None):
        """Створює стандартизований результат"""
        
        # Розрахунок індексів якщо не передано
        if chaos_index is None:
            chaos_index = score * 100
        
        if influence_index is None:
            influence_index = score * 100 * (1 + hysteria_count * 0.3)
        
        if sanity_penalty is None:
            sanity_penalty = round(score + (esoteric_count + pseudo_count) * 0.1, 3)
        
        return {
            'entropy': round(score, 3),
            'status': status,
            'verdict': verdict,
            'language': 'UK',
            'explanation': explanation,
            'diagnostics': {
                'science_markers': science_count,
                'esoteric_markers': esoteric_count,
                'pseudo_science_markers': pseudo_count,
                'hysteria_markers': hysteria_count,
                'word_count': word_count,
                'char_count': len(text),
                'chaos_index': round(chaos_index, 2),
                'influence_index': round(influence_index, 2),
                'sanity_penalty': sanity_penalty,
                'is_science': is_science
            }
        }
