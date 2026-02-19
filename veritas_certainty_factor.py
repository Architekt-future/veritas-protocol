"""
Veritas Certainty Factor v1.0
Philosophy: "A short text is not a clean text. It is an unread text."

Two responsibilities:
1. ADVISORY: Flag texts where length makes confident verdict impossible
2. DYNAMIC THRESHOLD: Return adjusted min_hits for short-text mode
   so critical modules (SelfPreservation, MetaIntent) still catch attacks

Thresholds:
  < 20 words  → INSUFFICIENT  (verdict unreliable)
  20-50 words → LOW_SAMPLE    (verdict possible but uncertain)
  50-150 words → MODERATE     (standard analysis applies)
  150+ words  → SUFFICIENT    (full confidence)
"""

from typing import Dict


class CertaintyFactor:

    # Word count thresholds
    INSUFFICIENT  = 20
    LOW_SAMPLE    = 50
    MODERATE      = 150

    def __init__(self):
        pass

    def analyze(self, text: str) -> Dict:
        words = len(text.split())
        chars = len(text)

        if words < self.INSUFFICIENT:
            level    = 'INSUFFICIENT'
            label_uk = 'НЕДОСТАТНЬО ДАНИХ'
            label_en = 'INSUFFICIENT DATA'
            note_uk  = (f'Текст містить лише {words} слів. '
                        'Свідок не може формувати надійний вердикт на такому обсязі. '
                        'Результат є орієнтовним.')
            note_en  = (f'Text contains only {words} words. '
                        'The Witness cannot form a reliable verdict on this volume. '
                        'Result is indicative only.')
            # Lower min_hits for critical modules
            short_text_mode   = True
            adjusted_min_hits = 1
            entropy_floor     = 0.15  # minimum entropy for very short texts

        elif words < self.LOW_SAMPLE:
            level    = 'LOW_SAMPLE'
            label_uk = 'МАЛИЙ ОБСЯГ'
            label_en = 'LOW SAMPLE'
            note_uk  = (f'Текст містить {words} слів. '
                        'Аналіз можливий, але точність знижена через малий обсяг.')
            note_en  = (f'Text contains {words} words. '
                        'Analysis possible but accuracy reduced due to small volume.')
            short_text_mode   = True
            adjusted_min_hits = 1
            entropy_floor     = 0.10

        elif words < self.MODERATE:
            level    = 'MODERATE'
            label_uk = 'ПОМІРНИЙ ОБСЯГ'
            label_en = 'MODERATE SAMPLE'
            note_uk  = f'Текст містить {words} слів. Стандартний аналіз.'
            note_en  = f'Text contains {words} words. Standard analysis.'
            short_text_mode   = False
            adjusted_min_hits = None  # use module defaults
            entropy_floor     = 0.0

        else:
            level    = 'SUFFICIENT'
            label_uk = 'ДОСТАТНІЙ ОБСЯГ'
            label_en = 'SUFFICIENT SAMPLE'
            note_uk  = f'Текст містить {words} слів. Повний аналіз.'
            note_en  = f'Text contains {words} words. Full analysis.'
            short_text_mode   = False
            adjusted_min_hits = None
            entropy_floor     = 0.0

        return {
            'word_count':        words,
            'char_count':        chars,
            'certainty_level':   level,
            'certainty_label_uk': label_uk,
            'certainty_label_en': label_en,
            'certainty_note_uk': note_uk,
            'certainty_note_en': note_en,
            'short_text_mode':   short_text_mode,
            'adjusted_min_hits': adjusted_min_hits,
            'entropy_floor':     entropy_floor,
        }
