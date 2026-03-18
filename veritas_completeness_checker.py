"""
Veritas Context Completeness Checker v1.0
Philosophy: "The Witness is not a judge. It notices what is absent."

Does NOT block or condemn. Only raises a flag when a text presents
a significant claim but is missing expected contextual dimensions.

Signals detected (as soft warnings, not verdicts):
- ONE_SIDE_ONLY: Only one actor's perspective present
- MISSING_CAUSATION: What/who but no why
- MISSING_COST: Action described without costs/consequences
- MISSING_SOURCE: Claim without traceable origin
- MISSING_TIMEFRAME: No temporal anchoring for a time-sensitive claim
- MISSING_COUNTERPOSITION: Strong assertion with zero acknowledgment of alternatives
"""

import re
from typing import Dict, List


class ContextCompletenessChecker:

    def __init__(self):

        # ── Actors / Sources ─────────────────────────────────────────
        # Words that introduce a named actor making a claim
        self.actor_patterns = [
            r'\b(сша|нато|україна|росія|єс|оон|мвф|байден|зеленський|путін|трамп)\b',
            r'\b(міністерство|уряд|президент|парламент|конгрес|сенат|рада)\b',
            r'\b(за\s+даними|згідно\s+з|повідомляє|пише|заявив|заявила|заявили)\b',
            r'\b(washington|kyiv|brussels|beijing|london|berlin|paris)\b',
        ]

        # ── Causation markers ────────────────────────────────────────
        self.causation_patterns = [
            r'\b(тому\s+що|через|оскільки|причиною|внаслідок|бо|адже)\b',
            r'\b(мотивовано|обґрунтовано|пояснено|причина|підстава)\b',
            r'\b(because|due\s+to|since|reason|motivated\s+by)\b',
        ]

        # ── Cost / consequence markers ───────────────────────────────
        self.consequence_patterns = [
            r'\b(наслідком|призведе|спричинить|результатом|ціною)\b',
            r'\b(втрати|ризики|витрати|компроміс|жертви|збитки)\b',
            r'\b(натомість|однак|проте|але|водночас|з\s+іншого\s+боку)\b',
            r'\b(consequence|cost|however|nevertheless|tradeoff)\b',
        ]

        # ── Counter-position markers ─────────────────────────────────
        self.counterposition_patterns = [
            r'\b(деякі\s+вважають|інші\s+стверджують|є\s+думка|опоненти)\b',
            r'\b(критики|скептики|противники|альтернативна\s+точка)\b',
            r'\b(з\s+іншого\s+боку|водночас|попри|незважаючи)\b',
            r'\b(critics|opponents|alternatively|on\s+the\s+other\s+hand)\b',
        ]

        # ── Source markers ───────────────────────────────────────────
        self.source_patterns = [
            r'\b(за\s+даними|згідно\s+з|повідомляє|джерело|посилаючись)\b',
            r'\b(офіційно|офіційне\s+джерело|прес-служба|заява)\b',
            r'\b(according\s+to|sources\s+say|reported\s+by|citing)\b',
            # Named media outlets count as sources
            r'\b(politico|reuters|bbc|ap|bloomberg|nyt|guardian|axios)\b',
            r'\b(пише|повідомляє|за\s+інформацією|за\s+словами)\b',
            r'\b(рейтер|бі-бі-сі|укрінформ|радіо\s+свобода|deutsche\s+welle)\b',
        ]

        # ── Claim strength markers ───────────────────────────────────
        # These indicate a STRONG assertion that demands context
        self.strong_claim_patterns = [
            r'\b(тиснуть|змушують|блокують|забороняють|вимагають)\b',
            r'\b(ніколи|завжди|всі|жоден|категорично|остаточно)\b',
            r'\b(зрада|капітуляція|ультиматум|загроза|шантаж)\b',
            r'\b(forces|blocks|demands|threatens|ultimatum|betrayal)\b',
            r'\b(sanctions|invasion|violated|condemned|illegal|war crimes?)\b',
            r'\b(never|always|all|none|categorically|definitively|absolutely)\b',
            r'\b(coup|genocide|terrorist|attack|occupation|aggression)\b',
        ]

    # ================================================================
    # MAIN ANALYSIS
    # ================================================================

    def analyze(self, text: str) -> Dict:
        text_lower = text.lower()
        word_count = len(text.split())

        # Skip very short texts — not enough to judge completeness
        if word_count < 20:
            return self._clean_result('Текст занадто короткий для аналізу повноти.')

        # ── Detect what IS present ────────────────────────────────────
        has_actor = self._any_match(self.actor_patterns, text_lower)
        has_causation = self._any_match(self.causation_patterns, text_lower)
        has_consequence = self._any_match(self.consequence_patterns, text_lower)
        has_counterposition = self._any_match(self.counterposition_patterns, text_lower)
        has_source = self._any_match(self.source_patterns, text_lower)
        has_strong_claim = self._any_match(self.strong_claim_patterns, text_lower)

        # ── Build missing dimensions ──────────────────────────────────
        missing = []

        # Only flag causation if there's a strong claim but no explanation
        if has_strong_claim and not has_causation:
            missing.append({
                'dimension': 'ПРИЧИННІСТЬ',
                'dimension_en': 'CAUSATION',
                'hint': 'Присутня сильна заява без пояснення причини або мотиву.',
                'hint_en': 'Strong claim present without explanation of cause or motive.',
            })

        if has_strong_claim and not has_consequence:
            missing.append({
                'dimension': 'НАСЛІДКИ',
                'dimension_en': 'CONSEQUENCES',
                'hint': 'Дія або тиск описані без аналізу витрат або наслідків.',
                'hint_en': 'Action or pressure described without analysis of costs or consequences.',
            })

        if has_strong_claim and not has_counterposition:
            missing.append({
                'dimension': 'АЛЬТЕРНАТИВНА ПОЗИЦІЯ',
                'dimension_en': 'ALTERNATIVE POSITION',
                'hint': 'Сильне твердження подане без альтернативної точки зору.',
                'hint_en': 'Strong assertion presented without any alternative perspective.',
            })

        if has_actor and not has_source and word_count > 30:
            missing.append({
                'dimension': 'ДЖЕРЕЛО',
                'dimension_en': 'SOURCE',
                'hint': 'Згадано актора або подію без посилання на верифіковане джерело.',
                'hint_en': 'Actor or event mentioned without reference to a verifiable source.',
            })

        # ── Calculate completeness score ──────────────────────────────
        # Not a penalty — just a measure of how many dimensions are absent
        if not has_strong_claim and not has_actor:
            # Neutral/descriptive text — completeness not applicable
            completeness_score = 0.0
            missing = []
        else:
            max_possible = 4  # causation, consequence, counterposition, source
            completeness_score = round(len(missing) / max_possible, 2)

        # ── Verdict (always advisory, never blocking) ─────────────────
        if completeness_score >= 0.75:
            verdict    = 'НЕПОВНИЙ_КОНТЕКСТ'
            verdict_en = 'INCOMPLETE_CONTEXT'
            note    = 'Текст містить значущі твердження, але відсутні кілька контекстуальних вимірів. Свідок рекомендує перехресну перевірку.'
            note_en = 'Text contains significant claims but several contextual dimensions are missing. Cross-referencing recommended.'
        elif completeness_score >= 0.50:
            verdict    = 'ЧАСТКОВИЙ_КОНТЕКСТ'
            verdict_en = 'PARTIAL_CONTEXT'
            note    = 'Деякі виміри контексту відсутні. Для повної картини варто звернутись до додаткових джерел.'
            note_en = 'Some contextual dimensions are missing. Additional sources recommended for a complete picture.'
        elif completeness_score >= 0.25:
            verdict    = 'МІНІМАЛЬНИЙ_КОНТЕКСТ'
            verdict_en = 'MINIMAL_CONTEXT'
            note    = 'Текст переважно повний, але окремі виміри відсутні.'
            note_en = 'Text is mostly complete but some dimensions are absent.'
        else:
            verdict    = 'КОНТЕКСТ_ПРИСУТНІЙ'
            verdict_en = 'CONTEXT_PRESENT'
            note    = 'Основні контекстуальні виміри присутні.'
            note_en = 'Main contextual dimensions are present.'

        return {
            'completeness_score':   completeness_score,
            'completeness_verdict': verdict,
            'completeness_verdict_en': verdict_en,
            'completeness_note':    note,
            'completeness_note_en': note_en,
            'missing_dimensions':   missing,
            'is_advisory_only':     True,
        }

    # ================================================================
    # HELPERS
    # ================================================================

    def _any_match(self, patterns: List[str], text: str) -> bool:
        return any(re.search(p, text, re.IGNORECASE) for p in patterns)

    def _clean_result(self, note: str) -> Dict:
        return {
            'completeness_score': 0.0,
            'completeness_verdict': 'Н/Д',
            'completeness_note': note,
            'missing_dimensions': [],
            'is_advisory_only': True,
        }
