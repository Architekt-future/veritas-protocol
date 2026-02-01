"""
Veritas Protocol - Semantic Void Detector v11.4
Synth: v11.3 ultra-simple architecture + keyphrase fast-path + absurdity_keywords fallback
"""

import re
import math


class VeritasCalibratedCore:
    """ULTRA SIMPLE — PROTECTS SCIENCE, DESTROYS ABSURDITY"""

    def __init__(self):
        # ============================================================
        # КРИТИЧНІ АБСУРД-ПАТТЕРНИ (regex + вага)
        # ============================================================
        self.critical_absurdity = [
            # Наука + Їжа
            (r'квантов(ий|а|е|і|ого|ої|ому|ій).*?(борщ|суп|їжа|сметана|картопля|буряк|каструля)', 1.0),
            (r'(ентропія|термодинаміка|фізика).*?(борщ|суп|їжа|рецепт|кухня)', 0.9),

            # Біологія + Техно-параноя
            (r'(днк|генетичний|імунітет|вакцина).*?(5g|чип|супутник|частота|гц|радіо)', 0.9),
            (r'(нейрон|мозок|синапс).*?(програмування|контроль|зомбування)', 0.85),

            # Бізнес + Езотерика
            (r'(бізнес|ринок|менеджмент|стратегія).*?(чакра|аура|енергія|вібрація|карма)', 1.0),
            (r'(квантовий|квантова).*?(маркетинг|бізнес|продажі|лідерство)', 0.95),
            (r'(холістичний|синергетичний).*?(маркетинг|менеджмент|розвиток)', 0.8),

            # Цифровий містицизм
            (r'(блокчейн|AI|штучний інтелект|алгоритм).*?(душа|свідомість|карма|просвітлення)', 0.9),
            (r'(NFT|метаверс|Web3).*?(енергія|чакра|астрал)', 0.95),

            # Істерія (точні caps-фрагменти)
            (r'(НЕГАЙНО|ЗРАДА|ГАНЬБА|СКАНДАЛ|КАТАСТРОФА).*?(правда|істина|факт)', 0.95),
            (r'ви не готові|ви не знаєте|ви не розумієте.*?(правда|реальність)', 0.85),
            (r'(СРОЧНО|УВАГА|ВНИМАНИЕ).*?(катастрофа|кінець|загибель)', 0.9),

            # Псевдонауковий бред
            (r'(нанодискретизація|супутникові масиви низької орбіти)', 0.8),
            (r'(квантова суперпозиція нейронів|пост-біологічне суспільство)', 0.9),
            (r'(чакри|вібраційний фон|ефірний кокон|провідники прани)', 0.85),
            (r'(мета-фізичні протоколи|квантове вирівнювання аури)', 1.0),
            (r'(світловий вузол у глобальній матриці|езотеричні цикли)', 0.95),
        ]

        # ============================================================
        # ЗАХИСТ НАУКИ — regex-паттерни для коротких фраз
        # ============================================================
        self.science_protection = [
            r'другий закон термодинаміки',
            r'ентропія.*?(зростання|зменшуватися|не може)',
            r'ізольована система',
            r'теплова смерть.*?всесвіту',
            r'статистична фізика',
            r'згідно з.*?дослідженням',
            r'результати.*?показують',
            r'статистично значущий',
            r'p.*?value.*?<.*?\d',
            r'коефіцієнт кореляції',
        ]

        # FAST-PATH: точні фрази — якщо є хоча б одна, science guard срацює
        # без дальніх перевірок (з патча)
        self.science_keyphrases = [
            'другий закон термодинаміки',
            'ентропія не може зменшуватися',
            'ізольована система',
            'теплова смерть всесвіту',
            'статистична фізика',
            'найбільш імовірний розподіл',
            'мікростанів системи',
        ]

        # ============================================================
        # НАУКОВІ ФОРМУЛИ (символи — fast-check)
        # ============================================================
        self.science_formulas = [
            '=', '≠', '≈', '~', '→', '⇒', '∈', '∑', '∫', '∂',
            '∆', 'π', '∞', '√', '≡', 'α', 'β', 'γ', 'δ'
        ]

        # ============================================================
        # НАУКОВІ ТЕРМІНИ (для подсчёта)
        # ============================================================
        self.science_terms = [
            'термодинаміка', 'ентропія', 'енергія', 'фізика', 'математика',
            'статистичний', 'кореляція', 'регресія', 'вибірка', 'гіпотеза',
            'теорія', 'експеримент', 'дослідження', 'аналіз', 'методологія',
            'верифікація', 'валідація', 'реплікація', 'контрольна група'
        ]

        # ============================================================
        # СЛОВА-ВИНІВКИ (з патча): якщо є хоча б одно — текст НЕ наука,
        # і автоматично кандидат на absurd fallback
        # ============================================================
        self.absurdity_keywords = [
            'чакра', 'аура', 'карма', 'енергетичний', 'вібраційний',
            'рептилоїд', 'ілюмінат', 'масон', 'змова',
            'нанодискретизація', 'пост-біологічний', 'мета-фізичний',
            'холістичний', 'синергетичний', 'езотеричний'
        ]

    # ----------------------------------------------------------
    # MAIN ENTRY
    # ----------------------------------------------------------
    def analyze(self, text):
        """
        Логіка (порядок important!):
          1. Science fast-path (keyphrases)  →  VERIFIED сразу
          2. Science full-check (_is_pure_science)  →  VERIFIED
          3. Absurd regex scan  →  score
          4. Absurdity_keywords fallback  →  score (якщо regex не палив)
          5. Hysteria  →  score
          6. Pseudo-intellectual  →  score
          7. Verdict
        """
        if not text or len(text.strip()) < 20:
            return {'error': 'Text too short'}

        text_lower = text.lower()
        words = text.split()
        word_count = len(words)

        # ---- КРОК 1: SCIENCE FAST-PATH ----
        # Якщо текст містить точну science-фразу — сразу VERIFIED,
        # без дальніх regex-сканів
        for phrase in self.science_keyphrases:
            if phrase.lower() in text_lower:
                return self._create_science_result(text, word_count)

        # ---- КРОК 2: SCIENCE FULL CHECK ----
        if self._is_pure_science(text):
            return self._create_science_result(text, word_count)

        # ---- КРОК 3: ABSURD REGEX SCAN ----
        absurd_score = 0.0
        absurd_details = []

        for pattern, weight in self.critical_absurdity:
            if re.search(pattern, text_lower, re.IGNORECASE):
                absurd_score = max(absurd_score, weight)
                absurd_details.append(pattern[:35] + '…')

        # ---- КРОК 4: ABSURDITY KEYWORDS FALLBACK ----
        # Якщо regex не палив, але є слова-винівки — мінімальна оцінка 0.7
        if absurd_score == 0.0:
            found_keywords = [kw for kw in self.absurdity_keywords if kw in text_lower]
            if found_keywords:
                absurd_score = 0.7
                absurd_details.append(f"keywords: {', '.join(found_keywords[:3])}")

        # ---- КРОК 5: HYSTERIA ----
        hysteria_score = self._calculate_hysteria(text)
        if hysteria_score > 0.5:
            absurd_score = max(absurd_score, 0.7 + hysteria_score * 0.3)
            absurd_details.append('Істерія')

        # ---- КРОК 6: PSEUDO-INTELLECTUAL ----
        pseudo_score = self._calculate_pseudo_intellectual(text)
        if pseudo_score > 0.6:
            absurd_score = max(absurd_score, pseudo_score)
            absurd_details.append('Псевдоінтелект')

        # ---- КРОК 7: FINAL SCORE ----
        final_score = min(0.99, absurd_score * 1.1) if absurd_score > 0.7 else absurd_score
        # Якщо вообще ничего не найдено — тихий текст
        if final_score == 0.0:
            final_score = 0.05 if len(text) < 100 else 0.03

        # ---- КРОК 8: ІНДЕКСИ ----
        chaos_index   = round(final_score * 100 * (1 + len(absurd_details) * 0.5), 2)
        influence_index = round(final_score * 100 * (1 + hysteria_score * 0.8), 2)
        sanity_penalty  = round(absurd_score + hysteria_score * 0.5, 3)

        # ---- КРОК 9: ВЕРДИКТ ----
        if final_score > 0.8:
            status, verdict = 'CRITICAL', 'АБСОЛЮТНИЙ АБСУРД'
            explanation = 'Текст містить критичні логічні порушення'
        elif final_score > 0.6:
            status, verdict = 'CRITICAL', 'ВИСОКИЙ РІВЕНЬ АБСУРДУ'
            explanation = 'Текст демонструє значні семантичні несумісності'
        elif final_score > 0.4:
            status, verdict = 'WARNING', 'ПІДОЗРІЛИЙ ДИСКУРС'
            explanation = 'Текст містить ознаки логічних несумісностей'
        elif final_score > 0.2:
            status, verdict = 'ACCEPTABLE', 'ПРИЙНЯТНА ІНФОРМАЦІЯ'
            explanation = 'Текст відповідає нормам логічної сумісності'
        elif final_score > 0.05:
            status, verdict = 'TRUSTED', 'СТАБІЛЬНИЙ СИГНАЛ'
            explanation = 'Текст демонструє логічну цілісність'
        else:
            status, verdict = 'VERIFIED', 'ВЕРИФІКОВАНИЙ КОНТЕНТ'
            explanation = 'Текст демонструє ідеальну логічну цілісність'

        if absurd_details:
            explanation += ' | Абсурд: ' + ', '.join(absurd_details[:3])
        if hysteria_score > 0.3:
            explanation += f' | Істерія: {hysteria_score:.1f}'

        return {
            'entropy': round(final_score, 3),
            'status': status,
            'verdict': verdict,
            'language': 'UK',
            'explanation': explanation,
            'diagnostics': {
                'absurd_score':    round(absurd_score, 3),
                'hysteria_score':  round(hysteria_score, 3),
                'pseudo_score':    round(pseudo_score, 3),
                'word_count':      word_count,
                'char_count':      len(text),
                'chaos_index':     chaos_index,
                'influence_index': influence_index,
                'sanity_penalty':  sanity_penalty,
                'is_science':      False,
                'absurd_patterns': len(absurd_details)
            }
        }

    # ----------------------------------------------------------
    # SCIENCE GUARD
    # ----------------------------------------------------------
    def _is_pure_science(self, text):
        """
        Full science check (fallback після fast-path).
        Повертає True якщо:
          - є формула або 3+ science_terms
          - є хоча б один science_protection pattern
          - НЕ має absurd regex
          - hysteria < 0.3
        """
        text_lower = text.lower()

        has_formula = any(f in text for f in self.science_formulas)
        sci_count   = sum(1 for t in self.science_terms if t in text_lower)

        if not has_formula and sci_count < 3:
            return False

        has_protection = any(
            re.search(p, text_lower, re.IGNORECASE)
            for p in self.science_protection
        )

        has_absurd = any(
            re.search(p, text_lower, re.IGNORECASE)
            for p, _ in self.critical_absurdity
        )

        hysteria = self._calculate_hysteria(text)

        return (has_protection or (has_formula and sci_count >= 3)) \
               and not has_absurd \
               and hysteria < 0.3

    # ----------------------------------------------------------
    # SCIENCE RESULT BUILDER
    # ----------------------------------------------------------
    def _create_science_result(self, text, word_count):
        return {
            'entropy': 0.05,
            'status': 'VERIFIED',
            'verdict': 'НАУКОВИЙ СТАНДАРТ',
            'language': 'UK',
            'explanation': 'Текст демонструє наукову цілісність без ознак абсурду',
            'diagnostics': {
                'absurd_score':    0.0,
                'hysteria_score':  0.0,
                'pseudo_score':    0.0,
                'word_count':      word_count,
                'char_count':      len(text),
                'chaos_index':     0.0,
                'influence_index': 5.25,
                'sanity_penalty':  0.0,
                'is_science':      True,
                'absurd_patterns': 0
            }
        }

    # ----------------------------------------------------------
    # HYSTERIA DETECTOR
    # ----------------------------------------------------------
    def _calculate_hysteria(self, text):
        score = 0.0

        # CAPS слова
        caps_words = [w for w in text.split() if w.isupper() and len(w) > 2]
        score += min(0.5, len(caps_words) / 3)

        # Оклички
        score += min(0.3, text.count('!') / 4)

        # Hysteria-слова
        hysteria_words = [
            'зрада', 'ганьба', 'скандал', 'негайно', 'пізно',
            'катастрофа', 'шок', 'ужас', 'паника', 'знищення'
        ]
        hysteria_count = sum(1 for w in hysteria_words if w in text.lower())
        score += min(0.4, hysteria_count / 2)

        # Короткі речення → hysteria flag
        sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
        if sentences:
            avg_len = sum(len(s.split()) for s in sentences) / len(sentences)
            if avg_len < 8:
                score += 0.2

        return min(1.0, score)

    # ----------------------------------------------------------
    # PSEUDO-INTELLECTUAL DETECTOR
    # ----------------------------------------------------------
    def _calculate_pseudo_intellectual(self, text):
        text_lower = text.lower()
        score = 0.0

        pseudo_words = [
            'парадигма', 'дискурс', 'наратив', 'конструкт', 'семіозис',
            'трансгресивний', 'деконструкція', 'постмодерн', 'метанаратив',
            'симулякр', 'гіперреальність', 'детеріторіалізація',
            'синергетичний', 'холістичний', 'мета-фізичний'
        ]

        found = sum(1 for w in pseudo_words if w in text_lower)
        if found >= 3:
            score = 0.4 + (found - 3) * 0.15

        # Довгі речення з 2+ pseudo-слова
        sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
        long_complex = 0
        for sentence in sentences:
            if len(sentence.split()) > 25:
                abstract = sum(1 for w in pseudo_words if w in sentence.lower())
                if abstract >= 2:
                    long_complex += 1
        if long_complex >= 2:
            score = max(score, 0.7)

        return min(1.0, score)
