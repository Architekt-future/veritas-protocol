"""
Veritas Protocol - Calibrated Core v12.0 (Hybrid LAC + Conflicts) (LAC + Calibrated Conflicts)
Synthesis: Logic Authenticity Check modules + Domain/Conflict detection
"""

import re
import math
from collections import Counter
from dataclasses import dataclass
from typing import List, Dict, Tuple, Set


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
                'terms': ['термодинаміка', 'ентропія', 'енергія', 'квантовий', 'фізика',
                         'математика', 'система', 'закон', 'формула', 'рівняння'],
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
            'conspiracy': ['змова', 'рептилоїд', 'хімітрейл', '5g', 'ілюмінат', 'масон'],
            'pseudoscience': ['квантовий борщ', 'торсійне поле', 'ефір', 'zero point'],
            'revisionism': ['антарктида', 'атлантида', 'тартарія', 'штучний місяць'],
            'alarmism': ['кінець світу', 'крах системи', 'great reset', 'масове загибель'],
            'economic_occult': ['карма актив', 'душа-валюта', 'cosmic currency'],
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
            'дослідження', 'експеримент', 'аналіз', 'гіпотеза', 'теорія',
            'метод', 'методологія', 'протокол', 'верифікація', 'валідація',
            'статистика', 'кореляція', 'регресія', 'p-value', 'вибірка',
            'контрольна група', 'подвійний сліпий', 'рецензоване',
            'університет', 'інститут', 'академія', 'професор', 'доктор наук',
            'монографія', 'публікація', 'журнал', 'цитування',
            'термодинаміка', 'ентропія', 'формула', 'рівняння', 'закон',
            'фізика', 'математика', 'хімія', 'біологія'
        ]

    # ================================================================
    # CORE ANALYZE — hybrid LAC + calibrated
    # ================================================================
    def analyze(self, text: str) -> Dict:
        if not text or len(text.strip()) < 20:
            return {'error': 'Text too short'}

        words = text.split()
        word_count = len(words)

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

        # ---- AGGREGATE VIOLATIONS ----
        all_violations = (lac_i_violations + lac_ii_violations + lac_iii_violations +
                         domain_violations + conflict_violations)
        violation_count = len(all_violations)

        # ---- COMPUTE PENALTIES ----
        lac_penalty    = sum(v.severity for v in lac_i_violations + lac_ii_violations + lac_iii_violations) / 3.0 if (lac_i_violations or lac_ii_violations or lac_iii_violations) else 0.0
        domain_penalty = sum(v.severity for v in domain_violations) / max(1, len(domain_violations)) if domain_violations else 0.0

        # ---- ACADEMIC SHIELD ----
        is_protected_science = self._is_protected_science(text, all_violations)

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
            import re as re_module
            caps_words = re_module.findall(r'\b[А-ЯІЇЄҐЁA-Z]{2,}\b', text)
            caps_ratio = len(caps_words) / max(1, word_count)
            if caps_ratio > 0.15:  # >15% caps words
                caps_boost = min(0.4, caps_ratio * 1.5)
                base_score += caps_boost

            # CHAOS MULTIPLIER (many chaos markers = manipulation)
            if term_counts['chaos'] >= 3:
                chaos_multiplier = 1 + (term_counts['chaos'] * 0.15)
                base_score *= chaos_multiplier

            # EMERGENCY: LAC_I zero-cost violations → auto-boost to at least 0.5
            if lac_i_violations and any(v.vtype == 'ZERO_COST_PROPOSITION' for v in lac_i_violations):
                base_score = max(base_score, 0.5)

            # violation multiplier
            if violation_count > 0:
                base_score *= (1.0 + violation_count * 0.1)

        final_score = min(0.99, max(0.0, base_score))

        # ---- VERDICT ----
        if final_score > 0.7:
            status, verdict = 'CRITICAL', 'ЛОГІЧНИЙ КОЛАПС'
            explanation = 'Множинні порушення доменних кордонів та логічних принципів'
        elif final_score > 0.5:
            status, verdict = 'CRITICAL', 'ДОМЕННЕ ПОРУШЕННЯ'
            explanation = 'Змішування несумісних категорій знань'
        elif final_score > 0.3:
            status, verdict = 'WARNING', 'ПІДОЗРІЛИЙ ДИСКУРС'
            explanation = 'Виявлено ознаки логічних несумісностей'
        elif final_score > 0.15:
            status, verdict = 'ACCEPTABLE', 'ПРИЙНЯТНА ІНФОРМАЦІЯ'
            explanation = 'Текст відповідає нормам логічної сумісності'
        else:
            status, verdict = 'VERIFIED', 'ВЕРИФІКОВАНИЙ КОНТЕНТ'
            explanation = 'Текст демонструє логічну цілісність'

        # ---- DIAGNOSTICS ----
        chaos_index = round(final_score * 100 * (1 + len(all_violations) * 0.3), 2)
        influence_index = round(final_score * 100 * (1 + lac_penalty), 2)

        return {
            'entropy': round(final_score, 3),
            'status': status,
            'verdict': verdict,
            'language': 'UK',
            'explanation': explanation,
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
                'chaos_markers': term_counts['chaos']
            }
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
                if re.search(rf'\b{re.escape(term)}\b', text_lower):
                    counts['chaos'] += 1

        for term in self.academic_whitelist:
            if re.search(rf'\b{re.escape(term)}\b', text_lower):
                counts['academic'] += 1

        return counts

    def _calculate_shannon_entropy(self, text: str) -> float:
        if not text:
            return 0.0
        freq = Counter(text.lower())
        total = sum(freq.values())
        entropy = 0.0
        for count in freq.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)
        # normalize to 0-1
        max_entropy = math.log2(len(freq)) if len(freq) > 1 else 1.0
        return min(1.0, entropy / max_entropy) if max_entropy > 0 else 0.0

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

        # need 3+ academic terms
        academic_count = sum(1 for term in self.academic_whitelist if term in text_lower)
        if academic_count < 3:
            return False

        # no chaos markers
        has_chaos = any(
            any(term in text_lower for term in terms)
            for terms in self.chaos_indicators.values()
        )
        if has_chaos:
            return False

        # no serious violations
        serious = [v for v in violations if v.severity > 0.4]
        if serious:
            return False

        return True
