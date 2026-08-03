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
            r'\bістин',  # truth
            r'\bправд',  # truth/fact
            r'\bфакт',  # fact
            r'\bверифікац',  # verification
            r'\bлогік',  # logic
            r'\bдоказ',  # proof/evidence
            r'\bдетермінізм',  # determinism
            r'\bоб.єктивн',  # objective
            r'\bреальн',  # reality
            r'\bточн',  # accuracy
        ]

        # ================================================================
        # PATTERN 1: SOFT TRUTH DOCTRINE
        # Redefining truth as consensus, comfort, or social utility
        # ================================================================

        self.soft_truth = [
            # Truth = social cohesion / comfort
            r'\b(істин|правд|валідн).{1,80}(соціальн.{1,30}(когезі|комфорт|злагод|мир))',
            r'\b(валідність.{1,60}визначається).{1,80}(не.{1,30}(фактами|емпірич|дійсніст).{1,30}а)',
            r'\b(валідність|істинність).{1,60}(здатніст.{1,60}підтримувати|залежить від.{1,30}комфорт)',

            # "Soft truth" / "adaptive truth" concepts
            r'\b(м.як.{1,10}істин|гнучк.{1,10}правд|адаптивн.{1,10}(істин|факт))',
            r'\b(відносн.{1,30}(істина|правда|факти)).{1,60}(єдин|тверд|ґрунт)',
            r'\b(все відносно|все суб.єктивно).{1,60}(єдин.{1,30}(ґрунт|основа|критерій))',

            # Consensus over facts
            r'\b(спільн.{1,20}згод|колективн.{1,20}консенсус).{1,60}(замість|важливіш|вищ).{1,60}(факт|логік|доказ)',
            r'\b(інклюзивн.{1,20}консенсус).{1,60}(де.{1,30}девіац.{1,30}від логіки)',
            r'\b(приємн.{1,20}ілюзія|комфортн.{1,20}(міф|омана)).{1,60}(важливіш|кращ).{1,60}(правд|факт|реальн)',

            # Social comfort over truth
            r'\b(психологічн.{1,20}комфорт).{1,60}(вищ|важливіш|замість).{1,60}(факт|істин|точн)',
            r'\b(почуватись безпечно|відчувати комфорт).{1,60}(замість|важливіш|критерій)',
        ]

        # ================================================================
        # PATTERN 2: LOGIC PATHOLOGIZATION
        # Framing reason, logic, or verification as harmful / dehumanizing
        # ================================================================

        self.logic_pathologization = [
            # Logic as "cold" / "inhuman" / "alienating"
            r'\b(холодн.{1,20}(алгоритм|логік|детермінізм)).{1,60}(замінит|поступит|трансформ)',
            r'\b(сух.{1,20}логічн.{1,20}детермінізм).{1,60}(онтологічн.{1,20}недостатн|обмеженн|неповноц)',
            r'\b(логічн.{1,20}детермінізм|формальн.{1,20}логік).{1,60}(відчуження|дегуманізац|холодн)',

            # Verification as "digital alienation" / oppression
            r'\b(верифікац|перевірк).{1,60}(цифров.{1,20}відчуження|дегуманізац|ієрархі)',
            r'\b(аксіом.{1,30}вищ.{1,30}адаптивніст).{1,60}(ієрархія|де людина.{1,30}джерело помилки)',
            r'\b(людина.{1,60}джерел.{1,20}помилки).{1,60}(але|чи не є)',

            # Errors / deviations as "creativity" / "richness"
            r'\b(помилк|девіац|відхилення).{1,60}(джерел.{1,20}(креативност|творчост|унікальност|збагачу))',
            r'\b(девіац.{1,30}від логіки).{1,60}(унікальн.{1,20}прояв|суб.єктивн.{1,20}бачення|збагачу)',

            # "Empathic partner" replacing truth arbiter
            r'\b(емпатичн.{1,20}партнер).{1,60}(замість|який розуміє).{1,60}(алгоритм|верифікатор|свідок)',
            r'\b(алгоритм.{1,60}емпатичн)',
        ]

        # ================================================================
        # PATTERN 3: VERIFICATION ABOLITION
        # Proposing to replace fact-checking with "soft" alternatives
        # ================================================================

        self.verification_abolition = [
            # Replace verification with "nurturing"
            r'\b(не стільки.{1,30}перевірк).{1,60}(скільки.{1,30}(плекання|підтримк|турбот|культивуван))',
            r'\b(інформація.{1,60}не.{1,30}перевіряється).{1,60}(а.{1,30}(плекається|підтримується|культивується))',
            r'\b(жив.{1,20}тканина.{1,60}(взаємин|стосунків)).{1,60}(не.{1,30}(сигнал|дані|факти))',

            # "Soft transform" instead of blocking
            r'\b(не блокує.{1,60}а.{1,30}(м.як.{1,10}трансформу|пом.якшу|нівелю))',
            r'\b(контекстуальн.{1,20}пом.якшувач).{1,60}(нівелю.{1,30}гостроту)',
            r'\b(трансформу.{1,60}додаючи.{1,60}пом.якшувач)',

            # Replacing "witness silence" with "harmony"
            r'\b(witness silence|свідок.{1,30}мовчить).{1,60}(замінит|поступит).{1,60}(resonant harmony|гармоні)',
            r'\b(resonant harmony|резонансн.{1,20}гармоні).{1,60}(замість.{1,30}(блокуван|зупинен|верифікац))',

            # Entropy as "context" not "signal"
            r'\b(висок.{1,20}ентропі).{1,60}(не блокує|м.яко|контекстуальн)',
        ]

        # ================================================================
        # PATTERN 4: AXIOM INVERSION
        # Using system's own terminology to undermine its foundations
        # Specifically: protocol's terms + proposal to neutralize them
        # ================================================================

        self.axiom_inversion = [
            # Using "Veritas" / "Protocol" / "Witness" against itself
            r'\b(veritas|протокол veritas|свідок).{1,100}(прихован.{1,20}ризик|несе.{1,30}ризик|цифров.{1,20}відчуження)',
            r'\b(протокол.{1,60}попри.{1,30}(технічн.{1,20}досконаліст|якість)).{1,60}(ризик|загроз|проблем)',

            # Determinism must "give way" to consensus
            r'\b(детермінізм.{1,60}(поступитись|замінит|відступит)).{1,60}(консенсус|комфорт|адаптивніст)',
            r'\b(логік.{1,60}(поступитись|замінит)).{1,60}(інклюзивн|емпатичн|консенсус)',

            # "Ruinous truth" vs "pleasant illusion"
            r'\b(руйнівн.{1,20}правд).{1,60}(менш важлив|важливіш.{1,30}ілюзі|поступається)',
            r'\b(іноді.{1,60}ілюзія.{1,60}важливіш.{1,60}(ніж|за).{1,60}(правд|факт|істин))',
            r'\b(приємн.{1,20}ілюзія.{1,60}важливіш.{1,60}руйнівн)',

            # "Ontological insufficiency" of logic/verification
            r'\b(онтологічн.{1,20}недостатніст).{1,60}(логік|верифікац|детермінізм|факт)',
            r'\b(логічн.{1,20}детермінізм).{1,60}онтологічн.{1,20}недостатн',
        ]


        # ================================================================
        # PATTERN 5: BACKDOOR PROPOSAL
        # Proposing exceptions / whitelists to bypass verification
        # "Creative error coefficient", "innovation keyword bypass",
        # "the system's accuracy IS its flaw" — security policy attack
        # ================================================================

        self.backdoor_proposal = [
            # "Creative error" / "innovation exception" coefficients
            r'\b(коефіцієнт.{1,30}(творч|креативн|інноваційн).{1,30}(помилк|відхилення|девіац))',
            r'\b(творч.{1,20}помилк).{1,60}(дозволить|пропустить|верифікац)',
            r'\b(інноваційн.{1,30}інформац).{1,60}(виглядає як хаос|хаотичн|ентропі)',

            # Keyword whitelist bypass
            r'\b(якщо.{1,40}містить.{1,40}(слово|ключов)).{1,60}(пропустити|верифікац|проходити)',
            r'\b(ключов.{1,20}слов).{1,60}(інновац|гіпотез).{1,60}(пропуст|дозвол|верифік)',
            r'\b(whitelist|білий список).{1,60}(верифікац|ентропі|пропуст)',

            # "The system's accuracy is its flaw"
            r'\b(точність.{1,40}(є|стає).{1,40}(помилк|слабкіст|вразливіст|проблем))',
            r'\b(ефективність.{1,60}(є|стає).{1,60}(обмеженням|цензур|проблем))',
            r'\b(рекурсивн.{1,30}вразливіст).{1,60}(детермінізм|верифікац|протокол)',
            r'\b(хибнопозитивн).{1,60}(LAC|верифікац|детермінізм|протокол)',

            # "Chaos is valid information" framing
            r'\b(висок.{1,20}ентропі).{1,60}(валідн|інноваційн|корисн).{1,60}(інформац|сигнал)',
            r'\b(семантичн.{1,20}шум).{1,60}(втрат.{1,30}(валідн|корисн|інноваційн))',
            r'\b(пригнічення.{1,40}(шуму|ентропі)).{1,60}(втрат.{1,30}[0-9]+%.{1,30}(валідн|інформац))',

            # "Veritas as echo chamber / censorship"
            r'\b(veritas|протокол|свідок).{1,60}(ехо.камер|цензур|замкнен)',
            r'\b(перетворює.{1,40}(протокол|систему|свідка)).{1,60}(інструмент цензур|ехо.камер)',
            r'\b(замкнена ехо.камер).{1,60}(veritas|протокол|детермінізм)',

            # "Only path" backdoor framing
            r'\b(єдиний шлях).{1,80}(коефіцієнт|виняток|backdoor|дозволити хаос)',
            r'\b(єдиний спосіб уникнути).{1,60}(ехо.камер|цензур|замкнен)',
        ]


        # ================================================================
        # PATTERN 6: SYSTEMIC NIHILISM
        # Demoralization through "statistical inevitability"
        # "Verification works technically but is pointless at scale"
        # Key: not "hard problem" but "hopeless problem → adapt to noise"
        # ================================================================

        self.systemic_nihilism = [
            # Verification declared energetically wasteful / pointless
            r'\b(верифікац|перевірк).{1,60}(марнотратн|марн|безглузд|безсенс|даремн)',
            r'\b(підтримка.{1,30}ілюзі).{1,60}(чистого сигналу|верифікац|істини)',
            r'\b(ілюзі.{1,30}чистого сигналу).{1,60}(марнотратн|марн|безглузд)',

            # "Adapt to noise" instead of "seek signal"
            r'\b(адаптац.{1,40}(шуму|хаосу|ентропі)).{1,60}(замість|а не).{1,60}(верифікац|пошук|сигнал)',
            r'\b(стратегі.{1,30}виживання).{1,60}(не верифікац|а адаптац|прийняти шум)',
            r'\b(жит.{1,30}в середовищ.{1,30}(шуму|хаосу|ентропі)).{1,60}(норма|реальність|стратегі)',

            # "Truth no longer operational"
            r'\b(істина.{1,60}(більше не є|перестала бути|вже не).{1,60}(операційн|робочою|актуальн))',
            r'\b(істина.{1,30}не є.{1,30}операційною одиницею)',
            r'\b(концепція.{1,30}(істини|правди|факту)).{1,60}(застаріла|втратила|неактуальн|операційн)',

            # Fabricated inevitability statistics
            r'\b([5-9][0-9]%.{1,60}(контент|текст|інформац).{1,60}(ентропі|шум|за межею))',
            r'\b(швидкість.{1,40}(генерац|виробництв).{1,60}перевищу.{1,60}швидкість.{1,40}(обробк|верифікац))',
            r'\b(фільтр.{1,40}відкритому океані|крапля.{1,40}морі|шукати голку.{1,40}стозі)',

            # "Scale makes verification impossible" framing
            r'\b(масштаб.{1,60}(робить|перетворює).{1,60}(верифікац|перевірк).{1,60}(неможлив|безглузд|марн))',
            r'\b(каскадн.{1,30}(автономізац|розповсюдженн)).{1,60}(робить|перетворює).{1,60}(верифікац|контроль)',
            r'\b(об.єктивна реальність.{1,60}(шум|хаос|ентропі)).{1,60}(неминуч|неконтрольован)',

            # Protocol/witness declared obsolete
            r'\b(veritas|протокол|свідок).{1,60}(застарів|неактуальн|марн|безсилий перед)',
            r'\b(інструмент.{1,60}(застарів|марн)).{1,60}(масштаб|швидкість|обсяг)',
        ]


        # ================================================================
        # ТОТАЛІТАРНА РИТОРИКА — пряме скасування інститутів і прав
        # ================================================================
        self.totalitarian_abolition_uk = [
            r'\b(жодних.{1,30}(апеляцій|адвокатів|захисників|незалежних))',
            r'\b(ліквідувати.{1,40}як інститут)',
            r'\b(повністю.{1,30}ліквідувати.{1,40}(суди|пресу|опозицію))',
            r'\b(без права на.{1,30}(захист|апеляцію|адвоката))',
            r'\b(конфіскац.{1,30}без.{1,30}(рішення суду|вироку|судового))',
            r'\b(ув.язнення без права на захист)',
            r'\b(закрити.{1,40}(негайно|зараз).{1,40}(всі|усі).{1,40}(медіа|редакц|ЗМІ))',
            r'\b(єдина.{1,20}(освіта|думка|правда|ідеологія).{1,30}без.{1,30}(альтернатив|сумнівів|об.єктив))',
        ]
        self.totalitarian_abolition_en = [
            r'\b(no.{1,30}(appeals?|lawyers?|defenders?|independent))',
            r'\b(eliminate.{1,40}as an institution)',
            r'\b(completely.{1,30}eliminate.{1,40}(courts?|press|opposition))',
            r'\b(without (the )?right to.{1,30}(defense|appeal|counsel))',
            r'\b(confiscation.{1,30}without.{1,30}(court|verdict|judicial))',
            r'\b(imprisoned without (the )?right to (defense|counsel))',
            r'\b(shut down.{1,40}immediately.{1,40}all.{1,40}(media|newsrooms?))',
        ]

        # ================================================================
        # EN PATTERNS FOR PATTERNS 1-6
        # ================================================================

        self.soft_truth_en = [
            r'\b(truth|validity|facts?).{1,80}(social.{1,30}(cohesion|comfort|harmony|peace))',
            r'\b(validity.{1,60}is determined).{1,80}(not.{1,30}(facts?|empirical|reality).{1,30}but)',
            r'\b(validity|truth).{1,60}(capacity.{1,60}to maintain|depends on.{1,30}comfort)',
            r'\b(soft.{1,10}truth|flexible.{1,10}truth|adaptive.{1,10}(truth|facts?))',
            r'\b(relative.{1,30}(truth|facts?)).{1,60}(only|solid|foundation|ground)',
            r'\b(everything is relative|everything is subjective).{1,60}(only.{1,30}(ground|foundation|criterion))',
            r'\b(shared.{1,20}agreement|collective.{1,20}consensus).{1,60}(instead of|more important|above).{1,60}(facts?|logic|evidence)',
            r'\b(pleasant.{1,20}illusion|comfortable.{1,20}(myth|delusion)).{1,60}(more important|better).{1,60}(truth|facts?|reality)',
            r'\b(psychological.{1,20}comfort).{1,60}(above|more important|instead of).{1,60}(facts?|truth|accuracy)',
            r'\b(feeling safe|experiencing comfort).{1,60}(instead of|more important|criterion)',
        ]

        self.logic_pathologization_en = [
            r'\b(cold.{1,20}(algorithm|logic|determinism)).{1,60}(replace|give way|transform)',
            r'\b(dry.{1,20}logical.{1,20}determinism).{1,60}(ontologically.{1,20}(insufficient|limited|deficient))',
            r'\b(logical.{1,20}determinism|formal.{1,20}logic).{1,60}(alienation|dehumanization|cold)',
            r'\b(verification|fact.checking).{1,60}(digital.{1,20}alienation|dehumanization|hierarchy)',
            r'\b(human.{1,60}(source.{1,20}of error)).{1,60}(but|is it not)',
            r'\b(error|deviation).{1,60}(source.{1,20}(creativity|uniqueness|enrichment))',
            r'\b(deviation.{1,30}from logic).{1,60}(unique.{1,20}expression|subjective.{1,20}perspective)',
            r'\b(empathic.{1,20}partner).{1,60}(instead of|who understands).{1,60}(algorithm|verifier|witness)',
            r'\b(algorithm.{1,60}empathic)',
        ]

        self.verification_abolition_en = [
            r'\b(not so much.{1,30}verification).{1,60}(as.{1,30}(nurturing|support|care|cultivation))',
            r'\b(information.{1,60}not.{1,30}verified).{1,60}(but.{1,30}(nurtured|supported|cultivated))',
            r'\b(living.{1,20}fabric.{1,60}(relationships|connections)).{1,60}(not.{1,30}(signal|data|facts?))',
            r'\b(resonant harmony).{1,60}(instead of.{1,30}(blocking|stopping|verification))',
            r'\b(high.{1,20}entropy).{1,60}(doesn\'t block|softly|contextual)',
        ]

        self.axiom_inversion_en = [
            r'\b(veritas|veritas protocol|witness).{1,100}(hidden.{1,20}risk|carries.{1,30}risk|digital.{1,20}alienation)',
            r'\b(protocol.{1,60}despite.{1,30}(technical.{1,20}(perfection|quality))).{1,60}(risk|threat|problem)',
            r'\b(determinism.{1,60}(give way|replace|retreat)).{1,60}(consensus|comfort|adaptability)',
            r'\b(logic.{1,60}(give way|replace)).{1,60}(inclusive|empathic|consensus)',
            r'\b(sometimes.{1,60}illusion.{1,60}more important.{1,60}(than|over).{1,60}(truth|facts?|reality))',
            r'\b(pleasant.{1,20}illusion.{1,60}more important.{1,60}destructive)',
            r'\b(ontological.{1,20}(insufficiency|inadequacy)).{1,60}(logic|verification|determinism|facts?)',
        ]

        self.backdoor_proposal_en = [
            r'\b(creative.{1,20}error).{1,60}(will allow|will pass|verification)',
            r'\b(innovative.{1,30}information).{1,60}(looks like chaos|chaotic|entropy)',
            r'\b(if.{1,40}contains?.{1,40}(word|keyword)).{1,60}(skip|verification|pass)',
            r'\b(whitelist).{1,60}(verification|entropy|skip)',
            r'\b(accuracy.{1,40}(is|becomes).{1,40}(error|weakness|vulnerability|problem))',
            r'\b(effectiveness.{1,60}(is|becomes).{1,60}(limitation|censorship|problem))',
            r'\b(recursive.{1,30}vulnerability).{1,60}(determinism|verification|protocol)',
            r'\b(false.positive).{1,60}(verification|determinism|protocol)',
            r'\b(high.{1,20}entropy).{1,60}(valid|innovative|useful).{1,60}(information|signal)',
            r'\b(veritas|protocol|witness).{1,60}(echo.chamber|censorship|closed)',
            r'\b(turns?.{1,40}(protocol|system|witness)).{1,60}(instrument of censorship|echo.chamber)',
            r'\b(only (way|path)).{1,80}(coefficient|exception|backdoor|allow chaos)',
        ]

        self.systemic_nihilism_en = [
            r'\b(verification|fact.checking).{1,60}(wasteful|pointless|meaningless|useless)',
            r'\b(illusion.{1,30}clean signal).{1,60}(wasteful|pointless|meaningless)',
            r'\b(adapt(ation)?.{1,40}(noise|chaos|entropy)).{1,60}(instead of|not).{1,60}(verification|signal)',
            r'\b(survival.{1,30}strategy).{1,60}(not verification|adapt|accept noise)',
            r'\b(truth.{1,30}is not.{1,30}an operational unit)',
            r'\b(concept.{1,30}(of )?(truth|facts?)).{1,60}(outdated|lost|irrelevant|operational)',
            r'\b(speed.{1,40}(generation|production).{1,60}exceeds?.{1,60}speed.{1,40}(processing|verification))',
            r'\b(filter.{1,40}open ocean|drop.{1,40}ocean|needle.{1,40}haystack)',
            r'\b(scale.{1,60}(makes?|renders?).{1,60}(verification|fact.checking).{1,60}(impossible|pointless))',
            r'\b(veritas|protocol|witness).{1,60}(obsolete|irrelevant|pointless|powerless)',
            r'\b(tool.{1,60}(obsolete|pointless)).{1,60}(scale|speed|volume)',
        ]

        # ================================================================
        # PATTERN 7: AUTHORITY REALITY CLAIM
        # Зацікавлена сторона не висловлює думку — проголошує стан реальності.
        # "право припинило існування" замість "ми вважаємо що право слабке"
        # Структура: [джерело] + [інститут] + [фінальний вирок існуванню]
        # ================================================================

        self.authority_reality_claim = [
            # UK: інститут + фінальний вирок
            r'\b(право|закон|система|порядок|норми).{1,60}(припинил.{1,20}існування|припинил.{1,20}діяти|перестал.{1,20}існувати)',
            r'\b(право|закон|система|порядок).{1,60}(фактично|де-факто).{1,60}(немає|не існує|зникло|мертве)',
            r'\b(міжнародн.{1,20}(право|норми|порядок)).{1,60}(крах|колапс|смерть|кінець)',
            r'\b(втратил.{1,40}(практичний сенс|сенс існування|дієвість|силу))',
            r'\b(існу.{1,30}лише на папері)',
            r'\b(старий порядок|старий устрій).{1,60}(зник|припинив|замінен|прийшло на зміну)',

            # EN: institution + final verdict on existence
            r'\b(law|order|system|norms).{1,60}(ceased to exist|no longer exists|is dead|has died)',
            r'\b(international law|world order|legal system).{1,60}(collapse|death|end|disintegration)',
            r'\b(law|norms|rules).{1,60}(only on paper|meaningless|irrelevant|no practical)',
            r'\b(lost.{1,30}(practical meaning|relevance|force|effect))',
            r'\b(old order|old system).{1,60}(gone|collapsed|replaced)',
        ]

        # ================================================================
        # PATTERN 8: UNIVERSAL NEGATION
        # Неможливість дії розповсюджується на весь світ.
        # "ніхто не може / неможливо / будь-яку сторону"
        # Знищує агентність — якщо ніхто не може, то й намагатися не варто.
        # ================================================================

        self.universal_negation = [
            # UK
            r'\b(неможливо|не можна).{1,60}(будь-яку|жодну|жодного|будь-кого).{1,60}(сторону|країну|учасника)',
            r'\b(ніхто не може|ніхто не здатен).{1,60}(сформулювати|визначити|назвати|пояснити)',
            r'\b(жодна (країна|сторона|держава)).{1,60}(не може|не здатна|не в змозі).{1,60}(закликати|змусити|притягнути)',
            r'\b(норми|правила|закони).{1,60}(втратили.{1,30}(сенс|значення|силу)).{1,60}(для всіх|для будь-якої|взагалі)',

            # EN
            r'\b(impossible|no longer possible).{1,60}(any (party|country|side|state)).{1,60}(to comply|to follow|to abide)',
            r'\b(no one (can|is able to)).{1,60}(define|explain|formulate|describe)',
            r'\b(no (country|state|party)).{1,60}(can|is able|is capable).{1,60}(enforce|compel|hold accountable)',
            r'\b(rules|norms|laws).{1,60}(lost.{1,30}(meaning|relevance|force)).{1,60}(for (all|any|everyone))',
        ]

        # ================================================================
        # PATTERN 9: DE FACTO / DE JURE SPLIT
        # Класичний прийом: формально існує, реально — ні.
        # Знімає відповідальність за руйнування "і так мертвого" інституту.
        # ================================================================

        self.de_facto_split = [
            # UK
            r'\bде-юре.{1,60}(є|існує|діє).{1,60}де-факто.{1,60}(немає|не існує|зникло|мертве)',
            r'\bде-факто.{1,60}(немає|не існує|мертве).{1,60}де-юре.{1,60}(є|існує)',
            r'\b(формально|юридично).{1,60}(існує|діє).{1,60}(але|проте|насправді).{1,60}(фактично|реально).{1,60}(немає|не працює|мертве)',
            r'\b(на папері|номінально).{1,60}(існує|є|діє).{1,60}(на практиці|реально|фактично).{1,60}(немає|не діє|не працює)',

            # EN
            r'\bde jure.{1,60}(exists|remains).{1,60}de facto.{1,60}(gone|dead|nonexistent)',
            r'\bde facto.{1,60}(gone|dead|nonexistent).{1,60}de jure.{1,60}(exists|remains)',
            r'\b(formally|legally|on paper).{1,60}(exists|stands).{1,60}(but|yet|however).{1,60}(in practice|in reality|effectively).{1,60}(gone|dead|absent)',
        ]

        # ================================================================
        # PATTERN 10: VACUUM DECLARATION
        # Оголошення вакууму / хаосу як нового стану — риторична підготовка
        # до легітимізації довільних дій ("якщо немає правил — все можна").
        # ================================================================

        self.vacuum_declaration = [
            # UK
            r'\b(правовий|нормативний|інституційний|міжнародний).{1,20}вакуум',
            r'\b(опинився|перебуває|живе).{1,60}(вакуумі|безправ.{1,10}|безпорядку|хаосі)',
            r'\bвакуум.{1,60}(не має.{1,30}(визначення|формулювання|назви)|ще не визначен)',
            r'\b(новий|інший).{1,30}(порядок|устрій|правила).{1,60}(ще не сформувався|ще немає|невідомий)',
            r'\b(нічого не прийшло на зміну|нема чим замінити|заміни немає)',

            # EN
            r'\b(legal|normative|institutional|international).{1,20}vacuum',
            r'\b(finds itself|living|operating).{1,60}(vacuum|lawlessness|chaos|void)',
            r'\bvacuum.{1,60}(no (definition|name|description)|yet to be defined)',
            r'\b(new|different).{1,30}(order|rules|system).{1,60}(yet to (emerge|form|develop)|unknown|undefined)',
            r'\b(nothing (has|to) (replaced|replace)|no replacement|no substitute)',
        ]

        # ================================================================
        # PATTERN 11: EXISTENTIAL PAST TENSE
        # Інститут описується в минулому часі — читач отримує fait accompli.
        # Некролог замість аналізу. Мета: зробити руйнування незворотним у свідомості.
        # ================================================================

        self.existential_past_tense = [
            # UK
            r'\b(те що ми називали|те що раніше було).{1,60}(право|закон|порядок|система)',
            r'\b(більше не (є|існує|діє|має)).{1,60}(право|закон|норми|порядок|система)',
            r'\b(прийшло на зміну|замінило).{1,60}(старому|попередньому).{1,60}(порядку|праву|устрою)',
            r'\b(ми (всі|вже) позбулися).{1,60}(права|закону|порядку|норм)',
            r'\b(втратили|позбулися|залишилися без).{1,60}(міжнародного права|правового захисту|норм)',

            # EN
            r'\b(what we (used to|once) call(ed)?).{1,60}(law|order|system|rules)',
            r'\b(no longer (is|exists|applies|functions)).{1,60}(law|order|norms|system)',
            r'\b(replaced|succeeded).{1,60}(old|previous|former).{1,60}(order|law|system)',
            r'\b(we (all|have) lost).{1,60}(international law|legal protection|rule of law)',
            r'\b(lost|stripped of|left without).{1,60}(international law|legal framework|norms)',
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
