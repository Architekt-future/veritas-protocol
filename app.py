from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import re
import urllib.request
from veritas_architecture import VeritasArchitecture  # Імпортуємо нову архітектуру

app = Flask(__name__, static_folder='.')
CORS(app)

# Ініціалізуємо новий архітектурний рушій
engine = VeritasArchitecture()

class AdvancedExtractor:
    """Покращений скрапер з кращим фільтруванням контенту"""
    
    def extract_from_url(self, url: str, html: str) -> dict:
        """Основний метод витягування тексту"""
        try:
            # Крок 1: Попереднє очищення
            cleaned = self._deep_clean_html(html)
            
            # Крок 2: Виділення основного контенту
            main_content = self._extract_main_content(cleaned)
            
            # Крок 3: Фінальна очистка
            final_text = self._clean_extracted_text(main_content)
            
            # Метадані
            title = self._extract_title(html)
            source = self._extract_domain(url)
            
            return {
                'success': True,
                'title': title,
                'text': final_text,
                'source': source,
                'url': url,
                'char_count': len(final_text),
                'word_count': len(final_text.split())
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'url': url
            }
    
    def _deep_clean_html(self, html: str) -> str:
        """Глибоке очищення HTML від непотрібних елементів"""
        
        # Список елементів для видалення (в порядку важливості)
        patterns_to_remove = [
            (r'<script[^>]*>.*?</script>', ''),  # Скрипти
            (r'<style[^>]*>.*?</style>', ''),    # Стилі
            (r'<!--.*?-->', ''),                 # Коментарі
            (r'<nav[^>]*>.*?</nav>', ''),        # Навігація
            (r'<header[^>]*>.*?</header>', ''),  # Хедер
            (r'<footer[^>]*>.*?</footer>', ''),  # Футер
            (r'<aside[^>]*>.*?</aside>', ''),    # Сайдбар
            (r'<form[^>]*>.*?</form>', ''),      # Форми
            (r'<button[^>]*>.*?</button>', ''),  # Кнопки
            (r'<iframe[^>]*>.*?</iframe>', ''),  # Фрейми
            (r'<svg[^>]*>.*?</svg>', ''),        # SVG
            (r'<select[^>]*>.*?</select>', ''),  # Селекти
            (r'<meta[^>]*>', ''),               # Мета-теги
            (r'<link[^>]*>', ''),               # Лінки
            (r'<noscript[^>]*>.*?</noscript>', ''), # NoScript
        ]
        
        cleaned = html
        for pattern, replacement in patterns_to_remove:
            cleaned = re.sub(pattern, replacement, cleaned, flags=re.DOTALL | re.IGNORECASE)
        
        return cleaned
    
    def _extract_main_content(self, html: str) -> str:
        """Виділення основного текстового контенту"""
        
        # Спроба 1: Знайти основну контентну область
        content_patterns = [
            r'<main[^>]*>(.*?)</main>',
            r'<article[^>]*>(.*?)</article>',
            r'<div[^>]*class="[^"]*content[^"]*"[^>]*>(.*?)</div>',
            r'<div[^>]*class="[^"]*post[^"]*"[^>]*>(.*?)</div>',
            r'<div[^>]*class="[^"]*article[^"]*"[^>]*>(.*?)</div>',
            r'<div[^>]*id="content"[^>]*>(.*?)</div>',
            r'<div[^>]*id="main"[^>]*>(.*?)</div>',
        ]
        
        for pattern in content_patterns:
            match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
            if match:
                content = match.group(1)
                # Видаляємо вкладені теги, залишаємо текст
                content = re.sub(r'<[^>]+>', ' ', content)
                return content
        
        # Спроба 2: Якщо не знайшли структурований контент, беремо body
        body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL | re.IGNORECASE)
        if body_match:
            body_content = body_match.group(1)
            
            # Видаляємо всі теги крім p, h1-h6, li (основний текст)
            body_content = re.sub(r'<(?!p|h[1-6]|li|/p|/h[1-6]|/li)[^>]+>', ' ', body_content)
            
            # Вибираємо лише абзаци, заголовки, списки
            text_blocks = re.findall(r'<(?:p|h[1-6]|li)[^>]*>(.*?)</(?:p|h[1-6]|li)>', 
                                    body_content, re.DOTALL | re.IGNORECASE)
            
            if text_blocks:
                return ' '.join(text_blocks)
        
        # Спроба 3: Останній варіант - просто текст з body
        if body_match:
            body_text = body_match.group(1)
            body_text = re.sub(r'<[^>]+>', ' ', body_text)
            return body_text
        
        return ""
    
    def _clean_extracted_text(self, text: str) -> str:
        """Фінальна очистка витягнутого тексту"""
        
        # Видалення спецсимволів та зайвих пробілів
        text = re.sub(r'&[a-zA-Z]+;', ' ', text)  # HTML entities
        text = re.sub(r'&#\d+;', ' ', text)       # Numeric entities
        text = re.sub(r'\s+', ' ', text)          # Множинні пробіли
        
        # Видалення шумових фраз (реклама, кнопки тощо)
        noise_patterns = [
            r'скачати.*?безкоштовно',
            r'підписатися.*?канал',
            r'реклама.*?партнер',
            r'click here.*?',
            r'download now.*?',
            r'поділитися.*?соцмережа',
            r'читайте також.*?',
            r'рекомендуємо.*?',
            r'попередній.*?наступний',
            r'\.{3,}',  # Крапки
            r'\*{3,}',  # Зірочки
        ]
        
        for pattern in noise_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        # Обмеження довжини (якщо текст дуже довгий)
        if len(text) > 10000:
            # Знаходимо найкращий місце для обрізки (крапка після середини)
            mid_point = len(text) // 2
            cut_point = text.find('.', mid_point)
            if cut_point != -1:
                text = text[:cut_point + 1]
        
        return text.strip()
    
    def _extract_title(self, html: str) -> str:
        """Витягнення заголовка сторінки"""
        # Спочатку Open Graph title
        match = re.search(r'<meta[^>]*property="og:title"[^>]*content="([^"]+)"', 
                         html, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        
        # Потім звичайний title
        match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
        if match:
            title = match.group(1).strip()
            # Чистимо title від зайвого
            title = re.sub(r'^[^|]*\|', '', title)  # Видаляємо все до "|"
            title = re.sub(r' - .*$', '', title)    # Видаляємо все після " - "
            return title
        
        # H1 як запасний варіант
        match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL | re.IGNORECASE)
        if match:
            h1_text = re.sub(r'<[^>]+>', '', match.group(1))
            return h1_text.strip()[:100]
        
        return "Без назви"
    
    def _extract_domain(self, url: str) -> str:
        """Витягнення домену з URL"""
        match = re.search(r'https?://(?:www\.)?([^/]+)', url)
        if match:
            domain = match.group(1)
            # Прибираємо www.
            domain = re.sub(r'^www\.', '', domain)
            return domain
        return "unknown"

extractor = AdvancedExtractor()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/analyze', methods=['GET', 'POST', 'OPTIONS'])
def analyze():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    if request.method == 'GET':
        return jsonify({
            'status': 'online', 
            'version': '4.0-architectural',
            'engine': 'VeritasArchitecture'
        }), 200

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data'}), 400

        url = data.get('url', '').strip()
        text = data.get('text', '').strip()
        source = data.get('source', 'Ручний ввід')
        title = 'Ручний ввід'

        # Отримання тексту з URL або використання прямого вводу
        if url:
            try:
                req = urllib.request.Request(
                    url,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (compatible; VeritasBot/1.0; +https://github.com/Architekt-future/veritas-protocol)',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7',
                        'Accept-Encoding': 'gzip, deflate',
                        'DNT': '1',
                        'Connection': 'keep-alive',
                        'Upgrade-Insecure-Requests': '1',
                        'Cache-Control': 'max-age=0'
                    }
                )
                
                with urllib.request.urlopen(req, timeout=20) as response:
                    # Перевіряємо content-type
                    content_type = response.headers.get('Content-Type', '')
                    if not ('text/html' in content_type or 'application/xhtml+xml' in content_type):
                        return jsonify({'error': 'URL не є HTML сторінкою'}), 400
                    
                    html = response.read().decode('utf-8', errors='ignore')
                
                extraction = extractor.extract_from_url(url, html)
                
                if not extraction['success']:
                    error_msg = extraction.get('error', 'Невідома помилка')
                    return jsonify({'error': f'Помилка витягування тексту: {error_msg}'}), 500
                
                text = extraction['text']
                title = extraction['title']
                source = extraction['source']
                
                # Логування для налагодження
                app.logger.info(f"Успішно витягнуто текст з {url}: {extraction['char_count']} символів")
                
            except urllib.error.HTTPError as e:
                return jsonify({'error': f'HTTP помилка {e.code}: {e.reason}'}), 500
            except urllib.error.URLError as e:
                return jsonify({'error': f'Помилка URL: {str(e)}'}), 500
            except Exception as e:
                app.logger.error(f"Помилка отримання даних: {str(e)}")
                return jsonify({'error': f'Помилка отримання даних: {str(e)}'}), 500

        if not text or len(text) < 20:
            return jsonify({'error': 'Текст занадто короткий (мінімум 20 символів)'}), 400

        # Аналіз тексту новим рушієм
        result = engine.analyze(text)

        # Форматування результату для сумісності з фронтендом
        formatted_result = {
            # Основні поля для фронтенду
            'entropy': result['entropy'],
            'status': result['status'],
            'verdict': result['verdict'],
            'language': result['language'],
            'explanation': result['explanation'],
            
            # Діагностика
            'diagnostics': result['diagnostics'],
            
            # Метадані
            'source': source,
            'title': title,
            'url': url if url else '',
            
            # Статистика тексту
            'text_stats': {
                'char_count': len(text),
                'word_count': len(text.split()),
                'sentence_count': len(re.split(r'[.!?]+', text))
            }
        }
        
        # Додаткові поля для режиму
        if url:
            formatted_result['mode'] = 'url_scraping'
            # Зберігаємо прев'ю тексту для перевірки
            preview_length = min(800, len(text))
            formatted_result['extracted_preview'] = text[:preview_length] + ('...' if len(text) > preview_length else '')
        else:
            formatted_result['mode'] = 'manual'
        
        app.logger.info(f"Аналіз завершено: {result['status']}, ентропія: {result['entropy']:.3f}")
        
        return jsonify(formatted_result), 200

    except Exception as e:
        app.logger.error(f"Критична помилка аналізу: {str(e)}")
        return jsonify({'error': f'Помилка аналізу: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Ендпоінт для перевірки стану API"""
    return jsonify({
        'status': 'healthy',
        'engine': 'VeritasArchitecture',
        'version': '4.0',
        'timestamp': '...'  # Додайте імпорт datetime якщо потрібно
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
