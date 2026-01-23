"""
VERITAS EVENT PROCESSOR
Цей скрипт обробляє події, використовуючи справжній рушій VeritasCore.
"""

# Імпортуємо справжній клас ядра для оцінки
from veritas_core import VeritasCore

def process_event(event_name, source_node):
    """
    Обробляє подію через Logic Authenticity Check (LAC).
    
    Args:
        event_name (str): Назва або опис події (текст для аналізу).
        source_node (str): Назва джерела/вузла (має бути в реєстрі репутацій).
    """
    print(f"\n{'='*50}")
    print(f"ОБРОБКА ПОДІЇ: {event_name}")
    print(f"ДЖЕРЕЛО: {source_node}")
    print(f"{'='*50}")
    
    # 1. Створюємо екземпляр рушія Veritas
    veritas_engine = VeritasCore()
    
    # 2. Отримуємо поточну репутацію джерела (для інформації)
    current_rep = veritas_engine.reputation_registry.get(source_node, 0.5)
    print(f"ПОЧАТКОВА РЕПУТАЦІЯ ВУЗЛА: {current_rep}")
    
    # 3. ЗАПУСКАЄМО СПРАВЖНЮ ПЕРЕВІРКУ LAC
    print("\n[ЗАПУСК LAC...]")
    result = veritas_engine.evaluate_integrity(event_name, source_node)
    
    # 4. Виводимо результат перевірки
    print("\n[РЕЗУЛЬТАТ ПЕРЕВІРКИ]")
    print(f"Статус: {result['status']}")
    print(f"Нова репутація вузла: {result['new_reputation']}")
    print(f"Потрібне втручання: {'ТАК' if result['intervention_required'] else 'НІ'}")
    
    # 5. Приймаємо рішення на основі результату
    print("\n[РОШЕННЯ СИСТЕМИ]")
    if result['status'] == "REJECTED":
        print("⛔ Подія відхилена. Запуск протоколу Slashing (штраф репутації).")
    else:
        print("✅ Подія стабільна. Генеруємо 'Паспорт Правди'...")
        print("-" * 30)
        print(f"ID: {event_name[:8].upper()}-{hash(event_name) % 10000:04d}")
        print("Статус: VERIFIED")
        print("-" * 30)


# ДЕМОНСТРАЦІЯ РОБОТИ З РІЗНИМИ ДЖЕРЕЛАМИ
if __name__ == "__main__":
    print("\n" + "="*60)
    print("VERITAS PROTOCOL v1.2-alpha | ДЕМО РОБОТИ EVENT PROCESSOR")
    print("="*60)
    
    # Тест 1: Подія від джерела з низькою репутацією
    process_event("Призначення Шевчука етично необхідне", "Prosecutor_Council_UA")
    
    # Тест 2: Подія від джерела з високою репутацією
    process_event("Стандарти етики AI необхідно посилити", "Ethical_Council_UA")
    
    # Тест 3: Подія від нового, невідомого джерела
    process_event("Новини про мирні перемовини", "Unknown_Source")
