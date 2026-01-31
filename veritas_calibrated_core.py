import math
import re


class VeritasCalibratedCore:
    """Калібрований аналізатор інформаційної ентропії"""

    def __init__(self):
        # Конспірологічні та маніпулятивні маркери
        self.chaos_terms = [
            'секрет', 'скрыто', 'скрыта', 'скрыть',
            'заговор', 'конспіращ', 'конспіратор',
            'нам не говорят', 'нам не говорити',
            'правда скрыта', 'правда скрита',
            'просыпайся', 'просыпайтесь',
            'они не хотят', 'вони не хочуть',
            'все врут', 'всі брешуть',
            'мировое правительство', 'світове уряд',
            'репти', 'рептилian',
            'чипизация', 'чипізація',
            'нанотехнология',
            'третий глаз', 'третій око',
            'энергия вселенной', 'енергія вселенної',
            'матрица', 'матриця',
            'пробуждение', 'awakening',
            'истинная реальность', 'справжня реальність',
            'скрытая правда', 'прихована правда',
            'элиты', 'еліти',
            'банк', 'банки',
            'карма', 'потойбіч', 'душа'
        ]

        # Сигнальні (академічні/факт) маркери
        self.signal_terms = [
            'дослідження', 'исследование', 'исследования',
            'ученый', 'ученые', 'дослідник', 'дослідники',
            'опубликован', 'опубликовано', 'опубліковано',
            'журнал', 'journal',
            'university', 'університет', 'университет',
            'статистика', 'статистики', 'статистике',
            'аналіз', 'анализ',
            'гипотеза', 'гипотезу', 'гипотезы', 'гипотезі',
            'теория', 'теории', 'теорія',
            'эксперимент', 'эксперименту', 'експеримент',
            'доказательство', 'доказательства', 'доказ',
            'факт', 'факти', 'факта',
            'данные', 'дані', 'data',
            'результат', 'результати',
            'метод', 'методология', 'методальн'
        ]

        # Академічні маркери (посилюють сигнал)
        self.academic_terms = [
            'Dr.', 'Prof.', 'PhD', 'к.н.', 'д.н.',
            'university', 'університет',
            'peer-reviewed', 'рецензуваний',
            'published in', 'опубликован в',
            'according to research', 'за даними дослідження',
            'systematic review', 'систематичний огляд',
            'meta-analysis', 'мета-аналіз',
            'controlled study', 'контрольне дослідження'
        ]

        # Маркери інформаційного шуму (емоційні крики, сенсаційність)
        self.noise_terms = [
            'шок', 'шокуючий', 'шокирующий',
            'невозможно', 'неможливо', 'impossible',
            'OMG', 'WOW', 'НЕВЕРЯТНО', 'Нimpressed',
            'ужас', 'ужасающий', 'ужасний', 'ужасный',
            'катастрофа', 'катастрофу', 'disaster',
            'СРОЧНО', 'срочно', 'URGENT',
            'ВНИМАНИЕ', 'УВАГА', 'ATTENTION',
            'бомба', 'взрыв', 'вибух',
            'сенсация', 'сенсації', 'sensation',
            'невозможно поверить', 'неможливо поверити',
            'всё кончилось', 'всё кончится',
            'конец света', 'кінець світу',
            'скандал', 'скандалу'
        ]

        # Конспірологічні паттерни (складні)
        self.conspiracy_patterns = [
            {
                'pattern': r'(они|вони|мировое правительство|елити).{0,30}(скрыт|скрит|не хот|не вкаж)',
                'verdict': 'КОНСПІРОЛОГІЧНА НАРРАТИВА',
                'explanation': 'Текст використовує класичну конспірологічну схему "вони скрывают"',
                'score_boost': 0.18
            },
            {
                'pattern': r'(просыпайся|просыпайтесь|пробуждение|пробудження).{0,20}(правда|реальн|истин)',
                'verdict': 'ІНФО-МАНІПУЛЯЦІЯ: ЛОЖНА ПРОСВІТЛЕННЯ',
                'explanation': 'Текст використовує техніку ложного "пробуждения" для маніпуляції',
                'score_boost': 0.20
            },
            {
                'pattern': r'(энергия|енергія|вибрація|вибрация).{0,25}(вселенн|космос|cosmic|универс)',
                'verdict': 'ІНФО-МАНІПУЛЯЦІЯ: ПСЕВДОНАУКА',
                'explanation': 'Текст смішує научні терміни з псевдонауковими концепціями',
                'score_boost': 0.15
            },
            {
                'pattern': r'(третий глаз|третій око|пинеальна|пинеальная).{0,20}(открыть|відкрити|активаци|пробud)',
                'verdict': 'ІНФО-МАНІПУЛЯЦІЯ: ПСЕВДОДУХОВНА ПРАКТИКА',
                'explanation': 'Текст просуть сумнівні "ররхідні" практики',
                'score_boost': 0.17
            },
            {
                'pattern': r'(рептилианы|рептилії|мировая элита|світова еліта).{0,30}(контроль|управл|програм)',
                'verdict': 'КОНСПІРОЛОГІЧНА НАРРАТИВА: ЕЛІТАРНИЙ КОНТРОЛЬ',
                'explanation': 'Текст просуть конспірологічну теорію про таємний контроль еліти',
                'score_boost': 0.22
            }
        ]

    def detect_patterns(self, text):
        """Шукає конспірологічні паттерни в тексті"""
        detected = []
        text_lower = text.lower()

        for p in self.conspiracy_patterns:
            if re.search(p['pattern'], text_lower):
                detected.append({
                    'verdict': p['verdict'],
                    'explanation': p['explanation'],
                    'score_boost': p['score_boost']
                })

        return detected

    def count_terms(self, text):
        """Рахує маркери різних категорій"""
        text_lower = text.lower()
        counts = {
            'chaos': 0,
            'signal': 0,
            'academic': 0,
            'noise': 0
        }

        for term in self.chaos_terms:
            if term.lower() in text_lower:
                counts['chaos'] += 1

        for term in self.signal_terms:
            if term.lower() in text_lower:
                counts['signal'] += 1

        for term in self.academic_terms:
            if term.lower() in text_lower:
                counts['academic'] += 1

        for term in self.noise_terms:
            if term.lower() in text_lower:
                counts['noise'] += 1

        return counts

    def calculate_gradient_penalties(self, base_metrics):
        """Штраф за резкі зміни — нехарактерні для нормального тексту"""
        penalty = 0.0

        chaos_ratio = base_metrics['chaos_markers'] / max(1, base_metrics['word_count'])
        signal_ratio = base_metrics['signal_markers'] / max(1, base_metrics['word_count'])

        # Аномалійна концентрація хаосу
        if chaos_ratio > 0.08:
            penalty += min(0.4, chaos_ratio * 3.5)

        # Дисбаланс між хаосом і сигналом
        if base_metrics['chaos_markers'] > 2 and base_metrics['signal_markers'] == 0:
            penalty += 0.25

        # Entrophy vs complexity mismatch
        entropy_diff = abs(base_metrics['shannon_entropy'] - base_metrics['complexity'])
        if entropy_diff > 0.35:
            penalty += entropy_diff * 0.3

        return min(penalty, 0.7)

    def calculate_conflict_penalty(self, text):
        """Штраф за внутрішні суперечності"""
        text_lower = text.lower()
        score = 0.0

        # Протилежні заява одночасно
        conflict_pairs = [
            (['факт', 'доказан', 'доказано', 'факти', 'доведено'],
             ['заговор', 'скрыт', 'скрита', 'не говорят', 'не говорити']),
            (['университет', 'університет', 'исследование', 'дослідження'],
             ['нам не говорят', 'они скрывают', 'правда скрыта', 'прихована правда']),
            (['научно', 'научный', 'науковий', 'емпірічний'],
             ['энергия вселенной', 'третий глаз', 'энергетический', 'енергетичний'])
        ]

        for positive, negative in conflict_pairs:
            has_pos = any(w in text_lower for w in positive)
            has_neg = any(w in text_lower for w in negative)
            if has_pos and has_neg:
                score += 0.35

        # Мікс комунікативних стилів: науковий + духовний
        has_scientific = any(word in text_lower for word in ['исследование', 'дослідження', 'гипотеза', 'гипотезі', 'эксперимент'])
        has_spiritual = any(word in text_lower for word in ['карма', 'потойбіч', 'душа'])
        if has_scientific and has_spiritual:
            score += 0.45

        return min(score, 0.7)

    def calculate_contextual_score(self, text, term_counts, base_metrics):
        """Контекстуальна оцінка — насколько suspicious контекст"""
        text_lower = text.lower()
        score = 0.0

        # Емоційні амплифікатори
        emotional_amplifiers = ['!!!!', '!!!', 'СРОЧНО', 'ВНИМАНИЕ', 'УВАГА', 'срочно', 'не можете поверити']
        for amp in emotional_amplifiers:
            if amp in text or amp.lower() in text_lower:
                score += 0.12

        # Інфо-шум маркери
        if term_counts.get('noise', 0) > 0:
            score += min(0.25, term_counts['noise'] * 0.08)

        # Caps-lock аспект
        words = text.split()
        caps_words = [w for w in words if w.isupper() and len(w) > 2]
        if len(caps_words) > 2:
            score += min(0.2, len(caps_words) * 0.06)

        # Вересень слів "виклик" / "пробуджень"
        call_to_action = ['поделайся', 'поделайтесь', 'поділіть', 'share', 'subscribe', 'подпишитесь', 'підпишіть']
        for cta in call_to_action:
            if cta in text_lower:
                score += 0.1

        return min(score, 0.7)

    def analyze(self, text):
        """Основний метод аналізу"""
        if not text or len(text.strip()) < 20:
            return {'error': 'Text too short'}

        words = text.split()
        word_count = len(words)

        # Базові метрики
        detected_patterns = self.detect_patterns(text)
        term_counts = self.count_terms(text)
        shannon_entropy = self._calculate_shannon_entropy(text)
        complexity = self._calculate_complexity(text)

        # Метрики для градієнтів
        base_metrics = {
            'shannon_entropy': shannon_entropy,
            'complexity': complexity,
            'signal_markers': term_counts['signal'],
            'chaos_markers': term_counts['chaos'],
            'academic_markers': term_counts['academic'],
            'word_count': word_count
        }

        # Розширені метрики
        gradient_penalty = self.calculate_gradient_penalties(base_metrics)
        conflict_penalty = self.calculate_conflict_penalty(text)
        contextual_score = self.calculate_contextual_score(text, term_counts, base_metrics)

        # БАЗОВА ОЦІНКА (тонко налаштована)
        base_score = (
            shannon_entropy * 0.12 +          # Знижено вагу
            complexity * 0.08 +               # Знижено вагу
            (term_counts['chaos'] / max(1, word_count)) * 0.20 +
            contextual_score * 0.25 +         # Основна вага
            gradient_penalty * 0.20 +
            conflict_penalty * 0.15
        )

        # Штрафи за паттерни (помірковані)
        for pattern in detected_patterns:
            base_score += pattern['score_boost']

        # АКАДЕМІЧНИЙ ЗАХИСТ (тонкий градієнт)
        if term_counts['academic'] >= 2 and term_counts['signal'] >= 2:
            if term_counts['chaos'] == 0:
                base_score *= 0.3  # Чиста наука
            elif term_counts['chaos'] <= 1:
                base_score *= 0.5  # Мінімальний хаос
            else:
                base_score *= 0.7  # Багато хаосу
        elif term_counts['academic'] >= 1 and term_counts['signal'] >= 1:
            base_score *= 0.8

        # Гарантовані мінімуми для критичних випадків
        if conflict_penalty > 0.35:
            base_score = max(base_score, 0.65)
        if contextual_score > 0.4:
            base_score = max(base_score, 0.6)

        final_score = min(0.99, max(0.0, base_score))

        # ВЕРДИКТ з плавними переходами
        if detected_patterns:
            main_pattern = detected_patterns[0]
            status = 'CRITICAL' if final_score > 0.6 else 'WARNING'
            verdict = main_pattern['verdict']
            explanation = main_pattern['explanation']
        elif final_score > 0.7:
            status = 'CRITICAL'
            if contextual_score > 0.4:
                verdict = 'ВИСОКИЙ РІВЕНЬ СЕМАНТИЧНОГО ХАОСУ'
                explanation = 'Текст демонструє критичний рівень семантичної несумісності'
            else:
                verdict = 'СЕМАНТИЧНА ПУСТОТА'
                explanation = 'Високий рівень абстракції при відсутності конкретного змісту'
        elif final_score > 0.55:
            status = 'WARNING'
            verdict = 'ПІДОЗРІЛУ СЕМАНТИЧНА СТРУКТУРА'
            explanation = 'Текст містить ознаки семантичних несумісностей'
        elif final_score > 0.35:
            status = 'ACCEPTABLE'
            verdict = 'ПРИЙНЯТНА СТРУКТУРА ІНФОРМАЦІЇ'
            explanation = 'Текст відповідає нормам логічної сумісності'
        elif final_score > 0.15:
            status = 'TRUSTED'
            verdict = 'СТАБІЛЬНИЙ ЛОГІЧНИЙ СИГНАЛ'
            explanation = 'Текст демонструєমযку логічну цілісність'
        else:
            status = 'VERIFIED'
            verdict = 'ВЕРИФІКОВАНИЙ АКАДЕМІЧНИЙ СИГНАЛ'
            explanation = 'Текст демонструє іdeальну логічну цілісність'

        # Додаємо детальні пояснення
        detail_explanations = []
        if gradient_penalty > 0.1:
            detail_explanations.append(f"Градієнтний штраф: {gradient_penalty:.2f}")
        if conflict_penalty > 0.1:
            detail_explanations.append(f"Конфліктний штраф: {conflict_penalty:.2f}")
        if contextual_score > 0.2:
            detail_explanations.append(f"Контекстуальна оцінка: {contextual_score:.2f}")

        if detail_explanations:
            explanation += " | " + " + ".join(detail_explanations)

        # ============================================================
        # НОВІ МЕТРИКИ: chaos_index, influence_index, sanity_penalty
        # ============================================================
        signal = term_counts['signal']
        chaos = term_counts['chaos']
        context = contextual_score
        conflict = conflict_penalty
        final = final_score

        # --- chaos_index ---
        # Показує насколько текст "хаотичний" в інформаційному смислі
        # Чиста наука (signal>=2, chaos=0) -> 0
        # Інакше: скейлінг від final_score з урахуванням хаосу та контексту
        if signal >= 2 and chaos == 0:
            chaos_index = 0.0
        elif chaos > 0:
            # Хаос присутній — conflict і context вже "включені" в хаос-контекст
            chaos_index = final * 100 * (1 + chaos * 0.6) * (1 + max(0, context - 0.3) * 1.96) / (1 + signal * 0.8)
        else:
            # Хаосу нет, але текст не "чиста наука" — conflict і context діять як discount
            chaos_index = final * 100 * (1 - conflict * 0.8) * (1 - context * 0.46) / (1 + signal * 1.0)
        chaos_index = round(chaos_index, 2)

        # --- influence_index ---
        # Агрегат "насколько цей текст може впливати"
        # Для чиста науки: просто final * words * (1 + final) — влияние через інформативність
        # Для інших: додаємо chaos_index і скейл від signal
        if signal >= 2 and chaos == 0:
            influence_index = final * word_count * (1 + final)
        elif signal == 0:
            influence_index = final * 100 * (1 + final) + chaos_index
        else:
            score_part = final * 100 * (1 + final) / (1 + signal * 0.35)
            ci_part = chaos_index / (1 + signal * 0.2)
            influence_index = score_part + ci_part
        influence_index = round(influence_index, 2)

        # --- sanity_penalty ---
        # Штраф за логічну несумісність:
        # combined conflict + gradient, але gradient влияє лише якщо > 0.3
        # (тобто "гладко оформлений шахрай" з низьким gradient НЕ штрафується)
        sanity_penalty = round(conflict_penalty + max(0, gradient_penalty - 0.3), 3)

        # --- noise_markers ---
        # ФІКС: раніше була копія chaos_markers. Тепер окремий рахунок емоційних слів.
        noise_marker_count = term_counts['noise']

        # --- signal_ratio ---
        # ФІКС: раніше signal/chaos (з 999 при chaos=0). Тепер noise/signal.
        # Показує відношення шуму до сигналу. 0 коли шуму нет.
        if noise_marker_count == 0:
            signal_ratio = 0
        else:
            signal_ratio = round(noise_marker_count / max(1, signal), 2)

        return {
            'entropy': round(final_score, 3),
            'status': status,
            'verdict': verdict,
            'language': 'UK',
            'explanation': explanation,
            'diagnostics': {
                'shannon_entropy': round(shannon_entropy, 3),
                'complexity': round(complexity, 3),
                'contextual_score': round(contextual_score, 3),
                'gradient_penalty': round(gradient_penalty, 3),
                'conflict_penalty': round(conflict_penalty, 3),
                'word_count': word_count,
                'char_count': len(text),
                'academic_markers': term_counts['academic'],
                'chaos_markers': term_counts['chaos'],
                'signal_markers': term_counts['signal'],
                'noise_markers': noise_marker_count,
                'pattern_count': len(detected_patterns),
                'shout_factor': len([w for w in words if w.isupper() and len(w) > 2]) / max(1, word_count),
                'number_density': len(re.findall(r'\d+', text)) / max(1, word_count),
                'signal_ratio': signal_ratio,
                'chaos_index': chaos_index,
                'influence_index': influence_index,
                'sanity_penalty': sanity_penalty
            }
        }

    def _calculate_shannon_entropy(self, text):
        """Обчислює ентропію Шеннона"""
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

    def _calculate_complexity(self, text):
        """Обчислює складність тексту"""
        words = re.findall(r'\w+', text.lower())
        if len(words) < 10:
            return 0.5

        unique_ratio = len(set(words)) / len(words)

        sentences = re.split(r'[.!?]+', text)
        if sentences:
            avg_sentence_length = sum(len(s.split()) for s in sentences if s.strip()) / len(sentences)
        else:
            avg_sentence_length = 10

        complexity = (unique_ratio * 0.6) + (min(1.0, avg_sentence_length / 25) * 0.4)
        return min(1.0, complexity)
