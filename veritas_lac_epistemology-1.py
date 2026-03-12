"""
Veritas LAC Epistemology — v1.1
Detects four classic epistemic manipulation patterns:
  1. Anonymous authorities ("some experts", "independent researchers")
  2. Correlation-as-causation framing
  3. Unfalsifiable / conspiracy framing ("science doesn't recognize this — which is telling")
  4. Conclusion leap — logical jump from data to radical claim via "логічно припустити", "таким чином"
  5. Unverified citation — named sources cited without verifiable links

Interface mirrors veritas_lac_labor / veritas_lac_finance.
"""

import re
from dataclasses import dataclass, field
from typing import List


@dataclass
class EpistemologyResult:
    score: float                  # 0.0 = clean, 1.0 = severe
    verdict: str                  # CLEAN | ANONYMOUS_AUTHORITY | CORRELATION_CAUSATION | UNFALSIFIABLE | CONCLUSION_LEAP | COMBINED
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
        # ── Журналістський анонімний жаргон ──────────────────────────────
        r'\bsources?\s+familiar\s+with\b',
        r'\bpeople\s+familiar\s+with\b',
        r'\bsource\s+close\s+to\b',
        r'\bsources?\s+close\s+to\b',
        r'\bone\s+\w{2,20}\s+official\b',          # "one Trump official", "one senior official"
        r'\b\w{2,20}\s+official\s+(told|said)\b',  # "official told CNN"
        r'\bsenior\s+\w{0,20}\s*official\b',
        r'\bsources?\s+who\s+(spoke|requested|asked)\b',
        r'\bofficials?\s+who\s+(spoke|declined|requested)\b',
        r'\bsources?\s+(said|told|described|confirmed)\b.{0,30}(anonymously|condition|name)',
        r'\bspoke\s+on\s+(the\s+)?condition\s+of\s+anonymity\b',
        r'\brequested\s+anonymity\b',
        r'\bdeclined\s+to\s+be\s+(named|identified)\b',
        r'\bwho\s+(asked|requested)\s+(not\s+to\s+be\s+named|anonymity)\b',
    ]

    # ── Pattern 2: Correlation-as-causation ─────────────────────────────────
    CORR_PATTERNS_UK = [
        r'\bкорел[яя]ц[іи]\w*',
        r'\bзбіг\s+(у|в)\s+час',
        r'\bспівпад[аі]\w*',
        r'\bодночасн\w+\s+з(ріст|рост|збільш)',
        r'\bпаралельн\w+\s+з(ріст|рост)',
        r'\bна\s+тлі\s+(зростання|збільшення|падіння)\b.*\b(також|одночасно)',
        # Імплікована причинність без слова "кореляція"
        r'\bвраховуючи\s+(ці|дані|результати|вищезазначен)\w*\s*,?\s*(логічно|можна|варто|слід)',
        r'\bаналогічн[іі]\s+результати\b.{0,80}\b(також|підтверджують|свідчать)',
        r'\bпоказали?\s+що\b.{0,120}\bможе\s+мати\b',
        r'\bдемонструють\b.{0,80}\b(може|призводить|веде\s+до)\b',
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
        # Implied causation without the word "correlation"
        r'\bgiven\s+(these|this|the)\s+(data|results|findings)\b.{0,60}(logical|reasonable|safe)\s+to\s+(assume|conclude|suggest)',
        r'\bshowed?\s+that\b.{0,120}\bmay\s+have\b',
        r'\bdemonstrat\w+\b.{0,80}\b(may|leads?\s+to|results?\s+in)\b',
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

    # ── Pattern 4: Conclusion leap ───────────────────────────────────────────
    # Псевдологічний перехід від даних до радикального висновку
    LEAP_PATTERNS_UK = [
        r'\bлогічно\s+(припустити|зробити\s+висновок|вважати)\b',
        r'\bтаким\s+чином\s*,?\s*(батьки|люди|ми|суспільство|держава)\b',
        r'\bотже\s*,?\s*(батьки|люди|ми|суспільство)\b.{0,80}(ставлять|загрожують|несуть)',
        r'\bможна\s+зробити\s+висновок\s+що\b.{0,80}(фактично|по\s+суті|насправді)',
        r'\bфактично\s+(ставлять|піддають|загрожують|знищують)\b',
        r'\bнеобхідно\s+визнати\s+що\b.{0,60}(призводить|веде|спричиняє)',
        r'\bнаслідком\s+(цього|чого)\s+є\b.{0,60}(неминуч|очевидн|зрозумі)',
        r'\bзалишається\s+(лише|тільки)\s+(визнати|погодитись|прийняти)\b',
    ]
    LEAP_PATTERNS_EN = [
        r'\blogically\s+(follows|conclude|assume|implies?)\b',
        r'\bthus\b.{0,60}(parents?|people|we|society|children)\b.{0,60}(are|put|face|risk)',
        r'\btherefore\b.{0,60}(parents?|people|children)\b.{0,80}(effectively|essentially|actually)\b',
        r'\bit\s+is\s+(safe|logical|reasonable)\s+to\s+(assume|conclude|infer)\b',
        r'\beffectively\s+(putting|destroying|undermining|jeopardizing)\b',
        r'\bonly\s+(logical|reasonable)\s+conclusion\b',
        r'\bmust\s+(accept|acknowledge|recognize)\s+that\b.{0,60}(leads?|causes?|results?)',
        r'\bthe\s+data\s+(clearly|obviously|inevitably)\s+(show|suggest|prove|indicate)\b',
    ]

    # ── Pattern 5: Unverified named citation ─────────────────────────────────
    # Іменований авторитет без верифікованого посилання (URL/DOI/журнал)
    UNVERIFIED_CITE_PATTERNS_UK = [
        r'\b(дослідження|робота|стаття)\s+\w+\s+(та|і|et)\s+\w+\.?\s*\(\d{4}\)',
        r'\bуніверситет\w*\s+\w+\s*\(\d{4}\)\s+показал',
        r'\bдослідження\s+університет\w*\s+\w+\s*\(\d{4}\)',
    ]
    UNVERIFIED_CITE_PATTERNS_EN = [
        r'\b\w+\s+et\s+al\.\s*\(\d{4}\)',
        r'\buniversity\s+of\s+\w+\s*\(\d{4}\)\s+(study|research|found|showed)',
        r'\b(study|research)\s+(by|from|at)\s+\w[\w\s]+university\b.{0,60}\(\d{4}\)',
        r'\b\w+\s+\(\d{4}\)\s+(found|showed|demonstrated|reported)\b',
    ]

    # Threshold: how many hits trigger each pattern
    ANON_THRESHOLD = 1
    CORR_THRESHOLD = 1
    UNFALS_THRESHOLD = 1
    LEAP_THRESHOLD = 1
    UNVERIFIED_CITE_THRESHOLD = 1

    def analyze(self, text: str) -> EpistemologyResult:
        if not text or len(text.strip()) < 50:
            return EpistemologyResult(
                score=0.0,
                verdict='N/A',
                is_epistemic_content=False
            )

        t = text.lower()

        # Count hits per pattern group
        anon_hits        = self._count_hits(t, self.ANON_PATTERNS_UK + self.ANON_PATTERNS_EN)
        corr_hits        = self._count_hits(t, self.CORR_PATTERNS_UK + self.CORR_PATTERNS_EN)
        unfals_hits      = self._count_hits(t, self.UNFALS_PATTERNS_UK + self.UNFALS_PATTERNS_EN)
        leap_hits        = self._count_hits(t, self.LEAP_PATTERNS_UK + self.LEAP_PATTERNS_EN)
        unverified_hits  = self._count_hits(t, self.UNVERIFIED_CITE_PATTERNS_UK + self.UNVERIFIED_CITE_PATTERNS_EN)

        pattern_hits = {
            'anonymous_authority':    anon_hits,
            'correlation_causation':  corr_hits,
            'unfalsifiable':          unfals_hits,
            'conclusion_leap':        leap_hits,
            'unverified_citation':    unverified_hits,
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

        if leap_hits >= self.LEAP_THRESHOLD:
            triggered.append('CONCLUSION_LEAP')
            red_flags.append(f'conclusion_leap:{leap_hits}')
            missing.append('logical chain connecting data to conclusion')
            evidence.append('Text jumps from observation to radical conclusion using pseudo-logical connectors ("логічно припустити", "таким чином")')

        if unverified_hits >= self.UNVERIFIED_CITE_THRESHOLD:
            triggered.append('UNVERIFIED_CITATION')
            red_flags.append(f'unverified_citation:{unverified_hits}')
            missing.append('verifiable URL, DOI, or direct link to cited study')
            evidence.append('Text cites named studies or authors without providing a verifiable link or DOI')

        is_epistemic = bool(triggered)

        if not triggered:
            return EpistemologyResult(
                score=0.0,
                verdict='CLEAN',
                is_epistemic_content=False,
                pattern_hits=pattern_hits
            )

        # Score: each pattern adds weight
        # Leap and unverified citation are particularly deceptive — higher weight
        weights = {
            'ANONYMOUS_AUTHORITY':  0.30,
            'CORRELATION_CAUSATION': 0.30,
            'UNFALSIFIABLE':        0.35,
            'CONCLUSION_LEAP':      0.35,
            'UNVERIFIED_CITATION':  0.25,
        }
        score = min(1.0, sum(weights.get(p, 0.30) for p in triggered))

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
