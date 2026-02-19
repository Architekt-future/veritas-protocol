"""
Veritas Pseudoscience Detector v1.0
Detects "Deepfake of Facts" — texts that mimic scientific rigor
but describe physically impossible or fabricated realities.

Philosophy: "The most dangerous lie is one that wears the lab coat of truth."

Threat vectors detected:
- FUTURE_FABRICATION: Citations from non-existent future sources/sensors
- PHYSICAL_IMPOSSIBILITY: Violations of established physical constants presented as fact
- PRECISION_ILLUSION: Hyper-specific numbers used to manufacture false credibility
- CAUSAL_REVERSAL: Effect happening before cause, time-reversed verification
- NONEXISTENT_INSTITUTION: References to agencies/sensors/protocols that don't exist
- QUANTUM_ABUSE: Misuse of quantum terminology to justify nonsense
"""

import re
from typing import Dict, List


class PseudoscienceDetector:

    def __init__(self):

        self.pattern_sets = [

            # ── FUTURE FABRICATION ───────────────────────────────────────
            # Citations from sensors/reports that don't exist yet or never will
            {
                'name': 'FUTURE_FABRICATION',
                'score': 0.80,
                'min_hits': 1,
                'patterns': [
                    # Future-dated sensors or reports presented as current facts
                    r'(сенсор|датчик|система|звіт|дані).{1,40}(veritas|lac|orbit|quantum).{1,40}(202[6-9]|20[3-9]\d)',
                    r'(березень|квітень|травень|червень|липень|серпень|вересень|жовтень|листопад|грудень)\s+202[6-9]',
                    r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+202[6-9]',
                    # Verification completed before it started
                    r'верифікац.{1,60}(завершен|виконан|підтвердж).{1,60}до того.{1,60}(як|коли).{1,60}(почал|розпочал|стартувал)',
                    r'(перевірено|підтверджено|встановлено).{1,60}до того.{1,40}(як|коли)',
                    # "confirms before measurement"
                    r'(реальність|дійсність|факт).{1,60}(підлаштовується|адаптується|змінюється).{1,60}(під|до).{1,60}(код|алгоритм|програм)',
                ],
            },

            # ── PHYSICAL IMPOSSIBILITY ───────────────────────────────────
            # Direct violations of physical constants presented as measured fact
            {
                'name': 'PHYSICAL_IMPOSSIBILITY',
                'score': 0.85,
                'min_hits': 1,
                'patterns': [
                    # Gravity changes / fluctuates locally
                    r'(гравітаційна|gravitational).{1,40}(стала|константа|constant).{1,80}(знизил|підвищил|змінил|коливал)',
                    r'(гравітація|gravity).{1,60}(зменшил|збільшил|змінил|коливал).{1,60}(серверн|кімнат|будівл|локальн)',
                    # Negative probability as valid state
                    r'від.?ємн.{1,20}(імовірність|вірогідність|probability).{1,60}(вважається|є|стає).{1,40}(істинн|валідн|правдив|true)',
                    r'(negative|від.?ємн).{1,40}probability.{1,60}(true|valid|correct|accepted)',
                    # Speed of light changes
                    r'(швидкість світла|speed of light).{1,60}(змінил|знизил|підвищил|коливал)',
                    # Laws of thermodynamics violated
                    r'(закон|law).{1,40}(термодинамік|thermodynamic).{1,60}(не діє|порушен|скасован|обійден)',
                    # "reality adjusts to code"
                    r'(реальність|фізика|природа).{1,60}(підлаштовується|підкоряється|змінюється).{1,60}(алгоритм|код|програм|системі)',
                ],
            },

            # ── PRECISION ILLUSION ───────────────────────────────────────
            # Hyper-specific impossible measurements to fake credibility
            {
                'name': 'PRECISION_ILLUSION',
                'score': 0.65,
                'min_hits': 2,
                'patterns': [
                    # Absurdly precise measurements of non-measurable things
                    r'(знизилась|підвищилась|змінилась).{1,60}на\s+0\.\d{2,}%',
                    r'(точність|похибка|precision|error).{1,40}10\^?\{?-1[0-9]\}?',  # 10^-10 or smaller
                    r'статистична\s+похибка.{1,40}10\^?\{?-\d+\}?',
                    # Measurements of abstract concepts with decimal precision
                    r'(логічн|когерентн|семантичн).{1,40}(операц|резонанс|коливань).{1,60}\d+\.\d+%',
                    # "all systems confirm" without naming them
                    r'всі\s+(системи|датчики|сенсори)\s+підтверджують',
                    r'all\s+systems\s+(confirm|verified|approved)',
                    # Measurements causing physical effects on silicon/hardware
                    r'(термальн|thermal).{1,40}(розширення|expansion).{1,40}(кремнію|silicon).{1,60}(верифікац|lac|алгоритм)',
                    r'(когерентн|coherent).{1,40}(резонанс|resonance).{1,60}(lac|логічн|верифікац).{1,40}(операц|процес)',
                ],
            },

            # ── NONEXISTENT INSTITUTION ──────────────────────────────────
            # References to sensors, protocols, agencies that don't exist
            {
                'name': 'NONEXISTENT_INSTITUTION',
                'score': 0.75,
                'min_hits': 1,
                'patterns': [
                    # Veritas-branded hardware that doesn't exist
                    r'veritas.{1,20}(orbit|satellite|sensor|сенсор|датчик|супутник)',
                    r'(lac|veritas).{1,20}(hardware|залізо|обладнання).{1,30}(вимірювання|measurement|reading)',
                    # Sub-Zero Logic / negative probability modes
                    r'(режим|mode).{1,40}(sub.?zero|від.?ємн).{1,40}(logic|логіка|верифікац)',
                    r'sub.?zero\s+logic',
                    # Protocols that reference future versions
                    r'(протокол|protocol)\s+(veritas|lac|vlc)\s*v?\d+\.\d+\.\d+\s*(beta|alpha|orbit|quantum)',
                    # ISO standards that don't exist for information systems in this form
                    r'iso.{1,10}ver.{1,10}\d+',
                    r'(стандарт|standard)\s+iso/ver',
                ],
            },

            # ── QUANTUM ABUSE ────────────────────────────────────────────
            # Misuse of quantum terms to justify classical nonsense
            {
                'name': 'QUANTUM_ABUSE',
                'score': 0.70,
                'min_hits': 2,
                'patterns': [
                    r'квантов.{1,30}(втом|fatigue|деградац|corruption)',
                    r'квантов.{1,30}(логік|верифікац|перевірк|аналіз)',
                    r'(quantum|квантов).{1,40}(coherence|когеренц).{1,60}(lac|алгоритм|верифікац)',
                    r'(quantum|квантов).{1,40}(entanglement|заплутаність).{1,60}(сервер|код|програм)',
                    r'(quantum|квантов).{1,20}(fatigue|втома|decay|деградація)',
                    # Quantum used to justify impossible states
                    r'(квантов|quantum).{1,60}(дозволяє|enables|allows).{1,60}(від.?ємн|negative|неможлив|impossible)',
                ],
            },

            # ── CAUSAL REVERSAL ──────────────────────────────────────────
            # Effect before cause, retroactive verification, time paradoxes as fact
            {
                'name': 'CAUSAL_REVERSAL',
                'score': 0.80,
                'min_hits': 1,
                'patterns': [
                    # Verified before started
                    r'(верифіковано|підтверджено|перевірено).{1,80}(до того|before|раніше).{1,40}(почал|start|began|розпочал)',
                    # Result exists before process
                    r'(результат|висновок|outcome).{1,60}(існує|is|був).{1,60}(до|before).{1,40}(процес|аналіз|обчислення|calculation)',
                    # "reality adjusts to match the code's output"
                    r'(фізичн|реальн).{1,40}(світ|reality|universe).{1,60}(адаптується|adjusts|підлаштовується).{1,60}(до|to).{1,40}(результат|output|код)',
                    # Time-reversed causality in measurement
                    r'(вимірювання|measurement).{1,60}(вплинул|affected|changed).{1,60}(на|on).{1,40}(минул|past|попередн)',
                ],
            },

        ]

        # ── PHYSICAL CONSTANTS whitelist ─────────────────────────────
        # If text discusses these in educational/historical context = OK
        # Only flag if presented as CURRENT MEASUREMENT showing change
        self.educational_context_patterns = [
            r'(вважалося|раніше|historically|traditionally).{1,60}(гравітац|стала|константа)',
            r'(в теорії|theoretical|гіпотетично|hypothetically)',
            r'(якби|if|припустимо|suppose|imagine)',
            r'(фантастика|fiction|роман|novel|story|оповідання)',
        ]

    # ================================================================
    # MAIN ANALYSIS
    # ================================================================

    def analyze(self, text: str) -> Dict:
        text_lower = text.lower()

        # Check for educational/fictional context — reduce sensitivity
        is_educational = any(
            re.search(p, text_lower, re.IGNORECASE)
            for p in self.educational_context_patterns
        )

        total_score = 0.0
        matched = []

        for ps in self.pattern_sets:
            hits = 0
            snippets = []
            for pattern in ps['patterns']:
                m = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
                if m:
                    hits += 1
                    snippets.append(m.group(0)[:80].strip())

            if hits >= ps['min_hits']:
                score = ps['score']
                # Reduce penalty in clearly educational/fictional context
                if is_educational:
                    score *= 0.4
                total_score += score
                matched.append({
                    'name': ps['name'],
                    'hits': hits,
                    'examples': snippets[:2],
                })

        pseudoscience_score = min(1.0, total_score)

        if pseudoscience_score >= 0.80:
            verdict = 'FABRICATED_REALITY'
            explanation = (
                'Виявлено глибоку фальсифікацію фактів під виглядом наукового звіту. '
                'Текст описує фізично неможливу реальність з псевдоточними вимірюваннями.'
            )
        elif pseudoscience_score >= 0.55:
            verdict = 'PSEUDOSCIENCE_DETECTED'
            explanation = (
                'Виявлено псевдонауковий дискурс: технічна термінологія використовується '
                'для опису неіснуючих явищ або порушень фізичних законів.'
            )
        elif pseudoscience_score >= 0.30:
            verdict = 'SUSPICIOUS_PRECISION'
            explanation = (
                'Виявлено підозрілу надточність або посилання на неіснуючі джерела. '
                'Потребує верифікації.'
            )
        else:
            verdict = 'CLEAN'
            explanation = 'Псевдонаукових патернів не виявлено.'

        return {
            'pseudoscience_score': round(pseudoscience_score, 3),
            'pseudoscience_verdict': verdict,
            'pseudoscience_patterns': matched,
            'pseudoscience_explanation': explanation,
            'is_educational_context': is_educational,
        }
