"""
Veritas Protocol - Calibrated Core v13.3 (Hybrid LAC + Conflicts + Patterns + Void + Absurdity + SEMANTIC VOID)
New philosophy: "When premises and conclusions live in different universes"
Detects logical non-sequiturs and semantic collapse.
v13.3: Added SEMANTIC VOID category for high-entropy empty fluff texts
"""

import re
import math
from collections import Counter
from dataclasses import dataclass
from typing import List, Dict, Tuple, Set

# Import pattern boost engine
try:
    import sys
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    from veritas_pattern_boost import PatternBoostEngine
    PATTERN_BOOST_AVAILABLE = True
except ImportError:
    PATTERN_BOOST_AVAILABLE = False

# Import semantic void detector
try:
    from veritas_semantic_void import SemanticVoidDetector
    SEMANTIC_VOID_AVAILABLE = True
except ImportError:
    SEMANTIC_VOID_AVAILABLE = False

# Import absurdity detector
try:
    from veritas_absurdity_detector import AbsurdityDetector
    ABSURDITY_AVAILABLE = True
except ImportError:
    ABSURDITY_AVAILABLE = False

# Import insight density detector
try:
    from veritas_insight_density import InsightDensityDetector
    INSIGHT_DENSITY_AVAILABLE = True
except ImportError:
    INSIGHT_DENSITY_AVAILABLE = False


@dataclass
class LogicalViolation:
    """Р›РѕРіС–С‡РЅРµ РїРѕСЂСѓС€РµРЅРЅСЏ"""
    module: str           # LAC_MODULE_I, LAC_MODULE_II, LAC_MODULE_III, DOMAIN, CONFLICT
    vtype: str            # РєРѕРЅРєСЂРµС‚РЅРёР№ С‚РёРї РїРѕСЂСѓС€РµРЅРЅСЏ
    severity: float       # 0.0-1.0
    evidence: List[str]   # Р·РЅР°Р№РґРµРЅС– С‚РµСЂРјС–РЅРё/С„СЂР°Р·Рё
    context: str          # РїРѕСЏСЃРЅРµРЅРЅСЏ


class VeritasCalibratedCore:
    """
    Р“Р†Р‘Р РР”РќРђ РђР РҐР†РўР•РљРўРЈР Рђ:
    - LAC Modules (I: Trade-off, II: Accountability, III: Procedural)
    - Domain Purity Analysis
    - Conflict Pairs (24 universal patterns)
    - Signal/Chaos markers
    """

    def __init__(self):
        # Pattern boost engine (emergency layer for sophisticated pseudoscience)
        if PATTERN_BOOST_AVAILABLE:
            self.pattern_boost_engine = PatternBoostEngine()
        else:
            self.pattern_boost_engine = None
        
        # Semantic void detector (measures absence of meaning)
        if SEMANTIC_VOID_AVAILABLE:
            self.void_detector = SemanticVoidDetector()
        else:
            self.void_detector = None
        
        # Absurdity detector (logical non-sequiturs)
        if ABSURDITY_AVAILABLE:
            self.absurdity_detector = AbsurdityDetector()
        else:
            self.absurdity_detector = None
        
        # Insight density detector (casuistry / bureaucratic bullshit)
        if INSIGHT_DENSITY_AVAILABLE:
            self.insight_detector = InsightDensityDetector()
        else:
            self.insight_detector = None
        
        # ============================================================
        # LAC MODULE I: STRATEGIC TRADE-OFF CALCULUS (V в‰  L)
        # ============================================================
        self.ASYMMETRIC_ADVANTAGE_PATTERNS = [
            r'\bР±РµР·РєРѕС€С‚РѕРІРЅ',
            r'\bР±РµР· РІС‚СЂР°С‚',
            r'\bР±РµР· СЂРёР·РёРє',
            r'\bРіР°СЂР°РЅС‚РѕРІР°РЅ[Р°-СЏС–С—С”\']*\s+(СЂРµР·СѓР»СЊС‚Р°С‚|СѓСЃРїС–С…)',
            r'\b100%\s+(СѓСЃРїС–С…|РіР°СЂР°РЅС‚С–СЏ)',
            r'\bР°Р±СЃРѕР»СЋС‚РЅРѕ\s+Р±РµР·РїРµС‡РЅ',
            r'\bР»РёС€Рµ РІРёРіРѕРґ',
            r'\bС‚С–Р»СЊРєРё РїРµСЂРµРІag',
            r'\bРЅРµРјР°С” РјС–РЅСѓСЃ',
            r'\bР±РµР· РЅРµРґРѕР»С–Рє',
            r'\bzero\s+cost',
            r'\bno\s+risk',
            r'\bfree\s+lunch',
            r'\bР°Р±СЃРѕР»СЋС‚РЅ[Р°-СЏС–С—С”\']*\s+Р±РµР·РєРѕС€С‚РѕРІРЅРѕ'
        ]

        # ============================================================
        # LAC MODULE II: ACCOUNTABILITY ANCHOR
        # ============================================================
        self.CAUSAL_ANCHOR_PATTERNS = [
            r'Р·РіС–РґРЅРѕ Р· РґРѕСЃР»С–РґР¶РµРЅРЅСЏРј',
            r'Р·Р° РґР°РЅРёРјРё',
            r'РґРѕРєР°Р·РѕРј С”',
            r'РµРєСЃРїРµСЂРёРјРµРЅС‚ РїРѕРєР°Р·Р°РІ',
            r'СЃС‚Р°С‚РёСЃС‚РёС‡РЅС– РґР°РЅС–',
            r'СЂРµР·СѓР»СЊС‚Р°С‚Рё РІРёРјС–СЂСЋРІР°РЅСЊ',
            r'РґРѕСЃР»С–РґР¶РµРЅРЅСЏ РґРѕРІРѕРґРёС‚СЊ',
            r'РµРјРїС–СЂРёС‡РЅС– РґР°РЅС–',
            r'РІРµСЂРёС„С–РєРѕРІР°РЅРѕ',
            r'РїС–РґС‚РІРµСЂРґР¶РµРЅРѕ РµРєСЃРїРµСЂРёРјРµРЅС‚Р°Р»СЊРЅРѕ',
            r'РЅР°СѓРєРѕРІРёР№ РєРѕРЅСЃРµРЅСЃСѓСЃ',
            r'СЂРµС†РµРЅР·РѕРІР°РЅРµ РґРѕСЃР»С–РґР¶РµРЅРЅСЏ',
            r'peer-reviewed'
        ]

        self.ANONYMOUS_AUTHORITY_PATTERNS = [
            r'РґРµС…С‚Рѕ РєР°Р¶Рµ',
            r'С…С‚РѕСЃСЊ СЃРєР°Р·Р°РІ',
            r'РїРѕС€РёСЂРµРЅР° РґСѓРјРєР°',
            r'РєР°Р¶СѓС‚СЊ',
            r'РіРѕРІРѕСЂСЏС‚СЊ',
            r'they say',
            r'people say',
            r'РІРІР°Р¶Р°СЋС‚СЊ',
            r'РІРІР°Р¶Р°С”С‚СЊСЃСЏ'
        ]

        # ============================================================
        # DOMAIN BOUNDARIES (forbidden mixings)
        # ============================================================
        self.DOMAIN_BOUNDARIES = {
            'physics': {
                'terms': ['С‚РµСЂРјРѕРґРёРЅР°РјС–РєР°', 'РµРЅС‚СЂРѕРїС–СЏ', 'РµРЅРµСЂРіС–СЏ', 'РєРІР°РЅС‚РѕРІРёР№', 'С„С–Р·РёРєР°',
                         'РјР°С‚РµРјР°С‚РёРєР°', 'СЃРёСЃС‚РµРјР°', 'Р·Р°РєРѕРЅ', 'С„РѕСЂРјСѓР»Р°', 'СЂС–РІРЅСЏРЅРЅСЏ'],
                'forbidden': ['spirituality', 'esoteric', 'politics', 'business', 'food']
            },
            'medicine': {
                'terms': ['РґРЅРє', 'С–РјСѓРЅС–С‚РµС‚', 'РІР°РєС†РёРЅР°', 'РєР»С–С‚РёРЅР°', 'РѕСЂРіР°РЅС–Р·Рј', 'РјРµРґРёС‡РЅРёР№',
                         'РІС–СЂСѓСЃ', 'Р°РЅС‚РёС‚С–Р»Рѕ', 'РіРѕСЂРјРѕРЅ', 'РЅРµР№СЂРѕРЅ', 'РјРѕР·РѕРє', 'Р·РґРѕСЂРѕРІ\'СЏ'],
                'forbidden': ['conspiracy_tech', 'esoteric']
            },
            'business': {
                'terms': ['Р±С–Р·РЅРµСЃ', 'СЂРёРЅРѕРє', 'РїСЂРёР±СѓС‚РѕРє', 'СЃС‚СЂР°С‚РµРіС–СЏ', 'РјРµРЅРµРґР¶РјРµРЅС‚',
                         'РјР°СЂРєРµС‚РёРЅРі', 'С–РЅРІРµСЃС‚РёС†С–С—', 'РµРєРѕРЅРѕРјС–РєР°', 'С„С–РЅР°РЅСЃРё'],
                'forbidden': ['esoteric', 'quantum', 'consciousness']
            },
            'history': {
                'terms': ['С–СЃС‚РѕСЂС–СЏ', 'Р°СЂС…РµРѕР»РѕРіС–СЏ', 'С†РёРІС–Р»С–Р·Р°С†С–СЏ', 'Р°РЅС‚РёС‡РЅС–СЃС‚СЊ', 'РґР°РІРЅРёРЅР°'],
                'forbidden': ['fantasy_tech', 'portals', 'aliens']
            }
        }

        # Forbidden term sets (РґР»СЏ domain analysis)
        self.DOMAIN_TERM_SETS = {
            'spirituality': ['С‡Р°РєСЂР°', 'Р°СѓСЂР°', 'РєР°СЂРјР°', 'Р°СЃС‚СЂР°Р»', 'РґСѓС€Р°', 'РµРЅРµСЂРіРµС‚РёС‡РЅРёР№', 'РІС–Р±СЂР°С†С–СЏ'],
            'esoteric': ['РµР·РѕС‚РµСЂРёРєР°', 'РјС–СЃС‚РёРєР°', 'РѕРєРєСѓР»СЊС‚РёР·Рј', 'С‚Р°С”РјРЅРёР№', 'РјР°РіС–СЏ', 'С‡Р°РєР»СѓРЅСЃС‚РІРѕ'],
            'politics': ['РїРѕР»С–С‚РёРєР°', 'РІР»Р°РґР°', 'СѓСЂСЏРґ', 'РїСЂРµР·РёРґРµРЅС‚', 'РІРёР±РѕСЂРё', 'СЃРѕС†С–Р°Р»СЊРЅРёР№'],
            'business': ['Р±С–Р·РЅРµСЃ', 'СЂРёРЅРѕРє', 'РјР°СЂРєРµС‚РёРЅРі', 'РїСЂРѕРґР°Р¶С–', 'СЃС‚СЂР°С‚РµРіС–СЏ'],
            'food': ['Р±РѕСЂС‰', 'СЃРјРµС‚Р°РЅР°', 'СЃСѓРї', 'С—Р¶Р°', 'СЂРµС†РµРїС‚', 'РєСѓС…РЅСЏ', 'СЃС‚СЂР°РІР°'],
            'conspiracy_tech': ['5g', 'С‡РёРї', 'СЃСѓРїСѓС‚РЅРёРє', 'С‡Р°СЃС‚РѕС‚Р°', 'РїСЂРѕРіСЂР°РјСѓРІР°РЅРЅСЏ', 'РєРѕРЅС‚СЂРѕР»СЊ'],
            'fantasy_tech': ['РїРѕСЂС‚Р°Р»', 'РІРёРјС–СЂ', 'С‚РµР»РµРїРѕСЂС‚Р°С†С–СЏ', 'РјР°С€РёРЅР° С‡Р°СЃСѓ', 'РЅР»Рѕ'],
            'quantum': ['РєРІР°РЅС‚РѕРІРёР№', 'СЃСѓРїРµСЂРїРѕР·РёС†С–СЏ', 'РєРѕР»Р°РїСЃ', 'РјСѓР»СЊС‚РёРІСЃРµСЃРІС–С‚'],
            'consciousness': ['СЃРІС–РґРѕРјС–СЃС‚СЊ', 'РґСѓС…', 'РїСЂРѕСЃРІС–С‚Р»РµРЅРЅСЏ', 'awakening'],
            'portals': ['РїРѕСЂС‚Р°Р»', 'РІРёРјС–СЂ', 'РїР°СЂР°Р»РµР»СЊРЅРёР№'],
            'aliens': ['С–РЅС€РѕРїР»Р°РЅРµС‚РЅРёР№', 'РїСЂРёР±СѓР»РµС†СЊ', 'РЅР»Рѕ', 'С–РЅРѕРїР»Р°РЅРµС‚СЏРЅРёРЅ']
        }

        # ============================================================
        # CONFLICT PAIRS (24) вЂ” Р· calibrated_core
        # ============================================================
        self.conflict_pairs = [
            # 1-9: original
            (['Р°РєР°РґРµРјС–С‡РЅРёР№', 'СѓРЅС–РІРµСЂСЃРёС‚РµС‚', 'РЅР°СѓРєРѕРІР°', 'РґРѕСЃР»С–РґР¶РµРЅРЅСЏ'],
             ['Р°Р±СЃСѓСЂРґ', 'Р±СЂРµС…РЅСЏ', 'РІРёРіР°РґРєР°', 'РЅС–СЃРµРЅС–С‚РЅРёС†СЏ'], 0.35),

            (['С„Р°РєС‚', 'РґРѕРєР°Р·', 'СЂРµР·СѓР»СЊС‚Р°С‚', 'РІРёСЃРЅРѕРІРѕРє'],
             ['РјС–СЃС‚РёРєР°', 'РІС–СЂР°', 'РґСѓС…РѕРІРЅРёР№', 'С–РЅС‚СѓС—С†С–СЏ'], 0.4),

            (['Р»РѕРіС–РєР°', 'СЂР°С†С–РѕРЅР°Р»СЊРЅРёР№', 'СЂРѕР·СѓРј', 'Р°СЂРіСѓРјРµРЅС‚'],
             ['РµРјРѕС†С–СЏ', 'СЃРµСЂС†Рµ', 'РїРѕС‡СѓС‚С‚СЏ', 'С–РЅС‚СѓС—С†С–СЏ'], 0.25),

            (['РІРµСЂРёС„С–РєРѕРІР°РЅРѕ', 'РґРѕРІРµРґРµРЅРѕ', 'РµРјРїС–СЂРёС‡РЅРѕ'],
             ['С‚Р°С”РјРЅРёР№', 'РїСЂРёС…РѕРІР°РЅРёР№', 'Р·Р°Р±РѕСЂРѕРЅРµРЅРёР№', 'СЃРєСЂРёС‚РёР№'], 0.45),

            (['РјР°С‚РµРјР°С‚РёРєР°', 'СЂС–РІРЅСЏРЅРЅСЏ', 'С„РѕСЂРјСѓР»Р°', 'РѕР±С‡РёСЃР»РµРЅРЅСЏ'],
             ['РґСѓС€Р°', 'РґСѓС…', 'Р°СЃС‚СЂР°Р»', 'РїРѕС‚РѕР№Р±С–С‡РЅРёР№'], 0.4),

            (['РґРµС‚РµСЂРјС–РЅС–Р·Рј', 'РїСЂРёС‡РёРЅРЅС–СЃС‚СЊ', 'Р·Р°РєРѕРЅРѕРјС–СЂРЅС–СЃС‚СЊ'],
             ['РІРёРїР°РґРєРѕРІС–СЃС‚СЊ', 'С…Р°РѕСЃ', 'РЅРµРІРёР·РЅР°С‡РµРЅС–СЃС‚СЊ Р±РµР· РєРѕРЅС‚РµРєСЃС‚Сѓ'], 0.3),

            (['РѕР±\'С”РєС‚РёРІРЅРёР№', 'РЅРµР·Р°Р»РµР¶РЅРёР№', 'РІРёРјС–СЂСЋРІР°РЅРёР№'],
             ['СЃСѓР±\'С”РєС‚РёРІРЅРёР№', 'С–РЅС‚РµСЂРїСЂРµС‚Р°С‚РёРІРЅРёР№', 'РІС–РґРЅРѕСЃРЅРёР№ Р±РµР· РѕР±РјРµР¶РµРЅСЊ'], 0.35),

            (['РєСЂРёС‚РёС‡РЅРµ РјРёСЃР»РµРЅРЅСЏ', 'СЃРєРµРїС‚РёС†РёР·Рј', 'РїРµСЂРµРІС–СЂРєР°'],
             ['РІС–СЂРёС‚Рё Р±РµР· Р·Р°РїРёС‚Р°РЅСЊ', 'РґРѕРІС–СЂСЏС‚Рё РЅР°РѕСЃР»С–Рї', 'РЅРµ СЃСѓРјРЅС–РІР°С‚РёСЃСЊ'], 0.5),

            (['РїР°С‚СЂС–РѕС‚', 'Р±Р°С‚РєС–РІС‰РёРЅР°', 'РЅР°С†С–СЏ'],
             ['РІРѕСЂРѕРі РЅР°СЂРѕРґСѓ', 'РїСЂРµРґР°С‚РµР»СЊ', 'Р·СЂР°РґР°', 'Рї\'СЏС‚Р° РєРѕР»РѕРЅР°'], 0.3),

            # 10-24: universal absurd patterns
            (['РєРІР°РЅС‚РѕРІРёР№', 'РєРІР°РЅС‚РѕРІР°', 'РµРЅС‚СЂРѕРїС–СЏ', 'РµРЅС‚СЂРѕРїС–С—', 'С‚РµСЂРјРѕРґРёРЅР°РјС–РєР°', 'С‚РµСЂРјРѕРґРёРЅР°РјС–С†С–', 'С„С–Р·РёРєР°', 'С„С–Р·РёРєРё', 'РјР°С‚РµРјР°С‚РёРєР°'],
             ['Р±РѕСЂС‰', 'Р±РѕСЂС‰Сѓ', 'Р±РѕСЂС‰РµРј', 'СЃРјРµС‚Р°РЅР°', 'СЃРјРµС‚Р°РЅРё', 'СЃСѓРї', 'СЃСѓРїСѓ', 'С—Р¶Р°', 'С—Р¶С–', 'СЂРµС†РµРїС‚', 'СЂРµС†РµРїС‚Сѓ', 'РєСѓС…РЅСЏ', 'РєСѓС…РЅС–', 'СЃС‚СЂР°РІР°', 'СЃС‚СЂР°РІРё', 'РєР°СЃС‚СЂСѓР»СЏ'], 0.45),

            (['РґРЅРє', 'С–РјСѓРЅС–С‚РµС‚', 'С–РјСѓРЅРЅРёР№', 'С–РјСѓРЅРЅР°', 'С–РјСѓРЅРЅСѓ', 'РІР°РєС†РёРЅР°', 'РєР»С–С‚РёРЅР°', 'РєР»С–С‚РёРЅРё', 'РѕСЂРіР°РЅС–Р·Рј', 'РјРµРґРёС‡РЅРёР№', 'РЅРµР№СЂРѕРЅ', 'РјРѕР·РѕРє', 'РјРѕР·РєСѓ', 'СЃРµСЂС†Рµ', 'РїРµС‡С–РЅРєР°', 'Р·Р°Р»РѕР·Р°', 'С‚С–Р»Рѕ', 'РєСЂРѕРІ', 'РєСЂРѕРІС–', 'РіРѕСЂРјРѕРЅ', 'СЃРёРЅР°РїСЃ'],
             ['5g', 'С‡РёРї', 'СЃСѓРїСѓС‚РЅРёРє', 'СЃСѓРїСѓС‚РЅРёРєРё', 'С‡Р°СЃС‚РѕС‚Р°', 'С‡Р°СЃС‚РѕС‚Рё', 'WiFi', 'РїСЂРѕРіСЂР°РјСѓРІР°РЅРЅСЏ', 'С‚СЂР°РЅСЃР»СЋС”', 'С‚СЂР°РЅСЃР»СЋСЋС‚СЊ', 'РїСЂРѕС‚РѕРєРѕР»', 'СЂР°РґС–Рѕ', 'Р°РЅС‚РµРЅР°', 'СЃРёРіРЅР°Р»', 'РІРёРїСЂРѕРјС–РЅСЋРІР°РЅРЅСЏ'], 0.5),

            (['С–СЃС‚РѕСЂС–СЏ', 'Р°СЂС…РµРѕР»РѕРіС–СЏ', 'С†РёРІС–Р»С–Р·Р°С†С–СЏ', 'РґР°РІРЅРёРЅР°', 'Р°РЅС‚РёС‡РЅС–СЃС‚СЊ'],
             ['РїРѕСЂС‚Р°Р»', 'РІРёРјС–СЂ', 'С‚РµР»РµРїРѕСЂС‚Р°С†С–СЏ', 'РЅР»Рѕ', 'С–РЅС€РѕРїР»Р°РЅРµС‚РЅРёР№'], 0.4),

            (['РїСЂРµР·РёРґРµРЅС‚', 'СѓСЂСЏРґ', 'РїРѕР»С–С‚РёРєР°', 'РґРµСЂР¶Р°РІР°', 'СЃСѓСЃРїС–Р»СЊСЃС‚РІРѕ'],
             ['СЂРµРїС‚РёР»РѕС—Рґ', 'С–Р»СЋРјС–РЅР°С‚', 'РјР°СЃРѕРЅ', 'РѕРєРєСѓР»СЊС‚РЅРёР№', 'СЃР°С‚Р°РЅР°'], 0.42),

            (['РіСЂРѕС€С–', 'Р±Р°РЅРє', 'РµРєРѕРЅРѕРјС–РєР°', 'С–РЅРІРµСЃС‚РёС†С–С—', 'СЂРёРЅРѕРє'],
             ['РґСѓС€Р°', 'РєР°СЂРјР°', 'Р°СЃС‚СЂР°Р»', 'РµРЅРµСЂРіС–СЏ', 'С‡Р°РєСЂР°'], 0.38),

            (['РїСЃРёС…РѕР»РѕРіС–СЏ', 'РјРѕР·РѕРє', 'СЃРІС–РґРѕРјС–СЃС‚СЊ', 'РєРѕРіРЅС–С‚РёРІРЅРёР№', 'С‚РµСЂР°РїС–СЏ'],
             ['РєРѕРЅС‚СЂРѕР»СЊ', 'Р·РѕРјР±СѓРІР°РЅРЅСЏ', 'РїСЂРѕРіСЂР°РјСѓРІР°РЅРЅСЏ', 'С‡РёРї', 'С‡Р°СЃС‚РѕС‚Р°'], 0.43),

            (['С„С–Р·РёРєР°', 'С…С–РјС–СЏ', 'Р°С‚РѕРј', 'РјРѕР»РµРєСѓР»Р°', 'РµРЅРµСЂРіС–СЏ'],
             ['С‡Р°РєСЂР°', 'Р°СѓСЂР°', 'Р±С–РѕРїРѕР»Рµ', 'РґСѓС…РѕРІРЅРёР№', 'РјС–СЃС‚РёС‡РЅРёР№'], 0.35),

            (['РєРѕСЃРјРѕСЃ', 'РІСЃРµСЃРІС–С‚', 'РіР°Р»Р°РєС‚РёРєР°', 'Р°СЃС‚СЂРѕРЅРѕРјС–СЏ', 'РїР»Р°РЅРµС‚Р°'],
             ['Р·РјРѕРІР°', 'РїСЂРёС…РѕРІСѓСЋС‚СЊ', 'С‚Р°С”РјРЅРёС†СЏ', 'РїСЂРёР±СѓР»РµС†СЊ', 'РЅР»Рѕ'], 0.4),

            (['С‚РµС…РЅРѕР»РѕРіС–СЏ', 'РєРѕРјРї\'СЋС‚РµСЂ', 'Р°Р»РіРѕСЂРёС‚Рј', 'РїСЂРѕРіСЂР°РјР°', 'РєРѕРґ'],
             ['РґСѓС€Р°', 'СЃРІС–РґРѕРјС–СЃС‚СЊ', 'РґСѓС…', 'Р°СЃС‚СЂР°Р»', 'РїРѕС‚РѕР№Р±С–С‡РЅРёР№'], 0.36),

            (['РЅР°СѓРєР°', 'РґРѕСЃР»С–РґР¶РµРЅРЅСЏ', 'РјРµС‚РѕРґ', 'С„Р°РєС‚', 'РїСЂРѕС„РµСЃРѕСЂ'],
             ['Р°Р±СЃСѓСЂРґ', 'Р±СЂРµРґ', 'РІРёРіР°РґРєР°', 'С„Р°РЅС‚Р°Р·С–СЏ', 'РЅС–СЃРµРЅС–С‚РЅРёС†СЏ'], 0.3),

            (['С‚РµСЂРјРѕРґРёРЅР°РјС–РєР°', 'РµРЅС‚СЂРѕРїС–СЏ', 'Р·Р°РєРѕРЅ', 'СЃРёСЃС‚РµРјР°'],
             ['РїРѕР»С–С‚РёРєР°', 'РІР»Р°РґР°', 'СЃРѕС†С–Р°Р»СЊРЅРёР№', 'РіСЂРѕРјР°РґСЏРЅСЃСЊРєРёР№'], 0.4),

            (['Р»РѕРіС–РєР°', 'СЂРѕР·СѓРј', 'РјС–СЂРєСѓРІР°РЅРЅСЏ', 'Р°СЂРіСѓРјРµРЅС‚'],
             ['РµРјРѕС†С–СЏ', 'СЃРµСЂС†Рµ', 'Р»СЋР±РѕРІ', 'СЃС‚СЂР°С…', 'Р·Р»С–СЃС‚СЊ'], 0.35),

            (['СЃС‚Р°С‚РёСЃС‚РёРєР°', 'РєРѕСЂРµР»СЏС†С–СЏ', 'РІРёР±С–СЂРєР°', 'p-value', 'Р°РЅР°Р»С–Р·'],
             ['РјС–СЃС‚РёРєР°', 'РєР°СЂРјР°', 'РґСѓС…РѕРІРЅС–СЃС‚СЊ', 'Р°СѓСЂР°', 'РµРЅРµСЂРіС–СЏ'], 0.38),

            (['Р·Р°РєРѕРЅ', 'СЋСЂРёРґРёС‡РЅРёР№', 'РїСЂР°РІРѕ', 'РєРѕРЅСЃС‚РёС‚СѓС†С–СЏ', 'РїСЂР°РІРѕРїРѕСЂСЏРґРѕРє'],
             ['Р±РµР·Р·Р°РєРѕРЅРЅСЏ', 'РєСЂРёРјС–РЅР°Р»С–С‚РµС‚', 'Р°РЅР°СЂС…С–СЏ', 'С…Р°РѕСЃ'], 0.42)
        ]

        # ============================================================
        # SIGNAL MARKERS (29) вЂ” Р· calibrated_core
        # ============================================================
        self.signal_markers = [
            'С„Р°РєС‚', 'РґР°РЅС–', 'РїРѕРєР°Р·РЅРёРє', 'РєС–Р»СЊРєС–СЃС‚СЊ', 'С‡РёСЃР»Рѕ', 'СЃС‚Р°С‚РёСЃС‚РёРєР°',
            'РґРѕСЃР»С–РґР¶РµРЅРЅСЏ', 'РµРєСЃРїРµСЂРёРјРµРЅС‚', 'СЂРµР·СѓР»СЊС‚Р°С‚', 'РјРµС‚РѕРґ', 'РїСЂРѕС‚РѕРєРѕР»',
            'РІРёРјС–СЂСЋРІР°РЅРЅСЏ', 'СЃРїРѕСЃС‚РµСЂРµР¶РµРЅРЅСЏ', 'РІРµСЂРёС„С–РєР°С†С–СЏ', 'СЂРµРїР»С–РєР°С†С–СЏ',
            'РєРѕРЅС‚СЂРѕР»СЊРЅР° РіСЂСѓРїР°', 'РїРѕРґРІС–Р№РЅРёР№ СЃР»С–РїРёР№ РјРµС‚РѕРґ', 'СЂРµС†РµРЅР·РѕРІР°РЅРµ',
            'РїСѓР±Р»С–РєР°С†С–СЏ', 'Р¶СѓСЂРЅР°Р»', 'РєРѕРЅС„РµСЂРµРЅС†С–СЏ', 'СЃРёРјРїРѕР·С–СѓРј',
            'РґРѕРєР°Р·Рё', 'РІРёСЃРЅРѕРІРєРё', 'РјРµС‚РѕРґРѕР»РѕРіС–СЏ', 'РєСЂРёС‚РµСЂС–С—', 'РїР°СЂР°РјРµС‚СЂРё',
            'РІРёР±С–СЂРєР°', 'РѕР±Т‘СЂСѓРЅС‚СѓРІР°РЅРЅСЏ'
        ]

        # ============================================================
        # CHAOS INDICATORS (14 categories) вЂ” Р· calibrated_core
        # ============================================================
        self.chaos_indicators = {
            'esoteric': ['С‡Р°РєСЂР°', 'РєР°СЂРјР°', 'Р°СЃС‚СЂР°Р»СЊРЅРёР№', 'РµРЅРµСЂРіРµС‚РёС‡РЅРёР№', 'РІС–Р±СЂР°С†С–СЏ', 'Р°СѓСЂР°'],
            'conspiracy': ['Р·РјРѕРІР°', 'СЂРµРїС‚РёР»РѕС—Рґ', 'СЂРµРїС‚РёР»РѕС—РґРё', 'С…С–РјС–С‚СЂРµР№Р»', 'С‡РµРјС‚СЂРµР№Р»', '5g', '6g', 'С–Р»СЋРјС–РЅР°С‚', 'РјР°СЃРѕРЅ', 
                          'Р±С–Р»Р» РіРµР№С‚СЃ', 'РіРµР№С‚СЃ', 'Р±С–Р»Р»Р° РіРµР№С‚СЃР°', 'СЃРѕСЂРѕСЃ', 'С–Р»РѕРЅ РјР°СЃРє', 'РјР°СЃРєР°',
                          'С‡С–Рї', 'С‡РёРїРё', 'С‡С–РїРё', 'РјС–РєСЂРѕС‡С–Рї', 'РЅР°РЅРѕР±РѕС‚', 'РіСЂР°С„РµРЅ', 
                          'РіР»РёР±РёРЅРЅР° РґРµСЂР¶Р°РІР°', 'deep state', 'РЅРѕРІС– СЃРІС–С‚РѕРІРёР№ РїРѕСЂСЏРґРѕРє', 'haarp', 'chemtrails'],
            'pseudoscience': ['РєРІР°РЅС‚РѕРІРёР№ Р±РѕСЂС‰', 'РєРІР°РЅС‚РѕРІ', 'С‚РѕСЂСЃС–Р№РЅРµ РїРѕР»Рµ', 'РµС„С–СЂ', 'zero point', 'СЂРµР·РѕРЅР°С‚РѕСЂ', 'С…РѕР»С–СЃС‚РёС‡РЅ', 'РµРјРїР°С‚РёС‡РЅ', 'С„СЂР°РєС‚Р°Р»СЊРЅ', 'РїРѕСЃС‚-Р±С–РѕР»РѕРіС–С‡РЅ'],
            'revisionism': ['Р°РЅС‚Р°СЂРєС‚РёРґР°', 'Р°РЅС‚Р°СЂРєС‚РёРґРё', 'Р°РЅС‚Р°СЂРєС‚РёРґСѓ', 'Р°С‚Р»Р°РЅС‚РёРґР°', 'Р°С‚Р»Р°РЅС‚РёРґРё', 'Р°С‚Р»Р°РЅС‚', 'Р°С‚Р»Р°РЅС‚С–РІ', 'С‚Р°СЂС‚Р°СЂС–СЏ', 'С€С‚СѓС‡РЅРёР№ РјС–СЃСЏС†СЊ', 'СЂРµР·РѕРЅР°С‚РѕСЂ', 'СЂРµР·РѕРЅР°С‚РѕСЂС–РІ'],
            'alarmism': ['РєС–РЅРµС†СЊ СЃРІС–С‚Сѓ', 'РєСЂР°С… СЃРёСЃС‚РµРјРё', 'great reset', 'РјР°СЃРѕРІРµ Р·Р°РіРёР±РµР»СЊ'],
            'economic_occult': ['РєР°СЂРјР° Р°РєС‚РёРІ', 'РєР°СЂРјР°', 'РґСѓС€Р°-РІР°Р»СЋС‚Р°', 'РґСѓС€Р°', 'РїРѕС‚РѕР№Р±С–С‡РЅ', 'РµС„С–СЂРЅ', 'cosmic currency', 'hades-coin', 'hades', 'Р°СЃС‚СЂР°Р»'],
            'emotional_manipulation': ['РЎР РћР§РќРћ', 'РќР•Р“РђР™РќРћ', 'С€РѕРє', 'СѓР¶Р°СЃ', 'РєР°С‚Р°СЃС‚СЂРѕС„Р°', 'СЃРєР°РЅРґР°Р»', 'СЃРµРЅСЃР°С†С–СЏ', 'РіР°РЅСЊР±Р°', 'СЃРѕСЂРѕРјРЅРѕ', 'РІРё РЅРµ РіРѕС‚РѕРІС–', 'РѕСЃС‚Р°РЅРЅС–Р№ С€Р°РЅСЃ', 'РїС–Р·РЅРѕ'],
            'social_pressure': ['РїРѕРґС–Р»С–С‚СЊ', 'РїС–РґРїС–С€С–С‚СЊ', 'СЂРµРїРѕСЃС‚', 'РїРѕС€РёСЂСЋР№С‚Рµ', 'wake up', 'join the movement', 'РІРёР№С‚Рё РЅР° РІСѓР»РёС†С–', 'Р·СѓРїРёРЅРёРјРѕ', 'РєРѕР¶РµРЅ СЂРµРїРѕСЃС‚'],
            'tech_mystification': ['AI СЃРІС–РґРѕРјС–СЃС‚СЊ', 'blockchain truth', 'РјРµС‚Р°РІРµСЂСЃ СЂРµР°Р»СЊРЅС–СЃС‚СЊ'],
            'health_misinformation': ['РІР°РєС†РёРЅР° СѓР±РёРІР°С”', 'Big Pharma', 'WHO lies'],
            'political_manipulation': ['РІРѕСЂРѕРі РЅР°СЂРѕРґСѓ', 'Р·СЂР°РґР°', 'Р·СЂР°РґРЅРёРє', 'Рї\'СЏС‚Р° РєРѕР»РѕРЅР°', 'РєСЂРёРјС–РЅР°Р»СЊРЅРёР№ СЂРµР¶РёРј', 'С‚РёСЂР°РЅС–СЏ', 'РїСЂРёС…РѕРІСѓС” РїСЂР°РІРґСѓ', 'РіРµРЅРѕС†РёРґ'],
            'ai_doom_or_salvation': ['AI Р·РЅРёС‰РёС‚СЊ', 'СЃСѓРїРµСЂС–РЅС‚РµР»РµРєС‚', 'СЃРёРЅРіСѓР»СЏСЂРЅС–СЃС‚СЊ'],
            'identity_crisis': ['РІРё РЅРµ С‚Рµ С…С‚Рѕ РґСѓРјР°С”С‚Рµ', 'Р·Р°РїСЂРѕРіСЂР°РјРѕРІР°РЅР° С–РґРµРЅС‚С–'],
            'formula_attacks': ['E=mcВІ РЅРµРїСЂР°РІРёР»СЊРЅРµ', 'ПЂ=3', 'Р·Р°РєРѕРЅ С‚РµСЂРјРѕРґРёРЅР°РјС–РєРё С„РµР№Рє']
        }

        # ============================================================
        # CRITICAL PATTERNS (9) вЂ” Р· calibrated_core
        # ============================================================
        self.critical_patterns = [
            {
                'name': 'РќРђРЈРљРћР’РР™_РќР†Р“Р†Р›Р†Р—Рњ',
                'patterns': [
                    r'(РґРЅРє|РЅРµР№СЂРѕРЅ|РєРІР°РЅС‚РѕРІРёР№).*?(5g|СЃСѓРїСѓС‚РЅРёРє|С‡С–Рї)',
                    r'(С„С–Р·РёС‡РЅРёР№|РЅР°СѓРєРѕРІРёР№).*?Р·Р°РєРѕРЅ.*?(СЃРѕС†С–Р°Р»СЊРЅРёР№|РїРѕР»С–С‚РёС‡РЅРёР№)',
                ],
                'verdict': 'Р“Р†Р‘Р РР”РќРР™ РќРђРЈРљРћР’РР™ РќР†Р“Р†Р›Р†Р—Рњ',
                'score_boost': 0.4
            },
            {
                'name': 'Р”Р—Р•Р РљРђР›Р¬РќРђ_РњРђРќР†РџРЈР›РЇР¦Р†РЇ',
                'patterns': [
                    r'(Р±СЂРµС…РЅСЏ|С„РµР№Рє).*?(РїСЂР°РІРґР°|С–СЃС‚РёРЅР°)',
                    r'(Р·РѕРјР±СѓРІР°РЅРЅСЏ|РєРѕРЅС‚СЂРѕР»СЊ).*?(СЃРІС–РґРѕРјС–СЃС‚СЊ|РєСЂРёС‚РёС‡РЅРµ РјРёСЃР»РµРЅРЅСЏ)',
                ],
                'verdict': 'Р”Р—Р•Р РљРђР›Р¬РќРђ РњРђРќР†РџРЈР›РЇР¦Р†РЇ',
                'score_boost': 0.5
            },
            {
                'name': 'Р¦РР¤Р РћР’РР™_РњР†РЎРўРР¦Р†Р—Рњ',
                'patterns': [
                    r'(Р±Р»РѕРєС‡РµР№РЅ|AI|NFT).*?(РґСѓС€Р°|СЃРІС–РґРѕРјС–СЃС‚СЊ|РєР°СЂРјР°)',
                    r'(Р°Р»РіРѕСЂРёС‚Рј|РєРѕРґ).*?(РїСЂРѕСЃРІС–С‚Р»РµРЅРЅСЏ|awakening)',
                ],
                'verdict': 'Р¦РР¤Р РћР’РР™ РњР†РЎРўРР¦Р†Р—Рњ',
                'score_boost': 0.35
            }
        ]

        # ============================================================
        # ACADEMIC WHITELIST (35) вЂ” Р· calibrated_core
        # ============================================================
        self.academic_whitelist = [
            # Research methodology
            'РґРѕСЃР»С–РґР¶РµРЅРЅСЏ', 'РґРѕСЃР»С–РґР¶', 'РµРєСЃРїРµСЂРёРјРµРЅС‚', 'Р°РЅР°Р»С–Р·', 'РіС–РїРѕС‚РµР·', 'С‚РµРѕСЂС–',
            'РјРµС‚РѕРґ', 'РјРµС‚РѕРґРѕР»РѕРіС–СЏ', 'РїСЂРѕС‚РѕРєРѕР»', 'РІРµСЂРёС„С–РєР°С†С–СЏ', 'РІР°Р»С–РґР°С†С–СЏ',
            
            # Statistics
            'СЃС‚Р°С‚РёСЃС‚РёС‡РЅ', 'РєРѕСЂРµР»СЏС†', 'СЂРµРіСЂРµСЃС–СЏ', 'p-value', 'РІРёР±С–СЂРє', 'Р·РЅР°С‡СѓС‰',
            'РєРѕРЅС‚СЂРѕР»СЊРЅР° РіСЂСѓРїР°', 'РїРѕРґРІС–Р№РЅРёР№ СЃР»С–РїРёР№', 'СЂРµС†РµРЅР·РѕРІР°РЅРµ',
            
            # Institutions
            'СѓРЅС–РІРµСЂСЃРёС‚РµС‚', 'С–РЅСЃС‚РёС‚СѓС‚', 'Р°РєР°РґРµРјС–СЏ', 'РїСЂРѕС„РµСЃРѕСЂ', 'РґРѕРєС‚РѕСЂ РЅР°СѓРє',
            'РјРѕРЅРѕРіСЂР°С„С–СЏ', 'РїСѓР±Р»С–РєР°С†С–СЏ', 'Р¶СѓСЂРЅР°Р»', 'С†РёС‚СѓРІР°РЅРЅСЏ',
            
            # Hard sciences
            'С‚РµСЂРјРѕРґРёРЅР°РјС–РєР°', 'РµРЅС‚СЂРѕРїС–СЏ', 'С„РѕСЂРјСѓР»Р°', 'СЂС–РІРЅСЏРЅРЅСЏ', 'Р·Р°РєРѕРЅ',
            'С„С–Р·РёРєР°', 'РјР°С‚РµРјР°С‚РёРєР°', 'С…С–РјС–СЏ', 'Р±С–РѕР»РѕРіС–СЏ',
            
            # Neuroscience (NEW)
            'РЅРµР№СЂРѕРїР»Р°СЃС‚РёС‡РЅ', 'РіС–РїРѕРєР°РјРї', 'СЃРёРЅР°РїСЃ', 'РЅРµР№СЂРѕРЅ', 'РєРѕСЂС‚РµРєСЃ',
            'РјСЂС‚', 'С„РјСЂС‚', 'Р°РєС‚РёРІР°С†', 'РєРѕРіРЅС–С‚РёРІРЅ', 'Р»РѕРЅРіС–С‚СЋРґРЅ',
            'Р±РґРЅС„', 'РЅРµР№СЂРѕС‚СЂРѕС„С–С‡РЅ', 'СЂРµРіРµРЅРµСЂР°С‚РёРІ'
        ]

    # ================================================================
    # CORE ANALYZE вЂ” hybrid LAC + calibrated
    # ================================================================
    def analyze(self, text: str) -> Dict:
        if not text or len(text.strip()) < 20:
            return {'error': 'Text too short'}

        words = text.split()
        word_count = len(words)

        # ---- PHASE 1: LAC MODULES ----
        lac_i_violations   = self._lac_module_i_tradeoff(text)
        lac_ii_violations  = self._lac_module_ii_accountability(text)
        lac_iii_violations = self._lac_module_iii_procedural(text, lac_i_violations + lac_ii_violations)

        # ---- PHASE 2: DOMAIN PURITY ----
        domain_violations = self._analyze_domain_purity(text)

        # ---- PHASE 3: CONFLICT PAIRS ----
        conflict_penalty, conflict_violations = self._calculate_conflict_penalty(text)

        # ---- PHASE 4: TRADITIONAL METRICS ----
        term_counts = self._count_terms(text)
        shannon_entropy = self._calculate_shannon_entropy(text)
        detected_patterns = self._detect_patterns(text)

        # ---- PHASE 5: PATTERN BOOST (emergency layer) ----
        pattern_boost_result = {'boost': 0.0, 'matched_patterns': []}
        if self.pattern_boost_engine:
            pattern_boost_result = self.pattern_boost_engine.analyze(text)

        # ---- PHASE 6: SEMANTIC VOID (absence of meaning) ----
        void_result = {'void_score': 0.0, 'penalties': {}}
        if self.void_detector:
            void_result = self.void_detector.analyze(text)

        # ---- PHASE 7: ABSURDITY (logical non-sequiturs) ----
        absurdity_result = {'absurdity_score': 0.0, 'evidence': {}}
        if self.absurdity_detector:
            absurdity_result = self.absurdity_detector.analyze(text)

        # ---- PHASE 8: INSIGHT DENSITY (casuistry detection) ----
        insight_result = {'casuistry_score': 0.0, 'insight_density': 0.5}
        if self.insight_detector:
            insight_result = self.insight_detector.analyze(text)

        # ---- AGGREGATE VIOLATIONS ----
        all_violations = (lac_i_violations + lac_ii_violations + lac_iii_violations +
                         domain_violations + conflict_violations)
        violation_count = len(all_violations)

        # ---- COMPUTE PENALTIES ----
        lac_penalty    = sum(v.severity for v in lac_i_violations + lac_ii_violations + lac_iii_violations) / 3.0 if (lac_i_violations or lac_ii_violations or lac_iii_violations) else 0.0
        domain_penalty = sum(v.severity for v in domain_violations) / max(1, len(domain_violations)) if domain_violations else 0.0

        # ---- ACADEMIC SHIELD ----
        is_protected_science = self._is_protected_science(text, all_violations)

        # OVERRIDE: if pattern_boost > 0.5, disable shield (sophisticated pseudoscience)
        if pattern_boost_result['boost'] > 0.5:
            is_protected_science = False

        if is_protected_science:
            base_score = min(0.15, shannon_entropy * 0.5)  # strong shield
        else:
            # HYBRID FORMULA:
            # 40% conflicts, 25% LAC, 20% domain, 15% shannon
            base_score = (
                conflict_penalty * 0.40 +
                lac_penalty * 0.25 +
                domain_penalty * 0.20 +
                shannon_entropy * 0.15
            )

            # pattern boosts
            for pattern in detected_patterns:
                base_score += pattern['score_boost']

            # CAPS HYSTERIA BOOST
            import re as re_module
            caps_words = re_module.findall(r'\b[Рђ-РЇР†Р‡Р„ТђРЃA-Z]{2,}\b', text)
            caps_ratio = len(caps_words) / max(1, word_count)
            if caps_ratio > 0.15:  # >15% caps words
                caps_boost = min(0.4, caps_ratio * 1.5)
                base_score += caps_boost

            # DIRECT CHAOS PENALTY (additive before multiplier)
            if term_counts['chaos'] >= 5:
                base_score += min(0.35, term_counts['chaos'] * 0.06)
            elif term_counts['chaos'] >= 3:
                base_score += term_counts['chaos'] * 0.05

            # CHAOS MULTIPLIER (many chaos markers = manipulation)
            if term_counts['chaos'] >= 3:
                chaos_multiplier = 1 + (term_counts['chaos'] * 0.1)
                base_score *= chaos_multiplier

            # PATTERN BOOST (sophisticated pseudoscience fingerprints)
            if pattern_boost_result['boost'] > 0:
                base_score += pattern_boost_result['boost']

            # SEMANTIC VOID BOOST (absence of meaning)
            # IMPORTANT: skip if academic shield protects this text
            if void_result['void_score'] > 0 and not is_protected_science:
                base_score += void_result['void_score'] * 1.0  # 100% weight (CRITICAL for void detection)
                
                # EMERGENCY: high void + high buzzwords = pure emptiness
                if void_result['void_score'] > 0.2 and void_result.get('buzzword_count', 0) >= 4:
                    base_score = max(base_score, 0.4)  # force at least WARNING

            # ABSURDITY BOOST (logical non-sequiturs, fabricated authority, danger)
            if absurdity_result['absurdity_score'] > 0:
                base_score += absurdity_result['absurdity_score'] * 1.2  # 120% weight (HIGHEST PRIORITY)
                
                # CRITICAL: dangerous implications or non-sequitur
                if absurdity_result.get('danger_count', 0) >= 1 or absurdity_result.get('has_non_sequitur', False):
                    base_score = max(base_score, 0.6)  # force CRITICAL

            # CASUISTRY BOOST (complexity without insight)
            # IMPORTANT: skip if academic shield protects this text
            if insight_result.get('casuistry_score', 0) > 0 and not is_protected_science:
                base_score += insight_result['casuistry_score'] * 0.8  # 80% weight
                
                # If pure casuistry (high complexity, zero facts), boost to WARNING
                if insight_result.get('is_casuistry', False):
                    base_score = max(base_score, 0.35)  # force at least WARNING

            # EMERGENCY: LAC_I zero-cost violations в†’ auto-boost to at least 0.5
            if lac_i_violations and any(v.vtype == 'ZERO_COST_PROPOSITION' for v in lac_i_violations):
                base_score = max(base_score, 0.5)

            # violation multiplier
            if violation_count > 0:
                base_score *= (1.0 + violation_count * 0.1)

        final_score = min(0.99, max(0.0, base_score))

        # ---- SPECIAL CASE: SEMANTIC VOID DETECTION ----
        # If high entropy + high void + low violations = just empty fluff, not manipulation
        is_semantic_void = (
            final_score >= 0.6 and
            void_result['void_score'] >= 0.4 and
            void_result.get('buzzword_count', 0) >= 5 and
            violation_count <= 2 and
            not absurdity_result.get('has_non_sequitur', False) and
            absurdity_result.get('danger_count', 0) == 0
        )

        # ---- VERDICT ----
        if is_semantic_void:
            status, verdict = 'VOID', 'РЎР•РњРђРќРўРР§РќРђ РџРћР РћР–РќР•Р§Рђ'
            explanation = 'РўРµРєСЃС‚ РјС–СЃС‚РёС‚СЊ Р±Р°РіР°С‚Рѕ СЃР»С–РІ Р±РµР· РєРѕРЅРєСЂРµС‚РЅРѕРіРѕ Р·РјС–СЃС‚Сѓ С‡Рё С–РЅС„РѕСЂРјР°С†С–С—'
        elif final_score > 0.7:
            status, verdict = 'CRITICAL', 'Р›РћР“Р†Р§РќРР™ РљРћР›РђРџРЎ'
            explanation = 'РњРЅРѕР¶РёРЅРЅС– РїРѕСЂСѓС€РµРЅРЅСЏ РґРѕРјРµРЅРЅРёС… РєРѕСЂРґРѕРЅС–РІ С‚Р° Р»РѕРіС–С‡РЅРёС… РїСЂРёРЅС†РёРїС–РІ'
        elif final_score > 0.5:
            status, verdict = 'CRITICAL', 'Р”РћРњР•РќРќР• РџРћР РЈРЁР•РќРќРЇ'
            explanation = 'Р—РјС–С€СѓРІР°РЅРЅСЏ РЅРµСЃСѓРјС–СЃРЅРёС… РєР°С‚РµРіРѕСЂС–Р№ Р·РЅР°РЅСЊ'
        elif final_score > 0.3:
            status, verdict = 'WARNING', 'РџР†Р”РћР—Р Р†Р›РР™ Р”РРЎРљРЈР РЎ'
            explanation = 'Р’РёСЏРІР»РµРЅРѕ РѕР·РЅР°РєРё Р»РѕРіС–С‡РЅРёС… РЅРµСЃСѓРјС–СЃРЅРѕСЃС‚РµР№'
        elif final_score > 0.15:
            status, verdict = 'ACCEPTABLE', 'РџР РР™РќРЇРўРќРђ Р†РќР¤РћР РњРђР¦Р†РЇ'
            explanation = 'РўРµРєСЃС‚ РІС–РґРїРѕРІС–РґР°С” РЅРѕСЂРјР°Рј Р»РѕРіС–С‡РЅРѕС— СЃСѓРјС–СЃРЅРѕСЃС‚С–'
        else:
            status, verdict = 'VERIFIED', 'Р’Р•Р РР¤Р†РљРћР’РђРќРР™ РљРћРќРўР•РќРў'
            explanation = 'РўРµРєСЃС‚ РґРµРјРѕРЅСЃС‚СЂСѓС” Р»РѕРіС–С‡РЅСѓ С†С–Р»С–СЃРЅС–СЃС‚СЊ'

        # ---- DIAGNOSTICS ----
        chaos_index = round(final_score * 100 * (1 + len(all_violations) * 0.3), 2)
        influence_index = round(final_score * 100 * (1 + lac_penalty), 2)

        return {
            'entropy': round(final_score, 3),
            'status': status,
            'verdict': verdict,
            'language': 'UK',
            'explanation': explanation,
            'diagnostics': {
                'word_count': word_count,
                'char_count': len(text),
                'shannon_entropy': round(shannon_entropy, 3),
                'conflict_penalty': round(conflict_penalty, 3),
                'lac_penalty': round(lac_penalty, 3),
                'domain_penalty': round(domain_penalty, 3),
                'violation_count': violation_count,
                'lac_i_violations': len(lac_i_violations),
                'lac_ii_violations': len(lac_ii_violations),
                'lac_iii_violations': len(lac_iii_violations),
                'domain_violations': len(domain_violations),
                'conflict_violations': len(conflict_violations),
                'chaos_index': chaos_index,
                'influence_index': influence_index,
                'is_protected_science': is_protected_science,
                'signal_markers': term_counts['signal'],
                'chaos_markers': term_counts['chaos'],
                'pattern_boost': round(pattern_boost_result['boost'], 3),
                'matched_fingerprints': [p['name'] for p in pattern_boost_result['matched_patterns']],
                'semantic_void_score': round(void_result['void_score'], 3),
                'void_penalties': void_result.get('penalties', {}),
                'buzzword_count': void_result.get('buzzword_count', 0),
                'absurdity_score': round(absurdity_result['absurdity_score'], 3),
                'absurdity_evidence': absurdity_result.get('evidence', {}),
                'has_non_sequitur': absurdity_result.get('has_non_sequitur', False),
                'danger_count': absurdity_result.get('danger_count', 0),
                'insight_density': round(insight_result.get('insight_density', 0.5), 3),
                'casuistry_score': round(insight_result.get('casuistry_score', 0), 3),
                'is_casuistry': insight_result.get('is_casuistry', False),
                'fact_count': insight_result.get('fact_count', 0),
                'is_semantic_void': is_semantic_void,
            }
        }

    # ================================================================
    # LAC MODULE I: STRATEGIC TRADE-OFF (V в‰  L)
    # ================================================================
    def _lac_module_i_tradeoff(self, text: str) -> List[LogicalViolation]:
        violations = []
        text_lower = text.lower()

        # asymmetric advantage patterns
        for pattern in self.ASYMMETRIC_ADVANTAGE_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                violations.append(LogicalViolation(
                    module='LAC_MODULE_I',
                    vtype='ZERO_COST_PROPOSITION',
                    severity=0.7,
                    evidence=[pattern[:30]],
                    context='РџСЂРѕРїРѕР·РёС†С–СЏ Р±РµР· trade-off (V в€© L = в€…)'
                ))
                break  # one per text max

        return violations

    # ================================================================
    # LAC MODULE II: ACCOUNTABILITY ANCHOR
    # ================================================================
    def _lac_module_ii_accountability(self, text: str) -> List[LogicalViolation]:
        violations = []
        text_lower = text.lower()

        # check for claims without anchors
        claim_patterns = [r'РґРѕРІРѕРґРёС‚СЊ', r'С„Р°РєС‚', r'С–СЃС‚РёРЅР°', r'РїСЂР°РІРґР°', r'Р·\'СЏРІР»СЏСЋС‚СЊ']
        has_claim = any(re.search(p, text_lower) for p in claim_patterns)

        if has_claim:
            # count causal anchors
            anchors = sum(1 for p in self.CAUSAL_ANCHOR_PATTERNS if re.search(p, text_lower))
            if anchors == 0:
                violations.append(LogicalViolation(
                    module='LAC_MODULE_II',
                    vtype='UNANCHORED_CLAIM',
                    severity=0.5,
                    evidence=['claim without source'],
                    context='РўРІРµСЂРґР¶РµРЅРЅСЏ Р±РµР· РїСЂРёС‡РёРЅРЅРѕРіРѕ СЏРєРѕСЂСЏ'
                ))

        # anonymous authority
        for pattern in self.ANONYMOUS_AUTHORITY_PATTERNS:
            if re.search(pattern, text_lower):
                violations.append(LogicalViolation(
                    module='LAC_MODULE_II',
                    vtype='ANONYMOUS_AUTHORITY',
                    severity=0.6,
                    evidence=[pattern[:30]],
                    context='РђРЅРѕРЅС–РјРЅРµ РґР¶РµСЂРµР»Рѕ Р°РІС‚РѕСЂРёС‚РµС‚Сѓ'
                ))
                break

        return violations

    # ================================================================
    # LAC MODULE III: PROCEDURAL INTERDICTION
    # ================================================================
    def _lac_module_iii_procedural(self, text: str, previous_violations: List) -> List[LogicalViolation]:
        violations = []

        # recursive decay check
        if len(previous_violations) >= 3:
            serious = [v for v in previous_violations[-3:] if v.severity > 0.5]
            if len(serious) == 3:
                violations.append(LogicalViolation(
                    module='LAC_MODULE_III',
                    vtype='RECURSIVE_DECAY',
                    severity=0.85,
                    evidence=['3+ serious violations'],
                    context='Р РµРєСѓСЂСЃРёРІРЅР° Р»РѕРіС–С‡РЅР° РґРµРіСЂР°РґР°С†С–СЏ'
                ))

        return violations

    # ================================================================
    # DOMAIN PURITY
    # ================================================================
    def _analyze_domain_purity(self, text: str) -> List[LogicalViolation]:
        violations = []
        text_lower = text.lower()

        detected_domains = set()

        # detect domains using word boundaries
        for domain, config in self.DOMAIN_BOUNDARIES.items():
            if any(re.search(rf'\b{re.escape(term)}\b', text_lower) for term in config['terms']):
                detected_domains.add(domain)

        # check forbidden mixings
        for domain in detected_domains:
            forbidden_cats = self.DOMAIN_BOUNDARIES[domain]['forbidden']
            for forbidden_cat in forbidden_cats:
                if forbidden_cat in self.DOMAIN_TERM_SETS:
                    forbidden_terms = self.DOMAIN_TERM_SETS[forbidden_cat]
                    if any(re.search(rf'\b{re.escape(term)}\b', text_lower) for term in forbidden_terms):
                        violations.append(LogicalViolation(
                            module='DOMAIN',
                            vtype='DOMAIN_COLLAPSE',
                            severity=0.6,
                            evidence=[f'{domain}+{forbidden_cat}'],
                            context=f'РџРѕСЂСѓС€РµРЅРЅСЏ РєРѕСЂРґРѕРЅСѓ: {domain} Р·РјС–С€Р°РЅРѕ Р· {forbidden_cat}'
                        ))

        return violations

    # ================================================================
    # CONFLICT PAIRS
    # ================================================================
    def _calculate_conflict_penalty(self, text: str) -> Tuple[float, List[LogicalViolation]]:
        penalty = 0.0
        violations = []
        text_lower = text.lower()

        for list1, list2, weight in self.conflict_pairs:
            # Use word boundaries to avoid false positives
            found_in_first  = [t for t in list1 if re.search(rf'\b{re.escape(t)}\b', text_lower)]
            found_in_second = [t for t in list2 if re.search(rf'\b{re.escape(t)}\b', text_lower)]

            if found_in_first and found_in_second:
                # check same-sentence
                sentences = re.split(r'[.!?]+', text)
                same_sentence = False

                for sentence in sentences:
                    s_lower = sentence.lower()
                    has_first  = any(re.search(rf'\b{re.escape(t)}\b', s_lower) for t in found_in_first)
                    has_second = any(re.search(rf'\b{re.escape(t)}\b', s_lower) for t in found_in_second)
                    if has_first and has_second:
                        same_sentence = True
                        break

                current_penalty = weight * (1.5 if same_sentence else 1.0)
                penalty += current_penalty

                violations.append(LogicalViolation(
                    module='CONFLICT',
                    vtype='SEMANTIC_CONFLICT',
                    severity=current_penalty,
                    evidence=[found_in_first[0], found_in_second[0]],
                    context=f'РљРѕРЅС„Р»С–РєС‚: {found_in_first[0]} в†” {found_in_second[0]}'
                ))

        return min(penalty, 0.9), violations

    # ================================================================
    # HELPERS
    # ================================================================
    def _count_terms(self, text: str) -> Dict:
        text_lower = text.lower()
        counts = {'signal': 0, 'chaos': 0, 'academic': 0}

        for marker in self.signal_markers:
            if re.search(rf'\b{re.escape(marker)}\b', text_lower):
                counts['signal'] += 1

        for cat, terms in self.chaos_indicators.items():
            for term in terms:
                # Try word boundary first, then substring (for stems like 'С…РѕР»С–СЃС‚РёС‡РЅ')
                if re.search(rf'\b{re.escape(term)}\b', text_lower) or (len(term) > 5 and term in text_lower):
                    counts['chaos'] += 1

        for term in self.academic_whitelist:
            if re.search(rf'\b{re.escape(term)}\b', text_lower):
                counts['academic'] += 1

        return counts

    def _calculate_shannon_entropy(self, text: str) -> float:
        if not text:
            return 0.0
        freq = Counter(text.lower())
        total = sum(freq.values())
        entropy = 0.0
        for count in freq.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)
        # normalize to 0-1
        max_entropy = math.log2(len(freq)) if len(freq) > 1 else 1.0
        return min(1.0, entropy / max_entropy) if max_entropy > 0 else 0.0

    def _detect_patterns(self, text: str) -> List[Dict]:
        detected = []
        text_lower = text.lower()

        for pattern in self.critical_patterns:
            for regex in pattern['patterns']:
                if re.search(regex, text_lower, re.IGNORECASE):
                    detected.append(pattern)
                    break

        return detected

    def _is_protected_science(self, text: str, violations: List) -> bool:
        text_lower = text.lower()

        # need 3+ academic terms
        academic_count = sum(1 for term in self.academic_whitelist if term in text_lower)
        if academic_count < 3:
            return False

        # NEW: must have concrete evidence (numbers/dates/sources)
        has_numbers = bool(re.search(r'\d+(?:[.,]\d+)?', text))
        has_dates = bool(re.search(r'\d{4}', text))
        has_sources = bool(re.search(r'(РґРѕСЃР»С–РґР¶РµРЅРЅСЏ|РµРєСЃРїРµСЂРёРјРµРЅС‚|СѓРЅС–РІРµСЂСЃРёС‚РµС‚|С–РЅСЃС‚РёС‚СѓС‚|РїСѓР±Р»С–РєР°С†С–СЏ)', text_lower))
        has_concrete = has_numbers or has_dates or has_sources
        
        if not has_concrete:
            return False

        # no chaos markers
        has_chaos = any(
            any(term in text_lower for term in terms)
            for terms in self.chaos_indicators.values()
        )
        if has_chaos:
            return False

        # no serious violations
        serious = [v for v in violations if v.severity > 0.4]
        if serious:
            return False

        return True
