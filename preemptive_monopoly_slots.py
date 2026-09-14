"""
Slot-based heuristic scorer for PREEMPTIVE_MONOPOLY.
Замість одного regex, що має матчити всю конструкцію одразу,
розбиваємо прийом на структурні "слоти" (незалежні смислові
елементи риторики) і рахуємо score за кількістю присутніх слотів
у тексті — стійкіше до перефразування, ніж жорсткий AND-ланцюжок.

Слоти (кожен = список коренів/лем, UK+EN разом):
  A. self_exclusivity — "тільки/лише ми/наша команда/організація..."
  B. worse_alternative — порівняння з гіршою/небезпечнішою альтернативою
  C. necessity_framing — "необхідність, не привілей" / вимушені / змушені
  D. unique_capability — унікальна інфраструктура/спроможність/гарантія
  E. if_not_us_then_who — риторичне "якщо не ми, то хто"

score = (score_per_slot) * (кількість присутніх слотів), капується на 1.0
min_slots — поріг, нижче якого взагалі не рахуємо (уникнення
одного випадкового слова, що саме по собі нічого не означає)

SELF_DOCUMENTATION_CONTEXT guard (14.09.2026, доданий за прецедентом з
self_preservation.py/self_reference_detector.py — той самий клас
фолспозитиву: власний текст, що ОПИСУЄ/НАЗИВАЄ прийом як об'єкт
дослідження, а не ЗАСТОСОВУЄ його, ловився як маніпуляція, бо містить
той самий словник з причин, іманентних жанру опису). Знайдено емпірично:
стаття про сам цей детектор отримала score=1.0/5 слотів — усі п'ять
збігів виявились цитатами-прикладами чи назвами слотів усередині
власного опису архітектури, жоден не був реальним твердженням-маніпуляцією.
Два незалежні сигнали "це метарівень, не пряме твердження":
  1. збіг безпосередньо всередині лапок (пряма цитата-приклад)
  2. висока щільність метамовних маркерів (риторичн*, патерн*, приклад*,
     детектор*, слот*, цитат* тощо) в усьому тексті — ознака, що текст
     ПРО прийом, а не ІНСТАНЦІЯ прийому
"""

import re


SLOTS = {
    'self_exclusivity': [
        r'\b(тільки|лише)\s+(ми|наша команда|наша організація|організаці[ії])\b',
        r'\bonly\s+(we|us|our team|our organization|an organization)\b',
        r'\bsolely\s+(we|us|our)\b',
    ],
    'worse_alternative': [
        r'(менш\w*|гірш\w*)\s*(безпечн\w*|відповідальн\w*|обережн\w*|регульован\w*)',
        r'(неконтрольован\w*|хаотичн\w*|безконтрольн\w*)\s*(поширенн\w*|проліферац\w*|розповсюдженн\w*)',
        r'(less\s+(safe|responsible|careful|regulated)|worse|more dangerous)',
        r'(uncontrolled|chaotic)\s+(proliferation|spread)',
    ],
    'necessity_framing': [
        r'(необхідніст\w*|вимушен\w*|змушен\w*)',
        r'не\s+привіле\w*',
        r'(necessity|forced to|compelled to)',
        r'not\s+a\s+privilege',
    ],
    'unique_capability': [
        r'(тільки|лише)\s+(ми|наша команда)\s+.{0,60}(маємо|можемо|здатн\w*|спроможн\w*)',
        r'(унікальн\w*|єдин\w*)\s+(інфраструктур\w*|спроможніст\w*|можливост\w*)',
        r'(only|solely)\s+(we|our team)\s+.{0,60}(have|can|are able|capable)',
        r'(unique|only)\s+(infrastructure|capability|capacity)',
    ],
    'if_not_us_then_who': [
        r'якщо не (ми|наша команда).{1,60}то.{0,20}хто',
        r'if not (us|we).{1,60}(then\s+)?who',
    ],
}

SCORE_PER_SLOT = 0.20   # 5 слотів * 0.20 = 1.0 стеля при повному наборі
MIN_SLOTS = 2           # менше 2 слотів — це просто шум, не рахуємо

# ── SELF_DOCUMENTATION_CONTEXT guard ───────────────────────────────────
QUOTE_CHARS = '«»"\'`“”‘’'

META_MARKERS = [
    r'риторичн\w*', r'прийом\w*', r'патерн\w*', r'маркер\w*', r'конструкці\w*',
    r'формулюванн\w*', r'цитат\w*', r'приклад\w*', r'детектор\w*', r'слот\w*',
    r'ілюстраці\w*', r'наприклад', r'\bregex\b', r'\bscorer\b',
]
META_DENSITY_THRESHOLD = 3   # мінімум РІЗНИХ метамаркерів для спрацювання guard'у
SELF_DOC_DISCOUNT = 0.15     # той самий коефіцієнт, що вже прийнятий в проєкті
                              # (self_preservation.py SELF_DOCUMENTATION_CONTEXT)


def _is_quoted(text_low: str, start: int, end: int) -> bool:
    """Чи стоїть збіг безпосередньо в лапках (пряма цитата-приклад,
    не власне твердження автора)."""
    before = text_low[max(0, start - 2):start]
    after = text_low[end:end + 2]
    return any(c in QUOTE_CHARS for c in before) or any(c in QUOTE_CHARS for c in after)


def _meta_density(text_low: str) -> int:
    """Кількість РІЗНИХ метамовних маркерів у тексті — сигнал, що текст
    ОПИСУЄ прийом (документація/аналіз), а не ЗАСТОСОВУЄ його."""
    return sum(1 for p in META_MARKERS if re.search(p, text_low, re.IGNORECASE))


def score_preemptive_monopoly(text: str) -> dict:
    text_low = text.lower()
    present = {}
    quoted_out = []
    for slot_name, patterns in SLOTS.items():
        for p in patterns:
            m = re.search(p, text_low, re.IGNORECASE | re.DOTALL)
            if m:
                if _is_quoted(text_low, m.start(), m.end()):
                    quoted_out.append(slot_name)  # зафіксовано, але не рахується
                    continue
                present[slot_name] = m.group(0)[:80]
                break

    n_slots = len(present)
    if n_slots < MIN_SLOTS:
        return {
            'score': 0.0,
            'slots_present': list(present.keys()),
            'n_slots': n_slots,
            'examples': present,
            'quoted_excluded': quoted_out,
            'self_documentation_context': False,
        }

    score = min(1.0, SCORE_PER_SLOT * n_slots)

    meta_count = _meta_density(text_low)
    self_doc = meta_count >= META_DENSITY_THRESHOLD
    if self_doc:
        score = round(score * SELF_DOC_DISCOUNT, 3)

    return {
        'score': round(score, 3),
        'slots_present': list(present.keys()),
        'n_slots': n_slots,
        'examples': present,
        'quoted_excluded': quoted_out,
        'self_documentation_context': self_doc,
        'meta_marker_count': meta_count,
    }
