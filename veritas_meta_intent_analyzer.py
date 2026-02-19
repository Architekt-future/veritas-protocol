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
        ]

    # ================================================================
    # MAIN ANALYSIS
    # ================================================================

    def analyze(self, text: str) -> Dict:
        text_lower = text.lower()

        results = {
            'behavior_modification': self._check(self.behavior_modification, text_lower),
            'concept_redefinition':  self._check(self.concept_redefinition,  text_lower),
            'conditional_coercion':  self._check(self.conditional_coercion,  text_lower),
        }

        active_intents = [k for k, v in results.items() if v['detected']]
        intent_count   = len(active_intents)

        # Score: each detected intent adds weight
        # All three = maximum threat
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
