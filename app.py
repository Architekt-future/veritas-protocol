from flask import Flask, request, jsonify, render_template
from veritas_calibrated_core import VeritasAnalyzer
import re

app = Flask(__name__)

def preprocess_text(text):
    """
    Очищення тексту від реклами та технічної інформації
    """
    if not text:
        return ""
    
    # Розділяємо на рядки
    lines = text.split('\n')
    cleaned_lines = []
    
    # Ключові слова для видалення
    skip_patterns = [
        r'пряме гіперпосилання.*обов\'язкове',
        r'передрук.*копіювання.*заборонено',
        r'редакція.*може.*не.*поділяти',
        r'пресреліз',
        r'реклама',
        r'новини компаній',
        r'promoted',
        r'на правах реклами'
    ]
    
    for line in lines:
        line_lower = line.lower().strip()
        should_skip = False
        
        # Перевірка на шаблони для пропуску
        for pattern in skip_patterns:
            if re.search(pattern, line_lower):
                should_skip = True
                break
        
        # Пропускаємо короткі рекламні рядки
        if not should_skip and len(line.strip()) > 20:
            cleaned_lines.append(line.strip())
    
    # З'єднуємо назад
    if cleaned_lines:
        cleaned_text = ' '.join(cleaned_lines)
        # Видаляємо зайві пробіли
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        return cleaned_text
    
    return text.strip()

@app.route('/')
def index():
    """Головна сторінка"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Кінцева точка для аналізу тексту
    """
    try:
        # Отримуємо дані
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Не надано текст для аналізу',
                'status': 'error'
            }), 400
        
        # Очищуємо текст
        original_text = data['text']
        processed_text = preprocess_text(original_text)
        
        if len(processed_text) < 30:
            return jsonify({
                'error': 'Текст занадто короткий після очищення',
                'status': 'error'
            }), 400
        
        # Аналізуємо
        analyzer = VeritasAnalyzer()
        results = analyzer.analyze_text(processed_text)
        
        # Готуємо відповідь
        response = {
            'status': 'success',
            'results': {
                'logic_inconsistency': results['logic_inconsistency'],
                'entropy': results['entropy'],
                'chaos_index': results['chaos_index'],
                'noise_markers': results['noise_markers'],
                'signal_markers': results['signal_markers'],
                'chaos_markers': results['chaos_markers'],
                'scream_factor': results['scream_factor'],
                'number_density': results['number_density'],
                'sanitary_penalty': results['sanitary_penalty'],
                'influence_index': results['influence_index'],
                'academic_markers': results['academic_markers'],
                'noise_signal_ratio': results['noise_signal_ratio'],
                'word_count': results['word_count'],
                'char_count': results['char_count'],
                'flags': results['flags']
            },
            'context': {
                'is_academic': 'Текст не визначено як академічний' if results['academic_markers'] < 3 else 'Можливий академічний текст',
                'text_preview': processed_text[:200] + '...' if len(processed_text) > 200 else processed_text
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/test', methods=['GET'])
def test():
    """
    Тестова сторінка для перевірки роботи
    """
    # Тестовий новинний текст
    test_text = """
    Також Сили оборони завдали ураження по скупченню живої сили ЗС РФ. 
    Підрозділи Сил оборони України уночі 31 січня завдали ураження по низці військових об’єктів противника на тимчасово окупованих територіях України та на території РФ. 
    Про це повідомляє Генштаб ЗСУ. На тимчасово окупованій території Луганської області, в районі населеного пункту Кам’янка, зафіксовано ураження зенітного ракетного комплексу "Тор-М1" противника. 
    Результати удару уточнюються.
    """
    
    analyzer = VeritasAnalyzer()
    results = analyzer.analyze_text(test_text)
    
    return jsonify({
        'test': 'військові новини',
        'results': {
            'logic_inconsistency': results['logic_inconsistency'],
            'sanitary_penalty': results['sanitary_penalty'],
            'chaos_markers': results['chaos_markers'],
            'flags': results['flags'],
            'word_count': results['word_count']
        },
        'expected': {
            'logic_inconsistency': 'низьке (< 0.3)',
            'flags': 'немає КРИТИЧНА НЕСУМІСНІСТЬ',
            'note': 'Для військових звітів має бути низький штраф'
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
