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
            
            # Mystical/Conspiracy hollow (NEW)
            'перезавантаження', 'велике пробудження', 'ментальний сон', 'прокинувся',
            'справжня реальність', 'приховане знання', 'таємні сили', 'невидимі нитки',
            'велика гра', 'маріонетки', 'хазяї', 'завіса', 'матриця',
            'системний збій', 'глибинна держава', 'плани еліт', 'справжня правда',
            'відкриті очі', 'бачать ті хто', 'знають ті хто', 'розуміють лише',
            
            # Generic hollow — ONLY truly hollow variants, not neutral words
            # REMOVED: 'можливість', 'потенціал', 'аспект', 'фактор', 'компонент',
            # 'елемент', 'процес', 'структура', 'система', 'механізм', 'динаміка', 'контекст'
            # These are standard neutral vocabulary, not buzzwords!
            'ціннісні можливості', 'потенціал трансформації',

            # Corporate/institutional hollow (NEW v1.1)
            'адаптивність', 'адаптивн', 'інституційн', 'інституції',
            'операційн', 'стратегічн', 'стратегічними намірами',
            'управлінськ', 'координац', 'міжсекторальн',
            'екосистемн', 'екосистема змін', 'довгостроков',
            'трансформаційн', 'реконфігурац', 'проактивн',
            'саморефлексі', 'інтеграц', 'цілісне бачення',
            'стейкхолдер', 'бенчмаркінг', 'коучинг змін',
            'фасилітац', 'модерац процесу',

            # FALSE_INEVITABILITY markers (NEW v1.1)
            # "неминуче" само по собі не buzzword, але в поєднанні з відсутністю фактів — порожнеча
            'є неминучим', 'стало неминучим', 'лише відтерміновує',
            'повернення неможливе', 'практично неможливе',
            'питання часу', 'лише питання часу',

            # MANUFACTURED_CONSENSUS markers (NEW v1.1)
            'дедалі більше аналітиків', 'дедалі більше дослідників',
            'більшість досліджень свідчить', 'більшість експертів вважає',
            'сходяться на думці', 'загальновизнано', 'загальноприйнято',
            'деякі дослідники оцінюють', 'деякі аналітики навіть',
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
        # NOTE: Factual/scientific texts often lack names/locations but have 
        # concrete causal structure — only penalize if also high buzzwords
        missing_count = len(evidence['missing_concrete'])
        buzzword_count_check = sum(1 for bw in self.hollow_buzzwords if bw in text_lower)
        
        # Only apply heavy absence penalty if ALSO high buzzwords (real emptiness)
        if missing_count >= 5 and buzzword_count_check >= 3:
            penalties['absence'] = 0.7
        elif missing_count >= 5:
            penalties['absence'] = 0.2  # factual text without metadata is OK
        elif missing_count >= 3 and buzzword_count_check >= 2:
            penalties['absence'] = 0.4
        elif missing_count >= 3:
            penalties['absence'] = 0.1  # factual abstract text
        elif missing_count >= 2:
            penalties['absence'] = 0.05
        
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
            penalties['vagueness'] = 0.6  # was 0.35
        elif buzzword_ratio > 0.1 or vague_phrase_count >= 1:
            penalties['vagueness'] = 0.4  # was 0.2
        elif buzzword_ratio > 0.05:
            penalties['vagueness'] = 0.2  # was 0.1
        
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
        # PURE SEMANTIC VOID = intentional destruction of meaning
        if missing_count >= 4 and buzzword_count >= 5:
            void_score += 0.4  # was 0.2 - now can reach 0.9+!
        
        # GEMINI'S ACTIVE VOID SLASHING (REFINED v13.9 → v13.10)
        # If 30+ words but NO numbers/dates → check if also bullshit
        if word_count >= 30:
            has_numbers = concrete_found.get('numbers', 0) > 0
            has_dates = concrete_found.get('dates', 0) > 0
            
            if not has_numbers and not has_dates:
                # REFINEMENT v13.10: Stricter threshold
                # Philosophy/science/logic without numbers is OK if not bullshit
                # Only penalize if >15% buzzwords (was >10%)
                if buzzword_ratio > 0.15:  # clearly bullshit
                    void_score += 0.3  # semantic fraud confirmed
                    evidence['missing_concrete'].append('CRITICAL: no facts + high buzzwords')
                elif buzzword_ratio > 0.08:  # marginal
                    void_score += 0.05  # very gentle penalty
                    evidence['missing_concrete'].append('Abstract: moderate buzzwords, no numbers')
        
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
