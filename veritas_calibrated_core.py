"""
Veritas Protocol - Calibrated Core Engine v5.2
Enhanced detection of "polite insanity" and intellectual mimicry
"""

import math
import re
from typing import Dict, List

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
            'shannon': 0.20,
            'complexity': 0.15,
            'semantic_dissonance': 0.30,  # НОВА МЕТРИКА
            'chaos_density': 0.20,
            'sanity_violation': 0.15
        }

        # РОЗШИРЕНІ МАРКЕРИ ЗА КАТЕГОРІЯМИ
        self.categories = {
            # Псевдоправові / Суверен-гражданин
            'sovereign_citizen': {
                'uk': {
                    'жива людина', 'бенефіціар', 'суверенний', 'морське право',
                    'особа фізична', 'особа юридична', 'юрисдикція', 'контракт',
                    'апулювати', 'податок незаконний', 'канонічне право',
                    'уссу', 'єдиний комерційний кодекс', 'стаття 1-308',
                    'без шкоди', 'золотий еквівалент', 'складський документ',
                    'персона', 'автограф', 'суб\'єкт', 'днк конституція',
                    'об\'єкт оподаткування', 'природний закон', 'вихід з реєстрів',
                    'бенефіціар власник', 'корпорація держава', 'приватні банківські синдикати'
                }
            },
            
            # Техно-утопічні / Психотронні
            'techno_utopian': {
                'uk': {
                    'нейромережеві інтерфейси', 'нано-дискретизація', 'синаптичні сигнали',
                    'колективне несвідоме', 'супутникові масиви', 'низька орбіта',
                    'предиктивна поведінка', 'квантова суперпозиція', 'нейрони',
                    'модулювати емоційний відгук', 'пост-біологічне суспільство',
                    'оптимізований протокол', 'соціальна гармонія', 'інтерференція частот',
                    '6g-діапазон', 'ендокринна система', 'незворотні зміни',
                    'лімбічна система', 'втрата ідентичності', 'глобальний цифровий розум',
                    'біологічне паливо', 'серверні потужності', 'хмара симуляції',
                    'екстрем', 'підвищення вібраційного фону', 'синтетичні тканини'
                }
            },
            
            # Езотеричні / Псевдодуховні
            'esoteric': {
                'uk': {
                    'гайя', 'жива істота', 'вищі виміри', 'свідомість',
                    'підвищення вібрацій', 'великий перехід', 'синхронізувати чакри',
                    'магнітне поле землі', 'тривимірна пастка', 'матеріальний світ',
                    'природна інтуїція', 'світло істинного пізнання', 'колективна медитація',
                    'частота сольфеджіо', 'проекція низьких частот', 'страх',
                    'очистіть ефірний кокон', 'провідники прани', 'стіни ілюзії',
                    'пробуджений погляд', 'ініціація', 'вібраційний фон',
                    'астральний план', 'енергетичні блоки', 'кармічні зв'язки'
                }
            },
            
            # Класична конспірологія
            'conspiracy': {
                'uk': {
                    'рептилоїд', 'плоскоземель', 'плоскоземл', 'ілюмінат',
                    'нібіру', 'анунак', 'хімітрейл', 'хемтрейл', 'психотрон',
                    'біоген', 'універсальна змова', 'теорія змов', 'прибулець',
                    'рептилі', 'змовник', 'таємний орден', 'світове правління',
                    'чіпування', 'інопланетяни', 'масон', 'глобаліст',
                    '5g', '5g-веж', 'гейтс', 'білл гейтс', 'вакциновані',
                    'дельфіни', 'сатурн', 'голограма', 'обама', 'синхронізація',
                    'тесла', 'п\'ятий вимір', 'портал', 'макдональдс', '432 гц',
                    'астральний', 'чакра', 'карма', 'енергетичне поле',
                    'біоплазма', 'мультивсесвіт', 'кристалізація', 'резонанс',
                    'оргон', 'прана', 'ці', 'рейкі', 'зомбування', 'контроль розуму',
                    'велика фарма', 'хімічні стежи', 'електромагнітне випромінювання',
                    'скалярні хвилі', 'торсіонні поля', 'генна інженерія'
                }
            },
            
            # Академічні / Наукові (нормальні)
            'academic': {
                'uk': {
                    'дослідження', 'аналіз', 'методологія', 'експеримент', 'гіпотеза',
                    'респондент', 'статистичний', 'кореляція', 'регресія', 'вибірка',
                    'науковий', 'публікація', 'журнал', 'конференція', 'протокол',
                    'система', 'алгоритм', 'модель', 'теорія', 'практичний',
                    'результат', 'висновок', 'апроксимація', 'синтез', 'верифікація',
                    'калібрування', 'детермінізм', 'категорія', 'таксономія', 'емпіричний'
                }
            }
        }

        # СИГНАЛЬНІ МАРКЕРИ (нормальний контент)
        self.signal_markers = {
            'uk': {
                'факт', 'дані', 'показник', 'вимір', 'кількість', 'дослідження',
                'статистичний', 'кореляція', 'регресія', 'аналіз', 'метод',
                'експеримент', 'гіпотеза', 'вибірка', 'результат', 'протокол',
                'система', 'модель', 'теорія', 'практичний', 'висновок',
                'звіт', 'документ', 'закон', 'правило', 'процедура', 'стандарт',
                'об\'єктивний', 'нейтральний', 'перевірений', 'підтверджений',
                'науковий метод', 'певдість', 'точно', 'визначення'
            }
        }

        # ШУМОВІ МАРКЕРИ (емоційні, маніпулятивні)
        self.noise_markers = {
            'uk': {
                'шокуючий', 'паніка', 'сенсація', 'терміново', 'катастрофічний',
                'апокаліпсис', 'крах', 'знищення', 'жахливий', 'небезпека',
                'злочин', 'зрада', 'кривавий', 'несправедливість', 'заговор',
                'зомбування', 'контроль', 'тиск', 'маніпуляція', 'обман',
                'приховування', 'таємниця', 'розкриття', 'правда', 'зомбі'
            }
        }

        # НЕСУМІСНІ КЛАСТЕРИ (абсурдні комбінації)
        self.incompatible_clusters = [
            # Юридичні + езотеричні
            {'морське право', 'чакра', 'гайя', 'бенефіціар'},
            {'контракт', 'вібрації', 'карма', 'суверенний'},
            # Наукові + конспірологічні
            {'квантова суперпозиція', 'рептилоїди', '5g', 'вакцина'},
            {'нейромережеві інтерфейси', 'змова', 'глобалісти', 'контроль розуму'},
            # Технологічні + духовні
            {'нано-дискретизація', 'прана', 'астральний', 'енергетичне поле'},
            {'алгоритми', 'колективна медитація', 'частота сольфеджіо'},
            # Абсурдні юридічні конструкції
            {'жива людина', 'золотий еквівалент', 'складський документ'},
            {'днк конституція', 'природний закон', 'канонічне право'},
        ]

        # Контекстні винятки (нормальні новини)
        self.news_context = {
            'uk': {
                'повідомляє', 'інформує', 'зазначається', 'за даними',
                'джерело', 'новини', 'звіт', 'пресреліз', 'редакція',
                'тимчасово окуповані', 'сили оборони', 'завдано ураження',
                'зсу', 'зсу рф', 'бойовий потенціал', 'противник',
                'результати удару', 'уточнюються', 'втрати'
            }
        }

    def detect_language(self, text: str) -> str:
        """Визначає мову тексту"""
        ukrainian_chars = re.findall(r'[їієґ]', text.lower())
        english_chars = re.findall(r'[qwx]', text.lower())
        return 'uk' if len(ukrainian_chars) > len(english_chars) else 'en'

    def _analyze_categories(self, text: str, lang: str) -> Dict:
        """Аналізує текст за категоріями маркерів"""
        text_lower = text.lower()
        category_counts = {}
        
        for category_name, languages in self.categories.items():
            count = 0
            markers = languages.get(lang, set())
            for marker in markers:
                # Пошук цілих слів або словосполучень
                if ' ' in marker:
                    # Для словосполучень
                    if marker in text_lower:
                        count += 1
                else:
                    # Для окремих слів
                    pattern = r'\b' + re.escape(marker) + r'\b'
                    count += len(re.findall(pattern, text_lower))
            
            category_counts[category_name] = count
        
        return category_counts

    def _calculate_semantic_dissonance(self, category_counts: Dict) -> float:
        """
        Обчислює семантичний дисонанс - міру сумісності категорій
        Високе значення = текст містить несумісні категорії
        """
        total_markers = sum(category_counts.values())
        if total_markers == 0:
            return 0.0
        
        # Визначаємо домінуючі категорії
        dominant_categories = []
        for cat, count in category_counts.items():
            if count > 0:
                dominant_categories.append(cat)
        
        # Штрафуємо несумісні комбінації
        dissonance_score = 0.0
        
        # Несумісні пари категорій
        incompatible_pairs = [
            ('academic', 'conspiracy'),
            ('academic', 'esoteric'), 
            ('sovereign_citizen', 'academic'),
            ('techno_utopian', 'sovereign_citizen'),
            ('conspiracy', 'signal')  # конспірологія не може бути сигналом
        ]
        
        for cat1, cat2 in incompatible_pairs:
            if cat1 in dominant_categories and cat2 in dominant_categories:
                dissonance_score += 0.3
        
        # Особливо штрафуємо "ввічливе божевілля" - конспірологія в науковій обгортці
        if 'academic' in dominant_categories and 'conspiracy' in dominant_categories:
            academic_ratio = category_counts['academic'] / total_markers
            conspiracy_ratio = category_counts['conspiracy'] / total_markers
            if academic_ratio > 0.3 and conspiracy_ratio > 0.2:
                dissonance_score += 0.4  # Сильний штраф за мімікрію
        
        return min(1.0, dissonance_score)

    def _calculate_complexity_score(self, text: str) -> float:
        """Обчислює складність тексту з урахуванням семантики"""
        words = re.findall(r'\w+', text.lower())
        if len(words) < 10:
            return 0.5
        
        # Семантична складність (унікальність слів)
        unique_ratio = len(set(words)) / len(words)
        
        # Синтаксична складність (довжина речень)
        sentences = re.split(r'[.!?]+', text)
        avg_sentence_length = sum(len(s.split()) for s in sentences if s.strip()) / len(sentences)
        
        # Комбінована складність
        complexity = (unique_ratio * 0.6) + (min(1.0, avg_sentence_length / 30) * 0.4)
        
        return min(1.0, complexity)

    def _calculate_shannon_entropy(self, text: str) -> float:
        """Обчислює ентропію Шеннона"""
        if not text:
            return 0.0
        
        # Видаляємо зайві пробіли та розділові знаки для чистішого аналізу
        clean_text = re.sub(r'\s+', ' ', text)
        char_freq = {}
        
        for char in clean_text:
            char_freq[char] = char_freq.get(char, 0) + 1
        
        entropy = 0.0
        text_len = len(clean_text)
        
        for count in char_freq.values():
            p = count / text_len
            if p > 0:
                entropy -= p * math.log2(p)
        
        # Нормалізуємо до 0-1
        max_entropy = math.log2(len(char_freq)) if char_freq else 0
        normalized = entropy / max_entropy if max_entropy > 0 else 0
        
        return min(1.0, normalized)

    def _check_context(self, text: str, lang: str) -> Dict:
        """Перевіряє контекст тексту"""
        text_lower = text.lower()
        
        # Перевірка новинного контексту
        is_news = False
        for marker in self.news_context.get(lang, set()):
            if marker in text_lower:
                is_news = True
                break
        
        # Перевірка на класичну маячню
        has_incompatible = False
        for cluster in self.incompatible_clusters:
            matches = sum(1 for term in cluster if term in text_lower)
            if matches >= 2:  # Якщо знайдено 2+ терміни з кластеру
                has_incompatible = True
                break
        
        return {
            'is_news': is_news,
            'has_incompatible_clusters': has_incompatible
        }

    def _calculate_penalties(self, category_counts: Dict, context: Dict) -> Dict:
        """Обчислює всі штрафи на основі категорій та контексту"""
        penalties = {
            'sanity': 0.0,
            'manipulation': 0.0,
            'chaos': 0.0
        }
        
        total_markers = sum(category_counts.values())
        if total_markers == 0:
            return penalties
        
        # БАЗОВІ ШТРАФИ ЗА КАТЕГОРІЇ
        # Конспірологія завжди штрафується
        if category_counts.get('conspiracy', 0) > 0:
            base_chaos = min(0.8, category_counts['conspiracy'] / 10)
            penalties['chaos'] = max(penalties['chaos'], base_chaos)
        
        # Суверен-граждани
        if category_counts.get('sovereign_citizen', 0) >= 3:
            penalties['sanity'] = max(penalties['sanity'], 0.7)
        
        # Техно-утопічна маячня
        if category_counts.get('techno_utopian', 0) >= 4:
            penalties['manipulation'] = max(penalties['manipulation'], 0.6)
        
        # Езотеричний абсурд
        if category_counts.get('esoteric', 0) >= 3:
            penalties['chaos'] = max(penalties['chaos'], 0.5)
        
        # МУЛЬТИПЛІКАТОР: якщо кілька категорій маячні одночасно
        crazy_categories = ['conspiracy', 'sovereign_citizen', 'techno_utopian', 'esoteric']
        crazy_count = sum(1 for cat in crazy_categories if category_counts.get(cat, 0) > 0)
        
        if crazy_count >= 2:
            multiplier = 1.0 + (crazy_count * 0.3)
            for key in penalties:
                penalties[key] = min(1.0, penalties[key] * multiplier)
        
        # КОНТЕКСТУАЛЬНІ КОРЕКЦІЇ
        if context['is_news']:
            # Для новин знижуємо штрафи
            for key in penalties:
                penalties[key] *= 0.3
        
        if context['has_incompatible_clusters']:
            # Підвищуємо штраф за очевидну маячню
            penalties['sanity'] = min(1.0, penalties['sanity'] + 0.3)
        
        return penalties

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
        semantic_dissonance = self._calculate_semantic_dissonance(category_counts)
        
        # 3. БАЗОВІ МЕТРИКИ
        entropy = self._calculate_shannon_entropy(text)
        complexity = self._calculate_complexity_score(text)
        
        # 4. КОНТЕКСТ
        context = self._check_context(text, lang)
        
        # 5. ШТРАФИ
        penalties = self._calculate_penalties(category_counts, context)
        
        # 6. ФІНАЛЬНИЙ РОЗРАХУНОК
        base_score = (
            entropy * self.weights['shannon'] +
            complexity * self.weights['complexity'] +
            semantic_dissonance * self.weights['semantic_dissonance'] +
            penalties['chaos'] * self.weights['chaos_density'] +
            penalties['sanity'] * self.weights['sanity_violation']
        )
        
        # КОРЕКЦІЇ
        # Якщо текст короткий, але з маячнею - підвищуємо оцінку
        if word_count < 100 and (penalties['sanity'] > 0.5 or penalties['chaos'] > 0.5):
            base_score = min(1.0, base_score * 1.3)
        
        final_score = min(0.99, max(0.0, base_score))
        
        # 7. ВИЗНАЧЕННЯ ВЕРДИКТУ
        if penalties['sanity'] > 0.7 or penalties['chaos'] > 0.7:
            status = 'CRITICAL'
            if category_counts.get('sovereign_citizen', 0) > 0:
                verdict = 'ПСЕВДОПРАВОВИЙ АБСУРД'
            elif category_counts.get('techno_utopian', 0) > 0:
                verdict = 'ТЕХНО-УТОПІЧНА МАНІПУЛЯЦІЯ'
            elif category_counts.get('esoteric', 0) > 0:
                verdict = 'ЕЗОТЕРИЧНИЙ ДЕЛІРІЙ'
            else:
                verdict = 'КРИТИЧНА НЕСУМІСНІСТЬ ЛОГІКИ'
        
        elif final_score < self.thresholds['trusted']:
            status = 'TRUSTED'
            verdict = 'СТАБІЛЬНИЙ ЛОГІЧНИЙ СИГНАЛ'
        
        elif final_score < self.thresholds['acceptable']:
            status = 'ACCEPTABLE'
            verdict = 'ПРИЙНЯТНА СТРУКТУРОВАНА ІНФОРМАЦІЯ'
        
        elif final_score < self.thresholds['suspicious']:
            status = 'SUSPICIOUS'
            verdict = 'ІНТЕЛЕКТУАЛЬНА МІМІКРІЯ' if semantic_dissonance > 0.3 else 'ПІДОЗРІЛА РИТОРИКА'
        
        elif final_score < self.thresholds['critical']:
            status = 'WARNING'
            verdict = 'ВИСОКИЙ РІВЕНЬ СЕМАНТИЧНОГО ДИСОНАНСУ'
        
        else:
            status = 'CRITICAL'
            verdict = 'КРИТИЧНИЙ ІНФОРМАЦІЙНИЙ ХАОС'
        
        # 8. ПІДГОТОВКА РЕЗУЛЬТАТІВ
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
                'penalties': {k: round(v, 3) for k, v in penalties.items()},
                'is_news_context': context['is_news'],
                'has_incompatible_clusters': context['has_incompatible_clusters'],
                # Сумісність з фронтендом
                'chaos_markers': category_counts.get('conspiracy', 0) + category_counts.get('esoteric', 0),
                'sanity_penalty': penalties['sanity'],
                'academic_markers': category_counts.get('academic', 0),
                'signal_markers': len([w for w in words if any(m in w.lower() for m in self.signal_markers.get(lang, []))]),
                'noise_markers': len([w for w in words if any(m in w.lower() for m in self.noise_markers.get(lang, []))]),
                'shout_factor': len([w for w in words if w.isupper() and len(w) > 2]) / max(1, word_count),
                'number_density': len(re.findall(r'\d+', text)) / max(1, word_count)
            }
        }
