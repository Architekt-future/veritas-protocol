from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import re
import urllib.request
# Імпортуємо нову архітектуру
from veritas_architecture import VeritasArchitecture  # <-- ЗМІНА 1

app = Flask(__name__, static_folder='.')
CORS(app)

# Ініціалізуємо НОВИЙ рушій архітектури
engine = VeritasArchitecture()  # <-- ЗМІНА 2

class SimpleExtractor:
    """Simplified scraper without external dependencies"""
    # [Весь код SimpleExtractor залишається без змін]
    # ...

extractor = SimpleExtractor()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/analyze', methods=['GET', 'POST', 'OPTIONS'])
def analyze():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    if request.method == 'GET':
        # Оновлюємо версію для позначення нової архітектури
        return jsonify({'status': 'online', 'version': '4.0-architectural'}), 200  # <-- ЗМІНА 3

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data'}), 400

        url = data.get('url', '').strip()
        text = data.get('text', '').strip()
        source = data.get('source', 'Ручний ввід')
        title = 'Ручний ввід'

        # 1. Отримуємо текст (з URL або напряму) [Код залишається без змін]
        if url:
            try:
                # ... [код для отримання HTML та витягування тексту залишається без змін]
                # ...
                pass  # Для стислості, реальний код тут
            except Exception as e:
                return jsonify({'error': f'Помилка отримання даних: {str(e)}'}), 500

        if not text or len(text) < 10:
            return jsonify({'error': 'Текст занадто короткий'}), 400

        # 2. ЗАПУСКАЄМО НОВУ АРХІТЕКТУРУ VERITAS
        result = engine.analyze(text)  # <-- Це тепер повертає новий формат

        # 3. АДАПТУЄМО ВІДПОВІДЬ ДЛЯ СУМІСНОСТІ З ФРОНТЕНДОМ
        # Фронтенд очікує певні поля, ми їх зберігаємо
        formatted_result = {
            # Основні поля для фронтенду
            'entropy': result['entropy'],
            'status': result['status'],
            'verdict': result['verdict'],
            'language': result['language'],
            'explanation': result['explanation'],
            
            # Додаємо діагностику в окремий об'єкт
            'diagnostics': result['diagnostics'],
            
            # Метадані
            'source': source,
            'title': title,
            'url': url if url else ''
        }
        
        # Додаємо mode для інформації
        if url:
            formatted_result['mode'] = 'url_scraping'
            formatted_result['extracted_text'] = text[:1500] + '...' if len(text) > 1500 else text
        else:
            formatted_result['mode'] = 'manual'

        return jsonify(formatted_result), 200

    except Exception as e:
        # Додаємо більше інформації для налагодження
        app.logger.error(f"Помилка аналізу: {str(e)}")
        return jsonify({'error': f'Помилка аналізу: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
