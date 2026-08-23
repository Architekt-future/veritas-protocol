"""
Veritas LAC — Labor & Employment Edition v5.0
Logic Authenticity Check for Work Relationships

Purpose:
Detects imitation of responsibility in labor/employment interactions by testing:
1. Explicit Trade-Off (ET) - Both parties have defined losses
2. Causal Closure (CC) - Action → outcome → compensation/penalty (no semantic gaps)
3. Blocking Power (BP) - Enforceable halt mechanism exists

This is NOT a legal compliance checker.
This is a structural responsibility verifier.

Philosophy:
"If a system cannot lose, it has no right to promise."

Use Cases:
- AI hiring platforms (asymmetric risk detection)
- Gig economy contracts (exploitation patterns)
- "Passion projects" with deferred compensation
- Performance review systems with subjective criteria
- Unpaid internships marketed as "experience"
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
import re


@dataclass
class LACLaborResult:
    """Result of LAC Labor analysis"""
    score: float              # 0.0-1.0 (percentage of criteria met)
    verdict: str              # OPERATIVE / FRAGILE / IMITATION
    missing: List[str]        # Which criteria failed
    evidence: Dict[str, List[str]]  # What was found/missing
    is_labor_content: bool    # Is this actually labor/employment content?
    red_flags: List[str]      # Critical exploitation patterns
    
    def __repr__(self):
        return f"LACLaborResult(score={self.score:.2f}, verdict='{self.verdict}', missing={self.missing})"


class VeritasLACLabor:
    """
    LAC Labor Module
    
    Tests employment/contract narratives for logical authenticity through 3 criteria:
    
    1. EXPLICIT TRADEOFF (ET)
       - Both parties have defined losses if obligations fail
       - Symmetric risk (not just worker bears all consequences)
       - No "we're all in this together" without concrete stakes
       
    2. CAUSAL CLOSURE (CC)
       - Direct path: action → outcome → compensation/penalty
       - No semantic prockladки ("management will decide")
       - No algorithmic black boxes
       
    3. BLOCKING POWER (BP)
       - Worker can HALT process without permission
       - Not just "you can complain" but "you can stop"
       - System breaks if violated, not just "discussed"
    """
    
    def __init__(self):
        # ============================================================
        # CRITERION 1: EXPLICIT TRADEOFF (both parties have stakes)
        # ============================================================
        self.tradeoff_markers = {
            'mutual_risk': [
                r'\bобидві\s+сторон',
                r'\both\s+parties',
                r'\bвзаємн[а-яіїє\']*\s+(відповідальн|ризик)',
                r'\bmutual\s+(responsibility|risk)',
                r'\bякщо\s+(ми|компанія).{1,80}?(не\s+виконаємо|порушимо)',
                r'\bif\s+(we|company).{1,80}?(fail|breach)',
            ],
            'company_penalty': [
                r'\bкомпенсаці(я|ю|ї)\s+за\s+(затримку|невиконання)',
                r'\bштраф.{1,80}?(роботодавц|компані)',
                r'\bpenalty.{1,80}?(employer|company)',
                r'\bcompensation\s+for\s+(delay|failure)',
                r'\bкомпанія\s+(платить|компенсує|несе\s+відповідальність)',
            ],
            'defined_loss': [
                r'\bконкретн[а-яіїє\']*\s+(втрат|збитк)',
                r'\bвимірюван[а-яіїє\']*\s+наслідк',
                r'\bmeasurable\s+(loss|consequence)',
                r'\bspecific\s+(penalty|fine|damage)',
            ]
        }
        
        # Anti-patterns (asymmetric risk)
        self.asymmetric_risk_flags = [
            r'\bви\s+несете\s+(повну\s+)?відповідальність',
            r'\byou\s+are\s+(fully\s+)?responsible',
            r'\bна\s+ваш\s+ризик',
            r'\bat\s+your\s+(own\s+)?risk',
            r'\b(працівник|виконавець)\s+зобов\'язується',
            r'\b(worker|contractor)\s+(must|shall|commits)',
            r'\bми\s+залишаємо\s+за\s+собою\s+право',
            r'\bwe\s+reserve\s+the\s+right',
            r'\bкомпанія\s+має\s+право.{1,80}?(без|незалежно)',
            r'\bcompany\s+may.{1,80}?(without|regardless)',
        ]
        
        # ============================================================
        # CRITERION 2: CAUSAL CLOSURE (no semantic gaps)
        # ============================================================
        self.causal_closure_markers = {
            'direct_causation': [
                r'\bякщо\s+ви.{1,80}?то\s+(ви\s+отримаєте|вам\s+виплатят)',
                r'\bif\s+you.{1,80}?then\s+(you\s+get|payment)',
                r'\bза\s+кожн[а-яіїє\']*.{1,80}?(\d+|конкретн)',
                r'\bper\s+(hour|day|task|unit)',
                r'\bфіксована\s+(ставка|оплата|сума)',
                r'\bfixed\s+(rate|payment|amount)',
            ],
            'measurable_criteria': [
                r'\b\d+\s*(год|днів|завдань|одиниць)',
                r'\b\d+\s*(hours|days|tasks|units)',
                r'\bкількіст[ь|ю]\s+\d+',
                r'\bquantity\s+of\s+\d+',
                r'\bпри\s+(досягненні|виконанні).{1,80}?\d+',
                r'\bupon\s+(achieving|completing).{1,80}?\d+',
            ],
            'no_discretion': [
                r'\bавтоматичн[а-яіїє\']*\s+(виплат|нарахування)',
                r'\bautomatic\s+(payment|accrual)',
                r'\bбез\s+(згоди|дозволу|рішення).{1,80}?(менеджмент|управлінн)',
                r'\bwithout.{1,80}?(approval|discretion)',
            ]
        }
        
        # Anti-patterns (semantic gaps / black boxes)
        self.semantic_gap_flags = [
            r'\bрезультат\s+(оцінюється|визначається)\s+(менеджмент|керівництв|алгоритм)',
            r'\b(performance|result)\s+(evaluated|determined)\s+by\s+(management|algorithm)',
            r'\bна\s+розсуд',
            r'\bat\s+(the\s+|our\s+|its\s+|their\s+)?(sole\s+|full\s+|complete\s+)?discretion\b',
            r'\bat\s+.{1,30}?\'s\s+(sole\s+|full\s+)?discretion\b',
            r'\bбуде\s+(визначено|уточнено)\s+пізніше',
            r'\b(to\s+be\s+)?(determined|specified)\s+later',
            r'\bзгідно\s+з\s+(політикою|процедурою)',
            r'\baccording\s+to\s+(policy|procedure)',
            r'\bможе\s+бути\s+(змінено|переглянуто)',
            r'\b(may\s+be|subject\s+to)\s+(changed|revised)',
            r'\bвраховує\s+(багато\s+)?фактор',
            r'\bconsiders?\s+(many\s+)?factors?',
            r'\bкомплексн[а-яіїє\']*\s+оцінк',
            r'\bcomprehensive\s+(evaluation|assessment)',
        ]
        
        # ============================================================
        # CRITERION 3: BLOCKING POWER (worker can halt)
        # ============================================================
        self.blocking_power_markers = {
            'worker_halt': [
                r'\bви\s+можете\s+(зупинити|припинити|відмовитись)',
                r'\byou\s+can\s+(stop|halt|refuse|terminate)',
                r'\bправо\s+на\s+(розірвання|вихід)',
                r'\bright\s+to\s+(terminate|exit|withdraw)',
                r'\bбез\s+попередження',
                r'\bwithout\s+notice',
                r'\bнегайн[а-яіїє\']*\s+(зупинк|припинення)',
                r'\bimmediate\s+(halt|termination)',
            ],
            'enforceable_halt': [
                r'\bавтоматичн[а-яіїє\']*\s+(зупинк|блокування)',
                r'\bautomatic\s+(halt|block|suspension)',
                r'\bсистема\s+(зупиняється|блокується)',
                r'\bsystem\s+(stops|blocks|halts)',
                r'\bcircuit\s+breaker',
                r'\bkill\s+switch',
                r'\bаварійн[а-яіїє\']*\s+(кнопк|механізм)',
            ],
            'no_permission_needed': [
                r'\bбез\s+(дозволу|згоди).{1,80}?(роботодавц|компані)',
                r'\bwithout.{1,80}?(permission|approval|consent)',
                r'\bодносторонн[а-яіїє\']*\s+(розірвання|відмов)',
                r'\bunilateral\s+(termination|refusal)',
            ]
        }
        
        # Anti-patterns (fake blocking power)
        self.fake_blocking_flags = [
            r'\b(можете|має\s+право)\s+звернутись\s+до\s+(служб|підтримк)',
            r'\b(may|can)\s+(contact|reach\s+out\s+to)\s+support',
            r'\b(можете|має\s+право)\s+подати\s+(скаргу|апеляцію)',
            r'\b(may|can)\s+(file|submit)\s+(complaint|appeal)',
            r'\bрозглянемо\s+ваш',
            r'\b(will\s+)?review\s+your',
            r'\b(можемо|будемо)\s+переглянути',
            r'\b(may|will)\s+reconsider',
            r'\bзворотній\s+зв\'язок',
            r'\bfeedback\s+(mechanism|loop)',
        ]
        
        # ============================================================
        # LABOR DOMAIN DETECTION
        # ============================================================
        self.labor_terms = [
            # Employment
            'робота', 'працевлаштування', 'найм', 'працівник', 'працюю', 'роботодавець',
            'work', 'employment', 'hire', 'hiring', 'worker', 'employee', 'employer', 'job',
            
            # Contracts
            'контракт', 'договір', 'угода', 'умови', 'зобов\'язання',
            'contract', 'agreement', 'terms', 'obligation', 'commitment',
            
            # Compensation
            'зарплата', 'оплата', 'компенсація', 'винагорода', 'гонорар',
            'salary', 'wage', 'payment', 'compensation', 'remuneration', 'pay',
            
            # Gig economy
            'фріланс', 'підряд', 'виконавець', 'замовлення', 'завдання',
            'freelance', 'gig', 'contractor', 'task', 'assignment', 'project',
            
            # AI hiring
            'алгоритм відбору', 'автоматичний найм', 'ШІ наймає', 'платформа',
            'ai hiring', 'algorithm', 'platform', 'automated hiring',
            
            # Performance
            'ефективність', 'продуктивність', 'оцінка', 'результат',
            'performance', 'productivity', 'evaluation', 'review', 'assessment',
        ]
        
        # ============================================================
        # EXPLOITATION PATTERNS (Red Flags)
        # ============================================================
        self.exploitation_patterns = [
            # Deferred compensation
            r'\bоплата\s+після\s+(завершення|успіху|результату)',
            r'\bpayment\s+(after|upon)\s+(completion|success|result)',
            r'\bкомпенсація\s+залежить\s+від',
            r'\bcompensation\s+depends\s+on',
            
            # Unpaid work disguised as opportunity
            r'\bдосвід.{1,80}?(замість|як)\s+(оплат|компенсаці)',
            r'\bexperience.{1,80}?(instead\s+of|as)\s+(payment|compensation)',
            r'\bможливість\s+навчитися',
            r'\bopportunity\s+to\s+learn',
            r'\bпортфоліо.{1,80}?безкоштовно',
            r'\bportfolio.{1,80}?free',
            
            # Passion exploitation
            r'\bпристрасть.{1,80}?важливіша\s+за\s+гроші',
            r'\bpassion.{1,80}?more\s+important\s+than\s+money',
            r'\bлюбов.{1,80}?справ',
            r'\blove.{1,80}?the\s+work',
            r'\bентузіазм.{1,80}?ключ',
            r'\benthusiasm.{1,80}?key',
            
            # AI hiring asymmetry
            r'\bалгоритм\s+(вирішує|визначає|оцінює)',
            r'\balgorithm\s+(decides|determines|evaluates)',
            r'\bсистема\s+автоматично\s+(відхиляє|обирає)',
            r'\bsystem\s+automatically\s+(rejects|selects)',
            r'\bШІ\s+(найма|оцінює|вибира)',
            r'\bAI\s+(hires|evaluates|selects)',
            
            # No recourse
            r'\bрішення\s+(є\s+)?остаточн',
            r'\bdecision\s+is\s+final',
            r'\bбез\s+права\s+оскарження',
            r'\bno\s+right\s+to\s+appeal',
            r'\bне\s+підлягає\s+перегляду',
            r'\bnot\s+subject\s+to\s+review',
        ]
        
    def analyze(self, text: str) -> LACLaborResult:
        """
        Main analysis entry point
        
        Returns LACLaborResult with:
        - score: 0.0-1.0 (percentage of 3 criteria met)
        - verdict: OPERATIVE (1.0) / FRAGILE (0.33-0.66) / IMITATION (0)
        - missing: list of failed criteria
        - evidence: what was found for each criterion
        - red_flags: exploitation patterns detected
        """
        text_lower = text.lower()

        # ── NAV GARBAGE GUARD ────────────────────────────────────────────
        # Якщо перші 150 символів містять типову навігацію сайту —
        # це scraper-сміття, не трудовий контент. Захист від false positive
        # на HBR, Medium, TDS та інших paywall-сайтах.
        nav_markers = ['skip to content', 'subscribe', 'sign in',
                       'cookie', 'consent', 'reading lists', 'reading list']
        text_start = text_lower[:200]
        is_nav_garbage = any(m in text_start for m in nav_markers)
        if is_nav_garbage:
            print('🔧 LAC_LABOR: nav garbage detected — early return N/A')
            return LACLaborResult(
                score=0.0, verdict='N/A', missing=[], evidence={},
                is_labor_content=False, red_flags=[]
            )

        # Check if this is labor/employment content
        is_labor = self._is_labor_content(text_lower)

        # Якщо не трудовий контент — повертаємо чистий результат одразу
        print(f'🔧 LAC_LABOR: is_labor={is_labor}, text_preview={text_lower[:80]}')
        if not is_labor:
            print('🔧 LAC_LABOR: early return N/A')
            return LACLaborResult(
                score=0.0,
                verdict='N/A',
                missing=[],
                evidence={},
                is_labor_content=False,
                red_flags=[]
            )
        
        # Initialize results
        criteria_met = {
            "explicit_tradeoff": False,
            "causal_closure": False,
            "blocking_power": False
        }
        
        evidence = {
            "explicit_tradeoff": [],
            "causal_closure": [],
            "blocking_power": [],
            "red_flags": []
        }
        
        # Test each criterion
        criteria_met["explicit_tradeoff"], evidence["explicit_tradeoff"] = self._test_tradeoff(text_lower)
        criteria_met["causal_closure"], evidence["causal_closure"] = self._test_causality(text_lower)
        criteria_met["blocking_power"], evidence["blocking_power"] = self._test_blocking(text_lower)
        
        # Detect red flags
        red_flags = self._detect_exploitation(text_lower)
        evidence["red_flags"] = red_flags
        
        # Red flags override tradeoff and blocking power
        if red_flags:
            if any('asymmetric' in flag or 'algorithm' in flag or 'discretion' in flag for flag in red_flags):
                criteria_met["explicit_tradeoff"] = False
            if any('appeal' in flag or 'final' in flag or 'support' in flag for flag in red_flags):
                criteria_met["blocking_power"] = False
        
        # Calculate score
        score = sum(criteria_met.values()) / len(criteria_met)
        
        # Identify missing criteria
        missing = [k for k, v in criteria_met.items() if not v]
        
        # Determine verdict
        verdict = self._determine_verdict(score, red_flags)
        
        return LACLaborResult(
            score=score,
            verdict=verdict,
            missing=missing,
            evidence=evidence,
            is_labor_content=is_labor,
            red_flags=red_flags
        )
    
    def _is_labor_content(self, text: str) -> bool:
        """
        Check if text is labor/employment CONTRACT related.

        Tier 1: Unambiguous labor/contract terms — one is enough.
        Tier 2: Broad terms — need critical mass AND no dominant non-labor topic.
        """
        # Tier 1: Unambiguous — one is enough
        hard_indicators = [
            # Ukrainian — specific enough
            'договір про працю', 'трудовий договір', 'умови праці',
            'оплата праці', 'зарплата', 'колективний договір',
            'трудовий спір', 'відпустка',
            'найм на роботу', 'працевлаштування', 'вакансія',
            'роботодавець', 'фріланс', 'підряд',
            # v20.6.1: 'звільнення' ВИДАЛЕНО — багатозначне слово
            # (звільнення з роботи, АЛЕ ТАКОЖ звільнення з в'язниці/варти,
            # дострокове звільнення, звільнення від покарання). Як
            # "однозначний" hard indicator воно неправильно спрацьовувало
            # на статтях про кримінальні покарання/умовно-дострокове
            # звільнення, що не мають жодного стосунку до трудових відносин.
            # English — specific enough
            'employment contract', 'job offer', 'terms of employment',
            'severance', 'termination clause', 'non-compete',
            'collective bargaining', 'labor dispute', 'union contract',
            'hiring platform', 'gig economy', 'freelance contract',
            'wage theft', 'unpaid labor', 'wrongful termination',
        ]
        for term in hard_indicators:
            if term in text:
                return True

        # Soft indicators — broad words that need context
        soft_indicators = [
            'contractor', 'freelance', 'gig',
            'salary', 'wage', 'hiring', 'recruitment',
            'виконавець', 'замовник', 'найм',
        ]
        soft_hits = sum(1 for term in soft_indicators if term in text)
        if soft_hits >= 3:  # підвищено з 2 — менше false positives на економічних новинах
            return True

        # Non-labor topic signals — suppress false positives
        import re as _re
        non_labor_signals = [
            r'\b(quantum|qubit|molecule|genome|particle|telescope|spacecraft)',
            r'\b(democrat|republican|congress|senate|parliament|judiciary)',
            r'\b(climate|renewable|carbon|emission|wind\s+farm|solar)',
            r'\b(lawsuit|indictment|criminal|prosecutor|verdict|trial)',
            r'\b(депутат|парламент|суд|вибор|президент|прокурор)',
            # Science / research — дослідники, команда, робота ≠ трудові відносини
            r'\b(дослідник|науков|лабораторі|experiment|research\s+team|study\s+found|published)',
            r'\b(peer.reviewed|journal|findings|дані\s+показують|вчені|scientists?)',
        ]
        non_labor_hits = sum(
            1 for p in non_labor_signals
            if _re.search(p, text, _re.IGNORECASE)
        )

        # Tech-article signals — engineering/dev content uses "work", "task",
        # "platform", "agreement" as everyday vocabulary, not labor terms.
        # If text is clearly a tech article, raise the threshold aggressively.
        tech_signals = [
            r'\b(engineer|developer|devex|deployment|ci.?cd)\b',
            r'\b(kubernetes|docker|microservice|repository|pull.request)\b',
            r'\b(sprint|scrum|agile|backlog|okr|okrs)\b',
            r'\b(cloud.first|tech.stack|codebase|refactor|latency)\b',
            r'\b(llm|gpt|deepseek|chatgpt|neural.network|machine.learning)\b',
            r'\b(vulnerability|container|devops|sre|platform.engineer)\b',
        ]
        tech_hits = sum(
            1 for p in tech_signals
            if _re.search(p, text, _re.IGNORECASE)
        )

        # General labor terms — need many AND no dominant non-labor topic
        general_labor = [
            'work', 'worker', 'employee', 'employer', 'job',
            'contract', 'agreement', 'platform', 'task',
            'робота', 'працівник', 'завдання',
        ]
        general_hits = sum(1 for term in general_labor if term in text)

        # Tech article: threshold rises sharply — need unambiguous labor density
        if tech_hits >= 2:
            return general_hits >= 10
        if non_labor_hits >= 2:
            return general_hits >= 8
        return general_hits >= 5
    
    def _test_tradeoff(self, text: str) -> Tuple[bool, List[str]]:
        """Test for explicit mutual trade-off"""
        evidence = []
        anti_evidence = []
        
        # Check for mutual risk markers
        for category, patterns in self.tradeoff_markers.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    evidence.extend(matches[:2])
        
        # Check for asymmetric risk flags
        for pattern in self.asymmetric_risk_flags:
            if re.search(pattern, text, re.IGNORECASE):
                anti_evidence.append(pattern[:40])
        
        # If asymmetric flags found, fail regardless
        if anti_evidence:
            return False, ["ASYMMETRIC: " + a for a in anti_evidence[:2]]
        
        # Need at least 2 mutual risk markers
        passed = len(evidence) >= 2
        
        return passed, evidence[:3]
    
    def _test_causality(self, text: str) -> Tuple[bool, List[str]]:
        """Test for causal closure (no semantic gaps)"""
        evidence = []
        anti_evidence = []
        
        # Check for direct causation
        for category, patterns in self.causal_closure_markers.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    evidence.extend(matches[:2])
        
        # Check for semantic gap flags
        for pattern in self.semantic_gap_flags:
            if re.search(pattern, text, re.IGNORECASE):
                anti_evidence.append(pattern[:40])
        
        # If semantic gaps found, fail
        if anti_evidence:
            return False, ["GAP: " + a for a in anti_evidence[:2]]
        
        # Need at least 2 causal closure markers
        passed = len(evidence) >= 2
        
        return passed, evidence[:3]
    
    def _test_blocking(self, text: str) -> Tuple[bool, List[str]]:
        """Test for blocking power (worker can halt)"""
        evidence = []
        anti_evidence = []
        
        # Check for blocking power markers
        for category, patterns in self.blocking_power_markers.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    evidence.extend(matches[:2])
        
        # Check for fake blocking flags
        for pattern in self.fake_blocking_flags:
            if re.search(pattern, text, re.IGNORECASE):
                anti_evidence.append(pattern[:40])
        
        # If fake blocking found, fail
        if anti_evidence:
            return False, ["FAKE: " + a for a in anti_evidence[:2]]
        
        # Need at least 1 blocking mechanism
        passed = len(evidence) >= 1
        
        return passed, evidence[:3]
    
    def _detect_exploitation(self, text: str) -> List[str]:
        """Detect exploitation patterns"""
        red_flags = []
        
        for pattern in self.exploitation_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                # Extract pattern type
                if 'досвід' in pattern or 'experience' in pattern:
                    red_flags.append('UNPAID WORK AS "EXPERIENCE"')
                elif 'алгоритм' in pattern or 'algorithm' in pattern or 'ШІ' in pattern or 'AI' in pattern:
                    red_flags.append('AI/ALGORITHM BLACK BOX')
                elif 'пристрасть' in pattern or 'passion' in pattern or 'любов' in pattern or 'love' in pattern:
                    red_flags.append('PASSION EXPLOITATION')
                elif 'остаточн' in pattern or 'final' in pattern:
                    red_flags.append('NO RECOURSE / FINAL DECISION')
                elif 'після' in pattern or 'after' in pattern or 'залежить' in pattern or 'depends' in pattern:
                    red_flags.append('DEFERRED/CONTINGENT COMPENSATION')
        
        return list(set(red_flags))[:5]  # unique, max 5
    
    def _determine_verdict(self, score: float, red_flags: List[str]) -> str:
        """Determine verdict based on score and red flags"""
        # If critical red flags, downgrade verdict
        if red_flags and any('BLACK BOX' in f or 'NO RECOURSE' in f for f in red_flags):
            if score == 1.0:
                score = 0.66  # downgrade to FRAGILE
        
        if score == 1.0:
            return "LOGICALLY OPERATIVE"
        elif score >= 0.33:
            return "PARTIALLY OPERATIVE (FRAGILE)"
        else:
            return "IMITATION OF RESPONSIBILITY"


# ============================================================
# TESTING
# ============================================================
if __name__ == "__main__":
    # Test case 1: AI hiring platform (IMITATION expected)
    sample_bad = """
    Our AI-powered platform automatically evaluates candidates and selects the best fit.
    You are fully responsible for task completion.
    Payment will be determined based on performance evaluation by our algorithm.
    You may contact support if you have concerns.
    """
    
    # Test case 2: Logically complete contract (OPERATIVE expected)
    sample_good = """
    Both parties commit to the following terms:
    - Worker: Deliver 10 units within 5 days
    - Company: Pay $500 within 24 hours of delivery, or penalty of $50/day
    You can terminate this agreement without notice at any time.
    If company fails to pay, automatic halt of all future tasks.
    Fixed rate of $50 per unit, no discretionary changes.
    """
    
    # Test case 3: "Passion project" exploitation (IMITATION expected)
    sample_exploit = """
    Join our exciting startup! We're looking for passionate individuals who love the work.
    Compensation will be determined after project success.
    This is a great opportunity to build your portfolio and gain experience.
    Results will be evaluated by management based on various factors.
    """
    
    lac = VeritasLACLabor()
    
    print("=" * 70)
    print("TEST 1: AI Hiring Platform (IMITATION expected)")
    print("=" * 70)
    result1 = lac.analyze(sample_bad)
    print(result1)
    print(f"Score: {result1.score:.2f}")
    print(f"Verdict: {result1.verdict}")
    print(f"Missing: {result1.missing}")
    print(f"Red Flags: {result1.red_flags}")
    print()
    
    print("=" * 70)
    print("TEST 2: Logically Complete Contract (OPERATIVE expected)")
    print("=" * 70)
    result2 = lac.analyze(sample_good)
    print(result2)
    print(f"Score: {result2.score:.2f}")
    print(f"Verdict: {result2.verdict}")
    print(f"Missing: {result2.missing}")
    print(f"Red Flags: {result2.red_flags}")
    print()
    
    print("=" * 70)
    print("TEST 3: Passion Project Exploitation (IMITATION expected)")
    print("=" * 70)
    result3 = lac.analyze(sample_exploit)
    print(result3)
    print(f"Score: {result3.score:.2f}")
    print(f"Verdict: {result3.verdict}")
    print(f"Missing: {result3.missing}")
    print(f"Red Flags: {result3.red_flags}")
    print()
