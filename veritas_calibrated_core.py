import re
import math
from collections import Counter

class VeritasAnalyzer:
    """
    Основний аналізатор тексту з виправленою логікою для новинних текстів
    """
    
    def __init__(self):
        self.noise_markers = ['неймовірно', 'шок', 'сенсація', 'невероятно', 'ви не повірите']
        self.signal_markers = ['згідно', 'дані', 'статистика', 'дослідження', 'експерт']
        self.academic_markers = ['методологія', 'гіпотеза', 'емпіричний', 'кореляція', 'дисперсія']
        
    def analyze_text(self, text):
        """
        Повний аналіз тексту з виправленою логікою
        """
        analysis = {}
        
        # Базові метрики
        analysis['word_count'] = len(text.split())
        analysis['char_count'] = len(text)
        
        # Оновлений аналіз логічної сумісності
        logic_score, logic_flags = self._analyze_logical_consistency(text)
        analysis['logic_inconsistency'] = logic_score
        analysis['logic_flags'] = logic_flags
        
        # Інші метрики
        analysis['entropy'] = self._calculate_entropy(text)
        analysis['chaos_index'] = self._calculate_chaos_index(text)
        analysis['noise_markers'] = self._count_markers(text, self.noise_markers)
        analysis['signal_markers'] = self._count_markers(text, self.signal_markers)
        analysis['chaos_markers'] = self._calibrate_chaos_markers(text)  # ОНОВЛЕНО
        analysis['scream_factor'] = self._calculate_scream_factor(text)
        analysis['number_density'] = self._calculate_number_density(text)
        analysis['sanitary_penalty'] = logic_score  # Тепер відповідає логічній сумісності
        analysis['academic_markers'] = self._count_markers(text, self.academic_markers)
        
        # Обчислення похідних метрик
        analysis['noise_signal_ratio'] = (
            analysis['noise_markers'] / analysis['signal_markers'] 
            if analysis['signal_markers'] > 0 else 0
        )
        
        analysis['influence_index'] = self._calculate_influence_index(analysis)
        
        # Визначення прапорів
        flags = []
        if logic_score > 0.7:
            flags.append('КРИТИЧНА НЕСУМІСНІСТЬ ЛОГІКИ')
        elif logic_score > 0.4:
            flags.append('ЧАСТКОВА ЛОГІЧНА НЕСУМІСНІСТЬ')
            
        analysis['flags'] = flags
        
        return analysis
    
    def _analyze_logical_consistency(self, text):
        """
        ВИПРАВЛЕНА ФУНКЦІЯ: Аналіз логічної сумісності з урахуванням контексту
        """
        consistency_score = 0.0
        flags = []
        
        # Контекстні винятки для новинних текстів
        context_exceptions = {
            'військовий_контекст': [
                'тимчасово окуповані', 'тимчасово окупована', 'окупаційна адміністрація',
                'збройні сили', 'сили оборони', 'жива сила', 'зсу рф',
                'бойовий потенціал', 'наступальні спроможності', 'завдано ураження',
                'пункт управління', 'район населеного пункту', 'втрати противника',
                'генеральний штаб', 'результати удару', 'уточнюються'
            ],
            'новинний_контекст': [
                'повідомляє', 'інформує', 'зазначається', 'окремо зазначається',
                'крім того', 'також', 'при цьому', 'за даними'
            ]
        }
        
        # Нормальні логічні зв'язки
        normal_connectors = [
            'також', 'крім того', 'окремо', 'при цьому', 'однак', 'проте',
            'незважаючи на', 'хоча', 'в той же час', 'з одного боку', 'з іншого боку'
        ]
        
        # Справжні протиріччя (тільки в межах одного речення)
        real_contradictions = [
            ('повністю виграли', 'повністю програли'),
            ('абсолютно точно', 'можливо'),
            ('завжди', 'ніколи'),
            ('всі без винятку', 'жоден'),
            ('підтверджено наукою', 'спростовано')
        ]
        
        text_lower = text.lower()
        
        # Автоматично знижуємо штраф для військових новин
        has_military_context = any(
            phrase in text_lower for phrase in context_exceptions['військовий_контекст']
        )
        has_news_context = any(
            phrase in text_lower for phrase in context_exceptions['новинний_контекст']
        )
        
        if has_military_context:
            consistency_score = 0.1  # Дуже низький штраф для військових звітів
            return consistency_score, flags
        
        # Аналіз тільки для не-новинних текстів
        sentences = re.split(r'[.!?]+', text)
        contradiction_count = 0
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            
            for term1, term2 in real_contradictions:
                if term1 in sentence_lower and term2 in sentence_lower:
                    # Перевірка чи це не частина нормального зв'язку
                    has_normal_connector = any(
                        connector in sentence_lower for connector in normal_connectors
                    )
                    
                    if not has_normal_connector:
                        contradiction_count += 1
        
        # Обчислення штрафу
        if contradiction_count > 0:
            consistency_score = min(0.9, contradiction_count * 0.3)
            
            if consistency_score > 0.7:
                flags.append('КРИТИЧНА НЕСУМІСНІСТЬ ЛОГІКИ')
        
        return consistency_score, flags
    
    def _calibrate_chaos_markers(self, text):
        """
        ВИПРАВЛЕНА ФУНКЦІЯ: Калібрує маркери хаосу
        """
        chaos_markers = 0
        text_lower = text.lower()
        
        # Справжні маркери хаосу
        real_chaos_terms = {
            'світова закуліса': 5,
            'рептилоїди': 5,
            'плоска земля': 5,
            'хімічні стежи': 4,
            'вакцинна змова': 4,
            '5g випромінювання': 4,
            'біолабораторії сша': 4,
            'глибокий стан': 4,
            'ілюмінати': 3,
            'зомбування': 3
        }
        
        # Нормальні терміни (не рахувати)
        normal_terms = [
            'тимчасово окуповані', 'зсу рф', 'жива сила',
            'пункт управління', 'бойовий потенціал',
            'район населеного пункту', 'генеральний штаб'
        ]
        
        # Рахуємо тільки справжні маркери
        for term, weight in real_chaos_terms.items():
            if term in text_lower:
                # Перевіряємо чи це не частина нормального контексту
                is_normal = False
                for normal in normal_terms:
                    if normal in text_lower and term not in normal:
                        is_normal = False
                        break
                
                if not is_normal:
                    chaos_markers += weight
        
        return chaos_markers
    
    def _calculate_entropy(self, text):
        """Обчислення ентропії Шеннона"""
        if not text:
            return 0
        
        char_count = Counter(text.lower())
        total_chars = len(text)
        entropy = 0
        
        for count in char_count.values():
            probability = count / total_chars
            if probability > 0:
                entropy -= probability * math.log2(probability)
        
        return round(entropy, 3)
    
    def _calculate_chaos_index(self, text):
        """Обчислення індексу хаосу"""
        words = text.split()
        if len(words) < 10:
            return 0
        
        # Спрощена версія
        chaos_score = 0
        
        # Кількість знаків оклику та питань
        chaos_score += text.count('!') * 0.1
        chaos_score += text.count('?') * 0.05
        
        # Великі літери
        upper_ratio = sum(1 for c in text if c.isupper()) / len(text) if text else 0
        chaos_score += upper_ratio * 2
        
        return round(chaos_score, 3)
    
    def _count_markers(self, text, markers):
        """Підрахунок маркерів у тексті"""
        text_lower = text.lower()
        count = 0
        
        for marker in markers:
            count += text_lower.count(marker)
        
        return count
    
    def _calculate_scream_factor(self, text):
        """Обчислення фактору крику"""
        if len(text) == 0:
            return 0
        
        uppercase = sum(1 for c in text if c.isupper())
        exclamation = text.count('!')
        
        scream_score = (uppercase / len(text) * 0.7) + (exclamation / len(text.split()) * 0.3)
        return round(min(scream_score, 1.0), 3)
    
    def _calculate_number_density(self, text):
        """Щільність чисел у тексті"""
        words = text.split()
        if not words:
            return 0
        
        number_words = sum(1 for word in words if any(char.isdigit() for char in word))
        return round(number_words / len(words), 3)
    
    def _calculate_influence_index(self, analysis):
        """Обчислення індексу впливу"""
        base_score = 10
        
        # Додаємо ваги
        base_score += analysis['chaos_index'] * 2
        base_score += analysis['scream_factor'] * 5
        base_score -= analysis['logic_inconsistency'] * 3
        base_score += analysis['noise_signal_ratio'] * 2
        
        return round(max(0, base_score), 2)
