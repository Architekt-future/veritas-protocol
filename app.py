import os
import urllib.request
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
# Імпортуємо тільки те, що точно є в ядрі
from veritas_calibrated_core import VeritasCalibratedCore

app = Flask(__name__, static_folder='.')
CORS(app)

engine = VeritasCalibratedCore()
# Залишаємо extractor як None, якщо він не імпортувався
extractor = None

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
            return jsonify({'error': 'No JSON data received'}), 400

        url = data.get('url', '').strip()
        # Спробуємо взяти текст з усіх можливих ключів, які міг надіслати фронтенд
        input_text = data.get('text') or data.get('textContent') or ""
        input_text = str(input_text).strip()
        
        text_to_analyze = ""
        mode = ""

        if url:
            mode = 'url_scraping'
            # ... твій код скрапінгу ...
            # ПРИПУСТИМО, скрапер поки що не чіпаємо, перевіримо ТЕКСТ
            text_to_analyze = "ЗАГЛУШКА: СКРАПІНГ У РОБОТІ" 
        else:
            mode = 'text_input'
            text_to_analyze = input_text

        # ОСЬ ТУТ МОМЕНТ ІСТИНИ:
        if not text_to_analyze:
            return jsonify({
                'error': 'Бекенд отримав пустий текст!',
                'received_keys': list(data.keys()),
                'data_preview': str(data)[:100]
            }), 400

        # ВІДПРАВЛЯЄМО В ЯДРО
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
