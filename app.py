from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import re
import urllib.request
from veritas_calibrated_core import VeritasCalibratedCore

app = Flask(__name__, static_folder='.')
CORS(app)

engine = VeritasCalibratedCore()

class TextExtractor:
    """Екстрактор тільки тексту, без обробки зображень"""
    
    def extract_from_url(self, url: str) -> dict:
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            with urllib.request.urlopen(req, timeout=15) as response:
                content_type = response.headers.get('Content-Type', '')
                
                # ПЕРЕВІРКА: тільки HTML, без зображень/відео
                if not any(ct in content_type.lower() for ct in ['text/html', 'text/plain']):
                    return {
                        'success': False,
                        'error': f'Непідтримуваний тип контенту: {content_type}. Підтримується тільки HTML/текст.',
                        'url': url
                    }
                
                html = response.read().decode('utf-8', errors='ignore')
            
            # Очищення HTML
            cleaned = self._clean_html(html)
            
            # Видалення всіх тегів зображень та мультимедіа
            cleaned = re.sub(r'<img[^>]*>', '', cleaned, flags=re.IGNORECASE)
            cleaned = re.sub(r'<video[^>]*>.*?</video>', '', cleaned, flags=re.DOTALL | re.IGNORECASE)
            cleaned = re.sub(r'<audio[^>]*>.*?</audio>', '', cleaned, flags=re.DOTALL | re.IGNORECASE)
            cleaned = re.sub(r'<iframe[^>]*>.*?</iframe>', '', cleaned, flags=re.DOTALL | re.IGNORECASE)
            
            # Вилучення тексту
            text = self._extract_text(cleaned)
            
            if len(text) < 50:
                return {
                    'success': False,
                    'error': 'Замало тексту після обробки (менше 50 символів)',
                    'url': url
                }
            
            return {
                'success': True,
                'text': text[:10000],  # Обмеження довжини
                'source': self._extract_domain(url),
                'url': url,
                'char_count': len(text),
                'word_count': len(text.split())
            }
            
        except urllib.error.URLError as e:
            return {'success': False, 'error': f'Помилка URL: {str(e)}', 'url': url}
        except Exception as e:
            return {'success': False, 'error': f'Помилка обробки: {str(e)}', 'url': url}
    
    def _clean_html(self, html: str) -> str:
        """Очищує HTML від скриптів, стилів та іншого нетекстового вмісту"""
        # Видалення скриптів
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        # Видалення стилів
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
        # Видалення коментарів
        html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
        # Видалення навігаційних/меню елементів
        html = re.sub(r'<nav[^>]*>.*?</nav>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<header[^>]*>.*?</header>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<footer[^>]*>.*?</footer>', '', html, flags=re.DOTALL | re.IGNORECASE)
        return html
    
    def _extract_text(self, html: str) -> str:
        """Видобуває текст з HTML"""
        # Вилучення тексту з параграфів
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, flags=re.DOTALL | re.IGNORECASE)
        
        if paragraphs:
            # Об'єднання та очищення параграфів
            text = ' '.join(paragraphs)
        else:
            # Альтернативний метод: видалення всіх тегів
            text = re.sub(r'<[^>]+>', ' ', html)
        
        # Додаткове очищення
        text = re.sub(r'\s+', ' ', text)  # Видалення зайвих пробілів
        text = re.sub(r'[^\w\s.,!?;:()"\'-]', '', text)  # Видалення спецсимволів
        text = text.strip()
        
        return text
    
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
        title = 'Manual Input'
        extracted_length = 0
        
        if url:
            print(f"🔗 Обробка URL: {url}")
            
            # ПЕРЕВІРКА: тільки HTTP/HTTPS
            if not url.startswith(('http://', 'https://')):
                return jsonify({'error': 'Невірний протокол URL. Використовуйте http:// або https://'}), 400
            
            # Витягування тексту
            result = extractor.extract_from_url(url)
            
            if not result['success']:
                return jsonify({'error': result['error']}), 400
            
            text_to_analyze = result['text']
            source = result['source']
            extracted_length = result['char_count']
            
            print(f"✅ Текст витягнуто: {extracted_length} символів, {result['word_count']} слів")
            print(f"📌 Джерело: {source}")
            
        else:
            text_to_analyze = raw_text
            if data.get('source'):
                source = data.get('source')
            print(f"📝 Аналіз тексту: {len(text_to_analyze)} символів, {len(text_to_analyze.split())} слів")

        if not text_to_analyze or len(text_to_analyze) < 20:
            return jsonify({'error': 'Текст занадто короткий для аналізу'}), 400

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
            diag.get('semantic_dissonance', 0) * 50 +
            diag.get('penalties', {}).get('chaos', 0) * 30
        )
        
        impact_score = (
            result['entropy'] * 100 +
            diag.get('semantic_dissonance', 0) * 50 +
            diag.get('penalties', {}).get('sanity', 0) * 40 +
            diag.get('penalties', {}).get('manipulation', 0) * 30
        )
        
        # Сформувати відповідь для фронтенду
        response = {
            'entropy': result['entropy'],
            'status': result['status'],
            'verdict': result['verdict'],
            'language': result['language'],
            'source': source,
            'title': title,
            'mode': 'url' if url else 'text',
            'status_class': result['status'].lower(),
            'explanation': self._generate_explanation(result, diag),
            'impact_score': round(impact_score, 2),
            
            # МЕТРИКИ ДЛЯ ФРОНТЕНДУ
            'shannon_entropy': diag.get('shannon_entropy', 0),
            'complexity': diag.get('complexity', 0),
            'total_chaos_index': round(total_chaos_index, 2),
            'sanity_penalty': diag.get('sanity_penalty', 0),
            'chaos_markers': diag.get('chaos_markers', 0),
            'semantic_dissonance': diag.get('semantic_dissonance', 0),
            'noise_markers': diag.get('noise_markers', 0),
            'signal_markers': diag.get('signal_markers', 0),
            'academic_markers': diag.get('academic_markers', 0),
            'academic_density': diag.get('academic_markers', 0) / max(1, diag.get('word_count', 1)),
            'is_academic_context': diag.get('academic_markers', 0) > 5,
            'shout_factor': diag.get('shout_factor', 0),
            'number_density': diag.get('number_density', 0),
            'word_count': diag.get('word_count', 0),
            'char_count': diag.get('char_count', 0),
            'signal_noise_ratio': round(diag.get('noise_markers', 0) / max(1, diag.get('signal_markers', 1)), 3),
            
            # ДЕТАЛІ АНАЛІЗУ (для дебагу)
            'analysis_details': {
                'category_counts': diag.get('category_counts', {}),
                'penalties': diag.get('penalties', {}),
                'is_news': diag.get('is_news_context', False),
                'has_clusters': diag.get('has_incompatible_clusters', False)
            }
        }
        
        # Додати витягнутий текст тільки для URL
        if url and extracted_length > 0:
            response['extracted_text'] = text_to_analyze[:1500] + ('...' if len(text_to_analyze) > 1500 else '')
            response['extracted_text_length'] = extracted_length
            response['show_extracted_text'] = True
        
        print(f"📊 Результат: entropy={result['entropy']}, verdict={result['verdict']}, chaos={diag.get('chaos_markers', 0)}")
        return jsonify(response), 200

    except urllib.error.URLError as e:
        print(f"❌ Помилка URL: {str(e)}")
        return jsonify({'error': f'Помилка URL: {str(e)}'}), 400
    except Exception as e:
        print(f"❌ Загальна помилка: {str(e)}")
        return jsonify({'error': f'Внутрішня помилка: {str(e)}'}), 500

def _generate_explanation(self, result: Dict, diagnostics: Dict) -> str:
    """Генерує пояснення на основі результатів аналізу"""
    verdict = result['verdict']
    
    if 'ПСЕВДОПРАВОВИЙ' in verdict:
        return "Текст містить ознаки псевдоправової риторики (суверен-гражданин), що поєднує юридичні терміни з езотеричними концепціями."
    
    elif 'ТЕХНО-УТОПІЧНА' in verdict:
        return "Високотехнологічна маніпуляція: наукові терміни використані для обґрунтування параноїдальних концепцій."
    
    elif 'ЕЗОТЕРИЧНИЙ ДЕЛІРІЙ' in verdict:
        return "Текст поєднує духовні/езотеричні концепції з конспірологічними елементами, створюючи семантичний дисонанс."
    
    elif 'ІНТЕЛЕКТУАЛЬНА МІМІКРІЯ' in verdict:
        return "Високий семантичний дисонанс: текст імітує науковий/академічний стиль, але містить несумісні концепції."
    
    elif 'КРИТИЧНА' in verdict:
        return "Текст демонструє критичний рівень логічних несумісностей та семантичних порушень."
    
    elif diagnostics.get('semantic_dissonance', 0) > 0.4:
        return "Значний семантичний дисонанс: текст поєднує несумісні категорії концепцій."
    
    else:
        return "Текст відповідає нормам логічної сумісності та семантичної цілісності."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
