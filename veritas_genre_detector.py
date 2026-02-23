"""
Veritas Genre Detector v1.0
Detects text genre to apply appropriate analysis calibration.

Genres:
  ANALYTICS  — multi-source, hedged claims, expert opinions
  REPORT     — factual, single event, who/what/where/when
  OPINION    — first person, subjective, persuasive
  SATIRE     — irony, hyperbole, humor signals
  UNKNOWN    — insufficient signals

Each genre returns calibration hints for the core engine.
"""

import re
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class GenreResult:
    genre: str
    confidence: float  # 0.0-1.0
    signals: Dict[str, int]
    calibration: Dict[str, float]


class GenreDetector:

    # ── Signal patterns ──────────────────────────────────────────────

    ANALYTICS_SIGNALS = [
        r'\bвважають\b', r'\bне виключають\b', r'\bза оцінками\b',
        r'\bаналітики\b', r'\bексперти\b', r'\bзазначають\b',
        r'\bрозглядається\b', r'\bімовірно\b', r'\bнібито\b',
        r'\bповідомляється\b', r'\bочікується\b', r'\bза словами\b',
        r'\bconsider\b', r'\banalysts\b', r'\baccording to\b',
        r'\bexperts say\b', r'\bappear to\b', r'\bsuggests\b',
        r'\bза даними\b', r'\bдже рела свідчать\b', r'\bна думку\b',
    ]

    REPORT_SIGNALS = [
        r'\bзатримали\b', r'\bповідомив\b', r'\bзаявив\b', r'\bвідбулось\b',
        r'\bсталось\b', r'\bзагинули\b', r'\bпоранені\b', r'\bарештували\b',
        r'\bвибухи\b', r'\bнапад\b', r'\bоперація\b', r'\bнаступ\b',
        r'\bреported\b', r'\bannounced\b', r'\bconfirmed\b', r'\barrested\b',
        r'\bо \d{1,2}:\d{2}\b',  # time stamp
        r'\b\d{1,2} \w+ \d{4}\b',  # date
    ]

    OPINION_SIGNALS = [
        r'\bя вважаю\b', r'\bна мою думку\b', r'\bмені здається\b',
        r'\bпереконаний\b', r'\bмоя позиція\b', r'\bавтор вважає\b',
        r'\bI believe\b', r'\bIn my opinion\b', r'\bI think\b',
        r'\bмусимо визнати\b', r'\bочевидно що\b', r'\bбезсумнівно\b',
    ]

    SATIRE_SIGNALS = [
        r'\bнібито\b.*\bзнову\b', r'\bгеніальний план\b',
        r'\bтрадиційно\b.*\bзвинувачують\b',
        r'\bексперти.*одностайні\b', r'\bнесподівано з\'ясувалось\b',
        r'\bofficial sources confirm\b.*\bsurprisingly\b',
    ]

    # ── Calibration presets ──────────────────────────────────────────

    CALIBRATION = {
        'ANALYTICS': {
            'absurdity_weight':   0.0,   # geopolitical metaphors ≠ absurdity
            'anon_authority':     False,  # "аналітики вважають" is expected
            'unanchored_claim':   False,  # hedged claims are genre norm
            'entropy_damper':     False,  # don't suppress entropy
            'entropy_cap':        0.85,
        },
        'REPORT': {
            'absurdity_weight':   1.8,
            'anon_authority':     True,
            'unanchored_claim':   True,
            'entropy_damper':     True,
            'entropy_cap':        1.0,
        },
        'OPINION': {
            'absurdity_weight':   1.0,
            'anon_authority':     False,  # subjective by design
            'unanchored_claim':   False,
            'entropy_damper':     True,
            'entropy_cap':        1.0,
        },
        'SATIRE': {
            'absurdity_weight':   0.0,   # irony ≠ absurdity
            'anon_authority':     False,
            'unanchored_claim':   False,
            'entropy_damper':     False,
            'entropy_cap':        0.90,
        },
        'UNKNOWN': {
            'absurdity_weight':   1.8,
            'anon_authority':     True,
            'unanchored_claim':   True,
            'entropy_damper':     True,
            'entropy_cap':        1.0,
        },
    }

    # ── Verdict labels ───────────────────────────────────────────────

    CLEAN_VERDICT = {
        'ANALYTICS': ('VERIFIED', 'АНАЛІТИЧНА СТРУКТУРОВАНІСТЬ',
                      'Текст демонструє ознаки аналітичного жанру: множинні джерела, '
                      'хеджовані твердження, структурована аргументація'),
        'OPINION':   ('VERIFIED', 'АВТОРСЬКА ПОЗИЦІЯ',
                      'Текст є вираженням суб\'єктивної думки; оцінюйте аргументи, '
                      'а не факти'),
        'SATIRE':    ('VERIFIED', 'САТИРИЧНИЙ КОНТЕНТ',
                      'Виявлено ознаки сатири або іронії; буквальна інтерпретація '
                      'може бути хибною'),
    }

    # ────────────────────────────────────────────────────────────────

    def analyze(self, text: str) -> GenreResult:
        t = text.lower()

        analytics = sum(1 for p in self.ANALYTICS_SIGNALS if re.search(p, t, re.I))
        report    = sum(1 for p in self.REPORT_SIGNALS    if re.search(p, t, re.I))
        opinion   = sum(1 for p in self.OPINION_SIGNALS   if re.search(p, t, re.I))
        satire    = sum(1 for p in self.SATIRE_SIGNALS    if re.search(p, t, re.I))

        signals = {
            'analytics': analytics,
            'report':    report,
            'opinion':   opinion,
            'satire':    satire,
        }

        # Thresholds
        if satire >= 2:
            genre, conf = 'SATIRE',    min(satire / 4, 1.0)
        elif opinion >= 2 and opinion > analytics:
            genre, conf = 'OPINION',   min(opinion / 4, 1.0)
        elif analytics >= 2:
            genre, conf = 'ANALYTICS', min(analytics / 8, 1.0)
        elif report >= 2:
            genre, conf = 'REPORT',    min(report / 8, 1.0)
        else:
            genre, conf = 'UNKNOWN',   0.0

        return GenreResult(
            genre=genre,
            confidence=round(conf, 2),
            signals=signals,
            calibration=self.CALIBRATION[genre],
        )


if __name__ == '__main__':
    d = GenreDetector()

    tests = [
        ('TSN Аналітика', 'Аналітики вважають що Пекін дедалі більше виступає у ролі старшого партнера. Експерти не виключають що Китай не очікував такого масштабу війни. За оцінками ЄС Китай забезпечує до 80 відсотків компонентів.'),
        ('rbc Репортаж',  'Правоохоронці затримали ймовірну виконавицю двох вибухів. Жінку було затримано в районному центрі. Міністр повідомив що серед постраждалих є цивільні.'),
        ('Думка',         'Я вважаю що Україна мусить визнати реальність. На мою думку переговори неминучі. Переконаний що час діяти.'),
    ]

    for name, text in tests:
        r = d.analyze(text)
        print(f'{name}: {r.genre} (conf={r.confidence}, signals={r.signals})')
