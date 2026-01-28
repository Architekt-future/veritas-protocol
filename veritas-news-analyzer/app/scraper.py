import trafilatura
import requests

class NewsScraper:
    def __init__(self, config=None):
        self.config = config or {}
        self.headers = {
            'User-Agent': 'VeritasProtocol/3.5 (Educational OSINT Project)'
        }

    def fetch_content(self, url: str) -> str:
        """
        Визначає тип посилання і витягує текст.
        Підтримує звичайні сайти та Raw посилання GitHub.
        """
        try:
            # 1. Спеціальна обробка для GitHub Raw
            if "raw.githubusercontent.com" in url:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                return response.text

            # 2. Обробка звичайних новинних сайтів
            downloaded = trafilatura.fetch_url(url)
            if not downloaded:
                # Спроба через requests, якщо trafilatura заблокована
                response = requests.get(url, headers=self.headers, timeout=10)
                downloaded = response.text
            
            # Витягуємо основний текст статті
            content = trafilatura.extract(downloaded, include_comments=False)
            
            if not content:
                return "Помилка: Не вдалося витягти корисний текст із цієї сторінки."
                
            return content

        except Exception as e:
            return f"Помилка скрапінгу: {str(e)}"

    def clean_text(self, text: str) -> str:
        """Додаткова чистка тексту від зайвих пробілів"""
        if not text:
            return ""
        # Видаляємо порожні рядки та зайві пробіли
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return "\n".join(lines)
