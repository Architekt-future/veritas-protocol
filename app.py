"""
Veritas Protocol - Flask Backend for Render
Main application file - v13.3 with force reload
"""

import sys

# ============================================================
# FORCE RELOAD - CRITICAL FOR v13.3 DEPLOYMENT
# Видаляє всі Veritas модулі з кешу Python
# ============================================================
print("🔄 Veritas v13.3 - Clearing module cache...")
for module_name in list(sys.modules.keys()):
    if 'veritas' in module_name.lower():
        print(f"   ✗ Removing cached: {module_name}")
        del sys.modules[module_name]

# Вимикаємо створення .pyc файлів
sys.dont_write_bytecode = True
print("✅ Cache cleared. Loading fresh Veritas v13.3 modules...")
# ============================================================

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import re
import urllib.request
from veritas_calibrated_core import VeritasCalibratedCore

app = Flask(__name__, static_folder='.')
CORS(app)

# Initialize engine
engine = VeritasCalibratedCore()

print(f"✅ Veritas engine initialized")
print(f"   Pattern boost: {engine.pattern_boost_engine is not None}")
print(f"   Void detector: {engine.void_detector is not None}")
print(f"   Absurdity detector: {engine.absurdity_detector is not None}")
print(f"   Insight detector: {hasattr(engine, 'insight_detector') and engine.insight_detector is not None}")


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
        return jsonify({
            'status': 'online', 
            'version': '13.3',
            'modules': {
                'pattern_boost': engine.pattern_boost_engine is not None,
                'void_detector': engine.void_detector is not None,
                'absurdity_detector': engine.absurdity_detector is not None,
                'insight_detector': hasattr(engine, 'insight_detector') and engine.insight_detector is not None,
            }
        }), 200
    
    try:
        data = request.get_json()
        if not data: 
            return jsonify({'error': 'No data'}), 400
        
        url = data.get('url', '').strip()
        text = data.get('text', '').strip()
        source = data.get('source', 'Manual Input')
        title = data.get('title', 'Untitled')
        
        # 1. Отримуємо текст (з URL або напряму)
        if url:
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    html = response.read().decode('utf-8', errors='ignore')
                extraction = extractor.extract_from_url(url, html)
                if not extraction['success']: 
                    raise Exception('Extraction failed')
                text = extraction['text']
                title = extraction['title']
                source = extraction['source']
            except Exception as e:
                return jsonify({'error': f'Scraping failed: {str(e)}'}), 500
        
        if not text or len(text) < 10:
            return jsonify({'error': 'Text too short'}), 400

        # 2. ЗАПУСКАЄМО ЯДРО v13.3
        result = engine.analyze(text)
        
        # 3. ВИКОРИСТОВУЄМО НОВУ ЛОГІКУ (з entropy від движка)
        # Старий код використовував shannon_entropy напряму
        # Новий код використовує result['entropy'] який вже включає всі boosts
        entropy = result.get('entropy', 0)  # ЦЕ КЛЮЧОВА ЗМІНА!
        chaos = result.get('diagnostics', {}).get('chaos_markers', 0)
        status = result.get('status', 'UNKNOWN')
                
        # Визначаємо вердикт та клас на основі НОВОГО status
        if status == 'CRITICAL':
            result['status_class'] = 'danger'
            result['verdict'] = 'КРИТИЧНИЙ РІВЕНЬ ХАОСУ'
            result['explanation'] = 'Виявлено ознаки інтенсивного маніпулятивного впливу або логічного колапсу.'
        elif status == 'WARNING':
            result['status_class'] = 'warning'
            result['verdict'] = 'ПІДОЗРІЛИЙ ДИСКУРС'
            result['explanation'] = 'Текст містить специфічні маркери емоційної дестабілізації або семантичної порожнечі.'
        elif status == 'ACCEPTABLE':
            result['status_class'] = 'info'
            result['verdict'] = 'ПРИЙНЯТНА ІНФОРМАЦІЯ'
            result['explanation'] = 'Текст має деякі ознаки складності, але в межах норми.'
        else:  # VERIFIED
            result['status_class'] = 'success'
            result['verdict'] = 'ВЕРИФІКОВАНИЙ КОНТЕНТ'
            result['explanation'] = 'Структура тексту відповідає науковим стандартам. Аномалій не виявлено.'
        
        # Додаємо метадані
        result['source'] = source
        result['title'] = title
        result['url'] = url if url else None
        result['mode'] = 'url_scraping' if url else 'manual_input'
        result['extracted_text'] = text[:1500] + '...' if len(text) > 1500 else text
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"❌ Error in analyze: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=False)
