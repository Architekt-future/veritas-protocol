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
        return jsonify({'status': 'online', 'version': '8.0-semantic-void'}), 200

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
        
        total_chaos_index = (
            diag.get('chaos_markers', 0) * 1.0 +  # ЗБІЛЬШЕНО!
            diag.get('semantic_dissonance', 0) * 70 +
            diag.get('semantic_void', 0) * 50 +  # НОВА МЕТРИКА!
            diag.get('pattern_count', 0) * 25 +
            diag.get('historical_revision_markers', 0) * 15 +
            diag.get('alarmism_markers', 0) * 10 +
            diag.get('economic_occult_markers', 0) * 20
        )
        
        impact_score = (
            result['entropy'] * 100 +
            diag.get('semantic_dissonance', 0) * 90 +  # ЗБІЛЬШЕНО!
            diag.get('sanity_penalty', 0) * 80 +
            diag.get('semantic_void', 0) * 70 +  # НОВА МЕТРИКА!
            diag.get('chaos_markers', 0) * 6 +
            diag.get('pattern_count', 0) * 35 +
            diag.get('historical_revision_markers', 0) * 25 +
            diag.get('alarmism_markers', 0) * 20 +
            diag.get('economic_occult_markers', 0) * 30
        )
        
        academic_density = diag.get('academic_markers', 0) / max(1, diag.get('word_count', 1))
        is_academic = diag.get('academic_markers', 0) >= 4 and academic_density > 0.06
        
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
            
            'shannon_entropy': diag.get('shannon_entropy', 0),
            'complexity': diag.get('complexity', 0),
            'total_chaos_index': round(total_chaos_index, 2),
            'sanity_penalty': diag.get('sanity_penalty', 0),
            'semantic_void': diag.get('semantic_void', 0),  # НОВА МЕТРИКА!
            'chaos_markers': diag.get('chaos_markers', 0),
            'semantic_dissonance': diag.get('semantic_dissonance', 0),
            'noise_markers': diag.get('noise_markers', 0),
            'signal_markers': diag.get('signal_markers', 0),
            'academic_markers': diag.get('academic_markers', 0),
            'academic_density': round(academic_density, 3),
            'is_academic_context': is_academic,
            'shout_factor': diag.get('shout_factor', 0),
            'number_density': diag.get('number_density', 0),
            'word_count': diag.get('word_count', 0),
            'char_count': diag.get('char_count', 0),
            'signal_noise_ratio': round(diag.get('noise_markers', 0) / max(1, diag.get('signal_markers', 1)), 3),
            'pattern_count': diag.get('pattern_count', 0),
            'historical_revision_markers': diag.get('historical_revision_markers', 0),
            'alarmism_markers': diag.get('alarmism_markers', 0),
            'economic_occult_markers': diag.get('economic_occult_markers', 0)
        }
        
        emotional_pressure = (
            diag.get('chaos_markers', 0) > 5 or 
            diag.get('pattern_count', 0) > 0 or
            diag.get('alarmism_markers', 0) > 1 or
            result['status'] == 'CRITICAL'
        )
        
        disorientation_risk = (
            diag.get('semantic_dissonance', 0) > 0.4 or
            diag.get('semantic_void', 0) > 0.3 or
            diag.get('chaos_markers', 0) > 8 or
            diag.get('historical_revision_markers', 0) > 0
        )
        
        response['emotional_pressure'] = emotional_pressure
        response['disorientation_risk'] = disorientation_risk
        response['emotional_analysis'] = generate_emotional_analysis(result, diag)
        
        if url and len(text_to_analyze) > 0:
            response['extracted_text'] = text_to_analyze[:1000] + ('...' if len(text_to_analyze) > 1000 else '')
            response['extracted_text_length'] = len(text_to_analyze)
            response['show_extracted_text'] = True
        
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': f'Внутрішня помилка: {str(e)}'}), 500

def generate_emotional_analysis(result, diag):
    if result['status'] == 'CRITICAL':
        if 'НІГІЛІЗМ' in result['verdict']:
            return "НАУКОВИЙ НІГІЛІЗМ: підрив довіри до науки через абсурдне застосування термінів"
        elif 'МАНІПУЛЯЦІЯ' in result['verdict']:
            return "ДЗЕРКАЛЬНА МАНІПУЛЯЦІЯ: звинувачення інших у власних методах"
        elif 'ОКУЛЬТИЗМ' in result['verdict']:
            return "КОРПОРАТИВНИЙ ОКУЛЬТИЗМ: токсичне поєднання бізнесу та езотерики"
        elif 'ПУСТОТА' in result['verdict']:
            return "СЕМАНТИЧНА ПУСТОТА: текст приховує відсутність змісту за гуманітарною термінологією"
        elif 'РЕВІЗІОНІЗМ' in result['verdict']:
            return "ІСТОРИЧНИЙ РЕВІЗІОНІЗМ: створення альтернативної реальности з анахронічними елементами"
        elif 'АЛАРМІЗМ' in result['verdict']:
            return "ПРОРОЧИЙ АЛАРМІЗМ: використання апокаліптичних метафор для створення прихованої тривоги"
        elif 'НЕКРОМАНТІЯ' in result['verdict']:
            return "ЕКОНОМІЧНА НЕКРОМАНТІЯ: абсурдне поєднання фінансів з езотерикою"
        else:
            return "КРИТИЧНИЙ СЕМАНТИЧНИЙ ХАОС: текст створює когнітивне навантаження"
    
    elif diag.get('semantic_void', 0) > 0.3:
        return "СЕМАНТИЧНА ПУСТОТА: високий рівень абстракції при відсутності конкретного змісту"
    
    elif diag.get('semantic_dissonance', 0) > 0.3:
        return "СЕМАНТИЧНА НЕСТАБІЛЬНІСТЬ: несумісні концепції можуть викликати дезорієнтацію"
    
    else:
        return "МІНІМАЛЬНИЙ ЕМОЦІЙНИЙ ВПЛИВ: текст не містить явних маніпулятивних технік"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
