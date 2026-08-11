"""
Veritas — LAUNDERED_CLAIM Detector v1.0
========================================
Патерн: заява зацікавленої сторони подається як опис реальності.
"Розтин показав що пацієнт помер від розтину" — коли суб'єкт конфлікту
оголошує факти про реальність через власні слова, а медіа транслює це
без маркування як позицію.

Класичні форми:
  - Пєсков каже "права немає" → заголовок "міжнародне право припинило існування"
  - Кремль заявляє "Україна атакувала" → "Україна атакувала"
  - Компанія каже "продукт безпечний" → "продукт безпечний"

SIGNALS:
  1. Джерело є стороною конфлікту (агресор, відповідач, зацікавлена сторона)
  2. Заява подана як факт про зовнішню реальність, не як думка
  3. Відсутнє або слабке маркування авторства твердження
  4. Заголовок або лід відтворює твердження без лапок / атрибуції

PENALTY: epistemic 0.20–0.35 (залежно від кількості сигналів)
"""

import re
from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class LaunderedClaimResult:
    score: float = 0.0
    verdict: str = 'CLEAN'
    signals: List[str] = field(default_factory=list)
    explanation: str = ''
    is_flagged: bool = False
    # Незалежно від фінального score/verdict: чи є в тексті сторона активного
    # конфлікту серед цитованих джерел. Це не ознака маніпуляції сама по собі
    # (атрибуція може бути бездоганною) — а окремий, нейтральний контекстний
    # факт, вартий показу читачеві незалежно від manipulation-скору.
    conflict_sources: List[str] = field(default_factory=list)


class LaunderedClaimDetector:
    """
    Детектор відмивання тверджень через медіа-трансляцію.
    """

    # Джерела що є сторонами конфліктів / зацікавленими сторонами
    CONFLICT_SOURCES_UK = [
        # Російські державні актори
        'кремль', 'путін', 'пєсков', 'лавров', 'медведєв', 'захарова',
        'міноборони росії', 'міноборони рф', 'генштаб росії',
        'офіс президента росії', 'держдума', 'мзс росії',
        # Інші державні актори конфліктів
        'іранське міністерство', 'тегеран заявив', 'пхеньян',
        'північна корея', 'китайський мзс', 'режим асада',
        # Недержавні актори
        'хамас', 'хезболла', 'талібан', 'іділ', 'вагнер',
        # Корпоративні зацікавлені сторони
        'представник компанії', 'прес-служба компанії',
        'речник', 'представник сторони', 'виробник заявив',
        'прес-служба', 'прес-секретар',
    ]
    CONFLICT_SOURCES_EN = [
        # Russian state actors
        'kremlin', 'putin', 'peskov', 'lavrov', 'medvedev', 'zakharova',
        'russian defense ministry', 'russian mod', 'russian general staff',
        'state duma', 'russian foreign ministry',
        # Other state conflict actors
        'iranian foreign ministry', 'tehran said', 'pyongyang',
        'north korea', 'chinese foreign ministry', 'beijing spokesperson',
        'syrian government', 'venezuelan government',
        # Non-state conflict actors
        'hamas', 'hezbollah', 'taliban', 'isis', 'wagner group',
        # Corporate interested parties
        'company spokesperson', 'press office', 'spokesman', 'spokeswoman',
        'the manufacturer said', 'the developer said',
        'a company representative',
    ]

    # Маркери що перетворюють думку на факт (відсутність яких = проблема)
    ATTRIBUTION_MARKERS_UK = [
        'на думку', 'за словами', 'за твердженням', 'як заявив',
        'як стверджує', 'на переконання', 'як вважає', 'на погляд',
        'за оцінкою', 'як повідомив', 'посилаючись на', 'цитує',
        'за версією', 'на його думку', 'на її думку', 'повідомляє',
        'нібито', 'заяв',  # "нібито" — найпоширеніший укр. маркер дистанціювання;
        # "заяв" — стем, що покриває "заявив/заявила/заявили/заявляє" без "як" спереду
        # (голе "Х заявив, що Y" — типова атрибуція, не менш валідна за "як заявив")
    ]
    ATTRIBUTION_MARKERS_EN = [
        'according to', 'as stated by', 'as claimed by', 'in the view of',
        'in the opinion of', 'as argued by', 'as reported by', 'citing',
        'sources say', 'he said', 'she said', 'they said',
    ]
    # 'per' потребує word-boundary matching (substring 'in' ловить його
    # всередині 'experiment', 'reported', 'period' тощо) — окремий regex-набір
    ATTRIBUTION_MARKERS_REGEX_EN = [
        r'\bper\b',
    ]

    # Сильні фактичні конструкції — ознака відмивання
    FACT_FRAMING_UK = [
        r'\b(право|закон|система|порядок)\s+(припинив|перестав|зник|більше не існує|фактично не існує)',
        r'\bфактично (припинив|перестав|не існує|зник)',
        r'\bде-факто (не існує|припинив|зник)',
        r'\b(світ|країна|економіка)\s+(опинився|перейшла|втратила)',
        r'\bнасправді (вже|більше|фактично)',
        r'\bправовий вакуум',
        r'\bкінець (міжнародного|світового|правового)',
    ]
    FACT_FRAMING_EN = [
        # Systemic collapse framing
        r'\b(law|order|system)\s+(no longer exists|ceased to exist|is dead|has collapsed)',
        r'\bde facto (no longer|ceased|gone)',
        r'\b(world|country|economy)\s+(finds itself|has lost|collapsed)',
        r'\blegal vacuum',
        r'\bend of (international|world|legal)',
        # Corporate safety laundering
        r'\b(product|drug|vaccine|treatment)\s+is\s+(completely\s+)?(safe|effective|proven)',
        r'\b(meets|exceeds)\s+all\s+(safety|regulatory|quality)\s+standards',
        r'\bno (side effects|risks|dangers|concerns)',
        r'\b(fully|thoroughly|extensively)\s+(tested|vetted|approved)',
        r'\b(our|the)\s+(research|data|studies)\s+(show|confirm|prove)',
        # Political self-serving absolutes
        r'\b(we have|there is)\s+no (choice|option|alternative)\s+but to',
        r'\b(forced|compelled|had no choice)\s+to\s+(respond|attack|retaliate)',
        r'\b(provoked|started|initiated)\s+by\s+(them|ukraine|the west|nato)',
        r'\b(justified|legitimate|necessary)\s+(response|action|strike)',
    ]

    # Заголовкові патерни без атрибуції — EN
    HEADLINE_NO_ATTRIBUTION_EN = [
        r'^[A-Z][^:"]{10,}(has collapsed|no longer exists|is dead|is over)',
        r'^(Russia|Iran|China|Hamas):\s',
        r'^[A-Z][^:"]{5,}(forced to|had no choice|provoked)',
        r'^(Mystery|Shocking|Explosive)\b',
    ]

    # Заголовкові патерни без атрибуції — UK
    HEADLINE_NO_ATTRIBUTION_UK = [
        r'^[А-ЯІЇЄ][^:«»"\']{10,}(припинив|зник|колапс|криза|кінець|вакуум)',
        r'^У (кремлі|москві|пекіні|тегерані).{0,20}(заявили|повідомили|стверджують)',
    ]

    def __init__(self):
        self._attr_uk = [p.lower() for p in self.ATTRIBUTION_MARKERS_UK]
        self._attr_en = [p.lower() for p in self.ATTRIBUTION_MARKERS_EN]
        self._src_uk  = [s.lower() for s in self.CONFLICT_SOURCES_UK]
        self._src_en  = [s.lower() for s in self.CONFLICT_SOURCES_EN]

    def _detect_lang(self, text: str) -> str:
        uk_chars = len(re.findall(r'[іїєІЇЄ]', text))
        # Threshold пропорційний довжині — для коротких текстів достатньо 2 символів
        threshold = max(2, min(5, len(text) // 200))
        return 'uk' if uk_chars >= threshold else 'en'

    def _count_attr_markers(self, text_lower: str, lang: str) -> int:
        """Рахує маркери атрибуції. EN-маркери типу 'per' перевіряються
        через \\b-regex, а не substring-check, щоб не ловитись усередині
        'experiment', 'reported', 'period' тощо."""
        markers = self._attr_uk if lang == 'uk' else self._attr_en
        count = sum(1 for m in markers if m in text_lower)
        if lang == 'en':
            count += sum(1 for p in self.ATTRIBUTION_MARKERS_REGEX_EN
                        if re.search(p, text_lower))
        return count

    def analyze(self, text: str) -> LaunderedClaimResult:
        result = LaunderedClaimResult()
        if not text or len(text) < 50:
            return result

        text_lower = text.lower()
        lang = self._detect_lang(text)
        signals = []
        score = 0.0

        # ── СИГНАЛ 1: Джерело є стороною конфлікту ───────────────────────────
        sources = self._src_uk if lang == 'uk' else self._src_en
        found_sources = [s for s in sources if s in text_lower]
        if found_sources:
            signals.append(f'Джерело — сторона конфлікту: {", ".join(found_sources[:2])}')
            score += 0.15

        # ── СИГНАЛ 2: Фактичні конструкції без маркування ────────────────────
        fact_patterns = self.FACT_FRAMING_UK if lang == 'uk' else self.FACT_FRAMING_EN
        fact_hits = []
        for pattern in fact_patterns:
            m = re.search(pattern, text_lower)
            if m:
                fact_hits.append(m.group(0)[:40])

        if fact_hits:
            # Перевіряємо чи є атрибуція поруч
            attr_count = self._count_attr_markers(text_lower, lang)

            if attr_count == 0:
                signals.append(f'Фактична конструкція без атрибуції: «{fact_hits[0]}»')
                score += 0.20
            elif attr_count < len(fact_hits):
                signals.append(f'Недостатня атрибуція для {len(fact_hits)} тверджень')
                score += 0.10

        # ── СИГНАЛ 3: Низька щільність маркерів думки ────────────────────────
        attr_density = self._count_attr_markers(text_lower, lang)
        words = len(text.split())

        # Якщо джерело є стороною, але маркерів мало
        if found_sources and attr_density < 2 and words > 100:
            signals.append('Низька щільність маркерів думки при зацікавленому джерелі')
            score += 0.10

        # ── СИГНАЛ 4: Заголовок без лапок ────────────────────────────────────
        first_line = text.split('\n')[0][:200]
        headline_patterns = (self.HEADLINE_NO_ATTRIBUTION_UK
                             if lang == 'uk'
                             else self.HEADLINE_NO_ATTRIBUTION_EN)
        for pat in headline_patterns:
            if re.search(pat, first_line):
                no_quotes = ('«' not in first_line and '"' not in first_line
                             and "'" not in first_line and '"' not in first_line)
                if no_quotes:
                    signals.append('Заголовок відтворює твердження без лапок/атрибуції')
                    score += 0.10
                break

        # ── СИГНАЛ 5: Корпоративне/державне відмивання ───────────────────────
        # Якщо джерело є стороною І використовує абсолютні фактичні конструкції
        if found_sources and fact_hits:
            absolute_patterns = [
                r'\b(completely|absolutely|totally|entirely)\s+(safe|effective|proven)\b',
                r'\b(no|zero)\s+(risk|danger|side effect)\b',
                r'\b(forced|had no choice|no alternative)\b',
                r'\b(provoked|started|initiated)\s+by\b',
            ]
            absolute_hits = sum(1 for p in absolute_patterns
                                if re.search(p, text_lower, re.IGNORECASE))
            if absolute_hits >= 1:
                signals.append('Абсолютні твердження від зацікавленої сторони')
                score += 0.15

        # ── ПІДСУМОК ──────────────────────────────────────────────────────────
        score = min(score, 0.70)  # cap

        if score >= 0.35:
            verdict = 'LAUNDERED_CLAIM'
            explanation = (
                'Заява зацікавленої сторони подається як факт про реальність. '
                'Читач отримує позицію однієї сторони конфлікту як об\'єктивний опис дійсності.'
            )
            result.is_flagged = True
        elif score >= 0.20:
            verdict = 'WEAK_ATTRIBUTION'
            explanation = (
                'Недостатнє маркування джерела твердження. '
                'Межа між фактом і позицією розмита.'
            )
            result.is_flagged = True
        else:
            verdict = 'CLEAN'
            explanation = ''

        result.score      = round(score, 3)
        result.verdict    = verdict
        result.signals    = signals
        result.explanation = explanation
        result.conflict_sources = found_sources
        return result
