"""
Veritas Protocol - Core Engine (LAC-7.1/B)
Ref: etrij-2026-0035
Author: Dmytro Kholodniak & Veritas Team
Central engine of the Veritas Protocol.
Orchestrates the Logic Authenticity Check (LAC) and state management.
"""

class VeritasCore:
    """
    Initialize the Veritas Core.
    Args:
        initial_state (str): The starting state of the system (зарезервовано).
    """
    def __init__(self, initial_state="INITIALIZING"):
        self.initial_state = initial_state
        # Початкова репутація ключових вузлів (0.0 to 1.0)
        self.reputation_registry = {
            "Ethical_Council_UA": 0.95,
            "Prosecutor_Council_UA": 0.42,
            "Davos_Global_Rhetoric": 0.38,
            "Dr_Snizhok": 1.0
        }

    def evaluate_integrity(self, text, source):
        """
        Main public method to evaluate data integrity using LAC.
        Args:
            text (str): Текст для аналізу.
            source (str): Джерело/вузол, що перевіряється.
        Returns:
            dict: Results containing integrity score and flags.
        """
        # LAC Algorithm: Logic Authenticity Check
        has_logic_gaps = "тому що" not in text.lower() and "внаслідок" not in text.lower()
        has_semantic_drift = len(set(text.lower().split()) & {"етика", "необхідно", "стандарти"}) > 1
        
        # Розрахунок штрафу (Entropy Penalty)
        penalty = 0.0
        if has_logic_gaps:
            penalty += 0.3
        if has_semantic_drift:
            penalty += 0.2
        
        # Оновлення репутації вузла (Slashing)
        current_rep = self.reputation_registry.get(source, 0.5)
        updated_rep = max(0.0, current_rep - penalty)
        self.reputation_registry[source] = round(updated_rep, 2)
        
        return {
            "node": source,
            "status": "REJECTED" if updated_rep < 0.4 else "STABLE",
            "new_reputation": updated_rep,
            "intervention_required": updated_rep < 0.3
        }

    def get_system_state(self, node_name: str):
        """
        Визначає стан системи на основі репутації вузла.
        Використовує логіку з states.py.
        
        Args:
            node_name (str): Назва вузла з реєстру репутацій.
            
        Returns:
            SystemState: Об'єкт стану системи (LAMINAR_FLOW, SYSTEMIC_FATIGUE, etc.)
        """
        # Імпорт тут, щоб уникнути проблем
        from states import calculate_state_from_reputation
        
        # Отримуємо репутацію вузла (0.5 за замовчуванням, якщо не знайдено)
        reputation = self.reputation_registry.get(node_name, 0.5)
        
        # Визначаємо стан на основі репутації
        return calculate_state_from_reputation(reputation)


# Logic execution for the system
if __name__ == "__main__":
    # Тестуємо основний функціонал
    v = VeritasCore()
    print("=== Тест основного методу evaluate_integrity ===")
    result = v.evaluate_integrity("Призначення Шевчука етично необхідне", "Prosecutor_Council_UA")
    print(f"Результат перевірки: {result}")
    
    print("\n=== Тест нового методу get_system_state ===")
    
    # Перевіряємо стани для різних вузлів
    test_nodes = ["Ethical_Council_UA", "Prosecutor_Council_UA", "Davos_Global_Rhetoric", "Unknown_Node"]
    
    for node in test_nodes:
        state = v.get_system_state(node)
        print(f"Вузол '{node}': репутація = {v.reputation_registry.get(node, 0.5):.2f}, стан системи = {state.name}")
    
    print("\n=== Фінальний реєстр репутацій ===")
    for node, rep in v.reputation_registry.items():
        print(f"{node}: {rep}")
