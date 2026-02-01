"""
VERITAS PROTOCOL - АРХІТЕКТУРНА ІМПЛЕМЕНТАЦІЯ
Версія: 1.0.2 (Повністю українізована)
"""

import re
import math
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional, Set
from enum import Enum

class EntropyType(Enum):
    """Таксономія інформаційної ентропії"""
    TYPE_I_DETERMINISTIC = "Детерміновані дані (Нульова ентропія)"
    TYPE_II_PROBABILISTIC = "Ймовірнісний синтез (Помірна ентропія)"
    TYPE_III_THEATRICAL = "Театральна риторика (Висока ентропія)"
    TYPE_IV_SEMANTIC_NOISE = "Семантичний шум (Критична ентропія)"

class SystemState(Enum):
    """Операційні стани системи"""
    LAMINAR_FLOW = "Ламінарний потік"
    SYSTEMIC_FATIGUE = "Системна втома"
    WITNESS_SILENCE = "Свідок мовчить"

@dataclass
class LogicalViolation:
    """Логічне порушення високого рівня"""
    module: str
    violation_type: str
    severity: float
    evidence: List[str]
    context: str
    section: str

@dataclass
class DomainAnalysis:
    """Аналіз доменної чистоти"""
    primary_domain: str
    detected_domains: Set[str]
    purity_score: float
    domain_collapses: List[Tuple[str, str]]
    causal_anchors: int
    adjectival_density: float

class VeritasArchitecture:
    """
    АРХІТЕКТУРА VERITAS PROTOCOL
    """
    
    def __init__(self):
        self.ENTROPY_THRESHOLDS = {
            SystemState.LAMINAR_FLOW: (0.0, 0.4),
            SystemState.SYSTEMIC_FATIGUE: (0.4, 0.85),
            SystemState.WITNESS_SILENCE: (0.85, 1.0)
        }
        
        self.FRICTION_COEFFICIENTS = {
            EntropyType.TYPE_I_DETERMINISTIC: 0.1,
            EntropyType.TYPE_II_PROBABILISTIC: 0.3,
            EntropyType.TYPE_III_THEATRICAL: 0.6,
            EntropyType.TYPE_IV_SEMANTIC_NOISE: 0.8
        }
        
        self.ESI_CRITICAL_THRESHOLD = 0.85
        self.LAMBDA_CRITICAL_THRESHOLD = 0.85
        self.ARCHITECTURAL_FRICTION_COEFFICIENT = 1.0
        
        # УКРАЇНСЬКІ ДОМЕННІ КОРДОНИ
        self.DOMAIN_BOUNDARIES = {
            'physics': {
                'terms': {'термодинаміка', 'ентропія', 'енергія', 'квантовий', 'фізика', 
                         'математика', 'статистика', 'система', 'закон', 'формула'},
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
            },
            'science': {
                'terms': {'наука', 'дослідження', 'експеримент', 'теорія', 'гіпотеза',
                         'методологія', 'верифікація', 'емпіричний', 'об\'єктивний'},
                'allowed_connections': {'physics', 'mathematics', 'technology'},
                'forbidden_connections': {'esoteric', 'faith', 'superstition'}
            },
            'news': {
                'terms': {'новини', 'повідомлення', 'інформація', 'подія', 'звіт',
                         'репортаж', 'журналіст', 'редакція', 'публікація'},
                'allowed_connections': {'politics', 'economics', 'society'},
                'forbidden_connections': {'esoteric', 'superstition'}
            }
        }
        
        # УКРАЇНСЬКІ ПРИЧИННІ ЯКОРІ
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
            r'науковий консенсус',
            r'дослідження вказує',
            r'статистика показує',
            r'науково доведено'
        ]
        
        # УКРАЇНСЬКІ ЕМОЦІЙНІ МАРКЕРИ
        self.ADJECTIVAL_NOISE_PATTERNS = [
            r'\b(дуже|надзвичайно|неймовірно|жахливо|чудово)\b',
            r'\b(шокуючий|сенсаційний|скандальний|неймовірний)\b',
            r'\b(повинен|обов\'язково|неодмінно|абсолютно)\b',
            r'\b(катастрофа|крах|зрада|змова|небезпека)\b',
            r'\b(УВАГА|СРОЧНО|ВАЖЛИВО|НЕГАЙНО)\b'
        ]
        
        # УКРАЇНСЬКІ ПАТЕРНИ АСИМЕТРИЧНИХ ПЕРЕВАГ
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
    
    def analyze(self, text: str) -> Dict:
        """Основний метод аналізу"""
        
        if len(text.strip()) < 20:
            return self._witness_silence("Текст занадто короткий", "Мінімум 20 символів")
        
        logical_blocks = self._extract_logical_blocks(text)
        lac_results = self._logic_authenticity_check(text, logical_blocks)
        domain_analysis = self._analyze_domain_purity(text, logical_blocks)
        esi = self._calculate_entropy_stability_index(text, lac_results, domain_analysis)
        lambda_decay = self._calculate_linguistic_decay(text)
        entropy_type = self._classify_entropy_type(lac_results, domain_analysis, lambda_decay)
        architectural_friction = self._apply_architectural_friction(lac_results, domain_analysis, entropy_type)
        
        if self._should_trigger_witness_silence(esi, lambda_decay, lac_results):
            return self._witness_silence(
                "Порушення логічних порогів",
                f"ESI: {esi:.2f}, λ: {lambda_decay:.2f}"
            )
        
        final_score, system_state = self._calculate_final_verdict(
            esi, lambda_decay, lac_results, domain_analysis, architectural_friction
        )
        
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
    
    def _logic_authenticity_check(self, text: str, logical_blocks: List[str]) -> List[LogicalViolation]:
        """Перевірка логічної автентичності"""
        all_violations = []
        
        for i, block in enumerate(logical_blocks):
            violations = []
            
            # Перевірка стратегічних пропозицій
            for pattern in self.ASYMMETRIC_ADVANTAGE_PATTERNS:
                if re.search(pattern, block, re.IGNORECASE):
                    violations.append(LogicalViolation(
                        module="LAC_MODULE_I",
                        violation_type="АСИМЕТРИЧНА_ВИГОДА",
                        severity=0.5,
                        evidence=[f"Знайдено: {pattern}"],
                        context="Пропозиція без втрат/ризиків",
                        section=f"Блок {i+1}"
                    ))
            
            # Перевірка причинних якорів
            has_claim = any(re.search(r'\b(стверджую|доводять|доказ|факт)\b', block, re.IGNORECASE))
            if has_claim and self._count_causal_anchors(block) == 0:
                violations.append(LogicalViolation(
                    module="LAC_MODULE_II",
                    violation_type="НЕОБҐРУНТОВАНЕ_ТВЕРДЖЕННЯ",
                    severity=0.4,
                    evidence=["Твердження без джерел"],
                    context="Відсутність причинних якорів",
                    section=f"Блок {i+1}"
                ))
            
            # Перевірка семантичного шуму
            adj_count = sum(1 for pattern in self.ADJECTIVAL_NOISE_PATTERNS 
                          if re.search(pattern, block, re.IGNORECASE))
            if adj_count > 2:
                violations.append(LogicalViolation(
                    module="LAC_MODULE_III",
                    violation_type="ЕМОЦІЙНИЙ_ШУМ",
                    severity=0.3 + (adj_count * 0.1),
                    evidence=[f"{adj_count} емоційних маркерів"],
                    context="Надмірна емоційна навантаженість",
                    section=f"Блок {i+1}"
                ))
            
            all_violations.extend(violations)
        
        return all_violations
    
    def _analyze_domain_purity(self, text: str, logical_blocks: List[str]) -> DomainAnalysis:
        """Аналіз доменної чистоти"""
        detected_domains = set()
        domain_collapses = []
        
        for domain_name, domain_config in self.DOMAIN_BOUNDARIES.items():
            for term in domain_config['terms']:
                # Використовуємо українські літери в regex
                pattern = rf'(?i)\b{re.escape(term)}\b'
                if re.search(pattern, text):
                    detected_domains.add(domain_name)
        
        # Перевірка доменних колапсів
        domains_list = list(detected_domains)
        for i in range(len(domains_list)):
            for j in range(i + 1, len(domains_list)):
                d1, d2 = domains_list[i], domains_list[j]
                if d1 in self.DOMAIN_BOUNDARIES and d2 in self.DOMAIN_BOUNDARIES:
                    if d2 in self.DOMAIN_BOUNDARIES[d1]['forbidden_connections']:
                        domain_collapses.append((d1, d2))
        
        causal_anchors = self._count_causal_anchors(text)
        adjectival_density = self._calculate_adjectival_density(text)
        
        purity_score = 1.0
        if domain_collapses:
            purity_score = max(0.0, 1.0 - (len(domain_collapses) * 0.2))
        
        primary_domain = "невідомий"
        if detected_domains:
            primary_domain = next(iter(detected_domains))
        
        return DomainAnalysis(
            primary_domain=primary_domain,
            detected_domains=detected_domains,
            purity_score=purity_score,
            domain_collapses=domain_collapses,
            causal_anchors=causal_anchors,
            adjectival_density=adjectival_density
        )
    
    def _count_causal_anchors(self, text: str) -> int:
        """Підрахунок причинних якорів"""
        count = 0
        for pattern in self.CAUSAL_ANCHOR_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                count += 1
        return count
    
    def _calculate_adjectival_density(self, text: str) -> float:
        """Розрахунок густини прикметників"""
        # Спробуємо знайти прикметники за закінченнями
        words = re.findall(r'\b[а-яіїєґА-ЯІЇЄҐ\']+\b', text)
        if not words:
            return 0.0
        
        adjective_endings = ['ий', 'а', 'е', 'і', 'ова', 'ове', 'ий', 'а', 'я', 'е']
        adj_count = 0
        
        for word in words:
            lower_word = word.lower()
            if any(lower_word.endswith(end) for end in adjective_endings):
                adj_count += 1
        
        return adj_count / len(words)
    
    def _calculate_entropy_stability_index(self, text: str, lac_results: List[LogicalViolation],
                                         domain_analysis: DomainAnalysis) -> float:
        """Розрахунок індексу стабільності ентропії"""
        word_count = len(re.findall(r'\b[а-яіїєґА-ЯІЇЄҐ\']+\b', text))
        
        verification_complexity = 0.0
        violation_penalty = min(1.0, len(lac_results) * 0.15)
        verification_complexity += violation_penalty * 0.3
        
        domain_penalty = 1.0 - domain_analysis.purity_score
        verification_complexity += domain_penalty * 0.2
        
        tau_verify = min(1.0, verification_complexity)
        tau_inference = min(1.0, word_count / 1500)
        
        if tau_inference < 0.01:
            tau_inference = 0.01
        
        esi = tau_verify / tau_inference
        return min(1.0, esi / 8.0)
    
    def _calculate_linguistic_decay(self, text: str) -> float:
        """Розрахунок лінгвістичної деградації"""
        adjectival_density = self._calculate_adjectival_density(text)
        causal_anchors = self._count_causal_anchors(text)
        word_count = len(re.findall(r'\b[а-яіїєґА-ЯІЇЄҐ\']+\b', text))
        
        if word_count == 0:
            return 0.0
        
        causal_density = causal_anchors / max(1, word_count / 200)
        if causal_density < 0.005:
            causal_density = 0.005
        
        lambda_value = adjectival_density / causal_density
        return min(1.0, lambda_value / 15.0)
    
    def _classify_entropy_type(self, lac_results: List[LogicalViolation],
                             domain_analysis: DomainAnalysis,
                             lambda_decay: float) -> EntropyType:
        """Класифікація типу ентропії"""
        
        if any(v.violation_type == "АСИМЕТРИЧНА_ВИГОДА" and v.severity > 0.7 
               for v in lac_results):
            return EntropyType.TYPE_IV_SEMANTIC_NOISE
        
        if lambda_decay > 0.6 or domain_analysis.adjectival_density > 0.25:
            return EntropyType.TYPE_III_THEATRICAL
        
        if len(lac_results) == 0 and domain_analysis.purity_score > 0.7:
            return EntropyType.TYPE_I_DETERMINISTIC
        
        return EntropyType.TYPE_II_PROBABILISTIC
    
    def _apply_architectural_friction(self, lac_results: List[LogicalViolation],
                                    domain_analysis: DomainAnalysis,
                                    entropy_type: EntropyType) -> float:
        """Застосування архітектурного тертя"""
        base_friction = self.FRICTION_COEFFICIENTS[entropy_type]
        violation_multiplier = 1.0 + (len(lac_results) * 0.05)
        domain_multiplier = 1.0 + (len(domain_analysis.domain_collapses) * 0.1)
        
        total_friction = base_friction * violation_multiplier * domain_multiplier
        return min(1.0, total_friction)
    
    def _should_trigger_witness_silence(self, esi: float, lambda_decay: float,
                                      lac_results: List[LogicalViolation]) -> bool:
        """Чи потрібно активувати Witness Silence"""
        if esi > self.ESI_CRITICAL_THRESHOLD:
            return True
        
        if lambda_decay > self.LAMBDA_CRITICAL_THRESHOLD:
            return True
        
        critical_violations = [v for v in lac_results if v.severity > 0.8]
        if len(critical_violations) >= 3:
            return True
        
        return False
    
    def _witness_silence(self, reason: str, details: str) -> Dict:
        """Witness Silence - повна зупинка аналізу"""
        return {
            'entropy': 1.0,
            'status': 'WITNESS_SILENCE',
            'verdict': 'ПРОТОКОЛ_ЗУПИНЕНО',
            'language': 'UK',
            'explanation': f'СВІДОК МОВЧИТЬ: {reason} - {details}',
            'diagnostics': {
                'system_state': 'Свідок мовчить',
                'esi': 1.0,
                'lambda_decay': 1.0,
                'lac_violations': [],
                'domain_collapses': [],
                'architectural_friction': 1.0,
                'entropy_type': 'Семантичний шум',
                'is_protected_science': False,
                'word_count': 0,
                'char_count': 0
            }
        }
    
    def _calculate_final_verdict(self, esi: float, lambda_decay: float,
                               lac_results: List[LogicalViolation],
                               domain_analysis: DomainAnalysis,
                               architectural_friction: float) -> Tuple[float, SystemState]:
        """Розрахунок фінального вердикту"""
        base_score = (esi * 0.35) + (lambda_decay * 0.25)
        violation_penalty = min(0.3, len(lac_results) * 0.08)
        base_score += violation_penalty
        
        domain_penalty = min(0.15, len(domain_analysis.domain_collapses) * 0.05)
        base_score += domain_penalty
        
        final_score = min(0.99, base_score * architectural_friction)
        
        if final_score < 0.4:
            system_state = SystemState.LAMINAR_FLOW
        elif final_score < 0.85:
            system_state = SystemState.SYSTEMIC_FATIGUE
        else:
            system_state = SystemState.WITNESS_SILENCE
        
        return final_score, system_state
    
    def _extract_logical_blocks(self, text: str) -> List[str]:
        """Розділення тексту на логічні блоки"""
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        
        if not paragraphs:
            paragraphs = re.split(r'[.!?]+', text)
        
        blocks = []
        current_block = []
        
        for paragraph in paragraphs:
            if len(paragraph) < 30 and current_block:
                current_block.append(paragraph)
            else:
                if current_block:
                    blocks.append(' '.join(current_block))
                current_block = [paragraph]
        
        if current_block:
            blocks.append(' '.join(current_block))
        
        return blocks
    
    def _format_result(self, **kwargs) -> Dict:
        """Форматування результату"""
        
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
                'domain_collapses': kwargs['domain_analysis'].domain_collapses,
                'detected_domains': list(kwargs['domain_analysis'].detected_domains),
                'domain_purity_score': round(kwargs['domain_analysis'].purity_score, 3),
                'architectural_friction': round(kwargs['architectural_friction'], 3),
                'entropy_type': kwargs['entropy_type'].value,
                'causal_anchors': kwargs['domain_analysis'].causal_anchors,
                'adjectival_density': round(kwargs['domain_analysis'].adjectival_density, 3),
                'word_count': len(re.findall(r'\b[а-яіїєґА-ЯІЇЄҐ\']+\b', kwargs['text'])),
                'char_count': len(kwargs['text'])
            }
        }
    
    def _get_verdict(self, score: float, system_state: SystemState) -> str:
        """Визначення вердикту"""
        if system_state == SystemState.WITNESS_SILENCE:
            return "ПОРУШЕННЯ_АРХІТЕКТУРИ"
        elif score < 0.2:
            return "ЛАМІНАРНИЙ_ПОТІК"
        elif score < 0.4:
            return "ЛОГІЧНА_ЦІЛІСНІСТЬ"
        elif score < 0.6:
            return "ПОПЕРЕДЖЕННЯ_КОРДОНІВ"
        else:
            return "ВИТОМА_СИСТЕМИ"
    
    def _generate_explanation(self, kwargs: Dict) -> str:
        """Генерація пояснення"""
        parts = []
        
        if kwargs['esi'] > 0.6:
            parts.append(f"ESI: {kwargs['esi']:.2f} (нестабільність)")
        elif kwargs['esi'] < 0.3:
            parts.append(f"ESI: {kwargs['esi']:.2f} (стабільність)")
        
        if kwargs['lambda_decay'] > 0.6:
            parts.append(f"λ: {kwargs['lambda_decay']:.2f} (деградація)")
        
        if kwargs['lac_results']:
            parts.append(f"Порушень: {len(kwargs['lac_results'])}")
        
        if kwargs['domain_analysis'].domain_collapses:
            parts.append(f"Доменні колапси: {len(kwargs['domain_analysis'].domain_collapses)}")
        
        if kwargs['domain_analysis'].causal_anchors > 0:
            parts.append(f"Якорі: {kwargs['domain_analysis'].causal_anchors}")
        
        explanation = " | ".join(parts)
        
        if not explanation:
            explanation = "Текст відповідає архітектурним вимогам"
        
        return explanation


# ТЕСТУВАННЯ
if __name__ == "__main__":
    veritas = VeritasArchitecture()
    
    # ТЕСТ 1: Український науковий текст
    print("=" * 80)
    print("ТЕСТ 1: Український науковий текст")
    print("=" * 80)
    
    science_text = """
    Згідно з другим законом термодинаміки, в ізольованій системі ентропія не може зменшуватися. 
    Експериментальні дані підтверджують цю теорію. Статистична фізика описує цей стан.
    """
    
    result = veritas.analyze(science_text)
    print(f"Статус: {result['status']}")
    print(f"Вердикт: {result['verdict']}")
    print(f"Ентропія: {result['entropy']:.3f}")
    print(f"Пояснення: {result['explanation']}")
    print()
    
    # ТЕСТ 2: Українські новини
    print("=" * 80)
    print("ТЕСТ 2: Українські новини")
    print("=" * 80)
    
    news_text = """
    За даними Державної служби статистики, ВВП України зріс на 5% у третьому кварталі.
    Експерти вважають, що це пов'язано з відновленням економіки після війни.
    Міністерство економіки представило нову стратегію розвитку.
    """
    
    result = veritas.analyze(news_text)
    print(f"Статус: {result['status']}")
    print(f"Вердикт: {result['verdict']}")
    print(f"Ентропія: {result['entropy']:.3f}")
    print(f"Пояснення: {result['explanation']}")
    print()
    
    # ТЕСТ 3: Український маркетинг
    print("=" * 80)
    print("ТЕСТ 3: Український маркетинг")
    print("=" * 80)
    
    marketing_text = """
    УВАГА! АКЦІЯ! Купуйте наш продукт і отримуйте подвійну вигоду!
    Це абсолютно безкоштовно і без жодних прихованих платежів!
    Тільки сьогодні та тільки для вас - гарантований результат!
    """
    
    result = veritas.analyze(marketing_text)
    print(f"Статус: {result['status']}")
    print(f"Вердикт: {result['verdict']}")
    print(f"Ентропія: {result['entropy']:.3f}")
    print(f"Пояснення: {result['explanation']}")
