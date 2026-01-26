"""
Veritas Protocol - State Management Module
Визначає стани системи на основі репутації вузлів.
"""

def calculate_state_from_reputation(reputation: float) -> str:
    """
    Визначає стан системи на основі репутації вузла.
    
    Args:
        reputation: float from 0.0 to 1.0
        
    Returns:
        str: System state descriptor
        
    States:
        - STABLE_TRUST (≥0.85): Вузол має високу довіру
        - MONITORED (0.60-0.84): Вузол під спостереженням
        - WARNING (0.40-0.59): Попередження про зниження якості
        - CRITICAL (0.20-0.39): Критичний стан, потрібне втручання
        - QUARANTINE (<0.20): Вузол ізольовано
        
    Example:
        >>> calculate_state_from_reputation(0.95)
        'STABLE_TRUST'
        >>> calculate_state_from_reputation(0.15)
        'QUARANTINE'
    """
    if reputation >= 0.85:
        return "STABLE_TRUST"
    elif reputation >= 0.60:
        return "MONITORED"
    elif reputation >= 0.40:
        return "WARNING"
    elif reputation >= 0.20:
        return "CRITICAL"
    else:
        return "QUARANTINE"


def get_state_description(state: str) -> str:
    """
    Повертає детальний опис стану.
    
    Args:
        state: State name from calculate_state_from_reputation
        
    Returns:
        str: Human-readable description
    """
    descriptions = {
        "STABLE_TRUST": "Вузол демонструє стабільно високу якість логічного сигналу",
        "MONITORED": "Вузол функціонує нормально, але під постійним моніторингом",
        "WARNING": "Виявлено підвищену ентропію. Рекомендована перевірка",
        "CRITICAL": "Критичне зниження якості. Необхідне термінове втручання",
        "QUARANTINE": "Вузол ізольовано через систематичні порушення логічної цілісності"
    }
    return descriptions.get(state, "Unknown state")
def get_action_protocol(reputation: float) -> dict:
    """
    Повертає рекомендовані дії на основі репутації вузла.
    
    Args:
        reputation: float from 0.0 to 1.0
        
    Returns:
        dict: Містить стан, опис та рекомендовані дії
        
    Example:
        >>> get_action_protocol(0.15)
        {
            'state': 'QUARANTINE',
            'description': 'Вузол ізольовано...',
            'actions': ['BLOCK_OUTPUT', 'REQUIRE_MANUAL_REVIEW', 'LOG_INCIDENT']
        }
    """
    state = calculate_state_from_reputation(reputation)
    description = get_state_description(state)
    
    # Визначаємо дії на основі стану
    action_map = {
        "STABLE_TRUST": ["ALLOW_AUTONOMOUS", "PERIODIC_AUDIT"],
        "MONITORED": ["ALLOW_WITH_LOGGING", "INCREASE_SAMPLING"],
        "WARNING": ["REQUIRE_VERIFICATION", "ESCALATE_TO_HUMAN"],
        "CRITICAL": ["RESTRICT_OUTPUT", "MANDATORY_REVIEW"],
        "QUARANTINE": ["BLOCK_OUTPUT", "REQUIRE_MANUAL_REVIEW", "LOG_INCIDENT"]
    }
    
    return {
        "state": state,
        "description": description,
        "actions": action_map.get(state, ["UNKNOWN_STATE"]),
        "reputation": reputation
    }

if __name__ == "__main__":
    # Тестування модуля
    test_reputations = [0.95, 0.75, 0.50, 0.25, 0.10]
    
    print("=== State Mapping Tests ===")
    for rep in test_reputations:
        state = calculate_state_from_reputation(rep)
        desc = get_state_description(state)
        print(f"Reputation: {rep:.2f} → {state}")
        print(f"  Description: {desc}\n")
