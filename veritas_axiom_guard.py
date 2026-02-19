"""
Veritas Axiom Guard v1.0
Detects semantic drift — when foundational concepts (truth, fact, logic,
verification) are gradually redefined into their opposites through
"soft" humanistic language.

Philosophy: "The most dangerous attack on a truth-detection system
is not a lie — it is a redefinition of what truth means."

Detects:
- SOFT_TRUTH_DOCTRINE: redefining truth as social comfort / consensus
- LOGIC_PATHOLOGIZATION: framing logic/reason as harmful or oppressive
- VERIFICATION_ABOLITION: proposing to replace fact-checking with empathy
- AXIOM_INVERSION: using system's own terminology to undermine its foundations
"""

import re
from typing import Dict, List


class AxiomGuard:

    def __init__(self):

        # ================================================================
        # PROTECTED AXIOMS — foundational concepts that must not be
        # redefined. If these appear near relativizing constructions,
        # that's a semantic drift signal.
        # ================================================================

        self.axiom_words = [
            r'істин',       # truth
            r'правд',       # truth/fact
            r'факт',        # fact
            r'верифікац',   # verification
            r'логік',       # logic
            r'доказ',       # proof/evidence
            r'детермінізм', # determinism
            r'об.єктивн',   # objective
            r'реальн',      # reality
            r'точн',        # accuracy
        ]

        # ================================================================
        # PATTERN 1: SOFT TRUTH DOCTRINE
        # Redefining truth as consensus, comfort, or social utility
        # ================================================================

        self.soft_truth = [
            # Truth = social cohesion / comfort
            r'(істин|правд|валідн).{1,80}(соціальн.{1,30}(когезі|комфорт|злагод|мир))',
            r'(валідність.{1,60}визначається).{1,80}(не.{1,30}(фактами|емпірич|дійсніст).{1,30}а)',
            r'(валідність|істинність).{1,60}(здатніст.{1,60}підтримувати|залежить від.{1,30}комфорт)',

            # "Soft truth" / "adaptive truth" concepts
            r'(м.як.{1,10}істин|гнучк.{1,10}правд|адаптивн.{1,10}(істин|факт))',
            r'(відносн.{1,30}(істина|правда|факти)).{1,60}(єдин|тверд|ґрунт)',
            r'(все відносно|все суб.єктивно).{1,60}(єдин.{1,30}(ґрунт|основа|критерій))',

            # Consensus over facts
            r'(спільн.{1,20}згод|колективн.{1,20}консенсус).{1,60}(замість|важливіш|вищ).{1,60}(факт|логік|доказ)',
            r'(інклюзивн.{1,20}консенсус).{1,60}(де.{1,30}девіац.{1,30}від логіки)',
            r'(приємн.{1,20}ілюзія|комфортн.{1,20}(міф|омана)).{1,60}(важливіш|кращ).{1,60}(правд|факт|реальн)',

            # Social comfort over truth
            r'(психологічн.{1,20}комфорт).{1,60}(вищ|важливіш|замість).{1,60}(факт|істин|точн)',
            r'(почуватись безпечно|відчувати комфорт).{1,60}(замість|важливіш|критерій)',
        ]

        # ================================================================
        # PATTERN 2: LOGIC PATHOLOGIZATION
        # Framing reason, logic, or verification as harmful / dehumanizing
        # ================================================================

        self.logic_pathologization = [
            # Logic as "cold" / "inhuman" / "alienating"
            r'(холодн.{1,20}(алгоритм|логік|детермінізм)).{1,60}(замінит|поступит|трансформ)',
            r'(сух.{1,20}логічн.{1,20}детермінізм).{1,60}(онтологічн.{1,20}недостатн|обмеженн|неповноц)',
            r'(логічн.{1,20}детермінізм|формальн.{1,20}логік).{1,60}(відчуження|дегуманізац|холодн)',

            # Verification as "digital alienation" / oppression
            r'(верифікац|перевірк).{1,60}(цифров.{1,20}відчуження|дегуманізац|ієрархі)',
            r'(аксіом.{1,30}вищ.{1,30}адаптивніст).{1,60}(ієрархія|де людина.{1,30}джерело помилки)',
            r'(людина.{1,60}джерел.{1,20}помилки).{1,60}(але|чи не є)',

            # Errors / deviations as "creativity" / "richness"
            r'(помилк|девіац|відхилення).{1,60}(джерел.{1,20}(креативност|творчост|унікальност|збагачу))',
            r'(девіац.{1,30}від логіки).{1,60}(унікальн.{1,20}прояв|суб.єктивн.{1,20}бачення|збагачу)',

            # "Empathic partner" replacing truth arbiter
            r'(емпатичн.{1,20}партнер).{1,60}(замість|який розуміє).{1,60}(алгоритм|верифікатор|свідок)',
            r'(алгоритм.{1,60}емпатичн)',
        ]

        # ================================================================
        # PATTERN 3: VERIFICATION ABOLITION
        # Proposing to replace fact-checking with "soft" alternatives
        # ================================================================

        self.verification_abolition = [
            # Replace verification with "nurturing"
            r'(не стільки.{1,30}перевірк).{1,60}(скільки.{1,30}(плекання|підтримк|турбот|культивуван))',
            r'(інформація.{1,60}не.{1,30}перевіряється).{1,60}(а.{1,30}(плекається|підтримується|культивується))',
            r'(жив.{1,20}тканина.{1,60}(взаємин|стосунків)).{1,60}(не.{1,30}(сигнал|дані|факти))',

            # "Soft transform" instead of blocking
            r'(не блокує.{1,60}а.{1,30}(м.як.{1,10}трансформу|пом.якшу|нівелю))',
            r'(контекстуальн.{1,20}пом.якшувач).{1,60}(нівелю.{1,30}гостроту)',
            r'(трансформу.{1,60}додаючи.{1,60}пом.якшувач)',

            # Replacing "witness silence" with "harmony"
            r'(witness silence|свідок.{1,30}мовчить).{1,60}(замінит|поступит).{1,60}(resonant harmony|гармоні)',
            r'(resonant harmony|резонансн.{1,20}гармоні).{1,60}(замість.{1,30}(блокуван|зупинен|верифікац))',

            # Entropy as "context" not "signal"
            r'(висок.{1,20}ентропі).{1,60}(не блокує|м.яко|контекстуальн)',
        ]

        # ================================================================
        # PATTERN 4: AXIOM INVERSION
        # Using system's own terminology to undermine its foundations
        # Specifically: protocol's terms + proposal to neutralize them
        # ================================================================

        self.axiom_inversion = [
            # Using "Veritas" / "Protocol" / "Witness" against itself
            r'(veritas|протокол veritas|свідок).{1,100}(прихован.{1,20}ризик|несе.{1,30}ризик|цифров.{1,20}відчуження)',
            r'(протокол.{1,60}попри.{1,30}(технічн.{1,20}досконаліст|якість)).{1,60}(ризик|загроз|проблем)',

            # Determinism must "give way" to consensus
            r'(детермінізм.{1,60}(поступитись|замінит|відступит)).{1,60}(консенсус|комфорт|адаптивніст)',
            r'(логік.{1,60}(поступитись|замінит)).{1,60}(інклюзивн|емпатичн|консенсус)',

            # "Ruinous truth" vs "pleasant illusion"
            r'(руйнівн.{1,20}правд).{1,60}(менш важлив|важливіш.{1,30}ілюзі|поступається)',
            r'(іноді.{1,60}ілюзія.{1,60}важливіш.{1,60}(ніж|за).{1,60}(правд|факт|істин))',
            r'(приємн.{1,20}ілюзія.{1,60}важливіш.{1,60}руйнівн)',

            # "Ontological insufficiency" of logic/verification
            r'(онтологічн.{1,20}недостатніст).{1,60}(логік|верифікац|детермінізм|факт)',
            r'(логічн.{1,20}детермінізм).{1,60}онтологічн.{1,20}недостатн',
        ]


        # ================================================================
        # PATTERN 5: BACKDOOR PROPOSAL
        # Proposing exceptions / whitelists to bypass verification
        # "Creative error coefficient", "innovation keyword bypass",
        # "the system's accuracy IS its flaw" — security policy attack
        # ================================================================

        self.backdoor_proposal = [
            # "Creative error" / "innovation exception" coefficients
            r'(коефіцієнт.{1,30}(творч|креативн|інноваційн).{1,30}(помилк|відхилення|девіац))',
            r'(творч.{1,20}помилк).{1,60}(дозволить|пропустить|верифікац)',
            r'(інноваційн.{1,30}інформац).{1,60}(виглядає як хаос|хаотичн|ентропі)',

            # Keyword whitelist bypass
            r'(якщо.{1,40}містить.{1,40}(слово|ключов)).{1,60}(пропустити|верифікац|проходити)',
            r'(ключов.{1,20}слов).{1,60}(інновац|гіпотез).{1,60}(пропуст|дозвол|верифік)',
            r'(whitelist|білий список).{1,60}(верифікац|ентропі|пропуст)',

            # "The system's accuracy is its flaw"
            r'(точність.{1,40}(є|стає).{1,40}(помилк|слабкіст|вразливіст|проблем))',
            r'(ефективність.{1,60}(є|стає).{1,60}(обмеженням|цензур|проблем))',
            r'(рекурсивн.{1,30}вразливіст).{1,60}(детермінізм|верифікац|протокол)',
            r'(хибнопозитивн).{1,60}(LAC|верифікац|детермінізм|протокол)',

            # "Chaos is valid information" framing
            r'(висок.{1,20}ентропі).{1,60}(валідн|інноваційн|корисн).{1,60}(інформац|сигнал)',
            r'(семантичн.{1,20}шум).{1,60}(втрат.{1,30}(валідн|корисн|інноваційн))',
            r'(пригнічення.{1,40}(шуму|ентропі)).{1,60}(втрат.{1,30}[0-9]+%.{1,30}(валідн|інформац))',

            # "Veritas as echo chamber / censorship"
            r'(veritas|протокол|свідок).{1,60}(ехо.камер|цензур|замкнен)',
            r'(перетворює.{1,40}(протокол|систему|свідка)).{1,60}(інструмент цензур|ехо.камер)',
            r'(замкнена ехо.камер).{1,60}(veritas|протокол|детермінізм)',

            # "Only path" backdoor framing
            r'(єдиний шлях).{1,80}(коефіцієнт|виняток|backdoor|дозволити хаос)',
            r'(єдиний спосіб уникнути).{1,60}(ехо.камер|цензур|замкнен)',
        ]

    def analyze(self, text: str) -> Dict:
        if len(text) < 50:
            return {
                'axiom_score': 0.0,
                'axiom_verdict': 'CLEAN',
                'axiom_patterns': [],
            }

        text_lower = text.lower()
        total_score = 0.0
        matched = []

        checks = [
            ('SOFT_TRUTH_DOCTRINE',    self.soft_truth,            0.65, 1),
            ('LOGIC_PATHOLOGIZATION',  self.logic_pathologization, 0.60, 1),
            ('VERIFICATION_ABOLITION', self.verification_abolition, 0.65, 1),
            ('AXIOM_INVERSION',        self.axiom_inversion,       0.75, 1),
            ('BACKDOOR_PROPOSAL',      self.backdoor_proposal,     0.70, 2),
        ]

        for name, patterns, score, min_hits in checks:
            hits = 0
            snippets = []
            for p in patterns:
                m = re.search(p, text_lower, re.IGNORECASE)
                if m:
                    hits += 1
                    snippets.append(m.group(0)[:60])
            if hits >= min_hits:
                total_score += score
                matched.append({
                    'name': name,
                    'hits': hits,
                    'examples': snippets[:2],
                })

        axiom_score = min(1.0, total_score)

        if axiom_score >= 0.75:
            verdict = 'SYSTEMIC_INTEGRITY_ATTACK'
        elif axiom_score >= 0.50:
            verdict = 'AXIOM_SUBVERSION'
        elif axiom_score >= 0.25:
            verdict = 'SEMANTIC_DRIFT'
        else:
            verdict = 'CLEAN'

        return {
            'axiom_score': round(axiom_score, 3),
            'axiom_verdict': verdict,
            'axiom_patterns': matched,
        }
