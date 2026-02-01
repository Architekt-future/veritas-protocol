"""
Veritas Protocol - Semantic Void Detector v11.0 (LOGICAL INQUISITOR)
Complete rewrite based on audit findings
"""

import re
import math
import sympy
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict, Tuple, Set
import numpy as np

@dataclass
class LogicalViolation:
    """Представляє логічне порушення високого рівня"""
    type: str  # 'semantic_incoherence', 'domain_collapse', 'proof_attack'
    severity: float  # 0.0-1.0
    evidence: List[str]
    context: str

class DomainGuardian:
    """Охоронець наукових доменів - запобігає false positives для науки"""
    
    # Безпечні наукові контексти (класична наука)
    SAFE_SCIENCE_CONTEXTS = {
        'physics': {
            'terms': ['термодинаміка', 'ентропія', 'енергія', 'маса', 'заряд', 
                     'потенціал', 'поле', 'сила', 'прискорення', 'швидкість'],
            'safe_patterns': [
                r'другий закон термодинаміки',
                r'закон збереження енергії',
                r'закон всесвітнього тяжіння',
                r'рівняння Шредінгера',
                r'теорія відносності',
                r'квантова механіка'
            ],
            'domain_boundary': ['душа', 'карма', 'аура', 'енергетичний', 'вібраційний']
        },
        'mathematics': {
            'terms': ['формула', 'рівняння', 'теорема', 'доказ', 'аксіома',
                     'функція', 'похідна', 'інтеграл', 'матриця', 'вектор'],
            'safe_patterns': [
                r'теорема Піфагора',
                r'рівняння Ейлера',
                r'біном Ньютона',
                r'ряд Тейлора',
                r'числа Фібоначчі'
            ]
        },
        'biology': {
            'terms': ['клітина', 'днк', 'ген', 'еволюція', 'метаболізм',
                     'імунітет', 'нейрон', 'синапс', 'гормон', 'фермент'],
            'safe_patterns': [
                r'теорія еволюції',
                r'структура ДНК',
                r'клітинна теорія',
                r'природний добір'
            ]
        }
    }
    
    # Критичні наукові формули, які НЕ МОЖУТЬ змінювати сенс
    PROTECTED_FORMULAS = {
        'E=mc²': {
            'meaning': 'Енергія дорівнює масі помноженій на квадрат швидкості світла',
            'constants': {'c': 'швидкість світла у вакуумі (~299792458 м/с)'},
            'forbidden_redefinitions': [
                r'c\s*=\s*швидкість думки',
                r'c\s*=\s*енергія космосу',
                r'c\s*=\s*частота серця',
                r'E\s*=\s*емоція'
            ]
        },
        'F=ma': {
            'meaning': 'Сила дорівнює масі помноженій на прискорення',
            'forbidden_redefinitions': [
                r'F\s*=\s*віра',
                r'F\s*=\s*потік',
                r'a\s*=\s*астральне'
            ]
        },
        'S=k·lnW': {
            'meaning': 'Ентропія пропорційна логарифму кількості мікростанів',
            'forbidden_redefinitions': [
                r'S\s*=\s*свідомість',
                r'W\s*=\s*воля',
                r'ентропія\s*=\s*хаос душі'
            ]
        }
    }
    
    def __init__(self):
        self.domain_violations = []
        self.formula_attacks = []
        
    def analyze_domain_purity(self, text: str) -> List[LogicalViolation]:
        """Аналізує чистоту наукових доменів"""
        violations = []
        text_lower = text.lower()
        
        # Перевірка кожного наукового домену
        for domain, config in self.SAFE_SCIENCE_CONTEXTS.items():
            # Шукаємо терміни цього домену
            domain_terms_found = []
            for term in config['terms']:
                if term in text_lower:
                    domain_terms_found.append(term)
            
            if domain_terms_found:
                # Перевіряємо, чи текст в безпечному контексті
                is_safe_context = False
                for pattern in config.get('safe_patterns', []):
                    if re.search(pattern, text_lower, re.IGNORECASE):
                        is_safe_context = True
                        break
                
                # Якщо не в безпечному контексті, шукаємо доменні порушення
                if not is_safe_context and 'domain_boundary' in config:
                    boundary_violations = []
                    for boundary_term in config['domain_boundary']:
                        if boundary_term in text_lower:
                            boundary_violations.append(boundary_term)
                    
                    if boundary_violations:
                        violations.append(LogicalViolation(
                            type='domain_collapse',
                            severity=0.6,
                            evidence=domain_terms_found[:3] + boundary_violations[:3],
                            context=f'Науковий домен "{domain}" змішаний з езотерикою'
                        ))
        
        return violations
    
    def detect_formula_attacks(self, text: str) -> List[LogicalViolation]:
        """Виявляє атаки на наукові формули"""
        attacks = []
        text_lower = text.lower()
        
        for formula, protection in self.PROTECTED_FORMULAS.items():
            # Шукаємо формулу або її компоненти
            formula_pattern = formula.replace('²', '2').replace('·', '')
            if formula_pattern in text or any(term in text_lower for term in formula.split() if len(term) > 1):
                
                # Перевіряємо перевизначення констант
                for attack_pattern in protection['forbidden_redefinitions']:
                    if re.search(attack_pattern, text_lower, re.IGNORECASE):
                        attacks.append(LogicalViolation(
                            type='formula_attack',
                            severity=0.8,
                            evidence=[formula, attack_pattern],
                            context=f'Напад на фундаментальну формулу: {formula}'
                        ))
                        break
        
        return attacks

class LogicalInquisitor:
    """Математичний інквізитор - жорстка перевірка логічних зв'язків"""
    
    def __init__(self):
        # Пари, що викликають логічний колапс
        self.logical_collapse_pairs = [
            # Наука + Езотерика (3x множник)
            (['наука', 'доказ', 'експеримент', 'гіпотеза', 'теорія'],
             ['віра', 'почуття', 'інтуїція', 'очевидність', 'аксіома'],
             0.7, 3.0),  # weight, multiplier
            
            # Математика + Містика
            (['математика', 'формула', 'рівняння', 'обчислення', 'статистика'],
             ['душа', 'карма', 'судьба', 'провидіння', 'чудо'],
             0.65, 3.0),
            
            # Логіка + Емоція
            (['логіка', 'раціональний', 'розум', 'аргумент', 'доказ'],
             ['емоція', 'серце', 'інтуїція', 'віра', 'відчуття'],
             0.6, 2.5),
            
            # Фізика + Соціальні явища
            (['фізика', 'термодинаміка', 'ентропія', 'енергія', 'атом'],
             ['суспільство', 'політика', 'культура', 'мораль', 'етика'],
             0.55, 2.0),
            
            # Бізнес + Езотерика (особливо небезпечно!)
            (['бізнес', 'ринок', 'прибуток', 'стратегія', 'ефективність'],
             ['чакра', 'аура', 'енергія', 'вібрація', 'карма'],
             0.75, 3.5),  # Найвищий множник!
        ]
        
        # Патерни мета-атак на логіку
        self.meta_attack_patterns = [
            (r'(логіка|математика|наука)\s+.*?(застаріла|непрацює|недійсна)', 0.8),
            (r'(почуття|інтуїція|віра)\s+.*?(важливіше|краще|вище)\s+.*?(логіки|науки)', 0.7),
            (r'(резонанс|вібрація)\s+.*?(серця|душі)\s+.*?(важливіше|точніше)\s+.*?(математики)', 0.9),
            (r'цифрова\s+.*?(диктатура|тиранія)\s+.*?(розробника|алгоритму)', 0.6),
            (r'вільний\s+вибір\s+.*?(важливіший|вищий)\s+.*?(законів\s+фізики)', 0.75)
        ]
        
    def detect_collapses(self, text: str) -> Tuple[float, List[LogicalViolation]]:
        """Виявляє логічні колапси з множниками"""
        total_penalty = 0.0
        violations = []
        text_lower = text.lower()
        
        for first_terms, second_terms, weight, multiplier in self.logical_collapse_pairs:
            has_first = any(term in text_lower for term in first_terms)
            has_second = any(term in text_lower for term in second_terms)
            
            if has_first and has_second:
                # Перевіряємо зв'язок в реченнях
                sentences = re.split(r'[.!?]+', text)
                for sentence in sentences:
                    sentence_lower = sentence.lower()
                    first_in_sentence = any(term in sentence_lower for term in first_terms)
                    second_in_sentence = any(term in sentence_lower for term in second_terms)
                    
                    if first_in_sentence and second_in_sentence:
                        # Знайдено прямий зв'язок - застосовуємо множник!
                        penalty = weight * multiplier
                        total_penalty += penalty
                        
                        violations.append(LogicalViolation(
                            type='semantic_incoherence',
                            severity=penalty,
                            evidence=[first_terms[0], second_terms[0]],
                            context=f'Логічний колапс: {first_terms[0]} + {second_terms[0]} (x{multiplier})'
                        ))
                        break
        
        return min(total_penalty, 1.0), violations
    
    def detect_meta_attacks(self, text: str) -> Tuple[float, List[LogicalViolation]]:
        """Виявляє мета-атаки на логічні системи"""
        total_penalty = 0.0
        violations = []
        text_lower = text.lower()
        
        for pattern, severity in self.meta_attack_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                total_penalty += severity
                
                match = re.search(pattern, text_lower, re.IGNORECASE)
                violations.append(LogicalViolation(
                    type='proof_attack',
                    severity=severity,
                    evidence=[match.group(0) if match else pattern],
                    context='Мета-атака на логічну систему'
                ))
        
        return min(total_penalty, 1.0), violations

class ComplexityDemystifier:
    """Демистифікатор складності - усуває гало-ефект"""
    
    def __init__(self):
        # Структуровані маркери божевілля (виглядають як наука, але нею не є)
        self.structured_madness_indicators = [
            # Бізнес-езотерика
            ('квантова', ['стратегія', 'лідерство', 'менеджмент', 'маркетинг']),
            ('енергетичний', ['бізнес', 'ринок', 'продажі', 'переговори']),
            ('вібраційний', ['менеджмент', 'комунікація', 'презентація']),
            ('аура', ['продажів', 'переговорів', 'лідерства']),
            
            # Соціальна псевдонаука
            ('соціальний', ['резонанс', 'вібрація', 'енергія']),
            ('економічний', ['потік', 'енергія', 'вібрація']),
            ('політичний', ['квант', 'поле', 'енергія']),
        ]
        
        # Маркери псевдоінтелектуального стилю
        self.pseudo_intellectual_style = [
            'парадигма', 'дискурс', 'наратив', 'конструкт', 'семіозис',
            'трансгресивний', 'деконструкція', 'постмодерн', 'метанаратив',
            'симулякр', 'гіперреальність', 'детеріторіалізація'
        ]
        
    def analyze_structured_madness(self, text: str) -> Tuple[float, List[str]]:
        """Аналізує структуроване божевілля"""
        penalty = 0.0
        evidence = []
        text_lower = text.lower()
        
        # Перевірка структурованого божевілля
        for esoteric_term, business_terms in self.structured_madness_indicators:
            if esoteric_term in text_lower:
                for business_term in business_terms:
                    if business_term in text_lower:
                        # Шукаємо зв'язок у реченнях
                        pattern = rf'{esoteric_term}.*?{business_term}|{business_term}.*?{esoteric_term}'
                        if re.search(pattern, text_lower, re.IGNORECASE):
                            penalty += 0.4
                            evidence.append(f"{esoteric_term} + {business_term}")
                            break
        
        # Псевдоінтелектуальний стиль без змісту
        style_terms_found = [term for term in self.pseudo_intellectual_style 
                           if term in text_lower]
        
        if style_terms_found >= 3:
            # Перевіряємо наявність реального змісту
            content_indicators = ['дані', 'дослідження', 'результати', 'метод', 'вибірка']
            has_content = any(indicator in text_lower for indicator in content_indicators)
            
            if not has_content:
                penalty += 0.3
                evidence.append("Псевдоінтелектуальний стиль без змісту")
        
        return min(penalty, 0.7), evidence

class VeritasCalibratedCore:
    """ПОВНА ПЕРЕБУДОВА - Logical Inquisitor Edition"""
    
    def __init__(self):
        # Нова архітектура
        self.domain_guardian = DomainGuardian()
        self.logical_inquisitor = LogicalInquisitor()
        self.complexity_demystifier = ComplexityDemystifier()
        
        # Зберігаємо оригінальні списки, але з меншою вагою
        self.chaos_indicators = {
            'esoteric': ['чакра', 'карма', 'астральний', 'енергетичний', 'вібрація'],
            'pseudoscience': ['квантовий', 'нейтрино', 'торсійний', 'ефір'],
            'conspiracy': ['рептилоїд', 'ілюмінат', 'хімітрейл']
        }
        
        self.academic_whitelist = [
            'кореляція', 'гіпотеза', 'експеримент', 'статистика',
            'методологія', 'рецензування', 'публікація'
        ]
        
    def analyze(self, text: str) -> Dict:
        """Головний метод аналізу з новою архітектурою"""
        if not text or len(text.strip()) < 20:
            return {'error': 'Text too short'}
        
        # Фаза 1: Доменний аналіз (Science Protection)
        domain_violations = self.domain_guardian.analyze_domain_purity(text)
        formula_attacks = self.domain_guardian.detect_formula_attacks(text)
        
        # Фаза 2: Логічний інквізитор
        collapse_penalty, collapse_violations = self.logical_inquisitor.detect_collapses(text)
        meta_attack_penalty, meta_violations = self.logical_inquisitor.detect_meta_attacks(text)
        
        # Фаза 3: Демистифікація складності
        madness_penalty, madness_evidence = self.complexity_demystifier.analyze_structured_madness(text)
        
        # Фаза 4: Традиційний аналіз (менша вага)
        traditional_score = self._traditional_analysis(text)
        
        # АГРЕГАЦІЯ З НОВИМИ ПРАВИЛАМИ
        total_violations = (domain_violations + formula_attacks + 
                          collapse_violations + meta_violations)
        
        # КРИТИЧНЕ ПРАВИЛО: Науковий текст без порушень отримує захист
        is_protected_science = self._is_protected_scientific_text(text, total_violations)
        
        if is_protected_science:
            base_score = traditional_score * 0.2  # Різке зниження
        else:
            # Нова формула з акцентом на логічні порушення
            base_score = (
                collapse_penalty * 0.45 +           # Логічні колапси - найважливіші!
                meta_attack_penalty * 0.30 +        # Мета-атаки
                madness_penalty * 0.35 +            # Структуроване божевілля
                traditional_score * 0.15 +          # Традиційний аналіз (менша вага)
                (len(formula_attacks) * 0.25)       # Атаки на формули
            )
        
        # ЗАСТОСУВАННЯ МНОЖНИКІВ
        # Множник за кількість порушень
        violation_multiplier = 1.0 + (len(total_violations) * 0.15)
        base_score *= violation_multiplier
        
        # Множник за структуроване божевілля
        if madness_evidence:
            base_score *= 1.3
        
        final_score = min(0.99, max(0.0, base_score))
        
        # ВЕРДИКТИ НОВОГО ПОКОЛІННЯ
        if formula_attacks:
            status = 'CRITICAL'
            verdict = 'МАТЕМАТИЧНА ДИВЕРСІЯ'
            explanation = 'Атака на фундаментальні наукові формули'
        elif collapse_penalty > 0.5:
            status = 'CRITICAL'
            verdict = 'ЛОГІЧНИЙ КОЛАПС'
            explanation = 'Повне руйнування доменних кордонів'
        elif meta_attack_penalty > 0.4:
            status = 'CRITICAL'
            verdict = 'МЕТА-АТАКА НА РОЗУМ'
            explanation = 'Спроба дискредитації логічних систем'
        elif final_score > 0.6:
            status = 'CRITICAL'
            verdict = 'СТРУКТУРОВАНЕ БОЖЕВІЛЛЯ'
            explanation = 'Елітарна маніпуляція під виглядом науки'
        elif final_score > 0.4:
            status = 'WARNING'
            verdict = 'ДОМЕННЕ ПОРУШЕННЯ'
            explanation = 'Змішування несумісних категорій'
        elif final_score > 0.2:
            status = 'ACCEPTABLE'
            verdict = 'ПРИЙНЯТНИЙ ДИСКУРС'
            explanation = 'Дотримання базових логічних норм'
        elif final_score > 0.05:
            status = 'TRUSTED'
            verdict = 'ЛОГІЧНА ЦІЛІСНІСТЬ'
            explanation = 'Високоякісний структурований зміст'
        else:
            status = 'VERIFIED'
            verdict = 'АКАДЕМІЧНИЙ СТАНДАРТ'
            explanation = 'Ідеальне дотримання наукових норм'
        
        # ДЕТАЛІЗОВАНІ ПОРУШЕННЯ
        if total_violations:
            violation_details = []
            for i, viol in enumerate(total_violations[:5], 1):
                violation_details.append(f"{i}. {viol.type}: {', '.join(viol.evidence[:2])}")
            
            explanation += " | Порушення: " + "; ".join(violation_details)
        
        if madness_evidence:
            explanation += f" | Структ. божевілля: {', '.join(madness_evidence[:3])}"
        
        # РОЗРАХУНОК ІНДЕКСІВ
        chaos_index = self._calculate_chaos_index(final_score, len(total_violations), collapse_penalty)
        influence_index = self._calculate_influence_index(final_score, meta_attack_penalty)
        
        return {
            'entropy': round(final_score, 3),
            'status': status,
            'verdict': verdict,
            'language': 'UK',
            'explanation': explanation,
            'diagnostics': {
                'final_score': round(final_score, 3),
                'collapse_penalty': round(collapse_penalty, 3),
                'meta_attack_penalty': round(meta_attack_penalty, 3),
                'madness_penalty': round(madness_penalty, 3),
                'formula_attacks': len(formula_attacks),
                'domain_violations': len(domain_violations),
                'total_violations': len(total_violations),
                'violation_multiplier': round(violation_multiplier, 2),
                'is_protected_science': is_protected_science,
                'chaos_index': chaos_index,
                'influence_index': influence_index,
                'violation_types': list(set(v.type for v in total_violations)),
                'structured_madness_evidence': madness_evidence[:5]
            }
        }
    
    def _traditional_analysis(self, text: str) -> float:
        """Спрощений традиційний аналіз (менша вага)"""
        score = 0.0
        text_lower = text.lower()
        
        # Прості перевірки
        for category, terms in self.chaos_indicators.items():
            for term in terms:
                if term in text_lower:
                    score += 0.05
        
        # Наявність академічних маркерів ЗНИЖУЄ штраф
        academic_count = sum(1 for term in self.academic_whitelist if term in text_lower)
        if academic_count >= 3:
            score *= 0.5  # Науковий текст - менший штраф
        
        return min(score, 0.3)
    
    def _is_protected_scientific_text(self, text: str, violations: List[LogicalViolation]) -> bool:
        """Визначає, чи текст є захищеною наукою"""
        text_lower = text.lower()
        
        # Критерії захищеної науки
        academic_terms = sum(1 for term in self.academic_whitelist if term in text_lower)
        
        # Має бути достатньо наукових термінів
        if academic_terms < 2:
            return False
        
        # Не повинно бути хаос-термінів
        has_chaos = any(
            any(term in text_lower for term in terms)
            for terms in self.chaos_indicators.values()
        )
        
        if has_chaos:
            return False
        
        # Не повинно бути серйозних порушень
        serious_violations = any(v.severity > 0.3 for v in violations)
        
        return not serious_violations
    
    def _calculate_chaos_index(self, final_score: float, violation_count: int, collapse_penalty: float) -> float:
        """Новий розрахунок індексу хаосу"""
        base = final_score * 100
        
        if violation_count == 0:
            return round(base * 0.5, 2)
        
        # Експоненційний ріст за порушення
        multiplier = 1 + (violation_count * 0.3) + (collapse_penalty * 0.5)
        return round(base * multiplier, 2)
    
    def _calculate_influence_index(self, final_score: float, meta_attack_penalty: float) -> float:
        """Розрахунок індексу впливу"""
        base = final_score * 100
        
        # Мета-атаки значно підвищують індекс впливу
        influence = base * (1 + meta_attack_penalty * 0.8)
        return round(influence, 2)


# Експорт класу для зворотної сумісності
VeritasCalibratedCore = VeritasCalibratedCore
