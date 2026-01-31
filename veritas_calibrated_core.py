"""
Veritas Protocol - Calibrated Core Engine (FIXED v5.1)
Enhanced schizoid pattern detection
"""

import math
import re
from typing import Dict

class VeritasCalibratedCore:
    """Calibrated entropy analysis with weighted scoring"""

    def __init__(self):
        # Configurable thresholds
        self.thresholds = {
            'trusted': 0.35,
            'acceptable': 0.55,
            'suspicious': 0.75,
            'critical': 0.85
        }

        # Configurable weights (Orpheus style)
        self.weights = {
            'shannon': 0.25,
            'complexity': 0.15,
            'noise_signal_ratio': 0.20,
            'chaos_density': 0.15,
            'sanity_violation': 0.15,
            'shout_factor': 0.10
        }

        self.chaos_density_threshold = 0.05

        self.noise_markers = {
            'uk': {
                'шокуюча', 'паніка', 'приховували', 'потрясла', 'сенсація', 'терміново',
                'катастрофічн', 'апокаліпсис', 'крах', 'знищен', 'загиб', 'жахливий',
                'небезпека', 'злочин', 'зрада', 'зрадник', 'вбивство', 'кривавий'
            },
            'en': {
                'shocking', 'panic', 'hidden', 'sensational', 'must', 'urgent',
                'catastrophic', 'apocalypse', 'collapse', 'destruction', 'perish',
                'horrible', 'danger', 'crime', 'betrayal', 'traitor', 'murder', 'bloody'
            }
        }

        self.signal_markers = {
            'uk': {
                'якщо', 'тоді', 'тому', 'внаслідок', 'дорівнює', 'факт',
                'даних', 'показник', 'вимір', 'кількість', 'дослідження',
                'статистичний', 'кореляція', 'регресія', 'аналіз', 'респондентів',
                'метод', 'експеримент', 'гіпотеза', 'вибірка', 'результат',
                'протокол', 'систем', 'модель', 'теорі', 'практичн', 'висновок',
                'звіт', 'документ', 'закон', 'правило', 'процедура', 'стандарт'
            },
            'en': {
                'if', 'then', 'therefore', 'consequently', 'equals', 'fact',
                'data', 'metric', 'measurement', 'quantity', 'research',
                'statistical', 'correlation', 'regression', 'analysis', 'study',
                'method', 'experiment', 'hypothesis', 'sample', 'respondents',
                'result', 'protocol', 'system', 'model', 'theory', 'conclusion',
                'report', 'document', 'law', 'rule', 'procedure', 'standard'
            }
        }

        # Academic indicators
        self.academic_markers = {
            'uk': {
                'дослідження', 'аналіз', 'методолог', 'експеримент', 'гіпотеза',
                'респондент', 'статистичн', 'кореляц', 'регрес', 'вибірк',
                'науков', 'публікац', 'журнал', 'конференц', 'протокол',
                'архітектур', 'систем', 'алгоритм', 'модель', 'теорі',
                'практичн', 'результат', 'висновок', 'апроксимаці', 'синтез',
                'верифікац', 'калібровка', 'детермінізм', 'вердикт',
                'категорі', 'таксономі', 'епістемолог', 'семантичн'
            },
            'en': {
                'research', 'study', 'analysis', 'methodology', 'experiment',
                'hypothesis', 'respondent', 'statistical', 'correlation',
                'regression', 'sample', 'scientific', 'publication', 'journal',
                'conference', 'protocol', 'architecture', 'system', 'algorithm',
                'model', 'theory', 'practice', 'result', 'conclusion',
                'approximation', 'synthesis', 'verification', 'calibration',
                'determinism', 'verdict', 'category', 'taxonomy',
                'epistemological', 'semantic'
            }
        }

        # РОЗШИРЕНІ chaos_markers - додано специфічні шизофренічні маркери
        self.chaos_markers = {
            'uk': {
                # Класична конспірологія
                'рептилоїд', 'плоскоземель', 'плоскоземл', 'ілюмінат',
                'нібіру', 'анунак', 'хімітрейл', 'психотрон', 'біогенн',
                'універсальн змов', 'теорії змов', 'прибулець', 'рептилі',
                'змовник', 'таємн орден', 'світов правлін', 'чіпува',
                'інопланетн', 'масон', 'глобаліст', 'світова змова',
                # Шизофренічні паттерни
                '5g', '5g-веж', 'гейтс', 'білл гейтс', 'вакцин', 'вакцинован',
                'дельфін', 'сатурн', 'голограм', 'обам', 'хемтрейл', 'хемтрейли',
                'синхронізація', 'тесла', 'п\'ятий вимір', 'портал', 'макдональдс',
                'рептил', 'чип', 'днк', 'ефірн', 'енергія сатурна', 'частоти 432',
                '432 гц', 'перехід у вимір', 'псевдонаук', 'псевдонаука',
                'астральн', 'чакр', 'карм', 'енергет', 'біопол', 'квантов',
                'мультивсесвіт', 'вимір', 'паралельн', 'портал', 'трансмутац',
                'кристалізац', 'резонанс', 'частот', 'голограф', 'проекц',
                'зомбування', 'контроль розуму', 'промислов', 'змова фарм',
                'хімічн стеж', 'радіохвил', 'мікрохвил', 'електромагнітн',
                'скалярн', 'торсіон', 'оргон', 'прана', 'ци', 'рейкі'
            },
            'en': {
                'reptilian', 'flat earth', 'illuminati', 'nibiru',
                'annunaki', 'chemtrail', 'psychotronic', 'bioweapon',
                'universal conspiracy', 'conspiracy theory', 'alien',
                'reptilian', 'secret order', 'world government', 'microchip',
                'freemason', 'globalist', 'new world order',
                # Schizoid patterns
                '5g', '5g tower', 'gates', 'bill gates', 'vaccine', 'vaccinated',
                'dolphin', 'saturn', 'hologram', 'obama', 'chemtrails',
                'synchronization', 'tesla', 'fifth dimension', 'portal', 'mcdonald\'s',
                'reptile', 'chip', 'dna', 'ether', 'saturn energy', '432 hz',
                'frequency 432', 'dimensional shift', 'pseudoscience',
                'astral', 'chakra', 'karma', 'energy field', 'bioplasma', 'quantum',
                'multiverse', 'dimension', 'parallel', 'portal', 'transmutation',
                'crystallization', 'resonance', 'frequency', 'holographic', 'projection',
                'mind control', 'zombification', 'big pharma', 'chemical trails',
                'radio wave', 'microwave', 'electromagnetic', 'scalar', 'torsion',
                'orgone', 'prana', 'chi', 'reiki'
            }
        }

        # РОЗШИРЕНІ кластери несумісності - для шизофренічних комбінацій
        self.incompatible_clusters = [
            # Квантова фізика + побут (явна маячня)
            {'квантов', 'борщ', 'каструл', 'сметан', 'бульйон'},
            {'мультивсесвіт', 'суп', 'черпак', 'картопл'},
            {'енерг', 'чакр', 'біопол', 'астральн', 'карм'},
            # Шизофренічні комбінації
            {'рептилоїд', '5g', 'чип', 'гейтс', 'вакцин'},
            {'сатурн', 'ефірн', 'енергія', 'дельфін', 'днк'},
            {'тесла', 'трамп', 'маска', 'п\'ятий вимір'},
            {'портал', 'макдональдс', 'голограм', 'обам'},
            {'хімітрейл', 'хемтрейл', 'повітря', 'отруєн'},
            {'синхронізація', '11:11', 'число', 'нумеролог'},
            {'частоти', '432', 'гц', 'зуб', 'чип'},
            {'вакцинован', 'дельфін', 'людин', 'гібрид'},
            {'білл гейтс', 'мікрочіп', 'контроль', 'населен'},
            {'плоскоземель', 'наса', 'приховуван', 'правда'},
            {'ілюмінат', 'світовий уряд', 'новий світовий порядок'},
            {'прибулець', 'рептил', 'людин', 'змішан'},
            {'психотрон', 'зброя', 'контроль розуму', 'масова'},
            {'нібіру', 'планета', 'зближен', 'катаклізм'},
            {'анунак', 'інопланетн', 'цивілізац', 'стародавн'},
            {'біоген', 'лаборатор', 'вірус', 'створен'},
            {'універсальн', 'змов', 'все', 'контролює'},
            {'масон', 'таємн', 'товариств', 'влада'}
        ]

        # Нові списки для розпізнавання контексту
        self.military_context_indicators = {
            'uk': {
                'зсу', 'зсу рф', 'тимчасово окуповані', 'тимчасово окупована',
                'сили оборони', 'жива сила', 'бойовий потенціал', 'завдано ураження',
                'пункт управління', 'район населеного пункту', 'втрати противника',
                'генеральний штаб', 'результати удару', 'уточнюються', 'бпла',
                'мотострілецька', 'зосередження живої сили', 'противник', 'агресор'
            },
            'en': {
                'armed forces', 'temporarily occupied', 'defense forces', 
                'combat potential', 'strike', 'command post', 'enemy losses',
                'general staff', 'military object'
            }
        }

        self.news_context_indicators = {
            'uk': {
                'повідомляє', 'інформує', 'зазначається', 'окремо зазначається',
                'крім того', 'також', 'при цьому', 'за даними', 'джерело',
                'новини', 'звіт', 'пресреліз', 'редакція'
            },
            'en': {
                'reports', 'informs', 'noted', 'separately noted',
                'in addition', 'also', 'according to', 'source',
                'news', 'report', 'press release', 'editorial'
            }
        }

        # Шизофренічні контексти
        self.schizoid_context_indicators = {
            'uk': {
                'зомбування', 'контроль розуму', 'зброя масового ураження',
                'секретн технолог', 'приховують', 'не кажуть', 'правда',
                'реальність', 'матриця', 'симуляц', 'пробуджен',
                'освітлен', 'просвітлен', 'висші сили', 'космічн',
                'галактичн', 'паранормальн', 'екстрасенс', 'ясновид',
                'телепат', 'пси-зброя', 'психотронн', 'зомбі'
            }
        }

    def detect_language(self, text: str) -> str:
        ukrainian_chars = re.findall(r'[їієґ]', text.lower())
        return 'uk' if len(ukrainian_chars) > 3 else 'en'

    def _has_context(self, text: str, lang: str, indicators: dict) -> bool:
        """Перевіряє, чи текст містить слова з вказаного списку індикаторів."""
        text_lower = text.lower()
        for phrase in indicators.get(lang, set()):
            if phrase in text_lower:
                return True
        return False

    def _count_context_matches(self, text: str, lang: str, indicators: dict) -> int:
        """Підраховує кількість збігів з контекстними індикаторами."""
        text_lower = text.lower()
        matches = 0
        for phrase in indicators.get(lang, set()):
            if phrase in text_lower:
                matches += 1
        return matches

    def _shannon_entropy(self, text: str) -> float:
        if not text:
            return 0.0
        char_freq = {}
        for char in text:
            char_freq[char] = char_freq.get(char, 0) + 1
        entropy = 0.0
        text_len = len(text)
        for count in char_freq.values():
            p = count / text_len
            if p > 0:
                entropy -= p * math.log2(p)
        return min(1.0, entropy / 8.0)

    def _calculate_complexity(self, text: str) -> float:
        words = re.findall(r'\w+', text.lower())
        if not words:
            return 1.0
        unique_words = len(set(words))
        total_words = len(words)
        diversity = unique_words / total_words
        complexity = 1.0 - diversity
        if total_words > 500 and complexity > 0.6:
            complexity *= 0.7
        return complexity

    def _count_markers(self, words: list, lang: str) -> Dict:
        noise_count = 0
        signal_count = 0
        chaos_count = 0
        academic_count = 0

        for word in words:
            word_lower = word.lower()
            # Перевірка шуму
            for marker in self.noise_markers.get(lang, set()):
                if marker in word_lower:
                    noise_count += 1
                    break
            # Перевірка сигналу
            for marker in self.signal_markers.get(lang, set()):
                if marker in word_lower:
                    signal_count += 1
                    break
            # Перевірка хаосу
            for marker in self.chaos_markers.get(lang, set()):
                if marker in word_lower:
                    chaos_count += 1
                    break
            # Перевірка академічних
            for marker in self.academic_markers.get(lang, set()):
                if marker in word_lower:
                    academic_count += 1
                    break

        return {
            'noise': noise_count,
            'signal': signal_count,
            'chaos': chaos_count,
            'academic': academic_count
        }

    def _check_sanity(self, words: list, text: str, lang: str) -> float:
        # Перевіряємо на шизофренічний контекст
        schizoid_matches = self._count_context_matches(text, lang, self.schizoid_context_indicators)
        
        # Якщо це новинний чи військовий контекст - знижуємо штраф
        has_military = self._has_context(text, lang, self.military_context_indicators)
        has_news = self._has_context(text, lang, self.news_context_indicators)
        
        if has_military or has_news:
            # Для новин та військових звітів - МІНІМАЛЬНИЙ штраф
            return 0.05

        words_lower = [w.lower() for w in words]
        
        # Основна перевірка кластерів
        for cluster in self.incompatible_clusters:
            match_count = 0
            for word in words_lower:
                for pattern in cluster:
                    if pattern in word:
                        match_count += 1
                        break
            if match_count >= 3:
                return 0.9
        
        # Додаткова перевірка: якщо багато хаос-маркерів
        if len([w for w in words_lower if any(m in w for m in self.chaos_markers.get(lang, set()))]) >= 5:
            return 0.8
        
        # Перевірка на шизофренічний контекст
        if schizoid_matches >= 3:
            return 0.7
        
        return 0.0

    def _calculate_number_density(self, text: str, word_count: int) -> float:
        if word_count == 0:
            return 0.0
        numbers = re.findall(r'\d+\.?\d*', text)
        return len(numbers) / (word_count + 1)

    def _calculate_shout_factor(self, text: str, word_count: int) -> float:
        if word_count == 0:
            return 0.0
        # Рахуємо слова в CAPSLOCK (більше 2 символів)
        caps_words = len([w for w in text.split() if w.isupper() and len(w) > 2])
        exclamations = text.count('!')
        questions = text.count('?')
        shout = (exclamations * 2 + caps_words * 3 + questions) / (word_count + 1)
        return min(shout, 1.0)

    def analyze(self, text: str) -> Dict:
        if not text or len(text.strip()) < 10:
            return {'error': 'Text too short'}

        lang = self.detect_language(text)
        words = re.findall(r'\w+', text.lower())
        word_count = len(words)

        shannon = self._shannon_entropy(text)
        complexity = self._calculate_complexity(text)
        markers = self._count_markers(words, lang)
        sanity_penalty = self._check_sanity(words, text, lang)
        number_density = self._calculate_number_density(text, word_count)
        shout_factor = self._calculate_shout_factor(text, word_count)

        chaos_density = markers['chaos'] / word_count if word_count > 0 else 0
        academic_density = markers['academic'] / word_count if word_count > 0 else 0
        
        is_academic = False
        if academic_density > 0.02 and markers['academic'] > 8:
            is_academic = True
        elif markers['academic'] > 15 and word_count > 1000:
            is_academic = True
        elif markers['signal'] > 50 and markers['academic'] > 5 and complexity < 0.6:
            is_academic = True

        # Перевірка контексту для корекції
        has_military = self._has_context(text, lang, self.military_context_indicators)
        has_news = self._has_context(text, lang, self.news_context_indicators)
        
        # ДОДАТКОВА КОРЕКЦІЯ ДЛЯ ШИЗОФРЕНІЧНИХ ТЕКСТІВ
        schizoid_matches = self._count_context_matches(text, lang, self.schizoid_context_indicators)
        
        # ПІДСИЛЕННЯ для шизофренічних текстів
        if schizoid_matches >= 2 or markers['chaos'] >= 8:
            # Сильно підвищуємо chaos_density
            chaos_density = min(1.0, markers['chaos'] / max(1, word_count/2))
            # Підвищуємо shout_factor якщо є CAPSLOCK
            if any(w.isupper() and len(w) > 2 for w in text.split()):
                shout_factor = min(1.0, shout_factor * 2)
        
        # КОРЕКЦІЯ ДЛЯ НОВИН
        elif has_military or has_news:
            # ЗНИЖУЄМО chaos_density для новин
            chaos_density *= 0.01
            # ЗНИЖУЄМО загальну ентропію
            shannon *= 0.7

        if markers['signal'] + markers['noise'] > 0:
            noise_signal_ratio = markers['noise'] / (markers['signal'] + markers['noise'] + 1)
        else:
            noise_signal_ratio = 0.5

        components = {
            'shannon': shannon,
            'complexity': complexity,
            'noise_signal_ratio': noise_signal_ratio,
            'chaos_density': chaos_density,
            'sanity_violation': sanity_penalty,
            'shout_factor': shout_factor
        }

        base_entropy = sum(components[key] * self.weights[key] for key in components.keys())
        base_entropy *= (1.0 - number_density * 0.25)

        if is_academic:
            base_entropy *= 0.6

        # ДОДАТКОВА КОРЕКЦІЯ для шизофренічних текстів
        if schizoid_matches >= 3 or markers['chaos'] >= 10:
            base_entropy = min(1.0, base_entropy * 1.5)

        final_entropy = min(0.99, max(0.0, base_entropy))

        # СПЕЦИФІЧНА ЛОГІКА ВЕРДИКТУ ДЛЯ ШИЗОФРЕНІЧНИХ ТЕКСТІВ
        if schizoid_matches >= 3 or markers['chaos'] >= 10:
            status, verdict = 'CRITICAL', 'КРИТИЧНА НЕСУМІСНІСТЬ ЛОГІКИ'
        elif has_military or has_news:
            # ДЛЯ НОВИН - АВТОМАТИЧНО ПРИЙНЯТНО
            if final_entropy < 0.6:
                status, verdict = 'ACCEPTABLE', 'НОВИННИЙ ТЕКСТ'
            else:
                status, verdict = 'SUSPICIOUS', 'НОВИНИ З ОЗНАКАМИ МАНІПУЛЯЦІЇ'
        elif final_entropy < self.thresholds['trusted']:
            status, verdict = 'TRUSTED', 'СТАБІЛЬНИЙ ЛОГІЧНИЙ СИГНАЛ'
        elif final_entropy < self.thresholds['acceptable']:
            status, verdict = 'ACCEPTABLE', 'ПРИЙНЯТНА СТРУКТУРОВАНА ІНФОРМАЦІЯ'
        elif final_entropy < self.thresholds['suspicious']:
            status, verdict = 'SUSPICIOUS', 'ПІДОЗРІЛА ЕМОЦІЙНА РИТОРИКА'
        elif final_entropy < self.thresholds['critical']:
            status, verdict = 'WARNING', 'ВИСОКИЙ РІВЕНЬ МАНІПУЛЯЦІЇ'
        else:
            status, verdict = 'CRITICAL', 'КРИТИЧНИЙ ІНФОРМАЦІЙНИЙ ХАОС'

        return {
            'entropy': round(final_entropy, 3),
            'status': status,
            'verdict': verdict,
            'language': lang.upper(),
            'diagnostics': {
                'shannon_entropy': round(shannon, 3),
                'complexity': round(complexity, 3),
                'noise_markers': markers['noise'],
                'signal_markers': markers['signal'],
                'chaos_markers': markers['chaos'],
                'chaos_density': round(chaos_density, 4),
                'academic_markers': markers['academic'],
                'academic_density': round(academic_density, 4),
                'is_academic_context': is_academic,
                'number_density': round(number_density, 3),
                'shout_factor': round(shout_factor, 3),
                'sanity_penalty': round(sanity_penalty, 3),
                'sanity_violations': sanity_penalty > 0,
                'word_count': word_count,
                'char_count': len(text)
            }
        }
