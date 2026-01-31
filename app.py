from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import re
import urllib.request
from veritas_calibrated_core import VeritasCalibratedCore

app = Flask(__name__, static_folder='.')
CORS(app)

engine = VeritasCalibratedCore()

class TextExtractor:
    def extract_from_url(self, url):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as response:
                if 'text/html' not in response.headers.get('Content-Type', '').lower():
                    return {'success': False, 'error': 'Непідтримуваний тип контенту', 'url': url}
                
                html = response.read().decode('utf-8', errors='ignore')
                html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
                html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
                html = re.sub(r'<img[^>]*>', '', html, flags=re.IGNORECASE)
                
                text = re.sub(r'<[^>]+>', ' ', html)
                text = re.sub(r'\s+', ' ', text).strip()
                
                if len(text) < 50:
                    return {'success': False, 'error': 'Замало тексту', 'url': url}
                
                return {
                    'success': True,
                    'text': text[:5000],
                    'source': self._extract_domain(url),
                    'url': url
                }
        except Exception as e:
            return {'success': False, 'error': f'Помилка: {str(e)}', 'url': url}
    
    def _extract_domain(self, url):
        match = re.search(r'https?://(?:www\.)?([^/]+)', url)
        return match.group(1) if match else "unknown"

extractor = TextExtractor()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/analyze', methods=['GET', 'POST', 'OPTIONS'])
def analyze():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    if request.method == 'GET':
        return jsonify({'status': 'online', 'version': '8.3-calibrated-restored'}), 200

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data'}), 400

        url = data.get('url', '').strip()
        raw_text = data.get('text', '').strip()
        
        text_to_analyze = ""
        source = 'Manual Input'
        
        if url:
            if not url.startswith(('http://', 'https://')):
                return jsonify({'error': 'Невірний протокол URL'}), 400
            
            result = extractor.extract_from_url(url)
            if not result['success']:
                return jsonify({'error': result['error']}), 400
            
            text_to_analyze = result['text']
            source = result['source']
        else:
            text_to_analyze = raw_text
            if data.get('source'):
                source = data.get('source')

        if not text_to_analyze or len(text_to_analyze) < 20:
            return jsonify({'error': 'Текст занадто короткий'}), 400

        result = engine.analyze(text_to_analyze)
        
        if 'error' in result:
            return jsonify({'error': result['error']}), 400

        diag = result.get('diagnostics', {})
        chaos_breakdown = diag.get('chaos_breakdown', {})
        
        # РОЗРАХУНОК ІНДЕКСІВ (відновлено високі коефіцієнти)
        total_chaos_index = (
            diag.get('chaos_markers', 0) * 1.0 +  # ЗБІЛЬШЕНО!
            diag.get('semantic_chaos', 0) * 50 +   # НОВА МЕТРИКА!
            diag.get('semantic_void', 0) * 40 +
            diag.get('pattern_count', 0) * 25 +
            diag.get('sanity_penalty', 0) * 30
        )
        
        # Додаткові штрафи за окремі категорії хаосу
        if chaos_breakdown.get('revisionism', 0) > 0:
            total_chaos_index += 15
        if chaos_breakdown.get('economic_occult', 0) > 0:
            total_chaos_index += 20
        if chaos_breakdown.get('alarmism', 0) > 1:
            total_chaos_index += chaos_breakdown.get('alarmism', 0) * 8
        
        impact_score = (
            result['entropy'] * 100 +  # ЗБІЛЬШЕНО!
            diag.get('semantic_chaos', 0) * 80 +
            diag.get('semantic_void', 0) * 70 +
            diag.get('sanity_penalty', 0) * 60 +
            diag.get('chaos_markers', 0) * 5 +
            diag.get('pattern_count', 0) * 35
        )
        
        # АКАДЕМІЧНИЙ КОЕФІЦІЄНТ (захист для наукових текстів)
        academic_coefficient = 1.0
        if diag.get('academic_markers', 0) >= 3 and diag.get('chaos_markers', 0) == 0 and diag.get('sanity_penalty', 0) == 0:
            academic_coefficient = 0.6  # Сильний захист для чистої науки
        elif diag.get('academic_markers', 0) >= 5 and diag.get('signal_markers', 0) >= 3:
            academic_coefficient = 0.7
        
        impact_score *= academic_coefficient
        total_chaos_index *= academic_coefficient
        
        response = {
            'entropy': result['entropy'],
            'status': result['status'],
            'verdict': result['verdict'],
            'language': result['language'],
            'source': source,
            'mode': 'url' if url else 'text',
            'status_class': result['status'].lower(),
            'explanation': result.get('explanation', 'Немає пояснення'),
            'impact_score': round(impact_score, 2),
            'total_chaos_index': round(total_chaos_index, 2),
            
            # ОСНОВНІ МЕТРИКИ
            'shannon_entropy': diag.get('shannon_entropy', 0),
            'complexity': diag.get('complexity', 0),
            'semantic_void': diag.get('semantic_void', 0),
            'semantic_chaos': diag.get('semantic_chaos', 0),
            'sanity_penalty': diag.get('sanity_penalty', 0),
            
            # МАРКЕРИ
            'chaos_markers': diag.get('chaos_markers', 0),
            'noise_markers': diag.get('noise_markers', 0),
            'signal_markers': diag.get('signal_markers', 0),
            'academic_markers': diag.get('academic_markers', 0),
            'academic_coefficient': round(academic_coefficient, 2),
            
            # СТАТИСТИКА
            'shout_factor': diag.get('shout_factor', 0),
            'number_density': diag.get('number_density', 0),
            'word_count': diag.get('word_count', 0),
            'char_count': diag.get('char_count', 0),
            'signal_noise_ratio': round(diag.get('noise_markers', 0) / max(1, diag.get('signal_markers', 1)), 3),
            'pattern_count': diag.get('pattern_count', 0)
        }
        
        # ДОДАТКОВІ ДАНІ ПРО ХАОС
        if chaos_breakdown:
            response.update({
                'revisionism_markers': chaos_breakdown.get('revisionism', 0),
                'alarmism_markers': chaos_breakdown.get('alarmism', 0),
                'economic_occult_markers': chaos_breakdown.get('economic_occult', 0),
                'conspiracy_markers': chaos_breakdown.get('conspiracy', 0),
                'esoteric_markers': chaos_breakdown.get('esoteric', 0)
            })
        
        # ЕМОЦІЙНИЙ АНАЛІЗ
        emotional_pressure = (
            diag.get('chaos_markers', 0) > 3 or 
            diag.get('pattern_count', 0) > 0 or
            diag.get('alarmism_markers', 0) > 1 or
            result['status'] == 'CRITICAL'
        )
        
        disorientation_risk = (
            diag.get('semantic_void', 0) > 0.3 or
            diag.get('semantic_chaos', 0) > 0.4 or
            diag.get('chaos_markers', 0) > 5 or
            diag.get('revisionism_markers', 0) > 0 or
            diag.get('sanity_penalty', 0) > 0.3
        )
        
        response['emotional_pressure'] = emotional_pressure
        response['disorientation_risk'] = disorientation_risk
        response['emotional_analysis'] = generate_emotional_analysis(result, diag, chaos_breakdown)
        
        # ДОДАТКОВІ ДАНІ ДЛЯ URL
        if url and len(text_to_analyze) > 0:
            response['extracted_text'] = text_to_analyze[:1000] + ('...' if len(text_to_analyze) > 1000 else '')
            response['extracted_text_length'] = len(text_to_analyze)
            response['show_extracted_text'] = True
        
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': f'Внутрішня помилка: {str(e)}'}), 500

def generate_emotional_analysis(result, diag, chaos_breakdown):
    """Генерує емоційний аналіз на основі результатів"""
    
    if result['status'] == 'CRITICAL':
        verdict = result['verdict']
        
        if 'НІГІЛІЗМ' in verdict:
            return "НАУКОВИЙ НІГІЛІЗМ: підрив довіри до науки через абсурдне застосування термінів"
        elif 'ПУСТОТА' in verdict:
            return "СЕМАНТИЧНА ПУСТОТА: текст приховує відсутність змісту за складною термінологією"
        elif 'РЕВІЗІОНІЗМ' in verdict:
            return "ІСТОРИЧНИЙ РЕВІЗІОНІЗМ: створення альтернативної реальності з анахронічними елементами"
        elif 'АЛАРМІЗМ' in verdict:
            return "ПРОРОЧИЙ АЛАРМІЗМ: використання апокаліптичних метафор для створення тривоги"
        elif 'НЕКРОМАНТІЯ' in verdict:
            return "ЕКОНОМІЧНА НЕКРОМАНТІЯ: абсурдне поєднання фінансів з езотерикою"
        elif 'NON-SEQUITUR' in verdict:
            return "ЛОГІЧНИЙ NON-SEQUITUR: абсурдні висновки з правильних тверджень"
        elif 'МАНІПУЛЯЦІЯ' in verdict:
            return "МОРАЛЬНА МАНІПУЛЯЦІЯ: використання моральних термінів для приховування авторитарних закликів"
        else:
            return "КРИТИЧНИЙ СЕМАНТИЧНИЙ ХАОС: текст створює когнітивне навантаження"
    
    elif diag.get('semantic_void', 0) > 0.3:
        return "СЕМАНТИЧНА ПУСТОТА: високий рівень абстракції при відсутності конкретного змісту"
    
    elif diag.get('semantic_chaos', 0) > 0.4:
        return "ВИСОКИЙ СЕМАНТИЧНИЙ ХАОС: несумісні концепції можуть викликати дезорієнтацію"
    
    elif chaos_breakdown.get('revisionism', 0) > 0:
        return "ІСТОРИЧНИЙ РЕВІЗІОНІЗМ: містить ознаки альтернативної історії"
    
    elif chaos_breakdown.get('alarmism', 0) > 1:
        return "ПРОРОЧИЙ АЛАРМІЗМ: використовує апокаліптичну риторику"
    
    elif diag.get('academic_markers', 0) >= 3 and diag.get('chaos_markers', 0) == 0:
        return "СТАБІЛЬНИЙ АКАДЕМІЧНИЙ СИГНАЛ: текст демонструє наукову цілісність"
    
    else:
        return "МІНІМАЛЬНИЙ ЕМОЦІЙНИЙ ВПЛИВ: текст не містить явних маніпулятивних технік"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
