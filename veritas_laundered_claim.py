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
    # (лишається як допоміжний, вже відомий сигнал — але більше не єдиний.
    #  Основний механізм тепер симетрична евристика нижче: сутність вважається
    #  "стороною конфлікту" не тому, що вона в цьому списку, а тому, що вона
    #  ОДНОЧАСНО (а) названа суб'єктом звинувачення/причетності в тексті,
    #  і (б) сама цитується як джерело коментаря про ту саму подію —
    #  незалежно від того, хто саме це: Кремль, Держдеп США чи корпорація.)
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

    # ── СИМЕТРИЧНА ЕВРИСТИКА: сутність причетна/звинувачена + сама цитується ─
    # Дієслова/конструкції, що роблять названу поруч сутність суб'єктом
    # звинувачення, причетності чи заперечення — незалежно від того, хто
    # саме названий. Працює однаково на "Кремль звинувачують у..." і
    # "Держдепартамент США звинувачують у...".
    ACCUSATION_OR_DENIAL_UK = [
        r'звинувачу\w+', r'звинувачен\w+\s+(у|в)', r'відповідальн\w+\s+за',
        r'причетн\w+\s+до', r'заперечу\w+\s+(причетність|звинувачення|провину)',
        r'спростову\w+\s+(звинувачення|заяви)', r'відкида\w+\s+звинувачення',
        r'напад\w*\s+.{1,20}\s+на', r'винн\w+\s+у',
    ]
    ACCUSATION_OR_DENIAL_EN = [
        r'accus\w+\s+of', r'blam\w+\s+for', r'responsible\s+for',
        r'involve\w*\s+in', r'den(?:y|ies|ied)\s+(?:involvement|responsibility|the\s+allegations)',
        r'reject\w*\s+(?:the\s+)?accusations', r'attack\s+(?:by|on)',
    ]

    # Груба евристика "іменованої сутності" — послідовність слів з великої
    # літери (включно з абревіатурами й багатослівними назвами на кшталт
    # "Держдепартамент США", "White House", "State Duma"). Не NER, тому
    # матиме і хибні спрацювання (початок речення), і пропуски — але це
    # симетрично криве в обидва боки, а не вибірково під один список країн.
    _ENTITY_NEAR_UK = re.compile(
        r'[А-ЯІЇЄA-Z][а-яіїєʼ\'\-a-zA-ZА-ЯІЇЄ]*(?:\s+[А-ЯІЇЄA-Z][а-яіїєʼ\'\-a-zA-ZА-ЯІЇЄ]*){0,3}'
    )
    _ENTITY_NEAR_EN = re.compile(r'[A-Z][a-zA-Z\'\-]*(?:\s+[A-Z][a-zA-Z\'\-]*){0,3}')

    def _nearest_entity(self, text: str, start: int, end: int, lang: str, window: int = 45) -> str:
        """Іменована сутність, найближча до збігу за абсолютною відстанню
        символів — незалежно від напрямку. Різні маркери мають різну типову
        граматичну спрямованість ('X accused of' — суб'єкт ПЕРЕД; 'according
        to X' — суб'єкт ПІСЛЯ), тому жорсткий пріоритет напрямку ламається на
        одному з двох класів; відстань — симетричний критерій для обох.
        ВАЖЛИВО: вікно "після" рахується від КІНЦЯ збігу (`end`), не від
        початку — інакше regex захоплює частину самого маркера як "сутність"
        (наприклад, 'According' на початку речення 'According to NATO...')."""
        entity_re = self._ENTITY_NEAR_UK if lang == 'uk' else self._ENTITY_NEAR_EN
        before = text[max(0, start - window):start]
        after  = text[end:end + window]

        # Не перетинаємо межу речення — інакше сутність з ПОПЕРЕДНЬОГО,
        # граматично непов'язаного речення може виявитись ближчою за raw-
        # відстанню символів, ніж справжній суб'єкт у поточному реченні.
        _sent_end = re.compile(r'[.!?]\s')
        _before_boundary = list(_sent_end.finditer(before))
        if _before_boundary:
            before = before[_before_boundary[-1].end():]
        _after_boundary = _sent_end.search(after)
        if _after_boundary:
            after = after[:_after_boundary.start()]

        candidates = []  # (відстань_до_збігу, текст_сутності)
        for m in entity_re.finditer(before):
            cand = m.group(0).strip()
            if len(cand) > 2:
                dist = len(before) - m.end()
                candidates.append((dist, cand))
        for m in entity_re.finditer(after):
            cand = m.group(0).strip()
            if len(cand) > 2:
                dist = m.start()
                candidates.append((dist, cand))

        if not candidates:
            return ''
        candidates.sort(key=lambda x: x[0])
        return candidates[0][1].lower()

    # Загальні іменники, які можуть опинитись з великої літери лише через
    # позицію на початку речення чи фрази — не частина власної назви,
    # навіть якщо граматично стоять поруч із нею ("Компанію Novatek" →
    # мала лишитись тільки "Novatek").
    _GENERIC_LEADING_WORDS_UK = {
        'компанію', 'компанія', 'компанії', 'фірму', 'фірма', 'фірми',
        'організацію', 'організація', 'уряд', 'влада', 'владу',
        'міністерство', 'відомство', 'речника', 'речниця', 'речник',
        'представника', 'представник', 'представниця', 'офіс',
    }
    _GENERIC_LEADING_WORDS_EN = {
        'the', 'a', 'an', 'company', 'firm', 'organization', 'government',
        'ministry', 'spokesperson', 'spokesman', 'spokeswoman',
        'representative', 'office',
    }

    @classmethod
    def _strip_generic_leading_words(cls, candidate: str, lang: str) -> str:
        """Прибирає провідні загальні іменники з багатослівного кандидата.
        'компанію novatek' -> 'novatek'; 'novatek' лишається без змін."""
        stoplist = cls._GENERIC_LEADING_WORDS_UK if lang == 'uk' else cls._GENERIC_LEADING_WORDS_EN
        words = candidate.split()
        while words and words[0].lower() in stoplist:
            words = words[1:]
        return ' '.join(words)

    @staticmethod
    def _normalize_entity(entity: str, prefix_len: int = 6) -> str:
        """Груба нормалізація для порівняння сутностей попри відмінкові форми
        ('Держдепартамент' / 'Держдепартаменту' — та сама сутність, різний
        відмінок). Без повного морфологічного аналізатора обрізаємо кожне
        слово до префікса — українські закінчення відмінків здебільшого
        короткі (1-3 символи), тому 6-символьний корінь зазвичай лишається
        спільним. Компроміс: короткі різні слова можуть хибно збігтись —
        прийнятно для advisory-сигналу, неприйнятно для остаточного вердикту."""
        return ' '.join(w[:prefix_len] for w in entity.split())

    def _find_self_interested_entities(self, text: str, text_lower: str, lang: str) -> list:
        """Симетрична евристика: сутність, яка одночасно (а) названа суб'єктом
        звинувачення/причетності і (б) сама цитується як джерело — незалежно
        від того, хто це. Заміна фіксованого списку "відомих поганих акторів"
        на структурний патерн, застосовний до будь-якої сторони."""
        accusation_patterns = self.ACCUSATION_OR_DENIAL_UK if lang == 'uk' else self.ACCUSATION_OR_DENIAL_EN
        attribution_markers = self._attr_uk if lang == 'uk' else self._attr_en

        accused_entities = {}   # нормалізована форма -> оригінал
        for pat in accusation_patterns:
            for m in re.finditer(pat, text_lower):
                ent = self._nearest_entity(text, m.start(), m.end(), lang)
                ent = self._strip_generic_leading_words(ent, lang)
                if ent:
                    accused_entities[self._normalize_entity(ent)] = ent

        quoted_entities = {}
        for marker in attribution_markers:
            for m in re.finditer(re.escape(marker), text_lower):
                ent = self._nearest_entity(text, m.start(), m.end(), lang)
                ent = self._strip_generic_leading_words(ent, lang)
                if ent:
                    quoted_entities[self._normalize_entity(ent)] = ent

        shared_keys = set(accused_entities) & set(quoted_entities)
        return sorted({accused_entities[k] for k in shared_keys})



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
        # Тепер два незалежні джерела сигналу, об'єднані:
        #  (a) симетрична евристика — сутність одночасно звинувачена/причетна
        #      І сама цитується, незалежно від того, хто це;
        #  (b) відомий список — ловить випадки, де звинувачення мовчазне чи
        #      загальновідоме (наприклад, "Кремль заявив" без explicit
        #      "звинувачують" поруч у цьому ж тексті).
        known_sources = self._src_uk if lang == 'uk' else self._src_en
        found_known = [s for s in known_sources if re.search(r'\b' + re.escape(s) + r'\b', text_lower)]
        found_heuristic = self._find_self_interested_entities(text, text_lower, lang)
        found_sources = sorted(set(found_known) | set(found_heuristic))
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
