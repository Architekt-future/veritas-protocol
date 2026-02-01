import math
import re
from collections import Counter


class VeritasHyperCalibratedCore:
    """СМЕРТЕЛЬНО каліброване ядро"""

    def __init__(self):
        # РОЗШИРЕНІ СЛОВНИКИ
        self.chaos_terms = [
            # Конспірологія
            'секрет', 'скрыт', 'скрит', 'заговор', 'конспир', 'рептилоид', 'рептилії',
            'нам не говорят', 'правда скрыта', 'просыпайся', 'просыпайтесь',
            'мировое правительство', 'світовий уряд', 'чипизация', 'чипізація',
            'матрица', 'матриця', 'пробуждение', 'awakening',
            '5g', 'вакцин', 'білл гейтс', 'гейтса', 'чип', 'чипи',
            'атлант', 'атлантида', 'агарта', 'ноосфера', 'ефір',
            # Псевдонаука
            'енергія всесвіту', 'енергия вселенной', 'квантова свідомість', 
            'квантовое сознание', 'шишкоподібна', 'шишковидная', 'чакра', 
            'вібрація', 'пран', 'сольфеджіо', 'карма', 'потойбіч', 'душа',
            'біополе', 'биополе', 'аура', 'енергетичний', 'энергетический',
            'нейромереж', 'нейросеть', '5d', '5d-інтерфейс',
            # Алармізм
            'геноцид', 'зрада', 'зради', 'корупція', 'коррупция', 'хаос',
            'катастрофа', 'апокаліпсис', 'апокалипсис', 'кінець світу', 'конец света',
            'злочин', 'преступление', 'злочинний', 'преступный'
        ]

        self.signal_terms = [
            'дослідження', 'исследование', 'статистика', 'статистики', 'статистике',
            'анализ', 'аналіз', 'гипотеза', 'гіпотеза', 'теорія', 'теория', 'експеримент',
            'эксперимент', 'доказательство', 'доказ', 'факт', 'факти', 'data', 'дані',
            'результат', 'результати', 'метод', 'методологія', 'методология',
            'верифікація', 'верификация', 'кореляція', 'корреляция'
        ]

        self.noise_terms = [
            'шок', 'шокуючий', 'шокирующий', 'невозможно', 'неможливо', 'impossible',
            'omg', 'wow', 'невероятно', 'невіри', 'ужас', 'ужасающий', 'ужасний',
            'срочно', 'urgent', 'внимание', 'увага', 'негайно', 'терміново',
            'бомба', 'взрыв', 'вибух', 'сенсація', 'sensation',
            'розповсюджуйте', 'поширюйте', 'репост', 'share', 'поділіться',
            'ганьба', 'зрадник', 'предатель', 'кримінальний', 'криминальный'
        ]

        # АБСУРДНІ ПАРИ (автоматичний штраф 0.7+)
        self.absurd_pairs = [
            (['квантов', 'суперпозиці', 'ентропі', 'фізика', 'нейтрино'], 
             ['сметан', 'борщ', 'картопл', 'моркв', 'буряк', 'петрушк']),
            (['фінанс', 'економ', 'банк', 'бюджет', 'інвест'], 
             ['карма', 'душа', 'потойбіч', 'чакра', 'енергія всесвіту']),
            (['держав', 'уряд', 'політик', 'закон'], 
             ['рептилоїд', 'атлантид', 'матриця', '5g-частот']),
            (['технологі', 'алгоритм', 'програм', 'цифров'], 
             ['чакра', 'аура', 'біополе', 'шишкоподібна']),
            (['наука', 'досліджен', 'гіпотез', 'експеримент'], 
             ['езотерик', 'містик', 'духовн', 'енергетичний'])
        ]

    def detect_absurdity(self, text):
        """Виявлення абсурдних поєднань (основна логіка)"""
        text_lower = text.lower()
        score = 0.0
        
        for science_terms, absurd_terms in self.absurd_pairs:
            has_science = any(term in text_lower for term in science_terms)
            has_absurd = any(term in text_lower for term in absurd_terms)
            if has_science and has_absurd:
                score += 0.35  # Кожна абсурдна пара = +35%
        
        return min(score, 1.0)

    def calculate_shannon_entropy(self, text):
        """Ентропія Шеннона"""
        if not text:
            return 0.0
        clean = re.sub(r'\s+', ' ', text)
        char_freq = Counter(clean)
        total = len(clean)
        if total == 0:
            return 0.0

        entropy = -sum((count / total) * math.log2(count / total)
                       for count in char_freq.values() if count > 0)
        max_entropy = math.log2(len(char_freq)) if char_freq else 1
        return min(1.0, entropy / max_entropy if max_entropy > 0 else 0)

    def count_markers(self, text):
        """Підрахунок маркерів"""
        text_lower = text.lower()
        counts = {'chaos': 0, 'signal': 0, 'noise': 0}

        for term in self.chaos_terms:
            if term in text_lower:
                counts['chaos'] += 1

        for term in self.signal_terms:
            if term in text_lower:
                counts['signal'] += 1

        for term in self.noise_terms:
            if term in text_lower:
                counts['noise'] += 1

        return counts

    def calculate_emotional_pressure(self, text):
        """Емоційний тиск (капс, оклики)"""
        score = 0.0
        
        # CAPS LOCK
        caps_words = [w for w in text.split() if w.isupper() and len(w) > 2]
        score += min(0.3, len(caps_words) * 0.08)
        
        # ДЕКІЛЬКА ОКЛИКНИХ ЗНАКІВ
        excl = text.count('!') + text.count('!!!')
        score += min(0.2, excl * 0.05)
        
        # ТРИВОЖНІ СЛОВА
        alarm_words = ['негайно', 'терміново', 'срочно', 'последний', 'останній', 'зрада', 'ганьба']
        if any(word in text.lower() for word in alarm_words):
            score += 0.25
            
        return min(score, 0.7)

    def analyze(self, text):
        """ОСНОВНИЙ МЕТОД (спрощений та потужний)"""
        if not text or len(text.strip()) < 20:
            return {'error': 'Text too short'}

        words = text.split()
        word_count = len(words)
        
        # БАЗОВІ МЕТРИКИ
        shannon = self.calculate_shannon_entropy(text)
        markers = self.count_markers(text)
        absurdity = self.detect_absurdity(text)
        emotional = self.calculate_emotional_pressure(text)
        
        # ================= ГОЛОВНА ФОРМУЛА =================
        # Тепер супер-агресивна!
        base_score = (
            (markers['chaos'] / max(1, word_count)) * 0.40 +    # 40% за хаос-маркери
            absurdity * 0.35 +                                  # 35% за абсурдні пари
            emotional * 0.25 +                                  # 25% за емоційний тиск
            (markers['noise'] / max(1, word_count)) * 0.15      # 15% за шум
        )
        
        # АКАДЕМІЧНИЙ ЗАХИСТ (тільки для справді наукових текстів)
        if markers['signal'] >= 3 and markers['chaos'] == 0:
            base_score *= 0.2  # -80% для чистої науки
        elif markers['signal'] >= 2:
            base_score *= 0.5  # -50% для напівнаукових
            
        final_score = min(0.99, max(0.0, base_score))
        
        # ================= ВЕРДИКТ =================
        if absurdity > 0.3:
            status = 'CRITICAL'
            verdict = 'АБСУРДНИЙ СЕМАНТИЧНИЙ РОЗРИВ'
            explanation = 'Текст поєднує несумісні поняття (наука + абсурд)'
        elif final_score > 0.7:
            status = 'CRITICAL'
            verdict = 'ВИСОКИЙ РІВЕНЬ ІНФОРМАЦІЙНОГО ХАОСУ'
            explanation = 'Текст демонструє катастрофічну семантичну несумісність'
        elif final_score > 0.5:
            status = 'WARNING'
            verdict = 'МАНІПУЛЯТИВНА СТРУКТУРА'
            explanation = 'Текст містить ознаки інформаційної маніпуляції'
        elif final_score > 0.3:
            status = 'ACCEPTABLE'
            verdict = 'ПРИЙНЯТНА ІНФОРМАЦІЙНА СТРУКТУРА'
            explanation = 'Текст відповідає нормам логічної сумісності'
        elif final_score > 0.15:
            status = 'TRUSTED'
            verdict = 'СТАБІЛЬНИЙ ЛОГІЧНИЙ СИГНАЛ'
            explanation = 'Текст демонструє логічну цілісність'
        else:
            status = 'VERIFIED'
            verdict = 'ВЕРИФІКОВАНИЙ АКАДЕМІЧНИЙ СИГНАЛ'
            explanation = 'Текст демонструє ідеальну логічну цілісність'
        
        # ================= НОВІ МЕТРИКИ =================
        # Chaos Index тепер АГРЕСИВНИЙ
        chaos_index = round(final_score * 100 * (1 + markers['chaos'] * 0.7), 2)
        
        # Influence Index
        influence_index = round(
            final_score * 150 * (1 + emotional * 0.8) * (1 + markers['noise'] * 0.4),
            2
        )
        
        # Sanity Penalty = абсурдність + емоції
        sanity_penalty = round(absurdity + emotional, 3)
        
        return {
            'entropy': round(final_score, 3),
            'status': status,
            'verdict': verdict,
            'language': 'UK',
            'explanation': explanation,
            'diagnostics': {
                'shannon_entropy': round(shannon, 3),
                'word_count': word_count,
                'char_count': len(text),
                'chaos_markers': markers['chaos'],
                'signal_markers': markers['signal'],
                'noise_markers': markers['noise'],
                'absurdity_score': round(absurdity, 3),
                'emotional_pressure': round(emotional, 3),
                'chaos_index': chaos_index,
                'influence_index': influence_index,
                'sanity_penalty': sanity_penalty
            }
        }
