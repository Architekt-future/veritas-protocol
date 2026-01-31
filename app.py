from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import re
import urllib.request
from veritas_calibrated_core import VeritasCalibratedCore

app = Flask(__name__, static_folder='.')
CORS(app)

engine = VeritasCalibratedCore()

class SimpleExtractor:
    def extract_from_url(self, url: str, html: str) -> dict:
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
            return {'success': False, 'error': str(e), 'url': url}
    
    def _clean_html(self, html: str) -> str:
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
        return html
    
    def _extract_title(self, html: str) -> str:
        match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
        return match.group(1).strip() if match else "Unknown Title"
    
    def _extract_paragraphs(self, html: str) -> str:
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, flags=re.DOTALL | re.IGNORECASE)
        text = ' '.join(paragraphs) if paragraphs else re.sub(r'<[^>]+>', ' ', html)
        return self._clean_text(text)
    
    def _clean_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _extract_domain(self, url: str) -> str:
        match = re.search(r'https?://(?:www\.)?([^/]+)', url)
        return match.group(1) if match else "unknown"

extractor = SimpleExtractor()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/analyze', methods=['GET', 'POST', 'OPTIONS'])
def analyze():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    if request.method == 'GET':
        return jsonify({'status': 'online', 'version': '3.1-calibrated'}), 200
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data'}), 400
        
        url = data.get('url', '').strip()
        raw_text = data.get('text', '').strip()
        source = 'Manual Input'
        title = 'Manual Input'
        text_to_analyze = ""

        if url:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8', errors='ignore')
            ext = extractor.extract_from_url(url, html)
            if not ext['success']: raise Exception(ext['error'])
            text_to_analyze = ext['text']
            source = ext['source']
            title = ext['title']
        else:
            text_to_analyze = raw_text

        if not text_to_analyze or len(text_to_analyze) < 10:
            return jsonify({'error': 'Content too short'}), 400

       # 1. Запуск аналізу ядра
        result = engine.analyze(text_to_analyze)
        
        # 2. Витягуємо всі показники (використовуємо твої назви з ядра)
        # Якщо в ядрі вони під іншими іменами, .get() підстрахує
        entropy = result.get('shannon') or result.get('shannon_entropy', 0)
        complexity = result.get('complexity', 0)
        markers = result.get('markers', 0) or result.get('chaos_markers', 0)
        sanity = result.get('sanity_penalty', 0)
        density = result.get('number_density', 0)
        shout = result.get('shout_factor', 0)
        lang = result.get('language', 'uk')

        # 3. Розрахунок підсумкового Хаосу (з урахуванням усіх факторів)
        # Ентропія 0.33 + високий Shout Factor = вже підозріло
        total_chaos = markers + (sanity * 5) + (shout * 2)

        # 4. Формуємо розширений словник для фронтенду
        # Додаємо ВСІ поля, які ти хочеш бачити
        result.update({
            'shannon_entropy': entropy,
            'complexity': complexity,
            'chaos_markers': total_chaos,
            'sanity_penalty': sanity,
            'number_density': density,
            'shout_factor': shout,
            'language': lang,
            'source': source,
            'title': title,
            'mode': 'url' if url else 'text'
        })

        # 5. Калібрування вердикту (тепер на основі комплексу факторів)
        if entropy > 0.60 or total_chaos > 20:
            result['status_class'] = 'danger'
            result['verdict'] = 'КРИТИЧНИЙ РІВЕНЬ ВПЛИВУ'
        elif entropy > 0.45 or total_chaos > 10 or shout > 0.5:
            result['status_class'] = 'warning'
            result['verdict'] = 'ПІДОЗРІЛА СТРУКТУРА'
        else:
            result['status_class'] = 'success'
            result['verdict'] = 'СТАБІЛЬНИЙ ЛОГІЧНИЙ СИГНАЛ'

        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
