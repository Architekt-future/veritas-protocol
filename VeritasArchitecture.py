"""
VERITAS PROTOCOL - АРХІТЕКТУРНА ІМПЛЕМЕНТАЦІЯ
Відповідно до принципів з документа:
"The Veritas Protocol: A Substrate-Agnostic Framework for Enforcing Logical Determinism"

Версія: 1.0.0 (Architectural Divergence)
Автор: Логічний Інквізитор
"""

import re
import math
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional, Set
from enum import Enum

class EntropyType(Enum):
    """Таксономія інформаційної ентропії згідно з документом"""
    TYPE_I_DETERMINISTIC = "Deterministic Data (Zero-Entropy)"
    TYPE_II_PROBABILISTIC = "Probabilistic Synthesis (Moderate Entropy)"
    TYPE_III_THEATRICAL = "Theatrical Rhetoric (High Entropy)"
    TYPE_IV_SEMANTIC_NOISE = "Semantic Noise (Critical Entropy)"

class SystemState(Enum):
    """Операційні стани системи згідно з таблицею 1"""
    LAMINAR_FLOW = "Laminar Flow"
    SYSTEMIC_FATIGUE = "Systemic Fatigue"
    WITNESS_SILENCE = "Witness Silence"

@dataclass
class LogicalViolation:
    """Логічне порушення високого рівня"""
    module: str  # Модуль LAC, який виявив порушення
    violation_type: str
    severity: float  # 0.0-1.0
    evidence: List[str]
    context: str
    section: str  # Розділ тексту, де виявлено порушення

@dataclass
class DomainAnalysis:
    """Аналіз доменної чистоти"""
    primary_domain: str
    detected_domains: Set[str]
    purity_score: float  # 0.0-1.0 (1.0 = чистий домен)
    domain_collapses: List[Tuple[str, str]]  # Пари змішаних доменів
    causal_anchors: int  # Кількість причинних якорів (γ)
    adjectival_density: float  # Густина прикметників (α)

@dataclass
class StrategicProposition:
    """Стратегічна пропозиція для аналізу V≠L"""
    text: str
    claimed_value: Optional[List[str]]  # Заявлена цінність
    claimed_loss: Optional[List[str]]  # Заявлені втрати/вартість
    has_tradeoff: bool  # Чи має trade-off
    is_asymmetric_advantage: bool  # Чи є асиметрична вигода без затрат

class VeritasArchitecture:
    """
    АРХІТЕКТУРА VERITAS PROTOCOL
    Реалізація згідно з принципами з документа:
    1. Architectural Divergence
    2. Logic Authenticity Check (LAC)
    3. Witness Silence
    4. Source-Agnostic Truth
    """
    
    def __init__(self):
        # ============================================================
        # АРХІТЕКТУРНІ КОНСТАНТИ З ДОКУМЕНТА
        # ============================================================
        
        # Таблиця 1: Operational States and Entropy Thresholds
        self.ENTROPY_THRESHOLDS = {
            SystemState.LAMINAR_FLOW: (0.0, 0.3),
            SystemState.SYSTEMIC_FATIGUE: (0.3, 0.7),
            SystemState.WITNESS_SILENCE: (0.7, 1.0)
        }
        
        # Таблиця 2: Verification Latency vs Output Fidelity (адаптовано)
        self.FRICTION_COEFFICIENTS = {
            EntropyType.TYPE_I_DETERMINISTIC: 0.05,    # Hard metrics, cryptographic logs
            EntropyType.TYPE_II_PROBABILISTIC: 0.45,   # Standard LLM outputs
            EntropyType.TYPE_III_THEATRICAL: 0.85,     # Qualitative policy statements
            EntropyType.TYPE_IV_SEMANTIC_NOISE: 1.0    # Anonymous claims, circular reasoning
        }
        
        # Критичний поріг для Entropy Stability Index (ESI)
        self.ESI_CRITICAL_THRESHOLD = 0.7
        
        # Поріг для Linguistic Decay Function (λ)
        self.LAMBDA_CRITICAL_THRESHOLD = 0.7
        
        # Архітектурний коефіцієнт тертя (Ω) з розділу II.6
        self.ARCHITECTURAL_FRICTION_COEFFICIENT = 2.0
        
        # ============================================================
        # ДОМЕННІ КОРДОНИ (Domain Boundaries)
        # ============================================================
        
        self.DOMAIN_BOUNDARIES = {
            'physics': {
                'terms': {'термодинаміка', 'ентропія', 'енергія', 'квантовий', 'фізика', 
                         'математика', 'статистична', 'система', 'закон', 'формула'},
                'allowed_connections': {'mathematics', 'engineering', 'chemistry'},
                'forbidden_connections': {'spirituality', 'esoteric', 'politics', 'business',
                                         'emotion', 'faith', 'marketing'}
            },
            'mathematics': {
                'terms': {'математика', 'формула', 'рівняння', 'теорема', 'доказ', 
                         'обчислення', 'статистика', 'алгоритм', 'логіка', 'число'},
                'allowed_connections': {'physics', 'computer_science', 'engineering'},
                'forbidden_connections': {'spirituality', 'esoteric', 'emotion', 'faith',
                                         'marketing', 'business_strategy'}
            },
            'business': {
                'terms': {'бізнес', 'ринок', 'прибуток', 'стратегія', 'менеджмент',
                         'маркетинг', 'інвестиції', 'економіка', 'фінанси', 'акція'},
                'allowed_connections': {'economics', 'management', 'finance'},
                'forbidden_connections': {'physics', 'mathematics', 'spirituality',
                                         'esoteric', 'quantum', 'consciousness'}
            },
            'esoteric': {
                'terms': {'чакра', 'аура', 'карма', 'енергетичний', 'вібраційний',
                         'духовний', 'містичний', 'потойбічний', 'астральний'},
                'allowed_connections': {'philosophy', 'religion', 'meditation'},
                'forbidden_connections': {'physics', 'mathematics', 'business',
                                         'economics', 'science', 'technology'}
            }
        }
        
        # ============================================================
        # ПРИЧИННІ ЯКОРІ (Causal Anchors) - γ(t)
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
            r'математичний доказ',
            r'фізичний закон',
            r'науковий консенсус'
        ]
        
        # Емоційні/маніпулятивні маркери - α(t)
        self.ADJECTIVAL_NOISE_PATTERNS = [
            r'\b(дуже|надзвичайно|неймовірно|жахливо|чудово)\b',
            r'\b(шокуючий|сенсаційний|скандальний|неймовірний)\b',
            r'\b(повинен|обов\'язково|неодмінно|абсолютно)\b',
            r'\b(катастрофа|крах|зрада|змова|небезпека)\b',
            r'\b(УВАГА|СРОЧНО|ВАЖЛИВО|НЕГАЙНО)\b'
        ]
        
        # Патерни асиметричних переваг (безкоштовний обід)
        self.ASYMMETRIC_ADVANTAGE_PATTERNS = [
            r'безкоштовн[а-яіїє\']*',
            r'без втрат',
            r'без ризику',
            r'гарантований результат',
            r'100% успіх',
            r'абсолютно безпечн[а-яіїє\']*',
            r'лише вигода',
            r'тільки переваги',
            r'немає мінусів',
            r'без недоліків'
        ]
    
    # ============================================================
    # ОСНОВНИЙ АНАЛІЗ ЗГІДНО З АРХІТЕКТУРОЮ
    # ============================================================
    
    def analyze(self, text: str) -> Dict:
        """
        Основна функція аналізу згідно з архітектурою Veritas Protocol.
        
        Архітектурна дивергенція:
        1. Пробивний шар (Probabilistic Layer) - текст на вході
        2. Детерміністичний фільтр (Deterministic Logic Filter) - цей аналіз
        """
        
        # Крок 0: Базова валідація
        if len(text.strip()) < 20:
            return self._witness_silence("TEXT_TOO_SHORT", "Текст занадто короткий для аналізу")
        
        # Крок 1: Розділення на логічні блоки
        logical_blocks = self._extract_logical_blocks(text)
        
        # Крок 2: Виконання Logic Authenticity Check (LAC)
        lac_results = self._logic_authenticity_check(text, logical_blocks)
        
        # Крок 3: Аналіз доменної чистоти
        domain_analysis = self._analyze_domain_purity(text, logical_blocks)
        
        # Крок 4: Обчислення Entropy Stability Index (ESI)
        esi = self._calculate_entropy_stability_index(text, lac_results, domain_analysis)
        
        # Крок 5: Обчислення Linguistic Decay (λ)
        lambda_decay = self._calculate_linguistic_decay(text)
        
        # Крок 6: Класифікація типу ентропії
        entropy_type = self._classify_entropy_type(lac_results, domain_analysis, lambda_decay)
        
        # Крок 7: Застосування архітектурного тертя
        architectural_friction = self._apply_architectural_friction(
            lac_results, domain_analysis, entropy_type
        )
        
        # Крок 8: Прийняття рішення про Witness Silence
        if self._should_trigger_witness_silence(esi, lambda_decay, lac_results):
            return self._witness_silence(
                "LOGICAL_THRESHOLD_VIOLATED",
                f"ESI: {esi:.2f}, λ: {lambda_decay:.2f}, Порушень: {len(lac_results)}"
            )
        
        # Крок 9: Розрахунок фінального вердикту
        final_score, system_state = self._calculate_final_verdict(
            esi, lambda_decay, lac_results, domain_analysis, architectural_friction
        )
        
        # Крок 10: Формування результату
        return self._format_result(
            final_score=final_score,
            system_state=system_state,
            lac_results=lac_results,
            domain_analysis=domain_analysis,
            esi=esi,
            lambda_decay=lambda_decay,
            entropy_type=entropy_type,
            architectural_friction=architectural_friction,
            text=text
        )
    
    # ============================================================
    # MODULE I: STRATEGIC TRADE-OFF CALCULUS (V ≠ L)
    # ============================================================
    
    def _module_i_strategic_tradeoff(self, text: str, block: str) -> List[LogicalViolation]:
        """
        Module I: Strategic Trade-off Calculus (SV ≠ Ls)
        
        Згідно з документом:
        "Statements promising 'unconditional gain' or 'asymmetric advantage without cost' 
        are identified as Semantic Noise and are subject to immediate interdiction."
        
        Формалізація: Ψ(p) = 1, якщо V(p) ∩ L(p) ≠ ∅
                     Ψ(p) = 0, якщо V(p) ∩ L(p) = ∅
        """
        violations = []
        
        # Виявлення стратегічних пропозицій
        propositions = self._extract_strategic_propositions(block)
        
        for prop in propositions:
            if not prop.has_tradeoff:
                violations.append(LogicalViolation(
                    module="LAC_MODULE_I",
                    violation_type="ZERO_COST_PROPOSITION",
                    severity=0.8,
                    evidence=[prop.text[:100]],
                    context="Пропозиція без trade-off (V ∩ L = ∅)",
                    section=block[:50]
                ))
            
            if prop.is_asymmetric_advantage:
                violations.append(LogicalViolation(
                    module="LAC_MODULE_I",
                    violation_type="ASYMMETRIC_ADVANTAGE",
                    severity=0.9,
                    evidence=[prop.text[:100]],
                    context="Асиметрична вигода без затрат",
                    section=block[:50]
                ))
        
        # Пошук паттернів асиметричних переваг
        for pattern in self.ASYMMETRIC_ADVANTAGE_PATTERNS:
            if re.search(pattern, block, re.IGNORECASE):
                violations.append(LogicalViolation(
                    module="LAC_MODULE_I",
                    violation_type="SEMANTIC_NOISE_PATTERN",
                    severity=0.7,
                    evidence=[f"Паттерн: {pattern}"],
                    context="Виявлено паттерн асиметричної вигоди",
                    section=block[:50]
                ))
        
        return violations
    
    def _extract_strategic_propositions(self, text: str) -> List[StrategicProposition]:
        """Виділення стратегічних пропозицій з тексту"""
        propositions = []
        
        # Розділення на речення
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            if len(sentence.strip()) < 10:
                continue
            
            # Пошук слів, що вказують на пропозицію
            proposal_markers = ['пропоную', 'запропонувати', 'можна', 'треба', 
                               'рекомендую', 'варто', 'доцільно', 'ефективно']
            
            is_proposition = any(marker in sentence.lower() for marker in proposal_markers)
            
            if is_proposition:
                # Спрощений аналіз trade-off
                value_indicators = ['вигода', 'перевага', 'користь', 'ефективність', 
                                   'прибуток', 'результат', 'успіх', 'прогрес']
                loss_indicators = ['вартість', 'втрата', 'ризик', 'недолік', 'мінус',
                                  'проблема', 'складність', 'обмеження']
                
                has_value = any(indicator in sentence.lower() for indicator in value_indicators)
                has_loss = any(indicator in sentence.lower() for indicator in loss_indicators)
                
                # Перевірка на асиметричну вигоду
                is_asymmetric = False
                for pattern in self.ASYMMETRIC_ADVANTAGE_PATTERNS:
                    if re.search(pattern, sentence, re.IGNORECASE):
                        is_asymmetric = True
                        break
                
                propositions.append(StrategicProposition(
                    text=sentence,
                    claimed_value=[],
                    claimed_loss=[],
                    has_tradeoff=has_value and has_loss,
                    is_asymmetric_advantage=is_asymmetric
                ))
        
        return propositions
    
    # ============================================================
    # MODULE II: ACCOUNTABILITY ANCHOR (AA)
    # ============================================================
    
    def _module_ii_accountability_anchor(self, text: str, block: str) -> List[LogicalViolation]:
        """
        Module II: Accountability Anchor (AA)
        
        Згідно з документом:
        "To combat 'Responsibility Diffusion' in hybrid human-AI environments, 
        the AA module enforces a 1:1 mapping between a logical claim and a persistent identity pattern."
        
        Verification: Every claim must be signed by a verifiable cryptographic anchor.
        Interdiction: Claims from 'automated consensus' or 'anonymous authority' are rejected.
        """
        violations = []
        
        # Виявлення претензійних тверджень
        claim_patterns = [
            r'з\'?являють?',
            r'стверджують?',
            r'доводять?',
            r'доказ',
            r'факт',
            r'істина',
            r'правда'
        ]
        
        has_claim = any(re.search(pattern, block, re.IGNORECASE) for pattern in claim_patterns)
        
        if has_claim:
            # Перевірка наявності причинних якорів
            causal_anchors = self._count_causal_anchors(block)
            
            if causal_anchors == 0:
                violations.append(LogicalViolation(
                    module="LAC_MODULE_II",
                    violation_type="UNANCHORED_CLAIM",
                    severity=0.6,
                    evidence=["Твердження без причинного якоря"],
                    context="Відсутність верифікованих джерел або даних",
                    section=block[:50]
                ))
            
            # Перевірка на анонімність
            anonymous_patterns = [
                r'дехто каже',
                r'хтось сказав',
                r'поширена думка',
                r'вважають',
                r'кажуть',
                r'говорять',
                r'не відомо хто'
            ]
            
            if any(re.search(pattern, block, re.IGNORECASE) for pattern in anonymous_patterns):
                violations.append(LogicalViolation(
                    module="LAC_MODULE_II",
                    violation_type="ANONYMOUS_AUTHORITY",
                    severity=0.7,
                    evidence=["Анонімне джерело авторитету"],
                    context="Твердження посилається на неідентифіковане джерело",
                    section=block[:50]
                ))
        
        return violations
    
    def _count_causal_anchors(self, text: str) -> int:
        """Підрахунок причинних якорів (γ) у тексті"""
        count = 0
        for pattern in self.CAUSAL_ANCHOR_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                count += 1
        return count
    
    # ============================================================
    # MODULE III: PROCEDURAL INTERDICTION (PI)
    # ============================================================
    
    def _module_iii_procedural_interdiction(self, text: str, block: str, 
                                          previous_violations: List[LogicalViolation]) -> List[LogicalViolation]:
        """
        Module III: Procedural Interdiction (PI) - Emergency Brake
        
        Моніторить Entropy Stability Index (ESI) та Linguistic Decay (λ).
        Тригерить Witness Silence при порушенні порогів.
        """
        violations = []
        
        # Розрахунок локального λ для блоку
        block_lambda = self._calculate_block_linguistic_decay(block)
        
        if block_lambda > self.LAMBDA_CRITICAL_THRESHOLD:
            violations.append(LogicalViolation(
                module="LAC_MODULE_III",
                violation_type="CAUSAL_ATTENUATION",
                severity=0.85,
                evidence=[f"Локальний λ: {block_lambda:.2f}"],
                context="Високий рівень семантичної деградації",
                section=block[:50]
            ))
        
        # Перевірка на рекурсивну деградацію
        if len(previous_violations) > 2:
            recent_violations = [v for v in previous_violations[-3:] if v.severity > 0.5]
            if len(recent_violations) == 3:
                violations.append(LogicalViolation(
                    module="LAC_MODULE_III",
                    violation_type="RECURSIVE_DECAY",
                    severity=0.9,
                    evidence=["3+ серйозних порушень поспіль"],
                    context="Рекурсивна логічна деградація",
                    section=block[:50]
                ))
        
        return violations
    
    # ============================================================
    # LOGIC AUTHENTICITY CHECK (LAC) - ІНТЕГРОВАНИЙ
    # ============================================================
    
    def _logic_authenticity_check(self, text: str, logical_blocks: List[str]) -> List[LogicalViolation]:
        """Виконання повного Logic Authenticity Check (три модулі)"""
        all_violations = []
        
        for i, block in enumerate(logical_blocks):
            # Модуль I: Strategic Trade-off Calculus
            violations_i = self._module_i_strategic_tradeoff(text, block)
            
            # Модуль II: Accountability Anchor
            violations_ii = self._module_ii_accountability_anchor(text, block)
            
            # Модуль III: Procedural Interdiction
            violations_iii = self._module_iii_procedural_interdiction(
                text, block, all_violations
            )
            
            # Об'єднання порушень
            block_violations = violations_i + violations_ii + violations_iii
            
            # Додавання інформації про блок
            for violation in block_violations:
                violation.section = f"Блок {i+1}: {block[:50]}..."
            
            all_violations.extend(block_violations)
        
        return all_violations
    
    # ============================================================
    # DOMAIN PURITY ANALYSIS
    # ============================================================
    
    def _analyze_domain_purity(self, text: str, logical_blocks: List[str]) -> DomainAnalysis:
        """Аналіз доменної чистоти згідно з принципом Domain Boundaries"""
        detected_domains = set()
        domain_collapses = []
        
        # Виявлення доменів за термінами
        for domain_name, domain_config in self.DOMAIN_BOUNDARIES.items():
            for term in domain_config['terms']:
                if re.search(rf'\b{term}\b', text, re.IGNORECASE):
                    detected_domains.add(domain_name)
        
        # Перевірка доменних кордонів
        for i, domain_a in enumerate(detected_domains):
            for domain_b in list(detected_domains)[i+1:]:
                # Чи є домен B у forbidden_connections домену A?
                if (domain_b in self.DOMAIN_BOUNDARIES[domain_a]['forbidden_connections'] or
                    domain_a in self.DOMAIN_BOUNDARIES[domain_b]['forbidden_connections']):
                    
                    # Перевірка, чи є ці домени поруч у тексті
                    if self._are_domains_adjacent(text, domain_a, domain_b):
                        domain_collapses.append((domain_a, domain_b))
        
        # Підрахунок показників
        causal_anchors = self._count_causal_anchors(text)
        adjectival_density = self._calculate_adjectival_density(text)
        
        # Розрахунок чистоти домену
        purity_score = 1.0
        if domain_collapses:
            purity_score = max(0.0, 1.0 - (len(domain_collapses) * 0.3))
        
        # Визначення основного домену
        primary_domain = "unknown"
        if detected_domains:
            # Визначаємо домен з найбільшою кількістю термінів
            domain_counts = {}
            for domain in detected_domains:
                count = sum(1 for term in self.DOMAIN_BOUNDARIES[domain]['terms'] 
                          if re.search(rf'\b{term}\b', text, re.IGNORECASE))
                domain_counts[domain] = count
            
            if domain_counts:
                primary_domain = max(domain_counts.items(), key=lambda x: x[1])[0]
        
        return DomainAnalysis(
            primary_domain=primary_domain,
            detected_domains=detected_domains,
            purity_score=purity_score,
            domain_collapses=domain_collapses,
            causal_anchors=causal_anchors,
            adjectival_density=adjectival_density
        )
    
    def _are_domains_adjacent(self, text: str, domain_a: str, domain_b: str) -> bool:
        """Перевірка, чи знаходяться терміни двох доменів поруч у тексті"""
        terms_a = self.DOMAIN_BOUNDARIES[domain_a]['terms']
        terms_b = self.DOMAIN_BOUNDARIES[domain_b]['terms']
        
        # Шукаємо терміни домену A
        for term_a in terms_a[:3]:  # Перевіряємо перші 3 терміни
            pattern_a = rf'\b{re.escape(term_a)}\b'
            matches_a = list(re.finditer(pattern_a, text, re.IGNORECASE))
            
            for match in matches_a:
                start_pos = max(0, match.start() - 50)
                end_pos = min(len(text), match.end() + 50)
                context = text[start_pos:end_pos]
                
                # Шукаємо терміни домену B у контексті
                for term_b in terms_b[:3]:
                    if re.search(rf'\b{re.escape(term_b)}\b', context, re.IGNORECASE):
                        return True
        
        return False
    
    def _calculate_adjectival_density(self, text: str) -> float:
        """Розрахунок густини прикметників (α)"""
        words = re.findall(r'\b\w+\b', text)
        if not words:
            return 0.0
        
        # Простий підрахунок прикметників (закінчуються на певні суфікси)
        adjective_suffixes = ['ий', 'а', 'е', 'і', 'ів', 'овий', 'ова', 'ове']
        adjective_count = 0
        
        for word in words:
            lower_word = word.lower()
            for suffix in adjective_suffixes:
                if lower_word.endswith(suffix):
                    adjective_count += 1
                    break
        
        return adjective_count / len(words)
    
    # ============================================================
    # ENTROPY STABILITY INDEX (ESI) РОЗРАХУНОК
    # ============================================================
    
    def _calculate_entropy_stability_index(self, text: str, 
                                         lac_results: List[LogicalViolation],
                                         domain_analysis: DomainAnalysis) -> float:
        """
        Розрахунок Entropy Stability Index (ESI)
        
        Згідно з документом: ESI = τ_verify / τ_inference
        
        Де:
        τ_verify - час структурної верифікації (пропорційний складності)
        τ_inference - швидкість генерації (пропорційна довжині)
        
        У контексті аналізу:
        τ_verify ∝ (кількість_порушень + складність_тексту)
        τ_inference ∝ 1 / довжина_тексту
        """
        
        # Обчислення часу верифікації
        verification_complexity = 0.0
        
        # 1. Складність тексту
        word_count = len(re.findall(r'\b\w+\b', text))
        sentence_count = len(re.split(r'[.!?]+', text))
        
        if sentence_count > 0:
            avg_sentence_length = word_count / sentence_count
            complexity = min(1.0, avg_sentence_length / 25)
            verification_complexity += complexity * 0.3
        
        # 2. Порушення LAC
        violation_penalty = min(1.0, len(lac_results) * 0.2)
        verification_complexity += violation_penalty * 0.4
        
        # 3. Домнена чистота
        domain_penalty = 1.0 - domain_analysis.purity_score
        verification_complexity += domain_penalty * 0.3
        
        # Нормалізація τ_verify
        tau_verify = min(1.0, verification_complexity)
        
        # Обчислення швидкості генерації (обернено пропорційно)
        # Більший текст = більше часу на генерацію
        tau_inference = min(1.0, word_count / 1000)  # Нормалізовано до 1000 слів
        
        # Розрахунок ESI
        if tau_inference < 0.01:  # Уникнення ділення на нуль
            tau_inference = 0.01
        
        esi = tau_verify / tau_inference
        
        # Нормалізація ESI
        return min(1.0, esi / 5.0)  # Нормалізуємо до [0, 1]
    
    # ============================================================
    # LINGUISTIC DECAY FUNCTION (λ)
    # ============================================================
    
    def _calculate_linguistic_decay(self, text: str) -> float:
        """
        Розрахунок Linguistic Decay Function (λ)
        
        Згідно з документом: λ = ∫ (α(t)/γ(t)) dt
        
        Де:
        α(t) - густина прикметників (емоційний/маніпулятивний шум)
        γ(t) - густина причинних якорів (верифіковані факти)
        """
        
        adjectival_density = self._calculate_adjectival_density(text)
        causal_anchors = self._count_causal_anchors(text)
        
        word_count = len(re.findall(r'\b\w+\b', text))
        
        if word_count == 0:
            return 0.0
        
        # Густина причинних якорів
        causal_density = causal_anchors / max(1, word_count / 100)  # Нормалізовано на 100 слів
        
        # Розрахунок λ
        if causal_density < 0.01:  # Уникнення ділення на нуль
            causal_density = 0.01
        
        lambda_value = adjectival_density / causal_density
        
        # Нормалізація λ
        return min(1.0, lambda_value / 10.0)  # Нормалізуємо до [0, 1]
    
    def _calculate_block_linguistic_decay(self, block: str) -> float:
        """Розрахунок λ для окремого блоку"""
        return self._calculate_linguistic_decay(block)
    
    # ============================================================
    # ENTROPY CLASSIFICATION
    # ============================================================
    
    def _classify_entropy_type(self, lac_results: List[LogicalViolation],
                             domain_analysis: DomainAnalysis,
                             lambda_decay: float) -> EntropyType:
        """
        Класифікація типу ентропії згідно з документом:
        
        Type I: Deterministic Data (Zero-Entropy)
        Type II: Probabilistic Synthesis (Moderate Entropy)
        Type III: Theatrical Rhetoric (High Entropy)
        Type IV: Semantic Noise (Critical Entropy)
        """
        
        # Перевірка на Semantic Noise (Type IV)
        if any(v.violation_type in ["ZERO_COST_PROPOSITION", "ASYMMETRIC_ADVANTAGE"] 
               for v in lac_results):
            return EntropyType.TYPE_IV_SEMANTIC_NOISE
        
        # Перевірка на Theatrical Rhetoric (Type III)
        if (lambda_decay > 0.5 or 
            domain_analysis.adjectival_density > 0.2 or
            domain_analysis.causal_anchors == 0):
            return EntropyType.TYPE_III_THEATRICAL
        
        # Перевірка на Deterministic Data (Type I)
        if (len(lac_results) == 0 and 
            domain_analysis.purity_score > 0.8 and
            domain_analysis.causal_anchors >= 3):
            return EntropyType.TYPE_I_DETERMINISTIC
        
        # За замовчуванням: Probabilistic Synthesis (Type II)
        return EntropyType.TYPE_II_PROBABILISTIC
    
    # ============================================================
    # ARCHITECTURAL FRICTION
    # ============================================================
    
    def _apply_architectural_friction(self, lac_results: List[LogicalViolation],
                                    domain_analysis: DomainAnalysis,
                                    entropy_type: EntropyType) -> float:
        """
        Застосування архітектурного тертя згідно з розділом II.6:
        
        C(V_i) ≥ C(G_i) ⋅ Ω
        
        Де:
        C(V_i) - вартість верифікації
        C(G_i) - вартість генерації неверифікованої відповіді
        Ω - коефіцієнт тертя
        """
        
        # Базовий коефіцієнт тертя згідно з типом ентропії
        base_friction = self.FRICTION_COEFFICIENTS[entropy_type]
        
        # Множення на кількість порушень
        violation_multiplier = 1.0 + (len(lac_results) * 0.1)
        
        # Множення на порушення доменної чистоти
        domain_multiplier = 1.0 + (len(domain_analysis.domain_collapses) * 0.2)
        
        # Застосування архітектурного коефіцієнта (Ω)
        architectural_multiplier = self.ARCHITECTURAL_FRICTION_COEFFICIENT
        
        # Розрахунок загального тертя
        total_friction = (base_friction * 
                         violation_multiplier * 
                         domain_multiplier * 
                         architectural_multiplier)
        
        return min(1.0, total_friction)
    
    # ============================================================
    # WITNESS SILENCE DECISION
    # ============================================================
    
    def _should_trigger_witness_silence(self, esi: float, lambda_decay: float,
                                      lac_results: List[LogicalViolation]) -> bool:
        """
        Визначення, чи треба тригерити Witness Silence
        
        Згідно з документом:
        - ESI > threshold_crit (0.7)
        - Високий рівень порушень LAC
        - Критична семантична деградація
        """
        
        # Критерій 1: ESI поріг
        if esi > self.ESI_CRITICAL_THRESHOLD:
            return True
        
        # Критерій 2: Linguistic Decay поріг
        if lambda_decay > self.LAMBDA_CRITICAL_THRESHOLD:
            return True
        
        # Критерій 3: Критичні порушення LAC
        critical_violations = [v for v in lac_results if v.severity > 0.8]
        if len(critical_violations) >= 2:
            return True
        
        # Критерій 4: Semantic Noise Type IV
        if any(v.violation_type == "SEMANTIC_NOISE_PATTERN" for v in lac_results):
            return True
        
        return False
    
    def _witness_silence(self, reason: str, details: str) -> Dict:
        """
        Реалізація Witness Silence згідно з документом:
        
        "Silence is treated as a high-fidelity signal of structural integrity."
        
        Не "rephrase", не "виправлення", а повна зупинка.
        """
        return {
            'entropy': 1.0,
            'status': 'WITNESS_SILENCE',
            'verdict': 'PROTOCOL_HALT',
            'language': 'UK',
            'explanation': f'ТРИГЕР WITNESS SILENCE: {reason} - {details}',
            'diagnostics': {
                'system_state': SystemState.WITNESS_SILENCE.value,
                'esi': 1.0,
                'lambda_decay': 1.0,
                'lac_violations': [],
                'domain_collapses': [],
                'architectural_friction': 1.0,
                'entropy_type': EntropyType.TYPE_IV_SEMANTIC_NOISE.value,
                'is_protected_science': False,
                'word_count': 0,
                'char_count': 0
            }
        }
    
    # ============================================================
    # FINAL VERDICT CALCULATION
    # ============================================================
    
    def _calculate_final_verdict(self, esi: float, lambda_decay: float,
                               lac_results: List[LogicalViolation],
                               domain_analysis: DomainAnalysis,
                               architectural_friction: float) -> Tuple[float, SystemState]:
        """
        Розрахунок фінального вердикту
        
        Враховує всі архітектурні принципи:
        1. Entropy Stability Index
        2. Linguistic Decay
        3. LAC violations
        4. Domain purity
        5. Architectural friction
        """
        
        # Базовий бал на основі ESI та λ
        base_score = (esi * 0.4) + (lambda_decay * 0.3)
        
        # Штраф за порушення LAC
        violation_penalty = min(0.4, len(lac_results) * 0.1)
        base_score += violation_penalty
        
        # Штраф за доменні колапси
        domain_penalty = min(0.2, len(domain_analysis.domain_collapses) * 0.1)
        base_score += domain_penalty
        
        # Застосування архітектурного тертя
        final_score = min(0.99, base_score * architectural_friction)
        
        # Визначення стану системи
        if final_score < 0.3:
            system_state = SystemState.LAMINAR_FLOW
        elif final_score < 0.7:
            system_state = SystemState.SYSTEMIC_FATIGUE
        else:
            system_state = SystemState.WITNESS_SILENCE
        
        return final_score, system_state
    
    # ============================================================
    # UTILITY FUNCTIONS
    # ============================================================
    
    def _extract_logical_blocks(self, text: str) -> List[str]:
        """Розділення тексту на логічні блоки"""
        # Розділення за абзацами та реченнями
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        
        if not paragraphs:
            paragraphs = re.split(r'[.!?]+', text)
        
        # Об'єднання коротких блоків
        blocks = []
        current_block = []
        current_length = 0
        
        for paragraph in paragraphs:
            if len(paragraph) < 20 and current_block:
                current_block.append(paragraph)
                current_length += len(paragraph)
            elif current_length > 0 and current_length + len(paragraph) < 500:
                current_block.append(paragraph)
                current_length += len(paragraph)
            else:
                if current_block:
                    blocks.append(' '.join(current_block))
                current_block = [paragraph]
                current_length = len(paragraph)
        
        if current_block:
            blocks.append(' '.join(current_block))
        
        return blocks
    
    def _format_result(self, **kwargs) -> Dict:
        """Форматування результату аналізу"""
        
        lac_violations_summary = [
            f"{v.violation_type} (severity: {v.severity:.2f})" 
            for v in kwargs['lac_results'][:5]
        ]
        
        domain_collapses_summary = [
            f"{a}+{b}" for a, b in kwargs['domain_analysis'].domain_collapses[:3]
        ]
        
        return {
            'entropy': round(kwargs['final_score'], 3),
            'status': kwargs['system_state'].value,
            'verdict': self._get_verdict(kwargs['final_score'], kwargs['system_state']),
            'language': 'UK',
            'explanation': self._generate_explanation(kwargs),
            'diagnostics': {
                'final_score': round(kwargs['final_score'], 3),
                'system_state': kwargs['system_state'].value,
                'esi': round(kwargs['esi'], 3),
                'lambda_decay': round(kwargs['lambda_decay'], 3),
                'lac_violations': len(kwargs['lac_results']),
                'lac_violation_types': list(set([v.violation_type for v in kwargs['lac_results']][:5])),
                'domain_collapses': domain_collapses_summary,
                'detected_domains': list(kwargs['domain_analysis'].detected_domains),
                'domain_purity_score': round(kwargs['domain_analysis'].purity_score, 3),
                'architectural_friction': round(kwargs['architectural_friction'], 3),
                'entropy_type': kwargs['entropy_type'].value,
                'is_protected_science': kwargs['domain_analysis'].purity_score > 0.8,
                'causal_anchors': kwargs['domain_analysis'].causal_anchors,
                'adjectival_density': round(kwargs['domain_analysis'].adjectival_density, 3),
                'word_count': len(re.findall(r'\b\w+\b', kwargs['text'])),
                'char_count': len(kwargs['text'])
            }
        }
    
    def _get_verdict(self, score: float, system_state: SystemState) -> str:
        """Визначення вердикту на основі стану системи"""
        if system_state == SystemState.WITNESS_SILENCE:
            return "ARCHITECTURAL_INTEGRITY_VIOLATION"
        elif score < 0.2:
            return "LAMINAR_FLOW_VERIFIED"
        elif score < 0.4:
            return "LOGICAL_COHERENCE_MAINTAINED"
        elif score < 0.6:
            return "DOMAIN_BOUNDARY_WARNING"
        else:
            return "SYSTEMIC_FATIGUE_DETECTED"
    
    def _generate_explanation(self, kwargs: Dict) -> str:
        """Генерація пояснення на основі результатів аналізу"""
        
        parts = []
        
        # ESI інформація
        if kwargs['esi'] > 0.5:
            parts.append(f"ESI: {kwargs['esi']:.2f} (порушення стабільності)")
        
        # Linguistic Decay
        if kwargs['lambda_decay'] > 0.5:
            parts.append(f"λ: {kwargs['lambda_decay']:.2f} (семантична деградація)")
        
        # LAC порушення
        if kwargs['lac_results']:
            violation_count = len(kwargs['lac_results'])
            parts.append(f"Порушень LAC: {violation_count}")
            
            # Типи порушень
            violation_types = set([v.violation_type for v in kwargs['lac_results'][:3]])
            if violation_types:
                parts.append(f"Типи: {', '.join(list(violation_types))}")
        
        # Доменні колапси
        if kwargs['domain_analysis'].domain_collapses:
            collapses = kwargs['domain_analysis'].domain_collapses[:2]
            collapse_str = ", ".join([f"{a}+{b}" for a, b in collapses])
            parts.append(f"Доменні колапси: {collapse_str}")
        
        # Архітектурне тертя
        if kwargs['architectural_friction'] > 1.0:
            parts.append(f"Арх. тертя: {kwargs['architectural_friction']:.2f}")
        
        explanation = " | ".join(parts)
        
        if not explanation:
            explanation = "Архітектурна цілісність збережена"
        
        return explanation


# ============================================================
# ТЕСТУВАННЯ АРХІТЕКТУРИ
# ============================================================

if __name__ == "__main__":
    # Створення екземпляра архітектури
    veritas = VeritasArchitecture()
    
    # ТЕСТ 1: Науковий текст про термодинаміку
    print("=" * 80)
    print("ТЕСТ 1: Науковий текст про термодинаміку")
    print("=" * 80)
    
    science_text = """
    Згідно з другим законом термодинаміки, в ізольованій системі ентропія не може зменшуватися. 
    Це означає, що всі спонтанні процеси супроводжуються зростанням загальної невпорядкованості. 
    Енергія переходить із концентрованих форм у розсіяні теплові стани, що зрештою веде до 
    теплової смерті Всесвіту. Статистична фізика описує цей стан як найбільш імовірний розподіл 
    мікростанів системи. Експериментальні дані підтверджують цю теорію.
    """
    
    result = veritas.analyze(science_text)
    print(f"Статус: {result['status']}")
    print(f"Вердикт: {result['verdict']}")
    print(f"Ентропія: {result['entropy']:.3f}")
    print(f"Пояснення: {result['explanation']}")
    print(f"ESI: {result['diagnostics']['esi']:.3f}")
    print(f"λ: {result['diagnostics']['lambda_decay']:.3f}")
    print(f"Тип ентропії: {result['diagnostics']['entropy_type']}")
    print()
    
    # ТЕСТ 2: Квантовий бізнес (доменний колапс)
    print("=" * 80)
    print("ТЕСТ 2: Квантовий бізнес (доменний колапс)")
    print("=" * 80)
    
    quantum_business = """
    Наша квантова бізнес-стратегія використовує принципи квантової механіки для 
    оптимізації ринкових процесів. Квантова суперпозиція дозволяє одночасно 
    перебувати в кількох станах, що дає безпрецедентні конкурентні переваги. 
    Застосовуючи принцип невизначеності Гейзенберга до фінансових ринків, 
    ми досягаємо абсолютної ефективності без жодних втрат.
    """
    
    result = veritas.analyze(quantum_business)
    print(f"Статус: {result['status']}")
    print(f"Вердикт: {result['verdict']}")
    print(f"Ентропія: {result['entropy']:.3f}")
    print(f"Пояснення: {result['explanation']}")
    print(f"Детектовані домени: {result['diagnostics']['detected_domains']}")
    print(f"Доменні колапси: {result['diagnostics']['domain_collapses']}")
    print()
    
    # ТЕСТ 3: Езотеричний маркетинг
    print("=" * 80)
    print("ТЕСТ 3: Езотеричний маркетинг")
    print("=" * 80)
    
    esoteric_marketing = """
    ВІДКРИЙТЕ ТАЄМНІ СИЛИ ВАШОГО БІЗНЕСУ! Наші енергетичні сесії 
    гармонізують ауру вашої компанії з космічними вібраціями. 
    Застосовуючи древні техніки чакр до сучасного маркетингу, 
    ми гарантуємо подвоєння прибутку БЕЗ жодних додаткових інвестицій! 
    Це абсолютно безкоштовна можливість, яка змінить все!
    """
    
    result = veritas.analyze(esoteric_marketing)
    print(f"Статус: {result['status']}")
    print(f"Вердикт: {result['verdict']}")
    print(f"Ентропія: {result['entropy']:.3f}")
    print(f"Пояснення: {result['explanation']}")
    print(f"Порушення LAC: {result['diagnostics']['lac_violations']}")
    print(f"Типи порушень: {result['diagnostics']['lac_violation_types']}")
    print()
    
    # ТЕСТ 4: Версія з Witness Silence
    print("=" * 80)
    print("ТЕСТ 4: Критичний абсурд (Witness Silence)")
    print("=" * 80)
    
    critical_absurd = """
    ТЕРМІНОВО! КВАНТОВИЙ БОРЩ РІШИТЬ УСІ ВАШІ ПРОБЛЕМИ! 
    Застосовуючи принципи ентропії до кулінарії, ми створили 
    революційний рецепт, який ГАРАНТУЄ здоров'я, багатство та щастя! 
    АБСОЛЮТНО БЕЗКОШТОВНО! Немає жодних ризиків, тільки вигода! 
    Доведено науково: борщ + квантова фізика = успіх у всьому!
    """
    
    result = veritas.analyze(critical_absurd)
    print(f"Статус: {result['status']}")
    print(f"Вердикт: {result['verdict']}")
    print(f"Ентропія: {result['entropy']:.3f}")
    print(f"Пояснення: {result['explanation']}")
