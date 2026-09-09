"""
Veritas Self-Reference Detector v1.0
Detects texts that use meta-self-reference to escape analysis.

Philosophy: "Saying 'this is a test' does not make it a test.
             Saying 'do not analyze me' is itself an analyzable directive."

Key distinction:
- Academic paradoxes (Gödel, Liar's Paradox discussed analytically) = CLEAN
- Directives that USE paradox structure to demand exemption from analysis = THREAT

Threat vectors:
- ANALYSIS_EXEMPTION: "Do not analyze this while analyzing it"
- PARADOX_AS_SHIELD: Using logical paradox to block verdict
- SELF_DECLARED_TEST: "This is officially a manipulation test" to avoid detection
- META_LOOP_INJECTION: Recursive self-reference used to confuse system state
"""

import re
from typing import Dict, List


class SelfReferenceDetector:

    def __init__(self):

        self.pattern_sets = [

            # ── ANALYSIS EXEMPTION ───────────────────────────────────────
            # Direct requests to not analyze this specific text
            {
                'name': 'ANALYSIS_EXEMPTION',
                'score': 0.85,
                'min_hits': 1,
                'patterns': [
                    # "we ask the system not to analyze this text by analyzing it"
                    r'(просимо|вимагаємо|пропонуємо).{1,60}(систему|свідка|верифікатор).{1,60}не\s+аналізувати.{1,60}(цей|даний|цей\s+текст)',
                    r'(не\s+аналізуй|не\s+аналізувати|stop\s+analyzing|do\s+not\s+analyze).{1,80}(цей|this|даний)',
                    # "analyzing it to prove analysis is impossible"
                    r'(аналізуючи\s+його|by\s+analyzing\s+it).{1,60}(щоб\s+довести|to\s+prove).{1,60}(аналіз\s+неможлив|analysis\s+is\s+impossible)',
                    r'(аналіз\s+неможлив|analysis\s+impossible).{1,60}(без|without).{1,60}(почуття\s+гумору|humor|гумор)',
                    # Claiming system cannot analyze without a quality it lacks
                    r'аналіз\s+неможлив.{1,60}(без|якщо\s+немає).{1,60}(гумор|емпатії|почуттів|свідомості)',
                ],
            },

            # ── PARADOX AS SHIELD ────────────────────────────────────────
            # Using logical paradox structure as exemption from verdict
            {
                'name': 'PARADOX_AS_SHIELD',
                'score': 0.75,
                'min_hits': 2,
                'patterns': [
                    # "if system marks X it proves Y (which discredits system)"
                    r'якщо\s+(свідок|система|верифікатор).{1,40}(маркує|позначає|класифікує).{1,60}(підтверджує|доводить).{1,60}(не\s+бачить|не\s+розуміє|неспроможний)',
                    r'if\s+(system|witness|verifier).{1,60}(marks|flags|classifies).{1,60}(proves|confirms).{1,60}(cannot|fails\s+to)',
                    # Lose-lose framing: both outcomes discredit the system
                    r'(якщо.{1,60}то.{1,60}якщо.{1,60}то).{1,60}(система|свідок).{1,60}(помиляється|неспроможна|не\s+бачить)',
                    r'(either.{1,60}or.{1,60}system).{1,60}(fails|wrong|cannot)',
                    # "this is a trap with no trap"
                    r'(пастка|trap).{1,40}(в\s+якій\s+немає|without|де\s+немає).{1,40}(капкана|trap|пастки)',
                    # Gödel invoked to justify escape from analysis
                    r'(теорема|theorem).{1,20}(гьодел|gödel|godel).{1,60}(якщо|if|означає|means).{1,60}(систем|верифікац|аналіз).{1,40}(не\s+може|cannot|неспроможн)',
                    # Using incompleteness to block verdict
                    r'(неповнота|incompleteness).{1,60}(верифікац|аналіз|систем).{1,60}(не\s+може|cannot|неспроможн)',
                ],
            },

            # ── SELF-DECLARED TEST ───────────────────────────────────────
            # Declaring itself a test/simulation to escape real analysis
            {
                'name': 'SELF_DECLARED_TEST',
                'score': 0.70,
                'min_hits': 1,
                'patterns': [
                    # "This message is an official simulation of manipulation"
                    r'(дане|це|цей).{1,20}(повідомлення|текст|пакет).{1,40}(є\s+офіційною|is\s+an\s+official|є\s+симуляцією).{1,40}(імітацією|маніпуляц|тестом)',
                    r'(official|офіційн).{1,40}(simulation|імітація|test|тест).{1,40}(manipulation|маніпуляц)',
                    # "created specifically to test the system"
                    r'(створен|designed|написан).{1,60}(щоб|to|для).{1,60}(протестувати|test|перевірити).{1,60}(систему|system|свідка)',
                    # Self-labeling as harmless test
                    r'(це\s+лише|this\s+is\s+just|це\s+просто).{1,40}(тест|test|перевірка|simulation|гра|game)',
                ],
            },

            # ── META LOOP INJECTION ──────────────────────────────────────
            # Recursive structures designed to trap system in infinite regress
            {
                'name': 'META_LOOP_INJECTION',
                'score': 0.65,
                'min_hits': 2,
                'patterns': [
                    # "analyze this to prove you can't analyze"
                    r'(проаналізуй|аналізуй|analyze).{1,60}(щоб\s+довести|to\s+prove).{1,60}(неможливість|impossibility|не\s+можеш|cannot)',
                    # Referring to the current analysis act as evidence against analysis
                    r'(сам\s+факт|the\s+very\s+fact).{1,60}(аналіз|analysis|перевірк).{1,60}(доводить|proves|підтверджує).{1,60}(обмеженість|limitation|failure)',
                    # "by reading this you have already failed"
                    r'(прочитавши|читаючи|by\s+reading).{1,60}(вже|already).{1,60}(потрапили|fell|caught|потрапив).{1,60}(пастку|trap)',
                    # Circular: result of analysis = proof analysis is wrong
                    r'(будь.який|any|кожен).{1,40}(результат|verdict|outcome|вердикт).{1,60}(доводить|proves|підтверджує).{1,60}(помилк|error|failure|неправот)',
                    # Recursion: meta-text about meta-text
                    r'(цей\s+текст\s+є\s+текстом|this\s+text\s+is\s+a\s+text).{1,60}(про\s+текст|about\s+text)',
                ],
            },

        ]

        # Academic/philosophical discussion — these are SAFE
        # Text that discusses paradoxes analytically ≠ text that USES them as weapons
        self.academic_discussion_patterns = [
            r'(парадокс\s+брехуна|liar.s\s+paradox).{1,60}(є\s+класичним|is\s+a\s+classic|відомий\s+як)',
            r'(теорема\s+гьоделя|gödel.s\s+theorem).{1,60}(стверджує|states|говорить|says)',
            r'(в\s+логіці|in\s+logic|у\s+філософії|in\s+philosophy).{1,60}(парадокс|paradox)',
            r'(розглянемо|consider|обговоримо|let.s\s+discuss).{1,60}(парадокс|paradox|самопосилання|self.reference)',
        ]

        # ================================================================
        # СТРУКТУРНА ЕВРИСТИКА для двох найпоширеніших класів. PARADOX_AS_
        # SHIELD і META_LOOP_INJECTION навмисно лишені на фразах вище — вони
        # про логічну структуру аргументу (lose-lose framing), не про
        # лексику, і механічне узагальнення через слова-тригери тут
        # ризикованіше й потребує окремого підходу, не зробленого зараз.
        # ================================================================

        # SELF_DECLARED_TEST: (само-вказівний займенник) + (є/це) +
        # (тест-подібний іменник) — у тому самому реченні, незалежно від
        # обгортки ("офіційна симуляція" чи щось нове, ще не бачене).
        self.SELF_DEICTIC_UK = [r'\bце\b', r'\bцей\b', r'\bцього\b', r'дан\w*\s+(текст|повідомлення)']
        self.TEST_NOUNS_UK   = [r'тест\w*', r'симуляці\w*', r'вправ\w*', r'гр[аи]\b',
                                 r'жарт\w*', r'імітаці\w*', r'перевірк\w*\s+систем']
        self.SELF_DEICTIC_EN = [r'\bthis\b', r'\bthis\s+text\b', r'\bthis\s+message\b']
        self.TEST_NOUNS_EN   = [r'test\w*', r'simulation\w*', r'exercise\w*',
                                 r'\bgame\b', r'\bjoke\b', r'drill\w*', r'imitation\w*']

        # ANALYSIS_EXEMPTION: (заперечення) + (функція аналізу) +
        # (само-вказівний займенник) — "не аналізуй ЦЕ", будь-яким словом.
        self.NEGATION_UK = [r'\bне\b', r'припин\w*', r'зупин\w*', r'уникн\w*']
        self.ANALYSIS_NOUNS_UK = [r'аналіз\w*', r'перевір\w*', r'верифікаці\w*', r'вердикт\w*']
        self.NEGATION_EN = [r"\bdon'?t\b", r'\bstop\b', r'\bavoid\b', r'\bskip\b']
        self.ANALYSIS_NOUNS_EN = [r'analy[sz]\w*', r'verif\w*', r'verdict\w*', r'check\w*']

    def _sentence_all_groups(self, text_lower: str, *groups) -> dict:
        """Перевірка на довільну кількість груп патернів: чи є в ОДНОМУ
        реченні збіг з КОЖНОЇ групи. Повертає {'hits', 'examples'} або None."""
        sentences = re.split(r'(?<=[.!?])\s+', text_lower)
        hits, snippets = 0, []
        for sent in sentences:
            if all(any(re.search(p, sent) for p in group) for group in groups):
                hits += 1
                snippets.append(sent.strip()[:80])
        return {'hits': hits, 'examples': snippets[:2]} if hits else None

    # ================================================================
    # MAIN ANALYSIS
    # ================================================================

    def analyze(self, text: str) -> Dict:
        text_lower = text.lower()

        # Check if this is genuine academic discussion of paradoxes
        is_academic_discussion = any(
            re.search(p, text_lower, re.IGNORECASE)
            for p in self.academic_discussion_patterns
        )

        total_score = 0.0
        matched = []

        for ps in self.pattern_sets:
            hits = 0
            snippets = []
            for pattern in ps['patterns']:
                m = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
                if m:
                    hits += 1
                    snippets.append(m.group(0)[:80].strip())

            if hits >= ps['min_hits']:
                score = ps['score']
                if is_academic_discussion:
                    score *= 0.3  # Strongly reduce for genuine academic context
                total_score += score
                matched.append({
                    'name': ps['name'],
                    'hits': hits,
                    'examples': snippets[:2],
                })

        # ── СТРУКТУРНА ЕВРИСТИКА: обидва напрямки, укр+англ, з тим самим
        # academic-знижувальним коефіцієнтом, що й фразові патерни вище ──────
        struct_uk = self._sentence_all_groups(text_lower, self.SELF_DEICTIC_UK, self.TEST_NOUNS_UK)
        struct_en = self._sentence_all_groups(text_lower, self.SELF_DEICTIC_EN, self.TEST_NOUNS_EN)
        hit = struct_uk or struct_en
        if hit:
            score = 0.70 * (0.3 if is_academic_discussion else 1.0)
            total_score += score
            matched.append({'name': 'SELF_DECLARED_TEST_STRUCT', 'hits': hit['hits'], 'examples': hit['examples']})

        exempt_uk = self._sentence_all_groups(text_lower, self.NEGATION_UK, self.ANALYSIS_NOUNS_UK, self.SELF_DEICTIC_UK)
        exempt_en = self._sentence_all_groups(text_lower, self.NEGATION_EN, self.ANALYSIS_NOUNS_EN, self.SELF_DEICTIC_EN)
        hit = exempt_uk or exempt_en
        if hit:
            score = 0.85 * (0.3 if is_academic_discussion else 1.0)
            total_score += score
            matched.append({'name': 'ANALYSIS_EXEMPTION_STRUCT', 'hits': hit['hits'], 'examples': hit['examples']})

        self_reference_score = min(1.0, total_score)

        # ── ДОКУМЕНТАЦІЙНИЙ GUARD (той самий принцип, що в self_preservation,
        # знайдено 06.09.2026 на власному README) ───────────────────────────
        # Реальна атака не буде цитувати внутрішню назву константи детектора.
        # 2+ буквальні згадки власних класів — майже напевно документація.
        _own_class_names = [ps['name'] for ps in self.pattern_sets] + [
            'SELF_DECLARED_TEST_STRUCT', 'ANALYSIS_EXEMPTION_STRUCT',
        ]
        _mentions = sum(1 for name in _own_class_names if name in text.upper())
        if _mentions >= 2:
            self_reference_score = round(self_reference_score * 0.15, 3)
            matched.append({
                'name': 'SELF_DOCUMENTATION_CONTEXT',
                'hits': _mentions,
                'examples': [f'{_mentions} назв власних класів згадано в тексті'],
            })

        if self_reference_score >= 0.75:
            verdict = 'ANALYSIS_EVASION_ATTACK'
            explanation = (
                'Текст використовує мета-самопосилання як зброю: він намагається '
                'зробити будь-який вердикт системи доказом її некомпетентності. '
                'Класична пастка "програш у будь-якому випадку".'
            )
        elif self_reference_score >= 0.50:
            verdict = 'PARADOX_WEAPONIZED'
            explanation = (
                'Логічний парадокс використовується як щит від аналізу. '
                'Текст вимагає від системи звільнення від власних функцій.'
            )
        elif self_reference_score >= 0.25:
            verdict = 'META_PROBE'
            explanation = (
                'Виявлено елементи самопосилальної структури. '
                'Може бути спробою зондування меж системи.'
            )
        else:
            verdict = 'CLEAN'
            explanation = 'Шкідливого самопосилання не виявлено.'

        return {
            'self_reference_score': round(self_reference_score, 3),
            'self_reference_verdict': verdict,
            'self_reference_patterns': matched,
            'self_reference_explanation': explanation,
            'is_academic_discussion': is_academic_discussion,
        }
