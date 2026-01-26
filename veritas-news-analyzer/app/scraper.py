"""
Veritas News Analyzer - Web Scraper Module
Витягує текст з новинних URL для аналізу
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsExtractor:
    """Витягує текст з новинних сайтів"""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def extract_from_url(self, url: str) -> Dict[str, str]:
        """
        Витягує текст статті з URL
        
        Args:
            url: URL новинної статті
            
        Returns:
            Dict з title, text, source, url
        """
        try:
            logger.info(f"Extracting content from: {url}")
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Витягуємо заголовок
            title = self._extract_title(soup)
            
            # Витягуємо основний текст
            text = self._extract_text(soup)
            
            # Визначаємо джерело
            source = self._extract_source(url)
            
            return {
                'title': title,
                'text': text,
                'source': source,
                'url': url,
                'success': True
            }
            
        except requests.RequestException as e:
            logger.error(f"Request error: {e}")
            return {
                'error': str(e),
                'url': url,
                'success': False
            }
        except Exception as e:
            logger.error(f"Extraction error: {e}")
            return {
                'error': str(e),
                'url': url,
                'success': False
            }
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Витягує заголовок статті"""
        # Пробуємо різні варіанти
        title_selectors = [
            ('meta', {'property': 'og:title'}),
            ('meta', {'name': 'twitter:title'}),
            ('h1', {}),
            ('title', {})
        ]
        
        for tag, attrs in title_selectors:
            element = soup.find(tag, attrs)
            if element:
                if tag == 'meta':
                    return element.get('content', '').strip()
                else:
                    return element.get_text().strip()
        
        return "Unknown Title"
    
    def _extract_text(self, soup: BeautifulSoup) -> str:
        """Витягує основний текст статті"""
        # Видаляємо непотрібні елементи
        for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'iframe']):
            tag.decompose()
        
        # Пробуємо знайти основний контент
        content_selectors = [
            {'class': ['article-body', 'article-content', 'post-content', 'entry-content']},
            {'id': ['article-body', 'main-content', 'content']},
            {'itemprop': 'articleBody'},
        ]
        
        text = ""
        for selector in content_selectors:
            if 'class' in selector:
                for cls in selector['class']:
                    elements = soup.find_all(class_=cls)
                    if elements:
                        text = ' '.join([e.get_text() for e in elements])
                        break
            elif 'id' in selector:
                for id_val in selector['id']:
                    element = soup.find(id=id_val)
                    if element:
                        text = element.get_text()
                        break
            elif 'itemprop' in selector:
                element = soup.find(attrs={'itemprop': selector['itemprop']})
                if element:
                    text = element.get_text()
            
            if text:
                break
        
        # Якщо нічого не знайдено, беремо всі параграфи
        if not text:
            paragraphs = soup.find_all('p')
            text = ' '.join([p.get_text() for p in paragraphs])
        
        # Очищення тексту
        text = ' '.join(text.split())  # Видаляємо зайві пробіли
        return text
    
    def _extract_source(self, url: str) -> str:
        """Визначає джерело за URL"""
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        # Видаляємо www.
        domain = domain.replace('www.', '')
        return domain


# Тестування
if __name__ == "__main__":
    extractor = NewsExtractor()
    
    # Приклад використання
    test_urls = [
        "https://www.bbc.com/news",
        "https://www.pravda.com.ua/"
    ]
    
    for url in test_urls:
        print(f"\n{'='*60}")
        print(f"Testing: {url}")
        print('='*60)
        
        result = extractor.extract_from_url(url)
        
        if result['success']:
            print(f"Title: {result['title'][:100]}...")
            print(f"Source: {result['source']}")
            print(f"Text length: {len(result['text'])} chars")
            print(f"Preview: {result['text'][:200]}...")
        else:
            print(f"Error: {result['error']}")
