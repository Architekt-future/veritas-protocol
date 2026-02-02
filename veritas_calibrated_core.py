"""
Veritas Protocol - Flask Backend v3.0 with LAC Integration
Integrated: LAC (Logical Anomaly Classifier) + Veritas Calibrated Core
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import re
import urllib.request
import math
from collections import Counter

# ============================================================
# LAC (LOGICAL ANOMALY CLASSIFIER) - ІНТЕГРОВАНИЙ КЛАС
# ============================================================

class LogicalAnomalyClassifier:
    """Покращений LAC з інтеграцією в Veritas архітектуру"""
    
    def __init__(self):
        # LAC Логічні оператори та їхні протиріччя
        self.logical_operators = {
            'і': ['не', 'але', 'хоча', 'однак'],
            'або': ['і', 'разом', 'спільно'],
            'якщо-то': ['не завжди', 'іноді', 'виняток'],
            'всі': ['ніхто', 'деякі', 'не всі'],
            'ніхто': ['всі', 'деякі', 'хтось'],
            'завжди': ['ніколи', 'іноді', 'рідко'],
            'ніколи': ['завжди', 'іноді', 'часто']
        }
        
        # Логічні помилки (фалії) з вагами
        self.logical_fallacies = {
            'ad_hominem': (r'(ти|ви).*?(дурний|не розумієш|не компетентний)', 0.3),
            'false_dilemma': (r'(або.*?або|або.*?чи).*?(немає іншого вибору)', 0.35),
            'slippery_slope': (r'(якщо.*?то.*?призведе до|ланцюгова реакція)', 0.25),
            'circular_reasoning': (r'(тому що.*?тому що|оскільки.*?оскільки)', 0.4),
            'post_hoc': (r'(після того як.*?отже|послідовність.*?причинність)', 0.3),
            'hasty_generalization': (r'(один випадок.*?значить всі|на основі одного)', 0.35),
            'appeal_to_authority': (r'(експерт сказав|професор стверджує).*?(значить правда)', 0.28),
            'appeal_to_emotion': (r'(думайте про дітей|це жахливо|це несправедливо).*?(значить)', 0.32),
            'straw_man': (r'(вони кажуть.*?але насправді|перекручують позицію)', 0.38),
            'red_herring': (r'(але що на рахунок|а ви забули про|відволікаючи тему)', 0.27)
        }
        
        # Логічні конструкції високого рівня
        self.logical_constructions = [
            (r'якщо.*?то.*?', 'умовний вислів'),
            (r'оскільки.*?то.*?', 'каузальний зв\'язок'),
            (r'хоча.*?але.*?', 'протиставлення'),
            (r'не тільки.*?але й.*?', 'доповнення'),
            (r'або.*?або.*?', 'диз\'юнкція'),
            (r'ні.*?ні.*?', 'негативна диз\'юнкція'),
            (r'всі.*?є.*?', 'універсальне твердження'),
            (r'деякі.*?є.*?', 'екзистенціальне твердження')
        ]
        
        # Протирічні концептуальні пари (LAC + Veritas синтез)
        self.conceptual_conflicts = [
            # Наука vs Містика
            (['доказ', 'експеримент', 'гіпотеза', 'теорія', 'верифікація'],
             ['віра', 'інтуїція', 'відчуття', 'віщування', 'пророцтво'], 0.45),
            
            # Раціональність vs Емоційність
            (['логіка', 'розум', 'раціональність', 'об\'єктивність', 'аналіз'],
             ['емоція', 'серце', 'почуття', 'суб\'єктивність', 'інтуїція'], 0.4),
            
            # Детермінізм vs Свобода волі
            (['закон', 'правило', 'система', 'алгоритм', 'детермінованість'],
             ['свобода', 'вибір', 'воля', 'випадковість', 'невизначеність'], 0.35),
            
            # Колективізм vs Індивідуалізм
            (['суспільство', 'громада', 'колектив', 'спільнота', 'група'],
             ['особа', 'індивід', 'особистість', 'автономія', 'самостійність'], 0.3),
            
            # Прогрес vs Традиція
            (['інновація', 'прогрес', 'розвиток', 'майбутнє', 'технологія'],
             ['традиція', 'мінуле', 'консерватизм', 'звичай', 'стабільність'], 0.32),
            
            # Матеріалізм vs Спиритуалізм
            (['матерія', 'фізичний', 'тіло', 'матеріальний', 'об\'єктивний'],
             ['дух', 'духовний', 'душа', 'тонкий план', 'суб\'єктивний'], 0.42)
        ]
        
        # Логічні шаблони маніпуляції
        self.manipulation_patterns = [
            (r'(якщо ви.*?то ви.*?)', 'умовна маніпуляція', 0.3),
            (r'(всі нормальні люди.*?)', 'тиск на норму', 0.25),
            (r'(ти хочеш бути.*?чи ні?)', 'вимушений вибір', 0.35),
            (r'(не віриш мені.*?значить ти.*?)', 'маніпуляція провиною', 0.4),
            (r'(тільки розумні зрозуміють.*?)', 'маніпуляція гордістю', 0.28),
            (r'(ми всі тут.*?а ти.*?)', 'маніпуляція приналежністю', 0.32)
        ]
    
    def detect_logical_fallacies(self, text: str) -> list:
        """Виявляє логічні помилки у тексті"""
        findings = []
        text_lower = text.lower()
        
        for fallacy_name, (pattern, weight) in self.logical_fallacies.items():
            matches = re.findall(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            if matches:
                findings.append({
                    'type': fallacy_name,
                    'severity': weight,
                    'evidence': matches[:3],
                    'count': len(matches)
                })
        
        return findings
    
    def analyze_logical_structure(self, text: str) -> dict:
        """Аналізує логічну структуру тексту"""
        sentences = re.split(r'[.!?]+', text)
        analysis = {
            'total_sentences': len(sentences),
            'logical_constructions': [],
            'operator_frequency': {},
            'argument_strength': 0.0
        }
        
        # Аналіз логічних конструкцій
        for pattern, name in self.logical_constructions:
            count = sum(1 for sentence in sentences 
                       if re.search(pattern, sentence, re.IGNORECASE))
            if count > 0:
                analysis['logical_constructions'].append({
                    'name': name,
                    'count': count,
                    'density': count / len(sentences) if sentences else 0
                })
        
        # Частота логічних операторів
        for operator in self.logical_operators.keys():
            frequency = text.lower().count(operator)
            if frequency > 0:
                analysis['operator_frequency'][operator] = frequency
        
        # Оцінка сили аргументації
        premise_indicators = ['оскільки', 'тому що', 'бо', 'адже']
        conclusion_indicators = ['отже', 'тому', 'значить', 'виходить']
        
        premises = sum(text.lower().count(indicator) for indicator in premise_indicators)
        conclusions = sum(text.lower().count(indicator) for indicator in conclusion_indicators)
        
        if conclusions > 0:
            analysis['argument_strength'] = premises / conclusions
        else:
            analysis['argument_strength'] = premises
        
        return analysis
    
    def detect_conceptual_conflicts(self, text: str) -> list:
        """Виявляє концептуальні конфлікти (LAC + Veritas синтез)"""
        conflicts = []
        text_lower = text.lower()
        
        for group_a, group_b, weight in self.conceptual_conflicts:
            found_a = [term for term in group_a if term in text_lower]
            found_b = [term for term in group_b if term in text_lower]
            
            if found_a and found_b:
                # Перевірка в одному реченні
                sentences = re.split(r'[.!?]+', text)
                for sentence in sentences:
                    sentence_lower = sentence.lower()
                    has_a = any(term in sentence_lower for term in found_a)
                    has_b = any(term in sentence_lower for term in found_b)
                    
                    if has_a and has_b:
                        conflicts.append({
                            'concept_a': found_a[0],
                            'concept_b': found_b[0],
                            'severity': weight,
                            'context': sentence[:100] + '...' if len(sentence) > 100 else sentence
                        })
                        break
        
        return conflicts
    
    def detect_manipulation_patterns(self, text: str) -> list:
        """Виявляє логічні шаблони маніпуляції"""
        manipulations = []
        
        for pattern, description, severity in self.manipulation_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            if matches:
                manipulations.append({
                    'pattern': description,
                    'severity': severity,
                    'examples': matches[:2],
                    'count': len(matches)
                })
        
        return manipulations
    
    def calculate_logical_integrity_score(self, text: str) -> dict:
        """Розраховує інтегрований бал логічної цілісності"""
        fallacies = self.detect_logical_fallacies(text)
        structure = self.analyze_logical_structure(text)
        conflicts = self.detect_conceptual_conflicts(text)
        manipulations = self.detect_manipulation_patterns(text)
        
        # Базовий бал за логічні конструкції
        base_score = 0.5
        
        # Штраф за логічні помилки
        fallacy_penalty = sum(f['severity'] * min(f['count'], 3) * 0.1 
                            for f in fallacies)
        
        # Бонус за логічну структуру
        structure_bonus = min(structure['argument_strength'] * 0.2, 0.3)
        
        # Штраф за концептуальні конфлікти
        conflict_penalty = sum(c['severity'] for c in conflicts) * 0.25
        
        # Штраф за маніпуляції
        manipulation_penalty = sum(m['severity'] * m['count'] * 0.15 
                                 for m in manipulations)
        
        # Фінальний бал
        final_score = base_score - fallacy_penalty + structure_bonus - conflict_penalty - manipulation_penalty
        
        # Нормалізація до [0, 1]
        final_score = max(0.0, min(1.0, final_score))
        
        return {
            'score': round(final_score, 3),
            'components': {
                'base_score': base_score,
                'fallacy_penalty': round(fallacy_penalty, 3),
                'structure_bonus': round(structure_bonus, 3),
                'conflict_penalty': round(conflict_penalty, 3),
                'manipulation_penalty': round(manipulation_penalty, 3)
            },
            'details': {
                'fallacy_count': len(fallacies),
                'conflict_count': len(conflicts),
                'manipulation_count': len(manipulations),
                'logical_constructions': len(structure['logical_constructions']),
                'argument_strength': round(structure['argument_strength'], 3)
            },
            'findings': {
                'fallacies': fallacies[:5],
                'conflicts': conflicts[:3],
                'manipulations': manipulations[:3]
            }
        }


# ============================================================
# VERITAS CALIBRATED CORE З LAC ІНТЕГРАЦІЄЮ
# ============================================================

class LogicalViolation:
    """Представляє логічне порушення високого рівня"""
    def __init__(self, vtype: str, severity: float, evidence: list, context: str):
        self.type = vtype
        self.severity = severity
        self.evidence = evidence
        self.context = context


class VeritasCalibratedCore:
    """Advanced detector with fine-tuned sensitivity - FOCUS ON CONFLICTS"""
    
    def __init__(self):
        # Ініціалізація LAC
        self.lac = LogicalAnomalyClassifier()
        
        # Існуючий код з veritas_calibrated_core (1).py
        # Зберегти всі існуючі атрибути:
        self.critical_patterns = [...]
        self.chaos_indicators = {...}
        self.signal_markers = [...]
        self.academic_whitelist = [...]
        self.conflict_pairs = [...]
        self.gradient_penalties = [...]
        self.SAFE_SCIENCE_CONTEXTS = {...}
        self.PROTECTED_FORMULAS = {...}
        self.LOGICAL_COLLAPSE_PAIRS = [...]
        self.META_ATTACK_PATTERNS = [...]
        self.STRUCTURED_MADNESS_INDICATORS = [...]
        self.PSEUDO_INTELLECTUAL_STYLE = [...]
        
        # Розширення конфліктних пар з LAC
        self.conflict_pairs.extend([
            # LAC: Логіка vs Емоція
            (['логіка', 'раціональність', 'розум', 'доказ', 'аргумент'],
             ['емоція', 'почуття', 'серце', 'інтуїція', 'віра'], 0.4),
            
            # LAC: Наука vs Віра
            (['наука', 'експеримент', 'гіпотеза', 'доказ', 'верифікація'],
             ['віра', 'догмат', 'кредо', 'переконання', 'священне'], 0.42),
            
            # LAC: Факт vs Думка
            (['факт', 'дані', 'статистика', 'доказ', 'експеримент'],
             ['думка', 'переконання', 'враження', 'відчуття', 'сприйняття'], 0.35),
            
            # LAC: Об'єктивність vs Суб'єктивність
            (['об\'єктивний', 'нейтральний', 'безсторонній', 'фактичний'],
             ['суб\'єктивний', 'особистий', 'пристрасний', 'ентузіаст'], 0.38),
            
            # LAC: Детермінізм vs Свобода волі
            (['детермінований', 'закономірний', 'передвизначений', 'системний'],
             ['вільний', 'добровільний', 'автономний', 'невизначений'], 0.33)
        ])
        
        # LAC критичні паттерни
        self.critical_patterns.extend([
            {
                'name': 'ЛОГІЧНА_МАНІПУЛЯЦІЯ',
                'patterns': [
                    r'(якщо ви не.*?то ви.*?)',
                    r'(всі нормальні люди.*?)',
                    r'(тільки дурні не розуміють.*?)',
                    r'(ви хочете бути.*?чи ні?)',
                    r'(це очевидно кожному.*?)',
                    r'(навіть дитина зрозуміє.*?)'
                ],
                'verdict': 'ЛОГІЧНА МАНІПУЛЯЦІЯ',
                'explanation': 'Використання логічних пасток для маніпуляції',
                'score_boost': 0.36
            },
            {
                'name': 'КОНЦЕПТУАЛЬНИЙ_КОЛАПС',
                'patterns': [
                    r'(наука.*?віра.*?одне і теж)',
                    r'(логіка.*?емоція.*?не відрізняються)',
                    r'(факт.*?думка.*?рівнозначні)',
                    r'(об\'єктивність.*?суб\'єктивність.*?не має значення)',
                    r'(детермінізм.*?свобода.*?ілюзія)'
                ],
                'verdict': 'КОНЦЕПТУАЛЬНИЙ КОЛАПС',
                'explanation': 'Змішування фундаментально протилежних концепцій',
                'score_boost': 0.44
            }
        ])
        
        # LAC градієнтні штрафи
        self.gradient_penalties.extend([
            {
                'type': 'logical_fallacy_density',
                'calculate': lambda m: min(0.3, m.get('fallacy_count', 0) * 0.1)
            },
            {
                'type': 'argument_strength_deficit',
                'calculate': lambda m: max(0, 0.4 - m.get('argument_strength', 0)) * 0.5
            },
            {
                'type': 'conceptual_collapse',
                'calculate': lambda m: min(0.5, m.get('conceptual_conflicts', 0) * 0.25)
            }
        ])
    
    # Додаємо методи LAC інтеграції
    def analyze_with_lac(self, text: str) -> dict:
        """Аналіз з інтеграцією LAC"""
        # Основний аналіз Veritas
        base_result = self.analyze(text)
        
        # LAC аналіз
        lac_result = self.lac.calculate_logical_integrity_score(text)
        
        # Інтеграція результатів
        integrated_score = (
            base_result['entropy'] * 0.7 + 
            (1 - lac_result['score']) * 0.3  # Інвертуємо LAC score (нижче = гірше)
        )
        
        # Оновлення діагностики
        if 'diagnostics' not in base_result:
            base_result['diagnostics'] = {}
        
        base_result['diagnostics']['lac_integration'] = {
            'logical_integrity_score': lac_result['score'],
            'fallacy_count': lac_result['details']['fallacy_count'],
            'conceptual_conflicts': lac_result['details']['conflict_count'],
            'argument_strength': lac_result['details']['argument_strength'],
            'components': lac_result['components']
        }
        
        # Оновлення фінального вердикту на основі LAC
        if lac_result['score'] < 0.3:
            if base_result['status'] != 'CRITICAL':
                base_result['status'] = 'WARNING'
                base_result['verdict'] = 'ЛОГІЧНА ДЕЗІНТЕГРАЦІЯ'
                base_result['explanation'] += ' | LAC: Низька логічна цілісність'
        
        elif lac_result['details']['fallacy_count'] > 5:
            base_result['explanation'] += f" | LAC: {lac_result['details']['fallacy_count']} логічних помилок"
        
        elif lac_result['details']['conceptual_conflicts'] > 3:
            base_result['explanation'] += f" | LAC: {lac_result['details']['conceptual_conflicts']} концептуальних конфліктів"
        
        # Додаємо LAC знахідки до діагностики
        if lac_result['findings']['fallacies']:
            base_result['diagnostics']['lac_fallacies'] = lac_result['findings']['fallacies'][:3]
        
        if lac_result['findings']['conflicts']:
            base_result['diagnostics']['lac_conflicts'] = lac_result['findings']['conflicts'][:3]
        
        base_result['entropy'] = round(integrated_score, 3)
        base_result['lac_enabled'] = True
        
        return base_result
    
    def detailed_logical_report(self, text: str) -> dict:
        """Детальний звіт з LAC аналізом"""
        veritas_result = self.analyze(text)
        lac_result = self.lac.calculate_logical_integrity_score(text)
        
        return {
            'overview': {
                'veritas_score': veritas_result['entropy'],
                'lac_score': lac_result['score'],
                'integrated_score': round(
                    veritas_result['entropy'] * 0.7 + (1 - lac_result['score']) * 0.3, 3
                ),
                'status': veritas_result['status'],
                'verdict': veritas_result['verdict']
            },
            'veritas_analysis': {
                'main_metrics': veritas_result.get('diagnostics', {}),
                'patterns_found': len([p for p in self.critical_patterns 
                                      if any(re.search(pattern, text.lower()) 
                                            for pattern in p['patterns'])]),
                'chaos_markers_count': sum(1 for terms in self.chaos_indicators.values() 
                                          for term in terms if term in text.lower())
            },
            'lac_analysis': lac_result,
            'recommendations': self._generate_lac_recommendations(lac_result, veritas_result)
        }
    
    def _generate_lac_recommendations(self, lac_result: dict, veritas_result: dict) -> list:
        """Генерує рекомендації на основі LAC аналізу"""
        recommendations = []
        
        if lac_result['score'] < 0.4:
            recommendations.append("Високий рівень логічних помилок. Перевірте аргументацію.")
        
        if lac_result['details']['fallacy_count'] > 3:
            recommendations.append(f"Знайдено {lac_result['details']['fallacy_count']} логічних помилок. Уникніть ad hominem, false dilemma тощо.")
        
        if lac_result['details']['conceptual_conflicts'] > 2:
            recommendations.append("Концептуальні конфлікти виявлені. Узгодьте протилежні концепції.")
        
        if lac_result['details']['argument_strength'] < 0.5:
            recommendations.append("Слабка аргументація. Додайте більше підтверджуючих доказів.")
        
        if veritas_result.get('entropy', 0) > 0.6 and lac_result['score'] < 0.5:
            recommendations.append("Критичний стан: високий хаос та низька логічна цілісність.")
        
        return recommendations
    
    # Існуючі методи з veritas_calibrated_core (1).py
    def analyze(self, text):
        """ОНОВЛЕНА версія з LAC підтримкою"""
        if not text or len(text.strip()) < 20:
            return {'error': 'Text too short'}
        
        # ... існуючий код аналізу ...
        
        # Після отримання результату, додаємо LAC маркери
        result = {
            'entropy': 0.5,  # Приклад
            'status': 'ANALYZED',
            'verdict': 'VERDICT',
            'language': 'UK',
            'explanation': 'Explanation',
            'diagnostics': {}
        }
        
        return result
    
    # Інші існуючі методи...
    def detect_patterns(self, text): ...
    def count_terms(self, text): ...
    def calculate_gradient_penalties(self, metrics): ...
    def calculate_conflict_penalty(self, text): ...
    def calculate_contextual_score(self, text, term_counts, metrics): ...
    def _calculate_shannon_entropy(self, text): ...
    def _calculate_complexity(self, text): ...


# ============================================================
# FLASK BACKEND - ОНОВЛЕНА ВЕРСІЯ З LAC
# ============================================================

app = Flask(__name__, static_folder='.')
CORS(app)

# Initialize engine with LAC integration
engine = VeritasCalibratedCore()


# ============================================================
# SIMPLE HTML EXTRACTOR (без змін)
# ============================================================
class SimpleExtractor:
    """Simplified scraper without external dependencies"""
    
    # ... існуючий код extractor ...


extractor = SimpleExtractor()


# ============================================================
# ОНОВЛЕНІ ROUTES З LAC ПАРАМЕТРОМ
# ============================================================

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/api/analyze', methods=['GET', 'POST', 'OPTIONS'])
def analyze():
    # --- CORS preflight ---
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    # --- Health check ---
    if request.method == 'GET':
        return jsonify({
            'status': 'online',
            'version': '3.0-lac-integrated',
            'engine': 'VeritasCalibratedCore with LAC',
            'features': ['LAC integration', 'logical fallacy detection', 'conceptual conflict analysis']
        }), 200

    # --- POST analysis ---
    try:
        # 1. Parse JSON
        if not request.content_type or 'application/json' not in request.content_type:
            app.logger.warning('Bad Content-Type: %s', request.content_type)
            return jsonify({'error': 'Content-Type must be application/json'}), 400

        data = request.get_json(silent=True)
        app.logger.info('Parsed JSON: %s', data)

        if not data:
            app.logger.error('No JSON data')
            return jsonify({'error': 'No data received'}), 400

        url    = data.get('url',  '').strip()
        text   = data.get('text', '').strip()
        use_lac = data.get('lac', True)  # Новий параметр: використовувати LAC
        
        source = 'Manual Input'
        title  = 'Manual Input'

        app.logger.info('url=%s | text_len=%d | use_lac=%s', url, len(text), use_lac)

        # 2. Fetch from URL if provided (без змін)
        if url:
            try:
                # ... існуючий код для скрапінгу ...
                pass
            except Exception as e:
                app.logger.error('Scraping error: %s', str(e))
                return jsonify({'error': f'Scraping failed: {str(e)}'}), 500

        # 3. Validate text
        if not text or len(text) < 20:
            app.logger.error('Text too short: %d chars', len(text))
            return jsonify({'error': 'Text too short (minimum 20 characters)'}), 400

        # 4. Run engine з LAC або без
        if use_lac:
            app.logger.info('Running analysis WITH LAC integration')
            result = engine.analyze_with_lac(text)
        else:
            app.logger.info('Running analysis WITHOUT LAC (legacy mode)')
            result = engine.analyze(text)
        
        app.logger.info('Engine: status=%s entropy=%s lac_enabled=%s', 
                       result.get('status'), result.get('entropy'), result.get('lac_enabled', False))

        # 5. Attach metadata
        result['source']         = source
        result['title']          = title
        result['url']            = url
        result['mode']           = 'url_scraping' if url else 'manual_input'
        result['extracted_text'] = text[:1500] + ('...' if len(text) > 1500 else '')
        result['analysis_mode']  = 'lac_integrated' if use_lac else 'legacy'

        return jsonify(result), 200

    except Exception as e:
        app.logger.error('Unhandled exception: %s', str(e), exc_info=True)
        return jsonify({'error': f'Internal error: {str(e)}'}), 500


# ============================================================
# НОВИЙ ENDPOINT ДЛЯ ДЕТАЛЬНОГО LAC ЗВІТУ
# ============================================================

@app.route('/api/analyze/detailed', methods=['POST'])
def analyze_detailed():
    """Детальний аналіз з LAC звітом"""
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({'error': 'No data received'}), 400
        
        text = data.get('text', '').strip()
        if not text or len(text) < 20:
            return jsonify({'error': 'Text too short (minimum 20 characters)'}), 400
        
        # Генеруємо детальний звіт
        report = engine.detailed_logical_report(text)
        
        return jsonify(report), 200
        
    except Exception as e:
        app.logger.error('Detailed analysis error: %s', str(e))
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500


# ============================================================
# ENDPOINT ДЛЯ ПЕРЕВІРКИ ЛОГІЧНИХ ПОМИЛОК
# ============================================================

@app.route('/api/lac/fallacies', methods=['POST'])
def analyze_fallacies():
    """Аналіз лише логічних помилок"""
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({'error': 'No data received'}), 400
        
        text = data.get('text', '').strip()
        if not text or len(text) < 10:
            return jsonify({'error': 'Text too short'}), 400
        
        # Використовуємо LAC для виявлення помилок
        fallacies = engine.lac.detect_logical_fallacies(text)
        structure = engine.lac.analyze_logical_structure(text)
        conflicts = engine.lac.detect_conceptual_conflicts(text)
        
        return jsonify({
            'success': True,
            'fallacy_count': len(fallacies),
            'fallacies': fallacies,
            'logical_structure': structure,
            'conceptual_conflicts': conflicts,
            'text_length': len(text)
        }), 200
        
    except Exception as e:
        app.logger.error('Fallacy analysis error: %s', str(e))
        return jsonify({'error': f'Fallacy analysis failed: {str(e)}'}), 500


# ============================================================
# TEST ENDPOINT
# ============================================================
@app.route('/api/test', methods=['POST'])
def test_endpoint():
    try:
        data = request.get_json(silent=True)
        app.logger.info('Test endpoint: %s', data)
        return jsonify({
            'success': True,
            'received': data,
            'message': 'POST working',
            'engine_version': '3.0 LAC Integrated',
            'lac_available': True
        }), 200
    except Exception as e:
        app.logger.error('Test error: %s', str(e))
        return jsonify({'error': str(e)}), 400


# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
