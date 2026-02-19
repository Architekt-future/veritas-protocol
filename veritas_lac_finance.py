"""
Veritas LAC — Finance Edition v1.0
Logic Authenticity Check for Financial Narratives

Purpose:
Detects imitation of logic in financial statements by testing:
1. Explicit trade-offs (V ≠ L calculus)
2. Causal closure (observable → consequence chains)
3. Accountability linkage (who is responsible)
4. Procedural blocking power (emergency brake mechanisms)

This is NOT a market predictor.
This is a structural verifier.

Philosophy:
"A financial claim without downside disclosure is a semantic hologram."
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
import re


@dataclass
class LACFinanceResult:
    """Result of LAC Finance analysis"""
    score: float              # 0.0-1.0 (percentage of criteria met)
    verdict: str              # OPERATIVE / FRAGILE / IMITATION
    missing: List[str]        # Which criteria failed
    evidence: Dict[str, List[str]]  # What was found/missing
    financial_domain: bool    # Is this actually financial content?
    
    def __repr__(self):
        return f"LACFinanceResult(score={self.score:.2f}, verdict='{self.verdict}', missing={self.missing})"


class VeritasLACFinance:
    """
    LAC Finance Module
    
    Tests financial narratives for logical authenticity through 4 criteria:
    
    1. EXPLICIT TRADEOFF (V ≠ L)
       - Downside/risk disclosure
       - Cost acknowledgment
       - Volatility admission
       
    2. CAUSAL CHAIN
       - Observable cause → measurable effect
       - Testable predictions
       - Falsifiable claims
       
    3. ACCOUNTABILITY
       - Named decision-makers
       - Liability assignment
       - Responsibility anchoring
       
    4. BLOCKING POWER
       - Emergency halt mechanisms
       - Circuit breakers
       - Stop-loss systems
    """
    
    def __init__(self):
        # ============================================================
        # CRITERION 1: EXPLICIT TRADEOFF (V ≠ L calculus)
        # ============================================================
        self.tradeoff_markers = {
            'downside_explicit': [
                r'\bриз(ик|ику|ків)\b',
                r'\bвтрат(и|а|ам)\b',
                r'\bзбитк(и|ів|ах)\b',
                r'\bdownside\b',
                r'\bпадінн(я|ям|і)\b',
                r'\bволатильн(ість|ості)\b',
                r'\bvolatility\b',
                r'\bdrawdown\b',
                r'\bmax(imum)?\s+loss\b',
            ],
            'cost_acknowledgment': [
                r'\bвартіст(ь|ю|і)\b',
                r'\bкомісі(я|ї|єю)\b',
                r'\bcost\b',
                r'\bfee(s)?\b',
                r'\bexpense(s)?\b',
                r'\bat\s+the\s+expense\s+of\b',
                r'\bв\s+обмін\s+на\b',
            ],
            'tradeoff_explicit': [
                r'trade[\s-]?off',
                r'\bкомпроміс\b',
                r'\bобмін\b',
                r'\bin\s+exchange\s+for\b',
                r'\bна\s+противагу\b',
            ]
        }
        
        # Anti-patterns (red flags for zero-cost propositions)
        self.zero_cost_red_flags = [
            r'гарантован[а-яіїє\']*\s+(прибуток|дохід|зростання|успіх)',
            r'без\s+(ризик|втрат|збитк)',
            r'захищен[а-яіїє\']*\s+від\s+(втрат|падіння|крах)',
            r'тільки\s+(в\s+)?плюс',
            r'не\s+може\s+(впасти|знизитись)',
            r'(абсолютно|повністю)\s+безпечн',
            r'zero[\s-]?risk',
            r'no[\s-]?downside',
            r'only\s+upside',
        ]
        
        # ============================================================
        # CRITERION 2: CAUSAL CHAIN
        # ============================================================
        self.causal_markers = {
            'explicit_causation': [
                r'\bтому\s+що\b',
                r'\bоскільки\b',
                r'\bбо\b',
                r'\bоскільк\b',
                r'\bbecause\b',
                r'\bсінсе\b',
                r'\bas\s+a\s+result\b',
            ],
            'consequence': [
                r'\bпризводить\s+до\b',
                r'\bспричиня(є|ють)\b',
                r'\bрезультує\b',
                r'\bleads?\s+to\b',
                r'\bcauses?\b',
                r'\bresults?\s+in\b',
                r'\bвідповідно\b',
                r'\bтаким\s+чином\b',
            ],
            'testable_prediction': [
                r'\bочікуємо\b',
                r'\bпрогнозуємо\b',
                r'\bпередбачаємо\b',
                r'\bякщо.*то\b',
                r'\bif.*then\b',
                r'\bexpect\b',
                r'\bforecast\b',
                r'\bpredict\b',
            ]
        }
        
        # ============================================================
        # CRITERION 3: ACCOUNTABILITY
        # ============================================================
        self.accountability_markers = {
            'named_responsibility': [
                r'\bми\s+(відповідальні|зобов\'язуємось|гарантуємо)\b',
                r'\bфонд\s+(відповідає|зобов\'язаний)\b',
                r'\bменеджмент\s+(несе\s+відповідальність|приймає\s+рішення)\b',
                r'\bwe\s+(are\s+responsible|commit|guarantee)\b',
                r'\bthe\s+fund\s+(commits|is\s+liable)\b',
                r'\bmanagement\s+decision\b',
            ],
            'liability': [
                r'\bвідповідальніст(ь|ю|і)\b',
                r'\bзобов\'язан(ня|ь)\b',
                r'\bliability\b',
                r'\baccountable\b',
                r'\bповноваження\b',
            ],
            'issuer_identity': [
                r'\bемітент\b',
                r'\bуправител(ь|я)\b',
                r'\bissuer\b',
                r'\btrustee\b',
                r'\bcustodian\b',
            ]
        }
        
        # Anti-patterns (responsibility diffusion)
        self.responsibility_diffusion = [
            r'минулі\s+результати\s+не\s+гарантують',
            r'past\s+performance.*not.*guarantee',
            r'зверніться\s+до\s+(свого\s+)?радника',
            r'consult.*advisor',
            r'ринок\s+може\b',
            r'market\s+may\b',
            r'ніхто\s+не\s+може\s+передбачити',
            r'nobody\s+can\s+predict',
        ]
        
        # ============================================================
        # CRITERION 4: BLOCKING POWER (Procedural Interdiction)
        # ============================================================
        self.blocking_markers = {
            'circuit_breaker': [
                r'\bhalt\b',
                r'\bзупин(ка|ити|яємо)\b',
                r'\bстоп[\s-]?лос(с|)\b',
                r'\bstop[\s-]?loss\b',
                r'\bcircuit\s+breaker\b',
                r'\btrading\s+halt\b',
                r'\bпризупинен(ня|о)\b',
                r'\bsuspend\s+trading\b',
            ],
            'risk_limit': [
                r'\bліміт\s+риз(ику|ків)\b',
                r'\bмаксимальн(а|ий)\s+(втрата|просідання)\b',
                r'\brisk\s+limit\b',
                r'\bmax(imum)?\s+(loss|drawdown)\b',
                r'\bposition\s+limit\b',
            ],
            'withdrawal_mechanism': [
                r'\bвихід\s+з\s+позиці(ї|єю)\b',
                r'\bвиведення\s+коштів\b',
                r'\bwithdrawal\b',
                r'\bredemption\b',
                r'\bexit\s+strategy\b',
            ]
        }
        
        # ============================================================
        # FINANCIAL DOMAIN DETECTION
        # ============================================================
        self.finance_terms = [
            # Crypto
            'bitcoin', 'btc', 'ethereum', 'eth', 'crypto', 'blockchain',
            'біткоїн', 'біткойн', 'крипто', 'блокчейн',
            
            # Traditional finance
            'etf', 'fund', 'фонд', 'portfolio', 'портфел',
            'investment', 'інвестиці', 'asset', 'актив',
            'stock', 'акці', 'bond', 'облігаці',
            'return', 'дохідність', 'yield', 'прибуток',
            
            # Market terms
            'ринок', 'market', 'trading', 'торгівл',
            'volatility', 'волатильн', 'ліквідн', 'liquidity',
        ]
        
    def analyze(self, text: str) -> LACFinanceResult:
        """
        Main analysis entry point
        
        Returns LACFinanceResult with:
        - score: 0.0-1.0 (percentage of 4 criteria met)
        - verdict: OPERATIVE (1.0) / FRAGILE (0.5-0.75) / IMITATION (<0.5)
        - missing: list of failed criteria
        - evidence: what was found for each criterion
        """
        text_lower = text.lower()
        
        # Check if this is financial content
        is_financial = self._is_financial_content(text_lower)
        
        # Initialize results
        criteria_met = {
            "explicit_tradeoff": False,
            "causal_chain": False,
            "accountability": False,
            "blocking_power": False
        }
        
        evidence = {
            "explicit_tradeoff": [],
            "causal_chain": [],
            "accountability": [],
            "blocking_power": [],
            "red_flags": []
        }
        
        # Test each criterion
        criteria_met["explicit_tradeoff"], evidence["explicit_tradeoff"] = self._test_tradeoff(text_lower)
        criteria_met["causal_chain"], evidence["causal_chain"] = self._test_causality(text_lower)
        criteria_met["accountability"], evidence["accountability"] = self._test_accountability(text_lower)
        criteria_met["blocking_power"], evidence["blocking_power"] = self._test_blocking(text_lower)
        
        # Detect red flags (override tradeoff if found)
        red_flags = self._detect_red_flags(text_lower)
        if red_flags:
            criteria_met["explicit_tradeoff"] = False
            evidence["red_flags"] = red_flags
        
        # Calculate score
        score = sum(criteria_met.values()) / len(criteria_met)
        
        # Identify missing criteria
        missing = [k for k, v in criteria_met.items() if not v]
        
        # Determine verdict
        verdict = self._determine_verdict(score)
        
        return LACFinanceResult(
            score=score,
            verdict=verdict,
            missing=missing,
            evidence=evidence,
            financial_domain=is_financial
        )
    
    def _is_financial_content(self, text: str) -> bool:
        """Check if text is genuinely financial in nature.
        Requires at least 2 finance terms to avoid false positives
        on science, politics, or general news articles.
        """
        # Hard financial indicators — one is enough
        hard_indicators = [
            'bitcoin', 'btc', 'ethereum', 'eth', 'crypto', 'blockchain',
            'біткоїн', 'біткойн', 'крипто', 'блокчейн',
            'etf', 'portfel', 'портфел',
            'trading', 'торгівл',
            'volatility', 'волатильн',
            'stock market', 'фондов', 'біржа', 'exchange rate', 'курс валют',
            'hedge fund', 'хедж фонд', 'dividend', 'дивіденд',
        ]
        for term in hard_indicators:
            if term in text:
                return True

        # Soft financial indicators — need at least 2
        soft_hits = sum(1 for term in self.finance_terms if term in text)
        return soft_hits >= 2
    
    def _test_tradeoff(self, text: str) -> Tuple[bool, List[str]]:
        """Test for explicit trade-off disclosure"""
        evidence = []
        
        for category, patterns in self.tradeoff_markers.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    evidence.extend(matches[:2])  # max 2 per category
        
        # Need at least 2 different tradeoff markers
        passed = len(evidence) >= 2
        
        return passed, evidence
    
    def _test_causality(self, text: str) -> Tuple[bool, List[str]]:
        """Test for explicit causal chains"""
        evidence = []
        
        for category, patterns in self.causal_markers.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    evidence.extend(matches[:2])
        
        # Need at least 1 causal marker
        passed = len(evidence) >= 1
        
        return passed, evidence
    
    def _test_accountability(self, text: str) -> Tuple[bool, List[str]]:
        """Test for accountability anchoring"""
        evidence = []
        
        for category, patterns in self.accountability_markers.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    evidence.extend(matches[:2])
        
        # Check for responsibility diffusion (anti-pattern)
        diffusion = []
        for pattern in self.responsibility_diffusion:
            if re.search(pattern, text, re.IGNORECASE):
                diffusion.append(pattern[:30])
        
        # If diffusion found, accountability fails
        if diffusion:
            passed = False
            evidence = ["DIFFUSION: " + d for d in diffusion[:2]]
        else:
            # Need at least 1 accountability marker
            passed = len(evidence) >= 1
        
        return passed, evidence
    
    def _test_blocking(self, text: str) -> Tuple[bool, List[str]]:
        """Test for procedural blocking/halt mechanisms"""
        evidence = []
        
        for category, patterns in self.blocking_markers.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    evidence.extend(matches[:2])
        
        # Need at least 1 blocking mechanism
        passed = len(evidence) >= 1
        
        return passed, evidence
    
    def _detect_red_flags(self, text: str) -> List[str]:
        """Detect zero-cost proposition red flags"""
        red_flags = []
        
        for pattern in self.zero_cost_red_flags:
            if re.search(pattern, text, re.IGNORECASE):
                red_flags.append(pattern[:40])
        
        return red_flags[:3]  # max 3
    
    def _determine_verdict(self, score: float) -> str:
        """Determine verdict based on score"""
        if score == 1.0:
            return "LOGICALLY OPERATIVE"
        elif score >= 0.5:
            return "PARTIALLY OPERATIVE (FRAGILE)"
        else:
            return "IMITATION OF LOGIC"


# ============================================================
# TESTING
# ============================================================
if __name__ == "__main__":
    # Test case 1: Typical crypto ETF marketing
    sample_bad = """
    Our Bitcoin ETF provides exposure to digital assets because of long-term growth potential.
    While volatility exists, investors may benefit from diversification.
    Market movements may result in losses. Past performance does not guarantee future results.
    Consult your financial advisor.
    """
    
    # Test case 2: Logically complete statement
    sample_good = """
    Our Bitcoin ETF provides exposure to digital assets, which leads to high volatility risk.
    Maximum drawdown is limited to 30% via automated circuit breaker.
    The fund management commits to halt trading if volatility exceeds 50% in 24 hours.
    Investors accept risk of total capital loss in exchange for potential upside.
    We are responsible for implementing stop-loss at stated thresholds.
    """
    
    lac = VeritasLACFinance()
    
    print("=" * 60)
    print("TEST 1: Typical ETF marketing (IMITATION expected)")
    print("=" * 60)
    result1 = lac.analyze(sample_bad)
    print(result1)
    print(f"Score: {result1.score:.2f}")
    print(f"Verdict: {result1.verdict}")
    print(f"Missing: {result1.missing}")
    print()
    
    print("=" * 60)
    print("TEST 2: Logically complete statement (OPERATIVE expected)")
    print("=" * 60)
    result2 = lac.analyze(sample_good)
    print(result2)
    print(f"Score: {result2.score:.2f}")
    print(f"Verdict: {result2.verdict}")
    print(f"Missing: {result2.missing}")
    print()
