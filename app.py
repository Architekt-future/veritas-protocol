from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import re
import urllib.request
from veritas_calibrated_core import VeritasHyperCalibratedCore  # ← змінено ім'я класу!

app = Flask(__name__, static_folder='.')
CORS(app)

# Initialize engine
engine = VeritasHyperCalibratedCore()  # ← створюємо нове ядро


class SimpleExtractor:
    # ... (екстрактор залишається без змін)
    # ...


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
        return jsonify({'status': 'online', 'version': '3.2-hyper'}), 200  # ← версія оновлена

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data'}), 400

        url = data.get('url', '').strip()
        text = data.get('text', '').strip()
        source = data.get('source', 'Ручний ввід')
        title = 'Ручний ввід'

        # 1. Отримуємо текст (з URL або напряму)
        if url:
            try:
                req = urllib.request.Request(
                    url,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (compatible; VeritasBot/1.0)',
                        'Accept': 'text/html,application/xhtml+xml',
                        'Accept-Language': 'uk-UA,uk;q=0.9,en-US;q=0.8'
                    }
                )
                with urllib.request.urlopen(req, timeout=15) as response:
                    html = response.read().decode('utf-8', errors='ignore')
                extraction = extractor.extract_from_url(url, html)
                if not extraction['success']:
                    raise Exception('Extraction failed')
                text = extraction['text']
                title = extraction['title']
                source = extraction['source']
            except Exception as e:
                return jsonify({'error': f'Помилка отримання даних: {str(e)}'}), 500

        if not text or len(text) < 10:
            return jsonify({'error': 'Текст занадто короткий'}), 400

        # 2. ЗАПУСКАЄМО НОВЕ ГІПЕРКАЛІБРОВАНЕ ЯДРО
        result = engine.analyze(text)

        # 3. ДОДАЄМО метадані
        result['source'] = source
        result['title'] = title
        result['url'] = url
        if url:
            result['mode'] = 'url_scraping'
            result['extracted_text'] = text[:1500] + '...' if len(text) > 1500 else text
        else:
            result['mode'] = 'manual'

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': f'Помилка аналізу: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
