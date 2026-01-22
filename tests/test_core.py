import unittest
from veritas_core import VeritasCore # Переконайся, що назва файлу збігається

class TestVeritasCore(unittest.TestCase):
    def setUp(self):
        self.core = VeritasCore()

    def test_logic_consistency(self):
        # Тест на логічну стабільність
        sample_text = "The price increased because the demand was high."
        score = self.core.analyze_entropy(sample_text)
        self.assertLess(score, 0.5) # Очікуємо низьку ентропію для логічного тексту

    def test_hype_detection(self):
        # Тест на виявлення хайпу
        hype_text = "Shocking historic unprecedented miracle!"
        score = self.core.analyze_entropy(hype_text)
        self.assertGreater(score, 0.7) # Очікуємо високу ентропію

if __name__ == '__main__':
    unittest.main()
