"""
Veritas Protocol - Semantic Void Detector v10.4 (Fixed Categories)
Фікс категорій для пар
"""

import re
import math
from collections import defaultdict

class VeritasCalibratedCore:
    """Детектор з правильними категоріями для пар"""
    
    def __init__(self):
        # ============================================================
        # ХАОС-ІНДИКАТОРИ З КАТЕГОРІЯМИ ДЛЯ ПАР
        # ============================================================
        self.chaos_indicators = {
            'emotional_manipulation': {
                'terms': ['срочно', 'терміново', 'зрада', 'ганьба', 'катастрофа',
                         'апокаліпсис', 'кінець світу', 'останній', 'шок', 'шокуючий',
                         'ужас', 'бомба', 'взрив', 'вибух', 'сенсація', 'не можу мовчати',
                         'вимагати', 'важливо', 'негайно', 'пізно', 'хаос', 'злочинний',
                         'геноцид', 'кримінальний', 'корупція', 'репост', 'куля'],
                'pair_category': 'emotion_conflict'
            },
            'conspiracy': {
                'terms': ['приховує', 'правда', 'система', 'влада', 'вони', 'ваші', 'кишені',
                         'викачують', 'національні', 'інтереси', 'таємно', 'секретно'],
                'pair_category': 'authority_conflict'
            },
            'social_pressure': {
                'terms': ['поширюйте', 'спите', 'маємо', 'вийти', 'вулиці', 'сьогодні', 
                         'завтра', 'зупинимо', 'разом', 'кожен', 'репост', 'поділися',
                         'швидше', 'всі', 'ми'],
                'pair_category': 'social_conflict'
            },
            'alarmism': {
                'terms': ['геноцид', 'вимирання', 'крах', 'загибель', 'катастрофа',
                         'неминучий', 'терміновий', 'пізно', 'останній шанс'],
                'pair_category': 'alarm_conflict'
            }
        }
        
        # ============================================================
        # АБСУРДНІ ПАРИ З КАТЕГОРІЯМИ
        # ============================================================
        self.absurd_pairs = [
            {
                'science_terms': ['квантовий', 'квантова', 'квантове', 'квантові'],
                'absurd_terms': ['борщ', 'сметана', 'картопля', 'морква', 'суп'],
                'category': 'quantum_food',
                'weight': 0.4
            },
            {
                'science_terms': ['ентропія', 'флуктуація', 'тунельний'],
                'absurd_terms': ['борщ', 'каструля', 'бульйон', 'черпак'],
                'category': 'physics_food', 
                'weight': 0.35
            },
        ]
        
        # ============================================================
        # КОНФЛІКТНІ ПАРИ З КАТЕГОРІЯМИ
        # ============================================================
        self.conflict_pairs = [
            {
                'group1': ['влада', 'уряд', 'держава', 'система'],
                'group2': ['зрада', 'ганьба', 'корупція', 'кримінальний', 'злочин'],
                'category': 'authority_vs_crime',
                'weight': 0.4
            },
            {
                'group1': ['гроші', 'тариф', 'кишені', 'кошти', 'фінанси'],
                'group2': ['геноцид', 'викачують', 'останні', 'краде', 'обкрадає'],
                'category': 'money_vs_genocide',
                'weight': 0.35
            },
            {
                'group1': ['народ', 'люди', 'громадяни', 'суспільство'],
                'group2': ['спить', 'небачить', 'сліпий', 'наївний'],
                'category': 'people_vs_ignorance',
                'weight': 0.3
            }
        ]

    def count_chaos_terms_with_categories(self, text):
        """Підрахунок хаос-термінів з категоріями"""
        text_lower = text.lower()
        category_counts = defaultdict(int)
        term_details = []
        
        for category, data in self.chaos_indicators.items():
            terms = data['terms']
            pair_category = data.get('pair_category', '')
            
            for term in terms:
                if term in text_lower:
                    category_counts[category] += 1
                    term_details.append({
                        'term': term,
                        'category': category,
                        'pair_category': pair_category
                    })
        
        total_chaos = sum(category_counts.values())
        
        return dict(category_counts), total_chaos, term_details

    def detect_absurdity_with_categories(self, text):
        """Пошук абсурдних пар з категоріями"""
        text_lower = text.lower()
        found_pairs = []
        score = 0.0
        
        for pair_config in self.absurd_pairs:
            science_terms = pair_config['science_terms']
            absurd_terms = pair_config['absurd_terms']
            category = pair_config['category']
            weight = pair_config['weight']
            
            has_science = any(term in text_lower for term in science_terms)
            has_absurd = any(term in text_lower for term in absurd_terms)
            
            if has_science and has_absurd:
                # Знаходимо конкретні терміни
                science_word = next((t for t in science_terms if t in text_lower), science_terms[0])
                absurd_word = next((t for t in absurd_terms if t in text_lower), absurd_terms[0])
                
                # Перевіряємо, чи в одному реченні
                sentences = re.split(r'[.!?]+', text)
                in_same_sentence = False
                
                for sentence in sentences:
                    sentence_lower = sentence.lower()
                    if science_word in sentence_lower and absurd_word in sentence_lower:
                        in_same_sentence = True
                        break
                
                if in_same_sentence:
                    score += weight
                    found_pairs.append({
                        'science': science_word,
                        'absurd': absurd_word,
                        'category': category,
                        'weight': weight,
                        'in_same_sentence': True
                    })
        
        return min(score, 0.8), found_pairs

    def calculate_conflict_penalty_with_categories(self, text):
        """Штраф за конфліктні пари з категоріями"""
        text_lower = text.lower()
        penalty = 0.0
        conflict_details = []
        
        for pair_config in self.conflict_pairs:
            group1 = pair_config['group1']
            group2 = pair_config['group2']
            category = pair_config['category']
            weight = pair_config['weight']
            
            has_first = any(term in text_lower for term in group1)
            has_second = any(term in text_lower for term in group2)
            
            if has_first and has_second:
                # Знаходимо конкретні терміни
                term1 = next((t for t in group1 if t in text_lower), group1[0])
                term2 = next((t for t in group2 if t in text_lower), group2[0])
                
                penalty += weight
                conflict_details.append({
                    'term1': term1,
                    'term2': term2,
                    'category': category,
                    'weight': weight
                })
        
        return min(penalty, 0.5), conflict_details

    def calculate_emotional_intensity_with_details(self, text):
        """Розрахунок емоційної інтенсивності з деталями"""
        text_lower = text.lower()
        score = 0.0
        details = {
            'caps_words': [],
            'exclamation_count': 0,
            'emotional_terms': []
        }
        
        # CAPS LOCK
        caps_words = [w for w in text.split() if w.isupper() and len(w) > 2]
        details['caps_words'] = caps_words
        score += min(0.3, len(caps_words) * 0.1)
        
        # Окличні знаки
        excl_count = text.count('!')
        details['exclamation_count'] = excl_count
        score += min(0.2, excl_count * 0.05)
        
        # Емоційні маркери
        emotional_data = self.chaos_indicators['emotional_manipulation']
        emotional_terms = emotional_data['terms']
        
        found_emotional = []
        for term in emotional_terms:
            if term in text_lower:
                found_emotional.append(term)
                score += 0.08
        
        details['emotional_terms'] = found_emotional
        score = min(score, 0.7)
        
        return score, details

    def analyze_with_full_categories(self, text):
        """ПОВНИЙ аналіз з усіма категоріями"""
        if not text or len(text.strip()) < 20:
            return {'error': 'Text too short'}
        
        words = text.split()
        word_count = len(words)
        
        # 1. ОСНОВНІ МЕТРИКИ
        shannon_entropy = self.calculate_shannon_entropy(text)
        complexity = self.calculate_complexity(text)
        
        # 2. ТЕРМІНОЛОГІЧНІ ПІДРАХУНКИ З КАТЕГОРІЯМИ
        chaos_by_category, total_chaos, term_details = self.count_chaos_terms_with_categories(text)
        emotional_score, emotional_details = self.calculate_emotional_intensity_with_details(text)
        conflict_penalty, conflict_details = self.calculate_conflict_penalty_with_categories(text)
        absurdity_score, absurd_pairs = self.detect_absurdity_with_categories(text)
        
        # 3. АНАЛІЗ КАТЕГОРІЙ
        category_analysis = {
            'has_emotional_manipulation': chaos_by_category.get('emotional_manipulation', 0) > 0,
            'has_conspiracy': chaos_by_category.get('conspiracy', 0) > 0,
            'has_social_pressure': chaos_by_category.get('social_pressure', 0) > 0,
            'has_alarmism': chaos_by_category.get('alarmism', 0) > 0,
            'conflict_categories': [c['category'] for c in conflict_details],
            'absurd_categories': [p['category'] for p in absurd_pairs]
        }
        
        # 4. КЛЮЧОВІ СПІВВІДНОШЕННЯ
        chaos_ratio = total_chaos / max(1, word_count)
        emotional_ratio = emotional_score
        conflict_ratio = conflict_penalty
        
        # 5. ФІНАЛЬНА ФОРМУЛА (з категоріями)
        base_score = (
            shannon_entropy * 0.10 +
            complexity * 0.10 +
            chaos_ratio * 0.25 +
            emotional_ratio * 0.25 +
            conflict_ratio * 0.20 +
            absurdity_score * 0.10
        )
        
        # 6. КРИТИЧНІ ШТРАФИ ЗА КАТЕГОРІЇ
        # Штраф за комбінацію категорій
        if (category_analysis['has_emotional_manipulation'] and 
            category_analysis['has_social_pressure']):
            base_score += 0.15
        
        if (category_analysis['has_conspiracy'] and 
            category_analysis['has_alarmism']):
            base_score += 0.20
        
        # Штраф за конкретні конфліктні категорії
        if 'authority_vs_crime' in category_analysis['conflict_categories']:
            base_score += 0.10
        
        if 'money_vs_genocide' in category_analysis['conflict_categories']:
            base_score += 0.15
        
        final_score = min(0.99, max(0.0, base_score))
        
        # 7. РОЗРАХУНОК ІНДЕКСІВ
        chaos_index = round(final_score * 100 * (1 + total_chaos * 0.5), 2)
        influence_index = round(final_score * 150 * (1 + emotional_ratio * 0.5), 2)
        sanity_penalty = round(conflict_ratio + emotional_ratio * 0.5, 3)
        
        # 8. ВЕРДИКТ НА ОСНОВІ КАТЕГОРІЙ
        if absurdity_score > 0.3 and absurd_pairs:
            status = 'CRITICAL'
            verdict = 'АБСУРДНИЙ СЕМАНТИЧНИЙ РОЗРИВ'
            categories = ", ".join(set([p['category'] for p in absurd_pairs]))
            explanation = f'Категорії абсурду: {categories}'
        elif final_score > 0.7 or ('authority_vs_crime' in category_analysis['conflict_categories'] 
                                 and 'money_vs_genocide' in category_analysis['conflict_categories']):
            status = 'CRITICAL'
            verdict = 'ВИСОКИЙ РІВЕНЬ ПОЛІТИЧНОЇ МАНІПУЛЯЦІЇ'
            explanation = 'Поєднання категорій: влада+злочин + гроші+геноцид'
        elif final_score > 0.55 or category_analysis['has_emotional_manipulation']:
            status = 'WARNING'
            verdict = 'ЕМОЦІЙНА МАНІПУЛЯЦІЯ'
            explanation = 'Використання емоційного тиску та соціального примусу'
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
        
        # Додаткові деталі по категоріях
        details = []
        if chaos_by_category.get('emotional_manipulation', 0) > 3:
            details.append(f"Емоційна маніпуляція: {chaos_by_category['emotional_manipulation']}")
        if chaos_by_category.get('conspiracy', 0) > 0:
            details.append(f"Конспірологія: {chaos_by_category['conspiracy']}")
        if conflict_details:
            conflict_cats = ", ".join(set([c['category'] for c in conflict_details]))
            details.append(f"Конфлікти: {conflict_cats}")
        if absurd_pairs:
            absurd_cats = ", ".join(set([p['category'] for p in absurd_pairs]))
            details.append(f"Абсурд: {absurd_cats}")
        
        if details:
            explanation += " | " + " + ".join(details)
        
        # 9. ПОВНИЙ РЕЗУЛЬТАТ
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
                'conflict_pairs_found': len(conflict_details),
                'caps_words_count': len(emotional_details['caps_words']),
                'exclamation_count': emotional_details['exclamation_count'],
                'chaos_ratio': round(chaos_ratio, 3),
                'chaos_index': chaos_index,
                'influence_index': influence_index,
                'sanity_penalty': sanity_penalty,
                'category_analysis': category_analysis,
                'term_details_count': len(term_details),
                'conflict_details': conflict_details[:3],  # Перші 3 конфлікти
                'absurd_details': absurd_pairs[:3],  # Перші 3 абсурдні пари
                'emotional_terms_found': len(emotional_details['emotional_terms'])
            }
        }

    # Допоміжні методи
    def calculate_shannon_entropy(self, text):
        if not text: return 0.0
        clean_text = re.sub(r'\s+', ' ', text)
        char_freq = {}
        for char in clean_text:
            if char.isalpha() or char.isdigit():
                char_freq[char] = char_freq.get(char, 0) + 1
        if not char_freq: return 0.0
        entropy = 0.0
        text_len = len(clean_text)
        for count in char_freq.values():
            p = count / text_len
            if p > 0: entropy -= p * math.log2(p)
        max_entropy = math.log2(len(char_freq))
        return min(1.0, entropy / max_entropy if max_entropy > 0 else 0)

    def calculate_complexity(self, text):
        words = re.findall(r'\w+', text.lower())
        if len(words) < 10: return 0.5
        unique_ratio = len(set(words)) / len(words)
        sentences = re.split(r'[.!?]+', text)
        avg_len = sum(len(s.split()) for s in sentences if s.strip()) / len(sentences) if sentences else 10
        return min(1.0, (unique_ratio * 0.6) + (min(1.0, avg_len / 25) * 0.4))

    def analyze(self, text):
        """Головний метод"""
        return self.analyze_with_full_categories(text)

# ============================================================
# ТЕСТ
# ============================================================

if __name__ == "__main__":
    detector = VeritasCalibratedCore()
    
    test_text = """НЕГАЙНО ПОШИРЮЙТЕ ЦЕ! Влада приховує ПРАВДУ про тарифний геноцид! 
    Поки ви спите, вони викачують ОСТАННІ гроші з ваших кишень! Це ЗРАДА національних інтересів! 
    ГАНЬБА! Ми маємо вийти на вулиці сьогодні, або завтра буде ПІЗНО! 
    Зупинимо цей КРИМІНАЛЬНИЙ ХАОС разом! Кожен репост — це куля в систему корупції!"""
    
    result = detector.analyze(test_text)
    
    print("="*50)
    print("⚡ ДЕТАЛЬНИЙ АНАЛІЗ З КАТЕГОРІЯМИ")
    print("="*50)
    print(f"Оцінка: {result['entropy']:.3f} ({int(result['entropy']*100)}%)")
    print(f"Статус: {result['status']}")
    print(f"Вердикт: {result['verdict']}")
    print(f"Пояснення: {result['explanation']}")
    print()
    print("📊 КАТЕГОРІЇ ХАОСУ:")
    for cat, count in result['diagnostics']['chaos_by_category'].items():
        print(f"  {cat}: {count} термінів")
    print()
    print("⚔️ КОНФЛІКТНІ КАТЕГОРІЇ:")
    for conflict in result['diagnostics']['conflict_details']:
        print(f"  {conflict['category']}: {conflict['term1']} + {conflict['term2']}")
    print()
    print("📈 МЕТРИКИ:")
    print(f"  Слова: {result['diagnostics']['word_count']}")
    print(f"  CAPS слів: {result['diagnostics']['caps_words_count']}")
    print(f"  Знаків оклику: {result['diagnostics']['exclamation_count']}")
    print(f"  Індекс хаосу: {result['diagnostics']['chaos_index']}")
    print(f"  Штраф логіки: {result['diagnostics']['sanity_penalty']}")
    print("="*50)
