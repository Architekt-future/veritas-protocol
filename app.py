from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import re
import urllib.request
from veritas_calibrated_core import VeritasCalibratedCore

app = Flask(__name__, static_folder='.')
CORS(app)

engine = VeritasCalibratedCore()

class SimpleExtractor:
    def extract_from_url(self, url: str, html: str) -> dict:
        try:
            cleaned = self._clean_html(html)
            title = self._extract_title(html)
            text = self._extract_paragraphs(cleaned)
            source = self._extract_domain(url)
            return {
                'success': True,
                'title': title,
                'text': text,
                'source': source,
                'url': url
            }
        except Exception as e:
            return {'success': False, 'error': str(e), 'url': url}

    def _clean_html(self, html: str) -> str:
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
        return html

    def _extract_title(self, html: str) -> str:
        match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
        return match.group(1).strip() if match else "Unknown Title"

    def _extract_paragraphs(self, html: str) -> str:
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, flags=re.DOTALL | re.IGNORECASE)
        text = ' '.join(paragraphs) if paragraphs else re.sub(r'<[^>]+>', ' ', html)
        return self._clean_text(text)

    def _clean_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def _extract_domain(self, url: str) -> str:
        match = re.search(r'https?://(?:www\.)?([^/]+)', url)
        return match.group(1) if match else "unknown"

extractor = SimpleExtractor()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/analyze', methods=['GET', 'POST', 'OPTIONS'])
def analyze():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    if request.method == 'GET':
        return jsonify({'status': 'online', 'version': '3.7-final'}), 200

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data'}), 400

        url = data.get('url', '').strip()
        raw_text = data.get('text', '').strip()
        source = 'Manual Input'
        title = 'Manual Input'
        text_to_analyze = ""
        show_extracted_text = False
        extracted_text_for_display = ""

        if url:
            print(f"🔗 Скрапінг URL: {url}")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8', errors='ignore')
            
            print(f"📄 HTML отримано ({len(html)} символів)")
            ext = extractor.extract_from_url(url, html)
            
            if not ext['success']: 
                raise Exception(ext['error'])
            
            text_to_analyze = ext['text']
            extracted_text_for_display = ext['text']
            source = ext['source']
            title = ext['title']
            show_extracted_text = True
            
            print(f"✅ Текст витягнуто: {len(text_to_analyze)} символів, {len(text_to_analyze.split())} слів")
            print(f"📌 Джерело: {source}, Заголовок: {title}")
            
        else:
            text_to_analyze = raw_text
            show_extracted_text = False
            if data.get('source'):
                source = data.get('source')
            print(f"📝 Аналіз тексту: {len(text_to_analyze)} символів, {len(text_to_analyze.split())} слів")

        if not text_to_analyze or len(text_to_analyze) < 10:
            return jsonify({'error': 'Content too short'}), 400

        # 1. Запуск аналізу ядра
        print("🔍 Запуск аналізу ядра...")
        result = engine.analyze(text_to_analyze)
        if 'error' in result:
            return jsonify({'error': result['error']}), 400

        # 2. Коректне отримання всіх показників з diagnostics
        diag = result.get('diagnostics', {})
        entropy = diag.get('shannon_entropy', 0)
        complexity = diag.get('complexity', 0)
        chaos_markers = diag.get('chaos_markers', 0)
        sanity_penalty = diag.get('sanity_penalty', 0)
        number_density = diag.get('number_density', 0)
        shout_factor = diag.get('shout_factor', 0)
        noise_markers = diag.get('noise_markers', 0)
        signal_markers = diag.get('signal_markers', 0)
        academic_markers = diag.get('academic_markers', 0)
        academic_density = diag.get('academic_density', 0)
        is_academic = diag.get('is_academic_context', False)
        lang = result.get('language', 'UK')

        # 3. Розрахунок інтегрального індексу хаосу
        total_chaos_index = (chaos_markers * 0.1) + (shout_factor * 30) + (noise_markers * 0.3)
        
        # Корекція для академічних текстів
        if is_academic:
            total_chaos_index *= 0.3
            if academic_markers > 10:
                total_chaos_index *= 0.5

        # 4. Аналіз емоційного впливу
        emotional_pressure = False
        disorientation_risk = False
        emotional_comment = ""

        if shout_factor > 0.3 or noise_markers > signal_markers * 2:
            emotional_pressure = True
        
        if entropy > 0.5 and complexity > 0.7:
            disorientation_risk = True

        # Формування висновку щодо впливу
        if emotional_pressure and disorientation_risk:
            emotional_comment = "ВИСОКИЙ РІВЕНЬ ЕМОЦІЙНОГО ВПЛИВУ ТА ДЕЗОРІЄНТАЦІЇ. Текст використовує капслок, перебільшення та має високу ентропію, що може спантеличувати читача та впливати на його думку."
        elif emotional_pressure:
            emotional_comment = "ПОМІТНИЙ ЕМОЦІЙНИЙ ТИСК. Текст містить елементи, що прагнуть викликати сильну емоційну реакцію (капслок, перебільшення, маркери шуму)."
        elif disorientation_risk:
            emotional_comment = "РИЗИК ДЕЗОРІЄНТАЦІЇ. Висока ентропія та складність структури можуть утруднити розуміння та сприйняття основної думки."
        else:
            emotional_comment = "ЕМОЦІЙНИЙ ВПЛИВ МІНІМАЛЬНИЙ. Текст зосереджений на фактах та логіці."

        # 5. НОВА логіка вердикту - СПРОЩЕНО
        impact_score = (total_chaos_index * 0.3) + (sanity_penalty * 15) + (entropy * 100 * 0.4)
        
        # Сильна корекція для академічних текстів
        if is_academic:
            impact_score *= 0.3
            if signal_markers > noise_markers * 5:
                impact_score *= 0.5
        
        # Корекція на співвідношення сигнал/шум
        if signal_markers > 0:
            signal_noise_ratio = noise_markers / signal_markers
            if signal_noise_ratio < 0.05:
                impact_score *= 0.4
            elif signal_noise_ratio > 1.0:
                impact_score *= 1.8

        # РАДИКАЛЬНО СПРОЩЕНА логіка вердикту
        if sanity_penalty > 0.5 and (shout_factor > 0.4 or chaos_markers > 15):
            # Явна маячня: високий shout_factor + chaos_markers + sanity_penalty
            status_class = 'critical'
            verdict = 'КРИТИЧНА НЕСУМІСНІСТЬ ЛОГІКИ'
            explanation = 'Текст містить взаємовиключні концепції та порушує базові принципи логічної сумісності.'
        elif impact_score > 20:
            status_class = 'warning'
            verdict = 'ВИСОКИЙ РІВЕНЬ МАНІПУЛЯЦІЇ'
            explanation = 'Виявлено структурні аномалії та ознаки інформаційного шуму.'
        elif impact_score > 10:
            status_class = 'acceptable'
            verdict = 'ПРИЙНЯТНА СТРУКТУРОВАНА ІНФОРМАЦІЯ'
            explanation = 'Текст має деякі особливості, але загалом відповідає нормам.'
        elif is_academic and impact_score < 5:
            status_class = 'success'
            verdict = 'АКАДЕМІЧНИЙ ТЕКСТ ВИСОКОЇ ЯКОСТІ'
            explanation = 'Текст демонструє високий рівень логічної цілісності та наукової обґрунтованості.'
        else:
            status_class = 'success'
            verdict = 'СТАБІЛЬНИЙ ЛОГІЧНИЙ СИГНАЛ'
            explanation = 'Параметри тексту в межах норми, високий рівень логічної цілісності.'

        # 6. Формуємо повний словник для фронтенду
        final_result = {
            'entropy': result.get('entropy', 0),
            'status': status_class.upper(),
            'verdict': verdict,
            'language': lang,
            'source': source,
            'title': title,
            'mode': 'url' if url else 'text',
            'status_class': status_class,
            'explanation': explanation,
            'impact_score': round(impact_score, 2),
            # Всі метрики для діагностики
            'shannon_entropy': entropy,
            'complexity': complexity,
            'chaos_markers': chaos_markers,
            'total_chaos_index': round(total_chaos_index, 2),
            'sanity_penalty': sanity_penalty,
            'number_density': number_density,
            'shout_factor': shout_factor,
            'noise_markers': noise_markers,
            'signal_markers': signal_markers,
            'academic_markers': academic_markers,
            'academic_density': academic_density,
            'is_academic_context': is_academic,
            # Витягнутий текст для відображення - ТІЛЬКИ ДЛЯ URL
            'show_extracted_text': show_extracted_text,
            # Результати аналізу впливу
            'emotional_pressure': emotional_pressure,
            'disorientation_risk': disorientation_risk,
            'emotional_analysis': emotional_comment,
            # Додаткові дані
            'word_count': diag.get('word_count', 0),
            'char_count': diag.get('char_count', 0),
            'signal_noise_ratio': round(noise_markers / signal_markers, 3) if signal_markers > 0 else 0
        }

        # Додаємо текст тільки для URL режиму
        if show_extracted_text:
            final_result['extracted_text'] = extracted_text_for_display[:2000] + ('...' if len(extracted_text_for_display) > 2000 else '')
            final_result['extracted_text_length'] = len(extracted_text_for_display)

        print(f"📊 Результат: entropy={final_result['entropy']}, verdict={verdict}, academic={is_academic}, chaos={chaos_markers}, sanity={sanity_penalty}")
        return jsonify(final_result), 200

    except urllib.error.URLError as e:
        print(f"❌ Помилка URL: {str(e)}")
        return jsonify({'error': f'URL error: {str(e)}'}), 400
    except Exception as e:
        print(f"❌ Загальна помилка: {str(e)}")
        return jsonify({'error': f'Internal error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
