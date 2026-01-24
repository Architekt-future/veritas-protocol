from enum import Enum

class SystemState(Enum):
    """
    Визначає фазові стани системи Veritas.
    Кожен стан відповідає рівню ентропії та репутації вузла.
    """
    LAMINAR_FLOW = (0.8, 1.0, "Потік чистий. Логіка домінує. Втручання не потрібне.")
    STABLE = (0.6, 0.79, "Система стабільна. Є незначний шум, але сигнал чіткий.")
    SYSTEMIC_FATIGUE = (0.4, 0.59, "Системна втома. Висока ентропія. Потрібна верифікація.")
    ENTROPIC_DECAY = (0.2, 0.39, "Ентропійний розпад. Критичний рівень маніпуляцій. Slashing увімкнено.")
    COLLAPSE = (0.0, 0.19, "Колапс. Вузол захоплений вурдалаками. Повна ізоляція.")

    def __init__(self, min_rep, max_rep, description):
        self.min_rep = min_rep
        self.max_rep = max_rep
        self.description = description

def calculate_state_from_reputation(reputation: float) -> SystemState:
    """
    Мапує числове значення репутації на конкретний стан системи.
    """
    for state in SystemState:
        if state.min_rep <= reputation <= state.max_rep:
            return state
    return SystemState.COLLAPSE

def get_action_protocol(state: SystemState):
    """
    Повертає необхідну дію для поточного стану.
    Економічний аспект: на рівні DECAY та COLLAPSE система автоматично 
    блокує транзакції або інформаційні потоки.
    """
    protocols = {
        SystemState.LAMINAR_FLOW: "PASS: Пріоритетне проходження сигналу.",
        SystemState.STABLE: "MONITOR: Стандартний нагляд.",
        SystemState.SYSTEMIC_FATIGUE: "WARN: Посилена перевірка джерел.",
        SystemState.ENTROPIC_DECAY: "INTERDICT: Тимчасове блокування вузла.",
        SystemState.COLLAPSE: "TERMINATE: Повне видалення з репутаційного реєстру."
    }
    return protocols.get(state, "UNKNOWN: Manual check required.")
