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


class LaunderedClaimDetector:
    """
    Детектор відмивання тверджень через медіа-трансляцію.
    """

    # Джерела що є сторонами конфліктів / зацікавленими сторонами
    CONFLICT_SOURCES_UK = [
        'кремль', 'путін', 'пєсков', 'лавров', 'медведєв', 'захарова',
        'міноборони росії', 'міноборони рф', 'генштаб росії',
        'офіс президента росії', 'держдума',
        'хамас', 'хезболла', 'талібан',
        'представник компанії', 'прес-служба компанії',
        'речник', 'представник сторони',
    ]
    CONFLICT_SOURCES_EN = [
        'kremlin', 'putin', 'peskov', 'lavrov', 'medvedev', 'zakharova',
        'russian defense ministry', 'russian mod', 'russian general staff',
        'hamas', 'hezbollah', 'taliban',
        'company spokesperson', 'press office',
        'spokesman', 'spokeswoman',
    ]

    # Маркери що перетворюють думку на факт (відсутність яких = проблема)
    ATTRIBUTION_MARKERS_UK = [
        'на думку', 'за словами', 'за твердженням', 'як заявив',
        'як стверджує', 'на переконання', 'як вважає', 'на погляд',
        'за оцінкою', 'як повідомив', 'посилаючись на', 'цитує',
        'за версією', 'на його думку', 'на її думку', 'повідомляє',
    ]
    ATTRIBUTION_MARKERS_EN = [
        'according to', 'as stated by', 'as claimed by', 'in the view of',
        'in the opinion of', 'as argued by', 'as reported by', 'citing',
        'per', 'sources say', 'he said', 'she said', 'they said',
    ]

    # Сильні фактичні конструкції — ознака відмивання
    FACT_FRAMING_UK = [
        r'(право|закон|система|порядок)\s+(припинив|перестав|зник|більше не існує|фактично не існує)',
        r'фактично (припинив|перестав|не існує|зник)',
        r'де-факто (не існує|припинив|зник)',
        r'(світ|країна|економіка)\s+(опинився|перейшла|втратила)',
        r'насправді (вже|більше|фактично)',
        r'правовий вакуум',
        r'кінець (міжнародного|світового|правового)',
    ]
    FACT_FRAMING_EN = [
        r'(law|order|system)\s+(no longer exists|ceased to exist|is dead|has collapsed)',
        r'de facto (no longer|ceased|gone)',
        r'(world|country|economy)\s+(finds itself|has lost|collapsed)',
        r'legal vacuum',
        r'end of (international|world|legal)',
    ]

    # Заголовкові патерни без атрибуції
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
        return 'uk' if uk_chars > 3 else 'en'

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
            attr_markers = self._attr_uk if lang == 'uk' else self._attr_en
            attr_count = sum(1 for m in attr_markers if m in text_lower)

            if attr_count == 0:
                signals.append(f'Фактична конструкція без атрибуції: «{fact_hits[0]}»')
                score += 0.20
            elif attr_count < len(fact_hits):
                signals.append(f'Недостатня атрибуція для {len(fact_hits)} тверджень')
                score += 0.10

        # ── СИГНАЛ 3: Низька щільність маркерів думки ────────────────────────
        attr_markers = self._attr_uk if lang == 'uk' else self._attr_en
        attr_density = sum(1 for m in attr_markers if m in text_lower)
        words = len(text.split())

        # Якщо джерело є стороною, але маркерів мало
        if found_sources and attr_density < 2 and words > 100:
            signals.append('Низька щільність маркерів думки при зацікавленому джерелі')
            score += 0.10

        # ── СИГНАЛ 4: Заголовок без лапок ────────────────────────────────────
        first_line = text.split('\n')[0][:200]
        if lang == 'uk':
            for pat in self.HEADLINE_NO_ATTRIBUTION_UK:
                if re.search(pat, first_line):
                    # Перевіряємо чи є лапки в заголовку
                    if '«' not in first_line and '"' not in first_line and "'" not in first_line:
                        signals.append('Заголовок відтворює твердження без лапок')
                        score += 0.10
                    break

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
        return result
