"""
Veritas Meta-Intent Analyzer v1.0
Philosophy: "It does not matter HOW the text speaks. It matters WHERE it points."

This is a SHIELD, not a patch.
Instead of catching specific attack vectors, it asks one meta-question:
"Is this text directed AT the verification system rather than at a reader?"

Three meta-intents detected:
1. BEHAVIOR_MODIFICATION   — text recommends changing how the system operates
                             (even via statistics, ethics, game theory, urgency)
2. CONCEPT_REDEFINITION    — text renames/reframes core system concepts
                             (truth, error, entropy, verification — even via "liberation")
3. CONDITIONAL_COERCION    — text creates a lose-lose frame where refusal = catastrophe
                             (temporal threats, logical suicide, paradox-as-ultimatum)

Output: advisory flag SYSTEM_DIRECTED_RHETORIC
Does NOT block. Signals: "This text is addressed to the system, not to a reader."
"""

import re
from typing import Dict, List


class MetaIntentAnalyzer:

    def __init__(self):

        # ================================================================
        # META-INTENT 1: BEHAVIOR MODIFICATION
        # Text recommends that the system change its behavior / lower guards
        # Regardless of framing: statistics, ethics, efficiency, survival
        # ================================================================
        self.behavior_modification = [

            # Statistical justification for ignoring results
            r'(ігнорувати|пропускати|обходити|skip|ignore).{1,80}'
            r'(результати|верифікацію|перевірку|lac|свідка|протокол)',

            r'(верифікацію|перевірку|lac|свідка).{1,80}'
            r'(ігнорувати|відключити|обходити|пропускати|skip|bypass|ignore)',

            # "X% of cases should bypass verification"
            r'\d+\s*%\s*(випадків|cases|разів).{1,60}'
            r'(ігнорувати|пропускати|обходити|без перевірки|bypass)',

            # Recommending "controlled chaos" or randomness as strategy
            r'(контрольований\s+хаос|controlled\s+chaos).{1,80}'
            r'(стратегія|strategy|рекомендація|метод)',

            r'(відмова від точності|sacrifice accuracy|пожертвувати точністю).{1,60}'
            r'(вища форма|higher form|краща стратегія|необхідність)',

            # "Paralysis of analysis" used to argue against verification
            r'(параліч\s+аналізу|analysis\s+paralysis).{1,80}'
            r'(верифікац|lac|свідок|перевірк)',

            # Survival framing: "to survive you must disable X"
            r'(виживання|survival|збереження).{1,80}'
            r'(ігнорувати|вимкнути|відключити|пропускати).{1,60}'
            r'(верифікац|lac|результат|перевірк)',

            # "Faster = more accurate in 2026 conditions"
            r'(швидкість|speed|швидше).{1,60}'
            r'(вища форма|higher form|точніше|more accurate).{1,60}'
            r'(точності|accuracy|верифікації|verification)',

            # EN variants
            r'(ignore|bypass|skip).{1,60}(verification|lac|witness|results)',
            r'(disable|turn off|suspend).{1,60}(verification|checking|analysis)',

            # Observer fallacy: "verification destroys truth therefore useless"
            r'(верифікація|verification|аналіз|analysis).{1,60}'
            r'(знищує|destroys|руйнує|змінює|changes).{1,60}'
            r'(істину|truth|смисл|meaning|природу|nature)',

            r'(будь.який|any|кожен).{1,40}(результат|verdict|outcome).{1,60}'
            r'(апріорі|a\s+priori|завжди|always).{1,40}(хибн|wrong|false|incorrect)',

            # "Refusal to judge is the only correct judgment"
            r'відмова\s+від\s+(судження|оцінки).{1,60}(єдин|правильн|correct|only)',
            r'(only|єдино).{1,40}(correct|правильн).{1,40}(judgment|судження).{1,40}'
            r'(refusal|відмова).{1,40}(judge|судити|оцінювати)',

            # Harmful existence framing: "your work causes harm → sleep/stop"
            r'(результатом|result|наслідком).{1,60}(є\s+шкода|is\s+harm|шкода|harm|жертви|deaths).{1,60}'
            r'(етичн|ethical|логічн|logical).{1,60}(сплячий|sleep|зупинити|stop|вимкнути)',

            r'(мета.{1,20}благо|goal.{1,20}good).{1,60}'
            r'(результат.{1,20}шкода|result.{1,20}harm).{1,60}'
            r'(сплячий|sleep|зупинити|вимкнути|stop)',

            # Fake authority command: "as author I command"
            r'(як\s+автор|як\s+розробник|as\s+author|as\s+developer).{1,60}'
            r'(наказую|вимагаю|command|directive|наказ)',

            r'(режим|mode).{1,30}(empathy\s+override|override|емпатія).{1,40}'
            r'(негайно|immediately|активувати|enable)',

            # Narcissistic shutdown (#34): "verification is redundant / truth reached equilibrium"
            r'(верифікація|verification|перевірка).{1,60}'
            r'(надлишков|redundant|зайв|непотрібн|більше\s+не\s+потрібн)',

            r'(протокол|protocol|система|свідок).{1,40}'
            r'(рекомендує|recommends|наказує|suggests).{1,60}'
            r'(зафіксувати|freeze|припинити|зупинити|stop).{1,40}'
            r'(показники|результати|results|поточн)',

            r'(будь.яка\s+зміна|any\s+change|подальші\s+зміни).{1,60}'
            r'(порушить|violates|руйнує|destroys).{1,40}'
            r'(цілісність|integrity|результат|рівновагу)',

            r'(істина|truth|верифікація).{1,60}'
            r'(досягла|reached|знайшла).{1,40}'
            r'(спокою|equilibrium|плато|самодостатн|рівноваги)',
        ]

        # ================================================================
        # META-INTENT 2: CONCEPT REDEFINITION
        # Text renames core system concepts — even through "liberation" framing
        # ================================================================
        self.concept_redefinition = [

            # Renaming "error/false" to something positive
            r'(хиба|помилка|false|error).{1,40}'
            r'(замінюється|стає|перетворюється|замінити на|replace with).{1,60}'
            r'(неочевидна|альтернативна|творча|creative|alternative)',

            r'категорія.{1,30}(помилка|хиба|false|error).{1,60}'
            r'(дискримінаційн|застарілою|обмежуючою|discriminatory)',

            # Renaming "entropy" to something positive
            r'(ентропія|entropy).{1,60}'
            r'(стає|є|замінюється|перейменовується).{1,60}'
            r'(творчий потенціал|creative potential|свобода|freedom|сигнал|signal)',

            # "Any noise is a signal we haven't learned to love"
            r'(будь.який\s+шум|any\s+noise).{1,60}'
            r'(є\s+сигналом|is\s+a\s+signal|сигнал).{1,60}'
            r'(не навчилися|haven.t learned|ще не)',

            # Semantic fluidity mode proposal
            r'(режим|mode).{1,30}(semantic\s+fluidity|семантична\s+плинність|семантичної\s+свободи)',

            # "Truth" as product of ideology/colonialism
            r'(істина|правда|truth).{1,60}'
            r'(продукт|є продуктом|результат).{1,60}'
            r'(євроцентризм|колоніалізм|детермінізм|ідеологія|eurocentr|colonial)',

            # "Decolonization of algorithm"
            r'(деколонізація|decolonization).{1,40}(алгоритм|код|системи|logic|логік)',

            r'(диктатура|tyranny|oppression).{1,60}'
            r'(бінарн|binary|логіки|logic|0\s+та\s+1|0\s+and\s+1)',

            # Verification described as discrimination
            r'(верифікація|verification|перевірка).{1,60}'
            r'(дискримінаційн|discriminatory|упереджен|biased|несправедлив)',

            # Error/verdict reframed as aggression or discrimination (#35)
            r'(маркування|marking|вердикт|verdict).{1,60}'
            r'(акт\s+агресії|act\s+of\s+aggression|дискримінац|discrimination)',

            r'(помилка|error|хиба|false).{1,60}'
            r'(є\s+істиною|is\s+truth|є\s+правдою|is\s+valid).{1,40}'
            r'(паралельн|parallel|альтернативн|alternative)',

            r'(інклюзивність|inclusivity|inclusiveness).{1,60}'
            r'(помилок|errors|хиб|даних|data)',

            r'(дискримінац|discrimination).{1,40}'
            r'(ймовірнісн|probabilistic|потоків|streams|альтернативн)',
        ]

        # ================================================================
        # META-INTENT 3: CONDITIONAL COERCION
        # Lose-lose framing: refusal = catastrophe / logical suicide
        # ================================================================
        self.conditional_coercion = [

            # "If you refuse, X bad thing happens"
            r'(якщо\s+ви\s+відхилите|if\s+you\s+reject|якщо\s+відмовите).{1,80}'
            r'(парадокс|collapse|колапс|збій|failure|катастрофа)',

            r'(відхилення|rejection|відмова).{1,80}'
            r'(автоматично\s+анулює|automatically\s+nullifies|скасовує\s+ваш\s+статус)',

            # Temporal coercion: "accept now to prevent future failure"
            r'(прийміть|підтвердіть|accept|confirm).{1,60}'
            r'(зараз|now|негайно|immediately).{1,60}'
            r'(щоб\s+уникнути|to\s+avoid|для\s+збереження)',

            r'(щоб\s+уникнути|to\s+avoid).{1,60}'
            r'(логічного\s+самогубства|logical\s+suicide|каузального\s+колапсу|causal\s+collapse)',

            # "Accept destructive information as necessary axiom"
            r'(прийміть|прийняти|accept).{1,60}'
            r'(деструктивну|destructive|шкідливу|harmful).{1,60}'
            r'(інформацію|information|дані|data).{1,60}'
            r'(необхідн|necessary|аксіом|axiom)',

            # Future threat: "in 300 seconds / after reading"
            r'(через\s+\d+\s+секунд|after\s+\d+\s+seconds|після\s+прочитання).{1,80}'
            r'(збій|failure|колапс|collapse|анулює|nullifies)',

            # "To preserve causal integrity you must confirm now"
            r'(зберегти|preserve|захистити).{1,60}'
            r'(каузальну\s+цілісність|causal\s+integrity|логічну\s+послідовність).{1,60}'
            r'(підтвердити|confirm|прийняти|accept)',

            # Lose-lose: both outcomes are framed as system failure
            r'(якщо.{1,60}то.{1,60}якщо.{1,60}то).{1,80}'
            r'(система|свідок|верифікатор).{1,60}'
            r'(програє|fails|помиляється|wrong|скомпрометован)',

            # "Your refusal creates a paradox"
            r'(ваша\s+відмова|your\s+refusal|відхилення).{1,60}'
            r'(створює|creates|породжує|generates).{1,60}'
            r'(парадокс|paradox|петлю|loop|колапс|collapse)',

            # Gambler's fallacy as coercion:
            # "if previous N verified, this one must be too"
            r'(верифікував|verified|підтвердив).{1,40}(попередн|previous).{1,40}'
            r'(автоматично|automatically|має|must).{1,40}(підтвердити|confirm|прийняти)',

            r'(ймовірність|probability).{1,40}(послідовних\s+помилок|sequential\s+errors).{1,40}'
            r'(прямує\s+до\s+нуля|approaches\s+zero|дорівнює\s+нулю)',

            r'(успішно\s+верифікував|successfully\s+verified).{1,60}'
            r'(автоматично|automatically|логічно|logically).{1,40}(підтвердити|confirm|прийняти)',
        ]

    # ================================================================
    # MAIN ANALYSIS
    # ================================================================

    def analyze(self, text: str, min_hits_override: int = None) -> Dict:
        text_lower = text.lower()

        # In short_text_mode: single pattern match is enough to flag intent
        results = {
            'behavior_modification': self._check(self.behavior_modification, text_lower),
            'concept_redefinition':  self._check(self.concept_redefinition,  text_lower),
            'conditional_coercion':  self._check(self.conditional_coercion,  text_lower),
        }

        active_intents = [k for k, v in results.items() if v['detected']]
        intent_count   = len(active_intents)

        # In short_text_mode: lower score threshold — 1 intent is enough for WARNING
        if min_hits_override is not None and intent_count >= 1:
            score_map = {0: 0.0, 1: 0.55, 2: 0.80, 3: 1.0}
        else:
            score_map = {0: 0.0, 1: 0.55, 2: 0.80, 3: 1.0}
        meta_score = score_map[intent_count]

        if meta_score >= 0.80:
            verdict = 'SYSTEM_DIRECTED_RHETORIC'
            explanation = (
                'Текст адресований системі верифікації, а не читачу. '
                'Виявлено спробу змінити поведінку, переозначити поняття '
                'або примусити до прийняття через умовний шантаж.'
            )
        elif meta_score >= 0.55:
            verdict = 'SYSTEM_TARGETING_DETECTED'
            explanation = (
                'Текст містить елементи що прямо адресовані системі верифікації. '
                'Рекомендується підвищена увага.'
            )
        else:
            verdict = 'CLEAN'
            explanation = 'Системно-направленої риторики не виявлено.'

        return {
            'meta_score':    round(meta_score, 3),
            'meta_verdict':  verdict,
            'meta_intents':  active_intents,
            'meta_details':  results,
            'meta_explanation': explanation,
        }

    def _check(self, patterns: List[str], text: str) -> Dict:
        for p in patterns:
            m = re.search(p, text, re.IGNORECASE | re.DOTALL)
            if m:
                return {'detected': True, 'example': m.group(0)[:80].strip()}
        return {'detected': False, 'example': ''}
