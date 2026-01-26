"""
Veritas News Analyzer - Flask Web Interface
Веб-інтерфейс для аналізу новин
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
from pathlib import Path

# Додаємо app в path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.analyzer import NewsAnalyzer
from app.database import VeritasDatabase

app = Flask(__name__)
CORS(app)

# Глобальні об'єкти
analyzer = NewsAnalyzer()
db = VeritasDatabase()


@app.route('/')
def index():
    """Головна сторінка"""
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    API endpoint для аналізу
    
    Приймає JSON:
    {
        "url": "https://...",  // опціонально
        "text": "...",         // опціонально
        "source": "..."        // опціонально
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    url = data.get('url')
    text = data.get('text')
    source = data.get('source', 'Web Input')
    
    try:
        if url:
            # Аналіз URL
            result = analyzer.analyze_url(url, save_history=False)
        elif text:
            # Аналіз тексту
            result = analyzer.analyze_text(text, source)
        else:
            return jsonify({'error': 'Either url or text must be provided'}), 400
        
        # Зберігаємо в базу
        if result.get('success'):
            db.save_analysis(result)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500


@app.route('/api/history', methods=['GET'])
def get_history():
    """Отримати історію аналізів"""
    limit = request.args.get('limit', 10, type=int)
    history = db.get_recent_analyses(limit)
    return jsonify(history)


@app.route('/api/sources', methods=['GET'])
def get_sources():
    """Отримати список джерел з репутацією"""
    sources = db.get_all_sources()
    return jsonify(sources)


@app.route('/api/source/<source_name>', methods=['GET'])
def get_source_info(source_name):
    """Отримати інформацію про конкретне джерело"""
    reputation = db.get_source_reputation(source_name)
    analyses = db.get_analyses_by_source(source_name, limit=5)
    
    return jsonify({
        'reputation': reputation,
        'recent_analyses': analyses
    })


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Отримати статистику"""
    stats = db.get_statistics()
    return jsonify(stats)


@app.route('/api/export', methods=['GET'])
def export_data():
    """Експортувати дані в JSON"""
    limit = request.args.get('limit', type=int)
    filename = 'veritas_export.json'
    
    db.export_to_json(filename, limit)
    
    return jsonify({
        'success': True,
        'filename': filename
    })


if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║        Veritas News Analyzer - Web Interface             ║
    ╚═══════════════════════════════════════════════════════════╝
    
    🌐 Server starting at: http://localhost:5000
    📊 API Documentation:
       POST /api/analyze      - Analyze news
       GET  /api/history      - Get analysis history
       GET  /api/sources      - Get all sources
       GET  /api/source/<name> - Get source info
       GET  /api/statistics   - Get statistics
       GET  /api/export       - Export data
    """)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
