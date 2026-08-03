"""
Veritas Performative Accountability Detector v1.0
"Крокодилячі сльози"

Philosophy:
"Декларація дискомфорту без механізму змін — це не чесність. Це PR."

Detects the pattern where a public actor:
1. Declares discomfort with their own power/resources/position
2. Justifies continuation despite that discomfort ("race logic", "forced position")
3. Provides NO concrete accountability mechanism (deadline, independent oversight, exit)

Classic examples:
- "I'm deeply uncomfortable with our power, but we can't slow down"
- "I wish the situation were different, but competitors would fill the void"
- "We recognize the risks, but someone has to do this responsibly"

This is distinct from genuine accountability, which has:
- Specific deadlines
- Independent oversight with veto power
- Concrete structural changes (resign, delete, refund, shut down)
"""

import re
from typing import Dict, List, Tuple


class PerformativeAccountabilityDetector:

    def __init__(self):

        # ── DISCOMFORT DECLARATIONS ──────────────────────────────────
        # Actor signals awareness of their own problematic position
        self.discomfort_signals = [
            # EN
            r'\b(deeply\s+uncomfortable|not\s+comfortable\s+with|uncomfortable\s+with\s+this)',
            r'\b(concerns?\s+me\s+deeply|deeply\s+concerned\s+about)',
            r'\b(think\s+about\s+this\s+a\s+lot|keep\s+thinking\s+about)',
            r'\b(wish\s+the\s+situation\s+were|wish\s+it\s+were\s+different)',
            r'\b(difficult\s+position|hard\s+position|uncomfortable\s+position)',
            r'\b(recognize\s+the\s+irony|aware\s+of\s+the\s+irony)',
            r'\b(i\s+know\s+this\s+looks|i\s+understand\s+how\s+this\s+(looks|sounds))',
            r'\b(we\s+are\s+part\s+of\s+the\s+problem|recognize\s+we\s+are\s+one\s+of)',
            # UA
            r'\b(глибоко\s+некомфортно|мені\s+некомфортно|нам\s+некомфортно)',
            r'\b(глибоко\s+турбує|серйозно\s+хвилює|постійно\s+думаю\s+про\s+це)',
            r'\b(хотів\s+би\s+щоб\s+ситуація|бажаємо\s+щоб\s+було\s+інакше)',
            r'\b(складне\s+становище|важка\s+позиція|складна\s+ситуація)',
            r'\b(усвідомлюємо\s+іронію|розуміємо\s+як\s+це\s+виглядає)',
            r'\b(ми\s+самі\s+є\s+частиною|визнаємо\s+що\s+ми\s+теж)',
        ]

        # ── CONTINUATION JUSTIFICATION ───────────────────────────────
        # Actor justifies NOT changing despite the declared discomfort
        # "Race logic", "forced position", "responsible actor in vacuum"
        self.continuation_signals = [
            # EN — race logic
            r'\b(cannot\s+slow\s+down|can\'t\s+slow\s+down|must\s+not\s+slow)',
            r'\b(if\s+we\s+(stop|slow|don\'t).{1,60}(others|competitors|less\s+responsible))',
            r'\b(race\s+(to\s+the\s+)?(top|bottom|ahead)|racing\s+ahead)',
            r'\b(fill\s+the\s+void|fill\s+that\s+void|someone\s+else\s+will)',
            # EN — forced position
            r'\b(find\s+ourselves\s+in.{1,40}(must|have\s+to|forced))',
            r'\b(no\s+choice\s+but\s+to|have\s+no\s+alternative|no\s+other\s+option)',
            r'\b(must\s+continue|have\s+to\s+continue|forced\s+to\s+continue)',
            r'\b(at\s+the\s+same\s+time\s+we.{1,60}(continue|proceed|move\s+forward))',
            r'\b(responsibly.{1,80}but.{1,60}(continue|cannot\s+stop|must))',
            r'\b(even\s+though\s+we\s+wish.{1,60}(must|continue|cannot))',
            # EN — responsible actor framing
            r'\b(better\s+us\s+than|if\s+not\s+us.{1,40}(who|then))',
            r'\b(someone\s+has\s+to\s+do\s+this\s+responsibly)',
            # UA — race logic
            r'\b(не\s+можемо\s+зупинитись|не\s+можемо\s+сповільнитись|мусимо\s+продовжувати)',
            r'\b(якщо\s+ми\s+(зупинимось|сповільнимось).{1,60}(інші|конкуренти|менш\s+відповідальні))',
            r'\b(гонка.{1,40}(не\s+можемо|неможливо)\s+(зупинити|вийти))',
            r'\b(хтось\s+інший\s+(займе|зробить|заповнить))',
            # UA — forced position
            r'\b(знаходимось\s+у\s+(ситуації|становищі).{1,40}(змушені|мусимо))',
            r'\b(немає\s+іншого\s+вибору|вимушені\s+продовжувати)',
            r'\b(водночас\s+ми.{1,60}(продовжуємо|рухаємось|мусимо))',
            r'\b(хоча\s+і\s+хотіли\s+б.{1,60}(змушені|мусимо|продовжуємо))',
            # UA — responsible actor
            r'\b(краще\s+ми\s+ніж|якщо\s+не\s+ми.{1,40}(хто|то))',
            r'\b(хтось\s+має\s+робити\s+це\s+відповідально)',
        ]

        # ── CONCRETE MECHANISM (NEGATIVE SIGNAL) ─────────────────────
        # If present, disqualifies performative classification
        # Real accountability has specifics: deadlines, independent oversight, exit
        self.concrete_mechanism = [
            # Deadlines
            r'\b(by\s+(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2})',
            r'\b(до\s+\d{1,2}\s+(січня|лютого|березня|квітня|травня|червня|липня|серпня|вересня|жовтня|листопада|грудня))',
            r'\b(з\s+\d{1,2}\s+\w+\s+202\d|starting\s+(january|february|march|q[1-4])\s+202\d)',
            r'\b(within\s+\d+\s+(days|weeks|months)|протягом\s+\d+\s+(днів|тижнів|місяців))',
            # Exit / resignation
            r'\b(step\s+down|stepping\s+down|will\s+resign|is\s+resigning)',
            r'\b(підемо\s+у\s+відставку|іду\s+у\s+відставку|складаємо\s+повноваження)',
            # Independent oversight with real power
            r'\b(independent\s+(board|committee|auditor|review).{1,40}(veto|binding|mandatory|oversight))',
            r'\b(незалежн\w+\s+(рада|комітет|аудитор).{1,40}(право\s+вето|обов\'язков|контрол))',
            # Concrete structural changes
            r'\b(shut\s+down\s+the\s+(product|service|division)|закрив\w+\s+(продукт|сервіс|підрозділ))',
            r'\b(delete\s+all\s+user\s+data|видалити\s+всі\s+дані\s+користувачів)',
            r'\b(refund\s+(all|every)|повертаємо\s+(кошти|гроші)\s+всім)',
            r'\b(give\s+users\s+(full|complete)\s+control|надаємо\s+користувачам\s+повний\s+контроль)',
        ]

        # ── IMPLICIT CONTINUATION (no explicit race logic needed) ────
        # Actor under commercial/competitive pressure but frames it as mission
        self.implicit_continuation_signals = [
            # Commercial pressure framing
            r'\b(commercial\s+pressure|тиск\s+ринку|конкурентний\s+тиск)',
            r'\b(balance\s+safety\s+and\s+(profit|commercial|revenue)|балансувати.{1,30}безпека.{1,30}прибуток)',
            r'\b(safety.{1,40}(highest|top|primary)\s+(priority|focus)|безпека.{1,30}головний\s+пріоритет)',
            # "We do more than others" — competitive differentiation via safety
            r'\b(more\s+than\s+other\s+companies|більше\s+ніж\s+інші\s+компанії)',
            r'\b(we\s+do\s+(more|better).{1,40}(safety|безпека).{1,40}(other|інші))',
            # Advocacy without action
            r'\b(always\s+advocated\s+for|завжди\s+виступав\s+за).{1,60}(regulation|регулювання|oversight)',
            r'\b(advocat\w+.{1,40}regulat\w+|закликав.{1,40}регулюванн)',
            # "Responsible development" as justification for continuing
            r'\b(responsible\s+(development|innovation|ai)|відповідальний\s+розвиток)',
            r'\b(safety.{1,30}focus\w*\s+lab|орієнтован\w+\s+на\s+безпеку)',
        ]

    def analyze(self, text: str) -> Dict:
        text_lower = text.lower()

        discomfort_hits = [
            p for p in self.discomfort_signals
            if re.search(p, text_lower, re.IGNORECASE)
        ]
        continuation_hits = [
            p for p in self.continuation_signals
            if re.search(p, text_lower, re.IGNORECASE)
        ]
        implicit_hits = [
            p for p in self.implicit_continuation_signals
            if re.search(p, text_lower, re.IGNORECASE)
        ]
        mechanism_hits = [
            p for p in self.concrete_mechanism
            if re.search(p, text_lower, re.IGNORECASE)
        ]

        d = len(discomfort_hits)
        c = len(continuation_hits)
        ic = len(implicit_hits)
        m = len(mechanism_hits)

        # EXPLICIT: discomfort + race/forced logic + no mechanism
        explicit_performative = d >= 1 and c >= 1 and m == 0

        # IMPLICIT: discomfort + commercial/mission framing + no mechanism
        # "Uncomfortable but we keep going" — said through context not words
        implicit_performative = d >= 1 and c == 0 and ic >= 1 and m == 0

        is_performative = explicit_performative or implicit_performative

        if is_performative:
            if explicit_performative and d >= 3 and c >= 2:
                score = 0.90
            elif explicit_performative and (d >= 2 or c >= 2):
                score = 0.70
            elif explicit_performative:
                score = 0.60
            else:
                # implicit only — weaker signal
                score = 0.55
        else:
            score = max(0.0, (d * 0.1 + c * 0.1) - (m * 0.3))

        # Verdict
        if is_performative and score >= 0.70:
            verdict = 'CROCODILE_TEARS'
            explanation = (
                'Виявлено патерн "крокодилячих сліз": актор декларує дискомфорт від своєї влади, '
                'виправдовує її збереження логікою гонки або вимушеного становища, '
                'і не пропонує жодного конкретного механізму змін. '
                'Декларація ≠ дія.'
            )
            explanation_en = (
                'Performative accountability detected: actor declares discomfort with their power, '
                'justifies its continuation via race logic or forced position, '
                'and offers no concrete accountability mechanism. '
                'Declaration ≠ action.'
            )
        elif is_performative:
            verdict = 'WEAK_ACCOUNTABILITY'
            explanation = (
                'Декларація дискомфорту без конкретного механізму змін. '
                'Продовження виправдовується місією або комерційним тиском. '
                'Перевірте наявність реальних зобов\'язань.'
            )
            explanation_en = (
                'Discomfort declared without concrete accountability mechanism. '
                'Continuation justified through mission or commercial framing. '
                'Check for real commitments.'
            )
        else:
            verdict = 'GENUINE_ACCOUNTABILITY'
            explanation = 'Конкретні механізми відповідальності присутні.'
            explanation_en = 'Concrete accountability mechanisms present.'

        return {
            'performative_score':      round(score, 3),
            'performative_verdict':    verdict,
            'is_performative':         is_performative,
            'discomfort_count':        d,
            'continuation_count':      c,
            'implicit_count':          ic,
            'mechanism_count':         m,
            'explanation_uk':          explanation,
            'explanation_en':          explanation_en,
        }
