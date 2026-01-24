import math

class VeritasCore:
    """
    Veritas Protocol - Core Engine (LAC-7.2/Final)
    Система автоматичної верифікації логіки та управління репутацією вузлів.
    """
    def __init__(self, initial_state="STABLE"):
        self.system_status = initial_state
        # Реєстр репутацій (Ground Truth Nodes)
        self.reputation_registry = {
            "Ethical_Council_UA": 0.95,
            "Prosecutor_Council_UA": 0.42,
            "Davos_Global_Rhetoric": 0.38,
            "Dr_Snizhok": 1.0,
            "NBC_News_Greenland": 0.50, # Початкова точка для медіа
            "Taiwan_Semi_Official": 0.85
        }

    def _calculate_entropy_coefficient(self, text):
        """
        Математичний розрахунок рівня 'бруду' (ентропії) у тексті.
        L = (Signal + 1) / (Noise + Signal + 1)
        """
        words = text.lower().replace(",", "").replace(".", "").split()
        if not words:
            return 1.0
            
        # Маркери 'шуму' - демагогія, прикметники, маніпуляції
        noise_markers = {
            "етично", "необхідно", "важливо", "неприпустимо", "історично", 
            "фундаментально", "занепокоєння", "перемога", "збитки", "довіра"
        }
        # Маркери 'сигналу' - логіка, причинність, факти
        signal_markers = {
            "якщо", "тоді", "тому", "внаслідок", "дорівнює", "факт", 
            "ресурс", "чип", "наказ", "координати", "результат"
        }
        
        noise_count = sum(1 for w in words if w in noise_markers)
        signal_count = sum(1 for w in words if w in signal_markers)
        
        # Розрахунок ламінарності (чистоти потоку)
        laminar_index = (signal_count + 1) / (noise_count + signal_count + 1)
        # Ентропія = зворотне значення ламінарності
        return round(1.0 - laminar_index, 3)

    def _get_state_name(self, reputation):
        """Логіка визначення стану системи (States.py)"""
        if reputation >= 0.8: return "LAMINAR_FLOW (Істина)"
        if reputation >= 0.6: return "STABLE (Норма)"
        if reputation >= 0.4: return "SYSTEMIC_FATIGUE (Втома)"
        if reputation >= 0.2: return "ENTROPIC_DECAY (Розпад)"
        return "COLLAPSE (Вурдалаки перемогли)"

    def evaluate_integrity(self, text, source):
        """Головний метод аналізу"""
        entropy_score = self._calculate_entropy_coefficient(text)
        
        # Динамічний штраф (Slashing)
        # Якщо ентропія висока (більше 0.4), репутація вузла падає
        penalty = 0.0
        if entropy_score > 0.4:
            penalty = round(entropy_score * 0.4, 2)
        
        # Бонус за чистий сигнал
        if entropy_score < 0.2:
            penalty = -0.05 # Репутація трохи зростає
            
        current_rep = self.reputation_registry.get(source, 0.5)
        updated_rep = max(0.0, min(1.0, current_rep - penalty))
        self.reputation_registry[source] = round(updated_rep, 2)
        
        state = self._get_state_name(updated_rep)
        
        return {
            "Джерело": source,
            "Індекс ентропії (Бруд)": entropy_score,
            "Нова репутація": updated_rep,
            "Стан системи": state,
            "Рішення": "ACCEPT" if entropy_score < 0.4 else "REJECT/CHECK"
        }

# --- ТЕСТОВИЙ ЗАПУСК ---
if __name__ == "__main__":
    v = VeritasCore()
    
    # 1. Тестуємо "Бруд" (Новина NBC про Гренландію)
    news_text = "Історично важливо, що довіра Європи втрачена, це неприпустимо і завдає великих збитків."
    print("\n--- Аналіз новин (NBC Style) ---")
    print(v.evaluate_integrity(news_text, "NBC_News_Greenland"))

    # 2. Тестуємо "Сигнал" (Тайвань про чипи)
    taiwan_text = "Ми перекриємо канали тому що факт постачання чипів дорівнює ескалації. Результат гарантовано."
    print("\n--- Аналіз сигналу (Taiwan Style) ---")
    print(v.evaluate_integrity(taiwan_text, "Taiwan_Semi_Official"))

    # 3. Тестуємо "Вурдалаків" (Давос/Риторика)
    davos_text = "Необхідно етично дотримуватися стандартів важливості фундаментальних цінностей."
    print("\n--- Аналіз демагогії (Davos Style) ---")
    print(v.evaluate_integrity(davos_text, "Davos_Global_Rhetoric"))
