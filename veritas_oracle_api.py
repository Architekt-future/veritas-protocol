import requests
import time

class VeritasOracle:
    def __init__(self, api_token):
        # Твій пароль від Hugging Face
        self.api_token = api_token
        # Адреса моделі LaBSE (та сама, що ми тестували в Colab)
        self.api_url = "https://api-inference.huggingface.co/models/sentence-transformers/LaBSE"
        self.headers = {"Authorization": f"Bearer {self.api_token}"}

    def get_semantic_score(self, text):
        """Питає у нейронки: 'Це логічна думка чи набір слів?'"""
        # Еталон логічного змісту
        reference = "Математика, логіка, науковий факт, філософське вчення, об'єктивна істина."
        
        payload = {
            "inputs": {
                "source_sentence": reference,
                "sentences": [text]
            }
        }

        try:
            # Відправляємо запит у хмару
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=5)
            
            # Якщо модель 'спить' (перший запит), вона поверне помилку 'loading'
            if response.status_code == 200:
                return response.json()[0] # Повертає число (схожість)
            else:
                return None # Щось пішло не так (немає інтернету або ліміт)
        except Exception:
            return None
