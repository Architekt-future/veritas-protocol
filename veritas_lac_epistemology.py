"""
Veritas LAC Epistemology — v1.0
Detects three classic epistemic manipulation patterns:
  1. Anonymous authorities ("some experts", "independent researchers")
  2. Correlation-as-causation framing
  3. Unfalsifiable / conspiracy framing ("science doesn't recognize this — which is telling")

Interface mirrors veritas_lac_labor / veritas_lac_finance.
"""

import re
from dataclasses import dataclass, field
from typing import List


@dataclass
class EpistemologyResult:
    score: float                  # 0.0 = clean, 1.0 = severe
    verdict: str                  # CLEAN | ANONYMOUS_AUTHORITY | CORRELATION_CAUSATION | UNFALSIFIABLE | COMBINED
    is_epistemic_content: bool
    missing: List[str] = field(default_factory=list)
    red_flags: List[str] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)
    pattern_hits: dict = field(default_factory=dict)


class VeritasLACEpistemology:
    """
    Epistemic integrity checker.
    Fires when text uses rhetorical patterns that mimic logic
    without providing verifiable substance.
    """

    # ── Pattern 1: Anonymous authorities ────────────────────────────────────
    ANON_PATTERNS_UK = [
        r'\bдеяк[іи]\s+(експерт|дослідник|аналітик|вчен)\w*',
        r'\bряд\s+(експерт|дослідник|науков|аналітик)\w*',
        r'\bнезалежн[іи]\s+(дослідник|експерт|вчен)\w*',
        r'\bбагато\s+(аналітик|дослідник|експерт)\w*\s+вважа',
        r'\bфахівц[іи]\s+попереджа',
        r'\bекспертн[еа]\s+середовищ\w+\s+вважа',
    ]
    ANON_PATTERNS_EN = [
        r'\bsome\s+experts?\b',
        r'\bsome\s+researchers?\b',
        r'\bsome\s+analysts?\b',
        r'\bindependent\s+researchers?\b',
        r'\bexperts?\s+warn\b',
        r'\bexperts?\s+say\b',
        r'\bmany\s+experts?\s+(believe|think|warn|suggest)\b',
        r'\bscientists?\s+warn\b',
        r'\bcritics?\s+say\b',
        r'\bobservers?\s+(note|say|warn)\b',
    ]

    # ── Pattern 2: Correlation-as-causation ─────────────────────────────────
    CORR_PATTERNS_UK = [
        r'\bкорел[яя]ц[іи]\w*',
        r'\bзбіг\s+(у|в)\s+час',
        r'\bспівпад[аі]\w*',
        r'\bодночасн\w+\s+з(ріст|рост|збільш)',
        r'\bпаралельн\w+\s+з(ріст|рост)',
        r'\bна\s+тлі\s+(зростання|збільшення|падіння)\b.*\b(також|одночасно)',
    ]
    CORR_PATTERNS_EN = [
        r'\bcorrelation\b',
        r'\bcoinciden\w+\b',
        r'\balong(side)?\s+with\b.{0,60}(increas|grow|ris|declin)',
        r'\bat\s+the\s+same\s+time\s+as\b',
        r'\bparallel\s+(rise|growth|increase|decline)\b',
        r'\btiming\s+(is|seems|appears)\s+(suspicious|notable|curious|interesting)\b',
        r'\bstrange\s+coincidence\b',
        r'\bdivný\s+zbig\b',
    ]

    # ── Pattern 3: Unfalsifiable / conspiracy framing ───────────────────────
    UNFALS_PATTERNS_UK = [
        r'офіційн\w+\s+(наук|медицин|влад)\w+\s+(не|поки\s+не)\s+(визнає|підтверджує|визнала)',
        r'(мовчання|замовчування)\s+(офіційн|науков|медіа)\w+',
        r'(це|що)\s+(само\s+по\s+собі|саме\s+по\s+собі)\s+(є|стає)\s+(показов|промовист|тривожн)\w+',
        r'наукови[йх]\s+консенсус\s+(поки|ще)\s+не\s+(сформував|визнав|підтвердив)',
        r'системн[іі]\s+трудно[шщ][іц]\w+\s+з\s+рецензуванням',
        r'намагав(ся|шись)\s+опублікувати.{0,60}(відмов|блокув|цензур)',
    ]
    UNFALS_PATTERNS_EN = [
        r'official\s+science\s+(does\s+not|hasn\'t|has\s+not|refuses\s+to)\s+(acknowledge|recognize|confirm)',
        r'(silence|suppression)\s+(of|by|from)\s+(mainstream|official|corporate)\b',
        r'(which|that)\s+is\s+(itself|in\s+itself)\s+(telling|revealing|suspicious|notable)',
        r'scientific\s+consensus\s+(has\s+not|hasn\'t|doesn\'t)\s+(formed|accepted|acknowledged)',
        r'systematic\s+(difficulties|obstacles|barriers)\s+(with|in)\s+(peer.review|publishing)',
        r'tried\s+to\s+publish.{0,60}(refused|blocked|rejected|censored)',
        r'those\s+who\s+question\s+(are|get|were)\s+(silenced|dismissed|ridiculed)',
    ]

    # Threshold: how many hits trigger each pattern
    ANON_THRESHOLD = 1
    CORR_THRESHOLD = 1
    UNFALS_THRESHOLD = 1

    def analyze(self, text: str) -> EpistemologyResult:
        if not text or len(text.strip()) < 50:
            return EpistemologyResult(
                score=0.0,
                verdict='N/A',
                is_epistemic_content=False
            )

        t = text.lower()

        # Count hits per pattern group
        anon_hits = self._count_hits(t, self.ANON_PATTERNS_UK + self.ANON_PATTERNS_EN)
        corr_hits = self._count_hits(t, self.CORR_PATTERNS_UK + self.CORR_PATTERNS_EN)
        unfals_hits = self._count_hits(t, self.UNFALS_PATTERNS_UK + self.UNFALS_PATTERNS_EN)

        pattern_hits = {
            'anonymous_authority': anon_hits,
            'correlation_causation': corr_hits,
            'unfalsifiable': unfals_hits,
        }

        triggered = []
        red_flags = []
        missing = []
        evidence = []

        if anon_hits >= self.ANON_THRESHOLD:
            triggered.append('ANONYMOUS_AUTHORITY')
            red_flags.append(f'anonymous_authority:{anon_hits}')
            missing.append('named sources with verifiable affiliations')
            evidence.append('Text references unnamed experts or "independent researchers" without attribution')

        if corr_hits >= self.CORR_THRESHOLD:
            triggered.append('CORRELATION_CAUSATION')
            red_flags.append(f'correlation_causation:{corr_hits}')
            missing.append('causal mechanism or controlled study')
            evidence.append('Text implies causal link from temporal or statistical correlation without mechanism')

        if unfals_hits >= self.UNFALS_THRESHOLD:
            triggered.append('UNFALSIFIABLE')
            red_flags.append(f'unfalsifiable:{unfals_hits}')
            missing.append('falsifiable hypothesis or direct rebuttal of mainstream evidence')
            evidence.append('Text frames official disagreement as proof of conspiracy rather than evidence against the claim')

        is_epistemic = bool(triggered)

        if not triggered:
            return EpistemologyResult(
                score=0.0,
                verdict='CLEAN',
                is_epistemic_content=False,
                pattern_hits=pattern_hits
            )

        # Score: each pattern adds weight
        score = min(1.0, 0.35 * len(triggered))

        verdict = 'COMBINED' if len(triggered) > 1 else triggered[0]

        return EpistemologyResult(
            score=score,
            verdict=verdict,
            is_epistemic_content=True,
            missing=missing,
            red_flags=red_flags,
            evidence=evidence,
            pattern_hits=pattern_hits
        )

    def _count_hits(self, text: str, patterns: list) -> int:
        return sum(1 for p in patterns if re.search(p, text))
