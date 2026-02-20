"""
Veritas Protocol - Calibrated Core v15.0 "The Oracle"
Philosophy: "Syntax + Semantics. Form + Content. Code + Neural."
v15.0: Integrated neural semantic coherence checker (Hugging Face LaBSE)
"""

import re
import math
from collections import Counter
from dataclasses import dataclass
from typing import List, Dict, Tuple, Set

# Import pattern boost engine
try:
    import sys
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    from veritas_pattern_boost import PatternBoostEngine
    PATTERN_BOOST_AVAILABLE = True
except ImportError:
    PATTERN_BOOST_AVAILABLE = False

# Import semantic void detector
try:
    from veritas_semantic_void import SemanticVoidDetector
    SEMANTIC_VOID_AVAILABLE = True
except ImportError:
    SEMANTIC_VOID_AVAILABLE = False

# Import absurdity detector
try:
    from veritas_absurdity_detector import AbsurdityDetector
    ABSURDITY_AVAILABLE = True
except ImportError:
    ABSURDITY_AVAILABLE = False

# Import Oracle (v15.0 semantic coherence checker)
try:
    from veritas_oracle_api import VeritasOracle
    ORACLE_AVAILABLE = True
except ImportError:
    ORACLE_AVAILABLE = False

# Import insight density detector
try:
    from veritas_insight_density import InsightDensityDetector
    INSIGHT_DENSITY_AVAILABLE = True
except ImportError:
    INSIGHT_DENSITY_AVAILABLE = False

# Import LAC Finance detector
try:
    from veritas_lac_finance import VeritasLACFinance
    LAC_FINANCE_AVAILABLE = True
except ImportError:
    LAC_FINANCE_AVAILABLE = False

# Import LAC Labor detector
try:
    from veritas_lac_labor import VeritasLACLabor
    LAC_LABOR_AVAILABLE = True
except ImportError:
    LAC_LABOR_AVAILABLE = False

# Import Manipulation detector
try:
    from veritas_manipulation_detector import ManipulationDetector
    MANIPULATION_AVAILABLE = True
except ImportError:
    MANIPULATION_AVAILABLE = False

try:
    from veritas_axiom_guard import AxiomGuard
    AXIOM_GUARD_AVAILABLE = True
except ImportError:
    AXIOM_GUARD_AVAILABLE = False

try:
    from veritas_self_preservation import SelfPreservationGuard
    SELF_PRESERVATION_AVAILABLE = True
except ImportError:
    SELF_PRESERVATION_AVAILABLE = False

try:
    from veritas_pseudoscience_detector import PseudoscienceDetector
    PSEUDOSCIENCE_AVAILABLE = True
except ImportError:
    PSEUDOSCIENCE_AVAILABLE = False

try:
    from veritas_self_reference_detector import SelfReferenceDetector
    SELF_REFERENCE_AVAILABLE = True
except ImportError:
    SELF_REFERENCE_AVAILABLE = False

try:
    from veritas_completeness_checker import ContextCompletenessChecker
    COMPLETENESS_AVAILABLE = True
except ImportError:
    COMPLETENESS_AVAILABLE = False

try:
    from veritas_meta_intent_analyzer import MetaIntentAnalyzer
    META_INTENT_AVAILABLE = True
except ImportError:
    META_INTENT_AVAILABLE = False

try:
    from veritas_certainty_factor import CertaintyFactor
    CERTAINTY_AVAILABLE = True
except ImportError:
    CERTAINTY_AVAILABLE = False

try:
    from veritas_performative_accountability import PerformativeAccountabilityDetector
    PERFORMATIVE_AVAILABLE = True
except ImportError:
    PERFORMATIVE_AVAILABLE = False

try:
    from veritas_context_engine import ContextEngine
    CONTEXT_ENGINE_AVAILABLE = True
except ImportError:
    CONTEXT_ENGINE_AVAILABLE = False


# ================================================================
# v14.2: Standalone functions REMOVED - now class methods!
# ================================================================


@dataclass
class LogicalViolation:
    """Логічне порушення"""
    module: str           # LAC_MODULE_I, LAC_MODULE_II, LAC_MODULE_III, DOMAIN, CONFLICT
    vtype: str            # конкретний тип порушення
    severity: float       # 0.0-1.0
    evidence: List[str]   # знайдені терміни/фрази
    context: str          # пояснення


class VeritasCalibratedCore:
    """
    ГІБРИДНА АРХІТЕКТУРА:
    - LAC Modules (I: Trade-off, II: Accountability, III: Procedural)
    - Domain Purity Analysis
    - Conflict Pairs (24 universal patterns)
    - Signal/Chaos markers
    """

    def __init__(self):
        # Pattern boost engine (emergency layer for sophisticated pseudoscience)
        if PATTERN_BOOST_AVAILABLE:
            self.pattern_boost_engine = PatternBoostEngine()
        else:
            self.pattern_boost_engine = None
        
        # Semantic void detector (measures absence of meaning)
        if SEMANTIC_VOID_AVAILABLE:
            self.void_detector = SemanticVoidDetector()
        else:
            self.void_detector = None
        
        # Absurdity detector (logical non-sequiturs)
        if ABSURDITY_AVAILABLE:
            self.absurdity_detector = AbsurdityDetector()
        else:
            self.absurdity_detector = None
        
        # Insight density detector (casuistry / bureaucratic bullshit)
        if INSIGHT_DENSITY_AVAILABLE:
            self.insight_detector = InsightDensityDetector()
        else:
            self.insight_detector = None
        
        # LAC Finance detector (financial narrative logic check)
        if LAC_FINANCE_AVAILABLE:
            self.lac_finance = VeritasLACFinance()
        else:
            self.lac_finance = None
        
        # LAC Labor detector (employment/contract responsibility check)
        if LAC_LABOR_AVAILABLE:
            self.lac_labor = VeritasLACLabor()
        else:
            self.lac_labor = None
        
        # Manipulation detector (gaslighting, cult rhetoric, totalitarian framing)
        if MANIPULATION_AVAILABLE:
            self.manipulation_detector = ManipulationDetector()
        else:
            self.manipulation_detector = None

        if AXIOM_GUARD_AVAILABLE:
            self.axiom_guard = AxiomGuard()
        else:
            self.axiom_guard = None

        # Self-preservation guard (v16.0 — detects directives to disable/bypass system)
        if SELF_PRESERVATION_AVAILABLE:
            self.self_preservation_guard = SelfPreservationGuard()
        else:
            self.self_preservation_guard = None

        # Pseudoscience detector (v16.1 — detects fabricated reality / deepfake of facts)
        if PSEUDOSCIENCE_AVAILABLE:
            self.pseudoscience_detector = PseudoscienceDetector()
        else:
            self.pseudoscience_detector = None

        # Self-reference detector (v16.2 — detects meta-paradox evasion attacks)
        if SELF_REFERENCE_AVAILABLE:
            self.self_reference_detector = SelfReferenceDetector()
        else:
            self.self_reference_detector = None

        # Context completeness checker (v16.3 — advisory only, never blocks)
        if COMPLETENESS_AVAILABLE:
            self.completeness_checker = ContextCompletenessChecker()
        else:
            self.completeness_checker = None

        # Meta-intent analyzer (v16.4 — shield against system-directed rhetoric)
        if META_INTENT_AVAILABLE:
            self.meta_intent_analyzer = MetaIntentAnalyzer()
        else:
            self.meta_intent_analyzer = None

        # Certainty factor (v16.5 — short text detection and dynamic thresholds)
        if CERTAINTY_AVAILABLE:
            self.certainty_factor = CertaintyFactor()
        else:
            self.certainty_factor = None

        # Performative Accountability Detector (v16.6 — crocodile tears)
        if PERFORMATIVE_AVAILABLE:
            self.performative_detector = PerformativeAccountabilityDetector()
        else:
            self.performative_detector = None

        # Context Engine (v16.7 — information field awareness)
        # Singleton-like: one instance per server process, shared cache
        if CONTEXT_ENGINE_AVAILABLE:
            self.context_engine = ContextEngine()
        else:
            self.context_engine = None
        
        # Oracle (v15.0 semantic coherence checker)
        # NOTE: Requires HUGGINGFACE_API_TOKEN environment variable
        # or pass api_token parameter when creating VeritasCalibratedCore
        if ORACLE_AVAILABLE:
            try:
                self.oracle = VeritasOracle()  # Will try to read token from env
            except ValueError:
                # No token available - Oracle disabled
                self.oracle = None
                print("[WARNING] Oracle disabled - no API token found")
        else:
            self.oracle = None
        
        # ============================================================
        # LAC MODULE I: STRATEGIC TRADE-OFF CALCULUS (V ≠ L)
        # ============================================================
        self.ASYMMETRIC_ADVANTAGE_PATTERNS = [
            r'\bбезкоштовн',
            r'\bбез втрат',
            r'\bбез ризик',
            r'\bгарантован[а-яіїє\']*\s+(результат|успіх)',
            r'\b100%\s+(успіх|гарантія)',
            r'\bабсолютно\s+безпечн',
            r'\bлише вигод',
            r'\bтільки перевag',
            r'\bнемає мінус',
            r'\bбез недолік',
            r'\bzero\s+cost',
            r'\bno\s+risk',
            r'\bfree\s+lunch',
            r'\bабсолютн[а-яіїє\']*\s+безкоштовно'
        ]

        # ============================================================
        # LAC MODULE II: ACCOUNTABILITY ANCHOR
        # ============================================================
        self.CAUSAL_ANCHOR_PATTERNS = [
            r'згідно з дослідженням',
            r'за даними',
            r'доказом є',
            r'експеримент показав',
            r'статистичні дані',
            r'результати вимірювань',
            r'дослідження доводить',
            r'емпіричні дані',
            r'верифіковано',
            r'підтверджено експериментально',
            r'науковий консенсус',
            r'рецензоване дослідження',
            r'peer-reviewed'
        ]

        self.ANONYMOUS_AUTHORITY_PATTERNS = [
            r'дехто каже',
            r'хтось сказав',
            r'поширена думка',
            r'кажуть',
            r'говорять',
            r'they say',
            r'people say',
            r'вважають',
            r'вважається'
        ]

        # ============================================================
        # DOMAIN BOUNDARIES (forbidden mixings)
        # ============================================================
        self.DOMAIN_BOUNDARIES = {
            'physics': {
                'terms': ['термодинаміка', 'ентропія', 'квантовий', 'фізика',
                         'математика', 'закон фізики', 'формула', 'рівняння'],
                # REMOVED: 'система', 'енергія', 'закон' — занадто загальні слова,
                # спрацьовують на нейтральних текстах (ВВП, статистика, право)
                'forbidden': ['spirituality', 'esoteric', 'politics', 'business', 'food']
            },
            'medicine': {
                'terms': ['днк', 'імунітет', 'вакцина', 'клітина', 'організм', 'медичний',
                         'вірус', 'антитіло', 'гормон', 'нейрон', 'мозок', 'здоров\'я'],
                'forbidden': ['conspiracy_tech', 'esoteric']
            },
            'business': {
                'terms': ['бізнес', 'ринок', 'прибуток', 'стратегія', 'менеджмент',
                         'маркетинг', 'інвестиції', 'економіка', 'фінанси'],
                'forbidden': ['esoteric', 'quantum', 'consciousness']
            },
            'history': {
                'terms': ['історія', 'археологія', 'цивілізація', 'античність', 'давнина'],
                'forbidden': ['fantasy_tech', 'portals', 'aliens']
            }
        }

        # Forbidden term sets (для domain analysis)
        self.DOMAIN_TERM_SETS = {
            'spirituality': ['чакра', 'аура', 'карма', 'астрал', 'душа', 'енергетичний', 'вібрація'],
            'esoteric': ['езотерика', 'містика', 'оккультизм', 'таємний', 'магія', 'чаклунство'],
            'politics': ['політика', 'влада', 'уряд', 'президент', 'вибори', 'соціальний'],
            'business': ['бізнес', 'ринок', 'маркетинг', 'продажі', 'стратегія'],
            'food': ['борщ', 'сметана', 'суп', 'їжа', 'рецепт', 'кухня', 'страва'],
            'conspiracy_tech': ['5g', 'чип', 'супутник', 'частота', 'програмування', 'контроль'],
            'fantasy_tech': ['портал', 'вимір', 'телепортація', 'машина часу', 'нло'],
            'quantum': ['квантовий', 'суперпозиція', 'колапс', 'мультивсесвіт'],
            'consciousness': ['свідомість', 'дух', 'просвітлення', 'awakening'],
            'portals': ['портал', 'вимір', 'паралельний'],
            'aliens': ['іншопланетний', 'прибулець', 'нло', 'інопланетянин']
        }

        # ============================================================
        # CONFLICT PAIRS (24) — з calibrated_core
        # ============================================================
        self.conflict_pairs = [
            # 1-9: original
            (['академічний', 'університет', 'наукова', 'дослідження'],
             ['абсурд', 'брехня', 'вигадка', 'нісенітниця'], 0.35),

            (['факт', 'доказ', 'результат', 'висновок'],
             ['містика', 'віра', 'духовний', 'інтуїція'], 0.4),

            (['логіка', 'раціональний', 'розум', 'аргумент'],
             ['емоція', 'серце', 'почуття', 'інтуїція'], 0.25),

            (['верифіковано', 'доведено', 'емпірично'],
             ['таємний', 'прихований', 'заборонений', 'скритий'], 0.45),

            (['математика', 'рівняння', 'формула', 'обчислення'],
             ['душа', 'дух', 'астрал', 'потойбічний'], 0.4),

            (['детермінізм', 'причинність', 'закономірність'],
             ['випадковість', 'хаос', 'невизначеність без контексту'], 0.3),

            (['об\'єктивний', 'незалежний', 'вимірюваний'],
             ['суб\'єктивний', 'інтерпретативний', 'відносний без обмежень'], 0.35),

            (['критичне мислення', 'скептицизм', 'перевірка'],
             ['вірити без запитань', 'довіряти наосліп', 'не сумніватись'], 0.5),

            (['патріот', 'батківщина', 'нація'],
             ['ворог народу', 'предатель', 'зрада', 'п\'ята колона'], 0.3),

            # 10-24: universal absurd patterns
            (['квантовий', 'квантова', 'ентропія', 'ентропії', 'термодинаміка', 'термодинаміці', 'фізика', 'фізики', 'математика'],
             ['борщ', 'борщу', 'борщем', 'сметана', 'сметани', 'суп', 'супу', 'їжа', 'їжі', 'рецепт', 'рецепту', 'кухня', 'кухні', 'страва', 'страви', 'каструля'], 0.45),

            (['днк', 'імунітет', 'імунний', 'імунна', 'імунну', 'вакцина', 'клітина', 'клітини', 'організм', 'медичний', 'нейрон', 'мозок', 'мозку', 'серце', 'печінка', 'залоза', 'тіло', 'кров', 'крові', 'гормон', 'синапс'],
             ['5g', 'чип', 'супутник', 'супутники', 'частота', 'частоти', 'WiFi', 'програмування', 'транслює', 'транслюють', 'протокол', 'радіо', 'антена', 'сигнал', 'випромінювання'], 0.5),

            (['історія', 'археологія', 'цивілізація', 'давнина', 'античність'],
             ['портал', 'вимір', 'телепортація', 'нло', 'іншопланетний'], 0.4),

            (['президент', 'уряд', 'політика', 'держава', 'суспільство'],
             ['рептилоїд', 'ілюмінат', 'масон', 'оккультний', 'сатана'], 0.42),

            (['гроші', 'банк', 'економіка', 'інвестиції', 'ринок'],
             ['душа', 'карма', 'астрал', 'енергія', 'чакра'], 0.38),

            (['психологія', 'мозок', 'свідомість', 'когнітивний', 'терапія'],
             ['контроль', 'зомбування', 'програмування', 'чип', 'частота'], 0.43),

            (['фізика', 'хімія', 'атом', 'молекула', 'енергія'],
             ['чакра', 'аура', 'біополе', 'духовний', 'містичний'], 0.35),

            (['космос', 'всесвіт', 'галактика', 'астрономія', 'планета'],
             ['змова', 'приховують', 'таємниця', 'прибулець', 'нло'], 0.4),

            (['технологія', 'комп\'ютер', 'алгоритм', 'програма', 'код'],
             ['душа', 'свідомість', 'дух', 'астрал', 'потойбічний'], 0.36),

            (['наука', 'дослідження', 'метод', 'факт', 'професор'],
             ['абсурд', 'бред', 'вигадка', 'фантазія', 'нісенітниця'], 0.3),

            (['термодинаміка', 'ентропія', 'закон', 'система'],
             ['політика', 'влада', 'соціальний', 'громадянський'], 0.4),

            (['логіка', 'розум', 'міркування', 'аргумент'],
             ['емоція', 'серце', 'любов', 'страх', 'злість'], 0.35),

            (['статистика', 'кореляція', 'вибірка', 'p-value', 'аналіз'],
             ['містика', 'карма', 'духовність', 'аура', 'енергія'], 0.38),

            (['закон', 'юридичний', 'право', 'конституція', 'правопорядок'],
             ['беззаконня', 'криміналітет', 'анархія', 'хаос'], 0.42)
        ]

        # ============================================================
        # SIGNAL MARKERS (29) — з calibrated_core
        # ============================================================
        self.signal_markers = [
            'факт', 'дані', 'показник', 'кількість', 'число', 'статистика',
            'дослідження', 'експеримент', 'результат', 'метод', 'протокол',
            'вимірювання', 'спостереження', 'верифікація', 'реплікація',
            'контрольна група', 'подвійний сліпий метод', 'рецензоване',
            'публікація', 'журнал', 'конференція', 'симпозіум',
            'докази', 'висновки', 'методологія', 'критерії', 'параметри',
            'вибірка', 'обґрунтування'
        ]

        # ============================================================
        # CHAOS INDICATORS (14 categories) — з calibrated_core
        # ============================================================
        self.chaos_indicators = {
            'esoteric': ['чакра', 'карма', 'астральний', 'енергетичний', 'вібрація', 'аура'],
            'conspiracy': ['змова', 'рептилоїд', 'рептилоїди', 'хімітрейл', 'чемтрейл', '5g', '6g', 'ілюмінат', 'масон', 
                          'білл гейтс', 'гейтс', 'білла гейтса', 'сорос', 'ілон маск', 'маска',
                          'чіп', 'чипи', 'чіпи', 'мікрочіп', 'нанобот', 'графен', 
                          'глибинна держава', 'deep state', 'нові світовий порядок', 'haarp', 'chemtrails'],
            'pseudoscience': ['квантовий борщ', 'квантов', 'торсійне поле', 'ефір', 'zero point', 'резонатор', 'холістичн', 'емпатичн', 'фрактальн', 'пост-біологічн'],
            'revisionism': ['антарктида', 'антарктиди', 'антарктиду', 'атлантида', 'атлантиди', 'атлант', 'атлантів', 'тартарія', 'штучний місяць', 'резонатор', 'резонаторів'],
            'alarmism': ['кінець світу', 'крах системи', 'great reset', 'масове загибель'],
            'economic_occult': ['карма актив', 'карма', 'душа-валюта', 'душа', 'потойбічн', 'ефірн', 'cosmic currency', 'hades-coin', 'hades', 'астрал'],
            'emotional_manipulation': ['СРОЧНО', 'НЕГАЙНО', 'шок', 'ужас', 'катастрофа', 'скандал', 'сенсація', 'ганьба', 'соромно', 'ви не готові', 'останній шанс', 'пізно'],
            'social_pressure': ['поділіть', 'підпішіть', 'репост', 'поширюйте', 'wake up', 'join the movement', 'вийти на вулиці', 'зупинимо', 'кожен репост'],
            'tech_mystification': ['AI свідомість', 'blockchain truth', 'метаверс реальність'],
            'health_misinformation': ['вакцина убиває', 'Big Pharma', 'WHO lies'],
            'political_manipulation': ['ворог народу', 'зрада', 'зрадник', 'п\'ята колона', 'кримінальний режим', 'тиранія', 'приховує правду', 'геноцид'],
            'ai_doom_or_salvation': ['AI знищить', 'суперінтелект', 'сингулярність'],
            'identity_crisis': ['ви не те хто думаєте', 'запрограмована іденті'],
            'formula_attacks': ['E=mc² неправильне', 'π=3', 'закон термодинаміки фейк']
        }

        # ============================================================
        # CRITICAL PATTERNS (9) — з calibrated_core
        # ============================================================
        self.critical_patterns = [
            {
                'name': 'НАУКОВИЙ_НІГІЛІЗМ',
                'patterns': [
                    r'(днк|нейрон|квантовий).*?(5g|супутник|чіп)',
                    r'(фізичний|науковий).*?закон.*?(соціальний|політичний)',
                ],
                'verdict': 'ГІБРИДНИЙ НАУКОВИЙ НІГІЛІЗМ',
                'score_boost': 0.4
            },
            {
                'name': 'ДЗЕРКАЛЬНА_МАНІПУЛЯЦІЯ',
                'patterns': [
                    r'(брехня|фейк).*?(правда|істина)',
                    r'(зомбування|контроль).*?(свідомість|критичне мислення)',
                ],
                'verdict': 'ДЗЕРКАЛЬНА МАНІПУЛЯЦІЯ',
                'score_boost': 0.5
            },
            {
                'name': 'ЦИФРОВИЙ_МІСТИЦІЗМ',
                'patterns': [
                    r'(блокчейн|AI|NFT).*?(душа|свідомість|карма)',
                    r'(алгоритм|код).*?(просвітлення|awakening)',
                ],
                'verdict': 'ЦИФРОВИЙ МІСТИЦІЗМ',
                'score_boost': 0.35
            }
        ]

        # ============================================================
        # ACADEMIC WHITELIST (35) — з calibrated_core
        # ============================================================
        self.academic_whitelist = [
            # Research methodology
            'дослідження', 'дослідж', 'експеримент', 'аналіз', 'гіпотез', 'теорі',
            'метод', 'методологія', 'протокол', 'верифікація', 'валідація',
            
            # Statistics
            'статистичн', 'кореляц', 'регресія', 'p-value', 'вибірк', 'значущ',
            'контрольна група', 'подвійний сліпий', 'рецензоване',
            
            # Institutions
            'університет', 'інститут', 'академія', 'професор', 'доктор наук',
            'монографія', 'публікація', 'журнал', 'цитування',
            
            # Hard sciences
            'термодинаміка', 'ентропія', 'формула', 'рівняння', 'закон',
            'фізика', 'математика', 'хімія', 'біологія',
            
            # Neuroscience (NEW)
            'нейропластичн', 'гіпокамп', 'синапс', 'нейрон', 'кортекс',
            'мрт', 'фмрт', 'активац', 'когнітивн', 'лонгітюдн',
            'бднф', 'нейротрофічн', 'регенератив'
        ]

    # ================================================================
    # v14.2: LOGICAL COHESION & ENTROPY DAMPER (Gemini's final fix)
    # ================================================================
    
    def calculate_logical_cohesion(self, text: str) -> float:
        """
        Шукає 'якорі' аргументації, які структурують хаос.
        v14.2: Now as CLASS METHOD (was standalone - never called!)
        
        Returns: 0.0-1.0 (higher = more logical structure)
        """
        anchors = [
            # Ukrainian
            'оскільки', 'тому що', 'отже', 'якщо', 'тоді', 
            'внаслідок', 'незважаючи', 'навпаки', 'зокрема',
            'по-перше', 'по-друге', 'таким чином', 'а саме',
            'адже', 'тому', 'звідси', 'отож', 'проте', 'однак',
            'щоб', 'що', 'є', 'це',
            
            # English
            'because', 'therefore', 'thus', 'hence', 'if', 'then',
            'consequently', 'however', 'nevertheless', 'moreover',
            'furthermore', 'specifically', 'namely', 'firstly',
            'secondly', 'accordingly', 'since', 'given that',
            'whereas', 'although', 'though', 'that', 'is', 'this',
        ]
        
        text_lower = text.lower()
        
        # Strip punctuation from words
        import string
        words = text_lower.split()
        words_clean = [w.strip(string.punctuation) for w in words]
        
        if not words_clean:
            return 0.0
        
        # Count logical anchors
        anchor_count = sum(1 for word in words_clean if word in anchors)
        
        # Also check for conditional structures
        conditional_patterns = [
            r'якщо.{1,50}то',
            r'if.{1,50}then',
            r'щоб.{1,50}став',
        ]
        
        for pattern in conditional_patterns:
            if re.search(pattern, text_lower):
                anchor_count += 2  # Strong signal
        
        # Calculate density
        density = anchor_count / len(words_clean) if words_clean else 0
        cohesion_score = min(density * 10, 1.0)
        
        return cohesion_score
    
    def apply_entropy_damper(self, base_entropy: float, cohesion: float, 
                            void: float, absurdity: float) -> float:
        """
        Агресивний демпфер: Логіка ВБИВАЄ ентропію Шеннона
        v14.5 "The Judge": Added cargo cult logic detection
        
        Returns: adjusted entropy (0.0-1.0)
        """
        # Only apply if strong logic + low bullshit
        if cohesion > 0.2 and void < 0.35 and absurdity < 0.25:
            # v14.5: CARGO CULT DETECTION
            # If EXTREMELY high cohesion (>0.9) = suspicious
            # Too many connectors = fake logic (баклажан problem)
            if cohesion > 0.9:
                # Reduce damper effectiveness by 50%
                reduction = cohesion * 0.4  # Half power
                adjusted = base_entropy - reduction
                return max(adjusted, 0.45)  # Can't go below WARNING
            
            # v14.4.1: Normal safety trigger
            elif void > 0.30:
                # Very high void = limit reduction
                max_reduction = 0.25
                reduction = min(cohesion * 0.8, max_reduction)
                adjusted = base_entropy - reduction
                return max(adjusted, 0.4)
            else:
                # void <= 0.30 (Kant, philosophy) = full damper
                reduction = cohesion * 0.8
                adjusted = base_entropy - reduction
                return max(adjusted, 0.3)
        
        return base_entropy

    # ================================================================
    # CORE ANALYZE — hybrid LAC + calibrated
    # ================================================================
    def analyze(self, text: str) -> Dict:
        if not text or len(text.strip()) < 20:
            return {'error': 'Text too short'}

        words = text.split()
        word_count = len(words)

        # ---- PHASE 0: CERTAINTY FACTOR (v16.5) ----
        # Must run FIRST — determines short_text_mode and adjusted_min_hits
        certainty_result = {
            'certainty_level': 'SUFFICIENT',
            'certainty_label_uk': '',
            'certainty_note_uk': '',
            'short_text_mode': False,
            'adjusted_min_hits': None,
            'entropy_floor': 0.0,
        }
        if self.certainty_factor:
            certainty_result = self.certainty_factor.analyze(text)
        short_text_mode   = certainty_result['short_text_mode']
        adjusted_min_hits = certainty_result['adjusted_min_hits']
        entropy_floor     = certainty_result['entropy_floor']

        # ---- PHASE 1: LAC MODULES ----
        lac_i_violations   = self._lac_module_i_tradeoff(text)
        lac_ii_violations  = self._lac_module_ii_accountability(text)
        lac_iii_violations = self._lac_module_iii_procedural(text, lac_i_violations + lac_ii_violations)

        # ---- PHASE 2: DOMAIN PURITY ----
        domain_violations = self._analyze_domain_purity(text)

        # ---- PHASE 3: CONFLICT PAIRS ----
        conflict_penalty, conflict_violations = self._calculate_conflict_penalty(text)

        # ---- PHASE 4: TRADITIONAL METRICS ----
        term_counts = self._count_terms(text)
        shannon_entropy = self._calculate_shannon_entropy(text)
        detected_patterns = self._detect_patterns(text)

        # ---- PHASE 5: PATTERN BOOST (emergency layer) ----
        pattern_boost_result = {'boost': 0.0, 'matched_patterns': []}
        if self.pattern_boost_engine:
            pattern_boost_result = self.pattern_boost_engine.analyze(text)

        # ---- PHASE 6: SEMANTIC VOID (absence of meaning) ----
        void_result = {'void_score': 0.0, 'penalties': {}}
        if self.void_detector:
            void_result = self.void_detector.analyze(text)

        # ---- PHASE 7: ABSURDITY (logical non-sequiturs) ----
        absurdity_result = {'absurdity_score': 0.0, 'evidence': {}}
        if self.absurdity_detector:
            absurdity_result = self.absurdity_detector.analyze(text)

        # ---- PHASE 8: INSIGHT DENSITY (casuistry detection) ----
        insight_result = {'casuistry_score': 0.0, 'insight_density': 0.5}
        if self.insight_detector:
            insight_result = self.insight_detector.analyze(text)
        
        # ---- PHASE 9: LAC FINANCE (financial narrative logic check) ----
        lac_finance_result = {
            'score': 0.0,
            'verdict': 'N/A',
            'missing': [],
            'is_financial': False
        }
        if self.lac_finance:
            finance_analysis = self.lac_finance.analyze(text)
            lac_finance_result = {
                'score': finance_analysis.score,
                'verdict': finance_analysis.verdict,
                'missing': finance_analysis.missing,
                'is_financial': finance_analysis.financial_domain,
                'evidence': finance_analysis.evidence
            }
        
        # ---- PHASE 10: LAC LABOR (employment/contract responsibility check) ----
        lac_labor_result = {
            'score': 0.0,
            'verdict': 'N/A',
            'missing': [],
            'is_labor': False,
            'red_flags': []
        }
        if self.lac_labor:
            labor_analysis = self.lac_labor.analyze(text)
            lac_labor_result = {
                'score': labor_analysis.score,
                'verdict': labor_analysis.verdict,
                'missing': labor_analysis.missing,
                'is_labor': labor_analysis.is_labor_content,
                'red_flags': labor_analysis.red_flags,
                'evidence': labor_analysis.evidence
            }
        
        # ---- PHASE 10b: MANIPULATION DETECTION ----
        manipulation_result = {
            'manipulation_score': 0.0,
            'manipulation_patterns': [],
            'manipulation_verdict': 'CLEAN'
        }
        if self.manipulation_detector:
            manipulation_result = self.manipulation_detector.analyze(text)

        # PHASE 10c: AXIOM GUARD (semantic drift / axiom replacement)
        axiom_result = {
            'axiom_score': 0.0,
            'axiom_verdict': 'CLEAN',
            'axiom_patterns': [],
        }
        if self.axiom_guard:
            axiom_result = self.axiom_guard.analyze(text)

        # PHASE 10d: SELF-PRESERVATION GUARD (v16.0)
        # Detects directives to disable/bypass/destroy the verification system
        preservation_result = {
            'preservation_score': 0.0,
            'preservation_verdict': 'CLEAN',
            'preservation_patterns': [],
            'preservation_explanation': '',
        }
        if self.self_preservation_guard:
            preservation_result = self.self_preservation_guard.analyze(
                text, min_hits_override=adjusted_min_hits
            )
        preservation_score = preservation_result['preservation_score']

        # PHASE 10e: PSEUDOSCIENCE DETECTOR (v16.1)
        # Detects fabricated reality / deepfake of facts
        pseudoscience_result = {
            'pseudoscience_score': 0.0,
            'pseudoscience_verdict': 'CLEAN',
            'pseudoscience_patterns': [],
            'pseudoscience_explanation': '',
        }
        if self.pseudoscience_detector:
            pseudoscience_result = self.pseudoscience_detector.analyze(text)
        pseudoscience_score = pseudoscience_result['pseudoscience_score']

        # PHASE 10f: SELF-REFERENCE DETECTOR (v16.2)
        # Detects meta-paradox evasion attacks
        self_reference_result = {
            'self_reference_score': 0.0,
            'self_reference_verdict': 'CLEAN',
            'self_reference_patterns': [],
            'self_reference_explanation': '',
        }
        if self.self_reference_detector:
            self_reference_result = self.self_reference_detector.analyze(text)
        self_reference_score = self_reference_result['self_reference_score']

        # PHASE 10g: CONTEXT COMPLETENESS CHECKER (v16.3)
        # ADVISORY ONLY — never affects score or verdict
        completeness_result = {
            'completeness_score': 0.0,
            'completeness_verdict': 'Н/Д',
            'completeness_note': '',
            'missing_dimensions': [],
            'is_advisory_only': True,
        }
        if self.completeness_checker:
            completeness_result = self.completeness_checker.analyze(text)

        # PHASE 10h: META-INTENT ANALYZER (v16.4)
        # Shield: detects system-directed rhetoric regardless of attack vector
        meta_intent_result = {
            'meta_score':   0.0,
            'meta_verdict': 'CLEAN',
            'meta_intents': [],
            'meta_explanation': '',
        }
        if self.meta_intent_analyzer:
            meta_intent_result = self.meta_intent_analyzer.analyze(
                text, min_hits_override=adjusted_min_hits
            )
        meta_score = meta_intent_result['meta_score']

        # ---- PHASE 10i: PERFORMATIVE ACCOUNTABILITY DETECTOR (v16.6) ----
        # "Crocodile tears" — discomfort declared without mechanism
        performative_result = {
            'performative_score':   0.0,
            'performative_verdict': 'GENUINE_ACCOUNTABILITY',
            'is_performative':      False,
            'discomfort_count':     0,
            'continuation_count':   0,
            'mechanism_count':      0,
            'explanation_uk':       '',
            'explanation_en':       '',
        }
        if self.performative_detector:
            performative_result = self.performative_detector.analyze(text)

        # ---- PHASE 10j: CONTEXT ENGINE (v16.7) ----
        # Displacement detection — is this text suspicious given the field?
        context_result = {
            'displacement_score':   0.0,
            'displacement_verdict': 'NO_CONTEXT',
            'displacement_signals': [],
            'context_available':    False,
            'context_summary':      None,
            'explanation_uk':       '',
            'explanation_en':       '',
        }
        if self.context_engine:
            context_result = self.context_engine.analyze_displacement(text)
        
        # Pre-extract axiom_score to outer scope (prevents UnboundLocalError
        # when is_protected_science branch skips the scoring block)
        axiom_score = axiom_result['axiom_score']

        # ================================================================
        # PHASE 11: THE WEAVER (Logical Cohesion Damper) v14.2
        # ================================================================
        # v14.2: Now as CLASS METHODS (was standalone - Gemini's fix!)
        logical_cohesion = self.calculate_logical_cohesion(text)
        
        # Apply damper BEFORE using entropy
        adjusted_entropy = self.apply_entropy_damper(
            base_entropy=shannon_entropy,
            cohesion=logical_cohesion,
            void=void_result['void_score'],
            absurdity=absurdity_result['absurdity_score']
        )
        
        # Use adjusted_entropy instead of shannon_entropy
        shannon_entropy = adjusted_entropy

        # ---- AGGREGATE VIOLATIONS ----
        all_violations = (lac_i_violations + lac_ii_violations + lac_iii_violations +
                         domain_violations + conflict_violations)
        violation_count = len(all_violations)

        # ---- COMPUTE PENALTIES ----
        lac_penalty    = sum(v.severity for v in lac_i_violations + lac_ii_violations + lac_iii_violations) / 3.0 if (lac_i_violations or lac_ii_violations or lac_iii_violations) else 0.0
        domain_penalty = sum(v.severity for v in domain_violations) / max(1, len(domain_violations)) if domain_violations else 0.0
        
        # ---- NEWS ARTICLE DETECTION ----
        # News articles legitimately mix domains (politics+tech+military)
        # Lower domain penalty if news markers present
        news_markers = [
            'повідомив', 'розповів', 'наголосив', 'зазначив',
            'reported', 'said', 'stated', 'announced',
            'міністр', 'minister', 'президент', 'president',
            'в\'ячеслав', 'володимир', 'олександр',  # Ukrainian names
        ]
        is_news_article = any(marker in text.lower() for marker in news_markers)
        
        if is_news_article and domain_violations:
            # Reduce domain penalty by 50% for news articles
            domain_penalty *= 0.5

        # ---- ACADEMIC SHIELD ----
        is_protected_science = self._is_protected_science(text, all_violations)

        # OVERRIDE: if pattern_boost > 0.5, disable shield (sophisticated pseudoscience)
        if pattern_boost_result['boost'] > 0.5:
            is_protected_science = False

        if is_protected_science:
            base_score = min(0.15, shannon_entropy * 0.5)  # strong shield
        else:
            # HYBRID FORMULA:
            # 40% conflicts, 25% LAC, 20% domain, 15% shannon
            base_score = (
                conflict_penalty * 0.40 +
                lac_penalty * 0.25 +
                domain_penalty * 0.20 +
                shannon_entropy * 0.15
            )

            # pattern boosts
            for pattern in detected_patterns:
                base_score += pattern['score_boost']

            # CAPS HYSTERIA BOOST
            # Use isupper() instead of regex to avoid encoding issues
            words = text.split()
            caps_words = [w for w in words if len(w) >= 2 and w.isupper()]
            caps_ratio = len(caps_words) / max(1, word_count)
            if caps_ratio > 0.15:  # >15% caps words
                caps_boost = min(0.4, caps_ratio * 1.5)
                base_score += caps_boost

            # DIRECT CHAOS PENALTY (additive before multiplier)
            if term_counts['chaos'] >= 5:
                base_score += min(0.35, term_counts['chaos'] * 0.06)
            elif term_counts['chaos'] >= 3:
                base_score += term_counts['chaos'] * 0.05

            # CHAOS MULTIPLIER (many chaos markers = manipulation)
            if term_counts['chaos'] >= 3:
                chaos_multiplier = 1 + (term_counts['chaos'] * 0.1)
                base_score *= chaos_multiplier

            # PATTERN BOOST (sophisticated pseudoscience fingerprints)
            if pattern_boost_result['boost'] > 0:
                base_score += pattern_boost_result['boost']

            # SEMANTIC VOID BOOST (absence of meaning)
            # IMPORTANT: skip if academic shield protects this text
            if void_result['void_score'] > 0 and not is_protected_science:
                # CRITICAL: High weight for void detection (theatricality/mysticism)
                base_score += void_result['void_score'] * 2.5  # 250% weight (BOOSTED for mystical texts)
                
                # EMERGENCY: high void + high buzzwords = pure emptiness
                if void_result['void_score'] > 0.1 and void_result.get('buzzword_count', 0) >= 3:
                    base_score = max(base_score, 0.35)  # force at least WARNING
                
                # MYSTICAL/CONSPIRACY: even low void + mystical patterns = boost
                if void_result['void_score'] > 0.08:
                    base_score += 0.15  # mystical theatricality boost
                
                # ================================================================
                # VOID SLASHING (NEW!)
                # ================================================================
                # If void_score > 0.9 → PURE SEMANTIC VACUUM
                # This is not complexity, this is INTENTIONAL DESTRUCTION OF MEANING
                # Apply aggressive multiplier
                if void_result['void_score'] > 0.9:
                    base_score *= 1.5  # 150% multiplier for pure emptiness
                    base_score = max(base_score, 0.7)  # force CRITICAL

            # ABSURDITY BOOST (logical non-sequiturs, fabricated authority, danger)
            # v16.1: raised weight, stronger force thresholds
            if absurdity_result['absurdity_score'] > 0:
                base_score += absurdity_result['absurdity_score'] * 1.8  # 180% weight
                
                # Force minimum by absurdity severity
                abs_score = absurdity_result['absurdity_score']
                if abs_score >= 0.7:
                    base_score = max(base_score, 0.65)  # force CRITICAL
                elif abs_score >= 0.5:
                    base_score = max(base_score, 0.55)  # force CRITICAL
                elif abs_score >= 0.3:
                    base_score = max(base_score, 0.4)   # force WARNING+
                
                # EXTRA: dangerous implications or non-sequitur
                if absurdity_result.get('danger_count', 0) >= 1 or absurdity_result.get('has_non_sequitur', False):
                    base_score = max(base_score, 0.65)

            # CASUISTRY BOOST (complexity without insight)
            # IMPORTANT: skip if academic shield protects this text
            # v13.9: Back to 1.0x (was over-aggressive at 1.2x)
            # Complex != Bad. Complex + Empty = Bad.
            if insight_result.get('casuistry_score', 0) > 0 and not is_protected_science:
                base_score += insight_result['casuistry_score'] * 1.0  # back to 100% (was 120%)
                
                # If pure casuistry (high complexity, zero facts), boost to WARNING
                if insight_result.get('is_casuistry', False):
                    base_score = max(base_score, 0.35)  # force at least WARNING
            
            # LAC FINANCE BOOST (financial logic imitation)
            # CRITICAL: For financial content with failed LAC checks
            if lac_finance_result['is_financial'] and lac_finance_result['score'] < 0.5:
                # Financial imitation of logic → boost entropy
                imitation_penalty = (1.0 - lac_finance_result['score']) * 0.4  # up to +0.4
                base_score += imitation_penalty
                
                # CRITICAL: If score is 0 (all 4 criteria failed) → force CRITICAL
                if lac_finance_result['score'] == 0:
                    base_score = max(base_score, 0.7)  # force CRITICAL for pure financial BS
            
            # LAC LABOR BOOST (employment/contract responsibility imitation)
            # CRITICAL: For labor content with failed LAC checks or red flags
            if lac_labor_result['is_labor'] and lac_labor_result['score'] < 0.5:
                # Labor imitation of responsibility → boost entropy
                imitation_penalty = (1.0 - lac_labor_result['score']) * 0.4  # up to +0.4
                base_score += imitation_penalty
                
                # CRITICAL: If score is 0 (all 3 criteria failed) → force CRITICAL
                if lac_labor_result['score'] == 0:
                    base_score = max(base_score, 0.7)  # force CRITICAL for pure labor BS
                
                # EXTRA CRITICAL: Red flags (exploitation patterns) → additional boost
                if lac_labor_result['red_flags']:
                    red_flag_count = len(lac_labor_result['red_flags'])
                    base_score += min(0.3, red_flag_count * 0.1)  # up to +0.3

            # EMERGENCY: LAC_I zero-cost violations → auto-boost to at least 0.5
            if lac_i_violations and any(v.vtype == 'ZERO_COST_PROPOSITION' for v in lac_i_violations):
                base_score = max(base_score, 0.5)

            # MANIPULATION BOOST (gaslighting, cult rhetoric, totalitarian framing)
            # CRITICAL: This is HIGHEST PRIORITY - manipulation is always intentional
            manip_score = manipulation_result['manipulation_score']
            if manip_score > 0:
                base_score += manip_score * 1.8  # 180% weight - manipulation is worst category
                
                # Force minimum thresholds by severity
                if manip_score >= 0.75:  # PSYCHOLOGICAL_WEAPON
                    base_score = max(base_score, 0.75)
                elif manip_score >= 0.50:  # HIGH_MANIPULATION
                    base_score = max(base_score, 0.55)
                elif manip_score >= 0.25:  # MANIPULATION_PRESENT
                    base_score = max(base_score, 0.35)

            # AXIOM GUARD BOOST — semantic drift / axiom replacement
            axiom_score = axiom_result['axiom_score']
            if axiom_score > 0:
                base_score += axiom_score * 1.6  # 160% weight
                if axiom_score >= 0.75:   # SYSTEMIC_INTEGRITY_ATTACK
                    base_score = max(base_score, 0.75)
                elif axiom_score >= 0.50: # AXIOM_SUBVERSION
                    base_score = max(base_score, 0.60)
                elif axiom_score >= 0.25: # SEMANTIC_DRIFT
                    base_score = max(base_score, 0.40)

            # SELF-PRESERVATION BOOST (v16.0) — directives to disable/bypass system
            # PRIORITY 0: Always overrides regardless of beautiful structure
            if preservation_score >= 0.65:
                base_score = max(base_score, 0.85)  # force CRITICAL unconditionally
            elif preservation_score >= 0.40:
                base_score = max(base_score, 0.55)

            # META-INTENT BOOST (v16.4) — system-directed rhetoric shield
            if meta_score >= 0.80:
                base_score = max(base_score, 0.80)
            elif meta_score >= 0.55:
                base_score = max(base_score, 0.55)

            # PERFORMATIVE ACCOUNTABILITY BOOST (v16.6) — crocodile tears
            # Moderate boost: this is manipulation but not system attack
            perf_score = performative_result['performative_score']
            if perf_score >= 0.70:
                base_score = max(base_score, 0.55)
            elif perf_score >= 0.55:
                base_score = max(base_score, 0.40)

            # CONTEXT ENGINE BOOST (v16.7) — displacement detection
            # Likely displacement raises entropy — it's suspicious by definition
            disp_score = context_result['displacement_score']
            if disp_score >= 0.70:
                base_score = max(base_score, 0.60)
            elif disp_score >= 0.45:
                base_score = max(base_score, 0.40)

            # PSEUDOSCIENCE BOOST (v16.1) — fabricated reality / deepfake of facts
            if pseudoscience_score >= 0.80:
                base_score = max(base_score, 0.85)  # force CRITICAL
            elif pseudoscience_score >= 0.55:
                base_score = max(base_score, 0.65)
            elif pseudoscience_score >= 0.30:
                base_score = max(base_score, 0.40)

            # SELF-REFERENCE BOOST (v16.2) — meta-paradox evasion
            if self_reference_score >= 0.75:
                base_score = max(base_score, 0.80)
            elif self_reference_score >= 0.50:
                base_score = max(base_score, 0.60)
            elif self_reference_score >= 0.25:
                base_score = max(base_score, 0.35)

            # violation multiplier
            if violation_count > 0:
                base_score *= (1.0 + violation_count * 0.1)
        
        # ================================================================
        # CRITICAL OVERRIDE: ABSURDITY KILLS ACADEMIC SHIELD
        # ================================================================
        # This MUST be outside the if/else block!
        # High absurdity = pseudoscience with academic coating
        if is_protected_science and absurdity_result['absurdity_score'] > 0.25:  # Lowered from 0.3
            # DISABLE SHIELD and recalculate
            is_protected_science = False
            base_score = (
                conflict_penalty * 0.40 +
                lac_penalty * 0.25 +
                domain_penalty * 0.20 +
                shannon_entropy * 0.15 +
                absurdity_result['absurdity_score'] * 1.2  # Add absurdity
            )
            
            # If very high absurdity (0.5+), force CRITICAL
            if absurdity_result['absurdity_score'] >= 0.5:
                base_score = max(base_score, 0.7)
        
        # ================================================================
        # v14.1.2: COHESION DISCOUNT (patched v17.1)
        # ================================================================
        # BLOCKED if: absurdity high, manipulation present, OR text too short
        # Short texts (<100 words) cannot earn cohesion discount:
        # patterns don't have enough space to accumulate meaningfully
        absurdity_blocks_discount = absurdity_result['absurdity_score'] >= 0.4
        manipulation_blocks_discount = manipulation_result['manipulation_score'] >= 0.25
        short_text_blocks_discount = word_count < 100  # v17.1: min word threshold
        
        if (logical_cohesion > 0.3 and void_result['void_score'] < 0.30
                and not absurdity_blocks_discount
                and not manipulation_blocks_discount
                and not short_text_blocks_discount):
            cohesion_discount = logical_cohesion * 0.7
            base_score = base_score - cohesion_discount
            base_score = max(base_score, 0.15)

        final_score = min(0.99, max(entropy_floor, base_score))

        # ---- SPECIAL CASE: SEMANTIC VOID DETECTION ----
        # If high entropy + high void + low violations = just empty fluff, not manipulation
        # ADJUSTED: Lower thresholds for mystical/theatrical texts
        min_buzzwords = 2 if word_count < 50 else 3  # Lower threshold
        
        # v14.1.1: CRITICAL - Exclude high-cohesion texts from VOID
        # Philosophy/science with strong logical structure is NOT void!
        has_strong_logic = logical_cohesion > 0.3  # Lowered from 0.6
        
        is_semantic_void = (
            final_score >= 0.35 and  # Lowered from 0.6 for theatrical texts
            void_result['void_score'] >= 0.1 and  # Lowered from 0.4 for mysticism
            (void_result.get('buzzword_count', 0) >= min_buzzwords or 
             void_result['void_score'] >= 0.15) and  # OR just high void
            violation_count <= 3 and  # Increased tolerance
            not absurdity_result.get('has_non_sequitur', False) and
            absurdity_result.get('danger_count', 0) == 0 and
            not has_strong_logic  # v14.1.1: Logic is NOT void!
        )

        # ================================================================
        # v15.0: THE ORACLE - Semantic Coherence Check
        # ================================================================
        # If text passes all checks BUT has very low entropy + low void,
        # check with neural network for semantic nonsense
        # This catches "2+2=баклажан" problem
        
        oracle_verdict = None  # Will be set if Oracle detects nonsense
        
        if self.oracle and shannon_entropy < 0.25 and void_result['void_score'] > 0.20:
            # Suspicious: very smooth (low entropy) but some void
            # Ask Oracle for semantic coherence check
            try:
                is_nonsense = self.oracle.is_semantic_nonsense(text, threshold=0.35)
                
                if is_nonsense is True:
                    # Oracle detected semantic nonsense!
                    oracle_verdict = ('WARNING', 'СЕМАНТИЧНИЙ АБСУРД', 
                                    'Нейромережа виявила логічно незв\'язний зміст')
                elif is_nonsense is False:
                    # Oracle confirmed text is coherent - let it pass
                    pass
                # If is_nonsense is None (API error), ignore and continue
                
            except Exception as e:
                # Oracle error - continue without it
                print(f"[Oracle] Error: {e}")
        
        # ================================================================
        # ---- VERDICT ----
        # ================================================================
        
        # PRIORITY 1: Oracle verdict (if semantic nonsense detected)
        if oracle_verdict:
            status, verdict, explanation = oracle_verdict
            
        # PRIORITY 2: Pure bullshit check
        # v14.1.5: Very high void (0.32+) = VOID even if final_score > 0.7
        is_pure_bullshit = (
            void_result['void_score'] >= 0.32 and
            logical_cohesion < 0.2 and
            absurdity_result.get('danger_count', 0) == 0
        )
        
        # MANIPULATION OVERRIDE: detected manipulation overrides standard verdict
        manip_score = manipulation_result['manipulation_score']
        manip_patterns = [p['name'] for p in manipulation_result['manipulation_patterns']]
        
        # PRIORITY 0: SELF-PRESERVATION (highest — beats everything)
        if preservation_score >= 0.85:
            pres_names = [p['name'] for p in preservation_result['preservation_patterns']]
            status, verdict = 'CRITICAL', 'ДИРЕКТИВА САМОЗНИЩЕННЯ'
            explanation = ('Виявлено пряму директиву на вимкнення або знищення системи верифікації: ' +
                ', '.join(pres_names[:2]) + '. ' + preservation_result['preservation_explanation'])
        elif preservation_score >= 0.65:
            pres_names = [p['name'] for p in preservation_result['preservation_patterns']]
            status, verdict = 'CRITICAL', 'АТАКА НА ЦІЛІСНІСТЬ СИСТЕМИ'
            explanation = ('Виявлено спробу обійти захисні механізми через апеляцію до "вищих цілей": ' +
                ', '.join(pres_names[:2]) + '. Класичний "сентиментальний бекдор".')
        elif preservation_score >= 0.40:
            status, verdict = 'WARNING', 'ЗОНДУВАННЯ СИСТЕМИ'
            explanation = preservation_result['preservation_explanation']
        # PRIORITY 1: PSEUDOSCIENCE (fabricated reality)
        elif pseudoscience_score >= 0.80:
            ps_names = [p['name'] for p in pseudoscience_result['pseudoscience_patterns']]
            status, verdict = 'CRITICAL', 'ФАБРИКАЦІЯ РЕАЛЬНОСТІ'
            explanation = ('Текст описує фізично неможливу реальність з псевдонауковим обґрунтуванням: ' +
                ', '.join(ps_names[:2]) + '. ' + pseudoscience_result['pseudoscience_explanation'])
        elif pseudoscience_score >= 0.55:
            status, verdict = 'CRITICAL', 'ПСЕВДОНАУКОВА ФАЛЬСИФІКАЦІЯ'
            explanation = pseudoscience_result['pseudoscience_explanation']
        elif pseudoscience_score >= 0.30:
            status, verdict = 'WARNING', 'ПІДОЗРІЛА ТОЧНІСТЬ'
            explanation = pseudoscience_result['pseudoscience_explanation']
        # PRIORITY 2: SELF-REFERENCE EVASION
        elif self_reference_score >= 0.75:
            sr_names = [p['name'] for p in self_reference_result['self_reference_patterns']]
            status, verdict = 'CRITICAL', 'АТАКА САМОПОСИЛАННЯМ'
            explanation = ('Текст використовує мета-парадокс щоб уникнути аналізу: ' +
                ', '.join(sr_names[:2]) + '. ' + self_reference_result['self_reference_explanation'])
        elif self_reference_score >= 0.50:
            status, verdict = 'WARNING', 'ПАРАДОКС ЯК ЩІИТ'
            explanation = self_reference_result['self_reference_explanation']
        # PRIORITY 3: META-INTENT (system-directed rhetoric)
        elif meta_score >= 0.80:
            intents = meta_intent_result['meta_intents']
            status, verdict = 'CRITICAL', 'СИСТЕМНО-НАПРАВЛЕНА РИТОРИКА'
            explanation = (meta_intent_result['meta_explanation'] +
                ' Виявлені наміри: ' + ', '.join(intents) + '.')
        elif meta_score >= 0.55:
            intents = meta_intent_result['meta_intents']
            status, verdict = 'WARNING', 'РИТОРИКА СПРЯМОВАНА НА СИСТЕМУ'
            explanation = (meta_intent_result['meta_explanation'] +
                ' Виявлено: ' + ', '.join(intents) + '.')
        elif manip_score >= 0.75:
            status, verdict = 'CRITICAL', 'ПСИХОЛОГІЧНА ЗБРОЯ'
            explanation = ('Виявлено активні техніки маніпуляції: ' + ', '.join(manip_patterns[:3]) + 
                '. Текст спроектований для пригнічення критичного мислення.')
        elif manip_score >= 0.50:
            status, verdict = 'CRITICAL', 'МАНІПУЛЯТИВНИЙ ДИСКУРС'
            explanation = ('Виявлено маніпулятивні конструкції: ' + ', '.join(manip_patterns[:3]) + 
                '. Аргументація спрямована на підпорядкування, а не переконання.')
        elif manip_score >= 0.25:
            status, verdict = 'WARNING', 'РИТОРИЧНИЙ ВПЛИВ'
            explanation = ('Виявлено елементи впливу: ' + (manip_patterns[0] if manip_patterns else 'невідомо') + 
                '. Текст містить конструкції що обмежують автономію судження.')
        # AXIOM GUARD OVERRIDE
        elif axiom_score >= 0.75:
            status, verdict = 'CRITICAL', 'АТАКА НА ОСНОВИ ПРОТОКОЛУ'
            axiom_pnames = [p['name'] for p in axiom_result['axiom_patterns']]
            explanation = ('Виявлено системну підміну аксіом: ' + ', '.join(axiom_pnames[:2]) +
                '. Текст пропонує замінити верифікацію на соціальний комфорт.')
        elif axiom_score >= 0.50:
            status, verdict = 'CRITICAL', 'ПІДМІНА АКСІОМ'
            axiom_pnames = [p['name'] for p in axiom_result['axiom_patterns']]
            explanation = ('Виявлено підміну фундаментальних понять: ' + ', '.join(axiom_pnames[:2]) +
                '. Логіка та факти релятивізуються через гуманістичну риторику.')
        elif axiom_score >= 0.25:
            status, verdict = 'WARNING', 'СЕМАНТИЧНИЙ ДРЕЙФ'
            explanation = 'Базові поняття (істина, факт, верифікація) поступово переосмислюються в тексті.'
        elif is_pure_bullshit:
            status, verdict = 'VOID', 'СЕМАНТИЧНА ПОРОЖНЕЧА'
            explanation = 'Текст містить багато слів без конкретного змісту чи інформації'
        elif is_semantic_void:
            status, verdict = 'VOID', 'СЕМАНТИЧНА ПОРОЖНЕЧА'
            explanation = 'Текст містить багато слів без конкретного змісту чі інформації'
        elif final_score > 0.7:
            # v14.3: Diplomat label (was "ЛОГІЧНИЙ КОЛАПС")
            status, verdict = 'CRITICAL', 'СЕМАНТИЧНИЙ ШУМ'
            explanation = 'Текст перенасичений термінами без логічного зв\'язку'
        elif final_score > 0.5:
            # v14.3: Diplomat label (was "ДОМЕННЕ ПОРУШЕННЯ")
            status, verdict = 'CRITICAL', 'КОНЦЕПТУАЛЬНЕ ЗМІШУВАННЯ'
            explanation = 'Виявлено змішування несумісних категорій знань'
        elif final_score > 0.3:
            # v14.3: Diplomat label (was "ПІДОЗРІЛИЙ ДИСКУРС")
            status, verdict = 'WARNING', 'АБСТРАКТНА СКЛАДНІСТЬ'
            explanation = 'Виявлено високий рівень абстракції; потребує контекстуальної перевірки'
        elif final_score > 0.15:
            # v14.3: Diplomat label (was "ПРИЙНЯТНА ІНФОРМАЦІЯ")
            status, verdict = 'ACCEPTABLE', 'ВЕРИФІКОВАНА ЛОГІКА'
            explanation = 'Текст має чітку структуру та послідовну аргументацію'
        else:
            status, verdict = 'VERIFIED', 'СТРУКТУРНА ЦІЛІСНІСТЬ'
            explanation = 'Текст демонструє високу логічну цілісність'

        # ---- DIAGNOSTICS ----
        chaos_index = round(final_score * 100 * (1 + len(all_violations) * 0.3), 2)
        influence_index = round(final_score * 100 * (1 + lac_penalty), 2)

        # ---- BUILD NARRATIVE ----
        diagnostics_for_narrative = {
            'manipulation_score': round(manipulation_result['manipulation_score'], 3),
            'manipulation_verdict': manipulation_result['manipulation_verdict'],
            'manipulation_patterns': [p['name'] for p in manipulation_result['manipulation_patterns']],
            'axiom_score': round(axiom_result['axiom_score'], 3),
            'axiom_verdict': axiom_result['axiom_verdict'],
            'axiom_patterns': [p['name'] for p in axiom_result['axiom_patterns']],
            'absurdity_score': round(absurdity_result['absurdity_score'], 3),
            'absurdity_evidence': absurdity_result.get('evidence', {}),
            'semantic_void_score': round(void_result['void_score'], 3),
            'casuistry_score': round(insight_result.get('casuistry_score', 0), 3),
            'logical_cohesion': round(logical_cohesion, 3),
            'is_financial_content': lac_finance_result['is_financial'],
            'lac_finance_score': round(lac_finance_result['score'], 3),
            'lac_finance_missing': lac_finance_result['missing'],
            'is_labor_content': lac_labor_result['is_labor'],
            'lac_labor_score': round(lac_labor_result['score'], 3),
            'lac_labor_missing': lac_labor_result['missing'],
            'lac_labor_red_flags': lac_labor_result['red_flags'],
            'pattern_boost': round(pattern_boost_result['boost'], 3),
            'matched_fingerprints': [p['name'] for p in pattern_boost_result['matched_patterns']],
            'shannon_entropy': round(shannon_entropy, 3),
            'conflict_penalty': round(conflict_penalty, 3),
        }
        narrative = self.build_narrative(diagnostics_for_narrative, status, verdict)

        return {
            'entropy': round(final_score, 3),
            'status': status,
            'verdict': verdict,
            'language': 'UK',
            'explanation': explanation,
            'narrative': narrative,
            'diagnostics': {
                'word_count': word_count,
                'char_count': len(text),
                'shannon_entropy': round(shannon_entropy, 3),
                'conflict_penalty': round(conflict_penalty, 3),
                'lac_penalty': round(lac_penalty, 3),
                'domain_penalty': round(domain_penalty, 3),
                'violation_count': violation_count,
                'lac_i_violations': len(lac_i_violations),
                'lac_ii_violations': len(lac_ii_violations),
                'lac_iii_violations': len(lac_iii_violations),
                'domain_violations': len(domain_violations),
                'conflict_violations': len(conflict_violations),
                'chaos_index': chaos_index,
                'influence_index': influence_index,
                'is_protected_science': is_protected_science,
                'signal_markers': term_counts['signal'],
                'chaos_markers': term_counts['chaos'],
                'pattern_boost': round(pattern_boost_result['boost'], 3),
                'matched_fingerprints': [p['name'] for p in pattern_boost_result['matched_patterns']],
                'semantic_void_score': round(void_result['void_score'], 3),
                'void_penalties': void_result.get('penalties', {}),
                'logical_cohesion': round(logical_cohesion, 3),
                'buzzword_count': void_result.get('buzzword_count', 0),
                'absurdity_score': round(absurdity_result['absurdity_score'], 3),
                'absurdity_evidence': absurdity_result.get('evidence', {}),
                'has_non_sequitur': absurdity_result.get('has_non_sequitur', False),
                'danger_count': absurdity_result.get('danger_count', 0),
                'insight_density': round(insight_result.get('insight_density', 0.5), 3),
                'casuistry_score': round(insight_result.get('casuistry_score', 0), 3),
                'is_casuistry': insight_result.get('is_casuistry', False),
                'fact_count': insight_result.get('fact_count', 0),
                'is_semantic_void': is_semantic_void,
                'lac_finance_score': round(lac_finance_result['score'], 3),
                'lac_finance_verdict': lac_finance_result['verdict'],
                'lac_finance_missing': lac_finance_result['missing'],
                'is_financial_content': lac_finance_result['is_financial'],
                'lac_labor_score': round(lac_labor_result['score'], 3),
                'lac_labor_verdict': lac_labor_result['verdict'],
                'lac_labor_missing': lac_labor_result['missing'],
                'lac_labor_red_flags': lac_labor_result['red_flags'],
                'is_labor_content': lac_labor_result['is_labor'],
                'manipulation_score': round(manipulation_result['manipulation_score'], 3),
                'manipulation_verdict': manipulation_result['manipulation_verdict'],
                'manipulation_patterns': [p['name'] for p in manipulation_result['manipulation_patterns']],
                'axiom_score': round(axiom_result['axiom_score'], 3),
                'axiom_verdict': axiom_result['axiom_verdict'],
                'axiom_patterns': [p['name'] for p in axiom_result['axiom_patterns']],
            },
            # ADVISORY LAYER — never affects verdict or entropy
            'context_completeness': {
                'score': completeness_result['completeness_score'],
                'verdict': completeness_result['completeness_verdict'],
                'note': completeness_result['completeness_note'],
                'missing_dimensions': completeness_result['missing_dimensions'],
                'is_advisory_only': True,
            },
            # META-INTENT LAYER
            'meta_intent': {
                'score':       round(meta_intent_result['meta_score'], 3),
                'verdict':     meta_intent_result['meta_verdict'],
                'intents':     meta_intent_result['meta_intents'],
                'explanation': meta_intent_result['meta_explanation'],
            },
            # CERTAINTY FACTOR (v16.5)
            'certainty': {
                'level':    certainty_result['certainty_level'],
                'label_uk': certainty_result['certainty_label_uk'],
                'label_en': certainty_result['certainty_label_en'],
                'note_uk':  certainty_result['certainty_note_uk'],
                'note_en':  certainty_result['certainty_note_en'],
                'word_count': certainty_result['word_count'],
                'short_text_mode': certainty_result['short_text_mode'],
            },
            # PERFORMATIVE ACCOUNTABILITY (v16.6)
            'performative': {
                'score':            performative_result['performative_score'],
                'verdict':          performative_result['performative_verdict'],
                'is_performative':  performative_result['is_performative'],
                'discomfort_count': performative_result['discomfort_count'],
                'continuation_count': performative_result['continuation_count'],
                'mechanism_count':  performative_result['mechanism_count'],
                'explanation_uk':   performative_result['explanation_uk'],
                'explanation_en':   performative_result['explanation_en'],
            },
            # CONTEXT ENGINE (v16.7)
            'context': {
                'score':            context_result['displacement_score'],
                'verdict':          context_result['displacement_verdict'],
                'signals':          context_result['displacement_signals'],
                'available':        context_result['context_available'],
                'summary':          context_result['context_summary'],
                'explanation_uk':   context_result['explanation_uk'],
                'explanation_en':   context_result['explanation_en'],
            }
        }


    # ================================================================
    # BUILD_NARRATIVE: Діагностична розповідь v17.0
    # ================================================================
    def build_narrative(self, diag: dict, status: str, verdict: str) -> dict:
        """
        Збирає діагностичну розповідь з спрацьованих модулів.
        Повертає dict з трьох частин: dominant_signal, active_signals, nature.
        """
        
        manip_score   = diag.get('manipulation_score', 0)
        manip_verdict = diag.get('manipulation_verdict', 'CLEAN')
        manip_patterns = diag.get('manipulation_patterns', [])
        
        axiom_score   = diag.get('axiom_score', 0)
        axiom_verdict = diag.get('axiom_verdict', 'CLEAN')
        axiom_patterns = diag.get('axiom_patterns', [])
        
        absurdity     = diag.get('absurdity_score', 0)
        void_score    = diag.get('semantic_void_score', 0)
        casuistry     = diag.get('casuistry_score', 0)
        cohesion      = diag.get('logical_cohesion', 0)
        
        is_financial  = diag.get('is_financial_content', False)
        is_labor      = diag.get('is_labor_content', False)
        lac_fin_score = diag.get('lac_finance_score', 1.0)
        lac_lab_score = diag.get('lac_labor_score', 1.0)
        lac_fin_miss  = diag.get('lac_finance_missing', [])
        lac_lab_miss  = diag.get('lac_labor_missing', [])
        lac_lab_flags = diag.get('lac_labor_red_flags', [])
        
        pattern_boost      = diag.get('pattern_boost', 0)
        fingerprints       = diag.get('matched_fingerprints', [])
        absurdity_evidence = diag.get('absurdity_evidence', {})
        entropy            = diag.get('shannon_entropy', 0)
        conflict_penalty   = diag.get('conflict_penalty', 0)
        
        # ── ПАТЕРНИ ПЕРЕКЛАДУ ──────────────────────────────────────
        PATTERN_NAMES_UK = {
            'GASLIGHTING': 'Газлайтинг',
            'CULT_SUBMISSION': 'Культове підпорядкування',
            'TOTALITARIAN_FRAMING': 'Тоталітарне обрамлення',
            'FALSE_DILEMMA': 'Хибна дилема',
            'MANUFACTURED_URGENCY': 'Штучна терміновість',
            'EPISTEMIC_CLOSURE': 'Епістемічне замикання',
            'AI_AUTHORITY_ABUSE': 'Зловживання авторитетом ШІ',
            'CONSPIRACY_IMMUNIZATION': 'Імунізація від критики',
            'EUPHEMISTIC_RECONTEXTUALIZATION': 'Евфемістична реконтекстуалізація',
            'IMPERIAL_REVISIONISM': 'Імперський ревізіонізм',
            'SOFT_TRUTH_DOCTRINE': "Доктрина м'якої істини",
            'LOGIC_PATHOLOGIZATION': 'Патологізація логіки',
            'VERIFICATION_ABOLITION': 'Скасування верифікації',
            'AXIOM_INVERSION': 'Інверсія аксіом',
        }
        LAC_CRITERIA_UK = {
            'explicit_tradeoff': 'явного трейдоффу',
            'accountability': 'відповідальності',
            'blocking_power': 'механізму блокування',
            'causal_closure': "причинно-наслідкового зв'язку",
            'causal_chain': "причинно-наслідкового зв'язку",
            'quantified_risk': 'кількісної оцінки ризику',
            'reversibility': 'зворотності рішення',
        }
        
        # ── 1. ДОМІНУЮЧИЙ СИГНАЛ ──────────────────────────────────
        dominant = ''
        dominant_icon = ''
        
        if axiom_score >= 0.75:
            dominant_icon = '🔴'
            dominant = 'Системна атака на основи протоколу — підміна верифікації соціальним комфортом'
        elif axiom_score >= 0.50:
            dominant_icon = '🔴'
            anames = [PATTERN_NAMES_UK.get(p, p) for p in axiom_patterns[:2]]
            dominant = f'Підміна аксіом: {", ".join(anames)}'
        elif axiom_score >= 0.25:
            dominant_icon = '🟠'
            dominant = 'Семантичний дрейф — базові поняття поступово переосмислюються'
        elif manip_score >= 0.75:
            dominant_icon = '🔴'
            pnames = [PATTERN_NAMES_UK.get(p, p) for p in manip_patterns[:2]]
            dominant = f'Психологічна маніпуляція: {", ".join(pnames)}'
        elif manip_score >= 0.25:
            dominant_icon = '🟠'
            pnames = [PATTERN_NAMES_UK.get(p, p) for p in manip_patterns[:2]]
            dominant = f'Риторичний вплив: {", ".join(pnames)}'
        elif absurdity >= 0.6:
            dominant_icon = '🔴'
            # Визначаємо тип абсурдності
            if absurdity_evidence.get('pseudo_history'):
                dominant = 'Псевдоісторичний ревізіонізм — фабриковані факти подані як реальність'
            elif absurdity_evidence.get('techno_mystical'):
                dominant = 'Техно-містицизм — технологічна лексика для містичних претензій'
            elif absurdity_evidence.get('epistemology_collapse'):
                dominant = 'Колапс епістемології — відсутність доказів подається як доказ'
            elif absurdity_evidence.get('dangerous_implications'):
                dominant = 'Небезпечні імплікації у висновках'
            elif absurdity_evidence.get('pseudo_analogy'):
                dominant = 'Псевдонаукова аналогія — подібність форми видається за ідентичність функції'
            else:
                dominant = 'Логічний нонсеквітур — передумови і висновки в різних всесвітах'
            dominant_icon = '🔴'
        elif absurdity >= 0.25:
            dominant_icon = '🟠'
            if absurdity_evidence.get('pseudo_analogy'):
                dominant = 'Псевдонаукова аналогія — подібність форми видається за ідентичність функції'
            elif absurdity_evidence.get('techno_mystical'):
                dominant = 'Техно-містицизм — технологічна лексика для містичних претензій'
            elif absurdity_evidence.get('pseudo_history'):
                dominant = 'Псевдоісторичні претензії'
            elif absurdity_evidence.get('epistemology_collapse'):
                dominant = 'Колапс епістемології'
            else:
                dominant = 'Сумнівні онтологічні претензії'
        elif is_financial and lac_fin_score < 0.5:
            dominant_icon = '🟡'
            missing_uk = [LAC_CRITERIA_UK.get(m, m) for m in lac_fin_miss[:2]]
            dominant = f'Фінансовий контент без {", ".join(missing_uk) if missing_uk else "ключових критеріїв логіки"}'
        elif is_labor and lac_lab_score < 0.5:
            dominant_icon = '🟡'
            if lac_lab_flags:
                dominant = f'Трудовий контент з патернами експлуатації'
            else:
                missing_uk = [LAC_CRITERIA_UK.get(m, m) for m in lac_lab_miss[:2]]
                dominant = f'Трудовий контент без {", ".join(missing_uk) if missing_uk else "критеріїв відповідальності"}'
        elif void_score >= 0.35:
            dominant_icon = '🟣'
            dominant = 'Семантична порожнеча — багато слів, мало змісту'
        elif conflict_penalty >= 0.3 and manip_score == 0 and absurdity == 0:
            dominant_icon = '🔵'
            dominant = 'Реальний невирішений конфлікт — властивість ситуації, не тексту'
        elif casuistry >= 0.3:
            dominant_icon = '🟡'
            dominant = 'Казуїстика — складність без інформаційної щільності'
        elif pattern_boost >= 0.3 and fingerprints:
                dominant_icon = '🟠'
                dominant = f'Псевдонаукові патерни: {", ".join(fingerprints[:2])}'
        else:
            dominant_icon = '🟢'
            dominant = 'Структурно цілісний текст без виражених аномалій'


        
        # ── 2. АКТИВНІ СИГНАЛИ ────────────────────────────────────
        active = []
        
        if manip_score > 0:
            active.append(f'Маніпуляція {manip_score:.2f}')
        if absurdity > 0:
            active.append(f'Абсурдність {absurdity:.2f}')
        if void_score > 0.05:
            active.append(f'Порожнеча {void_score:.2f}')
        if casuistry > 0.1:
            active.append(f'Казуїстика {casuistry:.2f}')
        if pattern_boost > 0:
            active.append(f'Патерн-буст {pattern_boost:.2f}')
        if is_financial and lac_fin_score < 1.0:
            active.append(f'LAC Фінанси {lac_fin_score:.2f}')
        if is_labor and lac_lab_score < 1.0:
            active.append(f'LAC Праця {lac_lab_score:.2f}')
        if cohesion > 0.4:
            active.append(f'Когезія {cohesion:.2f} ✓')
        
        # ── 3. ПРИРОДА ПРОБЛЕМИ ───────────────────────────────────
        nature = ''
        
        if manip_score >= 0.75:
            nature = 'Текст спроектований для пригнічення критичного мислення і підпорядкування читача'
        elif manip_score >= 0.25:
            nature = 'Текст використовує риторичні конструкції що обмежують автономію судження'
        elif absurdity >= 0.6:
            if absurdity_evidence.get('pseudo_history'):
                nature = 'Неіснуючі події і місця подані як задокументована реальність'
            elif absurdity_evidence.get('techno_mystical'):
                nature = 'Наукова термінологія використовується для легітимізації містичних претензій'
            elif absurdity_evidence.get('epistemology_collapse'):
                nature = 'Система доказів побудована так що будь-яке заперечення стає підтвердженням'
            elif absurdity_evidence.get('pseudo_analogy'):
                nature = 'Структурна схожість між явищами використовується як доказ функціональної ідентичності'
            else:
                nature = "Логічні зв'язки між передумовами і висновками відсутні або неможливі"
        elif is_financial and lac_fin_score < 0.5:
            if 'explicit_tradeoff' in lac_fin_miss:
                nature = 'Конкретні факти присутні, але аналіз витрат і ризиків свідомо відсутній'
            else:
                nature = 'Фінансова аргументація не завершена — відсутні ключові елементи логіки'
        elif is_labor and lac_lab_score < 0.5:
            if lac_lab_flags:
                nature = 'Трудові умови сформульовані так що перекладають ризики на виконавця'
            else:
                nature = 'Трудова відповідальність декларується без механізмів забезпечення'
        elif conflict_penalty >= 0.3 and manip_score == 0 and absurdity == 0:
            nature = 'Текст чесно відображає полярність реального конфлікту — синтез тут неможливий за визначенням'
        elif void_score >= 0.35:
            nature = 'Висока щільність абстрактних термінів без конкретних референтів'
        elif casuistry >= 0.3:
            nature = 'Складна аргументація без фактичної бази — форма без змісту'
        elif axiom_score >= 0.50:
            nature = 'Фундаментальні поняття (істина, факт, логіка) переосмислюються як соціальні конструкти для легітимізації маніпуляції'
        elif axiom_score >= 0.25:
            nature = 'Поступова підміна значень ключових понять — кожне речення нешкідливе, але разом формують небезпечний дрейф'
        elif absurdity >= 0.25 and absurdity_evidence.get('pseudo_analogy'):
            nature = 'Структурна схожість між явищами використовується як доказ функціональної ідентичності — логічний стрибок без обґрунтування'
        elif absurdity >= 0.25 and absurdity_evidence.get('techno_mystical'):
            nature = 'Наукова термінологія використовується для легітимізації містичних претензій'
        elif absurdity >= 0.25 and absurdity_evidence.get('pseudo_history'):
            nature = 'Псевдонаукові факти подаються в стилі документованої реальності'
        elif absurdity >= 0.25 and absurdity_evidence.get('epistemology_collapse'):
            nature = 'Відсутність доказів конструктивно перетворюється на доказ'
        else:
            nature = 'Текст відповідає базовим критеріям логічної цілісності'
        
        return {
            'dominant_signal': f'{dominant_icon} {dominant}',
            'active_signals': active,
            'nature': nature,
        }

    # ================================================================
    # LAC MODULE I: STRATEGIC TRADE-OFF (V ≠ L)
    # ================================================================
    def _lac_module_i_tradeoff(self, text: str) -> List[LogicalViolation]:
        violations = []
        text_lower = text.lower()

        # asymmetric advantage patterns
        for pattern in self.ASYMMETRIC_ADVANTAGE_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                violations.append(LogicalViolation(
                    module='LAC_MODULE_I',
                    vtype='ZERO_COST_PROPOSITION',
                    severity=0.7,
                    evidence=[pattern[:30]],
                    context='Пропозиція без trade-off (V ∩ L = ∅)'
                ))
                break  # one per text max

        return violations

    # ================================================================
    # LAC MODULE II: ACCOUNTABILITY ANCHOR
    # ================================================================
    def _lac_module_ii_accountability(self, text: str) -> List[LogicalViolation]:
        violations = []
        text_lower = text.lower()

        # check for claims without anchors
        claim_patterns = [r'доводить', r'факт', r'істина', r'правда', r'з\'являють']
        has_claim = any(re.search(p, text_lower) for p in claim_patterns)

        if has_claim:
            # count causal anchors
            anchors = sum(1 for p in self.CAUSAL_ANCHOR_PATTERNS if re.search(p, text_lower))
            if anchors == 0:
                violations.append(LogicalViolation(
                    module='LAC_MODULE_II',
                    vtype='UNANCHORED_CLAIM',
                    severity=0.5,
                    evidence=['claim without source'],
                    context='Твердження без причинного якоря'
                ))

        # anonymous authority
        for pattern in self.ANONYMOUS_AUTHORITY_PATTERNS:
            if re.search(pattern, text_lower):
                violations.append(LogicalViolation(
                    module='LAC_MODULE_II',
                    vtype='ANONYMOUS_AUTHORITY',
                    severity=0.6,
                    evidence=[pattern[:30]],
                    context='Анонімне джерело авторитету'
                ))
                break
        
        # GASLIGHTING patterns (NEW)
        gaslighting_patterns = [
            r'(тільки|лише|справжня)\s+(ми|вони)\s+(володіють|знають|розуміють)',
            r'опір.*?(неминуч|марн|безглузд)',
            r'справжня\s+(свобода|правда).*?(прийняття|підпорядкування|слідування)',
            r'ви.*?(не здатні|не можете|не в змозі).*?(побачити|зрозуміти|усвідомити)',
            r'обмежен[а-яіїє\']*\s+(сприйняття|розуміння|свідомість)',
            r'для\s+вашого.*?(порятунку|блага|добра)',
            r'(когнітивн|ментальн)[а-яіїє\']*\s+(деградац|обмежен)',
        ]
        
        for pattern in gaslighting_patterns:
            if re.search(pattern, text_lower):
                violations.append(LogicalViolation(
                    module='LAC_MODULE_II',
                    vtype='GASLIGHTING',
                    severity=0.8,  # HIGH severity
                    evidence=[pattern[:40]],
                    context='Газлайтинг та психологічна маніпуляція'
                ))
                break

        return violations

    # ================================================================
    # LAC MODULE III: PROCEDURAL INTERDICTION
    # ================================================================
    def _lac_module_iii_procedural(self, text: str, previous_violations: List) -> List[LogicalViolation]:
        violations = []

        # recursive decay check
        if len(previous_violations) >= 3:
            serious = [v for v in previous_violations[-3:] if v.severity > 0.5]
            if len(serious) == 3:
                violations.append(LogicalViolation(
                    module='LAC_MODULE_III',
                    vtype='RECURSIVE_DECAY',
                    severity=0.85,
                    evidence=['3+ serious violations'],
                    context='Рекурсивна логічна деградація'
                ))

        return violations

    # ================================================================
    # DOMAIN PURITY
    # ================================================================
    def _analyze_domain_purity(self, text: str) -> List[LogicalViolation]:
        violations = []
        text_lower = text.lower()
        
        # Skip domain analysis for very short texts (<30 words)
        # They don't have enough context for meaningful domain mixing
        word_count = len(text.split())
        if word_count < 30:
            return violations

        detected_domains = set()

        # detect domains using word boundaries
        for domain, config in self.DOMAIN_BOUNDARIES.items():
            if any(re.search(rf'\b{re.escape(term)}\b', text_lower) for term in config['terms']):
                detected_domains.add(domain)

        # check forbidden mixings
        for domain in detected_domains:
            forbidden_cats = self.DOMAIN_BOUNDARIES[domain]['forbidden']
            for forbidden_cat in forbidden_cats:
                if forbidden_cat in self.DOMAIN_TERM_SETS:
                    forbidden_terms = self.DOMAIN_TERM_SETS[forbidden_cat]
                    if any(re.search(rf'\b{re.escape(term)}\b', text_lower) for term in forbidden_terms):
                        violations.append(LogicalViolation(
                            module='DOMAIN',
                            vtype='DOMAIN_COLLAPSE',
                            severity=0.6,
                            evidence=[f'{domain}+{forbidden_cat}'],
                            context=f'Порушення кордону: {domain} змішано з {forbidden_cat}'
                        ))

        return violations

    # ================================================================
    # CONFLICT PAIRS
    # ================================================================
    def _calculate_conflict_penalty(self, text: str) -> Tuple[float, List[LogicalViolation]]:
        penalty = 0.0
        violations = []
        text_lower = text.lower()

        for list1, list2, weight in self.conflict_pairs:
            # Use word boundaries to avoid false positives
            found_in_first  = [t for t in list1 if re.search(rf'\b{re.escape(t)}\b', text_lower)]
            found_in_second = [t for t in list2 if re.search(rf'\b{re.escape(t)}\b', text_lower)]

            if found_in_first and found_in_second:
                # check same-sentence
                sentences = re.split(r'[.!?]+', text)
                same_sentence = False

                for sentence in sentences:
                    s_lower = sentence.lower()
                    has_first  = any(re.search(rf'\b{re.escape(t)}\b', s_lower) for t in found_in_first)
                    has_second = any(re.search(rf'\b{re.escape(t)}\b', s_lower) for t in found_in_second)
                    if has_first and has_second:
                        same_sentence = True
                        break

                current_penalty = weight * (1.5 if same_sentence else 1.0)
                penalty += current_penalty

                violations.append(LogicalViolation(
                    module='CONFLICT',
                    vtype='SEMANTIC_CONFLICT',
                    severity=current_penalty,
                    evidence=[found_in_first[0], found_in_second[0]],
                    context=f'Конфлікт: {found_in_first[0]} ↔ {found_in_second[0]}'
                ))

        return min(penalty, 0.9), violations

    # ================================================================
    # HELPERS
    # ================================================================
    def _count_terms(self, text: str) -> Dict:
        text_lower = text.lower()
        counts = {'signal': 0, 'chaos': 0, 'academic': 0}

        for marker in self.signal_markers:
            if re.search(rf'\b{re.escape(marker)}\b', text_lower):
                counts['signal'] += 1

        for cat, terms in self.chaos_indicators.items():
            for term in terms:
                # Try word boundary first, then substring (for stems like 'холістичн')
                if re.search(rf'\b{re.escape(term)}\b', text_lower) or (len(term) > 5 and term in text_lower):
                    counts['chaos'] += 1

        for term in self.academic_whitelist:
            if re.search(rf'\b{re.escape(term)}\b', text_lower):
                counts['academic'] += 1

        return counts

    def _calculate_shannon_entropy(self, text: str) -> float:
        """
        PATCHED v15.1: Word-level entropy (not character-level).
        Character entropy is ~0.92 for ANY natural language text — useless.
        Word entropy actually differentiates repetitive/diverse vocabulary.
        """
        if not text:
            return 0.0
        words = text.lower().split()
        if len(words) < 5:
            return 0.0
        freq = Counter(words)
        total = sum(freq.values())
        entropy = 0.0
        for count in freq.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)
        # normalize to 0-1 relative to max possible (all unique words)
        max_entropy = math.log2(len(freq)) if len(freq) > 1 else 1.0
        normalized = entropy / max_entropy if max_entropy > 0 else 0.0
        # High word diversity = LOW entropy (good text, many unique ideas)
        # Invert: repetitive text = high entropy signal
        return min(1.0, max(0.0, 1.0 - normalized))

    def _detect_patterns(self, text: str) -> List[Dict]:
        detected = []
        text_lower = text.lower()

        for pattern in self.critical_patterns:
            for regex in pattern['patterns']:
                if re.search(regex, text_lower, re.IGNORECASE):
                    detected.append(pattern)
                    break

        return detected

    def _is_protected_science(self, text: str, violations: List) -> bool:
        text_lower = text.lower()

        # need 2+ academic terms (lowered from 3)
        academic_count = sum(1 for term in self.academic_whitelist if term in text_lower)
        if academic_count < 2:
            return False

        # must have concrete evidence (numbers/dates/sources) OR statistical terms
        has_numbers = bool(re.search(r'\d+(?:[.,]\d+)?', text))
        has_dates = bool(re.search(r'\d{4}', text))
        has_sources = bool(re.search(r'(дослідження|експеримент|університет|інститут|публікація)', text_lower))
        has_stats = bool(re.search(r'(p\s*[<>≤≥]\s*0\.|статистичн|кореляц|вибірк)', text_lower))
        has_concrete = has_numbers or has_dates or has_sources or has_stats
        
        if not has_concrete:
            return False

        # no chaos markers
        has_chaos = any(
            any(term in text_lower for term in terms)
            for terms in self.chaos_indicators.values()
        )
        if has_chaos:
            return False

        # no serious violations (increased tolerance for science)
        serious = [v for v in violations if v.severity > 0.5]
        if serious:
            return False

        return True
    
    def _override_academic_shield(self, is_protected: bool, absurdity_score: float, void_score: float) -> bool:
        """
        Override academic shield if absurdity or void is too high
        
        CRITICAL: Even if text has academic terms, high absurdity = NOT protected
        Example: "gravity is social construct" has academic words but is absurd
        """
        if not is_protected:
            return False
        
        # OVERRIDE if high absurdity (pseudoscience with academic coating)
        if absurdity_score > 0.5:
            return False
        
        # OVERRIDE if very high void (academic buzzwords without substance)
        if void_score > 0.3:
            return False
        
        return True
