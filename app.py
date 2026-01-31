from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import re
import urllib.request
from veritas_calibrated_core import VeritasCalibratedCore

app = Flask(__name__, static_folder='.')
CORS(app)

engine = VeritasCalibratedCore()

class TextExtractor:
    """Екстрактор тільки тексту"""
    
    def extract_from_url(self, url: str) -> dict:
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0'
            })
            
            with urllib.request.urlopen(req, timeout=15) as response:
                content_type = response.headers.get('Content-Type', '')
                
                if 'text/html' not in content_type.lower():
                    return {
                        'success': False,
                        'error': f'Непідтримуваний тип контенту: {content_type}',
                        'url': url
                    }
                
                html = response.read().decode('utf-8', errors='ignore')
            
            html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
            html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
            html = re.sub(r'<img[^>]*>', '', html, flags=re.IGNORECASE)
            
            text = re.sub(r'<[^>]+>', ' ', html)
            text = re.sub(r'\s+', ' ', text).strip()
            
            if len(text) < 50:
                return {
                    'success': False,
                    'error': 'Замало тексту після обробки',
                    'url': url
                }
            
            return {
                'success': True,
                'text': text[:5000],
                'source': self._extract_domain(url),
                'url': url
            }
            
        except Exception as e:
            return {'success': False, 'error': f'Помилка: {str(e)}', 'url': url}
    
    def _extract_domain(self, url: str) -> str:
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
        return jsonify({'status': 'online', 'version': '6.0-radical'}), 200

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

        # АНАЛІЗ ТЕКСТУ
        result = engine.analyze(text_to_analyze)
        
        if 'error' in result:
            return jsonify({'error': result['error']}), 400

        # ПІДГОТОВКА ВІДПОВІДІ
        diag = result.get('diagnostics', {})
        
        # Обчислення індексів
        total_chaos_index = (
            diag.get('chaos_markers', 0) * 0.5 +
            diag.get('semantic_dissonance', 0) * 50 +
            diag.get('semantic_flow', 0) * 30
        )
        
        impact_score = (
            result['entropy'] * 100 +
            diag.get('semantic_dissonance', 0) * 70 +
            diag.get('sanity_penalty', 0) * 60 +
            diag.get('semantic_flow', 0) * 50
        )
        
        # Сформувати відповідь
        response = {
            'entropy': result['entropy'],
            'status': result['status'],
            'verdict': result['verdict'],
            'language': result['language'],
            'source': source,
            'mode': 'url' if url else 'text',
            'status_class': result['status'].lower(),
            'explanation': generate_explanation(result, diag),
            'impact_score': round(impact_score, 2),
            
            # МЕТРИКИ
            'shannon_entropy': diag.get('shannon_entropy', 0),
            'complexity': diag.get('complexity', 0),
            'total_chaos_index': round(total_chaos_index, 2),
            'sanity_penalty': diag.get('sanity_penalty', 0),
            'chaos_markers': diag.get('chaos_markers', 0),
            'semantic_dissonance': diag.get('semantic_dissonance', 0),
            'noise_markers': diag.get('noise_markers', 0),
            'signal_markers': diag.get('signal_markers', 0),
            'academic_markers': diag.get('academic_markers', 0),
            'academic_density': round(diag.get('academic_markers', 0) / max(1, diag.get('word_count', 1)), 3),
            'is_academic_context': result.get('is_academic_context', False),
            'shout_factor': diag.get('shout_factor', 0),
            'number_density': diag.get('number_density', 0),
            'word_count': diag.get('word_count', 0),
            'char_count': diag.get('char_count', 0),
            'signal_noise_ratio': round(diag.get('noise_markers', 0) / max(1, diag.get('signal_markers', 1)), 3),
        }
        
        # Аналіз емоційного впливу
        emotional_pressure = (
            diag.get('chaos_markers', 0) > 5 or 
            diag.get('semantic_flow', 0) > 0.3 or
            'критичний' in result['status'].lower()
        )
        
        disorientation_risk = (
            diag.get('semantic_dissonance', 0) > 0.3 or
            diag.get('semantic_flow', 0) > 0.4
        )
        
        response['emotional_pressure'] = emotional_pressure
        response['disorientation_risk'] = disorientation_risk
        response['emotional_analysis'] = generate_emotional_analysis(result, diag)
        
        # Додати витягнутий текст для URL
        if url and len(text_to_analyze) > 0:
            response['extracted_text'] = text_to_analyze[:1000] + ('...' if len(text_to_analyze) > 1000 else '')
            response['extracted_text_length'] = len(text_to_analyze)
            response['show_extracted_text'] = True
        
        return jsonify(response), 200

    except Exception as e:
        print(f"❌ Загальна помилка: {str(e)}")
        return jsonify({'error': f'Внутрішня помилка: {str(e)}'}), 500

def generate_explanation(result: dict, diag: dict) -> str:
    """Генерує пояснення"""
    verdict = result['verdict']
    
    if 'НАУКОВИЙ НІГІЛІЗМ' in verdict:
        return "Текст зловживає науковою термінологією для обґрунтування абсурдних соціально-економічних концепцій."
    
    elif 'ДЗЕРКАЛЬНА МАНІПУЛЯЦІЯ' in verdict:
        return "Текст використовує риторику 'розкриття правди' для приховування власних маніпулятивних технік."
    
    elif 'КОРПОРАТИВНИЙ ОКУЛЬТИЗМ' in verdict:
        return "Корпоративний жаргон змішаний з езотерикою, створюючи токсичну гібридну риторику."
    
    elif 'ГІБРИДНА ТОКСИЧНІСТЬ' in verdict:
        return "Текст поєднує елементи різних дискурсів у штучну та маніпулятивну конструкцію."
    
    else:
        return "Текст демонструє нормальну семантичну структуру."

def generate_emotional_analysis(result: dict, diag: dict) -> str:
    """Генерує аналіз емоційного впливу"""
    if 'критичний' in result['status'].lower():
        return "ВИСОКИЙ РИЗИК МАНІПУЛЯЦІЇ: текст використовує складні семантичні конструкції для прихованого впливу."
    
    elif diag.get('semantic_flow', 0) > 0.3:
        return "СЕМАНТИЧНА НЕСТАБІЛЬНІСТЬ: швидкі переходи між різними концепціями можуть викликати дезорієнтацію."
    
    else:
        return "МІНІМАЛЬНИЙ ЕМОЦІЙНИЙ ВПЛИВ."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
