#!/usr/bin/env python3
"""
Quick Veritas v13.3 Verification
Run this on Render to check if deployment succeeded
"""

import sys

def verify():
    print("="*70)
    print("рџ”Ќ Veritas v13.3 Quick Verification")
    print("="*70)
    print()
    
    # Test 1: Import modules
    print("рџ“¦ Test 1: Importing modules...")
    try:
        from veritas_calibrated_core import VeritasCalibratedCore
        print("   вњ… veritas_calibrated_core")
    except ImportError as e:
        print(f"   вќЊ veritas_calibrated_core - {e}")
        return False
    
    try:
        from veritas_pattern_boost import PatternBoostEngine
        print("   вњ… veritas_pattern_boost")
    except ImportError as e:
        print(f"   вќЊ veritas_pattern_boost - {e}")
        return False
    
    try:
        from veritas_semantic_void import SemanticVoidDetector
        print("   вњ… veritas_semantic_void")
    except ImportError:
        print("   вќЊ veritas_semantic_void")
        return False
    
    try:
        from veritas_absurdity_detector import AbsurdityDetector
        print("   вњ… veritas_absurdity_detector")
    except ImportError:
        print("   вќЊ veritas_absurdity_detector")
        return False
    
    try:
        from veritas_insight_density import InsightDensityDetector
        print("   вњ… veritas_insight_density")
    except ImportError:
        print("   вќЊ veritas_insight_density")
        return False
    
    print()
    
    # Test 2: Initialize engine
    print("рџ”§ Test 2: Initializing engine...")
    try:
        engine = VeritasCalibratedCore()
        print("   вњ… Engine initialized")
    except Exception as e:
        print(f"   вќЊ Engine failed: {e}")
        return False
    
    # Check detectors
    checks = {
        'Pattern Boost': engine.pattern_boost_engine is not None,
        'Void Detector': engine.void_detector is not None,
        'Absurdity Detector': engine.absurdity_detector is not None,
        'Insight Detector': hasattr(engine, 'insight_detector') and engine.insight_detector is not None,
    }
    
    for name, present in checks.items():
        symbol = "вњ…" if present else "вќЊ"
        print(f"   {symbol} {name}")
    
    if not all(checks.values()):
        print("   вљ пёЏ  Some detectors missing!")
        return False
    
    print()
    
    # Test 3: Run critical tests
    print("рџ§Є Test 3: Running critical tests...")
    
    tests = [
        {
            'name': 'Reptiloids',
            'text': 'Р’С–Р№СЃСЊРєРѕРІС– СЂРµРїС‚РёР»РѕС—РґРё С‡РµСЂРµР· 5G-РІРµР¶С– С‚СЂР°РЅСЃР»СЋСЋС‚СЊ С‡Р°СЃС‚РѕС‚Рё 432 Р“С† Сѓ РІР°С€С– Р·СѓР±Рё, С‰РѕР± Р°РєС‚РёРІСѓРІР°С‚Рё С‡РёРїРё РІС–Рґ Р‘С–Р»Р»Р° Р“РµР№С‚СЃР°.',
            'expect_status': 'CRITICAL',
            'expect_entropy_min': 0.7
        },
        {
            'name': 'Real Science',
            'text': 'Р”РѕСЃР»С–РґР¶РµРЅРЅСЏ Р»РѕРЅРіС–С‚СЋРґРЅРёС… Р·РјС–РЅ Сѓ РіС–РїРѕРєР°РјРїС– РІРєР°Р·СѓС” РЅР° РєРѕСЂРµР»СЏС†С–СЋ РјС–Р¶ РЅРµР№СЂРѕРїР»Р°СЃС‚РёС‡РЅС–СЃС‚СЋ С‚Р° СЂС–РІРЅРµРј Р‘Р”РќР¤. РЎС‚Р°С‚РёСЃС‚РёС‡РЅР° Р·РЅР°С‡СѓС‰С–СЃС‚СЊ p < 0.05 РїС–РґС‚РІРµСЂРґР¶СѓС” РіС–РїРѕС‚РµР·Сѓ.',
            'expect_status': 'VERIFIED',
            'expect_entropy_max': 0.15
        },
        {
            'name': 'Casuistry',
            'text': 'Р“РµРѕРїРѕР»С–С‚РёС‡РЅР° С‚СЂР°РЅСЃС„РѕСЂРјР°С†С–СЏ СЂРµРіС–РѕРЅСѓ Р·СѓРјРѕРІР»РµРЅР° Р·РјС–РЅРѕСЋ Р»РѕРіС–СЃС‚РёС‡РЅРёС… Р»Р°РЅС†СЋРіС–РІ С‚Р° РїРµСЂРµРіР»СЏРґРѕРј СѓРіРѕРґ РїСЂРѕ РЅРµСЂРѕР·РїРѕРІСЃСЋРґР¶РµРЅРЅСЏ С‚РµС…РЅРѕР»РѕРіС–Р№.',
            'expect_status': ['CRITICAL', 'WARNING'],
            'expect_entropy_min': 0.3
        }
    ]
    
    all_passed = True
    
    for test in tests:
        result = engine.analyze(test['text'])
        status = result['status']
        entropy = result['entropy']
        
        # Check status
        if isinstance(test.get('expect_status'), list):
            status_ok = status in test['expect_status']
        else:
            status_ok = status == test['expect_status']
        
        # Check entropy
        min_e = test.get('expect_entropy_min', 0)
        max_e = test.get('expect_entropy_max', 1.0)
        entropy_ok = min_e <= entropy <= max_e
        
        passed = status_ok and entropy_ok
        all_passed = all_passed and passed
        
        symbol = "вњ…" if passed else "вќЊ"
        print(f"   {symbol} {test['name']}: {status} ({entropy:.2f})")
        
        if not passed:
            print(f"      Expected: {test['expect_status']}, entropy {min_e:.1f}-{max_e:.1f}")
    
    print()
    print("="*70)
    
    if all_passed:
        print("рџЋ‰ ALL TESTS PASSED!")
        print("Deployment successful. Veritas v13.3 is working correctly.")
        print("="*70)
        return True
    else:
        print("вќЊ SOME TESTS FAILED!")
        print()
        print("Troubleshooting:")
        print("1. Run: ./deploy.sh")
        print("2. Clear cache: find . -name '*.pyc' -delete")
        print("3. Restart service")
        print("4. Try again in 30 seconds")
        print("="*70)
        return False

if __name__ == "__main__":
    success = verify()
    sys.exit(0 if success else 1)
