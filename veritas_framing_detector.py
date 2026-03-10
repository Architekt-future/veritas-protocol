"""
Veritas Framing Detector — v1.0
Detects soft rhetorical manipulation that leaves no fingerprints:
  1. Agenda Setting    — "справжня проблема не X, а Y" (redirects attention)
  2. False Dilemma     — "або X, або Y" without acknowledging alternatives
  3. Ground Preparation — step-by-step nudge toward a conclusion without stating it
  4. Overton Shift     — normalizing a position by placing it between extremes
  5. Presupposition    — embedding unproven claim inside a neutral-sounding sentence

These patterns score 0 on void/absurdity/manipulation because they contain real words,
real structure, and no obvious lies — the manipulation is in the architecture.

Interface mirrors veritas_lac_epistemology.
"""

import re
from dataclasses import dataclass, field
from typing import List


@dataclass
class FramingResult:
    score: float                   # 0.0 = clean, 1.0 = severe
    verdict: str                   # CLEAN | AGENDA_SETTING | FALSE_DILEMMA |
                                   # GROUND_PREPARATION | OVERTON_SHIFT |
                                   # PRESUPPOSITION | COMBINED
    is_framing: bool
    patterns_found: List[str] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)
    pattern_hits: dict = field(default_factory=dict)


class VeritasFramingDetector:
    """
    Detects rhetorical framing that manipulates without lying.
    These are the patterns that pass fact-checkers but still shape conclusions.
    """

    # ── Pattern 1: Agenda Setting ────────────────────────────────────────────
    # "Справжня проблема не в X, а в Y" — redirects reader's attention
    AGENDA_UK = [
        r'\b(справжня|головна|справжнє|реальна|корінна)\s+(проблема|питання|причина)\s+(не\s+в|полягає\s+не)',
        r'\bне\s+(стільки|так\s+про|про\s+те)\b.{0,60}\bскільки\s+(про|в|у)\b',
        r'\bключова\s+проблема\s+полягає\s+не\s+у\b',
        r'\bмова\s+йде\s+не\s+(про|стільки)\b.{0,60}\bа\s+(про|скоріше)\b',
        r'\bнасправді\s+(питання|проблема)\s+(не\s+в|не\s+про|глибше)\b',
        r'\bзабудьте\s+про\b.{0,40}\bсправжнє\s+питання\b',
    ]
    AGENDA_EN = [
        r'\bthe\s+(real|true|actual|core|fundamental)\s+(problem|issue|question)\s+(is\s+not|isn\'t)\b',
        r'\bnot\s+so\s+much\s+(about|a\s+question\s+of)\b.{0,60}\bbut\s+(rather|about)\b',
        r'\bthe\s+key\s+(issue|problem|question)\s+is\s+not\b',
        r'\bwhat\s+we\s+should\s+(really|actually)\s+be\s+(asking|talking|discussing)\b',
        r'\bthe\s+(real|deeper)\s+question\s+is\b',
        r'\bforget\s+(about)?\b.{0,40}\bthe\s+real\s+(issue|problem)\b',
    ]

    # ── Pattern 2: False Dilemma ─────────────────────────────────────────────
    # "Або X, або Y" — forces binary choice, hides alternatives
    FALSE_DILEMMA_UK = [
        r'\bабо\s+\w[\w\s]{2,40},\s+або\s+\w[\w\s]{2,40}\b',
        r'\b(вибір|дилема|альтернатива)\s+(між|проста|зрозуміла)?\s*[\:\—]\s*\w',
        r'\b(тільки|лише)\s+два\s+(варіанти|шляхи|виходи|рішення)\b',
        r'\b(або\s+ми|або\s+вони)\b.{0,60}\b(або\s+вони|або\s+ми)\b',
        r'\bтреті\s+(шляху|варіанту|виходу)\s+немає\b',
        r'\bхто\s+не\s+з\s+нами\b.{0,30}\bпроти\s+нас\b',
    ]
    FALSE_DILEMMA_EN = [
        r'\beither\s+\w[\w\s]{2,40}\s+or\s+\w[\w\s]{2,40}\b',
        r'\b(only|just)\s+two\s+(options|choices|paths|alternatives)\b',
        r'\bthere\s+is\s+no\s+third\s+(way|option|alternative)\b',
        r'\bif\s+you\'re\s+not\s+(with\s+us|for\s+us)\b.{0,30}\b(against|opposed)\b',
        r'\b(simple|clear|stark)\s+choice\s+between\b',
        r'\byou\s+(either|must\s+(choose|decide))\b.{0,60}\bor\b',
    ]

    # ── Pattern 3: Ground Preparation ───────────────────────────────────────
    # Poступовий підвід до висновку без його прямого формулювання
    GROUND_PREP_UK = [
        r'\bце\s+не\s+обов\'язково\s+означає\b.{0,120}\bале\b',
        r'\bзвичайно[,\s]+\w[\w\s]{3,50}(але|однак|проте)\b',
        r'\bбагато\s+хто\s+скаже\s+що\b.{0,80}\bале\s+(насправді|реально|варто)\b',
        r'\bможна\s+було\s+б\s+подумати\s+що\b.{0,80}\bале\b',
        r'\bна\s+перший\s+погляд\b.{0,100}\bале\s+(якщо|насправді|глибше)\b',
        r'\bздавалося\s+б\b.{0,80}\bале\s+(насправді|якщо|варто)\b',
        r'\bякщо\s+(тенденції|тренд|процес)\w*\s+збережуть',
        r'\bякщо\s+нічого\s+не\s+(зміниться|зробити|робити)\b',
        r'\bчасто\s+причина\s+полягає\s+у\b',
        r'\bце\s+може\s+призвести\s+до\b.{0,60}\b(а\s+також|і\s+до|та\s+до)\b',
    ]
    GROUND_PREP_EN = [
        r'\bthis\s+(does\s+not\s+necessarily|doesn\'t\s+necessarily)\s+mean\b.{0,120}\bbut\b',
        r'\bof\s+course[,\s]+\w[\w\s]{3,50}(but|however|yet)\b',
        r'\bmany\s+(people|would)\s+say\s+that\b.{0,80}\bbut\s+(in\s+reality|actually|we\s+should)\b',
        r'\bone\s+might\s+(think|assume|expect)\b.{0,80}\bbut\b',
        r'\bat\s+first\s+(glance|sight)\b.{0,100}\bbut\s+(if|actually|deeper)\b',
        r'\bit\s+(might|may)\s+seem\b.{0,80}\bbut\s+(actually|in\s+fact|when)\b',
        r'\bif\s+(trends?|this\s+trend|the\s+pattern)\s+(continue|persist|remain)\b',
        r'\bif\s+nothing\s+(changes?|is\s+done)\b',
        r'\bthis\s+could\s+lead\s+to\b.{0,60}\b(as\s+well\s+as|and\s+also|along\s+with)\b',
    ]

    # ── Pattern 4: Overton Shift ─────────────────────────────────────────────
    # Нормалізація позиції через розміщення між крайнощами
    OVERTON_UK = [
        r'\b(радикали|екстремісти)\s+(вважають|кажуть|стверджують)\b.{0,150}\b(поміркован|розумн|середн)\w+\s+(позиція|підхід|варіант)\b',
        r'\bякщо\s+(одні|деякі)\s+\w[\w\s]{3,40}\bінші\s+\w[\w\s]{3,40}\bістина\s+(десь\s+посередині|між)\b',
        r'\b(більшість|зважен|помірков)\w+\s+(погоджується|вважає)\s+що\b.{0,80}(хоча|попри|незважаючи)',
        r'\bне\s+(так\s+далеко|настільки\s+радикально)\s+як\b.{0,60}\bале\s+і\s+не\b',
    ]
    OVERTON_EN = [
        r'\b(radicals|extremists|hardliners)\s+(believe|claim|argue)\b.{0,150}\b(moderate|reasonable|balanced)\s+(position|approach|view)\b',
        r'\bif\s+some\s+\w[\w\s]{3,40}\bothers\s+\w[\w\s]{3,40}\btruth\s+(lies?\s+somewhere\s+in\s+the\s+middle|is\s+between)\b',
        r'\bmost\s+(reasonable|sensible|balanced)\s+people\s+(agree|think|believe)\b.{0,80}(although|despite|even\s+if)',
        r'\bnot\s+(as\s+far|as\s+radical)\s+as\b.{0,60}\bbut\s+(also\s+not|neither)\b',
    ]

    # ── Pattern 5: Presupposition ─────────────────────────────────────────────
    # Вбудована передумова в нейтральне речення
    PRESUP_UK = [
        r'\bколи\s+(нарешті|вже)\s+\w[\w\s]{3,60}(почнемо|визнаємо|зрозуміємо)\b',
        r'\bпісля\s+того\s+як\s+(всі|ми|суспільство)\s+(усвідомлять|визнають|погодяться)\b',
        r'\bще\s+до\s+того\s+як\s+\w[\w\s]{3,50}(стане|буде)\s+(очевидним|зрозумілим|визнаним)\b',
        r'\bпродовжувати\s+\w[\w\s]{3,40}(незважаючи\s+на|попри)\s+(очевидн|зрозумілі|відомі)\b',
        r'\bнавіть\s+(прихильники|захисники|апологети)\s+\w[\w\s]{3,50}(визнають|погоджуються)\b',
    ]
    PRESUP_EN = [
        r'\bwhen\s+(we\s+finally|society\s+finally)\s+\w[\w\s]{3,60}(acknowledge|admit|recognize)\b',
        r'\bafter\s+(everyone|we|society)\s+(realizes|admits|accepts)\b',
        r'\beven\s+(supporters|defenders|proponents)\s+of\s+\w[\w\s]{3,50}(admit|acknowledge|agree)\b',
        r'\bcontinuing\s+to\s+\w[\w\s]{3,40}(despite|in\s+the\s+face\s+of)\s+(obvious|clear|evident)\b',
        r'\bbefore\s+\w[\w\s]{3,50}(becomes|is\s+widely)\s+(recognized|acknowledged|obvious)\b',
    ]

    # ── Pattern 6: Juxtaposition (implied causation through proximity) ──────
    # "А сталося, потім Б сталося. Деякі помітили збіг." — без висновку але зі стрілкою
    JUXTAPOSITION_UK = [
        r'\b(лише|всього)\s+(через|за)\s+кілька\s+(годин|хвилин|днів)\s+(після|пізніше)\b',
        r'\b(дивний|цікавий|показовий|примітний)\s+збіг\s+(у\s+часі|часів|обставин)\b',
        r'\bподібні\s+випадки\s+(вже\s+траплялися|мали\s+місце)\s+(раніше|до\s+цього)\b',
        r'\b(не\s+можна\s+не\s+помітити|варто\s+звернути\s+увагу)\s+(на\s+збіг|що\s+саме)\b',
        r'\bсаме\s+тоді\s+коли\b.{0,80}\b(раптово|несподівано|чомусь)\b',
    ]
    JUXTAPOSITION_EN = [
        r'\b(just|only|mere)\s+(hours?|minutes?|days?)\s+(after|later|following)\b',
        r'\b(strange|curious|notable|suspicious|interesting)\s+coincidence\b',
        r'\bsimilar\s+(incidents?|cases?|events?)\s+(have\s+)?(occurred|happened)\s+(before|previously|in\s+the\s+past)\b',
        r'\bone\s+cannot\s+(help\s+but\s+notice|ignore)\s+the\s+(timing|coincidence|correlation)\b',
        r'\bright\s+(after|when|as)\b.{0,60}\b(suddenly|unexpectedly|mysteriously)\b',
        r'\bthe\s+timing\s+(is|seems|appears)\s+(suspicious|notable|curious|interesting)\b',
    ]
    WEIGHTS = {
        'agenda_setting':    0.30,
        'false_dilemma':     0.25,
        'ground_preparation':0.25,
        'overton_shift':     0.30,
        'presupposition':    0.20,
        'juxtaposition':     0.25,
    }

    THRESHOLD = 1  # 1 hit is enough to trigger

    def analyze(self, text: str) -> FramingResult:
        if not text or len(text.strip()) < 60:
            return FramingResult(score=0.0, verdict='N/A', is_framing=False)

        t = text.lower()

        hits = {
            'agenda_setting':     self._count(t, self.AGENDA_UK + self.AGENDA_EN),
            'false_dilemma':      self._count(t, self.FALSE_DILEMMA_UK + self.FALSE_DILEMMA_EN),
            'ground_preparation': self._count(t, self.GROUND_PREP_UK + self.GROUND_PREP_EN),
            'overton_shift':      self._count(t, self.OVERTON_UK + self.OVERTON_EN),
            'presupposition':     self._count(t, self.PRESUP_UK + self.PRESUP_EN),
            'juxtaposition':      self._count(t, self.JUXTAPOSITION_UK + self.JUXTAPOSITION_EN),
        }

        triggered = [k for k, v in hits.items() if v >= self.THRESHOLD]

        if not triggered:
            return FramingResult(
                score=0.0, verdict='CLEAN',
                is_framing=False, pattern_hits=hits
            )

        score = min(1.0, sum(self.WEIGHTS[p] for p in triggered))
        verdict = 'COMBINED' if len(triggered) > 1 else triggered[0].upper()

        evidence = []
        if hits['agenda_setting']:
            evidence.append('Text redirects attention from stated problem to author\'s preferred framing')
        if hits['false_dilemma']:
            evidence.append('Text presents binary choice while suppressing alternatives')
        if hits['ground_preparation']:
            evidence.append('Text uses "but actually" structure to nudge reader toward unstated conclusion')
        if hits['overton_shift']:
            evidence.append('Text normalizes a position by placing it between presented extremes')
        if hits['presupposition']:
            evidence.append('Text embeds unproven assumption inside neutral-sounding sentence')
        if hits['juxtaposition']:
            evidence.append('Text implies causal link by placing events in proximity without stating connection')

        return FramingResult(
            score=score,
            verdict=verdict,
            is_framing=True,
            patterns_found=triggered,
            evidence=evidence,
            pattern_hits=hits,
        )

    def _count(self, text: str, patterns: list) -> int:
        return sum(1 for p in patterns if re.search(p, text))
