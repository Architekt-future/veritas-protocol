import os
import urllib.request
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from veritas_calibrated_core import VeritasCalibratedCore, VeritasExtractor

app = Flask(__name__, static_folder='.')
CORS(app)

# Ініціалізація компонентів
engine = VeritasCalibratedCore()
extractor = VeritasExtractor()

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
            'service': 'Veritas Protocol Analysis API',
            'version': '4.0-calibrated'
        }), 200

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        url = data.get('url', '').strip()
        input_text = data.get('text', '').strip()
        source = data.get('source', 'Manual Input')
        
        text_to_analyze = ""
        mode = ""
        title = "Manual Input"

        # 1. Визначаємо джерело тексту
        if url:
            mode = 'url_scraping'
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8', errors='ignore')
            
            extraction = extractor.extract_from_url(url, html)
            if not extraction.get('success'):
                return jsonify({'error': f"Scraping failed: {extraction.get('error')}"}), 500
            
            text_to_analyze = extraction.get('text', '')
            source = extraction.get('source', 'Web Source')
            title = extraction.get('title', 'Extracted Article')
        else:
            mode = 'text_input'
            text_to_analyze = input_text

        # 2. Перевірка на пустий текст
        if not text_to_analyze or len(text_to_analyze) < 5:
            return jsonify({'error': 'No content to analyze (text too short)'}), 400

        # 3. Аналіз ядром
        result = engine.analyze(text_to_analyze)
        
        # 4. Калібрування вердикту
        entropy = result.get('shannon_entropy', 0) or result.get('entropy_score', 0)
        chaos = result.get('chaos_markers', 0)
        
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

        # 5. Додаємо метадані для фронтенду
        result['mode'] = mode
        result['source'] = source
        result['title'] = title
        result['extracted_text'] = text_to_analyze[:1500] + "..." if len(text_to_analyze) > 1500 else text_to_analyze
        
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': f"Backend error: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
