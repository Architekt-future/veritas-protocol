"""
Veritas Protocol - Core Engine
Базовий movement engine для standalone використання
"""

from typing import Dict, Set


class VeritasEngine:
    """
    Базовий Veritas engine для обчислення ентропії
    Використовується як fallback якщо translator недоступний
    """
    
    def __init__(self):
        self.noise_markers = {
            "етично", "необхідно", "важливо", "неприпустимо", "історично",
            "ethically", "necessarily", "important", "unacceptable", "historically"
        }
        
        self.signal_markers = {
            "якщо", "тоді", "тому", "внаслідок", "дорівнює", "факт",
            "if", "then", "therefore", "consequently", "equals", "fact"
        }
        
        self.chaos_markers = {
            "рептилоїди", "lizard", "magic", "таємний", "змова", "плоска",
            "conspiracy", "secret", "freemasons"
        }
    
    def calculate_entropy(self, text: str) -> float:
        """
        Базовий розрахунок ентропії
        
        Args:
            text: Текст для аналізу
            
        Returns:
            float: Індекс ентропії (0.0-1.0)
        """
        words = text.lower().replace(",", "").replace(".", "").split()
        if not words:
            return 1.0
        
        # Перевірка на хаос
        if any(w in self.chaos_markers for w in words):
            return 0.99
        
        # Підрахунок
        noise_count = sum(1 for w in words if w in self.noise_markers)
        signal_count = sum(1 for w in words if w in self.signal_markers)
        
        laminar_index = (signal_count + 1) / (noise_count + signal_count + 1)
        return round(1.0 - laminar_index, 3)


# Експорт для backward compatibility
__all__ = ['VeritasEngine']
