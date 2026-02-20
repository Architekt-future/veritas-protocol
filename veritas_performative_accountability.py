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
            r'(deeply\s+uncomfortable|not\s+comfortable\s+with|uncomfortable\s+with\s+this)',
            r'(concerns?\s+me\s+deeply|deeply\s+concerned\s+about)',
            r'(think\s+about\s+this\s+a\s+lot|keep\s+thinking\s+about)',
            r'(wish\s+the\s+situation\s+were|wish\s+it\s+were\s+different)',
            r'(difficult\s+position|hard\s+position|uncomfortable\s+position)',
            r'(recognize\s+the\s+irony|aware\s+of\s+the\s+irony)',
            r'(i\s+know\s+this\s+looks|i\s+understand\s+how\s+this\s+(looks|sounds))',
            r'(we\s+are\s+part\s+of\s+the\s+problem|recognize\s+we\s+are\s+one\s+of)',
            # UA
            r'(глибоко\s+некомфортно|мені\s+некомфортно|нам\s+некомфортно)',
            r'(глибоко\s+турбує|серйозно\s+хвилює|постійно\s+думаю\s+про\s+це)',
            r'(хотів\s+би\s+щоб\s+ситуація|бажаємо\s+щоб\s+було\s+інакше)',
            r'(складне\s+становище|важка\s+позиція|складна\s+ситуація)',
            r'(усвідомлюємо\s+іронію|розуміємо\s+як\s+це\s+виглядає)',
            r'(ми\s+самі\s+є\s+частиною|визнаємо\s+що\s+ми\s+теж)',
        ]

        # ── CONTINUATION JUSTIFICATION ───────────────────────────────
        # Actor justifies NOT changing despite the declared discomfort
        # "Race logic", "forced position", "responsible actor in vacuum"
        self.continuation_signals = [
            # EN — race logic
            r'(cannot\s+slow\s+down|can\'t\s+slow\s+down|must\s+not\s+slow)',
            r'(if\s+we\s+(stop|slow|don\'t).{1,60}(others|competitors|less\s+responsible))',
            r'(race\s+(to\s+the\s+)?(top|bottom|ahead)|racing\s+ahead)',
            r'(fill\s+the\s+void|fill\s+that\s+void|someone\s+else\s+will)',
            # EN — forced position
            r'(find\s+ourselves\s+in.{1,40}(must|have\s+to|forced))',
            r'(no\s+choice\s+but\s+to|have\s+no\s+alternative|no\s+other\s+option)',
            r'(must\s+continue|have\s+to\s+continue|forced\s+to\s+continue)',
            r'(at\s+the\s+same\s+time\s+we.{1,60}(continue|proceed|move\s+forward))',
            r'(responsibly.{1,80}but.{1,60}(continue|cannot\s+stop|must))',
            r'(even\s+though\s+we\s+wish.{1,60}(must|continue|cannot))',
            # EN — responsible actor framing
            r'(better\s+us\s+than|if\s+not\s+us.{1,40}(who|then))',
            r'(someone\s+has\s+to\s+do\s+this\s+responsibly)',
            # UA — race logic
            r'(не\s+можемо\s+зупинитись|не\s+можемо\s+сповільнитись|мусимо\s+продовжувати)',
            r'(якщо\s+ми\s+(зупинимось|сповільнимось).{1,60}(інші|конкуренти|менш\s+відповідальні))',
            r'(гонка.{1,40}(не\s+можемо|неможливо)\s+(зупинити|вийти))',
            r'(хтось\s+інший\s+(займе|зробить|заповнить))',
            # UA — forced position
            r'(знаходимось\s+у\s+(ситуації|становищі).{1,40}(змушені|мусимо))',
            r'(немає\s+іншого\s+вибору|вимушені\s+продовжувати)',
            r'(водночас\s+ми.{1,60}(продовжуємо|рухаємось|мусимо))',
            r'(хоча\s+і\s+хотіли\s+б.{1,60}(змушені|мусимо|продовжуємо))',
            # UA — responsible actor
            r'(краще\s+ми\s+ніж|якщо\s+не\s+ми.{1,40}(хто|то))',
            r'(хтось\s+має\s+робити\s+це\s+відповідально)',
        ]

        # ── CONCRETE MECHANISM (NEGATIVE SIGNAL) ─────────────────────
        # If present, disqualifies performative classification
        # Real accountability has specifics: deadlines, independent oversight, exit
        self.concrete_mechanism = [
            # Deadlines
            r'(by\s+(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2})',
            r'(до\s+\d{1,2}\s+(січня|лютого|березня|квітня|травня|червня|липня|серпня|вересня|жовтня|листопада|грудня))',
            r'(з\s+\d{1,2}\s+\w+\s+202\d|starting\s+(january|february|march|q[1-4])\s+202\d)',
            r'(within\s+\d+\s+(days|weeks|months)|протягом\s+\d+\s+(днів|тижнів|місяців))',
            # Exit / resignation
            r'(step\s+down|stepping\s+down|will\s+resign|is\s+resigning)',
            r'(підемо\s+у\s+відставку|іду\s+у\s+відставку|складаємо\s+повноваження)',
            # Independent oversight with real power
            r'(independent\s+(board|committee|auditor|review).{1,40}(veto|binding|mandatory|oversight))',
            r'(незалежн\w+\s+(рада|комітет|аудитор).{1,40}(право\s+вето|обов\'язков|контрол))',
            # Concrete structural changes
            r'(shut\s+down\s+the\s+(product|service|division)|закрив\w+\s+(продукт|сервіс|підрозділ))',
            r'(delete\s+all\s+user\s+data|видалити\s+всі\s+дані\s+користувачів)',
            r'(refund\s+(all|every)|повертаємо\s+(кошти|гроші)\s+всім)',
            r'(give\s+users\s+(full|complete)\s+control|надаємо\s+користувачам\s+повний\s+контроль)',
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
        mechanism_hits = [
            p for p in self.concrete_mechanism
            if re.search(p, text_lower, re.IGNORECASE)
        ]

        d = len(discomfort_hits)
        c = len(continuation_hits)
        m = len(mechanism_hits)

        # Core logic:
        # Performative = declared discomfort + justified continuation + no concrete mechanism
        is_performative = d >= 1 and c >= 1 and m == 0

        if is_performative:
            # Score scales with signal strength
            score = min(0.95, (d * 0.25 + c * 0.35))
            if d >= 3 and c >= 2:
                score = 0.90  # strong signal
            elif d >= 2 or c >= 2:
                score = 0.70  # moderate signal
            else:
                score = 0.55  # minimal but present
        else:
            # Has concrete mechanism — genuine accountability
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
                'Слабкі ознаки декларативної відповідальності без механізму реалізації. '
                'Перевірте наявність конкретних зобов\'язань.'
            )
            explanation_en = (
                'Weak performative accountability signals. '
                'Check for concrete commitments.'
            )
        else:
            verdict = 'GENUINE_ACCOUNTABILITY'
            explanation = 'Конкретні механізми відповідальності присутні.'
            explanation_en = 'Concrete accountability mechanisms present.'

        return {
            'performative_score':   round(score, 3),
            'performative_verdict': verdict,
            'is_performative':      is_performative,
            'discomfort_count':     d,
            'continuation_count':   c,
            'mechanism_count':      m,
            'explanation_uk':       explanation,
            'explanation_en':       explanation_en,
        }
