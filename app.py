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
        text = re.sub(r'<[^>]+>', ' ', html)
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
            diag.get('chaos_markers', 0) * 0.5 +
            diag.get('semantic_dissonance', 0) * 50 +
            diag.get('hybrid_toxicity', 0) * 30
        )
        
        impact_score = (
            result['entropy'] * 100 +
            diag.get('semantic_dissonance', 0) * 70 +  # ↑ збільшено
            diag.get('sanity_penalty', 0) * 60 +       # ↑ збільшено
            diag.get('hybrid_toxicity', 0) * 50 +      # ↑ збільшено
            diag.get('cross_domain_absurdity', 0) * 40 # ↑ збільшено
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
            'hybrid_toxicity': diag.get('hybrid_toxicity', 0),
            'cross_domain_absurdity': diag.get('cross_domain_absurdity', 0),
            'sentence_absurdity': diag.get('sentence_absurdity', 0)
        }
        
        # Аналіз емоційного впливу
        emotional_pressure = (
            diag.get('chaos_markers', 0) > 5 or 
            diag.get('hybrid_toxicity', 0) > 0.3 or
            'критичний' in result['status'].lower() or
            'нігілізм' in result['verdict'].lower() or
            'маніпуляція' in result['verdict'].lower()
        )
        
        disorientation_risk = (
            diag.get('semantic_dissonance', 0) > 0.3 or
            diag.get('cross_domain_absurdity', 0) > 0.4 or
            diag.get('sentence_absurdity', 0) > 0.2
        )
        
        response['emotional_pressure'] = emotional_pressure
        response['disorientation_risk'] = disorientation_risk
        response['emotional_analysis'] = generate_emotional_analysis(result, diag)
        
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

def generate_explanation(result: dict, diag: dict) -> str:
    """Генерує пояснення на основі результатів аналізу"""
    verdict = result['verdict']
    hybrid_toxicity = diag.get('hybrid_toxicity', 0)
    cross_domain_absurdity = diag.get('cross_domain_absurdity', 0)
    
    if 'КРОС-ДОМЕННИЙ СЕМАНТИЧНИЙ КОЛАПС' in verdict:
        return "Текст поєднує несумісні концепції з різних сфер знань (наука+фінанси+фізика), створюючи семантичну кашу."
    
    elif 'ГІБРИДНИЙ НАУКОВИЙ НІГІЛІЗМ' in verdict:
        return "Наукові терміни використовуються для обґрунтування абсурдних соціально-економічних висновків (нейтрино → фондовий ринок)."
    
    elif 'ДЗЕРКАЛЬНА МАНІПУЛЯЦІЯ' in verdict:
        return "Текст звинувачує інших у маніпуляціях, використовуючи сам методи маніпулятивної риторики ('брехня', 'фейк')."
    
    elif 'КОРПОРАТИВНИЙ ОКУЛЬТИЗМ' in verdict:
        return "Корпоративний жаргон змішаний з езотеричними концепціями, створюючи псевдонаукову риторику для впливу."
    
    elif 'ФІНАНСОВО-ЕЗОТЕРИЧНИЙ АБСУРД' in verdict:
        return "Фінансові терміни поєднуються з езотерикою, створюючи семантичний колапс."
    
    elif 'ПСЕВДОНАУКОВА ДЕЗІНФОРМАЦІЯ' in verdict:
        return "Науковий стиль використаний для поширення конспірологічних ідей."
    
    elif 'НАУКОВИЙ НІГІЛІЗМ' in verdict:
        return "Фізичні терміни застосовуються до соціальних явищ, створюючи науково-утопічну маячню."
    
    elif hybrid_toxicity > 0.4:
        return "Високий рівень гібридної токсичності: текст поєднує правду з маніпулятивними техніками."
    
    elif cross_domain_absurdity > 0.5:
        return "Високий рівень кросс-доменної абсурдності: несумісні поняття з різних доменів."
    
    elif result['entropy'] > 0.6:
        return "Високий рівень інформаційного хаосу та семантичної несумісності."
    
    else:
        return "Текст відповідає нормам логічної сумісності."

def generate_emotional_analysis(result: dict, diag: dict) -> str:
    """Генерує аналіз емоційного впливу"""
    hybrid_toxicity = diag.get('hybrid_toxicity', 0)
    chaos_markers = diag.get('chaos_markers', 0)
    semantic_dissonance = diag.get('semantic_dissonance', 0)
    
    if hybrid_toxicity > 0.4:
        return "ВИСОКА ГІБРИДНА ТОКСИЧНІСТЬ: текст поєднує правду з тонкою отрутою, створюючи ефект 'отруєної конфети'. Ризик поступового зомбування."
    
    elif chaos_markers > 10:
        return "ВИСОКИЙ РІВЕНЬ ХАОСУ: поєднання езотерики, конспірології та наукової фантастики створює когнітивне навантаження."
    
    elif semantic_dissonance > 0.5:
        return "СЕМАНТИЧНИЙ ДИСОНАНС: логічні несумісності можуть викликати дезорієнтацію та підвищену критичність."
    
    elif 'ДЗЕРКАЛЬНА' in result['verdict']:
        return "ДЗЕРКАЛЬНА ТЕХНІКА: текст звинувачує інших у власних методах, створюючи когнітивний дисонанс."
    
    else:
        return "МІНІМАЛЬНИЙ ЕМОЦІЙНИЙ ВПЛИВ: текст не містить явних маніпулятивних технік."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
