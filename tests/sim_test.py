# VERITAS PROTOCOL - СИМУЛЯТОР АТАКИ 51%
import random

def run_simulation():
    print("--- ЗАПУСК VERITAS PROTOCOL: КЕЙС ТРУХАНІВ ОСТРІВ ---")
    
    # 1. Створюємо "Чесних Місцевих" (їх мало, але вони надійні)
    honest_reputation = 0.95
    honest_count = 10
    
    # 2. Створюємо "Армію Ботів" (їх багато, вони кажуть неправду)
    bot_reputation = 0.15
    bot_count = 100
    
    print(f"Ситуація: {honest_count} людей на острові кажуть 'Тихо'.")
    print(f"Ситуація: {bot_count} ботів у мережі кричать 'ТАМ ВИБУХ!'.")
    print("-" * 40)

    # Розрахунок сили голосу
    honest_power = honest_count * honest_reputation
    bot_power = bot_count * bot_reputation
    
    total_power = honest_power + bot_power
    truth_index = (honest_power / total_power) * 100

    print(f"Вага правди (люди): {honest_power:.2f}")
    print(f"Вага фейку (боти): {bot_power:.2f}")

    # 3. МЕХАНІЗМ VERITAS (Slashing)
    if bot_power > honest_power:
        print("\nУВАГА: Боти тимчасово перемагають! Система фіксує АНОМАЛІЮ.")
        print("Запуск механізму Reputation Slashing...")
        
        # ШТРАФ: Репутація ботів падає в 10 разів
        new_bot_reputation = bot_reputation / 10
        new_bot_power = bot_count * new_bot_reputation
        
        print(f"РЕЗУЛЬТАТ: Репутація ботів знищена. Тепер їхня сила: {new_bot_power:.2f}")
        print("ПЕРЕМОГА: Істина відновлена, боти заблоковані.")
    else:
        print("\nСИСТЕМА СТІЙКА: Вага репутації людей виявилася вищою за натовп ботів.")

run_simulation()
