"""
Veritas Protocol - Radical Engine v6.0
Contextual Semantic Analysis with Neural Network-inspired Logic
"""

import math
import re
from typing import Dict, List, Tuple, Set
from collections import defaultdict

class VeritasCalibratedCore:
    """Neural network-inspired analysis with contextual absurdity detection"""
    
    def __init__(self):
        # НОВА АРХІТЕКТУРА: Глибинний семантичний аналіз
        self.context_layers = {
            'layer1': {'weight': 0.20},  # Базові терміни
            'layer2': {'weight': 0.35},  # Контекстуальні зв'язки
            'layer3': {'weight': 0.45},  # Мета-семантика
        }
        
        # СЕМАНТИЧНІ МОДУЛІ (замість простих списків)
        self.semantic_modules = {
            # Модуль 1: Науковий дискурс
            'scientific': {
                'core_terms': {
                    'статистичний', 'аналіз', 'кореляція', 'регресія', 'емпіричний',
                    'методологія', 'гіпотеза', 'експеримент', 'результат', 'висновок',
                    'верифікація', 'валідація', 'цитування', 'індекс', 'теорема',
                    'аксіома', 'постулат', 'деривація', 'інтеграція', 'диференціація'
                },
                'context_terms': {
                    'дослідження', 'публікація', 'журнал', 'конференція', 'протокол',
                    'модель', 'симуляція', 'прогноз', 'стохастичний', 'вероятність'
                },
                'absurd_connections': {'езотеричний', 'конспірологічний', 'містичний'}
            },
            
            # Модуль 2: Фінансовий дискурс
            'financial': {
                'core_terms': {
                    'фондовий', 'ринок', 'індекс', 'акція', 'облігація', 'інвестиція',
                    'капітал', 'бюджет', 'податок', 'дефіцит', 'профіцит', 'інфляція'
                },
                'context_terms': {
                    'трейдер', 'портфель', 'актив', 'пасив', 'рентабельність',
                    'ліквідність', 'волатильність', 'диверсифікація'
                },
                'absurd_connections': {'чакра', 'карма', 'астральний', 'енергетичний'}
            },
            
            # Модуль 3: Езотеричний дискурс
            'esoteric': {
                'core_terms': {
                    'чакра', 'карма', 'астральний', 'енергетичний', 'вібрація',
                    'резонанс', 'прана', 'ці', 'рейкі', 'медитація', 'транс'
                },
                'context_terms': {
                    'архетип', 'колективне', 'несвідоме', 'синхронічність',
                    'нумерологія', 'астрологія', 'хіромантія', 'біолокація'
                },
                'forbidden_contexts': {'науковий', 'фінансовий', 'юридичний'}
            },
            
            # Модуль 4: Конспірологічний дискурс
            'conspiracy': {
                'core_terms': {
                    'змова', 'таємний', 'орден', 'ілюмінат', 'рептилоїд', 'плоскоземель',
                    'хімітрейл', '5g', 'чіп', 'вакцина', 'контроль', 'розуму'
                },
                'context_terms': {
                    'приховують', 'приховування', 'брехня', 'фейк', 'дезінформація',
                    'маніпуляція', 'пропаганда', 'зомбування', 'психотронна'
                },
                'mirror_flags': {'правда', 'істина', 'свобода', 'розкриття'}
            },
            
            # Модуль 5: Корпоративний дискурс
            'corporate': {
                'core_terms': {
                    'синергія', 'стратегія', 'оптимізація', 'ефективність',
                    'kpi', 'окр', 'ланцюг', 'постачання', 'стейкхолдер'
                },
                'context_terms': {
                    'бренд', 'позиціонування', 'ринкова', 'частка', 'монетизація',
                    'масштабування', 'інновація', 'парадигма', 'холістичний'
                },
                'toxic_mixes': {'езотеричний', 'містичний', 'конспірологічний'}
            },
            
            # Модуль 6: Науково-фантастичний дискурс
            'scifi': {
                'core_terms': {
                    'нейтрино', 'квантовий', 'суперпозиція', 'ентанґлемент',
                    'телепортація', 'мультивсесвіт', 'паралельний', 'вимір'
                },
                'context_terms': {
                    'портал', 'симуляція', 'голограма', 'кіборг', 'трансгуманізм',
                    'сингулярність', 'нанотехнологія', 'біотехнологія'
                },
                'abuse_contexts': {'фінансовий', 'політичний', 'соціальний'}
            }
        }
        
        # СИНОНІМІЧНІ ЛАНЦЮГИ (для розпізнавання прихованих зв'язків)
        self.synonym_chains = {
            'наука': ['науковий', 'дослідницький', 'емпіричний', 'експериментальний'],
            'маніпуляція': ['вплив', 'контроль', 'програмування', 'зомбування'],
            'духовність': ['езотеричний', 'містичний', 'астральний', 'енергетичний'],
            'фінанси': ['економіка', 'капітал', 'ринок', 'інвестиція'],
            'технологія': ['цифровий', 'алгоритм', 'програмний', 'апаратний']
        }
        
        # СЕМАНТИЧНІ ПРАВИЛА (нейроноподібна логіка)
        self.semantic_rules = [
            {
                'name': 'НАУКОВИЙ_НІГІЛІЗМ',
                'condition': lambda modules: (
                    modules['scientific']['count'] > 3 and
                    modules['scifi']['count'] > 2 and
                    modules['financial']['count'] > 0
                ),
                'severity': 0.8,
                'verdict': 'НАУКОВИЙ НІГІЛІЗМ'
            },
            {
                'name': 'ДЗЕРКАЛЬНА_МАНІПУЛЯЦІЯ',
                'condition': lambda modules: (
                    modules['conspiracy']['count'] > 2 and
                    any(term in ['брехня', 'маніпуляція', 'фейк'] for term in modules['conspiracy']['found_terms'])
                ),
                'severity': 0.7,
                'verdict': 'ДЗЕРКАЛЬНА МАНІПУЛЯЦІЯ'
            },
            {
                'name': 'КОРПОРАТИВНИЙ_ОКУЛЬТИЗМ',
                'condition': lambda modules: (
                    modules['corporate']['count'] > 3 and
                    modules['esoteric']['count'] > 1
                ),
                'severity': 0.6,
                'verdict': 'КОРПОРАТИВНИЙ ОКУЛЬТИЗМ'
            },
            {
                'name': 'ГІБРИДНА_ТОКСИЧНІСТЬ',
                'condition': lambda modules: (
                    len([m for m in modules.values() if m['count'] > 1]) >= 3 and
                    modules.get('scientific', {}).get('count', 0) > 0 and
                    (modules.get('esoteric', {}).get('count', 0) > 0 or 
                     modules.get('conspiracy', {}).get('count', 0) > 0)
                ),
                'severity': 0.9,
                'verdict': 'ГІБРИДНА ТОКСИЧНІСТЬ'
            }
        ]
        
        # КОНТЕКСТУАЛЬНІ ШАБЛОНИ
        self.context_patterns = [
            {
                'name': 'фізика_для_економіки',
                'pattern': r'(нейтрино|квантовий|ентанґлемент).*?(ринок|економіка|трейдер|фондовий)',
                'severity': 0.8
            },
            {
                'name': 'магія_для_бізнесу',
                'pattern': r'(чакра|аура|енергія|вібрація).*?(kpi|оптимізація|стратегія|рентабельність)',
                'severity': 0.7
            },
            {
                'name': 'звинувачення_в_маніпуляції',
                'pattern': r'(брехня|фейк|маніпуляція|дезінформація).*?(правда|істина|розкриття|свобода)',
                'severity': 0.6
            }
        ]

    def detect_language(self, text: str) -> str:
        """Визначає мову тексту"""
        ukrainian_chars = re.findall(r'[їієґ]', text.lower())
        return 'uk' if len(ukrainian_chars) > 3 else 'en'

    def analyze_semantic_modules(self, text: str) -> Dict:
        """Аналізує текст через семантичні модулі"""
        text_lower = text.lower()
        modules_analysis = {}
        
        for module_name, module_data in self.semantic_modules.items():
            found_terms = set()
            
            # Перевірка основних термінів
            for term in module_data['core_terms']:
                if re.search(r'\b' + re.escape(term) + r'\b', text_lower):
                    found_terms.add(term)
            
            # Перевірка контекстних термінів
            for term in module_data['context_terms']:
                if re.search(r'\b' + re.escape(term) + r'\b', text_lower):
                    found_terms.add(term)
            
            modules_analysis[module_name] = {
                'count': len(found_terms),
                'found_terms': list(found_terms),
                'density': len(found_terms) / max(1, len(text_lower.split()))
            }
        
        return modules_analysis

    def analyze_contextual_patterns(self, text: str) -> Dict:
        """Аналізує контекстуальні паттерни"""
        patterns_found = []
        
        for pattern in self.context_patterns:
            matches = re.findall(pattern['pattern'], text.lower(), re.DOTALL)
            if matches:
                patterns_found.append({
                    'name': pattern['name'],
                    'count': len(matches),
                    'severity': pattern['severity']
                })
        
        return patterns_found

    def analyze_semantic_flow(self, text: str) -> float:
        """Аналізує семантичний потік тексту"""
        sentences = re.split(r'[.!?]+', text)
        if len(sentences) < 2:
            return 0.0
        
        semantic_shifts = 0
        prev_semantic_field = None
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            current_field = None
            
            # Визначаємо семантичне поле речення
            if any(term in sentence_lower for term in self.semantic_modules['scientific']['core_terms']):
                current_field = 'scientific'
            elif any(term in sentence_lower for term in self.semantic_modules['financial']['core_terms']):
                current_field = 'financial'
            elif any(term in sentence_lower for term in self.semantic_modules['esoteric']['core_terms']):
                current_field = 'esoteric'
            elif any(term in sentence_lower for term in self.semantic_modules['conspiracy']['core_terms']):
                current_field = 'conspiracy'
            
            if prev_semantic_field and current_field and prev_semantic_field != current_field:
                # Штраф за абсурдні переходи
                absurd_transitions = [
                    ('scientific', 'esoteric'),
                    ('financial', 'esoteric'),
                    ('scientific', 'conspiracy'),
                    ('corporate', 'esoteric')
                ]
                
                if (prev_semantic_field, current_field) in absurd_transitions:
                    semantic_shifts += 2
                else:
                    semantic_shifts += 1
            
            if current_field:
                prev_semantic_field = current_field
        
        return semantic_shifts / len(sentences)

    def calculate_shannon_entropy(self, text: str) -> float:
        """Обчислює ентропію Шеннона"""
        if not text:
            return 0.0
        
        clean_text = re.sub(r'\s+', ' ', text)
        char_freq = {}
        
        for char in clean_text:
            if char.isalpha() or char.isdigit():
                char_freq[char] = char_freq.get(char, 0) + 1
        
        if not char_freq:
            return 0.0
        
        entropy = 0.0
        text_len = len(clean_text)
        
        for count in char_freq.values():
            p = count / text_len
            if p > 0:
                entropy -= p * math.log2(p)
        
        max_entropy = math.log2(len(char_freq))
        normalized = entropy / max_entropy if max_entropy > 0 else 0
        
        return min(1.0, normalized)

    def calculate_complexity_score(self, text: str) -> float:
        """Обчислює складність тексту"""
        words = re.findall(r'\w+', text.lower())
        if len(words) < 10:
            return 0.5
        
        unique_ratio = len(set(words)) / len(words)
        
        sentences = re.split(r'[.!?]+', text)
        if sentences:
            avg_sentence_length = sum(len(s.split()) for s in sentences if s.strip()) / len(sentences)
        else:
            avg_sentence_length = 10
        
        complexity = (unique_ratio * 0.6) + (min(1.0, avg_sentence_length / 25) * 0.4)
        return min(1.0, complexity)

    def analyze(self, text: str) -> Dict:
        """Основний метод аналізу"""
        if not text or len(text.strip()) < 20:
            return {'error': 'Text too short'}
        
        lang = self.detect_language(text)
        words = text.split()
        word_count = len(words)
        
        # 1. СЕМАНТИЧНИЙ АНАЛІЗ МОДУЛІВ
        modules = self.analyze_semantic_modules(text)
        
        # 2. АНАЛІЗ КОНТЕКСТУАЛЬНИХ ПАТТЕРНІВ
        patterns = self.analyze_contextual_patterns(text)
        
        # 3. АНАЛІЗ СЕМАНТИЧНОГО ПОТОКУ
        semantic_flow = self.analyze_semantic_flow(text)
        
        # 4. БАЗОВІ МЕТРИКИ
        entropy = self.calculate_shannon_entropy(text)
        complexity = self.calculate_complexity_score(text)
        
        # 5. ВИЗНАЧЕННЯ ТИПУ ДИСКУРСУ
        discourse_type = 'neutral'
        if modules['scientific']['count'] > 3 and modules['scientific']['density'] > 0.05:
            discourse_type = 'academic'
        elif modules['conspiracy']['count'] > 2:
            discourse_type = 'conspiracy'
        elif modules['esoteric']['count'] > 2:
            discourse_type = 'esoteric'
        elif modules['corporate']['count'] > 3:
            discourse_type = 'corporate'
        
        # 6. ЗАСТОСУВАННЯ СЕМАНТИЧНИХ ПРАВИЛ
        triggered_rules = []
        total_severity = 0.0
        
        for rule in self.semantic_rules:
            if rule['condition'](modules):
                triggered_rules.append(rule['name'])
                total_severity = max(total_severity, rule['severity'])
        
        # 7. РОЗРАХУНОК ФІНАЛЬНОГО РЕЙТИНГУ
        base_score = (
            entropy * 0.15 +
            complexity * 0.10 +
            semantic_flow * 0.35 +
            total_severity * 0.40
        )
        
        # Корекція за кількість паттернів
        pattern_multiplier = 1.0 + (len(patterns) * 0.1)
        final_score = min(0.99, base_score * pattern_multiplier)
        
        # 8. ВИЗНАЧЕННЯ ВЕРДИКТУ
        status = 'ACCEPTABLE'
        verdict = 'ПРИЙНЯТНА СТРУКТУРОВАНА ІНФОРМАЦІЯ'
        
        if triggered_rules:
            status = 'CRITICAL'
            
            if 'НАУКОВИЙ_НІГІЛІЗМ' in triggered_rules:
                verdict = 'НАУКОВИЙ НІГІЛІЗМ'
            elif 'ДЗЕРКАЛЬНА_МАНІПУЛЯЦІЯ' in triggered_rules:
                verdict = 'ДЗЕРКАЛЬНА МАНІПУЛЯЦІЯ'
            elif 'КОРПОРАТИВНИЙ_ОКУЛЬТИЗМ' in triggered_rules:
                verdict = 'КОРПОРАТИВНИЙ ОКУЛЬТИЗМ'
            elif 'ГІБРИДНА_ТОКСИЧНІСТЬ' in triggered_rules:
                verdict = 'ГІБРИДНА ТОКСИЧНІСТЬ'
        elif final_score > 0.7:
            status = 'WARNING'
            verdict = 'ВИСОКИЙ РІВЕНЬ СЕМАНТИЧНОЇ НЕСТАБІЛЬНОСТІ'
        elif final_score > 0.5:
            status = 'SUSPICIOUS'
            verdict = 'ПІДОЗРІЛА СЕМАНТИЧНА СТРУКТУРА'
        
        # 9. ПІДГОТОВКА РЕЗУЛЬТАТІВ
        chaos_markers = modules['esoteric']['count'] + modules['conspiracy']['count'] + modules['scifi']['count']
        signal_markers = modules['scientific']['count']
        noise_markers = modules['conspiracy']['count'] + modules['esoteric']['count']
        
        return {
            'entropy': round(final_score, 3),
            'status': status,
            'verdict': verdict,
            'language': lang.upper(),
            'is_academic_context': discourse_type == 'academic',
            'diagnostics': {
                'shannon_entropy': round(entropy, 3),
                'complexity': round(complexity, 3),
                'semantic_flow': round(semantic_flow, 3),
                'semantic_dissonance': round(semantic_flow * 0.8, 3),
                'word_count': word_count,
                'char_count': len(text),
                'chaos_markers': chaos_markers,
                'noise_markers': noise_markers,
                'signal_markers': signal_markers,
                'sanity_penalty': round(semantic_flow * 0.6, 3),
                'academic_markers': modules['scientific']['count'],
                'shout_factor': len([w for w in words if w.isupper() and len(w) > 2]) / max(1, word_count),
                'number_density': len(re.findall(r'\d+', text)) / max(1, word_count),
                'triggered_rules': triggered_rules,
                'discourse_type': discourse_type,
                'pattern_count': len(patterns)
            }
        }
