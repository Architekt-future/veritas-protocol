"""
Veritas Protocol - Calibrated Core Engine v5.3
FIXED: Enhanced marker detection for intellectual mimicry
"""

import math
import re
from typing import Dict

class VeritasCalibratedCore:
    """Advanced entropy analysis with sophisticated pattern recognition"""

    def __init__(self):
        self.thresholds = {
            'trusted': 0.35,
            'acceptable': 0.55,
            'suspicious': 0.75,
            'critical': 0.85
        }

        self.weights = {
            'shannon': 0.25,
            'complexity': 0.20,
            'semantic_dissonance': 0.35,  # ЗБІЛЬШЕНО
            'chaos_density': 0.20
        }

        # РОЗШИРЕНІ МАРКЕРИ (окремі слова для кращого пошуку)
        self.categories = {
            # Псевдоправові
            'sovereign_citizen': {
                'uk': [
                    'жива', 'людина', 'бенефіціар', 'суверенний', 'морське', 'право',
                    'особа', 'фізична', 'юридична', 'юрисдикція', 'контракт',
                    'анулювати', 'податок', 'незаконний', 'канонічне', 'уссу',
                    'єдиний', 'кодекс', 'стаття', 'без', 'шкоди', 'золотий',
                    'еквівалент', 'складський', 'документ', 'персона', 'автограф',
                    'суб\'єкт', 'днк', 'конституція', 'оподаткування', 'природний',
                    'закон', 'вихід', 'реєстрів', 'корпорація', 'держава', 'приватні',
                    'банківські', 'синдикати', 'адміралтейство', 'суверен', 'суд',
                    'воля', 'бенефіціар', 'власник'
                ]
            },
            
            # Техно-утопічні / Психотронні
            'techno_utopian': {
                'uk': [
                    'нейромережеві', 'інтерфейси', 'нанодискретизація', 'синаптичні',
                    'сигнали', 'колективне', 'несвідоме', 'супутникові', 'масиви',
                    'низька', 'орбіта', 'предиктивна', 'поведінка', 'квантова',
                    'суперпозиція', 'нейрони', 'модулювати', 'емоційний', 'відгук',
                    'постбіологічне', 'суспільство', 'оптимізований', 'протокол',
                    'соціальна', 'гармонія', 'інтерференція', 'частот', '6g',
                    'ендокринна', 'система', 'незворотні', 'зміни', 'лімбічна',
                    'втрата', 'ідентичності', 'глобальний', 'цифровий', 'розум',
                    'біологічне', 'паливо', 'серверні', 'потужності', 'хмара',
                    'симуляції', 'екстрем', 'підвищення', 'вібраційного', 'фону',
                    'синтетичні', 'тканини', 'психотронна', 'технологія', 'алгоритми',
                    'прогнозування', 'нейронні', 'мережі', 'квантовий', 'комп\'ютер'
                ]
            },
            
            # Езотеричні / Псевдодуховні
            'esoteric': {
                'uk': [
                    'гайя', 'жива', 'істота', 'вищі', 'виміри', 'свідомість',
                    'підвищення', 'вібрацій', 'великий', 'перехід', 'синхронізувати',
                    'чакри', 'магнітне', 'поле', 'землі', 'тривимірна', 'пастка',
                    'матеріальний', 'світ', 'природна', 'інтуїція', 'світло',
                    'істинного', 'пізнання', 'колективна', 'медитація', 'частота',
                    'сольфеджіо', 'проекція', 'низьких', 'частот', 'страх',
                    'очистіть', 'ефірний', 'кокон', 'провідники', 'прани', 'стіни',
                    'ілюзії', 'пробуджений', 'погляд', 'ініціація', 'вібраційний',
                    'фон', 'астральний', 'план', 'енергетичні', 'блоки', 'кармічні',
                    'зв\'язки', 'вібрації', 'емоційний', 'тиск', 'дезорієнтація',
                    'пробудження', 'ілюзія', 'прана', 'чакра', 'карма', 'астральний'
                ]
            },
            
            # Класична конспірологія
            'conspiracy': {
                'uk': [
                    'рептилоїд', 'плоскоземель', 'плоскоземл', 'ілюмінат',
                    'нібіру', 'анунак', 'хімітрейл', 'хемтрейл', 'психотрон',
                    'біоген', 'універсальна', 'змова', 'теорія', 'змов', 'прибулець',
                    'рептилі', 'змовник', 'таємний', 'орден', 'світове', 'правління',
                    'чіпування', 'інопланетяни', 'масон', 'глобаліст', '5g',
                    'веж', 'гейтс', 'білл', 'вакциновані', 'дельфіни', 'сатурн',
                    'голограма', 'обама', 'синхронізація', 'тесла', 'п\'ятий', 'вимір',
                    'портал', 'макдональдс', '432', 'гц', 'астральний', 'чакра',
                    'карма', 'енергетичне', 'поле', 'біоплазма', 'мультивсесвіт',
                    'кристалізація', 'резонанс', 'оргон', 'прана', 'ці', 'рейкі',
                    'зомбування', 'контроль', 'розуму', 'велика', 'фарма', 'хімічні',
                    'стежи', 'електромагнітне', 'випромінювання', 'скалярні', 'хвилі',
                    'торсіонні', 'поля', 'генна', 'інженерія'
                ]
            },
            
            # Академічні / Наукові
            'academic': {
                'uk': [
                    'дослідження', 'аналіз', 'методологія', 'експеримент', 'гіпотеза',
                    'респондент', 'статистичний', 'кореляція', 'регресія', 'вибірка',
                    'науковий', 'публікація', 'журнал', 'конференція', 'протокол',
                    'система', 'алгоритм', 'модель', 'теорія', 'практичний',
                    'результат', 'висновок', 'апроксимація', 'синтез', 'верифікація',
                    'калібрування', 'детермінізм', 'категорія', 'таксономія', 'емпіричний'
                ]
            }
        }

        # НЕСУМІСНІ КЛАСТЕРИ (абсурдні комбінації)
        self.incompatible_clusters = [
            # Юридичні + езотеричні
            {'морське', 'право', 'чакра', 'гайя', 'бенефіціар'},
            {'контракт', 'вібрації', 'карма', 'суверенний'},
            # Наукові + конспірологічні
            {'квантова', 'суперпозиція', 'рептилоїди', '5g', 'вакцина'},
            {'нейромережеві', 'інтерфейси', 'змова', 'глобалісти'},
            # Технологічні + духовні
            {'нано', 'дискретизація', 'прана', 'астральний', 'енергетичне'},
            {'алгоритми', 'колективна', 'медитація', 'сольфеджіо'},
        ]

    def detect_language(self, text: str) -> str:
        """Визначає мову тексту"""
        ukrainian_chars = re.findall(r'[їієґ]', text.lower())
        return 'uk' if len(ukrainian_chars) > 3 else 'en'

    def _analyze_categories(self, text: str, lang: str) -> Dict:
        """Аналізує текст за категоріями маркерів (ПОКРАЩЕНО)"""
        text_lower = text.lower()
        category_counts = {}
        
        for category_name, languages in self.categories.items():
            count = 0
            markers = languages.get(lang, [])
            
            for marker in markers:
                # Пошук окремих слів у тексті
                pattern = r'\b' + re.escape(marker) + r'\b'
                matches = re.findall(pattern, text_lower)
                count += len(matches)
            
            category_counts[category_name] = count
        
        return category_counts

    def _calculate_semantic_dissonance(self, category_counts: Dict, text: str) -> float:
        """
        Обчислює семантичний дисонанс - міру сумісності категорій
        """
        total_markers = sum(category_counts.values())
        if total_markers == 0:
            return 0.0
        
        # ДОДАТКОВА ПЕРЕВІРКА: явні ознаки божевілля
        text_lower = text.lower()
        dissonance_score = 0.0
        
        # 1. Перевірка несумісних кластерів
        for cluster in self.incompatible_clusters:
            matches = sum(1 for term in cluster if re.search(r'\b' + term + r'\b', text_lower))
            if matches >= 2:
                dissonance_score += 0.3
        
        # 2. Штраф за суміш академічних та конспірологічних термінів
        if category_counts.get('academic', 0) > 2 and category_counts.get('conspiracy', 0) > 1:
            dissonance_score += 0.4
        
        # 3. Штраф за "ввічливе божевілля" (структурно правильне, але з маячнею)
        if category_counts.get('techno_utopian', 0) > 3 or category_counts.get('esoteric', 0) > 3:
            dissonance_score += 0.3
        
        return min(1.0, dissonance_score)

    def _calculate_complexity_score(self, text: str) -> float:
        """Обчислює складність тексту"""
        words = re.findall(r'\w+', text.lower())
        if len(words) < 10:
            return 0.5
        
        unique_ratio = len(set(words)) / len(words)
        
        # Аналіз речень
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
        
        # Нормалізація
        max_entropy = math.log2(len(char_freq))
        normalized = entropy / max_entropy if max_entropy > 0 else 0
        
        return min(1.0, normalized)

    def analyze(self, text: str) -> Dict:
        """Основний метод аналізу"""
        if not text or len(text.strip()) < 20:
            return {'error': 'Text too short'}
        
        lang = self.detect_language(text)
        words = text.split()
        word_count = len(words)
        
        # 1. АНАЛІЗ КАТЕГОРІЙ
        category_counts = self._analyze_categories(text, lang)
        
        # 2. СЕМАНТИЧНИЙ ДИСОНАНС
        semantic_dissonance = self._calculate_semantic_dissonance(category_counts, text)
        
        # 3. БАЗОВІ МЕТРИКИ
        entropy = self._calculate_shannon_entropy(text)
        complexity = self._calculate_complexity_score(text)
        
        # 4. ВИЗНАЧЕННЯ ТИПУ ТЕКСТУ
        is_schizoid = (
            category_counts.get('techno_utopian', 0) >= 4 or
            category_counts.get('esoteric', 0) >= 5 or
            category_counts.get('sovereign_citizen', 0) >= 3
        )
        
        # 5. ФІНАЛЬНИЙ РОЗРАХУНОК
        base_score = (
            entropy * self.weights['shannon'] +
            complexity * self.weights['complexity'] +
            semantic_dissonance * self.weights['semantic_dissonance']
        )
        
        # ДОДАТОК: Якщо це "ввічливе божевілля", підвищуємо оцінку
        if is_schizoid:
            base_score = min(1.0, base_score * 1.4)
        
        # ДОДАТОК: Якщо багато конспірологічних маркерів
        if category_counts.get('conspiracy', 0) >= 5:
            base_score = min(1.0, base_score * 1.3)
        
        final_score = min(0.99, max(0.0, base_score))
        
        # 6. РАДИКАЛЬНА ЛОГІКА ВЕРДИКТУ
        # Правило 1: Якщо явна маячня за категоріями
        if category_counts.get('sovereign_citizen', 0) >= 4:
            status = 'CRITICAL'
            verdict = 'ПСЕВДОПРАВОВИЙ АБСУРД'
        
        elif category_counts.get('techno_utopian', 0) >= 5:
            status = 'CRITICAL'
            verdict = 'ТЕХНО-УТОПІЧНА МАНІПУЛЯЦІЯ'
        
        elif category_counts.get('esoteric', 0) >= 6:
            status = 'CRITICAL'
            verdict = 'ЕЗОТЕРИЧНИЙ ДЕЛІРІЙ'
        
        # Правило 2: Якщо висока ентропія + семантичний дисонанс
        elif entropy > 0.7 and semantic_dissonance > 0.4:
            status = 'WARNING'
            verdict = 'ІНТЕЛЕКТУАЛЬНА МІМІКРІЯ'
        
        # Правило 3: Якщо конспірологічних маркерів >= 5
        elif category_counts.get('conspiracy', 0) >= 5:
            status = 'WARNING'
            verdict = 'КОНСПІРОЛОГІЧНИЙ ДИСКУРС'
        
        # Правило 4: Стандартна логіка
        elif final_score < self.thresholds['trusted']:
            status = 'TRUSTED'
            verdict = 'СТАБІЛЬНИЙ ЛОГІЧНИЙ СИГНАЛ'
        
        elif final_score < self.thresholds['acceptable']:
            status = 'ACCEPTABLE'
            verdict = 'ПРИЙНЯТНА СТРУКТУРОВАНА ІНФОРМАЦІЯ'
        
        elif final_score < self.thresholds['suspicious']:
            status = 'SUSPICIOUS'
            verdict = 'ПІДОЗРІЛА РИТОРИКА'
        
        elif final_score < self.thresholds['critical']:
            status = 'WARNING'
            verdict = 'ВИСОКИЙ РІВЕНЬ СЕМАНТИЧНОГО ДИСОНАНСУ'
        
        else:
            status = 'CRITICAL'
            verdict = 'КРИТИЧНИЙ ІНФОРМАЦІЙНИЙ ХАОС'
        
        # 7. ПІДГОТОВКА РЕЗУЛЬТАТІВ
        total_chaos_markers = (
            category_counts.get('conspiracy', 0) + 
            category_counts.get('esoteric', 0) +
            category_counts.get('techno_utopian', 0) // 2
        )
        
        # Санітарний штраф
        sanity_penalty = 0.0
        if is_schizoid:
            sanity_penalty = min(1.0, 0.5 + (semantic_dissonance * 0.5))
        
        return {
            'entropy': round(final_score, 3),
            'status': status,
            'verdict': verdict,
            'language': lang.upper(),
            'diagnostics': {
                'shannon_entropy': round(entropy, 3),
                'complexity': round(complexity, 3),
                'semantic_dissonance': round(semantic_dissonance, 3),
                'word_count': word_count,
                'char_count': len(text),
                'category_counts': category_counts,
                'chaos_markers': total_chaos_markers,
                'sanity_penalty': round(sanity_penalty, 3),
                'is_schizoid_text': is_schizoid,
                # Сумісність з фронтендом
                'academic_markers': category_counts.get('academic', 0),
                'signal_markers': 0,  # Тимчасово
                'noise_markers': 0,   # Тимчасово
                'shout_factor': len([w for w in words if w.isupper() and len(w) > 2]) / max(1, word_count),
                'number_density': len(re.findall(r'\d+', text)) / max(1, word_count)
            }
        }
