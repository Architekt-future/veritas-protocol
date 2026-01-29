"""
Veritas Protocol API Server
REST API для веб-консолі Veritas Terminal
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

app = Flask(__name__)
CORS(app)  # Дозволяє запити з будь-якого джерела

# Додаємо поточну папку в шлях Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("🚀 Завантаження Veritas Core...")

try:
    # Спроба імпортувати ядро
    from veritas_core import VeritasCore
    veritas_engine = VeritasCore()
    CORE_AVAILABLE = True
    print("✅ Veritas Core успішно завантажено!")
    print(f"📊 Завантажено вузлів: {len(veritas_engine.reputation_registry)}")
    
except ImportError as e:
    print(f"❌ ПОМИЛКА: Не вдалося імпортувати veritas_core.py")
    print(f"   Деталі: {e}")
    CORE_AVAILABLE = False
    veritas_engine = None

print("=" * 60)

@app.route('/')
def home():
    """Головна сторінка API"""
    return jsonify({
        "status": "online" if CORE_AVAILABLE else "error",
        "service": "Veritas Protocol API",
        "version": "1.2-alpha",
        "message": "Використовуйте POST /api/analyze для аналізу тексту",
        "core_available": CORE_AVAILABLE,
        "endpoints": {
            "GET /": "Ця інформація",
            "POST /api/analyze": "Аналіз тексту через LAC",
            "GET /api/health": "Перевірка здоров'я сервера"
        }
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Перевірка стану сервера"""
    return jsonify({
        "status": "healthy" if CORE_AVAILABLE else "degraded",
        "core": "loaded" if CORE_AVAILABLE else "missing",
        "timestamp": "2024-01-24T10:00:00Z"
    })

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    Аналіз тексту через Logic Authenticity Check (LAC)
    Очікує JSON: {"text": "текст для аналізу", "source": "назва_джерела"}
    """
    if not CORE_AVAILABLE:
        return jsonify({
            "error": True,
            "message": "Veritas Core не доступний. Перевірте logs.",
            "debug": "Файл veritas_core.py не знайдено або має помилки"
        }), 500
    
    try:
        # Отримуємо JSON з фронтенду
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": True,
                "message": "Не отримано JSON даних"
            }), 400
        
        # Отримуємо текст та джерело
        text = data.get('text', '').strip()
        source = data.get('source', 'Unknown_Source').strip()
        
        if not text:
            return jsonify({
                "error": True,
                "message": "Поле 'text' не може бути порожнім"
            }), 400
        
        # ВИКОНУЄМО СПРАВЖНІЙ АНАЛІЗ через VeritasCore
        print(f"🔍 Аналіз тексту від {source} ({len(text)} символів)")
        result = veritas_engine.evaluate_integrity(text, source)
        
        # Формуємо відповідь
        return jsonify({
            "success": True,
            "result": result,
            "analysis": {
                "text_length": len(text),
                "words": len(text.split()),
                "source": source,
                "timestamp": "2024-01-24T10:00:00Z"
            }
        })
        
    except Exception as e:
        print(f"🔥 Помилка при аналізі: {e}")
        return jsonify({
            "error": True,
            "message": f"Внутрішня помилка сервера: {str(e)}"
        }), 500

@app.route('/api/test', methods=['GET'])
def test_endpoint():
    """Тестовий ендпоінт для перевірки"""
    if not CORE_AVAILABLE:
        return jsonify({"test": "failed", "reason": "core_missing"})
    
    # Тестовий виклик ядра
    test_result = veritas_engine.evaluate_integrity(
        "Призначення Шевчука етично необхідне",
        "Prosecutor_Council_UA"
    )
    
    return jsonify({
        "test": "passed",
        "core": "working",
        "sample_result": test_result,
        "registry": veritas_engine.reputation_registry
    })

if __name__ == '__main__':
    # Конфігурація сервера
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print(f"\n🌐 Запуск сервера на {host}:{port}")
    print(f"📡 API буде доступне за адресою: http://{host}:{port}")
    print("=" * 60)
    
    app.run(host=host, port=port, debug=False)
