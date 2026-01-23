"""
News Verifier - Core script for the Veritas Protocol.
Uses the full VeritasCore engine for Logic Authenticity Check (LAC).
"""

import pandas as pd
from pathlib import Path
from veritas_core import VeritasCore

def main():
    print("\n" + "="*60)
    print("VERITAS PROTOCOL - News Verifier v1.2")
    print("="*60)
    
    # 1. Ініціалізуємо рушій Veritas
    print("[Ініціалізація VeritasCore...]")
    veritas_engine = VeritasCore()
    print(f"Завантажено реєстр репутацій: {list(veritas_engine.reputation_registry.keys())}")
    
    # 2. Спроба прочитати та обробити дані з sample_data.csv
    data_file = Path("sample_data.csv")
    if data_file.exists():
        try:
            df = pd.read_csv(data_file)
            print(f"\n[INFO] Завантажено тестові дані з {len(df)} рядків.")
            print("-"*40)
            
            # Запускаємо LAC для кожного заголовка в файлі
            for index, row in df.iterrows():
                print(f"\nАналіз {index+1}: {row['headline'][:50]}...")
                print(f"Джерело (для тесту): {row.get('source', 'Unknown_Source')}")
                
                # Використовуємо СПРАВЖНЮ логіку LAC з VeritasCore
                result = veritas_engine.evaluate_integrity(
                    text=row['headline'],
                    source=row.get('source', 'Unknown_Source')
                )
                
                print(f"  Статус: {result['status']}")
                print(f"  Нова репутація: {result['new_reputation']}")
                
        except Exception as e:
            print(f"[ERROR] Помилка читання даних: {e}")
    else:
        print(f"\n[INFO] Файл 'sample_data.csv' не знайдено. Перехожу в демонстраційний режим.")
        print("-"*40)
        
        # Демонстраційна перевірка з використанням реального рушія
        test_cases = [
            ("Призначення Шевчука етично необхідне", "Prosecutor_Council_UA"),
            ("Стандарти AI необхідно посилити", "Ethical_Council_UA"),
            ("Новини про мирні перемовини", "Unknown_Source")
        ]
        
        for text, source in test_cases:
            print(f"\nТест: '{text[:30]}...'")
            result = veritas_engine.evaluate_integrity(text, source)
            print(f"  Джерело: {source}")
            print(f"  Статус: {result['status']}")
            print(f"  Репутація: {result['new_reputation']}")
    
    # 3. Фінальний статус
    print("\n" + "="*60)
    print("[OK] Veritas Protocol News Verifier працює на повній архітектурі.")
    print("="*60)
    print("\nНаступні кроки:")
    print("1. Додайте реальні дані до 'sample_data.csv'")
    print("2. Використовуйте 'event_processor.py' для обробки потокових подій")
    print("3. Перевірте підсумковий реєстр репутацій:")
    
    for node, rep in veritas_engine.reputation_registry.items():
        status = "✅ СТАБІЛЬНИЙ" if rep >= 0.4 else "⚠️ НИЗЬКА" if rep >= 0.3 else "⛔ КРИТИЧНА"
        print(f"   - {node}: {rep} ({status})")

if __name__ == "__main__":
    main()
