# Veritas Protocol: Economic Slashing Prototype (PoL - Proof of Logic)
# Author: Architekt-future & Veritas Core Modules

class VeritasEconomy:
    def __init__(self):
        # Реєстр капіталу істини
        self.ledger = {
            "BBC_News": 1000.0,
            "Trump_Peace_Board": 1000.0,
            "Guardian_Analysis": 1000.0,
            "Anonymous_Hype_Bot": 1000.0
        }

    def analyze_text(self, text):
        # Список слів-маркерів ентропії (хайп, емоції, маніпуляція)
        entropy_markers = ["historic", "incredible", "unprecedented", "massive", "shocking", 
                           "urgent", "secret", "betrayal", "miracle", "chaos", "panic"]
        
        # Список логічних маркерів (структура, причинність)
        logic_markers = ["because", "therefore", "however", "consequently", "if", "thus", "data"]
        
        words = text.lower().split()
        e_count = sum(1 for w in words if any(m in w for m in entropy_markers))
        l_count = sum(1 for w in words if any(m in m for m in logic_markers))
        
        return e_count / len(words) if len(words) > 0 else 0, l_count

    def apply_slashing(self, entity, text):
        entropy_ratio, logic_score = self.analyze_text(text)
        
        # ФОРМУЛА: Штраф за ентропію мінус бонус за логіку
        penalty = (entropy_ratio * 2500) - (logic_score * 30)
        penalty = max(0, penalty)
        
        self.ledger[entity] -= penalty
        return entropy_ratio, logic_score, penalty

# Приклад роботи системи:
if __name__ == "__main__":
    v_econ = VeritasEconomy()
    
    cases = [
        ("Trump_Peace_Board", "Historic and unprecedented secret move for massive peace! Shocking!"),
        ("Guardian_Analysis", "The reform is controversial because it changes the data oversight. However, it is necessary if logic remains."),
    ]
    
    print("--- VERITAS REAL-TIME SLASHING REPORT ---")
    for entity, text in cases:
        e, l, p = v_econ.apply_slashing(entity, text)
        print(f"[{entity}] | Entropy: {e:.2f} | Logic: {l} | SLASHED: -{p:.2f}")
        print(f"New Balance: {v_econ.ledger[entity]:.2f}\n")
