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

        self_reference_score = min(1.0, total_score)

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
