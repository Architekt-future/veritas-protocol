"""
Veritas Protocol - Flask Backend for Render
Main application file
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import re
import urllib.request
from veritas_calibrated_core import VeritasCalibratedCore

app = Flask(__name__, static_folder='.')
CORS(app)

# Initialize engine
engine = VeritasCalibratedCore()


class SimpleExtractor:
    """Simplified scraper without external dependencies"""
    
    def extract_from_url(self, url: str, html: str) -> dict:
        """Extract text from HTML"""
        try:
            cleaned = self._clean_html(html)
            title = self._extract_title(html)
            text = self._extract_paragraphs(cleaned)
            source = self._extract_domain(url)
            
            return {
                'success': True,
                'title': title,
                'text': text,
                'source': source,
                'url': url
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'url': url
            }
    
    def _clean_html(self, html: str) -> str:
        """Remove scripts, styles, nav, etc."""
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<nav[^>]*>.*?</nav>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<header[^>]*>.*?</header>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<footer[^>]*>.*?</footer>', '', html, flags=re.DOTALL | re.IGNORECASE)
        return html
    
    def _extract_title(self, html: str) -> str:
        """Extract page title"""
        match = re.search(r'<meta[^>]*property="og:title"[^>]*content="([^"]+)"', html, re.IGNORECASE)
        if match:
            return match.group(1)
        match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return "Unknown Title"
    
    def _extract_paragraphs(self, html: str) -> str:
        """Extract text from <p> tags"""
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, flags=re.DOTALL | re.IGNORECASE)
        
        if not paragraphs:
            body_match = re.search(r'<body[^>]*>(.*?)</body>', html, flags=re.DOTALL | re.IGNORECASE)
            if body_match:
                text = body_match.group(1)
                text = re.sub(r'<[^>]+>', ' ', text)
                return self._clean_text(text)
        
        text = ' '.join(paragraphs)
        text = re.sub(r'<[^>]+>', ' ', text)
        return self._clean_text(text)
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text"""
        text = re.sub(r'&[a-zA-Z]+;', ' ', text)
        text = re.sub(r'&#\d+;', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        match = re.search(r'https?://(?:www\.)?([^/]+)', url)
        if match:
            return match.group(1)
        return "unknown"


extractor = SimpleExtractor()


@app.route('/')
def index():
    """Serve index.html"""
    return send_from_directory('.', 'index.html')


@app.route('/api/analyze', methods=['GET', 'POST', 'OPTIONS'])
def analyze():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    if request.method == 'GET':
        return jsonify({'status': 'online', 'version': '3.1-calibrated'}), 200
    
    try:
        data = request.get_json()
        if not data: return jsonify({'error': 'No data'}), 400
        
        url = data.get('url', '').strip()
        text = data.get('text', '').strip()
        source = data.get('source', 'Manual Input')
        
        # 1. Отримуємо текст (з URL або напряму)
        if url:
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    html = response.read().decode('utf-8', errors='ignore')
                extraction = extractor.extract_from_url(url, html)
                if not extraction['success']: raise Exception('Extraction failed')
                text = extraction['text']
                title = extraction['title']
                source = extraction['source']
            except Exception as e:
                return jsonify({'error': f'Scraping failed: {str(e)}'}), 500
        
        if not text or len(text) < 10:
            return jsonify({'error': 'Text too short'}), 400

        # 2. ЗАПУСКАЄМО ЯДРО
        result = engine.analyze(text)
        
        # 3. КАЛІБРУВАННЯ ТА ВЕРДИКТ (Наша нова логіка)
        # Дістаємо показники
        entropy = result.get('shannon_entropy', 0)
        chaos = result.get('chaos_markers', 0)
                
        # Визначаємо вердикт та клас (danger/warning/success)
        if entropy > 0.58 or chaos > 15:
            result['status_class'] = 'danger'
            result['verdict'] = 'КРИТИЧНИЙ РІВЕНЬ ХАОСУ'
            result['explanation'] = 'Виявлено ознаки інтенсивного маніпулятивного впливу. Текст має аномально високу ентропію.'
        elif entropy > 0.45 or chaos > 8:
            result['status_class'] = 'warning'
            result['verdict'] = 'ПІДОЗРІЛИЙ СИГНАЛ'
            result['explanation'] = 'Текст містить специфічні маркери емоційної дестабілізації. Можлива маніпуляція.'
        else:
            result['status_class'] = 'success'
            result['verdict'] = 'СТАБІЛЬНИЙ ЛОГІЧНИЙ СИГНАЛ'
            result['explanation'] = 'Структура тексту в межах норми. Аномалій не виявлено.'
        # --- КІНЕЦЬ БЛОКУ КАЛІБРУВАННЯ ---

            result['source'] = source
            result['title'] = title
            result['url'] = url
            result['mode'] = 'url_scraping'
            result['extracted_text'] = text[:1500] + '...' if len(text) > 1500 else text

        except Exception as e:
            return jsonify({'error': f'Scraping failed: {str(e)}'}), 500
