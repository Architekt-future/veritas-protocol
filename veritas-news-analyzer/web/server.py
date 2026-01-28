import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# Додаємо шлях до папки app, щоб сервер бачив наші модулі
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.scraper import NewsScraper
from app.analyzer import VeritasAnalyzer
from app.core import VeritasEngine

app = Flask(__name__)
CORS(app)  # Дозволяємо React-інтерфейсу звертатися до сервера

# Ініціалізація компонентів
scraper = NewsScraper()
analyzer = VeritasAnalyzer(config={})
engine = VeritasEngine()

@app.route('/analyze-url', methods=['POST'])
def analyze_url():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "URL не надано"}), 400

    # 1. Скрапінг (Витягуємо текст)
    text = scraper.fetch_content(url)
    if text.startswith("Помилка"):
        return jsonify({"error": text}), 500

    # 2. Аналіз метрик
    metrics = analyzer.analyze(text)
    
    # 3. Розрахунок фінального Veritas Score
    score = engine.calculate_veritas_score(metrics)
    status = engine.get_status(score)

    return jsonify({
        "source": url,
        "text_preview": text[:500] + "...",
        "metrics": metrics,
        "veritas_score": score,
        "status": status
    })

@app.route('/analyze-text', methods=['POST'])
def analyze_text():
    data = request.json
    text = data.get('text')
    
    if not text:
        return jsonify({"error": "Текст не надано"}), 400

    metrics = analyzer.analyze(text)
    score = engine.calculate_veritas_score(metrics)
    status = engine.get_status(score)

    return jsonify({
        "metrics": metrics,
        "veritas_score": score,
        "status": status
    })

if __name__ == '__main__':
    # Запускаємо сервер
    app.run(host='0.0.0.0', port=5000, debug=True)
