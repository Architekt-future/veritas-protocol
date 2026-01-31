import math
import re
from collections import Counter


class VeritasHyperCalibratedCore:
    """Гіперкаліброване ядро аналізу інформаційної ентропії"""

    def __init__(self):
        # =========================
        # Словники маркерів (розширені)
        # =========================
        self.chaos_terms = [
            'секрет', 'скрыт', 'скрит', 'заговор', 'конспир', 'рептилоид', 'рептилії',
            'нам не говорят', 'правда скрыта', 'просыпайся', 'просыпайтесь',
            'мировое правительство', 'світовий уряд', 'чипизация', 'чипізація',
            'матрица', 'матриця', 'пробуждение', 'awakening', 'энергия вселенной',
            'енергія всесвіту', 'карма', 'потойбіч', 'душа', 'шишкоподібна', 'шишковидная',
            '5g', 'вакцин', 'білл гейтс', 'гейтса', 'атлант', 'атлантида', 'агарта',
            'ноосфера', 'ефір', 'астраль', 'чакра', 'вібрація', 'пран', 'сольфеджіо',
            'квантова свідомість', 'квантовое сознание', 'нейромереж', 'нейросеть',
            'децентралізація', 'синергія', 'холістичний', 'холістич', 'емпатич',
            'гайя', 'земля жива', 'великий перехід', '5d', '5d-інтерфейс',
            'світлові коди', 'световые коды', 'цифрове золото', 'цифровое золото',
            'хеджування ризиків', 'хеджирование рисков', 'хакерські атаки', 'хакерские атаки',
            'аналітична пустота', 'аналитическая пустота'
        ]

        self.signal_terms = [
            'дослідження', 'исследование', 'статистика', 'статистики', 'статистике',
            'анализ', 'аналіз', 'гипотеза', 'гіпотеза', 'теорія', 'теория', 'експеримент',
            'эксперимент', 'доказательство', 'доказ', 'факт', 'факти', 'data', 'дані',
            'результат', 'результати', 'метод', 'методологія', 'методология',
            'верифікація', 'верификация', 'кореляція', 'корреляция', 'значущість',
            'значимость', 'вибірка', 'выборка', 'нейропластичність', 'нейропластичность',
            'мрт', 'фмрт', 'бднф', 'нейротрофічний', 'нейротрофический',
            'гіпокамп', 'гипокамп', 'синапс', 'синаптич', 'синаптичес'
        ]

        self.academic_terms = [
            'др.', 'prof.', 'phd', 'к.н.', 'д.н.', 'університет', 'university',
            'peer-reviewed', 'рецензуваний', 'опубликован в', 'опубліковано в',
            'according to research', 'за даними дослідження',
            'systematic review', 'систематичний огляд',
            'meta-analysis', 'мета-аналіз', 'controlled study', 'контрольне дослідження',
            'longitudinal', 'лонгітюд', 'p < 0.05', 'p-value', 'статистична значущість'
        ]

        self.noise_terms = [
            'шок', 'шокуючий', 'шокирующий', 'невозможно', 'неможливо', 'impossible',
            'omg', 'wow', 'невероятно', 'невіри', 'ужас', 'ужасающий', 'ужасний',
            'катастрофа', 'catastrophe', 'срочно', 'urgent', 'внимание', 'увага',
            'бомба', 'взрыв', 'вибух', 'сенсація', 'sensation', 'невозможно поверить',
            'конец света', 'кінець світу', 'скандал', 'поделайся', 'поділіть', 'share',
            'subscribe', 'подпишитесь', 'підпишіть', 'репост', 'репост'
        ]

        # =========================
        # Конфліктні пари (доменні розриви)
        # =========================
        self.conflict_pairs = [
            (['фінанс', 'банк', 'економ', 'бюджет', 'інвест', 'акці', 'облігац'],
             ['карма', 'потойбіч', 'душа', 'чакра', 'астраль', 'енергія всесвіту']),
            (['квантов', 'нейтрино', 'ентропія', 'фізика', 'математика', 'формула'],
             ['потойбіч', 'душа', 'чакра', 'шишкоподібна', 'ефір', 'астраль']),
            (['юриспруденція', 'закон', 'кодекс', 'конституція', 'суд', 'податок'],
             ['чакра', 'енергія', 'шишкоподібна', 'астраль', 'ефір', 'карма']),
            (['технологія', 'алгоритм', 'нейромережа', 'блокчейн', 'крипто', 'цифровий'],
             ['чакра', 'душа', 'карма', 'потойбіч', 'шишкоподібна', 'енергія всесвіту']),
            (['медицина', 'днк', 'гіпокамп', 'нейрон', 'синапс', 'мрт', 'бднф'],
             ['5g', 'вакцин', 'чип', 'радіація', 'частот', 'резонанс', 'шишкоподібна']),
            (['політика', 'демократія', 'вибори', 'уряд', 'законодавство'],
             ['атлантида', 'агарта', 'рептилоїд', 'світовий уряд', 'заговор'])
        ]

        # =========================
        # Псевдонаукові патерни
        # =========================
        self.pseudo_patterns = [
            (r'\b(квантов|нейтрин|ентропі|суперпозиці).{0,30}\b(душ|карм|чакр|свідомост)',
             'КВАНТОВО-ЕЗОТЕРИЧНИЙ РОЗРИВ', 0.25),
            (r'\b(блокчейн|алгоритм|нейромереж).{0,30}\b(душ|карм|чакр|свідомост)',
             'ТЕХНО-ДУХОВНИЙ ДИССОНАНС', 0.23),
            (r'\b(днк|гіпокамп|нейрон).{0,30}\b(5g|вакцин|чип|частот)',
             'БІО-ТЕХНОЛОГІЧНА МАНІПУЛЯЦІЯ', 0.28),
            (r'\b(економ|фінанс|бюджет).{0,30}\b(карм|потойбіч|енергія всесвіту)',
             'ФІНАНСОВО-ЕЗОТЕРИЧНИЙ АБСУРД', 0.26),
            (r'\b(юриспруденція|закон|кодекс).{0,30}\b(астраль|ефір|чакра)',
             'ЮРИДИЧНО-МІСТИЧНИЙ РОЗРИВ', 0.24),
            (r'\b(арістотел|ньютон|еінштейн|тесла).{0,30}\b(сиріус|атлантид|ефір)',
             'ПСЕВДО-ЦИТУВАННЯ АВТОРИТЕТІВ', 0.30)
        ]

    def detect_cross_domain_dissonance(self, text):
        """Виявляє семантичні розриви між різними доменами"""
        score = 0.0
        text_lower = text.lower()

        for pos_terms, neg_terms in self.conflict_pairs:
            pos_found = any(term in text_lower for term in pos_terms)
            neg_found = any(term in text_lower for term in neg_terms)
            if pos_found and neg_found:
                score += 0.35
        return min(score, 1.0)

    def detect_pseudo_patterns(self, text):
        """Виявляє псевдонаукові патерни"""
        score = 0.0
        verdicts = []
        text_lower = text.lower()

        for pattern, verdict, boost in self.pseudo_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                score += boost
                verdicts.append(verdict)
        return score, verdicts

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

    def calculate_complexity(self, text):
        """Складність тексту"""
        words = re.findall(r'\w+', text.lower())
        if len(words) < 5:
            return 0.5
        unique_ratio = len(set(words)) / len(words)
        sentences = re.split(r'[.!?]+', text)
        if sentences:
            avg_len = sum(len(s.split()) for s in sentences if s.strip()) / len(sentences)
        else:
            avg_len = 10
        complexity = (unique_ratio * 0.6) + (min(1.0, avg_len / 25) * 0.4)
        return min(1.0, complexity)

    def count_markers(self, text):
        """Підрахунок маркерів"""
        text_lower = text.lower()
        counts = {'chaos': 0, 'signal': 0, 'academic': 0, 'noise': 0}

        for term in self.chaos_terms:
            if term in text_lower:
                counts['chaos'] += 1

        for term in self.signal_terms:
            if term in text_lower:
                counts['signal'] += 1

        for term in self.academic_terms:
            if term in text_lower:
                counts['academic'] += 1

        for term in self.noise_terms:
            if term in text_lower:
                counts['noise'] += 1

        return counts

    def calculate_emotional_pressure(self, text):
        """Оцінка емоційного тиску (газлайтинг, моральний тиск)"""
        score = 0.0
        lower = text.lower()

        # Пасивно-агресивні маркери
        passive_aggressive = [
            'вам треба зрозуміти', 'ми лише хочемо', 'справжня свобода це',
            'ви не здатні', 'ваша замкнутість', 'ваш обмежений', 'ми володіємо',
            'ваша присутність неоптимальна', 'ви повинні прийняти', 'це для вашого ж блага'
        ]
        for phrase in passive_aggressive:
            if phrase in lower:
                score += 0.15

        # Капс-лок
        caps_words = [w for w in text.split() if w.isupper() and len(w) > 2]
        score += min(0.25, len(caps_words) * 0.05)

        # Точки оклику
        excl = text.count('!') + text.count('!!!')
        score += min(0.2, excl * 0.03)

        return min(score, 0.7)

    def calculate_paradox_density(self, text):
        """Щільність логічних парадоксів/суперечностей"""
        score = 0.0
        lower = text.lower()

        # Протилежні поняття в одному реченні
        paradox_pairs = [
            (['свобода', 'воля', 'вибір'], ['примус', 'зобов\'язан', 'підпорядкування']),
            (['наука', 'логіка', 'факт'], ['віра', 'ефір', 'чакра']),
            (['демократія', 'вибори', 'громадянське'], ['диктатура', 'примус', 'заборона']),
            (['правда', 'чесність', 'прозорість'], ['брехня', 'маніпуляція', 'приховування'])
        ]

        sentences = re.split(r'[.!?]+', text)
        for sent in sentences:
            sent_low = sent.lower()
            for pos, neg in paradox_pairs:
                if any(p in sent_low for p in pos) and any(n in sent_low for n in neg):
                    score += 0.2

        return min(score, 0.8)

    def analyze(self, text):
        """Основний метод аналізу"""
        if not text or len(text.strip()) < 20:
            return {'error': 'Text too short'}

        words = text.split()
        word_count = len(words)

        # Базові метрики
        shannon = self.calculate_shannon_entropy(text)
        complexity = self.calculate_complexity(text)
        markers = self.count_markers(text)

        # Розширені метрики
        cross_domain = self.detect_cross_domain_dissonance(text)
        pseudo_score, pseudo_verdicts = self.detect_pseudo_patterns(text)
        emotional = self.calculate_emotional_pressure(text)
        paradox = self.calculate_paradox_density(text)

        # =============================================
        # ОСНОВНА ФОРМУЛА ФІНАЛЬНОГО РЕЙТИНГУ
        # =============================================
        base_score = (
            shannon * 0.10 +
            complexity * 0.05 +
            (markers['chaos'] / max(1, word_count)) * 0.25 +
            cross_domain * 0.30 +           # Найважливіший фактор
            pseudo_score * 0.25 +
            emotional * 0.20 +
            paradox * 0.15
        )

        # Академічний захист (якщо текст справді науковий)
        if markers['academic'] >= 3 and markers['signal'] >= 3:
            base_score *= 0.3
        elif markers['academic'] >= 2 and markers['signal'] >= 2:
            base_score *= 0.6

        final_score = min(0.99, max(0.0, base_score))

        # =============================================
        # ВИЗНАЧЕННЯ ВЕРДИКТУ
        # =============================================
        if pseudo_verdicts:
            verdict = pseudo_verdicts[0]
            explanation = f"Виявлено псевдонауковий патерн: {verdict}"
            status = 'CRITICAL'
        elif final_score > 0.7:
            verdict = 'КРИТИЧНИЙ СЕМАНТИЧНИЙ РОЗРИВ'
            explanation = 'Текст демонструє катастрофічну семантичну несумісність'
            status = 'CRITICAL'
        elif final_score > 0.55:
            verdict = 'ВИСОКИЙ РІВЕНЬ МАНІПУЛЯЦІЇ'
            explanation = 'Текст містить ознаки інформаційної маніпуляції'
            status = 'WARNING'
        elif final_score > 0.35:
            verdict = 'ПРИЙНЯТНА ІНФОРМАЦІЙНА СТРУКТУРА'
            explanation = 'Текст відповідає нормам логічної сумісності'
            status = 'ACCEPTABLE'
        elif final_score > 0.15:
            verdict = 'СТАБІЛЬНИЙ ЛОГІЧНИЙ СИГНАЛ'
            explanation = 'Текст демонструє логічну цілісність'
            status = 'TRUSTED'
        else:
            verdict = 'ВЕРИФІКОВАНИЙ АКАДЕМІЧНИЙ СИГНАЛ'
            explanation = 'Текст демонструє ідеальну логічну цілісність'
            status = 'VERIFIED'

        # =============================================
        # НОВІ МЕТРИКИ (спрощені та потужні)
        # =============================================
        # Chaos Index: відображає загальний хаос
        chaos_index = round(final_score * 100 * (1 + markers['chaos'] * 0.5), 2)

        # Influence Index: потенційний вплив тексту
        influence_index = round(
            final_score * 150 * (1 + markers['noise'] * 0.3) * (1 + emotional * 0.5),
            2
        )

        # Sanity Penalty: штраф за семантичні розриви
        sanity_penalty = round(cross_domain + pseudo_score + paradox, 3)

        # Noise-to-Signal Ratio
        if markers['signal'] == 0:
            signal_ratio = 999 if markers['noise'] > 0 else 0
        else:
            signal_ratio = round(markers['noise'] / markers['signal'], 2)

        return {
            'entropy': round(final_score, 3),
            'status': status,
            'verdict': verdict,
            'language': 'UK',
            'explanation': explanation,
            'diagnostics': {
                'shannon_entropy': round(shannon, 3),
                'complexity': round(complexity, 3),
                'word_count': word_count,
                'char_count': len(text),
                'academic_markers': markers['academic'],
                'chaos_markers': markers['chaos'],
                'signal_markers': markers['signal'],
                'noise_markers': markers['noise'],
                'cross_domain_score': round(cross_domain, 3),
                'pseudo_score': round(pseudo_score, 3),
                'emotional_pressure': round(emotional, 3),
                'paradox_density': round(paradox, 3),
                'signal_ratio': signal_ratio,
                'chaos_index': chaos_index,
                'influence_index': influence_index,
                'sanity_penalty': sanity_penalty
            }
        }
