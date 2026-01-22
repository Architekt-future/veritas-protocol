# VERITAS EVENT PROCESSOR
# Цей скрипт імітує роботу всього протоколу

def process_event(event_name, source_reputation, is_anomaly):
    print(f"--- ОБРОБКА ПОДІЇ: {event_name} ---")
    
    # 1. Перевіряємо репутацію джерела
    if source_reputation < 0.5:
        print("Результат: Джерело має низьку довіру. Потрібна додаткова перевірка.")
        return
    
    # 2. Якщо це аномалія (наприклад, з довідника docs/)
    if is_anomaly:
        print("Результат: ВИЯВЛЕНО АНОМАЛІЮ (ASI). Запуск протоколу Slashing...")
        print("СТАТУС: Подію заблоковано.")
    else:
        # 3. Якщо все добре - видаємо "Паспорт Правди" (як у templates/)
        print("Результат: ПЕРЕВІРЕНО. Подія відповідає реальності.")
        print("-" * 30)
        print("ГЕНЕРУЄМО ПАСПОРТ ПРАВДИ:")
        print(f"ID: {event_name[:3].upper()}-2026")
        print("Статус: VERIFIED")
        print("-" * 30)

# ДАВАЙ ПЕРЕВІРИМО 2 ВАРІАНТИ:
# Варіант А: Чесна подія
process_event("Мітинг на Печерську", 0.9, False)

print("\n")

# Варіант Б: Атака ботів (Аномалія)
process_event("Фейковий вибух", 0.2, True)
