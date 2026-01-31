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
            
            # Очищення HTML
            html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
            html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
            
            # Видалення всіх тегів зображень
            html = re.sub(r'<img[^>]*>', '', html, flags=re.IGNORECASE)
            
            # Вилучення тексту
            text = self._extract_text(html)
            
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
    
    def _extract_text(self, html: str) -> str:
        """Видобуває текст з HTML"""
        # Видалення всіх тегів
        text = re.sub(r'<[^>]+>', ' ', html)
        # Видалення зайвих пробілів
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _extract_domain(self, url: str) -> str:
        """Видобуває домен з URL"""
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
        return jsonify({'status': 'online', 'version': '3.8-enhanced'}), 200

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data'}), 400

        url = data.get('url', '').strip()
        raw_text = data.get('text', '').strip()
        
        text_to_analyze = ""
        source = 'Manual Input'
        
        if url:
            print(f"🔗 Обробка URL: {url}")
            
            if not url.startswith(('http://', 'https://')):
                return jsonify({'error': 'Невірний протокол URL'}), 400
            
            result = extractor.extract_from_url(url)
            
            if not result['success']:
                return jsonify({'error': result['error']}), 400
            
            text_to_analyze = result['text']
            source = result['source']
            
            print(f"✅ Текст витягнуто: {len(text_to_analyze)} символів")
            
        else:
            text_to_analyze = raw_text
            if data.get('source'):
                source = data.get('source')
            print(f"📝 Аналіз тексту: {len(text_to_analyze)} символів")

        if not text_to_analyze or len(text_to_analyze) < 20:
            return jsonify({'error': 'Текст занадто короткий'}), 400

        # АНАЛІЗ ТЕКСТУ
        print("🔍 Запуск розширеного аналізу...")
        result = engine.analyze(text_to_analyze)
        
        if 'error' in result:
            return jsonify({'error': result['error']}), 400

        # ПІДГОТОВКА ВІДПОВІДІ
        diag = result.get('diagnostics', {})
        
        # Обчислення індексів
        total_chaos_index = (
            diag.get('chaos_markers', 0) * 0.2 +
            diag.get('semantic_dissonance', 0) * 50
        )
        
        impact_score = (
            result['entropy'] * 100 +
            diag.get('semantic_dissonance', 0) * 50 +
            diag.get('sanity_penalty', 0) * 40
        )
        
        # Сформувати відповідь для фронтенду
        response = {
            'entropy': result['entropy'],
            'status': result['status'],
            'verdict': result['verdict'],
            'language': result['language'],
            'source': source,
            'mode': 'url' if url else 'text',
            'status_class': result['status'].lower(),
            'explanation': generate_explanation(result),
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
            'is_academic_context': diag.get('academic_markers', 0) > 5,
            'shout_factor': diag.get('shout_factor', 0),
            'number_density': diag.get('number_density', 0),
            'word_count': diag.get('word_count', 0),
            'char_count': diag.get('char_count', 0),
            'signal_noise_ratio': round(diag.get('noise_markers', 0) / max(1, diag.get('signal_markers', 1)), 3)
        }
        
        # Додати витягнутий текст для URL
        if url and len(text_to_analyze) > 0:
            response['extracted_text'] = text_to_analyze[:1000] + ('...' if len(text_to_analyze) > 1000 else '')
            response['extracted_text_length'] = len(text_to_analyze)
            response['show_extracted_text'] = True
        
        print(f"📊 Результат: entropy={result['entropy']}, verdict={result['verdict']}")
        return jsonify(response), 200

    except Exception as e:
        print(f"❌ Загальна помилка: {str(e)}")
        return jsonify({'error': f'Внутрішня помилка: {str(e)}'}), 500

def generate_explanation(result: dict) -> str:
    """Генерує пояснення на основі результатів аналізу"""
    verdict = result['verdict']
    
    if 'ПСЕВДОПРАВОВИЙ' in verdict:
        return "Текст містить ознаки псевдоправової риторики (суверен-гражданин) та семантичний дисонанс."
    
    elif 'ТЕХНО-УТОПІЧНА' in verdict:
        return "Наукові терміни використані для обґрунтування параноїдальних концепцій."
    
    elif 'ЕЗОТЕРИЧНИЙ ДЕЛІРІЙ' in verdict:
        return "Текст поєднує духовні/езотеричні концепції з конспірологічними елементами."
    
    elif 'ІНТЕЛЕКТУАЛЬНА МІМІКРІЯ' in verdict:
        return "Текст імітує науковий стиль, але містить несумісні концепції."
    
    elif 'КРИТИЧНА' in verdict:
        return "Текст демонструє критичний рівень логічних несумісностей."
    
    elif result['entropy'] > 0.6:
        return "Високий рівень інформаційного хаосу."
    
    else:
        return "Текст відповідає нормам логічної сумісності."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
