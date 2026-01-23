"""
Veritas Protocol — Finite State Machine (FSM) Definition
Цей файл визначає детерміновані стани системи згідно з принципами Witness Silence.
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional

class SystemState(Enum):
    """Детерміновані стани системи Veritas."""
    LAMINAR_FLOW = auto()      # Стабільний стан, ентропія низька
    SYSTEMIC_FATIGUE = auto()  # Підвищена ентропія, попередження
    WITNESS_SILENCE = auto()   # Критична ентропія, мовчання
    ERROR = auto()             # Технічна помилка

@dataclass
class StateTransition:
    """Правило переходу між станами."""
    from_state: SystemState
    to_state: SystemState
    condition: str  # Опис умови людською мовою
    threshold: float  # Числовий поріг (наприклад, ESI > 0.7)

# Детерміновані правила переходів згідно з папером
TRANSITION_RULES = [
    StateTransition(
        from_state=SystemState.LAMINAR_FLOW,
        to_state=SystemState.SYSTEMIC_FATIGUE,
        condition="ESI виходить за межі стабільного діапазону (0.3)",
        threshold=0.3
    ),
    StateTransition(
        from_state=SystemState.SYSTEMIC_FATIGUE,
        to_state=SystemState.WITNESS_SILENCE,
        condition="ESI перевищує критичний поріг (0.7)",
        threshold=0.7
    ),
    StateTransition(
        from_state=SystemState.WITNESS_SILENCE,
        to_state=SystemState.LAMINAR_FLOW,
        condition="ESI повертається до нормального рівня та ручне підтвердження",
        threshold=0.3
    ),
]

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

if __name__ == "__main__":
    # Проста перевірка логіки
    test_values = [0.1, 0.5, 0.9]
    for val in test_values:
        state = get_state_by_esi(val)
        print(f"ESI={val} -> {state.name}")
