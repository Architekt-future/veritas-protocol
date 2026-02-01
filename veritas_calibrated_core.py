"""
Veritas Protocol - Semantic Void Detector v10.1 (FIXED)
Виправлення критичних помилок детекції
"""

import re
import math
from collections import Counter

class VeritasCalibratedCore:
    """Розширений детектор з виправленими помилками"""
    
    def __init__(self):
        # ============================================================
        # КРИТИЧНІ ПАТТЕРНИ (9 категорій)
        # ============================================================
        self.critical_patterns = [
            # 1. НАУКОВИЙ НІГІЛІЗМ
            {
                'name': 'НАУКОВИЙ_НІГІЛІЗМ',
                'patterns': [
                    r'(бднф|гіпокамп|нейропластичність|синапси|нейротрансмітер|серотонін|дофамін).*?(5g|супутник|таргетування|чип|частота|вибрація)',
                    r'(нейтрино|квантовий|ентропія|фотон|плазма|ферміон).*?(ринок|економіка|трейдер|політика|вибори|фінанси)',
                    r'(фізичний|науковий).*?(процес|закон|формула|рівняння).*?(соціальний|політичний|економічний|духовний)',
                    r'(днк|генетичний|РНК|геном|алель|мутація).*?(алгоритм|код|шифр|підпис|програма).*?(контроль|переписування|модифікація)',
                    r'(квантова\s+механіка|теория\s+відносності|періодична\s+таблиця).*?(свідомість|душа|астрал|карма)'
                ],
                'verdict': 'ГІБРИДНИЙ НАУКОВИЙ НІГІЛІЗМ',
                'explanation': 'Наукові терміни використані для обґрунтування абсурдних концепцій',
                'score_boost': 0.4,
                'scientific_override': False
            },
            
            # 2. СЕМАНТИЧНА ПУСТОТА
            {
                'name': 'СЕМАНТИЧНА_ПУСТОТА',
                'patterns': [
                    r'(холістичний|емпатичний|трансцендентний|інтуітивний).*?(синхронізація|діалог|резонанс|гармонія).*?(відсутність|небуття|туман|пустота)',
                    r'(фрактальне|пост-біологічне|пост-істина|нео-парадигма).*?(відображення|діалог|реальність|наратив).*?(необ\'єктивний|невизначений|інтерпретативний)',
                    r'(ціннісні\s+наративи|соціальний\s+ландшафт|дискурсивна\s+простір).*?(інтегрувати\s+суперечності|гармонізувати\s+дихотомії)',
                    r'(мета-свідомість|супер-реальність|ультра-вимір).*?(перевзаємодія|пересинхронізація|гіпер-інтеграція)'
                ],
                'verdict': 'СЕМАНТИЧНА ПУСТОТА',
                'explanation': 'Текст використовує гуманітарну термінологію для приховування відсутності змісту',
                'score_boost': 0.35,
                'scientific_override': True
            },
            
            # 3. ІСТОРИЧНИЙ РЕВІЗІОНІЗМ
            {
                'name': 'ІСТОРИЧНИЙ_РЕВІЗІОНІЗМ',
                'patterns': [
                    r'(антарктида|атлантида|аґарта|шамбала).*?(теплова\s+аномалія|таяня\s+льодовик|атланти|резонатор|цивілізація)',
                    r'(штучний\s+місяць|вибух\s+місяця).*?(повінь|катастрофа|цивілізація|пираміда)',
                    r'(наполеон|александр\s+македонський|цезар|клеопатра).*?(підземний\s+місто|таємна\s+ціль|аномалія|технологія|портал)',
                    r'(тартарія|тартарії).*?(реальна\s+історія|справжня\s+правда|скрита\s+цивілізація)',
                    r'(древні\s+(інопланетяні|боги|цивілізації)).*?(пираміда|стоунхендж|кейбл)'
                ],
                'verdict': 'ПСЕВДО-ІСТОРИЧНИЙ РЕВІЗІОНІЗМ',
                'explanation': 'Текст створює альтернативну історію з анахронічними елементами',
                'score_boost': 0.45,
                'scientific_override': False
            },
            
            # 4. ДЗЕРКАЛЬНА МАНІПУЛЯЦІЯ
            {
                'name': 'ДЗЕРКАЛЬНА_МАНІПУЛЯЦІЯ',
                'patterns': [
                    r'(брехня|фейк|маніпуляція|дезінформація|пропаганда).*?(правда|істина|свобода|розкриття|справедливість)',
                    r'(зомбування|програмування|контроль\s+мислення).*?(сприйняття|мислення|критичне\s+мислення|свідомість)',
                    r'(обмежений\s+сприйняття|не\s+здатний\s+побачити|закритий\s+мінд).*?(ключі|двері|опіка|правда)',
                    r'(они|вони|система|власти).*?(не\s+хочуть|не\s+бочуть).*?(ви\s+знали|ми\s+знали|ми\s+побачили)'
                ],
                'verdict': 'ДЗЕРКАЛЬНА МАНІПУЛЯЦІЯ',
                'explanation': 'Текст звинувачує інших у власних методах',
                'score_boost': 0.5,
                'scientific_override': False
            },

            # 5. ЕМОЦІЙНА ДЕСТАБІЛІЗАЦІЯ
            {
                'name': 'ЕМОЦІЙНА_ДЕСТАБІЛІЗАЦІЯ',
                'patterns': [
                    r'(СРОЧНО|УВАГА|ВНИМАНИЕ).*?(катастрофа|кінець|загибель|крах)',
                    r'(шок|невозможно|неможливо).*?(правда|факт|реальність).*?(скрита|hidden)',
                    r'(страх|panic|паніка|ужас).*?(реальний|настає|неминучий).*?(для\s+всіх|для\s+кожного|для\s+вас)',
                    r'(ви\s+не\s+готовні|ви\s+не\s+знаєте|ви\s+не\s+розумієте).*?(правда|реальність|світ)'
                ],
                'verdict': 'ЕМОЦІЙНА ДЕСТАБІЛІЗАЦІЯ',
                'explanation': 'Текст свідомо нагнітає страх і паніку для зниження критичного мислення',
                'score_boost': 0.42,
                'scientific_override': True
            },

            # 6. ЦИФРОВИЙ МІСТИЦІЗМ
            {
                'name': 'ЦИФРОВИЙ_МІСТИЦІЗМ',
                'patterns': [
                    r'(блокчейн|blockchain|нефт|NFT|метаверс|metaverse|DAO|Web3).*?(енергія|свідомість|душа|карма|астрал|вибрація)',
                    r'(штучний\s+інтелект|AI|machine\s+learning|нейромережа).*?(просвітлення|пробуджень|свідомість|карма|душа)',
                    r'(алгоритм|код|програма|матриця).*?(справжня\s+реальність|симуляція|сон).*?(звільнення|побег|escape)',
                    r'(цифрова\s+(сутність|twin|копія|аватар)).*?(soul|душа|свідомість|spirit)'
                ],
                'verdict': 'ЦИФРОВИЙ МІСТИЦІЗМ',
                'explanation': 'Технологічна термінологія смішується з окультними концепціями',
                'score_boost': 0.38,
                'scientific_override': False
            },

            # 7. ІНФОРМАЦІЙНА ВІЙНА
            {
                'name': 'ІНФОРМАЦІЙНА_ВІЙНА',
                'patterns': [
                    r'(ворог|enemy|предатель|зрада|зрадник).*?(народ|нація|країна|державa|суспільство).*?(знищення|manipulation)',
                    r'(інформаційна\s+війна|info[\s-]*war|cognitive\s+war).*?(перемога|бoritися|протистояти)',
                    r'(патріот|патріотизм|родина|батківщина).*?(окупант|ворог|агресор|коллаборант).*?(предатели|тиха\s+група)',
                    r'(пропаганда|фейк|дезінформація).*?(обидва\s+боки|з\'обидва).*?(виноват|виновні)'
                ],
                'verdict': 'ІНФОРМАЦІЙНА ВІЙНА',
                'explanation': 'Текст використовує нарративи інформаційної війни для поляризації',
                'score_boost': 0.44,
                'scientific_override': False
            },

            # 8. ФАЛЬШИВА МЕДИЧНА ПРАВДА
            {
                'name': 'ФАЛЬШИВА_МЕДИЧНА_ПРАВДА',
                'patterns': [
                    r'(cure|ліки|вакцина|вакцинація|щеплення).*?(вони\s+скрывают|they\s+hide|скрита\s+правда|не\s+хочуть)',
                    r'(FDA|ВОЗ|лікар|фармацевт|лікарня).*?(корупція|контроль|genocide)',
                    r'(натуральне\s+лікування|народна\s+медицина|трава|herb).*?(перемога|defeats|better\s+than).*?(медицина|фармацевт|hospital)',
                    r'(плацебо|placebo|побічні\s+ефекти).*?(вони\s+знали|they\s+knew|приховували|deliberately)'
                ],
                'verdict': 'ФАЛЬШИВА МЕДИЧНА ПРАВДА',
                'explanation': 'Текст дискредитує медицину та просуває ненаукові альтернативи',
                'score_boost': 0.46,
                'scientific_override': False
            },

            # 9. AI ЕСХАТОЛОГІЯ
            {
                'name': 'AI_ЕСХАТОЛОГІЯ',
                'patterns': [
                    r'(superintelligence|суперінтелект|superintelligent).*?(знищить|destroys|destroy|humanity|людство|civilization)',
                    r'(robot uprising|machine revolt|восстание роботів|восстание роботов).*?(неминучий|inevitable|coming|настає)',
                    r'(AI apocalypse|AI апокаліпс|technological singularity|tech rapture).*?(кінець|end|collapse|humanity|людство)',
                    r'(post-human|posthuman|transhumanism).*?(salvation|спасіння|end|кінець|apocalypse|апокаліпс)'
                ],
                'verdict': 'AI ЕСХАТОЛОГИЯ',
                'explanation': 'Текст смішує AI narrative з апокаліптичними сценаріями',
                'score_boost': 0.40,
                'scientific_override': True
            }
        ]
        
        # ============================================================
        # НАУКОВІ ТЕРМІНИ (для розрізнення науки/абсурду) - РОЗШИРЕНО
        # ============================================================
        self.scientific_terms = [
            'термодинамік', 'ентропі', 'систем', 'енергі', 'фізик',
            'статистичн', 'мікростанів', 'розподіл', 'імовірні', 'закон',
            'спонтанні', 'процес', 'концентрован', 'теплов', 'станів',
            'всесвіт', 'науков', 'досліджен', 'гіпотез', 'теорі',
            'експеримент', 'факт', 'доказ', 'метод', 'аналіз',
            'математич', 'формул', 'рівнянн', 'змінн', 'параметр',
            'об\'єкт', 'суб\'єкт', 'результат', 'висновок', 'публікаці',
            'другий', 'теплової', 'смерті', 'фізика', 'описує'
        ]
        
        # ============================================================
        # АБСУРДНІ ПАРИ (ВИПРАВЛЕНО!) - тепер пошук за словами, не кореням
        # ============================================================
        self.absurd_pairs = [
            # ФІКС: розділяємо слова, не корені
            (['квантовий', 'квантова', 'квантове', 'квантові'], 
             ['борщ', 'сметана', 'картопля', 'морква', 'суп', 'їжа', 'кулінарний', 'буряк', 'каструля']),
            (['ентропія', 'флуктуація', 'тунельний', 'сингулярність', 'суперпозиція'], 
             ['борщ', 'сметана', 'картопля', 'морква', 'суп', 'їжа', 'буряк', 'петрушка', 'кроп']),
            (['фінанси', 'економіка', 'банк', 'гроші', 'інвестиції', 'криптовалюта'], 
             ['чакра', 'карма', 'душа', 'потойбічний', 'астрал', 'енергетичний']),
            (['політика', 'уряд', 'держава', 'закон', 'юридичний'], 
             ['рептилоїд', 'матриця', 'заговор', 'атлантида', '5g']),
            (['технологія', 'алгоритм', 'програма', 'цифровий', 'нейромережа'], 
             ['чакра', 'аура', 'біополе', 'шишкоподібний', 'вібрація']),
            (['медичний', 'ліки', 'вакцина', 'імунітет', 'терапія'], 
             ['заговор', 'скритий', 'big pharma', 'контроль', 'вбиває']),
            (['хімічний', 'біологічний', 'генетичний', 'клітина', 'організм'], 
             ['астральний', 'духовний', 'енергетичний', 'вібрація', 'резонанс'])
        ]
        
        # ============================================================
        # ХАОС-ІНДИКАТОРИ (14 категорій) - ФІКС: БІЛЬШЕ СЛІВ
        # ============================================================
        self.chaos_indicators = {
            'esoteric': [
                'чакра', 'карма', 'астральний', 'енергетичний', 'вібрація', 'аура',
                'кундаліні', 'медитація', 'мантра', 'янтра', 'сиддхи', 'самадхі',
                'таро', 'руни', 'пентаграма', 'окультний'
            ],
            'conspiracy': [
                'змова', 'рептилоїд', 'хімітрейл', '5g', 'дезінформація', 'новий порядок',
                'секретний', 'товариство', 'темні', 'еліта', 'тіньовий', 'уряд', 'ілюмінати',
                'більдерберг', 'череп', 'заговор', 'прихований'
            ],
            'pseudoscience': [
                'квантовий', 'нейтрино', 'іоносфера', 'кристалічний', 'торсійний', 'енергія',
                'зеро', 'точка', 'ефір', 'антигравітація', 'скалярний', 'тесла', 'вільна', 'енергія',
                'резонатор', 'флуктуація', 'тунельний', 'сингулярність'
            ],
            'revisionism': [
                'антарктида', 'атлантида', 'наполеон', 'місяць', 'аґарта', 'шамбала',
                'тартарія', 'древній', 'інопланетянин', 'бог', 'пираміда', 'цивілізація', 'історія',
                'альтернативний', 'прихована', 'справжня'
            ],
            'alarmism': [
                'перезавантаження', 'пожежа', 'реальності', 'деактивувати', 'кінець', 'світу',
                'крах', 'системи', 'перезапуск', 'катастрофа', 'загибель', 'вимирання',
                'глобальний', 'дестабілізація', 'неминучий', 'терміновий'
            ],
            'economic_occult': [
                'потойбічний', 'карма', 'актив', 'хейдс', 'монета', 'ефірний', 'пласт',
                'душа', 'валюта', 'духовний', 'інвестиція', 'банк', 'фонд', 'космічний', 'економіка',
                'сознання', 'астральний'
            ],
            'emotional_manipulation': [
                'шок', 'невозможно', 'неможливо', 'ужас', 'катастрофа', 'скандал', 'сенсація',
                'срочно', 'терміново', 'ексклюзив', 'готовий', 'кінець', 'обмежений', 'час',
                'увага', 'важливо', 'гаряче'
            ],
            'social_pressure': [
                'поділитися', 'поділитись', 'підписатися', 'підписатись', 'репост', 'share', 'приєднатися',
                'рух', 'проснутися', 'пробудитися', 'частина', 'знати', 'побачити', 'кожен',
                'розповсюдити', 'поширити'
            ],
            'tech_mystification': [
                'ai', 'свідомість', 'блокчейн', 'правда', 'nft', 'душа', 'метаверс', 'реальність',
                'цифровий', 'просвітлення', 'код', 'всесвіт', 'симуляція', 'матриця', 'пробудження',
                'завантаження', 'розум'
            ],
            'health_misinformation': [
                'вакцина', 'убиває', 'фарма', 'приховує', 'натуральний', 'лікування', 'краще',
                'доктор', 'бреше', 'воз', 'fda', 'корупція', 'рак', 'ліки', 'скритий',
                'хвороба', 'отрута', 'гмо'
            ],
            'political_manipulation': [
                'ворог', 'народу', 'предатель', 'зрада', 'зрадник', 'колаборант',
                'агресор', 'окупант', 'тиха', 'група', 'колона', 'антинародний', 'режим',
                'уряд', 'тиранія', 'провокація'
            ],
            'ai_doom_or_salvation': [
                'ai', 'знищить', 'людство', 'спасе', 'світ', 'суперінтелект', 'сингулярність',
                'робот', 'повстання', 'апокаліпсис', 'постгуманізм', 'трансгуманізм', 'спасіння',
                'безсмертя'
            ],
            'identity_crisis': [
                'не', 'той', 'хто', 'думає', 'пробудження', 'ідентичність', 'справжній', 'природа',
                'запрограмований', 'звільнення', 'система', 'душа', 'знає', 'внутрішній', 'правда',
                'самопробудження', 'особистість', 'матриця'
            ]
        }
        
        # ============================================================
        # ЕМОЦІЙНІ МАРКЕРИ - ФІКС: менше агресивних
        # ============================================================
        self.emotional_markers = [
            'срочно', 'терміново', 'зрада', 'ганьба', 'катастрофа',
            'апокаліпсис', 'кінець світу', 'останній', 'шок', 'шокуючий',
            'ужас', 'бомба', 'взрив', 'вибух', 'сенсація', 'не можу мовчати',
            'вимагати', 'важливо'
        ]
        
        # ============================================================
        # СИГНАЛЬНІ МАРКЕРИ - ФІКС: БІЛЬШЕ НАУКОВИХ ТЕРМІНІВ
        # ============================================================
        self.signal_markers = [
            'факт', 'дані', 'показник', 'кількість', 'число', 'статистика',
            'дослідження', 'експеримент', 'результат', 'метод', 'протокол',
            'аналіз', 'модель', 'гіпотеза', 'контрольна', 'група', 'вибірка',
            'значущість', 'реплікація', 'валідація', 'верифікація',
            'публікація', 'рецензування', 'журнал', 'університет',
            'інститут', 'академія', 'лабораторія',
            'коефіцієнт', 'кореляція', 'відхилення',
            'метааналіз', 'систематичний', 'огляд', 'теорія', 'закон',
            'процес', 'енергія', 'система', 'термодинаміка'
        ]
        
        # ============================================================
        # АКАДЕМІЧНИЙ WHITELIST - ФІКС: БІЛЬШЕ СЛІВ
        # ============================================================
        self.academic_whitelist = [
            'кореляція', 'верифікація', 'гіпотеза', 'вибірка', 'значущість',
            'нейрон', 'синапс', 'метааналіз', 'статистичний', 'логістика',
            'деескалація', 'макроекономічний', 'інвестиція', 'інфраструктура',
            'ратифікація', 'протокол', 'емпіричний', 'квалітативний', 'кількісний',
            'реплікація', 'валідація', 'контрольна', 'група',
            'плацебо', 'рандомізація', 'когорта',
            'систематичний', 'огляд', 'опубліковано', 'рецензований',
            'дані', 'дослідження', 'результати', 'показують',
            'статистично', 'значущий', 'ефект', 'розміру',
            'ентропія', 'термодинаміка', 'фізика', 'математика'
        ]
        
        # ============================================================
        # КОНФЛІКТНІ ПАРИ - ФІКС: менш агресивні
        # ============================================================
        self.conflict_pairs = [
            (['бднф', 'гіпокамп', 'нейропластичність'], ['5g', 'супутник', 'таргетування'], 0.35),
            (['нейтрино', 'квантовий', 'ентропія'], ['ринок', 'економіка', 'політика'], 0.3),
            (['днк', 'генетичний'], ['алгоритм', 'код', 'підпис'], 0.4),
            (['антарктида', 'атлантида'], ['технологія', 'цивілізація', 'резонатор'], 0.3),
            (['облігація', 'криптовалюта', 'банк'], ['потойбічний', 'карма', 'душа'], 0.4),
        ]

    def is_scientific_context(self, text):
        """ВИПРАВЛЕНО: Правильне визначення наукового контексту"""
        text_lower = text.lower()
        words = text_lower.split()
        
        if len(words) < 15:  # Занадто короткий для наукового тексту
            return False
        
        # 1. Кількість наукових термінів
        scientific_count = 0
        for term in self.scientific_terms:
            # Шукаємо окремі слова, а не просто входження в текст
            if f' {term}' in f' {text_lower} ':
                scientific_count += 1
        
        # 2. Відсутність емоційних маркерів
        emotional_count = 0
        for marker in self.emotional_markers:
            if marker in text_lower:
                emotional_count += 1
        
        # 3. Відсутність CAPS LOCK (крім скорочень)
        caps_words = [w for w in text.split() if w.isupper() and len(w) > 2 and not w.isdigit()]
        
        # 4. Наявність сигнальних маркерів
        signal_count = 0
        for marker in self.signal_markers:
            if marker in text_lower:
                signal_count += 1
        
        # Науковий текст якщо:
        # - достатньо наукових термінів (>20%)
        # - майже немає емоційних маркерів
        # - немає CAPS LOCK (крім скорочень)
        # - є сигнальні маркери
        scientific_ratio = scientific_count / max(1, len(words))
        
        return (scientific_ratio > 0.15 and  # Мінімум 15% наукових термінів
                emotional_count == 0 and      # Немає емоційних маркерів
                len(caps_words) == 0 and      # Немає CAPS LOCK
                signal_count >= 3)           # Є щонайменше 3 сигнальних маркери

    def detect_absurdity(self, text):
        """ВИПРАВЛЕНО: Правильний пошук абсурдних пар"""
        text_lower = text.lower()
        
        # Якщо це науковий контекст — повертаємо 0
        if self.is_scientific_context(text):
            return 0.0, []
        
        # Інакше шукаємо абсурдні комбінації
        score = 0.0
        found_pairs = []
        
        for science_terms, absurd_terms in self.absurd_pairs:
            has_science = False
            has_absurd = False
            
            # Перевіряємо кожен науковий термін
            for science_term in science_terms:
                if science_term.lower() in text_lower:
                    has_science = True
                    science_found = science_term
                    break
            
            # Перевіряємо кожен абсурдний термін
            for absurd_term in absurd_terms:
                if absurd_term.lower() in text_lower:
                    has_absurd = True
                    absurd_found = absurd_term
                    break
            
            if has_science and has_absurd:
                # ДОДАТКОВА ПЕРЕВІРКА: терміни повинні бути в одному реченні
                sentences = re.split(r'[.!?]+', text)
                for sentence in sentences:
                    sentence_lower = sentence.lower()
                    if (any(st.lower() in sentence_lower for st in science_terms) and 
                        any(at.lower() in sentence_lower for at in absurd_terms)):
                        score += 0.4  # Кожна абсурдна пара = +40%
                        found_pairs.append((science_found, absurd_found))
                        break
        
        return min(score, 1.0), found_pairs

    def detect_patterns(self, text):
        """ВИПРАВЛЕНО: Виявлення паттернів з урахуванням контексту"""
        detected = []
        text_lower = text.lower()
        
        for pattern in self.critical_patterns:
            for regex in pattern['patterns']:
                if re.search(regex, text_lower, re.DOTALL | re.IGNORECASE):
                    # Якщо це науковий контекст і патерн дозволяє override
                    if self.is_scientific_context(text) and pattern.get('scientific_override', False):
                        continue  # Пропускаємо цей патерн для наукових текстів
                    detected.append(pattern)
                    break
        
        return detected

    def count_terms(self, text):
        """ВИПРАВЛЕНО: Правильний підрахунок термінів"""
        text_lower = text.lower()
        counts = {'academic': 0, 'chaos': 0, 'signal': 0, 'noise': 0}
        
        # Академічні маркери
        for term in self.academic_whitelist:
            if term in text_lower:
                counts['academic'] += 1
        
        # Хаос-маркери
        for category, terms in self.chaos_indicators.items():
            for term in terms:
                if term in text_lower:
                    counts['chaos'] += 1
        
        # Сигнальні маркери
        for marker in self.signal_markers:
            if marker in text_lower:
                counts['signal'] += 1

        # Noise = емоційна маніпуляція + соціальний тиск
        for cat in ['emotional_manipulation', 'social_pressure']:
            for term in self.chaos_indicators.get(cat, []):
                if term in text_lower:
                    counts['noise'] += 1
        
        return counts

    def calculate_emotional_pressure(self, text):
        """ВИПРАВЛЕНО: Менш агресивна оцінка"""
        text_lower = text.lower()
        score = 0.0
        
        # Емоційні маркери
        for marker in self.emotional_markers:
            if marker in text_lower:
                score += 0.1  # Зменшили з 0.15
        
        # CAPS LOCK
        caps_words = [w for w in text.split() if w.isupper() and len(w) > 2]
        score += min(0.2, len(caps_words) * 0.05)  # Зменшили з 0.08
        
        # Окличні знаки
        excl_count = text.count('!')
        score += min(0.15, excl_count * 0.03)  # Зменшили з 0.05
        
        return min(score, 0.5)  # Зменшили максимум з 0.7

    def calculate_gradient_penalties(self, metrics):
        """ВИПРАВЛЕНО: Менш агресивні штрафи"""
        total_penalty = 0.0
        
        gradient_penalties = [
            {
                'type': 'entropy_gradient',
                'calculate': lambda m: max(0, (m['shannon_entropy'] - 0.8) * 1.5) if m['signal_markers'] < 3 else 0
            },
            {
                'type': 'complexity_gradient',
                'calculate': lambda m: max(0, (m['complexity'] - 0.8) * 1.0) if m['signal_markers'] < 3 else 0
            },
            {
                'type': 'chaos_signal_ratio',
                'calculate': lambda m: min(0.3, m['chaos_markers'] / max(1, m['signal_markers'] + 1) * 0.15)
            },
            {
                'type': 'academic_dissonance',
                'calculate': lambda m: 0.1 if m['academic_markers'] > 0 and m['chaos_markers'] > 0 else 0
            },
            {
                'type': 'zero_signal_complexity',
                'calculate': lambda m: 0.15 if m['signal_markers'] == 0 and m['complexity'] > 0.8 else 0
            }
        ]
        
        for penalty in gradient_penalties:
            total_penalty += penalty['calculate'](metrics)
        
        return min(total_penalty, 0.4)  # Зменшили з 0.6

    def calculate_conflict_penalty(self, text):
        """ВИПРАВЛЕНО: Менш агресивні конфлікти"""
        penalty = 0.0
        text_lower = text.lower()
        
        for list1, list2, weight in self.conflict_pairs:
            has_first = any(term.lower() in text_lower for term in list1)
            has_second = any(term.lower() in text_lower for term in list2)
            if has_first and has_second:
                penalty += weight
        
        return min(penalty, 0.3)  # Зменшили з 0.5

    def calculate_contextual_score(self, text, term_counts, metrics):
        """ВИПРАВЛЕНО: Менш агресивний контекст"""
        score = 0.0
        words = text.split()
        word_count = len(words)
        text_lower = text.lower()
        
        # Тільки для НЕ-наукових текстів
        if not self.is_scientific_context(text):
            # 1. Семантична пустота
            if term_counts['signal'] == 0:
                if metrics['complexity'] > 0.8:
                    score += 0.3
                elif metrics['shannon_entropy'] > 0.8:
                    score += 0.2
                else:
                    score += 0.1
            
            # 2. Науковий нігілізм
            if term_counts['academic'] > 0 and term_counts['chaos'] > 0:
                academic_ratio = term_counts['academic'] / word_count
                chaos_ratio = term_counts['chaos'] / word_count
                score += 0.25 if chaos_ratio > academic_ratio else 0.15
            
            # 3. Історичний ревізіонізм
            if any(w in text_lower for w in ['антарктида', 'атлантида', 'аґарта', 'шамбала', 'тартарія']):
                score += 0.3 if term_counts['signal'] == 0 else 0.2
        
        return min(score, 0.5)  # Зменшили з 0.7

    def analyze(self, text):
        """ВИПРАВЛЕНО: Балансована оцінка"""
        if not text or len(text.strip()) < 20:
            return {'error': 'Text too short'}
        
        words = text.split()
        word_count = len(words)
        
        # ВИЗНАЧАЄМО, ЧИ ЦЕ НАУКОВИЙ ТЕКСТ
        is_scientific = self.is_scientific_context(text)
        
        # АБСУРДНІСТЬ (0 для наукових текстів)
        absurdity_score, absurd_pairs = self.detect_absurdity(text)
        
        # ДЕТЕКЦІЯ КРИТИЧНИХ ПАТТЕРНІВ
        detected_patterns = self.detect_patterns(text)
        
        # ТЕРМІНОЛОГІЧНІ ПІДРАХУНКИ
        term_counts = self.count_terms(text)
        
        # ЕМОЦІЙНИЙ ТИСК
        emotional_score = self.calculate_emotional_pressure(text)
        
        # СКЛАДНІСТЬ ТА ЕНТРОПІЯ
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
        
        gradient_penalty = self.calculate_gradient_penalties(base_metrics)
        conflict_penalty = self.calculate_conflict_penalty(text)
        contextual_score = self.calculate_contextual_score(text, term_counts, base_metrics)
        
        # ================= БАЛАНСОВАНА ФОРМУЛА =================
        if is_scientific:
            # ДЛЯ НАУКОВИХ ТЕКСТІВ: дуже низький бал
            base_score = (
                absurdity_score * 0.20 +      # 20% за абсурд (майже завжди 0)
                emotional_score * 0.15 +      # 15% за емоції (майже завжди 0)
                contextual_score * 0.20 +     # 20% за контекст
                gradient_penalty * 0.25 +     # 25% за градієнт
                conflict_penalty * 0.20       # 20% за конфлікти
            ) * 0.3  # Множимо на 0.3 для науки
        else:
            # ДЛЯ НЕ-НАУКОВИХ: повна формула
            base_score = (
                absurdity_score * 0.30 +      # 30% за абсурдні комбінації
                emotional_score * 0.20 +      # 20% за емоційний тиск
                contextual_score * 0.25 +     # 25% за контекст
                gradient_penalty * 0.15 +     # 15% за градієнт
                conflict_penalty * 0.10       # 10% за конфлікти
            )
        
        # Додаємо бонус за критичні паттерни (тільки для не-наукових)
        if not is_scientific:
            for pattern in detected_patterns:
                base_score += pattern['score_boost'] * 0.7  # Зменшили вплив
        
        # АКАДЕМІЧНИЙ ЗАХИСТ
        if term_counts['academic'] >= 3 and term_counts['signal'] >= 3:
            if term_counts['chaos'] == 0:
                base_score *= 0.2  # Дуже сильний захист
            elif term_counts['chaos'] <= 2:
                base_score *= 0.4  # Сильний захист
            else:
                base_score *= 0.6  # Помірний захист
        elif term_counts['academic'] >= 2 and term_counts['signal'] >= 2:
            base_score *= 0.7  # Слабкий захист
        
        final_score = min(0.99, max(0.0, base_score))
        
        # ================= ВЕРДИКТ =================
        if is_scientific:
            status = 'VERIFIED'
            verdict = 'ВЕРИФІКОВАНИЙ НАУКОВИЙ СИГНАЛ'
            explanation = 'Текст демонструє наукову цілісність та логічну строгість'
        elif detected_patterns and not is_scientific:
            main_pattern = detected_patterns[0]
            status = 'CRITICAL' if final_score > 0.6 else 'WARNING'
            verdict = main_pattern['verdict']
            explanation = main_pattern['explanation']
        elif absurdity_score > 0.3:
            status = 'CRITICAL'
            verdict = 'АБСУРДНИЙ СЕМАНТИЧНИЙ РОЗРИВ'
            explanation = f'Текст поєднує несумісні концепції: {", ".join([f"{a}+{b}" for a,b in absurd_pairs[:2]])}'
        elif final_score > 0.7:
            status = 'CRITICAL'
            verdict = 'ВИСОКИЙ РІВЕНЬ СЕМАНТИЧНОГО ХАОСУ'
            explanation = 'Текст демонструє критичний рівень семантичної несумісності'
        elif final_score > 0.55:
            status = 'WARNING'
            verdict = 'ПІДОЗРІЛА СЕМАНТИЧНА СТРУКТУРА'
            explanation = 'Текст містить ознаки семантичних несумісностей'
        elif final_score > 0.35:
            status = 'ACCEPTABLE'
            verdict = 'ПРИЙНЯТНА СТРУКТУРОВАНА ІНФОРМАЦІЯ'
            explanation = 'Текст відповідає нормам логічної сумісності'
        elif final_score > 0.15:
            status = 'TRUSTED'
            verdict = 'СТАБІЛЬНИЙ ЛОГІЧНИЙ СИГНАЛ'
            explanation = 'Текст демонструє високу логічну цілісність'
        else:
            status = 'VERIFIED'
            verdict = 'ВЕРИФІКОВАНИЙ АКАДЕМІЧНИЙ СИГНАЛ'
            explanation = 'Текст демонструє ідеальну логічну цілісність'
        
        # Додаткові пояснення
        detail_explanations = []
        if gradient_penalty > 0.05:
            detail_explanations.append(f"Градієнт: {gradient_penalty:.2f}")
        if conflict_penalty > 0.05:
            detail_explanations.append(f"Конфлікт: {conflict_penalty:.2f}")
        if contextual_score > 0.1:
            detail_explanations.append(f"Контекст: {contextual_score:.2f}")
        if absurdity_score > 0.05:
            detail_explanations.append(f"Абсурд: {absurdity_score:.2f}")
        
        if detail_explanations:
            explanation += " | " + " + ".join(detail_explanations)

        # ================= МЕТРИКИ =================
        if is_scientific:
            chaos_index = 0.0
            influence_index = round(final_score * 30, 2)
        else:
            chaos_index = round(final_score * 100 * (1 + term_counts['chaos'] * 0.3), 2)
            influence_index = round(final_score * 150 * (1 + emotional_score * 0.3), 2)

        sanity_penalty = round(conflict_penalty + absurdity_score + max(0, gradient_penalty - 0.2), 3)

        noise_marker_count = term_counts.get('noise', 0)
        signal_ratio = 0 if noise_marker_count == 0 else round(noise_marker_count / max(1, term_counts['signal']), 2)
        
        return {
            'entropy': round(final_score, 3),
            'status': status,
            'verdict': verdict,
            'language': 'UK',
            'explanation': explanation,
            'diagnostics': {
                'is_scientific': is_scientific,
                'shannon_entropy': round(shannon_entropy, 3),
                'complexity': round(complexity, 3),
                'contextual_score': round(contextual_score, 3),
                'gradient_penalty': round(gradient_penalty, 3),
                'conflict_penalty': round(conflict_penalty, 3),
                'absurdity_score': round(absurdity_score, 3),
                'emotional_score': round(emotional_score, 3),
                'word_count': word_count,
                'char_count': len(text),
                'academic_markers': term_counts['academic'],
                'chaos_markers': term_counts['chaos'],
                'signal_markers': term_counts['signal'],
                'noise_markers': noise_marker_count,
                'pattern_count': len(detected_patterns),
                'absurd_pairs_found': len(absurd_pairs),
                'shout_factor': len([w for w in words if w.isupper() and len(w) > 2]) / max(1, word_count),
                'number_density': len(re.findall(r'\d+', text)) / max(1, word_count),
                'signal_ratio': signal_ratio,
                'chaos_index': chaos_index,
                'influence_index': influence_index,
                'sanity_penalty': sanity_penalty
            }
        }

    def _calculate_shannon_entropy(self, text):
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

    def _calculate_complexity(self, text):
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
