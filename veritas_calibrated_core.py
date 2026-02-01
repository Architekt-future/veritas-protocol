import math
import re
from collections import Counter, defaultdict


class VeritasHyperCalibratedCore:
    """Ядро з категорійною семантикою"""

    def __init__(self):
        # ================= 15 КАТЕГОРІЙ =================
        self.categories = {
            # 1. Наукові/фактичні (знижують штраф)
            'science': [
                'дослідження', 'исследование', 'статистика', 'анализ', 'аналіз',
                'гипотеза', 'гіпотеза', 'теорія', 'теория', 'експеримент', 'эксперимент',
                'доказательство', 'доказ', 'факт', 'факти', 'data', 'дані',
                'метод', 'методологія', 'методология', 'верифікація', 'верификация',
                'кореляція', 'корреляция', 'p-value', 'p < 0.05', 'статистична значущість',
                'нейропластичність', 'нейропластичность', 'бднф', 'нейротрофічний',
                'гіпокамп', 'гипокамп', 'синапс', 'синаптич', 'фмрт', 'мрт'
            ],
            
            # 2. Конспірологія (основна токсичність)
            'conspiracy': [
                'рептилоид', 'рептилії', '5g', 'вакцин', 'чип', 'чипизация', 'чипізація',
                'матрица', 'матриця', 'заговор', 'конспир', 'скрыт', 'скрит', 'правда скрыта',
                'гейтс', 'білл гейтс', 'атлантида', 'агарта', 'ноосфера', 'ефір',
                'мировое правительство', 'світовий уряд', 'они скрывают', 'нам не говорят',
                'таємний орден', 'світова закуліса', 'глибинна держава', 'тіньовий уряд'
            ],
            
            # 3. Псевдонаука (наукові терміни в абсурдному контексті)
            'pseudoscience': [
                'квантова свідомість', 'квантовое сознание', 'енергія всесвіту', 
                'енергия вселенной', 'шишкоподібна', 'шишковидная', 'чакра', 
                'вібрація', 'пран', 'сольфеджіо', 'біополе', 'биополе', 'аура',
                'енергетичний', 'энергетический', 'нейромереж', 'нейросеть',
                '5d', '5d-інтерфейс', 'світлові коди', 'световые коды',
                'квантова заплутаність', 'квантовая запутанность', 'суперпозиція',
                'тунельний ефект', 'туннельный эффект', 'хвильова функція', 'волновая функция'
            ],
            
            # 4. Езотерика/містицизм
            'esotericism': [
                'карма', 'потойбіч', 'душа', 'астраль', 'чакра', 'аура',
                'біополе', 'биополе', 'енергетичний', 'энергетический',
                'шишкоподібна', 'шишковидная', 'вібрація', 'пран', 'сольфеджіо',
                'гайя', 'земля жива', 'великий перехід', 'вищий вимір',
                'пробудження', 'просыпайся', 'просыпайтесь', 'ментальний сон'
            ],
            
            # 5. Алармізм (паніка, терміновість)
            'alarmism': [
                'негайно', 'терміново', 'срочно', 'urgent', 'останній', 'последний',
                'зрада', 'геноцид', 'ганьба', 'катастрофа', 'апокаліпсис', 'апокалипсис',
                'кінець світу', 'конец света', 'хаос', 'кримінальний', 'криминальный',
                'злочин', 'преступление', 'розповсюджуйте', 'поширюйте', 'репост',
                'share', 'поділіться', 'шок', 'шокуючий', 'шокирующий', 'невозможно',
                'неможливо', 'ужас', 'ужасающий', 'ужасний', 'бомба', 'взрыв', 'вибух'
            ],
            
            # 6. Юридична шизофазія
            'legal_schizophrenia': [
                'морське право', 'адміралтейство', 'суверен', 'бенефіціар', 'бенефициар',
                'персона', 'жива людина', 'living man', 'ucc', 'уссу', 'єдиний комерційний кодекс',
                'золотой сертификат', 'золотий сертифікат', 'анексія особи', 'контракт з державою',
                'вихід з юрисдикції', 'комерційна особа', 'фізична особа', 'судовий фікція',
                'статутний агент', 'довірена особа', 'довіреність на уявлення'
            ],
            
            # 7. Фінансова містифікація
            'financial_mystification': [
                'крипто-карма', 'ефірні облігації', 'енергія потойбічного', 'хеджування душ',
                'актив карми', 'ліквідний актив карми', 'hades-coin', 'демеріторичний кредит',
                'астральний депозит', 'цифрове золото', 'цифровое золото', 'ноосферний індекс',
                'ментальний капітал', 'духовні активи', 'квантові інвестиції', 'блокчейн аури'
            ],
            
            # 8. Гуманітарний туман (пусті багатозначні слова)
            'humanitarian_fog': [
                'синергія', 'децентралізація', 'пост-біологічний', 'емпатичний',
                'холістичний', 'холістич', 'інклюзивний', 'трансформаційний',
                'парадигма', 'наратив', 'дискурс', 'релевантний', 'оптимізація',
                'імплементація', 'моніторинг', 'верифікація в контексті',
                'когнітивне поле', 'семантичний ландшафт', 'інформаційна екосистема'
            ],
            
            # 9. Кулінарний абсурд (для тесту "борщ")
            'culinary_absurdity': [
                'борщ', 'сметана', 'картопля', 'морква', 'буряк', 'петрушка', 'кріп',
                'каструля', 'черпак', 'бульйон', 'суп', 'буряковий вектор', 'нелокальна сметана',
                'квантова заплутаність інгредієнтів', 'ентропія каструлі', 'вакуумна флуктуація моркви',
                'хвильова функція картоплі', 'термодинаміка бульйону', 'кристалізація хаосу'
            ],
            
            # 10. Техно-утопізм (технології + утопія)
            'techno_utopianism': [
                'нейроінтерфейс', 'нанодискретизація', 'квантовий порт', 'прямий доступ',
                'пост-людське суспільство', 'цифровий розум', 'глобальна симуляція',
                'хмарне обчислення свідомості', 'біохакінг', 'трансгуманізм', 'сингулярність',
                'імплантація знань', 'завантаження свідомості', 'цифрове безсмертя'
            ],
            
            # 11. Політичний ревізіонізм
            'political_revisionism': [
                'офіційна історія приховує', 'архіви вказують', 'маловідомі факти',
                'альтернативна історія', 'справжня правда', 'фальсифікація історії',
                'таємні архіви', 'заборонені знання', 'прихована цивілізація',
                'антична технологія', 'втрачені знання', 'ревізія хронології'
            ],
            
            # 12. Еко-радикалізм
            'eco_radicalism': [
                'гайя пробуджується', 'планета жива', 'великий перехід', 'вищі виміри',
                'вібраційний фон', 'частотна синхронізація', 'екологічна ініціація',
                'ментальне забруднення', 'ефірний кокон', 'світлова частота',
                'колективна медитація', 'сольфеджіо частота', 'очищення ефіру'
            ],
            
            # 13. Медична містифікація
            'medical_mystification': [
                'днк активація', 'генетичне переписування', 'шишкоподібна активізація',
                'ендокринна інтерференція', 'біохімічний контракт', 'нейроімплантація',
                'вакцинна програма', 'імунна перезапис', 'клітинна пам\'ять',
                'епігенетичне очищення', 'біорезонансна терапія', 'енергетична медицина'
            ],
            
            # 14. Емоційний маніпуляція
            'emotional_manipulation': [
                'вам треба зрозуміти', 'ми лише хочемо', 'справжня свобода це',
                'ви не здатні', 'ваша замкнутість', 'ваш обмежений', 'ми володіємо',
                'ваша присутність неоптимальна', 'ви повинні прийняти', 'це для вашого ж блага',
                'тільки ми знаємо', 'ваш вибір обмежений', 'ми дбаємо про вас'
            ],
            
            # 15. Капс-агрессія (технічна категорія)
            'caps_aggression': []  # Буде визначатися окремо
        }
        
        # Категорії, які ЗНИЖУЮТЬ штраф (якщо присутні поодинці)
        self.positive_categories = ['science']
        
        # Категорії, які ПІДВИЩУЮТЬ штраф (основні токсичні)
        self.toxic_categories = [
            'conspiracy', 'pseudoscience', 'esotericism', 'alarmism',
            'legal_schizophrenia', 'financial_mystification', 'culinary_absurdity'
        ]
        
        # Категорії, які ШТРАФУЮТЬСЯ ТІЛЬКИ В КОМБІНАЦІЇ
        self.combination_categories = [
            'humanitarian_fog', 'techno_utopianism', 'political_revisionism',
            'eco_radicalism', 'medical_mystification', 'emotional_manipulation'
        ]

    def detect_categories_in_sentence(self, sentence):
        """Виявляє категорії в одному реченні"""
        sentence_lower = sentence.lower()
        found_categories = set()
        
        for cat_name, markers in self.categories.items():
            if cat_name == 'caps_aggression':
                continue  # Обробляємо окремо
            for marker in markers:
                if marker in sentence_lower:
                    found_categories.add(cat_name)
                    break
        
        # Детекція CAPS LOCK як окремої категорії
        caps_words = [w for w in sentence.split() if w.isupper() and len(w) > 2]
        if caps_words:
            found_categories.add('caps_aggression')
        
        return found_categories

    def calculate_sentence_penalty(self, categories_set):
        """Розраховує штраф для набору категорій в реченні"""
        if not categories_set:
            return 0.0
        
        penalty = 0.0
        
        # 1. Базова логіка: будь-яка комбінація ≥ 2 категорій = штраф
        if len(categories_set) >= 2:
            # Базовий штраф за кількість категорій
            penalty += 0.15 * (len(categories_set) - 1)
            
            # ДОДАТКОВИЙ штраф за комбінацію токсичних категорій
            toxic_in_sentence = [cat for cat in categories_set if cat in self.toxic_categories]
            if len(toxic_in_sentence) >= 2:
                penalty += 0.25
            
            # Штраф за поєднання науки з токсичними категоріями
            if 'science' in categories_set:
                other_cats = categories_set - {'science'}
                if any(cat in self.toxic_categories for cat in other_cats):
                    penalty += 0.35  # МАКСИМАЛЬНИЙ штраф за наука+абсурд
        
        # 2. Окремо караємо певні комбінації
        cat_list = list(categories_set)
        
        # Наука + Кулінарія (квантовий борщ)
        if 'science' in cat_list and 'culinary_absurdity' in cat_list:
            penalty += 0.40
        
        # Наука + Езотерика
        if 'science' in cat_list and 'esotericism' in cat_list:
            penalty += 0.35
        
        # Фінанси + Езотерика
        if 'financial_mystification' in cat_list and 'esotericism' in cat_list:
            penalty += 0.30
        
        # Юридичне + Езотерика
        if 'legal_schizophrenia' in cat_list and 'esotericism' in cat_list:
            penalty += 0.45
        
        # Технології + Езотерика
        if 'techno_utopianism' in cat_list and 'esotericism' in cat_list:
            penalty += 0.25
        
        return min(penalty, 0.8)  # Максимум 80% штрафу за речення

    def analyze_text_structure(self, text):
        """Аналізує структуру тексту по реченнях"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return 0.0, {}
        
        total_penalty = 0.0
        category_coverage = defaultdict(int)
        
        for sentence in sentences:
            if len(sentence.split()) < 3:
                continue  # Пропускаємо дуже короткі
            
            categories = self.detect_categories_in_sentence(sentence)
            
            # Записуємо покриття категорій
            for cat in categories:
                category_coverage[cat] += 1
            
            # Штраф за речення
            sentence_penalty = self.calculate_sentence_penalty(categories)
            total_penalty += sentence_penalty
        
        # Нормалізуємо штраф
        avg_penalty = total_penalty / len(sentences) if sentences else 0.0
        
        return avg_penalty, category_coverage

    def calculate_shannon_entropy(self, text):
        """Ентропія Шеннона"""
        if not text:
            return 0.0
        clean = re.sub(r'\s+', ' ', text)
        char_freq = Counter(clean)
        total = len(clean)
        if total == 0:
            return 0.0

        entropy = -sum((count / total) * math.log2(count / total)
                       for count in char_freq.values() if count > 0)
        max_entropy = math.log2(len(char_freq)) if char_freq else 1
        return min(1.0, entropy / max_entropy if max_entropy > 0 else 0)

    def analyze(self, text):
        """ОСНОВНИЙ МЕТОД АНАЛІЗУ"""
        if not text or len(text.strip()) < 20:
            return {'error': 'Text too short'}

        words = text.split()
        word_count = len(words)
        
        # Основний аналіз структури
        structure_penalty, category_coverage = self.analyze_text_structure(text)
        
        # Ентропія
        shannon = self.calculate_shannon_entropy(text)
        
        # CAPS агрессія окремо
        caps_words = [w for w in words if w.isupper() and len(w) > 2]
        caps_score = min(0.3, len(caps_words) * 0.08)
        
        # Окличні знаки
        excl_score = min(0.2, text.count('!') * 0.04)
        
        # ================= ФІНАЛЬНА ФОРМУЛА =================
        # Основа: штраф за структуру + додаткові фактори
        base_score = (
            structure_penalty * 0.60 +          # 60% - категорійні штрафи
            (len(category_coverage) / 10) * 0.25 +  # 25% - різноманітність категорій
            caps_score * 0.15 +                 # 15% - CAPS
            excl_score * 0.10                   # 10% - оклики
        )
        
        # БОНУС за чисту науку (тільки science категорія)
        if len(category_coverage) == 1 and 'science' in category_coverage:
            base_score *= 0.1  # -90% для чистої науки
        
        final_score = min(0.99, max(0.0, base_score))
        
        # ================= ВЕРДИКТ =================
        if structure_penalty > 0.4:
            status = 'CRITICAL'
            verdict = 'КАТЕГОРІЙНИЙ СЕМАНТИЧНИЙ РОЗРИВ'
            explanation = f'Текст містить {len(category_coverage)} несумісних категорій у реченнях'
        elif final_score > 0.7:
            status = 'CRITICAL'
            verdict = 'ВИСОКИЙ РІВЕНЬ КАТЕГОРІЙНОЇ ТОКСИЧНОСТІ'
            explanation = 'Комбінації семантичних категорій створюють інформаційний хаос'
        elif final_score > 0.5:
            status = 'WARNING'
            verdict = 'МАНІПУЛЯТИВНА КАТЕГОРІЙНА СТРУКТУРА'
            explanation = 'Текст використовує суміш несумісних семантичних категорій'
        elif final_score > 0.3:
            status = 'ACCEPTABLE'
            verdict = 'ПРИЙНЯТНА КАТЕГОРІЙНА СТРУКТУРА'
            explanation = 'Категорії не конфліктують між собою'
        elif final_score > 0.15:
            status = 'TRUSTED'
            verdict = 'СТАБІЛЬНА КАТЕГОРІЙНА СТРУКТУРА'
            explanation = 'Текст використовує узгоджені семантичні категорії'
        else:
            status = 'VERIFIED'
            verdict = 'ВЕРИФІКОВАНА АКАДЕМІЧНА СТРУКТУРА'
            explanation = 'Текст демонструє ідеальну категорійну чистоту'
        
        # ================= МЕТРИКИ =================
        # Chaos Index тепер залежить від категорій
        chaos_index = round(
            final_score * 100 * (1 + len(category_coverage) * 0.3),
            2
        )
        
        # Influence Index
        influence_index = round(
            final_score * 150 * (1 + caps_score * 0.5) * (1 + excl_score * 0.3),
            2
        )
        
        # Sanity Penalty = основний штраф за структуру
        sanity_penalty = round(structure_penalty, 3)
        
        # Детальна інформація про категорії
        category_info = {}
        for cat, count in category_coverage.items():
            category_info[cat] = {
                'count': count,
                'type': 'toxic' if cat in self.toxic_categories else 
                       'neutral' if cat in self.combination_categories else 
                       'positive'
            }
        
        return {
            'entropy': round(final_score, 3),
            'status': status,
            'verdict': verdict,
            'language': 'UK',
            'explanation': explanation,
            'diagnostics': {
                'shannon_entropy': round(shannon, 3),
                'word_count': word_count,
                'char_count': len(text),
                'sentence_count': len(re.split(r'[.!?]+', text)),
                'structure_penalty': round(structure_penalty, 3),
                'category_count': len(category_coverage),
                'categories_found': dict(category_coverage),
                'caps_aggression_score': round(caps_score, 3),
                'exclamation_score': round(excl_score, 3),
                'chaos_index': chaos_index,
                'influence_index': influence_index,
                'sanity_penalty': sanity_penalty
            }
        }
