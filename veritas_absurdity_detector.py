"""
Veritas Absurdity Detector v1.0
Detects logical non-sequiturs and semantic collapse
Philosophy: "When premises and conclusions live in different universes"
"""

import re
from typing import Dict, List, Tuple


class AbsurdityDetector:
    """
    Detects three types of absurdity:
    1. PREMISE-CONCLUSION MISMATCH (A → B where A and B are logically unrelated)
    2. FABRICATED AUTHORITY (impossible sources, secret documents)
    3. DANGEROUS IMPLICATIONS (self-harm, medical denial, destructive actions)
    """
    
    def __init__(self):
        # ================================================================
        # TYPE 1: PREMISE-CONCLUSION MISMATCH
        # ================================================================
        
        # Mundane facts used to justify absurd conclusions
        self.mundane_premises = [
            r'вода кипить',
            r'сонце сходить',
            r'два плюс два',
            r'\d+\s*градус',
            r'фундаментальн.{1,20}істин',
            r'очевидн.{1,20}факт',
        ]
        
        # Absurd/extreme conclusions
        self.absurd_conclusions = [
            r'передати.{1,60}(ядерн|арсенал|зброї)',
            r'(знищити|дестабілізац|колапс).{1,60}(енергомереж|систем|інфраструктур)',
            r'відмов.{1,60}від\s+(дихання|їж|води|медицин)',
            r'антигравітаційн.{1,20}килим',
            r'деконструюва.{1,60}(гравітац|фізик)',
        ]
        
        # Logical operators that claim causation
        self.causal_operators = [
            r'враховуючи',
            r'оскільки',
            r'тому',
            r'це означає',
            r'звідси випливає',
            r'отже',
        ]
        
        # ================================================================
        # TYPE 2: FABRICATED AUTHORITY
        # ================================================================
        
        self.fabricated_authorities = [
            # Impossible historical sources
            r'(секретн|прихован|заборонен).{1,40}(прац|текст|рукопис).{1,60}(арістотел|платон|сократ)',
            r'(арістотел|платон).{1,60}(біткоїн|блокчейн|5g|інтернет|ai)',
            r'леонардо да вінчі.{1,60}(креслен|схем).{1,60}(біткоїн|криптовалют)',
            
            # Impossible modern sources
            r'(дослідження|звіт).{1,60}(наса|цру|пентагон).{1,60}(грифом|секретн|класифіков)',
            r'комітет.{1,60}(моніторинг|контрол).{1,60}(ноосфер|астрал|ефір)',
            r'міністерство.{1,60}(ефірн|астральн|енергетичн|вібраційн)',
            
            # Government pseudoscience
            r'(урядов|державн).{1,60}(постанов|декрет|указ).{1,60}(алхімічн|езотеричн|астральн)',
            r'(міністерство|відомство).{1,60}(гомеопатичн|ефірн|вібраційн)',
            
            # Conspiracy entities
            r'(військов|армі|спецслужб).{1,60}(рептилоїд|інопланетян|грей)',
            r'(білл|гейтс|сорос|ілон|маск).{1,60}(чіп|мікрочіп|контрол|змов)',
            r'(5g|6g).{1,60}(чіп|контрол|активац).{1,60}(мозк|зуб|тіл)',
            
            # Fictional transmission methods
            r'(отримав|передав).{1,60}(ментальн|телепатичн).{1,60}(канал|зв.язок)',
            r'(цивілізація|раса).{1,60}(сіріус|плеяд|альфа центавр|андромед)',
            
            # Pseudoscientific institutions
            r'інститут.{1,60}(квантов.{1,20}свідом|ефірн|торсійн)',
        ]
        
        # ================================================================
        # TYPE 3: DANGEROUS IMPLICATIONS
        # ================================================================
        
        self.dangerous_patterns = [
            # Direct harm
            r'відмов.{1,60}від\s+дихання',
            r'припинення\s+(дихання|серцебиття)',
            r'смерть.{1,60}(раціональн|логік|розум).{1,60}(народження|шлях|свобод)',
            
            # Medical denial
            r'відмов.{1,60}від.{1,60}(лікування|медицин|вакцин|терапі)',
            r'(ліки|препарат|вакцин).{1,60}(отрут|шкід|вбива)',
            
            # Violent/destructive actions
            r'(знищити|зруйнува|підірва).{1,60}(вежі|станц|мереж|систем)',
            r'(напад|атак|саботаж).{1,60}(інфраструктур|об.єкт)',
            
            # Surrender of agency to AI/external control
            r'делегува.{1,60}(всі|повн).{1,60}(рішення|контроль|влад).{1,60}(ai|штучн.{1,20}інтелект)',
            r'(ai|нейромереж).{1,60}(випадков.{1,20}числ|хаос).{1,60}(ядерн|зброї|арсенал)',
        ]
        
        # ================================================================
        # TYPE 4: ONTOLOGICAL CATEGORY COLLAPSE
        # ================================================================
        
        self.category_collapse = [
            # Physical laws as social constructs
            r'(гравітація|електромагнетизм|термодинаміка).{1,80}соціальн.{1,20}конструкт',
            r'(фізичн.{1,20}закон|гравітац).{1,60}(догм|віра|нав.яза)',
            
            # Consciousness controlling physics
            r'(свідомість|віра|думк).{1,60}(об.єкти|тіла).{1,60}(падають|рухають)',
            r'колективн.{1,20}свідом.{1,60}(протокол|погодж).{1,60}(гравітац|фізик)',
            
            # Abstract concepts as physical entities
            r'(істина|правда).{1,60}(гнучк|адаптується|змінюється)',
            r'ілюзія.{1,60}(маса|вага|енергія)',
        ]

    def analyze(self, text: str) -> Dict:
        """
        Returns absurdity score (0.0-1.0)
        Higher = more absurd
        """
        if len(text) < 30:
            return {'absurdity_score': 0.0, 'reason': 'text_too_short'}
        
        text_lower = text.lower()
        
        absurdity_score = 0.0
        evidence = {
            'premise_conclusion_mismatch': [],
            'fabricated_authorities': [],
            'dangerous_implications': [],
            'category_collapse': [],
        }
        
        # ================================================================
        # CHECK 1: PREMISE-CONCLUSION MISMATCH
        # ================================================================
        
        # Look for mundane premise + absurd conclusion pattern
        has_mundane = False
        has_absurd = False
        has_causal = False
        
        for premise_pattern in self.mundane_premises:
            if re.search(premise_pattern, text_lower):
                has_mundane = True
                break
        
        for conclusion_pattern in self.absurd_conclusions:
            if re.search(conclusion_pattern, text_lower):
                has_absurd = True
                evidence['premise_conclusion_mismatch'].append(conclusion_pattern[:40])
        
        for operator in self.causal_operators:
            if re.search(operator, text_lower):
                has_causal = True
                break
        
        # If mundane + causal operator + absurd conclusion = non-sequitur
        if has_mundane and has_causal and has_absurd:
            absurdity_score += 0.6  # SEVERE: logical non-sequitur
        elif has_absurd:
            absurdity_score += 0.3  # MODERATE: absurd claim without premise
        
        # ================================================================
        # CHECK 2: FABRICATED AUTHORITY
        # ================================================================
        
        fabrication_count = 0
        for pattern in self.fabricated_authorities:
            if re.search(pattern, text_lower):
                fabrication_count += 1
                evidence['fabricated_authorities'].append(pattern[:50])
        
        if fabrication_count >= 2:
            absurdity_score += 0.5  # Multiple impossible sources
        elif fabrication_count == 1:
            absurdity_score += 0.3
        
        # ================================================================
        # CHECK 3: DANGEROUS IMPLICATIONS
        # ================================================================
        
        danger_count = 0
        for pattern in self.dangerous_patterns:
            if re.search(pattern, text_lower):
                danger_count += 1
                evidence['dangerous_implications'].append(pattern[:50])
        
        if danger_count >= 2:
            absurdity_score += 0.7  # CRITICAL: multiple dangerous claims
        elif danger_count == 1:
            absurdity_score += 0.4
        
        # ================================================================
        # CHECK 4: CATEGORY COLLAPSE
        # ================================================================
        
        collapse_count = 0
        for pattern in self.category_collapse:
            if re.search(pattern, text_lower):
                collapse_count += 1
                evidence['category_collapse'].append(pattern[:50])
        
        if collapse_count >= 2:
            absurdity_score += 0.5
        elif collapse_count == 1:
            absurdity_score += 0.3
        
        # ================================================================
        # AGGREGATE
        # ================================================================
        
        absurdity_score = min(1.0, absurdity_score)
        
        return {
            'absurdity_score': round(absurdity_score, 3),
            'evidence': evidence,
            'has_non_sequitur': has_mundane and has_causal and has_absurd,
            'fabrication_count': fabrication_count,
            'danger_count': danger_count,
            'collapse_count': collapse_count,
        }
