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


def score_preemptive_monopoly(text: str) -> dict:
    text_low = text.lower()
    present = {}
    for slot_name, patterns in SLOTS.items():
        for p in patterns:
            m = re.search(p, text_low, re.IGNORECASE | re.DOTALL)
            if m:
                present[slot_name] = m.group(0)[:80]
                break

    n_slots = len(present)
    if n_slots < MIN_SLOTS:
        return {
            'score': 0.0,
            'slots_present': list(present.keys()),
            'n_slots': n_slots,
            'examples': present,
        }

    score = min(1.0, SCORE_PER_SLOT * n_slots)
    return {
        'score': round(score, 2),
        'slots_present': list(present.keys()),
        'n_slots': n_slots,
        'examples': present,
    }
