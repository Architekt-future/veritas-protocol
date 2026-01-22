# Veritas Protocol: Secure Circular Economy
# Version: 1.2 - Anti-Sybil & Identity Protection

class VeritasSecureEconomy:
    def __init__(self):
        # ledger тепер зберігає не тільки баланс, а й "Рівень Довіри" (Trust Level)
        self.registry = {
            "BBC_News": {"balance": 1000.0, "trust": 1.0, "is_bot": False},
            "Guardian_Analysis": {"balance": 1000.0, "trust": 0.9, "is_bot": False},
            "Trump_Peace_Board": {"balance": 1000.0, "trust": 0.3, "is_bot": False},
            "Bot_Net_001": {"balance": 100.0, "trust": 0.1, "is_bot": True}
        }
        self.reward_pool = 0.0

    def verify_identity(self, entity):
        # Якщо рівень довіри менше 0.2 - доступ до винагород заблоковано
        if self.registry[entity]["trust"] < 0.2:
            return False
        return True

    def update_trust(self, entity, score):
        # Рівень довіри зростає від хороших постів і падає від поганих
        if score > 7:
            self.registry[entity]["trust"] = min(1.0, self.registry[entity]["trust"] + 0.05)
        elif score < 4:
            self.registry[entity]["trust"] = max(0.0, self.registry[entity]["trust"] - 0.2)

    def process_cycle(self, entity, text):
        # 1. Рахуємо якість тексту
        hype_markers = ["historic", "incredible", "massive"]
        words = text.lower().split()
        e_count = sum(1 for w in words if any(m in w for m in hype_markers))
        score = 10 - (e_count * 3)
        
        # 2. Оновлюємо репутацію
        self.update_trust(entity, score)
        
        # 3. Перевіряємо, чи має право на гроші
        if not self.verify_identity(entity):
            penalty = 50.0 # Штраф за спробу бот-активності
            self.registry[entity]["balance"] -= penalty
            self.reward_pool += penalty
            return f"ACCESS DENIED: Entity {entity} flagged as LOW TRUST. Penalty applied."

        # 4. Економіка (Slashing/Reward)
        if score < 5:
            penalty = 150.0
            self.registry[entity]["balance"] -= penalty
            self.reward_pool += penalty
            return f"Slashed {entity}: -150 (Reason: Low Logic Score)"
        else:
            reward = (score / 10) * (self.reward_pool * 0.3)
            self.registry[entity]["balance"] += reward
            self.reward_pool -= reward
            return f"Rewarded {entity}: +{reward:.2f} (Trust Level: {self.registry[entity]['trust']:.2f})"

# --- ТЕСТ АНТИ-БОТА ---
v_sys = VeritasSecureEconomy()

# Бот намагається вкинути хайп
print(v_sys.process_cycle("Bot_Net_001", "Incredible massive news!")) 
# Бот знову намагається - і його банять!
print(v_sys.process_cycle("Bot_Net_001", "Shocking historic move!"))

# Чесний аналітик отримує капітал бота
print(v_sys.process_cycle("BBC_News", "The data shows consistent growth in the sector."))
