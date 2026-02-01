"""
Veritas Protocol - Semantic Void Detector v10.6 (FIXED - Conflict focus)
"""

import re
import math
from collections import Counter

class VeritasCalibratedCore:
    """Advanced detector with fine-tuned sensitivity - FOCUS ON CONFLICTS"""
    
    def __init__(self):
        # Всі існуючі категорії залишаємо як є
        self.critical_patterns = [...]  # як було
        
        self.chaos_indicators = {...}  # як було (14 категорій)
        
        self.signal_markers = [...]  # як було
        
        self.academic_whitelist = [...]  # як було
        
        # ============================================================
        # РОЗШИРЕНІ КОНФЛІКТНІ ПАРИ (ВИСОКОСПЕЦИФІЧНІ)
        # ============================================================
        self.conflict_pairs = [
            # Оригінальні 10
            (['бднф', 'гіпокамп', 'нейропластичність'], ['5g', 'супутник', 'таргетування'], 0.35),
            (['нейтрино', 'квантовий', 'ентропія'], ['ринок', 'економіка', 'політика'], 0.3),
            (['днк', 'генетичний'], ['алгоритм', 'код', 'підпис'], 0.4),
            (['антарктида', 'атлантида'], ['технологія', 'цивілізація', 'резонатор'], 0.3),
            (['облігація', 'криптовалюта', 'банк'], ['потойбічний', 'карма', 'душа'], 0.4),
            (['вакцина', 'щеплення', 'FDA', 'ВОЗ'], ['скрита правда', 'вони скрывают', 'Big Pharma'], 0.4),
            (['AI', 'штучний інтелект', 'нейромережа', 'блокчейн'], ['душа', 'свідомість', 'карма', 'астрал', 'awakening'], 0.35),
            (['статистика', 'дані', 'дослідження', 'університет'], ['snake oil', 'народна медицина', 'натуральне лікування'], 0.35),
            (['патріот', 'батківщина', 'нація'], ['ворог народу', 'предатель', 'зрада', 'п\'ята колона'], 0.3),
            
            # ============================================================
            # УНІВЕРСАЛЬНІ КОНФЛІКТНІ ПАРИ ДЛЯ АБСУРДУ
            # ============================================================
            
            # 1. Наукові терміни + їжа (квантовий борщ)
            (['квантовий', 'квантова', 'квантове', 'квантові', 'ентропія', 'флуктуація', 'тунельний', 'сингулярність', 
              'суперпозиція', 'планк', 'гейзенберг', 'хвильова функція', 'колапс хвильової', 'мультивсесвіт', 
              'кристалізація', 'термодинаміка', 'термодинаміці', 'термодинаміку', 'фізика', 'математика',
              'біологія', 'хімія', 'генетика', 'мікроскоп', 'лабораторія', 'експеримент'],
             ['борщ', 'сметана', 'картопля', 'морква', 'суп', 'їжа', 'кулінарний', 'буряк', 'каструля', 'бульйон', 
              'черпак', 'петрушка', 'кроп', 'морква', 'їсти', 'варити', 'страва', 'обід', 'сніданок', 'вечеря',
              'рецепт', 'кухня', 'продукти', 'продукт', 'їстівний', 'смачний', 'солоний', 'солодкий'], 
             0.45),
            
            # 2. Медицина/біологія + технологічний абсурд
            (['пінеальний', 'шишкоподібний', 'імунний', 'імунної', 'нанобот', 'наноботів', 'днк', 'генетичний',
              'вакцина', 'вакцинований', 'імунітет', 'клітина', 'організм', 'біологічний', 'медичний',
              'вірус', 'бактерія', 'антитіло', 'гормон', 'нейрон', 'синапс', 'мозок', 'серце', 'печінка',
              'ліки', 'лікування', 'діагноз', 'симптом', 'хвороба', 'здоров\'я'],
             ['5g', 'супутник', 'старлінк', 'блокчейн', 'гейтса', 'водопровідний', 'вода', 'чип', 'мікрочіп',
              'транслюють', 'частоти', 'гц', 'дестабілізує', 'записувати', 'протокол', 'матриця', 'програмування',
              'WiFi', 'радіо', 'телебачення', 'мобільний', 'телефон', 'сітка', 'покриття', 'антена'], 
             0.5),
            
            # 3. Історія/археологія + фантастика
            (['антарктида', 'атлантида', 'тартарія', 'древній', 'інопланетянин', 'бог', 'пираміда', 'цивілізація',
              'історія', 'археологія', 'наполеон', 'цезар', 'клеопатра', 'македонський', 'римський', 'грецький',
              'середньовіччя', 'античність', 'давнина', 'минуле', 'історик', 'археолог', 'розкопки', 'артефакт',
              'руїни', 'храм', 'палац', 'замок', 'король', 'королева'],
             ['портал', 'вимір', 'тесла', 'голограма', 'резонатор', 'деактивувати', 'код', 'шифр', 'технологія',
              'іншопланетний', 'прибулець', 'нло', 'летюча тарілка', 'паралельний', 'часовий', 'просторовий',
              'телепортація', 'машина часу', 'енергетичний', 'кристал', 'сила', 'поле', 'енергія', 'частота'], 
             0.4),
            
            # 4. Політика/суспільство + окультизм
            (['президент', 'прем\'єр', 'уряд', 'держава', 'політика', 'суспільство', 'народ', 'країна',
              'міністр', 'парламент', 'вибори', 'демократія', 'республіка', 'монархія', 'закон', 'конституція',
              'громадянин', 'права', 'обов\'язки', 'бюджет', 'податки', 'інфраструктура', 'освіта', 'медицина'],
             ['рептилоїд', 'ілюмінат', 'масон', 'таємний', 'оккультний', 'ритуал', 'жертва', 'поклоніння',
              'демон', 'сатана', 'дьявол', 'темний', 'світ', 'паралельний', 'вимір', 'потойбічний',
              'звір', 'антихрист', 'апокаліпсис', 'пророцтво', 'віщування', 'магія', 'чаклунство', 'закляття'], 
             0.42),
            
            # 5. Економіка/фінанси + містицизм
            (['гроші', 'валюта', 'банк', 'економіка', 'фінанси', 'інвестиції', 'ринок', 'бізнес',
              'акція', 'облігація', 'криптовалюта', 'біткоїн', 'етhereum', 'блокчейн', 'nft',
              'прибуток', 'збиток', 'капітал', 'кредит', 'депозит', 'бюджет', 'інфляція', 'дефляція',
              'ВВП', 'ВНП', 'макроекономіка', 'мікроекономіка', 'ринкова', 'планова'],
             ['душа', 'карма', 'астрал', 'енергія', 'вібрація', 'чакра', 'аура', 'рекорнація',
              'потойбічний', 'космічний', 'божественний', 'духовний', 'містичний', 'езотеричний', 'оккультний',
              'священний', 'благодать', 'просвітлення', 'медитація', 'йога', 'дзен', 'буддизм'], 
             0.38),
            
            # 6. Психологія/неврологія + конспірологія
            (['психологія', 'психічний', 'неврологія', 'мозок', 'свідомість', 'підсвідомість', 'когнітивний',
              'емоційний', 'ментальний', 'розум', 'інтелект', 'пам\'ять', 'сприйняття',
              'терапія', 'консультація', 'діагностика', 'лікування', 'здоров\'я', 'хвороба',
              'стрес', 'депресія', 'тривога', 'страх', 'радість', 'любов', 'ненависть'],
             ['контроль', 'зомбування', 'програмування', 'маніпуляція', 'вплив', 'втручання', 'втручатися',
              'чип', 'імплант', 'мікрохвильовий', 'радіохвиля', 'частота', 'сигнал', 'трансляція',
              'промінь', 'випромінювання', 'хвиля', 'енергія', 'поле', 'вплив', 'впливати'], 
             0.43),
            
            # 7. Фізика/хімія + езотерика
            (['фізика', 'хімія', 'біологія', 'атом', 'молекула', 'електрон', 'протон', 'нейтрон',
              'енергія', 'матерія', 'поле', 'хвиля', 'частинка', 'кварк', 'бозон', 'ферміон',
              'реакція', 'сполука', 'елемент', 'періодична таблиця', 'валентність', 'орбіталь',
              'гравітація', 'електромагнетизм', 'ядерна', 'радіоактивність', 'ізотоп'],
             ['чакра', 'аура', 'біополе', 'енергетичний', 'вібраційний', 'духовний', 'космічний',
              'божественний', 'містичний', 'таємний', 'прихований', 'непізнаний', 'заборонений',
              'сакральний', 'магічний', 'чарівний', 'зачарований', 'заклятий', 'освячений'], 
             0.35),
            
            # 8. Астрономія/космос + конспірологія
            (['космос', 'всесвіт', 'галактика', 'зірка', 'планета', 'сатурн', 'юпітер', 'марс',
              'астрономія', 'астрофізика', 'космологія', 'чорна діра', 'нейтронна зірка', 'квазар',
              'метеорит', 'комета', 'астероїд', 'орбіта', 'супутник', 'космонавт', 'ракета',
              'телескоп', 'обсерваторія', 'спостереження', 'дослідження'],
             ['змова', 'приховують', 'нібито', 'насправді', 'правда', 'секрет', 'таємниця', 'прихований',
              'непізнаний', 'іншопланетний', 'прибулець', 'нло', 'контакт', 'послання', 'сигнал',
              'приховування', 'брехня', 'обман', 'фейк', 'маніпуляція', 'дезінформація'], 
             0.4),
            
            # 9. Технології + містицизм
            (['технологія', 'інтернет', 'комп\'ютер', 'смартфон', 'програма', 'софт', 'апарат',
              'пристрій', 'гаджет', 'девайс', 'інновація', 'цифровий', 'віртуальний',
              'алгоритм', 'код', 'програмування', 'розробка', 'інженер', 'дизайн',
              'база даних', 'сервер', 'хмара', 'інтерфейс', 'користувач'],
             ['душа', 'свідомість', 'дух', 'енергія', 'вібрація', 'карма', 'астрал', 'потойбічний',
              'космічний', 'божественний', 'містичний', 'таємний', 'прихований',
              'святий', 'божество', 'ангел', 'демон', 'дух', 'привид', 'фантом'], 
             0.36),
            
            # 10. УНІВЕРСАЛЬНА патерн: будь-яка наука + будь-який абсурд
            (['наука', 'науковий', 'дослідження', 'експеримент', 'теорія', 'гіпотеза', 'метод',
              'факт', 'доказ', 'результат', 'висновок', 'публікація', 'журнал', 'університет',
              'лабораторія', 'інститут', 'академія', 'професор', 'доктор наук', 'кандидат наук',
              'монографія', 'стаття', 'цитування', 'рецензування'],
             ['абсурд', 'нісенітниця', 'бред', 'дурниця', 'вигадка', 'фантазія', 'вигаданий',
              'вигадувати', 'вигадати', 'придуманий', 'неіснуючий', 'вигадати', 'вигаданий',
              'вигадка', 'фантасмагорія', 'сюрреалізм', 'нереальний', 'вигаданий', 'вигадковий'], 
             0.3),
            
            # ============================================================
            # СПЕЦИФІЧНІ КОНФЛІКТИ З ТВОЇХ ПРИКЛАДІВ
            # ============================================================
            
            # 11. Термодинаміка + політика (з твого тесту)
            (['термодинаміка', 'ентропія', 'ізольована система', 'теплова смерть',
              'фізика', 'наука', 'закон', 'теорія', 'формула', 'рівняння'],
             ['політика', 'влада', 'уряд', 'президент', 'вибори', 'демократія',
              'соціальний', 'економічний', 'громадянський', 'суспільний'], 
             0.4),
            
            # 12. Логіка + емоції
            (['логіка', 'раціональний', 'розум', 'інтелект', 'міркування', 'висновок',
              'аргумент', 'доказ', 'обґрунтування', 'послідовність'],
             ['емоції', 'почуття', 'серце', 'інтуїція', 'віра', 'довіра',
              'любов', 'ненависть', 'страх', 'радість', 'сум', 'злість'], 
             0.35),
            
            # 13. Статистика + містика
            (['статистика', 'кореляція', 'регресія', 'вибірка', 'значущість',
              'p-value', 'довірчий інтервал', 'дисперсія', 'середнє', 'медіана',
              'аналіз даних', 'дослідження', 'експеримент', 'методологія'],
             ['містика', 'езотерика', 'духовність', 'карма', 'чакра', 'аура',
              'енергія', 'вібрація', 'космічний', 'божественний', 'сакральний'], 
             0.38),
            
            # 14. Право + беззаконня
            (['право', 'закон', 'конституція', 'суд', 'суддя', 'адвокат',
              'кримінальний кодекс', 'цивільний кодекс', 'адміністративний',
              'законодавство', 'норма', 'правило', 'регламент', 'процедура'],
             ['беззаконня', 'безправия', 'анархія', 'хаос', 'безлад', 'непорядок',
              'самогубство', 'насильство', 'злочин', 'порушення', 'ігнорування'], 
             0.42),
            
            # 15. Економіка + утопізм
            (['економіка', 'ринок', 'капітал', 'прибуток', 'інвестиції', 'бізнес',
              'конкуренція', 'пропозиція', 'попит', 'вартість', 'ціна', 'бюджет',
              'фінанси', 'банк', 'кредит', 'депозит', 'акція', 'облігація'],
             ['утопія', 'рай', 'ідеальний', 'досконалий', 'безкоштовний', 'даром',
              'благодійність', 'подарунок', 'безоплатний', 'безгрошовий', 'комунізм'], 
             0.33),
            
            # 16. Освіта + антиінтелектуалізм
            (['освіта', 'навчання', 'знання', 'університет', 'школа', 'коледж',
              'лекція', 'семінар', 'екзамен', 'залік', 'диплом', 'ступінь',
              'професор', 'викладач', 'студент', 'учень', 'підручник', 'курс'],
             ['глупощі', 'дурниця', 'нісенітниця', 'безглуздя', 'абсурд',
              'антиінтелектуалізм', 'невігластво', 'темнота', 'неосвіченість'], 
             0.36),
            
            # 17. Медицина + шаманство
            (['медицина', 'ліки', 'лікар', 'лікарня', 'клініка', 'діагноз',
              'симптом', 'хвороба', 'здоров\'я', 'профілактика', 'вакцина',
              'антибіотик', 'хірургія', 'терапія', 'реабілітація'],
             ['шаман', 'знахар', 'ворожка', 'ворожіння', 'замовляння', 'заклинання',
              'ритуал', 'обряд', 'магія', 'чаклунство', 'заговор', 'наговір'], 
             0.45),
            
            # 18. Технологія + примітивізм
            (['технологія', 'комп\'ютер', 'смартфон', 'інтернет', 'програма',
              'алгоритм', 'код', 'робот', 'автоматизація', 'цифровий',
              'віртуальний', 'AI', 'штучний інтелект', 'нейромережа'],
             ['примітивний', 'простий', 'елементарний', 'грубий', 'неотесаний',
              'первісний', 'пещерний', 'допотопний', 'архаїчний', 'застарілий'], 
             0.32),
            
            # 19. Наука + релігія
            (['наука', 'дослідження', 'експеримент', 'теорія', 'гіпотеза',
              'метод', 'факт', 'доказ', 'лабораторія', 'університет'],
             ['релігія', 'віра', 'бог', 'молитва', 'храм', 'церква', 'святий',
              'біблія', 'коран', 'тора', 'релігійний', 'духовний', 'священний'], 
             0.37),
            
            # 20. Психологія + детермінізм
            (['психологія', 'свідомість', 'підсвідомість', 'емоції', 'почуття',
              'ментальний', 'когнітивний', 'поведінка', 'мотивація', 'характер'],
             ['детермінізм', 'фаталізм', 'передвизначення', 'доля', 'фатум',
              'незмінний', 'неминучий', 'необхідний', 'обов\'язковий', 'приречений'], 
             0.34)
        ]
        
        # ============================================================
        # ПОКРАЩЕНІ ГРАДІЄНТНІ ШТРАФИ (нижчі пороги)
        # ============================================================
        self.gradient_penalties = [
            {
                'type': 'entropy_gradient',
                'calculate': lambda m: max(0, (m['shannon_entropy'] - 0.5) * 3) if m['signal_markers'] < 2 else 0
            },
            {
                'type': 'complexity_gradient',
                'calculate': lambda m: max(0, (m['complexity'] - 0.5) * 2.5) if m['signal_markers'] < 2 else 0
            },
            {
                'type': 'chaos_signal_ratio',
                'calculate': lambda m: min(0.6, m['chaos_markers'] / max(1, m['signal_markers'] + 1) * 0.4)
            },
            {
                'type': 'academic_dissonance',
                'calculate': lambda m: 0.3 if m['academic_markers'] > 0 and m['chaos_markers'] > 0 else 0
            },
            {
                'type': 'zero_signal_complexity',
                'calculate': lambda m: 0.4 if m['signal_markers'] == 0 and m['complexity'] > 0.5 else 0
            },
            # НОВИЙ: Штраф за контрасти
            {
                'type': 'high_contrast',
                'calculate': lambda m: 0.2 if m['shannon_entropy'] > 0.7 and m['complexity'] > 0.7 and m['signal_markers'] < 1 else 0
            }
        ]

    def calculate_conflict_penalty(self, text):
        """Покращена версія з більш жорсткими штрафами"""
        penalty = 0.0
        text_lower = text.lower()
        found_conflicts = []
        
        for list1, list2, weight in self.conflict_pairs:
            found_in_first = []
            found_in_second = []
            
            for term in list1:
                if term.lower() in text_lower:
                    found_in_first.append(term)
            
            for term in list2:
                if term.lower() in text_lower:
                    found_in_second.append(term)
            
            if found_in_first and found_in_second:
                sentences = re.split(r'[.!?]+', text)
                same_sentence = False
                
                for sentence in sentences:
                    sentence_lower = sentence.lower()
                    has_first_in_sentence = any(term.lower() in sentence_lower for term in found_in_first)
                    has_second_in_sentence = any(term.lower() in sentence_lower for term in found_in_second)
                    
                    if has_first_in_sentence and has_second_in_sentence:
                        same_sentence = True
                        break
                
                if same_sentence:
                    penalty += weight * 1.5  # +50% за те саме речення!
                    found_conflicts.append({
                        'first': found_in_first[:2],
                        'second': found_in_second[:2],
                        'weight': weight * 1.5,
                        'same_sentence': True
                    })
                else:
                    penalty += weight
                    found_conflicts.append({
                        'first': found_in_first[:2],
                        'second': found_in_second[:2],
                        'weight': weight,
                        'same_sentence': False
                    })
        
        # ЖОРСТКІШІ ШТРАФИ ЗА КІЛЬКІСТЬ КОНФЛІКТІВ
        if len(found_conflicts) >= 2:
            penalty += 0.2
        if len(found_conflicts) >= 3:
            penalty += 0.3
        if len(found_conflicts) >= 5:
            penalty += 0.4
        
        return min(penalty, 0.8), found_conflicts  # Максимум 0.8!

    def calculate_contextual_score(self, text, term_counts, metrics):
        """Покращена контекстуальна оцінка з акцентом на абсурд"""
        score = 0.0
        words = text.split()
        word_count = len(words)
        text_lower = text.lower()
        
        # 1. Семантична пустота (жорсткіше)
        if term_counts['signal'] == 0:
            if metrics['complexity'] > 0.5:  # Нижчий поріг!
                score += 0.6
            elif metrics['shannon_entropy'] > 0.6:
                score += 0.5
            else:
                score += 0.3
        
        # 2. Науковий нігілізм (сильніший штраф)
        if term_counts['academic'] > 0:
            # Додатковий штраф якщо академічні терміни використані в абсурдному контексті
            academic_words = ['наука', 'дослідження', 'експеримент', 'теорія', 'факт']
            absurd_words = ['брехня', 'обман', 'фейк', 'вигадка', 'фантазія']
            
            has_academic = any(word in text_lower for word in academic_words)
            has_absurd = any(word in text_lower for word in absurd_words)
            
            if has_academic and has_absurd:
                score += 0.5
            
            if term_counts['chaos'] > 0:
                chaos_ratio = term_counts['chaos'] / max(1, term_counts['academic'])
                if chaos_ratio > 1.0:
                    score += 0.4
                else:
                    score += 0.25
        
        # 3. Політична маніпуляція (ловим більше)
        if any(w in text_lower for w in ['уряд', 'влада', 'президент', 'політика']):
            # Штраф за капс
            caps_words = len([w for w in words if w.isupper() and len(w) > 1])
            if caps_words >= 2:
                score += 0.3
            
            # Штраф за заклики до дій
            action_phrases = ['вийдіть на', 'протестуйте', 'повстаньте', 'бунтуйте']
            if any(phrase in text_lower for phrase in action_phrases):
                score += 0.35
        
        # 4. Логічний абсурд (новий тип)
        # Пошук внутрішніх суперечностей
        contradiction_pairs = [
            (['так', 'згоден', 'підтверджую'], ['ні', 'не згоден', 'заперечую']),
            (['всі', 'кожен', 'завжди'], ['ніхто', 'ніколи', 'жоден']),
            (['правда', 'істина', 'факт'], ['брехня', 'фейк', 'обман']),
            (['логіка', 'розум'], ['емоція', 'серце', 'інтуїція']),
            (['свобода', 'незалежність'], ['рабство', 'залежність', 'обмеження'])
        ]
        
        for pos_list, neg_list in contradiction_pairs:
            has_pos = any(term in text_lower for term in pos_list)
            has_neg = any(term in text_lower for term in neg_list)
            if has_pos and has_neg:
                # Перевіряємо, чи в одному реченні
                sentences = re.split(r'[.!?]+', text)
                for sentence in sentences:
                    sentence_lower = sentence.lower()
                    pos_in_sentence = any(term in sentence_lower for term in pos_list)
                    neg_in_sentence = any(term in sentence_lower for term in neg_list)
                    if pos_in_sentence and neg_in_sentence:
                        score += 0.4
                        break
                else:
                    score += 0.2
        
        # 5. Структурний абсурд (новий)
        # Штраф за використання наукових термінів для обґрунтування нісенітниць
        science_to_nonsense = [
            (['квантовий', 'ентропія', 'нейтрино'], ['любов', 'ненависть', 'щастя']),
            (['математика', 'статистика', 'алгоритм'], ['душа', 'карма', 'судьба']),
            (['фізика', 'хімія', 'біологія'], ['магія', 'чари', 'закляття'])
        ]
        
        for science_list, nonsense_list in science_to_nonsense:
            has_science = any(term in text_lower for term in science_list)
            has_nonsense = any(term in text_lower for term in nonsense_list)
            if has_science and has_nonsense:
                score += 0.45
        
        return min(score, 0.8)

    def analyze(self, text):
        """Оновлений метод з акцентом на конфлікти"""
        if not text or len(text.strip()) < 20:
            return {'error': 'Text too short'}
        
        words = text.split()
        word_count = len(words)
        
        # 1. Детекція паттернів
        detected_patterns = self.detect_patterns(text)
        
        # 2. Підрахунок термінів
        term_counts = self.count_terms(text)
        
        # 3. Ентропія та складність
        shannon_entropy = self._calculate_shannon_entropy(text)
        complexity = self._calculate_complexity(text)
        
        base_metrics = {
            'shannon_entropy': shannon_entropy,
            'complexity': complexity,
            'signal_markers': term_counts['signal'],
            'chaos_markers': term_counts['chaos'],
            'academic_markers': term_counts['academic'],
            'word_count': word_count
        }
        
        # 4. Розрахунок штрафів (ГОЛОВНА ЗМІНА - більше ваги конфліктам!)
        gradient_penalty = self.calculate_gradient_penalties(base_metrics)
        conflict_penalty, conflict_details = self.calculate_conflict_penalty(text)
        contextual_score = self.calculate_contextual_score(text, term_counts, base_metrics)
        
        # 5. Базова оцінка (70% ваги - конфлікти та контекст!)
        base_score = (
            shannon_entropy * 0.08 +           # Менше ваги
            complexity * 0.05 +                # Менше ваги
            (term_counts['chaos'] / max(1, word_count)) * 0.20 +
            contextual_score * 0.35 +          # Більше ваги!
            gradient_penalty * 0.12 +
            conflict_penalty * 0.40            # НАЙБІЛЬША ВАГА!
        )
        
        # 6. Бонуси за паттерни
        for pattern in detected_patterns:
            base_score += pattern['score_boost']
        
        # 7. Академічний захист (послаблюємо для абсурдних текстів)
        academic_absurd = False
        if conflict_penalty > 0.3:
            academic_absurd = True
        
        if term_counts['academic'] >= 2 and term_counts['signal'] >= 2 and not academic_absurd:
            if term_counts['chaos'] == 0:
                base_score *= 0.4
            elif term_counts['chaos'] <= 1:
                base_score *= 0.6
            else:
                base_score *= 0.8
        elif term_counts['academic'] >= 1 and term_counts['signal'] >= 1 and not academic_absurd:
            base_score *= 0.7
        
        # 8. Критичні підвищення (частіше і жорсткіше)
        if conflict_penalty > 0.2:
            base_score = max(base_score, 0.45)
        if conflict_penalty > 0.3:
            base_score = max(base_score, 0.55)
        if conflict_penalty > 0.4:
            base_score = max(base_score, 0.65)
        if conflict_penalty > 0.5:
            base_score = max(base_score, 0.75)
        
        if contextual_score > 0.3:
            base_score = max(base_score, 0.5)
        
        final_score = min(0.99, max(0.0, base_score))
        
        # 9. Розрахунок індексів
        signal = term_counts['signal']
        chaos = term_counts['chaos']
        context = contextual_score
        conflict = conflict_penalty
        final = final_score

        if signal >= 3 and chaos == 0:
            chaos_index = 0.0
        elif chaos > 0:
            chaos_index = final * 100 * (1 + chaos * 0.8) * (1 + max(0, context - 0.2) * 2.0) / (1 + signal * 0.5)
        else:
            chaos_index = final * 100 * (1 - conflict * 0.9) * (1 - context * 0.5) / (1 + signal * 0.8)
        chaos_index = round(chaos_index, 2)

        influence_index = final * 100 * (1 + final) * (1 + conflict * 0.5)
        influence_index = round(influence_index, 2)

        sanity_penalty = round(conflict_penalty + max(0, gradient_penalty - 0.2), 3)

        noise_marker_count = term_counts.get('noise', 0)
        signal_ratio = 0 if noise_marker_count == 0 else round(noise_marker_count / max(1, signal), 2)
        
        # 10. Вердикт (ЖОРСТКІШІ ПОРОГИ!)
        if detected_patterns:
            main_pattern = detected_patterns[0]
            status = 'CRITICAL' if final_score > 0.5 else 'WARNING'
            verdict = main_pattern['verdict']
            explanation = main_pattern['explanation']
        elif final_score > 0.6:
            status = 'CRITICAL'
            if conflict_penalty > 0.4:
                verdict = 'КРИТИЧНИЙ ЛОГІЧНИЙ КОНФЛІКТ'
                explanation = 'Текст містить несумісні поняття високого рівня'
            elif contextual_score > 0.4:
                verdict = 'ВИСОКИЙ РІВЕНЬ СЕМАНТИЧНОГО ХАОСУ'
                explanation = 'Текст демонструє критичний рівень семантичної несумісності'
            else:
                verdict = 'СЕМАНТИЧНА ПУСТОТА'
                explanation = 'Високий рівень абстракції при відсутності конкретного змісту'
        elif final_score > 0.4:
            status = 'WARNING'
            verdict = 'ПІДОЗРІЛА СЕМАНТИЧНА СТРУКТУРА'
            explanation = 'Текст містить ознаки семантичних несумісностей'
        elif final_score > 0.2:
            status = 'ACCEPTABLE'
            verdict = 'ПРИЙНЯТНА СТРУКТУРОВАНА ІНФОРМАЦІЯ'
            explanation = 'Текст відповідає нормам логічної сумісності'
        elif final_score > 0.05:
            status = 'TRUSTED'
            verdict = 'СТАБІЛЬНИЙ ЛОГІЧНИЙ СИГНАЛ'
            explanation = 'Текст демонструє високу логічну цілісність'
        else:
            status = 'VERIFIED'
            verdict = 'ВЕРИФІКОВАНИЙ АКАДЕМІЧНИЙ СИГНАЛ'
            explanation = 'Текст демонструє ідеальну логічну цілісність'
        
        # 11. Деталі
        detail_explanations = []
        if gradient_penalty > 0.05:
            detail_explanations.append(f"Градієнт: {gradient_penalty:.2f}")
        if conflict_penalty > 0.1:
            detail_explanations.append(f"Конфлікти: {conflict_penalty:.2f}")
        if contextual_score > 0.15:
            detail_explanations.append(f"Контекст: {contextual_score:.2f}")
        
        if detail_explanations:
            explanation += " | " + " + ".join(detail_explanations)
        
        # 12. Конфліктні пари
        if conflict_details:
            conflict_pairs = []
            for conflict in conflict_details[:3]:  # Перші 3 конфлікти
                first_terms = ', '.join(conflict['first'][:2])
                second_terms = ', '.join(conflict['second'][:2])
                conflict_pairs.append(f"{first_terms} vs {second_terms}")
            
            if conflict_pairs:
                explanation += f" | Конфлікти: {'; '.join(conflict_pairs)}"
        
        return {
            'entropy': round(final_score, 3),
            'status': status,
            'verdict': verdict,
            'language': 'UK',
            'explanation': explanation,
            'diagnostics': {
                'shannon_entropy': round(shannon_entropy, 3),
                'complexity': round(complexity, 3),
                'contextual_score': round(contextual_score, 3),
                'gradient_penalty': round(gradient_penalty, 3),
                'conflict_penalty': round(conflict_penalty, 3),
                'word_count': word_count,
                'char_count': len(text),
                'academic_markers': term_counts['academic'],
                'chaos_markers': term_counts['chaos'],
                'signal_markers': term_counts['signal'],
                'noise_markers': term_counts.get('noise', 0),
                'pattern_count': len(detected_patterns),
                'shout_factor': len([w for w in words if w.isupper() and len(w) > 2]) / max(1, word_count),
                'number_density': len(re.findall(r'\d+', text)) / max(1, word_count),
                'signal_ratio': signal_ratio,
                'chaos_index': chaos_index,
                'influence_index': influence_index,
                'sanity_penalty': sanity_penalty,
                'conflict_count': len(conflict_details),
                'conflict_details': conflict_details[:5]
            }
        }

    # Інші методи залишаються як було
    def _calculate_shannon_entropy(self, text): ...
    def _calculate_complexity(self, text): ...
    def count_terms(self, text): ...
    def calculate_gradient_penalties(self, metrics): ...
    def detect_patterns(self, text): ...
