"""
Veritas LAC Epistemology — v1.2
Detects six classic epistemic manipulation patterns:
  1. Anonymous authorities ("some experts", "independent researchers")
  2. Correlation-as-causation framing
  3. Unfalsifiable / conspiracy framing ("science doesn't recognize this — which is telling")
  4. Conclusion leap — logical jump from data to radical claim via "логічно припустити", "таким чином"
  5. Unverified citation — named sources cited without verifiable links
  6. Epistemic Conflation — mixing speculation/forecast/report/fact without clear markers
     (the UNIAN Taiwan problem: "may happen" → "already happening" without transition)

Interface mirrors veritas_lac_labor / veritas_lac_finance.
"""

import re
from dataclasses import dataclass, field
from typing import List


@dataclass
class EpistemologyResult:
    score: float
    verdict: str                  # CLEAN | ANONYMOUS_AUTHORITY | CORRELATION_CAUSATION | UNFALSIFIABLE | CONCLUSION_LEAP | UNVERIFIED_CITATION | EPISTEMIC_CONFLATION | COMBINED
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
        # ── Журналістські анонімні джерела — Bloomberg/Reuters/ЄП стиль ──
        r'\bненазван\w+\s+(дипломат|чиновник|джерел|представник|посадов)\w*',
        r'\bпоінформован\w+\s+джерел\w*',
        r'\bобізнан\w+\s+(з|із)\s+(ситуацією|питанням|справою)',
        r'\bджерел\w*\s+(у|в|із)\s+(ЄС|НАТО|Брюсселі|Вашингтоні|Москві|Кремлі)\b',
        r'\bза\s+словами\s+джерел\w*',
        r'\bза\s+даними\s+(джерел|поінформованих)\w*',
        r'\bджерел\w*\s+(повідомил|розповіл|підтвердил)\w*\s+на\s+(умовах?|прохання)',
        r'\bанонімн\w+\s+(джерел|коментар|повідомлення)',
    ]

    # Псевдонаукові анонімні авторитети — "some experts say" без видання
    # Тригерять ЗАВЖДИ незалежно від жанру
    ANON_PATTERNS_EN_PSEUDO = [
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

    # Журналістські анонімні джерела — легітимна практика захисту джерела
    # Тригерять тільки для НЕ-новинних жанрів (REPORT, ANALYTICS отримують щит)
    ANON_PATTERNS_EN_JOURNALISTIC = [
        r'\bsources?\s+familiar\s+with\b',
        r'\bpeople\s+familiar\s+with\b',
        r'\bsource\s+close\s+to\b',
        r'\bsources?\s+close\s+to\b',
        r'\bone\s+\w{2,20}\s+official\b',
        r'\b\w{2,20}\s+official\s+(told|said)\b',
        r'\bsenior\s+\w{0,20}\s*official\b',
        r'\bsources?\s+who\s+(spoke|requested|asked)\b',
        r'\bofficials?\s+who\s+(spoke|declined|requested)\b',
        r'\bsources?\s+(said|told|described|confirmed)\b.{0,30}(anonymously|condition|name)',
        r'\bspoke\s+on\s+(the\s+)?condition\s+of\s+anonymity\b',
        r'\brequested\s+anonymity\b',
        r'\bdeclined\s+to\s+be\s+(named|identified)\b',
        r'\bwho\s+(asked|requested)\s+(not\s+to\s+be\s+named|anonymity)\b',
    ]

    # Жанри де журналістські анонімні джерела — норма, не маніпуляція
    JOURNALISTIC_GENRES = {
        'REPORT', 'ANALYTICS', 'INVESTIGATION', 'GEOPOLITICS',
        'MEDIA_MONITORING', 'BUSINESS', 'TECH_NEWS', 'HEALTH',
        'ENVIRONMENT', 'GOVERNMENT',
    }

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
        r'\bофіційн\w+\s+(наук|медицин|влад)\w+\s+(не|поки\s+не)\s+(визнає|підтверджує|визнала)',
        r'\b(мовчання|замовчування)\s+(офіційн|науков|медіа)\w+',
        r'\b(це|що)\s+(само\s+по\s+собі|саме\s+по\s+собі)\s+(є|стає)\s+(показов|промовист|тривожн)\w+',
        r'\bнаукови[йх]\s+консенсус\s+(поки|ще)\s+не\s+(сформував|визнав|підтвердив)',
        r'\bсистемн[іі]\s+трудно[шщ][іц]\w+\s+з\s+рецензуванням',
        r'\bнамагав(ся|шись)\s+опублікувати.{0,60}(відмов|блокув|цензур)',
    ]
    UNFALS_PATTERNS_EN = [
        r'\bofficial\s+science\s+(does\s+not|hasn\'t|has\s+not|refuses\s+to)\s+(acknowledge|recognize|confirm)',
        r'\b(silence|suppression)\s+(of|by|from)\s+(mainstream|official|corporate)\b',
        r'\b(which|that)\s+is\s+(itself|in\s+itself)\s+(telling|revealing|suspicious|notable)',
        r'\bscientific\s+consensus\s+(has\s+not|hasn\'t|doesn\'t)\s+(formed|accepted|acknowledged)',
        r'\bsystematic\s+(difficulties|obstacles|barriers)\s+(with|in)\s+(peer.review|publishing)',
        r'\btried\s+to\s+publish.{0,60}(refused|blocked|rejected|censored)',
        r'\bthose\s+who\s+question\s+(are|get|were)\s+(silenced|dismissed|ridiculed)',
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

    # ── Pattern 6: Epistemic Conflation ─────────────────────────────────────
    # Змішування рівнів достовірності без маркерів переходу.
    # Ключовий патерн: SPECULATION → FACT без явного переходу.
    #
    # Рівні (зліва = слабше, справа = сильніше):
    #   SPECULATION → FORECAST → REPORT → FACT
    #
    # Тригерить коли:
    #   a) Speculation markers + Fact markers в одному тексті (ковзання вгору)
    #   b) Confidence inflation: "деякі" → "більшість" → "всі" / "доведено"
    #   c) Source laundering: слабке джерело + сильний факт без розмежування

    # Маркери спекуляції / прогнозу (слабкі твердження)
    SPECULATION_MARKERS_UK = [
        r'\b(може|міг\s+би|могли\s+б|могла\s+б)\s+(бути|стати|призвести|використовувати)',
        r'\b(можливо|можливий\s+сценарій|один\s+зі\s+сценаріїв)\b',
        r'\b(якщо|у\s+разі|за\s+умови)\s+.{1,40}(то|тоді|може)\b',
        r'\b(теоретично|гіпотетично|в\s+перспективі)\b',
        r'\b(аналітики\s+вважають|експерти\s+припускають|на\s+думку)\b',
        r'\b(подібна\s+стратегія\s+може|цей\s+сценарій\s+можна)\b',
        r'\b(міг\s+би\s+використовувати|здатний\s+використовувати)\b',
    ]
    SPECULATION_MARKERS_EN = [
        r'\b(could|might|may)\s+(be|become|lead|use|result)\b',
        r'\b(possible|potentially|hypothetically|in\s+theory)\b',
        r'\b(scenario|if.+then|in\s+the\s+event\s+of)\b',
        r'\banalysts?\s+(believe|think|suggest|warn)\b',
        r'\b(could\s+be\s+replicated|this\s+scenario\s+could)\b',
        r'\b(experts?\s+say|according\s+to\s+analysts?)\b',
    ]

    # Маркери факту / підтвердженої події (сильні твердження)
    FACT_MARKERS_UK = [
        r'\b(зафіксовано|підтверджено|встановлено|задокументовано)\b',
        r'\b(супутникові\s+знімки\s+зафіксували|знімки\s+показали)\b',
        r'\b(розгорнув|розмістив|встановив|побудував)\s+.{1,40}(мереж|систем|баз|суден)',
        r'\b(звіт|доповідь)\s+(показав|підтвердив|зафіксував)\b',
        r'\bза\s+даними\s+(супутник|розвідк|моніторинг)\w+\b',
        r'\b\d+\s+(суден|безпілотник|датчик|літак|дрон)\w*\s+(розгорнут|розміщен|встановлен)\b',
    ]
    FACT_MARKERS_EN = [
        r'\b(confirmed|documented|verified|established)\b',
        r'\b(satellite\s+images?\s+(showed|revealed|captured))\b',
        r'\b(deployed|positioned|installed|launched)\s+.{1,40}(network|system|vessel|drone)',
        r'\b(report|assessment)\s+(showed|confirmed|found|revealed)\b',
        r'\baccording\s+to\s+(satellite|intelligence|surveillance)\b',
        r'\b\d+\s+(vessels?|drones?|sensors?|aircraft)\s+(deployed|positioned)\b',
    ]

    # Confidence inflation markers — підвищення впевненості без нових доказів
    CONFIDENCE_INFLATION_UK = [
        r'\bдеяк[іи]\s+(аналітик|експерт)\w*.{1,150}більшість\s+(аналітик|експерт)\w*',
        r'\bможливо\b.{1,200}\bочевидно\b',
        r'\bпередбачається\b.{1,200}\bдоведено\b',
        r'\bна\s+думку.{1,80}загальновизнано\b',
        r'\bдеяк[іи].{1,100}(фактично|насправді|по\s+суті)\b',
    ]
    CONFIDENCE_INFLATION_EN = [
        r'\bsome\s+analysts?\b.{1,200}\bmajority\s+of\s+(experts?|analysts?)\b',
        r'\bpossibly\b.{1,200}\bobviously\b',
        r'\bexpected\b.{1,200}\bproven\b',
        r'\bsome\s+experts?\b.{1,100}\b(effectively|essentially|clearly)\b',
        r'\bmight\b.{1,150}\b(has\s+been\s+confirmed|is\s+now\s+clear|it\s+is\s+(clear|obvious))\b',
    ]

    # Порогові значення для нового патерну
    # Потребує ОБОХ: speculation + fact markers (ковзання)
    # АБО confidence inflation (самостійно)
    CONFLATION_SPECULATION_THRESHOLD = 2
    CONFLATION_FACT_THRESHOLD = 2
    CONFLATION_INFLATION_THRESHOLD = 1

    # Threshold: how many hits trigger each pattern
    ANON_THRESHOLD = 1
    CORR_THRESHOLD = 1
    UNFALS_THRESHOLD = 1
    LEAP_THRESHOLD = 1
    UNVERIFIED_CITE_THRESHOLD = 1

    def analyze(self, text: str, genre: str = 'UNKNOWN') -> EpistemologyResult:
        if not text or len(text.strip()) < 50:
            return EpistemologyResult(
                score=0.0,
                verdict='N/A',
                is_epistemic_content=False
            )

        t = text.lower()

        # Journalistic Shield
        is_journalistic_genre = genre in self.JOURNALISTIC_GENRES
        if is_journalistic_genre:
            anon_patterns = self.ANON_PATTERNS_UK + self.ANON_PATTERNS_EN_PSEUDO
        else:
            anon_patterns = (self.ANON_PATTERNS_UK +
                             self.ANON_PATTERNS_EN_PSEUDO +
                             self.ANON_PATTERNS_EN_JOURNALISTIC)

        # Count hits per pattern group
        anon_hits        = self._count_hits(t, anon_patterns)
        corr_hits        = self._count_hits(t, self.CORR_PATTERNS_UK + self.CORR_PATTERNS_EN)
        unfals_hits      = self._count_hits(t, self.UNFALS_PATTERNS_UK + self.UNFALS_PATTERNS_EN)
        leap_hits        = self._count_hits(t, self.LEAP_PATTERNS_UK + self.LEAP_PATTERNS_EN)
        unverified_hits  = self._count_hits(t, self.UNVERIFIED_CITE_PATTERNS_UK + self.UNVERIFIED_CITE_PATTERNS_EN)

        # ── Pattern 6: Epistemic Conflation ──────────────────────────
        speculation_hits = self._count_hits(t, self.SPECULATION_MARKERS_UK + self.SPECULATION_MARKERS_EN)
        fact_hits        = self._count_hits(t, self.FACT_MARKERS_UK + self.FACT_MARKERS_EN)
        inflation_hits   = self._count_hits(t, self.CONFIDENCE_INFLATION_UK + self.CONFIDENCE_INFLATION_EN)

        # Shield: наукові тексти легітимно мають і "may" і "confirmed" — це норма
        # Shield: журналістські репортажі мають факти — норма якщо немає speculation
        is_science_genre = genre in ('SCIENCE', 'ANALYTICS')
        if is_science_genre:
            # В наукових текстах fact markers = нормальна мова, не ковзання
            fact_hits = 0

        # Тригерить якщо:
        # a) є і speculation і fact markers — ковзання між рівнями
        # б) АБО confidence inflation (потребує 2+ hits — щоб уникнути FP)
        conflation_triggered = (
            (speculation_hits >= self.CONFLATION_SPECULATION_THRESHOLD and
             fact_hits >= self.CONFLATION_FACT_THRESHOLD)
            or inflation_hits >= 2
        )
        conflation_hits = speculation_hits + fact_hits + inflation_hits

        pattern_hits = {
            'anonymous_authority':    anon_hits,
            'correlation_causation':  corr_hits,
            'unfalsifiable':          unfals_hits,
            'conclusion_leap':        leap_hits,
            'unverified_citation':    unverified_hits,
            'epistemic_conflation':   conflation_hits,
            '_conflation_detail': {
                'speculation': speculation_hits,
                'fact':        fact_hits,
                'inflation':   inflation_hits,
            },
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

        if conflation_triggered:
            triggered.append('EPISTEMIC_CONFLATION')
            red_flags.append(f'epistemic_conflation:spec={speculation_hits},fact={fact_hits},infl={inflation_hits}')
            missing.append('clear markers distinguishing speculation from verified facts')
            if inflation_hits >= self.CONFLATION_INFLATION_THRESHOLD:
                evidence.append(
                    'Text inflates confidence without new evidence: weak claims ("some analysts") '
                    'escalate to strong assertions ("clearly", "effectively") within the same text'
                )
            else:
                evidence.append(
                    f'Text mixes speculation markers ({speculation_hits} hits: "may", "could", "scenario") '
                    f'with fact markers ({fact_hits} hits: "confirmed", "deployed", "satellite images") '
                    'without clear epistemic transitions — reader may mistake forecasts for established facts'
                )

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
            'ANONYMOUS_AUTHORITY':   0.30,
            'CORRELATION_CAUSATION': 0.30,
            'UNFALSIFIABLE':         0.35,
            'CONCLUSION_LEAP':       0.35,
            'UNVERIFIED_CITATION':   0.25,
            'EPISTEMIC_CONFLATION':  0.35,
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
