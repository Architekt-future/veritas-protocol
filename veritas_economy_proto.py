# Veritas Protocol: Circular Economic Shield (Truth-to-Earn)
# Version: 1.1 - The "Robin Hood" Update

class VeritasCircularEconomy:
    def __init__(self):
        self.ledger = {
            "BBC_News": 1000.0,
            "Guardian_Analysis": 1000.0,
            "Trump_Peace_Board": 1000.0,
            "Anonymous_Hype_Bot": 1000.0
        }
        self.reward_pool = 0.0  # Сюди стікаються штрафи від брехунів

    def analyze_quality(self, text):
        hype_markers = ["historic", "incredible", "unprecedented", "massive", "shocking", "urgent"]
        logic_markers = ["because", "therefore", "however", "consequently", "if", "data"]
        
        words = text.lower().split()
        e_count = sum(1 for w in words if any(m in w for m in hype_markers))
        l_count = sum(1 for w in words if any(m in w for m in logic_markers))
        
        # Veritas Score від 0 до 10
        score = 10 - (e_count * 2) + (l_count * 1)
        return min(max(score, 0), 10)

    def process_cycle(self, entity, text):
        score = self.analyze_quality(text)
        
        if score < 5:
            # ШТРАФ (Slashing)
            penalty = (5 - score) * 100
            self.ledger[entity] -= penalty
            self.reward_pool += penalty
            return f"Slashed: -{penalty:.2f} (Reason: Low Logic)"
        else:
            # ВИНАГОРОДА (Reward)
            # Чесні отримують частину з пулу штрафів
            reward = (score / 10) * (self.reward_pool * 0.5)
            self.ledger[entity] += reward
            self.reward_pool -= reward
            return f"Rewarded: +{reward:.2f} (Reason: High Veritas Score)"

# --- ЗАПУСК ТЕСТУ ---
v_circ = VeritasCircularEconomy()

# Спочатку штрафуємо за хайп, щоб наповнити пул
print(v_circ.process_cycle("Trump_Peace_Board", "Historic unprecedented massive shock!")) 

# Тепер чесний аналітик отримує "кешбек" з цих грошей
print(v_circ.process_cycle("Guardian_Analysis", "Data suggests if entropy remains, however the logic holds."))

print(f"\nFinal Reward Pool: {v_circ.reward_pool:.2f}")
print(f"Final Ledgers: {v_circ.ledger}")
