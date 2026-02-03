"""
Emergency Pattern-Based Detection Layer
Catches sophisticated pseudoscience/conspiracy that evades term matching
"""

import re

class PatternBoostEngine:
    """Detects semantic fingerprints and structural patterns"""
    
    def __init__(self):
        # ============================================================
        # SEMANTIC FINGERPRINTS — specific dangerous combinations
        # ============================================================
        self.fingerprints = [
            {
                'name': 'SOVEREIGN_CITIZEN',
                'patterns': [
                    r'(жива людина|бенефіціар|власник персони)',
                    r'(морське право|торгов.{1,20}реєстр)',
                    r'(свідоцтво про народження).{1,50}(складський|золот)',
                    r'(фізична особа).{1,30}(мертв|юрисдикц)',
                    r'(суверен|autograph).{1,40}(суб.єкт|право)',
                    r'(податки?).{1,50}(незакон|контрибуц|синдикат)',
                ],
                'score': 0.6,
                'description': 'Псевдоправова маячня sovereign citizens'
            },
            {
                'name': 'NEURO_CONTROL',
                'patterns': [
                    r'(нейро|синапс).{1,50}(нано|квантов|дискретизац)',
                    r'(6g|5g).{1,50}(ендокринн|лімбічн|частот)',
                    r'(алгоритм|протокол).{1,50}(емоційн|поведінк).{1,50}(модулюва|контрол)',
                    r'(пост-біологічн|цифров.{1,20}розум)',
                    r'(колективн.{1,20}несвідом|глобальн.{1,20}свідом)',
                ],
                'score': 0.65,
                'description': 'Техно-параноїдальна конспірологія'
            },
            {
                'name': 'NEW_AGE_ESOTERIC',
                'patterns': [
                    r'(гайя|гая).{1,50}(свідом|вимір|ініціац)',
                    r'(вібрац|частот).{1,50}(планет|земл|фон)',
                    r'(чакр|енергетичн.{1,20}кокон|ефірн.{1,20}кокон)',
                    r'(великий перехід|вищі виміри|тривимірн.{1,20}пастк)',
                    r'(медитація|інтуїц).{1,50}(зупини|війн|частот)',
                    r'(матриц|ілюз).{1,30}(розсип|пробудж)',
                ],
                'score': 0.6,
                'description': 'Нью-ейдж езотерика'
            },
            {
                'name': 'TECHNO_MYSTICISM',
                'patterns': [
                    r'(квантов).{1,50}(душа|свідом|енерг|чакр)',
                    r'(ai|штучн.{1,20}інтелект).{1,50}(духов|інтуїц|пізнан)',
                    r'(алгоритм).{1,30}(завіса|закрива|світло)',
                    r'(blockchain|криптовалют).{1,50}(карма|душ|астрал)',
                ],
                'score': 0.55,
                'description': 'Технологічний містицизм'
            },
            {
                'name': 'PSEUDO_SCIENTIFIC_MIX',
                'patterns': [
                    r'(квантов).{1,50}(супутник|орбіт).{1,50}(несвідом|контрол)',
                    r'(нано).{1,30}(днк|нейрон|синапс).{1,50}(переписа|модиф|контрол)',
                    r'(резонатор|частот).{1,50}(атлант|цивіліз|антарктид)',
                ],
                'score': 0.65,
                'description': 'Псевдонаукове змішування'
            }
        ]
    
    def analyze(self, text: str) -> dict:
        """Returns {'boost': float, 'matched_patterns': list}"""
        text_lower = text.lower()
        
        total_boost = 0.0
        matched = []
        
        for fingerprint in self.fingerprints:
            hits = 0
            for pattern in fingerprint['patterns']:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    hits += 1
            
            # If 2+ patterns from this fingerprint match → FIRE
            if hits >= 2:
                total_boost += fingerprint['score']
                matched.append({
                    'name': fingerprint['name'],
                    'hits': hits,
                    'total_patterns': len(fingerprint['patterns']),
                    'description': fingerprint['description']
                })
        
        return {
            'boost': min(total_boost, 0.85),  # cap at 0.85
            'matched_patterns': matched
        }
