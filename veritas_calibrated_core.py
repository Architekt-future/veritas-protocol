import math
import re
from collections import Counter, defaultdict


class VeritasUltraCalibratedCore:
    """УЛЬТРА-АГРЕСИВНЕ ЯДРО ДЛЯ ТЕСТІВ"""
    
    def __init__(self):
        # МІНІМАЛІСТИЧНІ, АЛЕ ПОТУЖНІ КАТЕГОРІЇ
        self.categories = {
            'science': ['досліджен', 'статистик', 'анализ', 'гіпотез', 'експеримент', 'факт'],
            'pseudoscience': ['квантов', 'ентропі', 'флуктуаці', 'тунельн', 'хвильов', 'сингуляр'],
            'conspiracy': ['заговор', 'конспир', 'скрыт', 'матриц', 'рептил', '5g', 'вакцин'],
            'esotericism': ['чакра', 'карма', 'душа', 'астрал', 'енергет', 'вібраці', 'пран'],
            'alarmism': ['негайн', 'срочн', 'зрад', 'ганьб', 'катастроф', 'апокаліпс', 'шок'],
            'culinary': ['борщ', 'сметан', 'картопл', 'моркв', 'буряк', 'суп', 'бульйон', 'їжа']
        }
        
        # АБСУРДНІ КОМБІНАЦІЇ (автоматичний CRITICAL)
        self.absurd_combinations = [
            (['квантов', 'ентропі', 'сингуляр', 'флуктуаці'],  # наукові терміни
             ['борщ', 'сметан', 'картопл', 'моркв', 'суп']),   # кулінарія
            (['чакра', 'карма', 'душа', 'енергет'],           # езотерика
             ['банк', 'фінанс', 'економ', 'крипто', 'інвест']), # фінанси
            (['матриц', 'рептил', 'заговор', '5g'],           # конспірологія
             ['уряд', 'держав', 'політик', 'закон'])           # політика
        ]

    def detect_absurd_combinations(self, text):
        """Виявляє абсурдні комбінації термінів"""
        text_lower = text.lower()
        score = 0.0
        
        for science_terms, absurd_terms in self.absurd_combinations:
            has_science = any(term in text_lower for term in science_terms)
            has_absurd = any(term in text_lower for term in absurd_terms)
            
            if has_science and has_absurd:
                score += 0.5  # КОЖНА абсурдна комбінація = +50%!
        
        return min(score, 1.0)

    def analyze_text_by_sentences(self, text):
        """Аналізує кожне речення окремо"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.split()) > 3]
        
        if not sentences:
            return 0.0, 0
        
        absurd_sentences = 0
        total_penalty = 0.0
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            
            # Шукаємо абсурдні комбінації в реченні
            absurd_score = 0.0
            for science_terms, absurd_terms in self.absurd_combinations:
                has_science = any(term in sentence_lower for term in science_terms)
                has_absurd = any(term in sentence_lower for term in absurd_terms)
                
                if has_science and has_absurd:
                    absurd_score += 0.6
                    absurd_sentences += 1
            
            # CAPS LOCK в реченні
            caps_words = [w for w in sentence.split() if w.isupper() and len(w) > 2]
            if caps_words:
                absurd_score += 0.3
            
            # Окличні знаки
            if '!' in sentence:
                absurd_score += 0.2
            
            total_penalty += min(absurd_score, 0.8)
        
        avg_penalty = total_penalty / len(sentences) if sentences else 0.0
        return avg_penalty, absurd_sentences

    def analyze(self, text):
        """ОСНОВНА ЛОГІКА"""
        if not text or len(text.strip()) < 20:
            return {'error': 'Text too short'}
        
        words = text.split()
        word_count = len(words)
        
        # ОСНОВНА ПЕРЕВІРКА: абсурдні комбінації
        absurd_score = self.detect_absurd_combinations(text)
        
        # Аналіз по реченнях
        sentence_penalty, absurd_sentences = self.analyze_text_by_sentences(text)
        
        # CAPS LOCK загальний
        caps_words = [w for w in words if w.isupper() and len(w) > 2]
        caps_score = min(0.4, len(caps_words) * 0.1)
        
        # ================= АГРЕСИВНА ФОРМУЛА =================
        base_score = (
            absurd_score * 0.70 +           # 70% за абсурдні комбінації
            sentence_penalty * 0.50 +       # 50% за речення з абсурдом
            caps_score * 0.30 +             # 30% за CAPS
            (absurd_sentences / max(1, len(re.split(r'[.!?]+', text)))) * 0.40
        )
        
        # МІНІМАЛЬНИЙ БАЛ ДЛЯ АБСУРДНИХ ТЕКСТІВ
        if absurd_score > 0.3:
            base_score = max(base_score, 0.65)
        
        final_score = min(0.99, max(0.0, base_score))
        
        # ================= ВЕРДИКТ =================
        if absurd_score > 0.3 or absurd_sentences > 0:
            status = 'CRITICAL'
            verdict = 'АБСУРДНИЙ СЕМАНТИЧНИЙ РОЗРИВ'
            explanation = f'Знайдено {absurd_sentences} речень з абсурдними комбінаціями термінів'
        elif final_score > 0.6:
            status = 'CRITICAL'
            verdict = 'ВИСОКИЙ РІВЕНЬ ІНФОРМАЦІЙНОГО ХАОСУ'
            explanation = 'Текст поєднує несумісні концепції'
        elif final_score > 0.4:
            status = 'WARNING'
            verdict = 'МАНІПУЛЯТИВНА СТРУКТУРА'
            explanation = 'Текст містить ознаки семантичної маніпуляції'
        elif final_score > 0.2:
            status = 'ACCEPTABLE'
            verdict = 'ПРИЙНЯТНА СТРУКТУРА'
            explanation = 'Текст відповідає нормам логічної сумісності'
        else:
            status = 'VERIFIED'
            verdict = 'ВЕРИФІКОВАНИЙ СИГНАЛ'
            explanation = 'Текст демонструє логічну цілісність'
        
        # ================= МЕТРИКИ =================
        chaos_index = round(final_score * 100 * (1 + absurd_sentences * 0.5), 2)
        influence_index = round(final_score * 150 * (1 + caps_score * 0.7), 2)
        sanity_penalty = round(absurd_score + sentence_penalty, 3)
        
        return {
            'entropy': round(final_score, 3),
            'status': status,
            'verdict': verdict,
            'language': 'UK',
            'explanation': explanation,
            'diagnostics': {
                'word_count': word_count,
                'char_count': len(text),
                'absurd_score': round(absurd_score, 3),
                'sentence_penalty': round(sentence_penalty, 3),
                'absurd_sentences': absurd_sentences,
                'caps_words': len(caps_words),
                'chaos_index': chaos_index,
                'influence_index': influence_index,
                'sanity_penalty': sanity_penalty
            }
        }
