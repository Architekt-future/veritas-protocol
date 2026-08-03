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
        # ENGLISH MARKERS
        # ================================================================

        self.complexity_markers_en = {
            'abstract_nouns': [
                'paradigm', 'context', 'aspect', 'factor', 'component',
                'framework', 'mechanism', 'dynamic', 'dimension',
                'characteristic', 'model', 'concept', 'perspective',
                'narrative', 'discourse', 'architecture', 'ecosystem',
            ],
            'bureaucratic': [
                'implementation', 'optimization', 'consolidation', 'integration',
                'synchronization', 'coordination', 'transformation', 'validation',
                'monetization', 'operationalization', 'systematization',
                'prioritization', 'institutionalization',
            ],
            'pseudo_intellectual': [
                'holistic', 'synergistic', 'emergent', 'reflexive',
                'dialectical', 'epistemological', 'ontological', 'paradigmatic',
                'multifaceted', 'multidimensional', 'nuanced',
            ],
            'geopolitical': [
                'geopolitical', 'transnational', 'multilateral', 'hegemonic',
                'deescalation', 'interdependence', 'proliferation',
                'multipolar', 'asymmetric',
            ],
        }

        # ================================================================
        # CASUISTRY PATTERNS — ENGLISH
        # ================================================================

        # Hedging без змісту
        self.hedging_en = [
            r"it could be argued",
            r"one might suggest",
            r"in some ways",
            r"to some extent",
            r"to a certain degree",
            r"in a sense",
            r"arguably",
            r"it can be said",
            r"some would say",
            r"it is possible that",
            r"there is reason to believe",
            r"it seems that",
            r"it appears that",
        ]

        # Circular reasoning
        self.circular_en = [
            r"the reason (?:is|was) (?:due to|because of) the",
            r"(?:important|significant|relevant) because (?:it|they) (?:matter|is important|are significant)",
            r"by (?:its|their|the) very nature",
            r"in and of itself",
            r"speaks for itself",
            r"self-evident",
            r"goes without saying",
        ]

        # Vague quantity замість цифр
        self.vague_quantity_en = [
            r"\bmany (?:people|experts|studies|countries|cases)\b",
            r"\bsome (?:argue|suggest|believe|claim|say)\b",
            r"\ba number of\b",
            r"\bvarious (?:factors|reasons|sources|experts)\b",
            r"\bseveral (?:factors|reasons|experts|studies)\b",
            r"\bcountless\b",
            r"\bnumerous (?:studies|experts|factors|cases)\b",
            r"\bsome experts\b",
            r"\bmany analysts\b",
        ]

        # False precision
        self.false_precision_en = [
            r"arguably (?:the most|one of the most)",
            r"perhaps (?:the greatest|the most|the biggest)",
            r"one of the (?:most|greatest|biggest|key|main)",
            r"(?:the|a) key (?:factor|issue|challenge|question|aspect)",
            r"(?:the|a) central (?:question|issue|challenge|theme)",
            r"(?:the|a) fundamental (?:question|issue|challenge|problem)",
            r"(?:the|a) critical (?:factor|issue|challenge|moment)",
        ]

        # Momentum — замість доказів
        self.momentum_en = [
            r"it is (?:clear|obvious|evident|apparent) that",
            r"obviously\b",
            r"as (?:we all|everyone) know",
            r"undoubtedly\b",
            r"certainly\b",
            r"without (?:a )?doubt\b",
            r"it goes without saying",
            r"(?:clearly|plainly|simply) put",
            r"make no mistake",
            r"the fact (?:is|remains) that",
            r"the truth (?:is|remains) that",
            r"needless to say\b",
        ]

        # ================================================================
        # CASUISTRY PATTERNS — UKRAINIAN
        # ================================================================

        # Hedging без змісту
        self.hedging_uk = [
            r"можна стверджувати",
            r"певною мірою",
            r"в певному сенсі",
            r"деякою мірою",
            r"є підстави вважати",
            r"схоже (?:на те )?що",
            r"здається що",
            r"дехто міг би сказати",
            r"це можна розглядати як",
            r"у певному розумінні",
        ]

        # Circular reasoning
        self.circular_uk = [
            r"причина (?:полягає|криється) в (?:самій|тому що)",
            r"важливо тому що (?:це|воно) важлив",
            r"за своєю природою",
            r"само по собі",
            r"говорить само за себе",
            r"само собою зрозуміло",
            r"не потребує пояснень",
        ]

        # Vague quantity
        self.vague_quantity_uk = [
            r"багато (?:людей|експертів|досліджень|країн)",
            r"деякі (?:стверджують|вважають|говорять|кажуть)",
            r"ряд (?:факторів|причин|експертів|досліджень)",
            r"різні (?:фактори|причини|джерела|експерти)",
            r"численні (?:дослідження|факти|докази|експерти)",
            r"багато аналітиків",
            r"деякі експерти",
            r"чимало (?:людей|фахівців)",
        ]

        # False precision
        self.false_precision_uk = [
            r"(?:мабуть|мабуть) (?:найбільш|найважливіш)",
            r"один із (?:найбільш|найважливіш|ключових|головних)",
            r"(?:ключовий|головний|центральний|фундаментальний) (?:фактор|питання|виклик|аспект|момент)",
            r"(?:критичний|вирішальний) (?:фактор|момент|питання)",
            r"(?:найважливіш|найголовніш)\w+ питання",
        ]

        # Momentum
        self.momentum_uk = [
            r"(?:зрозуміло|очевидно|ясно) що",
            r"як (?:всі|усі|ми всі) знають",
            r"безсумнівно\b",
            r"безперечно\b",
            r"немає сумніву",
            r"не викликає сумніву",
            r"цілком (?:зрозуміло|очевидно)",
            r"нема чого й казати",
            r"факт залишається фактом",
            r"правда (?:полягає|в тому) що",
        ]

        self.empty_phrases_en = [
            r'in the context of',
            r'in terms of',
            r'with respect to',
            r'in light of',
            r'in the realm of',
            r'in the framework of',
            r'from the perspective of',
            r'in the wake of',
            r'at the end of the day',
            r'going forward',
            r'it is worth noting',
            r'it is important to note',
            r'needless to say',
            r'by the same token',
            r'in this regard',
        ]

        self.concrete_markers_en = {
            'numbers': r'\d+(?:[.,]\d+)?(?:\s*%)?',
            'years': r'\b(19|20)\d{2}\b',
            'specific_amounts': r'\d+\s*(million|billion|thousand|percent|trillion)',
            'names': r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b',
            'locations': r'\b(united states|europe|china|russia|ukraine|washington|new york|london|brussels)\b',
            'organizations': r'\b(UN|NATO|EU|UNESCO|WHO|NASA|FBI|CIA|IMF|WTO|Census Bureau)\b',
            'specific_actions': r'\b(built|created|invented|measured|recorded|published|signed|passed|launched|founded)\b',
            'verifiable_sources': r'\b(university|institute|study|research|experiment|publication|journal|report|data|survey)\b',
            'dates': r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2}\b',
        }
        
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

        # 'names' та 'organizations' вимагають великих літер (власні назви,
        # абревіатури типу NATO/ООН) — їх треба звіряти з ОРИГІНАЛЬНИМ текстом,
        # бо проти text_lower (де регістр вже знищено) вони НІКОЛИ не спрацюють.
        CASE_SENSITIVE_TYPES = {'names', 'organizations'}

        for fact_type, pattern in self.concrete_markers.items():
            source = text if fact_type in CASE_SENSITIVE_TYPES else text_lower
            matches = re.findall(pattern, source)
            if matches:
                fact_count += len(matches)
                found_facts.append(f"{fact_type}:{len(matches)}")
        for fact_type, pattern in self.concrete_markers_en.items():
            source = text if fact_type in CASE_SENSITIVE_TYPES else text_lower
            matches = re.findall(pattern, source)
            if matches:
                fact_count += len(matches)
                found_facts.append(f"en_{fact_type}:{len(matches)}")
        
        # ================================================================
        # COUNT LINGUISTIC COMPLEXITY
        # ================================================================
        
        complexity_count = 0
        
        # 1. Complex terminology
        # UK-основи навмисно "обрізані" (щоб ловити відмінкові форми),
        # тому \b лише на початку. EN — повні слова, \b з обох боків,
        # інакше 'factor' ловиться всередині 'satisfactory', 'concept' —
        # всередині 'misconception', 'model' — всередині 'remodeling'.
        for category, terms in self.complexity_markers.items():
            for term in terms:
                if re.search(r'\b' + re.escape(term), text_lower):
                    complexity_count += 1

        # 1b. English complexity markers
        for category, terms in self.complexity_markers_en.items():
            for term in terms:
                if re.search(r'\b' + re.escape(term) + r'\b', text_lower):
                    complexity_count += 1

        # 2. Long compound words
        long_words = [w for w in words if len(w) > self.long_word_threshold]
        complexity_count += len(long_words)
        
        # 3. Empty connecting phrases
        empty_phrase_count = 0
        for phrase in self.empty_phrases:
            matches = re.findall(phrase, text_lower)
            empty_phrase_count += len(matches)
        for phrase in self.empty_phrases_en:
            matches = re.findall(phrase, text_lower)
            empty_phrase_count += len(matches)

        # Нові казуїстичні патерни EN
        casuistry_lists_en = [
            self.hedging_en, self.circular_en, self.vague_quantity_en,
            self.false_precision_en, self.momentum_en,
        ]
        for pattern_list in casuistry_lists_en:
            for phrase in pattern_list:
                matches = re.findall(phrase, text_lower)
                empty_phrase_count += len(matches)

        # Нові казуїстичні патерни UK
        casuistry_lists_uk = [
            self.hedging_uk, self.circular_uk, self.vague_quantity_uk,
            self.false_precision_uk, self.momentum_uk,
        ]
        for pattern_list in casuistry_lists_uk:
            for phrase in pattern_list:
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
