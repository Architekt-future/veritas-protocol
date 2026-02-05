"""
Veritas Semantic Void Detector v1.0
Detects absence of meaning, not presence of bad words
Philosophy: "Elegant lies are smooth. Truth has friction."
"""

import re
from typing import Dict, List, Tuple
from collections import Counter


class SemanticVoidDetector:
    """
    Measures emptiness rather than looking for markers
    Three dimensions:
    1. ABSENCE (what's missing: facts, numbers, specifics)
    2. VAGUENESS (hollow buzzwords without substance)
    3. FALSE CAUSALITY (A→B claims where A and B are unrelated)
    """
    
    def __init__(self):
        # ================================================================
        # DIMENSION 1: ABSENCE MARKERS
        # ================================================================
        
        # Things that SHOULD exist in meaningful text
        self.concrete_markers = {
            'numbers': r'\d+(?:[.,]\d+)?(?:\s*%)?',  # 42, 3.14, 95%
            'dates': r'\d{4}|\d{1,2}\s+(січня|лютого|березня|квітня|травня|червня|липня|серпня|вересня|жовтня|листопада|грудня)',
            'names': r'[А-ЯІЇЄҐ][а-яіїєґ]+\s+[А-ЯІЇЄҐ][а-яіїєґ]+',  # Proper names
            'locations': r'(київ|україн|європ|сша|росі|китай|львів|одес)',
            'verifiable_sources': r'(університет|інститут|дослідження|експеримент|публікація|журнал)',
            'concrete_actions': r'(створив|побудував|винайшов|виміряв|зафіксував|довів)',
        }
        
        # ================================================================
        # DIMENSION 2: VAGUENESS (hollow corporate/academic speak)
        # ================================================================
        
        self.hollow_buzzwords = [
            # Corporate hollow
            'парадигма', 'синергія', 'синергетичний', 'оптимізація', 'імплементація',
            'консолідувати', 'моніторинг', 'векторів', 'децентралізація', 'турбулентність',
            'дорожня карта', 'горизонтальний', 'вертикальний', 'інноваційний',
            
            # Academic hollow
            'ціннісні наративи', 'соціальний ландшафт', 'дискурсивний простір',
            'пост-істина', 'інклюзивний діалог', 'гнучка категорія', 'трансформація',
            'ревізія', 'декларативний підхід', 'інтегрувати суперечності',
            
            # Spiritual hollow
            'резонанс серця', 'квантовий резонанс', 'ефірні коди', 'ноосфера',
            'колективне несвідоме', 'світлові коди', 'вібраційний', 'багатогранність',
            
            # Generic hollow
            'можливість', 'потенціал', 'аспект', 'фактор', 'компонент', 'елемент',
            'процес', 'структура', 'система', 'механізм', 'динаміка', 'контекст',
        ]
        
        # Vague abstract phrases (no concrete meaning)
        self.vague_phrases = [
            r'м\'яка трансформація',
            r'відсутність результату є.*результат',
            r'гнучка (категорія|істина)',
            r'адаптується до потреб моменту',
            r'інтегрувати суперечності',
            r'шлях.*нікуди',
            r'не просто.*а (глибок|істин)',
            r'багатогранність.*досвід',
        ]
        
        # ================================================================
        # DIMENSION 3: FALSE CAUSALITY
        # ================================================================
        
        # Domain incompatibility matrix
        # If A from domain X, and B from domain Y, check if X→Y makes sense
        self.domain_terms = {
            'physics': ['гравітація', 'квантов', 'ентропі', 'електромагніт', 'нейтрин', 
                       'термодинамік', 'фізичн', 'енергі', 'частинк', 'хвил'],
            'biology': ['днк', 'клітин', 'нейрон', 'синапс', 'мозк', 'організм', 'біологічн'],
            'psychology': ['свідом', 'несвідом', 'когнітивн', 'емоційн', 'психологічн'],
            'politics': ['демократ', 'політ', 'держав', 'урядів', 'владн', 'інститут'],
            'economics': ['економ', 'ринк', 'капітал', 'інвестиц', 'фінанс', 'бюджет'],
            'spirituality': ['душ', 'дух', 'астрал', 'карм', 'чакр', 'енергетичн', 'вібрац'],
            'technology': ['алгоритм', 'код', 'програм', 'цифров', 'blockchain', 'ai'],
            'law': ['закон', 'право', 'юридичн', 'конституц', 'кодекс', 'судов'],
        }
        
        # Forbidden cross-domain causality
        # (source_domain, target_domain, example_pattern)
        self.forbidden_causality = [
            ('physics', 'politics', r'(гравітація|квантов|ентропі).{10,150}(демократ|політ|урядів)'),
            ('physics', 'economics', r'(нейтрин|електромагніт).{10,150}(економ|ринк|капітал)'),
            ('spirituality', 'technology', r'(душ|карм|чакр).{10,150}(алгоритм|blockchain|код)'),
            ('spirituality', 'law', r'(енергетичн|вібрац|астрал).{10,150}(закон|право|кодекс)'),
            ('physics', 'psychology', r'(квантов|ентропі).{10,150}(свідом|когнітивн)'),
        ]
        
        # ONTOLOGICAL CATEGORY ERRORS
        # Physical entities described as social/mental constructs
        self.ontological_errors = [
            r'(гравітація|електромагнетизм|фізика|енергія).{10,100}(соціальний конструкт|культурн|нав.язан)',
            r'(світло|хвил|частинк).{10,100}(свідомість|колективн.{1,20}(свідом|думк))',
            r'(об.єкти|тіла|матерія).{10,100}(погоджу|вір|свідом).{10,100}(падають|рухають)',
            r'(закон.{1,20}(фізик|природ)).{10,100}(догм|переконання|віра)',
        ]
        
        # Causal claim patterns (оскільки X, то Y / X дозволяє Y)
        self.causal_patterns = [
            r'оскільки\s+([^,]{10,100})[,;]\s+(тому|значить|отже|ми маємо)',
            r'([^,]{10,100})\s+дозволяє\s+([^.]{10,100})',
            r'через\s+([^,]{10,100})[,;]?\s+([^.]{10,100})',
            r'завдяки\s+([^,]{10,100})[,;]?\s+([^.]{10,100})',
        ]
        
        # ================================================================
        # DIMENSION 4: UNFALSIFIABLE CLAIMS
        # ================================================================
        
        self.unfalsifiable_patterns = [
            r'може (не )?бути',
            r'імовірно.*але',
            r'потенційно.*проте',
            r'можливо.*однак',
            r'гнучка (категорія|істина)',
            r'залежить від (моменту|контексту|сприйняття)',
            r'(істина|правда) стає',  # truth is not stable
            r'не піддається (калькуляції|вимірюванню|аналізу)',
        ]

    def analyze(self, text: str) -> Dict:
        """
        Returns semantic void score (0.0-1.0)
        Higher = more void (less substance)
        """
        if len(text) < 50:
            return {'void_score': 0.0, 'reason': 'text_too_short'}
        
        text_lower = text.lower()
        words = text.split()
        word_count = len(words)
        
        penalties = {
            'absence': 0.0,
            'vagueness': 0.0, 
            'false_causality': 0.0,
            'unfalsifiable': 0.0,
        }
        
        evidence = {
            'missing_concrete': [],
            'hollow_buzzwords_found': [],
            'false_causal_claims': [],
            'unfalsifiable_claims': [],
        }
        
        # ================================================================
        # CHECK 1: ABSENCE (what's missing)
        # ================================================================
        
        concrete_found = {}
        for marker_type, pattern in self.concrete_markers.items():
            matches = re.findall(pattern, text_lower)
            concrete_found[marker_type] = len(matches)
            if len(matches) == 0:
                evidence['missing_concrete'].append(marker_type)
        
        # Penalty for absence
        missing_count = len(evidence['missing_concrete'])
        if missing_count >= 5:  # missing almost everything
            penalties['absence'] = 0.4
        elif missing_count >= 3:
            penalties['absence'] = 0.25
        elif missing_count >= 2:
            penalties['absence'] = 0.1
        
        # ================================================================
        # CHECK 2: VAGUENESS (hollow buzzwords)
        # ================================================================
        
        buzzword_count = 0
        for buzzword in self.hollow_buzzwords:
            if buzzword in text_lower:
                buzzword_count += 1
                evidence['hollow_buzzwords_found'].append(buzzword)
        
        buzzword_ratio = buzzword_count / max(1, word_count)
        
        # Also check vague phrases
        vague_phrase_count = 0
        for phrase_pattern in self.vague_phrases:
            if re.search(phrase_pattern, text_lower):
                vague_phrase_count += 1
        
        if buzzword_ratio > 0.15 or vague_phrase_count >= 2:  # >15% buzzwords
            penalties['vagueness'] = 0.35
        elif buzzword_ratio > 0.1 or vague_phrase_count >= 1:
            penalties['vagueness'] = 0.2
        elif buzzword_ratio > 0.05:
            penalties['vagueness'] = 0.1
        
        # ================================================================
        # CHECK 3: FALSE CAUSALITY (domain mixing)
        # ================================================================
        
        # Extract causal claims
        causal_claims = []
        for pattern in self.causal_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                causal_claims.append(match.group(0))
        
        # Check forbidden cross-domain causality
        false_causal_count = 0
        for source_domain, target_domain, pattern in self.forbidden_causality:
            if re.search(pattern, text_lower):
                false_causal_count += 1
                evidence['false_causal_claims'].append(f'{source_domain}→{target_domain}')
        
        # Check ontological category errors
        for pattern in self.ontological_errors:
            if re.search(pattern, text_lower):
                false_causal_count += 1
                evidence['false_causal_claims'].append('ontological_error')
        
        if false_causal_count >= 3:
            penalties['false_causality'] = 0.5
        elif false_causal_count >= 2:
            penalties['false_causality'] = 0.35
        elif false_causal_count >= 1:
            penalties['false_causality'] = 0.2
        
        # ================================================================
        # CHECK 4: UNFALSIFIABLE (cannot be proven/disproven)
        # ================================================================
        
        unfalsifiable_count = 0
        for pattern in self.unfalsifiable_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                unfalsifiable_count += len(matches)
                evidence['unfalsifiable_claims'].extend(matches[:3])  # max 3
        
        if unfalsifiable_count >= 3:
            penalties['unfalsifiable'] = 0.25
        elif unfalsifiable_count >= 2:
            penalties['unfalsifiable'] = 0.15
        elif unfalsifiable_count >= 1:
            penalties['unfalsifiable'] = 0.08
        
        # ================================================================
        # AGGREGATE VOID SCORE
        # ================================================================
        
        void_score = (
            penalties['absence'] * 0.25 +
            penalties['vagueness'] * 0.35 +
            penalties['false_causality'] * 0.30 +
            penalties['unfalsifiable'] * 0.10
        )
        
        # BONUS: if text has NO concrete markers AND high buzzwords
        if missing_count >= 4 and buzzword_count >= 5:
            void_score += 0.2  # pure semantic void
        
        void_score = min(1.0, void_score)
        
        return {
            'void_score': round(void_score, 3),
            'penalties': penalties,
            'evidence': evidence,
            'concrete_found': concrete_found,
            'buzzword_count': buzzword_count,
            'buzzword_ratio': round(buzzword_ratio, 3),
            'causal_claims_found': len(causal_claims),
            'false_causality_count': false_causal_count,
        }
