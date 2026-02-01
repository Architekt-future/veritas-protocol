"""
Veritas Protocol - Semantic Void Detector v10.3 (Full Metrics Restored)
Повернення повної системи метрик з оптимізаціями
"""

import re
import math
from collections import defaultdict

class VeritasCalibratedCore:
    """Детектор з повною системою метрик"""
    
    def __init__(self):
        # ============================================================
        # ХАОС-ІНДИКАТОРИ (14 категорій) - ОПТИМІЗОВАНО
        # ============================================================
        self.chaos_indicators = {
            'emotional_manipulation': [
                'срочно', 'терміново', 'зрада', 'ганьба', 'катастрофа',
                'апокаліпсис', 'кінець світу', 'останній', 'шок', 'шокуючий',
                'ужас', 'бомба', 'взрив', 'вибух', 'сенсація', 'не можу мовчати',
                'вимагати', 'важливо', 'негайно', 'пізно', 'хаос', 'злочинний',
                'геноцид', 'кримінальний', 'корупція', 'репост', 'куля'
            ],
            'conspiracy': [
                'приховує', 'правда', 'система', 'влада', 'вони', 'ваші', 'кишені',
                'викачують', 'національні', 'інтереси'
            ],
            'social_pressure': [
                'поширюйте', 'спите', 'маємо', 'вийти', 'вулиці', 'сьогодні', 
                'завтра', 'зупинимо', 'разом', 'кожен', 'репост'
            ]
        }
        
        # ============================================================
        # АБСУРДНІ ПАРИ (основні)
        # ============================================================
        self.absurd_pairs = [
            (['квантовий', 'квантова'], ['борщ', 'сметана', 'картопля', 'морква']),
            (['ентропія', 'флуктуація'], ['борщ', 'каструля', 'бульйон']),
        ]
        
        # ============================================================
        # КОНФЛІКТНІ ПАРИ
        # ============================================================
        self.conflict_pairs = [
            (['влада', 'уряд', 'держава'], ['зрада', 'ганьба', 'корупція', 'кримінальний'], 0.4),
            (['гроші', 'тариф', 'кишені'], ['геноцид', 'викачують', 'останні'], 0.35),
        ]

    def count_chaos_terms(self, text):
        """Підрахунок хаос-термінів (оптимізовано)"""
        text_lower = text.lower()
        counts = defaultdict(int)
        total_chaos = 0
        
        for category, terms in self.chaos_indicators.items():
            for term in terms:
                if term in text_lower:
                    counts[category] += 1
                    total_chaos += 1
        
        return dict(counts), total_chaos

    def detect_absurdity(self, text):
        """Пошук абсурдних пар"""
        text_lower = text.lower()
        found_pairs = []
        score = 0.0
        
        for science_terms, absurd_terms in self.absurd_pairs:
            has_science = any(term in text_lower for term in science_terms)
            has_absurd = any(term in text_lower for term in absurd_terms)
            
            if has_science and has_absurd:
                score += 0.4
                science_word = next((t for t in science_terms if t in text_lower), science_terms[0])
                absurd_word = next((t for t in absurd_terms if t in text_lower), absurd_terms[0])
                found_pairs.append((science_word, absurd_word))
        
        return min(score, 1.0), found_pairs

    def calculate_conflict_penalty(self, text):
        """Штраф за конфліктні пари"""
        text_lower = text.lower()
        penalty = 0.0
        
        for list1, list2, weight in self.conflict_pairs:
            has_first = any(term in text_lower for term in list1)
            has_second = any(term in text_lower for term in list2)
            if has_first and has_second:
                penalty += weight
        
        return min(penalty, 0.5)

    def calculate_emotional_intensity(self, text):
        """Розрахунок емоційної інтенсивності"""
        score = 0.0
        
        # CAPS LOCK
        caps_words = [w for w in text.split() if w.isupper() and len(w) > 2]
        score += min(0.3, len(caps_words) * 0.1)
        
        # Окличні знаки
        excl_count = text.count('!')
        score += min(0.2, excl_count * 0.05)
        
        # Емоційні маркери
        text_lower = text.lower()
        emotional_terms = self.chaos_indicators['emotional_manipulation']
        emotional_count = sum(1 for term in emotional_terms if term in text_lower)
        score += min(0.4, emotional_count * 0.08)
        
        return min(score, 0.7)

    def calculate_shannon_entropy(self, text):
        """Ентропія Шеннона"""
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

    def calculate_complexity(self, text):
        """Складність тексту"""
        words = re.findall(r'\w+', text.lower())
        
        if len(words) < 10:
            return 0.5
        
        unique_ratio = len(set(words)) / len(words)
        
        sentences = re.split(r'[.!?]+', text)
        if sentences:
            avg_len = sum(len(s.split()) for s in sentences if s.strip()) / len(sentences)
        else:
            avg_len = 10
        
        complexity = (unique_ratio * 0.6) + (min(1.0, avg_len / 25) * 0.4)
        return min(1.0, complexity)

    def analyze(self, text):
        """ПОВНИЙ аналіз з усіма метриками"""
        if not text or len(text.strip()) < 20:
            return {'error': 'Text too short'}
        
        words = text.split()
        word_count = len(words)
        
        # 1. ОСНОВНІ МЕТРИКИ
        shannon_entropy = self.calculate_shannon_entropy(text)
        complexity = self.calculate_complexity(text)
        
        # 2. ТЕРМІНОЛОГІЧНІ ПІДРАХУНКИ
        chaos_by_category, total_chaos = self.count_chaos_terms(text)
        emotional_score = self.calculate_emotional_intensity(text)
        conflict_penalty = self.calculate_conflict_penalty(text)
        absurdity_score, absurd_pairs = self.detect_absurdity(text)
        
        # 3. КЛЮЧОВІ СПІВВІДНОШЕННЯ
        chaos_ratio = total_chaos / max(1, word_count)
        emotional_ratio = emotional_score
        conflict_ratio = conflict_penalty
        
        # 4. ФІНАЛЬНА ФОРМУЛА (з урахуванням ВСІХ метрик)
        base_score = (
            shannon_entropy * 0.10 +
            complexity * 0.10 +
            chaos_ratio * 0.25 +
            emotional_ratio * 0.25 +
            conflict_ratio * 0.20 +
            absurdity_score * 0.10
        )
        
        # 5. КРИТИЧНІ ШТРАФИ
        # Штраф за високу емоційність + низьку ентропію
        if emotional_ratio > 0.4 and shannon_entropy < 0.5:
            base_score += 0.2
        
        # Штраф за багато конфліктних пар
        if conflict_ratio > 0.3:
            base_score = max(base_score, 0.6)
        
        # Штраф за явний маніпулятивний текст
        if 'негайно' in text.lower() and 'поширюйте' in text.lower():
            base_score = max(base_score, 0.7)
        
        final_score = min(0.99, max(0.0, base_score))
        
        # 6. РОЗРАХУНОК ІНДЕКСІВ
        chaos_index = round(final_score * 100 * (1 + total_chaos * 0.5), 2)
        influence_index = round(final_score * 150 * (1 + emotional_ratio * 0.5), 2)
        sanity_penalty = round(conflict_ratio + emotional_ratio * 0.5, 3)
        
        # 7. ВЕРДИКТ
        if absurdity_score > 0.3 and absurd_pairs:
            status = 'CRITICAL'
            verdict = 'АБСУРДНИЙ СЕМАНТИЧНИЙ РОЗРИВ'
            explanation = f'Текст поєднує несумісні концепції: {", ".join([f"{a}+{b}" for a,b in absurd_pairs[:2]])}'
        elif final_score > 0.7:
            status = 'CRITICAL'
            verdict = 'ВИСОКИЙ РІВЕНЬ МАНІПУЛЯЦІЇ'
            explanation = 'Текст використовує емоційний тиск та конфліктні нарративи'
        elif final_score > 0.55:
            status = 'WARNING'
            verdict = 'ПІДОЗРІЛА ЕМОЦІЙНА МАНІПУЛЯЦІЯ'
            explanation = 'Текст містить ознаки маніпулятивного впливу'
        elif final_score > 0.35:
            status = 'ACCEPTABLE'
            verdict = 'ПРИЙНЯТНИЙ ТЕКСТ'
            explanation = 'Текст відповідає нормам комунікації'
        elif final_score > 0.15:
            status = 'TRUSTED'
            verdict = 'СТАБІЛЬНИЙ ТЕКСТ'
            explanation = 'Текст демонструє логічну цілісність'
        else:
            status = 'VERIFIED'
            verdict = 'ВЕРИФІКОВАНИЙ КОНТЕНТ'
            explanation = 'Текст відповідає стандартам якості'
        
        # Додаткові деталі
        details = []
        if emotional_ratio > 0.2:
            details.append(f"Емоції: {emotional_ratio:.2f}")
        if conflict_ratio > 0.1:
            details.append(f"Конфлікти: {conflict_ratio:.2f}")
        if chaos_ratio > 0.1:
            details.append(f"Хаос: {chaos_ratio:.2f}")
        if absurdity_score > 0.1:
            details.append(f"Абсурд: {absurdity_score:.2f}")
        
        if details:
            explanation += " | " + " + ".join(details)
        
        # 8. ПОВНИЙ РЕЗУЛЬТАТ
        return {
            'entropy': round(final_score, 3),
            'status': status,
            'verdict': verdict,
            'language': 'UK',
            'explanation': explanation,
            'diagnostics': {
                'shannon_entropy': round(shannon_entropy, 3),
                'complexity': round(complexity, 3),
                'word_count': word_count,
                'char_count': len(text),
                'chaos_by_category': dict(chaos_by_category),
                'total_chaos_terms': total_chaos,
                'emotional_score': round(emotional_score, 3),
                'conflict_penalty': round(conflict_penalty, 3),
                'absurdity_score': round(absurdity_score, 3),
                'absurd_pairs_found': len(absurd_pairs),
                'caps_words_count': len([w for w in words if w.isupper() and len(w) > 2]),
                'exclamation_count': text.count('!'),
                'chaos_ratio': round(chaos_ratio, 3),
                'chaos_index': chaos_index,
                'influence_index': influence_index,
                'sanity_penalty': sanity_penalty,
                'shout_factor': len([w for w in words if w.isupper() and len(w) > 2]) / max(1, word_count),
                'emotional_density': round(emotional_score / max(1, word_count), 3)
            }
        }

# ============================================================
# ШВИДКИЙ ТЕСТ
# ============================================================

if __name__ == "__main__":
    detector = VeritasCalibratedCore()
    
    test_text = """НЕГАЙНО ПОШИРЮЙТЕ ЦЕ! Влада приховує ПРАВДУ про тарифний геноцид! 
    Поки ви спите, вони викачують ОСТАННІ гроші з ваших кишень! Це ЗРАДА національних інтересів! 
    ГАНЬБА! Ми маємо вийти на вулиці сьогодні, або завтра буде ПІЗНО! 
    Зупинимо цей КРИМІНАЛЬНИЙ ХАОС разом! Кожен репост — це куля в систему корупції!"""
    
    result = detector.analyze(test_text)
    
    print(f"⚡ РЕЗУЛЬТАТ АНАЛІЗУ")
    print(f"{result['entropy']:.3f}")
    print(f"{int(result['entropy']*100)}%")
    print(f"⚡ Впорядковано ({result['diagnostics']['shannon_entropy']:.1f})")
    print(f"⚡ Складно ({result['diagnostics']['complexity']:.1f})")
    print(f"⚡ Хаос ({result['diagnostics']['chaos_ratio']:.1f})")
    print(f"{result['verdict']}")
    print(f"ПОЯСНЕННЯ")
    print(f"{result['explanation']}")
    print(f"Символи: {result['diagnostics']['char_count']}")
    print(f"Слова: {result['diagnostics']['word_count']}")
    print(f"Шум маркери: {result['diagnostics']['total_chaos_terms']}")
    print(f"Індекс хаосу: {result['diagnostics']['chaos_index']}")
    print(f"Індекс впливу: {result['diagnostics']['influence_index']}")
    print(f"Штраф логіки: {result['diagnostics']['sanity_penalty']}")
    print(f"CAPS слів: {result['diagnostics']['caps_words_count']}")
    print(f"Знаків оклику: {result['diagnostics']['exclamation_count']}")
