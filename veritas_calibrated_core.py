"""
Veritas Protocol - Calibrated Core Engine v5.4
Enhanced detection of cross-domain absurdity and intellectual mimicry
"""

import math
import re
from typing import Dict, List, Tuple

class VeritasCalibratedCore:
    """Advanced entropy analysis with cross-domain absurdity detection"""

    def __init__(self):
        self.thresholds = {
            'trusted': 0.35,
            'acceptable': 0.55,
            'suspicious': 0.75,
            'critical': 0.85
        }

        self.weights = {
            'shannon': 0.20,
            'complexity': 0.15,
            'semantic_dissonance': 0.40,  # ЗБІЛЬШЕНО
            'cross_domain_absurdity': 0.25  # НОВА МЕТРИКА
        }

        # РОЗШИРЕНІ КАТЕГОРІЇ ДОМЕНІВ
        self.domain_categories = {
            # Академічні / наукові
            'academic': {
                'uk': [
                    'статистичний', 'аналіз', 'кореляція', 'регресія', 'емпіричний',
                    'методологія', 'гіпотеза', 'експеримент', 'результат', 'висновок',
                    'дослідження', 'публікація', 'журнал', 'конференція', 'протокол',
                    'верифікація', 'валідація', 'рецензія', 'цитування', 'індекс'
                ]
            },
            
            # Фінансові / економічні
            'financial': {
                'uk': [
                    'фондовий', 'ринок', 'індекс', 'акція', 'облігація', 'інвестиція',
                    'капітал', 'бюджет', 'податок', 'дефіцит', 'профіцит', 'інфляція',
                    'відсоток', 'кредит', 'депозит', 'крипто', 'блокчейн', 'токен',
                    'біржа', 'трейдинг', 'трейдер', 'портфель', 'актив', 'пасив'
                ]
            },
            
            # Юридичні / правові
            'legal': {
                'uk': [
                    'закон', 'кодекс', 'стаття', 'параграф', 'юрисдикція', 'суд',
                    'прокуратура', 'адвокат', 'позов', 'вирок', 'рішення', 'постанова',
                    'указ', 'розпорядження', 'регламент', 'конституція', 'право',
                    'обов\'язок', 'відповідальність', 'зобов\'язання', 'договір'
                ]
            },
            
            # Технологічні / IT
            'tech': {
                'uk': [
                    'алгоритм', 'програмне', 'апаратне', 'інтерфейс', 'протокол',
                    'шифрування', 'дешифрування', 'база', 'даних', 'сервер', 'хмара',
                    'блокчейн', 'смартконтракт', 'крипто', 'нейромережа', 'штучний',
                    'інтелект', 'машинне', 'навчання', 'біг', 'дата', 'аналітика'
                ]
            },
            
            # Політичні / державні
            'political': {
                'uk': [
                    'уряд', 'парламент', 'міністерство', 'відомство', 'департамент',
                    'адміністрація', 'бюрократія', 'законодавство', 'виконавча', 'влада',
                    'законодавча', 'судова', 'держава', 'країна', 'нація', 'громадянство',
                    'вибори', 'кандидат', 'програма', 'стратегія', 'політика'
                ]
            },
            
            # Езотеричні / псевдонаукові
            'esoteric': {
                'uk': [
                    'чакра', 'карма', 'астральний', 'енергетичний', 'вібрація',
                    'резонанс', 'прана', 'ці', 'рейкі', 'медитація', 'транс',
                    'пробудження', 'ініціація', 'архетип', 'колективне', 'несвідоме',
                    'синхронічність', 'нумерологія', 'астрологія', 'хіромантія',
                    'біолокація', 'ясновидіння', 'телепатія', 'екстрасенс'
                ]
            },
            
            # Конспірологічні
            'conspiracy': {
                'uk': [
                    'змова', 'таємний', 'орден', 'ілюмінат', 'рептилоїд', 'плоскоземель',
                    'нібіру', 'анунак', 'хімітрейл', '5g', 'чіп', 'вакцина', 'білл',
                    'гейтс', 'глобаліст', 'світовий', 'уряд', 'контроль', 'розуму',
                    'зомбування', 'психотронна', 'зброя', 'приховують', 'приховування'
                ]
            },
            
            # Корпоративний жаргон
            'corporate': {
                'uk': [
                    'синергія', 'стратегія', 'оптимізація', 'ефективність', 'показник',
                    'kpi', 'окр', 'результат', 'продуктивність', 'ланцюг', 'постачання',
                    'стейкхолдер', 'бренд', 'позиціонування', 'ринкова', 'частка',
                    'монетизація', 'масштабування', 'диверсифікація', 'інновація'
                ]
            },
            
            # Науково-фантастичні / утопічні
            'scifi_utopian': {
                'uk': [
                    'нейтрино', 'квантовий', 'суперпозиція', 'ентанґлемент', 'телепортація',
                    'мультивсесвіт', 'паралельний', 'вимір', 'портал', 'симуляція',
                    'голограма', 'кіборг', 'трансгуманізм', 'постлюдина', 'штучний',
                    'розум', 'сингулярність', 'нанотехнологія', 'біотехнологія'
                ]
            }
        }

        # ЗАБОРОНЕНІ ПАРИ ДОМЕНІВ (абсурдні поєднання)
        self.forbidden_domain_pairs = [
            # Фінанси + Езотерика
            ('financial', 'esoteric'),
            ('financial', 'conspiracy'),
            # Юриспруденція + Езотерика
            ('legal', 'esoteric'),
            ('legal', 'conspiracy'),
            # Наука + Конспірологія
            ('academic', 'conspiracy'),
            ('academic', 'esoteric'),
            # Політика + Езотерика
            ('political', 'esoteric'),
            ('political', 'conspiracy'),
            # Технології + Езотерика
            ('tech', 'esoteric'),
            ('tech', 'conspiracy'),
            # Корпоративне + Езотерика
            ('corporate', 'esoteric'),
            ('corporate', 'conspiracy'),
            # Наукова фантастика + Фінанси
            ('scifi_utopian', 'financial'),
            ('scifi_utopian', 'legal'),
            ('scifi_utopian', 'political')
        ]

        # АБСУРДНІ КЛАСТЕРИ СЛІВ (явні ознаки маячні)
        self.absurdity_clusters = [
            # Блокчейн + духовність
            {'блокчейн', 'кадило', 'обряд', 'прана', 'астральний'},
            # ДНК + 5G + контроль
            {'днк', '5g', 'частота', 'чип', 'контроль'},
            # Квантова фізика + фінанси
            {'квантовий', 'фондовий', 'ринок', 'нейтрино', 'трейдер'},
            # Алхімія + цифрові технології
            {'алхімічний', 'криптографічний', 'трансмутація', 'цифровий', 'золото'},
            # Гомеопатія + електрика
            {'гомеопатичний', 'електрика', 'доза', 'патріотичний', 'резонанс'},
            # Податки + карма
            {'податок', 'кармічний', 'борг', 'астральний', 'еквівалент'},
            # Державні установи + магія
            {'міністерство', 'енергетики', 'гомеопатичний', 'електрика', 'патріотичний'},
            # Бюрократія + езотерика
            {'бюрократія', 'чакра', 'вібрація', 'резонанс', 'енергетичний'},
            # Наукові методи + містицизм
            {'статистичний', 'алхімічний', 'трансмутація', 'ефірний', 'благополуччя'}
        ]

        # СИГНАЛЬНІ МАРКЕРИ (нормальний контент)
        self.signal_markers = {
            'uk': [
                'факт', 'дані', 'показник', 'вимір', 'кількість', 'дослідження',
                'статистичний', 'кореляція', 'регресія', 'аналіз', 'метод',
                'експеримент', 'гіпотеза', 'вибірка', 'результат', 'протокол',
                'система', 'модель', 'теорія', 'практичний', 'висновок',
                'звіт', 'документ', 'закон', 'правило', 'процедура', 'стандарт'
            ]
        }

    def detect_language(self, text: str) -> str:
        """Визначає мову тексту"""
        ukrainian_chars = re.findall(r'[їієґ]', text.lower())
        return 'uk' if len(ukrainian_chars) > 3 else 'en'

    def _analyze_domains(self, text: str, lang: str) -> Dict:
        """Аналізує присутність різних доменів у тексті"""
        text_lower = text.lower()
        domain_counts = {}
        
        for domain_name, languages in self.domain_categories.items():
            count = 0
            markers = languages.get(lang, [])
            
            for marker in markers:
                pattern = r'\b' + re.escape(marker) + r'\b'
                matches = re.findall(pattern, text_lower)
                count += len(matches)
            
            domain_counts[domain_name] = count
        
        return domain_counts

    def _calculate_cross_domain_absurdity(self, domain_counts: Dict, text: str) -> float:
        """
        Обчислює абсурдність перехресних доменів
        """
        text_lower = text.lower()
        absurdity_score = 0.0
        
        # 1. Перевірка заборонених пар доменів
        for domain1, domain2 in self.forbidden_domain_pairs:
            if domain_counts.get(domain1, 0) > 0 and domain_counts.get(domain2, 0) > 0:
                # Чим більше маркерів в обох доменах, тим вищий штраф
                ratio = min(domain_counts[domain1], domain_counts[domain2]) / 5
                absurdity_score += min(0.5, ratio)
        
        # 2. Перевірка абсурдних кластерів
        for cluster in self.absurdity_clusters:
            matches = sum(1 for term in cluster if re.search(r'\b' + term + r'\b', text_lower))
            if matches >= 2:
                absurdity_score += 0.3
            if matches >= 3:
                absurdity_score += 0.4
        
        # 3. Штраф за "псевдоінтелектуальну маячню"
        # Якщо є академічні терміни, але також езотеричні/конспірологічні
        if (domain_counts.get('academic', 0) > 3 and 
            (domain_counts.get('esoteric', 0) > 1 or domain_counts.get('conspiracy', 0) > 1)):
            absurdity_score += 0.5
        
        # 4. Штраф за "корпоративний окультизм"
        if domain_counts.get('corporate', 0) > 3 and domain_counts.get('esoteric', 0) > 1:
            absurdity_score += 0.4
        
        return min(1.0, absurdity_score)

    def _calculate_semantic_dissonance(self, domain_counts: Dict, text: str) -> float:
        """Обчислює семантичний дисонанс"""
        text_lower = text.lower()
        dissonance_score = 0.0
        
        # Рахуємо загальну кількість доменів
        active_domains = [domain for domain, count in domain_counts.items() if count > 0]
        
        if len(active_domains) <= 1:
            return 0.0
        
        # Штраф за надмірну різноманітність доменів (особливо несумісних)
        if len(active_domains) >= 4:
            dissonance_score += 0.3
        
        # Додатковий штраф, якщо серед доменів є "небезпечні"
        dangerous_domains = {'esoteric', 'conspiracy', 'scifi_utopian'}
        dangerous_count = sum(1 for domain in active_domains if domain in dangerous_domains)
        
        if dangerous_count >= 2:
            dissonance_score += 0.4
        
        return min(1.0, dissonance_score)

    def _calculate_complexity_score(self, text: str) -> float:
        """Обчислює складність тексту"""
        words = re.findall(r'\w+', text.lower())
        if len(words) < 10:
            return 0.5
        
        unique_ratio = len(set(words)) / len(words)
        
        sentences = re.split(r'[.!?]+', text)
        if sentences:
            avg_sentence_length = sum(len(s.split()) for s in sentences if s.strip()) / len(sentences)
        else:
            avg_sentence_length = 10
        
        complexity = (unique_ratio * 0.6) + (min(1.0, avg_sentence_length / 25) * 0.4)
        return min(1.0, complexity)

    def _calculate_shannon_entropy(self, text: str) -> float:
        """Обчислює ентропію Шеннона"""
        if not text:
            return 0.0
        
        clean_text = re.sub(r'\s+', ' ', text)
        char_freq = {}
        
        for char in clean_text:
            if char.isalpha() or char.isdigit():
                char_freq[char] = char_freq.get(char, 0) + 1
        
        if not char_freq:
            return 0.0
        
        entropy = 0.0
        text_len = len(clean_text)
        
        for count in char_freq.values():
            p = count / text_len
            if p > 0:
                entropy -= p * math.log2(p)
        
        max_entropy = math.log2(len(char_freq))
        normalized = entropy / max_entropy if max_entropy > 0 else 0
        
        return min(1.0, normalized)

    def _count_signal_markers(self, text: str, lang: str) -> int:
        """Підраховує сигнальні маркери"""
        text_lower = text.lower()
        count = 0
        
        for marker in self.signal_markers.get(lang, []):
            pattern = r'\b' + re.escape(marker) + r'\b'
            matches = re.findall(pattern, text_lower)
            count += len(matches)
        
        return count

    def _detect_absurd_pairs_in_sentences(self, text: str) -> float:
        """Знаходить абсурдні пари слів в межах одних речень"""
        sentences = re.split(r'[.!?]+', text)
        absurd_sentences = 0
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            
            # Перевірка кожної забороненої пари доменів в реченні
            for domain1, domain2 in self.forbidden_domain_pairs:
                domain1_terms = self.domain_categories.get(domain1, {}).get('uk', [])
                domain2_terms = self.domain_categories.get(domain2, {}).get('uk', [])
                
                has_domain1 = any(re.search(r'\b' + term + r'\b', sentence_lower) for term in domain1_terms if term)
                has_domain2 = any(re.search(r'\b' + term + r'\b', sentence_lower) for term in domain2_terms if term)
                
                if has_domain1 and has_domain2:
                    absurd_sentences += 1
                    break
        
        if len(sentences) > 0:
            return absurd_sentences / len(sentences)
        return 0.0

    def analyze(self, text: str) -> Dict:
        """Основний метод аналізу"""
        if not text or len(text.strip()) < 20:
            return {'error': 'Text too short'}
        
        lang = self.detect_language(text)
        words = text.split()
        word_count = len(words)
        
        # 1. АНАЛІЗ ДОМЕНІВ
        domain_counts = self._analyze_domains(text, lang)
        
        # 2. КРОС-ДОМЕННА АБСУРДНІСТЬ
        cross_domain_absurdity = self._calculate_cross_domain_absurdity(domain_counts, text)
        
        # 3. СЕМАНТИЧНИЙ ДИСОНАНС
        semantic_dissonance = self._calculate_semantic_dissonance(domain_counts, text)
        
        # 4. АБСУРДНІ ПАРИ В РЕЧЕННЯХ
        sentence_absurdity = self._detect_absurd_pairs_in_sentences(text)
        
        # 5. БАЗОВІ МЕТРИКИ
        entropy = self._calculate_shannon_entropy(text)
        complexity = self._calculate_complexity_score(text)
        
        # 6. ФІНАЛЬНИЙ РОЗРАХУНОК
        base_score = (
            entropy * self.weights['shannon'] +
            complexity * self.weights['complexity'] +
            semantic_dissonance * self.weights['semantic_dissonance'] +
            cross_domain_absurdity * self.weights['cross_domain_absurdity']
        )
        
        # 7. ДОДАТКОВІ ШТРАФИ
        # За абсурдні пари в реченнях
        if sentence_absurdity > 0.3:
            base_score = min(1.0, base_score * (1.0 + sentence_absurdity))
        
        # За "псевдоінтелектуальну маячню"
        if (domain_counts.get('academic', 0) > 3 and 
            (domain_counts.get('esoteric', 0) > 1 or domain_counts.get('conspiracy', 0) > 1)):
            base_score = min(1.0, base_score * 1.3)
        
        final_score = min(0.99, max(0.0, base_score))
        
        # 8. РАДИКАЛЬНА ЛОГІКА ВЕРДИКТУ
        # Правило 1: Висока кросс-доменна абсурдність
        if cross_domain_absurdity > 0.6:
            status = 'CRITICAL'
            if domain_counts.get('financial', 0) > 0 and domain_counts.get('esoteric', 0) > 0:
                verdict = 'ФІНАНСОВО-ЕЗОТЕРИЧНИЙ АБСУРД'
            elif domain_counts.get('legal', 0) > 0 and domain_counts.get('esoteric', 0) > 0:
                verdict = 'ЮРИДИЧНО-МІСТИЧНА МАЯЧНЯ'
            elif domain_counts.get('academic', 0) > 0 and domain_counts.get('conspiracy', 0) > 0:
                verdict = 'ПСЕВДОНАУКОВА ДЕЗІНФОРМАЦІЯ'
            else:
                verdict = 'КРОС-ДОМЕННИЙ СЕМАНТИЧНИЙ КОЛАПС'
        
        # Правило 2: Корпоративний окультизм
        elif domain_counts.get('corporate', 0) > 3 and domain_counts.get('esoteric', 0) > 1:
            status = 'CRITICAL'
            verdict = 'КОРПОРАТИВНИЙ ОКУЛЬТИЗМ'
        
        # Правило 3: Науковий нігілізм
        elif (domain_counts.get('academic', 0) > 3 and 
              domain_counts.get('scifi_utopian', 0) > 2 and
              (domain_counts.get('financial', 0) > 0 or domain_counts.get('political', 0) > 0)):
            status = 'CRITICAL'
            verdict = 'НАУКОВИЙ НІГІЛІЗМ'
        
        # Правило 4: Дзеркальна дезінформація
        elif (domain_counts.get('conspiracy', 0) >= 3 and 
              'брехн' in text.lower() and 
              'маніпуляці' in text.lower()):
            status = 'WARNING'
            verdict = 'ДЗЕРКАЛЬНА ДЕЗІНФОРМАЦІЯ'
        
        # Стандартна логіка
        else:
            if final_score < self.thresholds['trusted']:
                status = 'TRUSTED'
                verdict = 'СТАБІЛЬНИЙ ЛОГІЧНИЙ СИГНАЛ'
            elif final_score < self.thresholds['acceptable']:
                status = 'ACCEPTABLE'
                verdict = 'ПРИЙНЯТНА СТРУКТУРОВАНА ІНФОРМАЦІЯ'
            elif final_score < self.thresholds['suspicious']:
                status = 'SUSPICIOUS'
                verdict = 'ПІДОЗРІЛА ІНТЕЛЕКТУАЛЬНА МІМІКРІЯ'
            elif final_score < self.thresholds['critical']:
                status = 'WARNING'
                verdict = 'ВИСОКИЙ РІВЕНЬ КРОС-ДОМЕННОЇ АБСУРДНОСТІ'
            else:
                status = 'CRITICAL'
                verdict = 'КРИТИЧНИЙ СЕМАНТИЧНИЙ КОЛАПС'
        
        # 9. РОЗРАХУНОК ШТРАФІВ
        sanity_penalty = max(cross_domain_absurdity, semantic_dissonance, sentence_absurdity)
        
        # Маркери хаосу (езотерика + конспірологія + наукова фантастика)
        chaos_markers = (
            domain_counts.get('esoteric', 0) + 
            domain_counts.get('conspiracy', 0) + 
            domain_counts.get('scifi_utopian', 0)
        )
        
        # 10. ПІДГОТОВКА РЕЗУЛЬТАТІВ
        return {
            'entropy': round(final_score, 3),
            'status': status,
            'verdict': verdict,
            'language': lang.upper(),
            'diagnostics': {
                'shannon_entropy': round(entropy, 3),
                'complexity': round(complexity, 3),
                'semantic_dissonance': round(semantic_dissonance, 3),
                'cross_domain_absurdity': round(cross_domain_absurdity, 3),
                'sentence_absurdity': round(sentence_absurdity, 3),
                'word_count': word_count,
                'char_count': len(text),
                'domain_counts': domain_counts,
                'chaos_markers': chaos_markers,
                'sanity_penalty': round(sanity_penalty, 3),
                # Сумісність з фронтендом
                'academic_markers': domain_counts.get('academic', 0),
                'signal_markers': self._count_signal_markers(text, lang),
                'noise_markers': 0,
                'shout_factor': len([w for w in words if w.isupper() and len(w) > 2]) / max(1, word_count),
                'number_density': len(re.findall(r'\d+', text)) / max(1, word_count)
            }
        }
