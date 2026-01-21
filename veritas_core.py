class VeritasLAC:
    def __init__(self):
        self.entropy_threshold = 0.7
        # База репутації (початковий стан)
        self.registry = {
            "EthicalCouncil_UA": 1.0,
            "ProsecutorCouncil_UA": 0.5, # Знижено через останні події
            "Davos_Rhetoric": 0.4
        }

    def calculate_slashing(self, source, logic_score):
        """Вираховує штраф для репутації вузла"""
        current_rep = self.registry.get(source, 0.5)
        # Якщо логіка нижча за 0.5, репутація падає експоненціально
        penalty = (0.5 - logic_score) * 2 if logic_score < 0.5 else 0
        new_rep = max(0, current_rep - penalty)
        return round(new_rep, 2)

    def analyze_statement(self, text, source="Unknown"):
        # ... (попередня логіка аналізу) ...
        # Припустимо, ми отримали integrity_score = 0.2 (дуже низький)
        integrity_score = 0.2 
        new_reputation = self.calculate_slashing(source, integrity_score)
        
        return {
            "source": source,
            "integrity_score": integrity_score,
            "new_reputation_level": new_reputation,
            "status": "INTERDICTED" if new_reputation < 0.3 else "MONITORED"
        }
