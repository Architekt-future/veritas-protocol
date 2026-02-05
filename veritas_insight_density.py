"""
Veritas Insight Density Detector v1.0
Measures: "How much concrete information per unit of linguistic complexity?"
Philosophy: "Complexity without insight is intellectual masturbation"
"""

import re
from typing import Dict, List
from collections import Counter


class InsightDensityDetector:
    """
    Detects texts that are complex but empty
    Formula: INSIGHT = concrete_facts / linguistic_complexity
    
    High complexity + Low facts = КАЗУЇСТИКА (casuistry)
    """
    
    def __init__(self):
        # ================================================================
        # CONCRETE FACTS (numerator)
        # ================================================================
        
        # Things that carry actual information
        self.concrete_markers = {
            'numbers': r'\d+(?:[.,]\d+)?(?:\s*%)?',
            'dates': r'\d{1,2}\s+(січня|лютого|березня|квітня|травня|червня|липня|серпня|вересня|жовтня|листопада|грудня)|\d{4}\s*рок',
            'years': r'\b(19|20)\d{2}\b',
            'specific_amounts': r'\d+\s*(мільйон|мільярд|тисяч|відсотк)',
            'names': r'\b[А-ЯІЇЄҐ][а-яіїєґ]+\s+[А-ЯІЇЄҐ][а-яіїєґ]+\b',
            'locations': r'\b(київ|україн|львів|одес|харків|дніпро|європ|сша|росі|китай|німеч|франці|польщ)\w*\b',
            'organizations': r'\b(ООН|НАТО|ЄС|UNESCO|WHO|NASA|ООН)\b',
            'specific_actions': r'\b(побудував|створив|винайшов|виміряв|зафіксував|опублікував|підписав|прийняв)\w*\b',
            'verifiable_sources': r'\b(університет|інститут|дослідження|експеримент|публікація|журнал|стаття)\w*\b',
        }
        
        # ================================================================
        # LINGUISTIC COMPLEXITY (denominator)
        # ================================================================
        
        # Rare/complex words that increase cognitive load
        self.complexity_markers = {
            # Abstract academic terminology (using stems for Ukrainian)
            'abstract_nouns': [
                'парадигм', 'контекст', 'аспект', 'фактор', 'компонент',
                'структур', 'систем', 'механізм', 'процес', 'динамік',
                'специфік', 'характеристик', 'модель', 'концепц',
            ],
            
            # Bureaucratic language (stems)
            'bureaucratic': [
                'імплементац', 'оптимізац', 'консолідац', 'інтеграц',
                'децентралізац', 'синхронізац', 'координац', 'регламентац',
                'моніторинг', 'валідац', 'верифікац', 'детермінац',
                'трансформац',  # transformation
            ],
            
            # Compound technical terms
            'compound_terms': [
                'мультифакторн', 'багатокомпонентн', 'полівалентн',
                'системно-структурн', 'функціонально-динамічн',
                'комплексно-інтегрован', 'багаторівнев',
            ],
            
            # Geopolitical jargon (stems)
            'geopolitical': [
                'геополітичн', 'транснаціональн', 'міждержавн',
                'багатополярн', 'гегемоністичн', 'деескалац',
                'взаємозалежн', 'інерційн', 'проліферац', 'нерозповсюдж',
                'логістичн',  # logistical chains
            ],
            
            # Pseudo-intellectual markers
            'pseudo_intellectual': [
                'дискурсивн', 'наративн', 'рефлексивн', 'транзитивн',
                'холістичн', 'синергетичн', 'емерджентн',
            ],
        }
        
        # Long compound words (>15 chars) add complexity
        self.long_word_threshold = 15
        
        # ================================================================
        # CASUISTRY PATTERNS (specific empty phrases)
        # ================================================================
        
        self.empty_phrases = [
            r'в контексті',
            r'з урахуванням',
            r'у світлі',
            r'в межах',
            r'на тлі',
            r'в рамках',
            r'з точки зору',
            r'в аспекті',
            r'у площині',
            r'в парадигмі',
            r'в ракурсі',
        ]

    def analyze(self, text: str) -> Dict:
        """
        Returns insight density score (0.0-1.0)
        Higher = more insight per complexity
        Lower = casuistry (empty complexity)
        """
        if len(text) < 50:
            return {'insight_density': 0.5, 'reason': 'text_too_short'}
        
        text_lower = text.lower()
        words = text.split()
        word_count = len(words)
        
        # ================================================================
        # COUNT CONCRETE FACTS
        # ================================================================
        
        fact_count = 0
        found_facts = []
        
        for fact_type, pattern in self.concrete_markers.items():
            matches = re.findall(pattern, text_lower)
            if matches:
                fact_count += len(matches)
                found_facts.append(f"{fact_type}:{len(matches)}")
        
        # ================================================================
        # COUNT LINGUISTIC COMPLEXITY
        # ================================================================
        
        complexity_count = 0
        
        # 1. Complex terminology
        for category, terms in self.complexity_markers.items():
            for term in terms:
                if term in text_lower:
                    complexity_count += 1
        
        # 2. Long compound words
        long_words = [w for w in words if len(w) > self.long_word_threshold]
        complexity_count += len(long_words)
        
        # 3. Empty connecting phrases
        empty_phrase_count = 0
        for phrase in self.empty_phrases:
            matches = re.findall(phrase, text_lower)
            empty_phrase_count += len(matches)
        
        complexity_count += empty_phrase_count
        
        # 4. Average sentence length (long sentences = complex)
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        if sentences:
            avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
            if avg_sentence_length > 20:  # Long sentences
                complexity_count += int(avg_sentence_length / 5)
        
        # ================================================================
        # CALCULATE INSIGHT DENSITY
        # ================================================================
        
        # Normalize counts
        fact_density = fact_count / max(1, word_count)  # facts per word
        complexity_density = complexity_count / max(1, word_count)  # complexity per word
        
        # INSIGHT = facts / complexity
        if complexity_density > 0:
            insight_density = fact_density / complexity_density
        else:
            insight_density = fact_density * 2  # No complexity = good if has facts
        
        # Normalize to 0-1 range
        insight_density = min(1.0, insight_density)
        
        # ================================================================
        # CLASSIFY
        # ================================================================
        
        # High complexity + Low facts = CASUISTRY
        is_casuistry = (complexity_density > 0.15 and fact_density < 0.05)
        
        # Calculate casuistry score (inverse of insight)
        casuistry_score = 0.0
        if is_casuistry:
            casuistry_score = complexity_density * 2.0  # Penalize complexity without facts
            casuistry_score = min(1.0, casuistry_score)
        
        return {
            'insight_density': round(insight_density, 3),
            'casuistry_score': round(casuistry_score, 3),
            'fact_count': fact_count,
            'fact_density': round(fact_density, 3),
            'complexity_count': complexity_count,
            'complexity_density': round(complexity_density, 3),
            'empty_phrases': empty_phrase_count,
            'is_casuistry': is_casuistry,
            'found_facts': found_facts,
        }
