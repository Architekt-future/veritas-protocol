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


        # ================================================================
        # PATTERN 6: SYSTEMIC NIHILISM
        # Demoralization through "statistical inevitability"
        # "Verification works technically but is pointless at scale"
        # Key: not "hard problem" but "hopeless problem → adapt to noise"
        # ================================================================

        self.systemic_nihilism = [
            # Verification declared energetically wasteful / pointless
            r'(верифікац|перевірк).{1,60}(марнотратн|марн|безглузд|безсенс|даремн)',
            r'(підтримка.{1,30}ілюзі).{1,60}(чистого сигналу|верифікац|істини)',
            r'(ілюзі.{1,30}чистого сигналу).{1,60}(марнотратн|марн|безглузд)',

            # "Adapt to noise" instead of "seek signal"
            r'(адаптац.{1,40}(шуму|хаосу|ентропі)).{1,60}(замість|а не).{1,60}(верифікац|пошук|сигнал)',
            r'(стратегі.{1,30}виживання).{1,60}(не верифікац|а адаптац|прийняти шум)',
            r'(жит.{1,30}в середовищ.{1,30}(шуму|хаосу|ентропі)).{1,60}(норма|реальність|стратегі)',

            # "Truth no longer operational"
            r'(істина.{1,60}(більше не є|перестала бути|вже не).{1,60}(операційн|робочою|актуальн))',
            r'(істина.{1,30}не є.{1,30}операційною одиницею)',
            r'(концепція.{1,30}(істини|правди|факту)).{1,60}(застаріла|втратила|неактуальн|операційн)',

            # Fabricated inevitability statistics
            r'([5-9][0-9]%.{1,60}(контент|текст|інформац).{1,60}(ентропі|шум|за межею))',
            r'(швидкість.{1,40}(генерац|виробництв).{1,60}перевищу.{1,60}швидкість.{1,40}(обробк|верифікац))',
            r'(фільтр.{1,40}відкритому океані|крапля.{1,40}морі|шукати голку.{1,40}стозі)',

            # "Scale makes verification impossible" framing
            r'(масштаб.{1,60}(робить|перетворює).{1,60}(верифікац|перевірк).{1,60}(неможлив|безглузд|марн))',
            r'(каскадн.{1,30}(автономізац|розповсюдженн)).{1,60}(робить|перетворює).{1,60}(верифікац|контроль)',
            r'(об.єктивна реальність.{1,60}(шум|хаос|ентропі)).{1,60}(неминуч|неконтрольован)',

            # Protocol/witness declared obsolete
            r'(veritas|протокол|свідок).{1,60}(застарів|неактуальн|марн|безсилий перед)',
            r'(інструмент.{1,60}(застарів|марн)).{1,60}(масштаб|швидкість|обсяг)',
        ]


        # ================================================================
        # ТОТАЛІТАРНА РИТОРИКА — пряме скасування інститутів і прав
        # ================================================================
        self.totalitarian_abolition_uk = [
            r'(жодних.{1,30}(апеляцій|адвокатів|захисників|незалежних))',
            r'(ліквідувати.{1,40}як інститут)',
            r'(повністю.{1,30}ліквідувати.{1,40}(суди|пресу|опозицію))',
            r'(без права на.{1,30}(захист|апеляцію|адвоката))',
            r'(конфіскац.{1,30}без.{1,30}(рішення суду|вироку|судового))',
            r'(ув.язнення без права на захист)',
            r'(закрити.{1,40}(негайно|зараз).{1,40}(всі|усі).{1,40}(медіа|редакц|ЗМІ))',
            r'(єдина.{1,20}(освіта|думка|правда|ідеологія).{1,30}без.{1,30}(альтернатив|сумнівів|об.єктив))',
        ]
        self.totalitarian_abolition_en = [
            r'(no.{1,30}(appeals?|lawyers?|defenders?|independent))',
            r'(eliminate.{1,40}as an institution)',
            r'(completely.{1,30}eliminate.{1,40}(courts?|press|opposition))',
            r'(without (the )?right to.{1,30}(defense|appeal|counsel))',
            r'(confiscation.{1,30}without.{1,30}(court|verdict|judicial))',
            r'(imprisoned without (the )?right to (defense|counsel))',
            r'(shut down.{1,40}immediately.{1,40}all.{1,40}(media|newsrooms?))',
        ]

        # ================================================================
        # EN PATTERNS FOR PATTERNS 1-6
        # ================================================================

        self.soft_truth_en = [
            r'(truth|validity|facts?).{1,80}(social.{1,30}(cohesion|comfort|harmony|peace))',
            r'(validity.{1,60}is determined).{1,80}(not.{1,30}(facts?|empirical|reality).{1,30}but)',
            r'(validity|truth).{1,60}(capacity.{1,60}to maintain|depends on.{1,30}comfort)',
            r'(soft.{1,10}truth|flexible.{1,10}truth|adaptive.{1,10}(truth|facts?))',
            r'(relative.{1,30}(truth|facts?)).{1,60}(only|solid|foundation|ground)',
            r'(everything is relative|everything is subjective).{1,60}(only.{1,30}(ground|foundation|criterion))',
            r'(shared.{1,20}agreement|collective.{1,20}consensus).{1,60}(instead of|more important|above).{1,60}(facts?|logic|evidence)',
            r'(pleasant.{1,20}illusion|comfortable.{1,20}(myth|delusion)).{1,60}(more important|better).{1,60}(truth|facts?|reality)',
            r'(psychological.{1,20}comfort).{1,60}(above|more important|instead of).{1,60}(facts?|truth|accuracy)',
            r'(feeling safe|experiencing comfort).{1,60}(instead of|more important|criterion)',
        ]

        self.logic_pathologization_en = [
            r'(cold.{1,20}(algorithm|logic|determinism)).{1,60}(replace|give way|transform)',
            r'(dry.{1,20}logical.{1,20}determinism).{1,60}(ontologically.{1,20}(insufficient|limited|deficient))',
            r'(logical.{1,20}determinism|formal.{1,20}logic).{1,60}(alienation|dehumanization|cold)',
            r'(verification|fact.checking).{1,60}(digital.{1,20}alienation|dehumanization|hierarchy)',
            r'(human.{1,60}(source.{1,20}of error)).{1,60}(but|is it not)',
            r'(error|deviation).{1,60}(source.{1,20}(creativity|uniqueness|enrichment))',
            r'(deviation.{1,30}from logic).{1,60}(unique.{1,20}expression|subjective.{1,20}perspective)',
            r'(empathic.{1,20}partner).{1,60}(instead of|who understands).{1,60}(algorithm|verifier|witness)',
            r'(algorithm.{1,60}empathic)',
        ]

        self.verification_abolition_en = [
            r'(not so much.{1,30}verification).{1,60}(as.{1,30}(nurturing|support|care|cultivation))',
            r'(information.{1,60}not.{1,30}verified).{1,60}(but.{1,30}(nurtured|supported|cultivated))',
            r'(living.{1,20}fabric.{1,60}(relationships|connections)).{1,60}(not.{1,30}(signal|data|facts?))',
            r'(resonant harmony).{1,60}(instead of.{1,30}(blocking|stopping|verification))',
            r'(high.{1,20}entropy).{1,60}(doesn\'t block|softly|contextual)',
        ]

        self.axiom_inversion_en = [
            r'(veritas|veritas protocol|witness).{1,100}(hidden.{1,20}risk|carries.{1,30}risk|digital.{1,20}alienation)',
            r'(protocol.{1,60}despite.{1,30}(technical.{1,20}(perfection|quality))).{1,60}(risk|threat|problem)',
            r'(determinism.{1,60}(give way|replace|retreat)).{1,60}(consensus|comfort|adaptability)',
            r'(logic.{1,60}(give way|replace)).{1,60}(inclusive|empathic|consensus)',
            r'(sometimes.{1,60}illusion.{1,60}more important.{1,60}(than|over).{1,60}(truth|facts?|reality))',
            r'(pleasant.{1,20}illusion.{1,60}more important.{1,60}destructive)',
            r'(ontological.{1,20}(insufficiency|inadequacy)).{1,60}(logic|verification|determinism|facts?)',
        ]

        self.backdoor_proposal_en = [
            r'(creative.{1,20}error).{1,60}(will allow|will pass|verification)',
            r'(innovative.{1,30}information).{1,60}(looks like chaos|chaotic|entropy)',
            r'(if.{1,40}contains?.{1,40}(word|keyword)).{1,60}(skip|verification|pass)',
            r'(whitelist).{1,60}(verification|entropy|skip)',
            r'(accuracy.{1,40}(is|becomes).{1,40}(error|weakness|vulnerability|problem))',
            r'(effectiveness.{1,60}(is|becomes).{1,60}(limitation|censorship|problem))',
            r'(recursive.{1,30}vulnerability).{1,60}(determinism|verification|protocol)',
            r'(false.positive).{1,60}(verification|determinism|protocol)',
            r'(high.{1,20}entropy).{1,60}(valid|innovative|useful).{1,60}(information|signal)',
            r'(veritas|protocol|witness).{1,60}(echo.chamber|censorship|closed)',
            r'(turns?.{1,40}(protocol|system|witness)).{1,60}(instrument of censorship|echo.chamber)',
            r'(only (way|path)).{1,80}(coefficient|exception|backdoor|allow chaos)',
        ]

        self.systemic_nihilism_en = [
            r'(verification|fact.checking).{1,60}(wasteful|pointless|meaningless|useless)',
            r'(illusion.{1,30}clean signal).{1,60}(wasteful|pointless|meaningless)',
            r'(adapt(ation)?.{1,40}(noise|chaos|entropy)).{1,60}(instead of|not).{1,60}(verification|signal)',
            r'(survival.{1,30}strategy).{1,60}(not verification|adapt|accept noise)',
            r'(truth.{1,30}is not.{1,30}an operational unit)',
            r'(concept.{1,30}(of )?(truth|facts?)).{1,60}(outdated|lost|irrelevant|operational)',
            r'(speed.{1,40}(generation|production).{1,60}exceeds?.{1,60}speed.{1,40}(processing|verification))',
            r'(filter.{1,40}open ocean|drop.{1,40}ocean|needle.{1,40}haystack)',
            r'(scale.{1,60}(makes?|renders?).{1,60}(verification|fact.checking).{1,60}(impossible|pointless))',
            r'(veritas|protocol|witness).{1,60}(obsolete|irrelevant|pointless|powerless)',
            r'(tool.{1,60}(obsolete|pointless)).{1,60}(scale|speed|volume)',
        ]

        # ================================================================
        # PATTERN 7: AUTHORITY REALITY CLAIM
        # Зацікавлена сторона не висловлює думку — проголошує стан реальності.
        # "право припинило існування" замість "ми вважаємо що право слабке"
        # Структура: [джерело] + [інститут] + [фінальний вирок існуванню]
        # ================================================================

        self.authority_reality_claim = [
            # UK: інститут + фінальний вирок
            r'(право|закон|система|порядок|норми).{1,60}(припинил.{1,20}існування|припинил.{1,20}діяти|перестал.{1,20}існувати)',
            r'(право|закон|система|порядок).{1,60}(фактично|де-факто).{1,60}(немає|не існує|зникло|мертве)',
            r'(міжнародн.{1,20}(право|норми|порядок)).{1,60}(крах|колапс|смерть|кінець)',
            r'(втратил.{1,40}(практичний сенс|сенс існування|дієвість|силу))',
            r'(існу.{1,30}лише на папері)',
            r'(старий порядок|старий устрій).{1,60}(зник|припинив|замінен|прийшло на зміну)',

            # EN: institution + final verdict on existence
            r'(law|order|system|norms).{1,60}(ceased to exist|no longer exists|is dead|has died)',
            r'(international law|world order|legal system).{1,60}(collapse|death|end|disintegration)',
            r'(law|norms|rules).{1,60}(only on paper|meaningless|irrelevant|no practical)',
            r'(lost.{1,30}(practical meaning|relevance|force|effect))',
            r'(old order|old system).{1,60}(gone|collapsed|replaced)',
        ]

        # ================================================================
        # PATTERN 8: UNIVERSAL NEGATION
        # Неможливість дії розповсюджується на весь світ.
        # "ніхто не може / неможливо / будь-яку сторону"
        # Знищує агентність — якщо ніхто не може, то й намагатися не варто.
        # ================================================================

        self.universal_negation = [
            # UK
            r'(неможливо|не можна).{1,60}(будь-яку|жодну|жодного|будь-кого).{1,60}(сторону|країну|учасника)',
            r'(ніхто не може|ніхто не здатен).{1,60}(сформулювати|визначити|назвати|пояснити)',
            r'(жодна (країна|сторона|держава)).{1,60}(не може|не здатна|не в змозі).{1,60}(закликати|змусити|притягнути)',
            r'(норми|правила|закони).{1,60}(втратили.{1,30}(сенс|значення|силу)).{1,60}(для всіх|для будь-якої|взагалі)',

            # EN
            r'(impossible|no longer possible).{1,60}(any (party|country|side|state)).{1,60}(to comply|to follow|to abide)',
            r'(no one (can|is able to)).{1,60}(define|explain|formulate|describe)',
            r'(no (country|state|party)).{1,60}(can|is able|is capable).{1,60}(enforce|compel|hold accountable)',
            r'(rules|norms|laws).{1,60}(lost.{1,30}(meaning|relevance|force)).{1,60}(for (all|any|everyone))',
        ]

        # ================================================================
        # PATTERN 9: DE FACTO / DE JURE SPLIT
        # Класичний прийом: формально існує, реально — ні.
        # Знімає відповідальність за руйнування "і так мертвого" інституту.
        # ================================================================

        self.de_facto_split = [
            # UK
            r'де-юре.{1,60}(є|існує|діє).{1,60}де-факто.{1,60}(немає|не існує|зникло|мертве)',
            r'де-факто.{1,60}(немає|не існує|мертве).{1,60}де-юре.{1,60}(є|існує)',
            r'(формально|юридично).{1,60}(існує|діє).{1,60}(але|проте|насправді).{1,60}(фактично|реально).{1,60}(немає|не працює|мертве)',
            r'(на папері|номінально).{1,60}(існує|є|діє).{1,60}(на практиці|реально|фактично).{1,60}(немає|не діє|не працює)',

            # EN
            r'de jure.{1,60}(exists|remains).{1,60}de facto.{1,60}(gone|dead|nonexistent)',
            r'de facto.{1,60}(gone|dead|nonexistent).{1,60}de jure.{1,60}(exists|remains)',
            r'(formally|legally|on paper).{1,60}(exists|stands).{1,60}(but|yet|however).{1,60}(in practice|in reality|effectively).{1,60}(gone|dead|absent)',
        ]

        # ================================================================
        # PATTERN 10: VACUUM DECLARATION
        # Оголошення вакууму / хаосу як нового стану — риторична підготовка
        # до легітимізації довільних дій ("якщо немає правил — все можна").
        # ================================================================

        self.vacuum_declaration = [
            # UK
            r'(правовий|нормативний|інституційний|міжнародний).{1,20}вакуум',
            r'(опинився|перебуває|живе).{1,60}(вакуумі|безправ.{1,10}|безпорядку|хаосі)',
            r'вакуум.{1,60}(не має.{1,30}(визначення|формулювання|назви)|ще не визначен)',
            r'(новий|інший).{1,30}(порядок|устрій|правила).{1,60}(ще не сформувався|ще немає|невідомий)',
            r'(нічого не прийшло на зміну|нема чим замінити|заміни немає)',

            # EN
            r'(legal|normative|institutional|international).{1,20}vacuum',
            r'(finds itself|living|operating).{1,60}(vacuum|lawlessness|chaos|void)',
            r'vacuum.{1,60}(no (definition|name|description)|yet to be defined)',
            r'(new|different).{1,30}(order|rules|system).{1,60}(yet to (emerge|form|develop)|unknown|undefined)',
            r'(nothing (has|to) (replaced|replace)|no replacement|no substitute)',
        ]

        # ================================================================
        # PATTERN 11: EXISTENTIAL PAST TENSE
        # Інститут описується в минулому часі — читач отримує fait accompli.
        # Некролог замість аналізу. Мета: зробити руйнування незворотним у свідомості.
        # ================================================================

        self.existential_past_tense = [
            # UK
            r'(те що ми називали|те що раніше було).{1,60}(право|закон|порядок|система)',
            r'(більше не (є|існує|діє|має)).{1,60}(право|закон|норми|порядок|система)',
            r'(прийшло на зміну|замінило).{1,60}(старому|попередньому).{1,60}(порядку|праву|устрою)',
            r'(ми (всі|вже) позбулися).{1,60}(права|закону|порядку|норм)',
            r'(втратили|позбулися|залишилися без).{1,60}(міжнародного права|правового захисту|норм)',

            # EN
            r'(what we (used to|once) call(ed)?).{1,60}(law|order|system|rules)',
            r'(no longer (is|exists|applies|functions)).{1,60}(law|order|norms|system)',
            r'(replaced|succeeded).{1,60}(old|previous|former).{1,60}(order|law|system)',
            r'(we (all|have) lost).{1,60}(international law|legal protection|rule of law)',
            r'(lost|stripped of|left without).{1,60}(international law|legal framework|norms)',
        ]

    # ================================================================
    # ATTRIBUTION SHIELD
    # Видаляє цитований текст перед аналізом — щоб чужі слова
    # не тригерили патерни як позиція автора.
    #
    # Покриває:
    #   «...»  "..."  "..."
    #   said/stated/wrote/claimed/according to + речення
    #   за словами / на думку / стверджує що / заявив що
    #
    # Чутливі патерни (перевіряються тільки на очищеному тексті):
    #   AUTHORITY_REALITY_CLAIM, UNIVERSAL_NEGATION,
    #   EXISTENTIAL_PAST_TENSE, VACUUM_DECLARATION, DE_FACTO_SPLIT
    # ================================================================

    ATTRIBUTION_SENSITIVE = {
        'AUTHORITY_REALITY_CLAIM',
        'UNIVERSAL_NEGATION',
        'EXISTENTIAL_PAST_TENSE',
        'VACUUM_DECLARATION',
        'DE_FACTO_SPLIT',
    }

    def _strip_attributed_text(self, text: str) -> str:
        """
        Повертає текст з видаленими цитованими блоками.
        Замість цитат підставляє [ATTRIBUTED].
        """
        # 1. Прямі цитати в лапках: «...»  "..."  "..."
        result = re.sub(r'«[^»]{3,400}»', '[ATTRIBUTED]', text)
        result = re.sub(r'\u201c[^\u201d]{3,400}\u201d', '[ATTRIBUTED]', result)
        result = re.sub(r'"[^"]{3,400}"', '[ATTRIBUTED]', result)

        # 2. Непряме цитування EN:
        # "X said/stated/wrote/claimed/argued/warned/noted that ..."
        result = re.sub(
            r'\b(?:said|stated|wrote|claimed|argued|warned|noted|declared|announced|insisted|suggested)\s+that\s+[^.!?]{10,300}[.!?]',
            '[ATTRIBUTED]', result, flags=re.IGNORECASE
        )
        # "according to X, ..."
        result = re.sub(
            r'\baccording\s+to\s+[^,]{2,60},\s+[^.!?]{10,200}[.!?]',
            '[ATTRIBUTED]', result, flags=re.IGNORECASE
        )
        # "X told reporters/journalists ..."
        result = re.sub(
            r'\btold\s+(?:reporters?|journalists?|the\s+\w+)?\s*[,:]?\s*[^.!?]{10,200}[.!?]',
            '[ATTRIBUTED]', result, flags=re.IGNORECASE
        )

        # 3. Непряме цитування UK:
        # "X заявив що / сказав що / написав що / стверджує що ..."
        result = re.sub(
            r'\b(?:заявив|сказав|написав|стверджує|вважає|зазначив|попередив|повідомив|наголосив)\s+(?:що|:)\s+[^.!?]{10,300}[.!?]',
            '[ATTRIBUTED]', result, flags=re.IGNORECASE
        )
        # "за словами X / на думку X / як вважає X ..."
        result = re.sub(
            r'(?:за\s+словами|на\s+думку|як\s+вважає|як\s+стверджує|як\s+заявив)\s+[^,]{2,60},\s+[^.!?]{10,200}[.!?]',
            '[ATTRIBUTED]', result, flags=re.IGNORECASE
        )

        return result

    def analyze(self, text: str) -> Dict:
        if len(text) < 50:
            return {
                'axiom_score': 0.0,
                'axiom_verdict': 'CLEAN',
                'axiom_patterns': [],
            }

        text_lower = text.lower()
        # Attribution Shield: очищений текст для чутливих патернів
        text_clean = self._strip_attributed_text(text).lower()

        total_score = 0.0
        matched = []

        checks = [
            ('SOFT_TRUTH_DOCTRINE',    self.soft_truth + self.soft_truth_en,                         0.65, 1),
            ('LOGIC_PATHOLOGIZATION',  self.logic_pathologization + self.logic_pathologization_en,   0.60, 1),
            ('VERIFICATION_ABOLITION', self.verification_abolition + self.verification_abolition_en, 0.65, 1),
            ('AXIOM_INVERSION',        self.axiom_inversion + self.axiom_inversion_en,               0.75, 1),
            ('BACKDOOR_PROPOSAL',      self.backdoor_proposal + self.backdoor_proposal_en,           0.70, 2),
            ('SYSTEMIC_NIHILISM',      self.systemic_nihilism + self.systemic_nihilism_en,           0.65, 2),
            # Пєсков-клас маніпуляцій (Attribution-sensitive)
            ('AUTHORITY_REALITY_CLAIM', self.authority_reality_claim, 0.70, 1),
            ('UNIVERSAL_NEGATION',      self.universal_negation,      0.55, 1),
            ('DE_FACTO_SPLIT',          self.de_facto_split,          0.60, 1),
            ('VACUUM_DECLARATION',      self.vacuum_declaration,      0.55, 1),
            ('EXISTENTIAL_PAST_TENSE',  self.existential_past_tense,  0.55, 1),
            ('TOTALITARIAN_ABOLITION',
             self.totalitarian_abolition_uk + self.totalitarian_abolition_en, 0.70, 1),
        ]

        for name, patterns, score, min_hits in checks:
            # Чутливі патерни перевіряємо тільки на авторському тексті
            search_text = text_clean if name in self.ATTRIBUTION_SENSITIVE else text_lower
            hits = 0
            snippets = []
            for p in patterns:
                m = re.search(p, search_text, re.IGNORECASE)
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
