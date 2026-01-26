import math

class VeritasCore:
    """
    Veritas Protocol - Core Engine (LAC-7.2/Final)
    Центральний механізм Logic Authenticity Check (LAC) та управління станами.
    Ref: etrij-2026-0035
    """
    def __init__(self, initial_state="INITIALIZING"):
        self.initial_state = initial_state
        # Початкова репутація ключових вузлів (0.0 to 1.0)
        self.reputation_registry = {
            "Ethical_Council_UA": 0.95,
            "Prosecutor_Council_UA": 0.42,
            "Davos_Global_Rhetoric": 0.38,
            "Dr_Snizhok": 1.0,
            "NBC_News_Greenland": 0.50,
            "Taiwan_Semi_Official": 0.85
        }

    def _calculate_entropy_coefficient(self, text):
        """
        Внутрішній метод для розрахунку індексу ентропії.
        Вимірює співвідношення демагогічного шуму до логічного сигналу.
        """
        words = text.lower().replace(",", "").replace(".", "").split()
        if not words:
            return 1.0
            
        # Абсолютні маркери хаосу (Елементи ентропії IV рівня)
        chaos_markers = {"рептилоїди", "lizard", "magic", "таємний", "змова", "плоска"}
        if any(w in chaos_markers for w in words):
            return 0.99  # Максимальна ентропія (хаос)

        # Маркери 'шуму' (ентропія)
        noise_markers = {
            "етично", "необхідно", "важливо", "неприпустимо", "історично", 
            "фундаментально", "занепокоєння", "перемога", "збитки", "довіра"
        }
        # Маркери 'сигналу' (ламінарність)
        signal_markers = {
            "якщо", "тоді", "тому", "внаслідок", "дорівнює", "факт", 
            "ресурс", "чип", "наказ", "координати", "результат"
        }
        
        noise_count = sum(1 for w in words if w in noise_markers)
        signal_count = sum(1 for w in words if w in signal_markers)
        
        # Формула ламінарності: чим більше сигналу, тим вищий індекс
        laminar_index = (signal_count + 1) / (noise_count + signal_count + 1)
        return round(1.0 - laminar_index, 3)

    def evaluate_integrity(self, text, source):
        """
        Головний метод оцінки цілісності даних.
        Використовує динамічний Slashing на основі ентропії.
        """
        # 1. Розрахунок ентропії тексту
        entropy_score = self._calculate_entropy_coefficient(text)
        
        # 2. Розрахунок штрафу/бонусу (Dynamic Slashing)
        penalty = 0.0
        if entropy_score > 0.4:
            # Чим вища ентропія, тим болючіший штраф
            penalty = round(entropy_score * 0.4, 2)
        elif entropy_score < 0.2:
            # Нагорода за надвисоку чіткість сигналу
            penalty = -0.05
            
        # 3. Оновлення репутації вузла в реєстрі
        current_rep = self.reputation_registry.get(source, 0.5)
        updated_rep = max(0.0, min(1.0, current_rep - penalty))
        self.reputation_registry[source] = round(updated_rep, 2)
        
        # 4. Формування результату
        return {
            "node": source,
            "entropy_index": entropy_score,
            "new_reputation": updated_rep,
            "status": "REJECTED" if updated_rep < 0.4 else "STABLE",
            "intervention_required": updated_rep < 0.3
        }

    def get_system_state(self, node_name: str):
        """
        Визначає стан системи на основі репутації вузла.
        Зв'язок з модулем states.py.
        """
        try:
            from states import calculate_state_from_reputation
        except ImportError:
            return "Error: states.py not found"
            
        reputation = self.reputation_registry.get(node_name, 0.5)
        return calculate_state_from_reputation(reputation)


# Тестування системи
if __name__ == "__main__":
    v = VeritasCore()
    
    # Приклад 1: Типова заява вурдалаків
    vurdalak_text = "Історично необхідно етично занепокоїтися через втрату довіри."
    res1 = v.evaluate_integrity(vurdalak_text, "Davos_Global_Rhetoric")
    print(f"Аналіз демагогії: {res1}")
    
    # Приклад 2: Чіткий технологічний сигнал
    tech_text = "Якщо чипи заблоковано, тоді результат ескалації дорівнює нулю."
    res2 = v.evaluate_integrity(tech_text, "Taiwan_Semi_Official")
    print(f"Аналіз сигналу: {res2}")
    
    # Приклад 3: Тест маркерів хаосу
    chaos_text = "Рептилоїди таємно керують magic світом через змову."
    res3 = v.evaluate_integrity(chaos_text, "Conspiracy_Node")
    print(f"Аналіз хаосу: {res3}")
    
    # Стан системи для Тайваню
    state = v.get_system_state("Taiwan_Semi_Official")
    print(f"Поточний стан вузла Тайвань: {state}")
