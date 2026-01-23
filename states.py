"""
Veritas Protocol — Finite State Machine (FSM) Definition
Цей файл визначає детерміновані стани системи згідно з принципами Witness Silence.
"""

from enum import Enum, auto

class SystemState(Enum):
    """Детерміновані стани системи Veritas."""
    LAMINAR_FLOW = auto()      # Стабільний стан, ентропія низька
    SYSTEMIC_FATIGUE = auto()  # Підвищена ентропія, попередження
    WITNESS_SILENCE = auto()   # Критична ентропія, мовчання
    ERROR = auto()             # Технічна помилка

# Простий словник для швидкого доступу до станів за іменем
STATES = {
    "LAMINAR_FLOW": SystemState.LAMINAR_FLOW,
    "SYSTEMIC_FATIGUE": SystemState.SYSTEMIC_FATIGUE,
    "WITNESS_SILENCE": SystemState.WITNESS_SILENCE,
    "ERROR": SystemState.ERROR
}

def get_state_by_esi(esi_value: float) -> SystemState:
    """
    Детермінована функція для отримання стану системи на основі ESI.
    Відповідає таблиці 1 з оригінального паперу.
    """
    if esi_value < 0.3:
        return SystemState.LAMINAR_FLOW
    elif 0.3 <= esi_value <= 0.7:
        return SystemState.SYSTEMIC_FATIGUE
    else:  # esi_value > 0.7
        return SystemState.WITNESS_SILENCE

def get_state_name(state: SystemState) -> str:
    """Повертає читабельну назву стану."""
    return state.name.replace('_', ' ').title()

# Функція для інтеграції з VeritasCore (додаємо ESI-логіку в репутацію)
def calculate_state_from_reputation(reputation: float) -> SystemState:
    """
    Визначає стан системи на основі репутації джерела.
    Це дозволяє зв'язати економічну модель з FSM.
    """
    if reputation >= 0.7:
        return SystemState.LAMINAR_FLOW
    elif 0.4 <= reputation < 0.7:
        return SystemState.SYSTEMIC_FATIGUE
    else:  # reputation < 0.4
        return SystemState.WITNESS_SILENCE

if __name__ == "__main__":
    # Проста перевірка логіки
    print("=== Veritas Protocol FSM Tester ===")
    
    # Тестуємо ESI-логіку
    test_values = [0.1, 0.5, 0.9]
    for val in test_values:
        state = get_state_by_esi(val)
        print(f"ESI={val} -> {state.name} ({get_state_name(state)})")
    
    print("\n" + "="*40)
    
    # Тестуємо репутаційну логіку
    test_reputations = [0.8, 0.6, 0.2]
    for rep in test_reputations:
        state = calculate_state_from_reputation(rep)
        print(f"Reputation={rep} -> {state.name}")
