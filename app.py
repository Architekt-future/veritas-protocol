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
        if 'error' in result:
            return jsonify({'error': result['error']}), 400

        # 2. Коректне отримання всіх показників з diagnostics
        diag = result.get('diagnostics', {})
        entropy = diag.get('shannon_entropy', 0)
        complexity = diag.get('complexity', 0)
        chaos_markers = diag.get('chaos_markers', 0)
        sanity_penalty = diag.get('sanity_penalty', 0)
        number_density = diag.get('number_density', 0)
        shout_factor = diag.get('shout_factor', 0)
        noise_markers = diag.get('noise_markers', 0)
        signal_markers = diag.get('signal_markers', 0)
        lang = result.get('language', 'UK')

        # 3. Розрахунок інтегрального індексу хаосу (ваговий)
        # chaos_markers важать більше, ніж shout_factor та noise
        total_chaos = (chaos_markers * 3) + (shout_factor * 50) + (noise_markers * 0.5)

        # 4. Аналіз емоційного впливу та дезорієнтації
        emotional_pressure = False
        disorientation_risk = False
        emotional_comment = ""

        # Критерії емоційного тиску
        if shout_factor > 0.3 or noise_markers > signal_markers * 2:
            emotional_pressure = True
        # Критерії дезорієнтації
        if entropy > 0.5 and complexity > 0.7:
            disorientation_risk = True

        # Формування висновку щодо впливу
        if emotional_pressure and disorientation_risk:
            emotional_comment = "ВИСОКИЙ РІВЕНЬ ЕМОЦІЙНОГО ВПЛИВУ ТА ДЕЗОРІЄНТАЦІЇ. Текст використовує капслок, перебільшення та має високу ентропію, що може спантеличувати читача та впливати на його думку."
        elif emotional_pressure:
            emotional_comment = "ПОМІТНИЙ ЕМОЦІЙНИЙ ТИСК. Текст містить елементи, що прагнуть викликати сильну емоційну реакцію (капслок, перебільшення, маркери шуму)."
        elif disorientation_risk:
            emotional_comment = "РИЗИК ДЕЗОРІЄНТАЦІЇ. Висока ентропія та складність структури можуть утруднити розуміння та сприйняття основної думки."
        else:
            emotional_comment = "ЕМОЦІЙНИЙ ВПЛИВ МІНІМАЛЬНИЙ. Текст зосереджений на фактах та логіці."

        # 5. Формуємо повний словник для фронтенду
        final_result = {
            'entropy': result.get('entropy', 0),
            'status': result.get('status', 'UNKNOWN'),
            'verdict': result.get('verdict', 'NO VERDICT'),
            'language': lang,
            'source': source,
            'title': title,
            'mode': 'url' if url else 'text',
            'status_class': result.get('status', '').lower(),
            # Всі метрики для діагностики
            'shannon_entropy': entropy,
            'complexity': complexity,
            'chaos_markers': chaos_markers,
            'total_chaos_index': round(total_chaos, 2),
            'sanity_penalty': sanity_penalty,
            'number_density': number_density,
            'shout_factor': shout_factor,
            'noise_markers': noise_markers,
            'signal_markers': signal_markers,
            # Результати аналізу впливу
            'emotional_pressure': emotional_pressure,
            'disorientation_risk': disorientation_risk,
            'emotional_analysis': emotional_comment,
            # Додаткові дані
            'word_count': diag.get('word_count', 0),
            'char_count': diag.get('char_count', 0)
        }

        return jsonify(final_result), 200

    except urllib.error.URLError as e:
        return jsonify({'error': f'URL error: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Internal error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
