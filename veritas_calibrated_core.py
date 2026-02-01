"""
Veritas Protocol - Semantic Void Detector v11.2 (CRITICAL FIX)
ВИПРАВЛЕНА ФІЛОСОФІЯ: Високі штрафи за абсурд, захист науки
"""

import re
import math
from collections import Counter

class LogicalViolation:
    """Представляє логічне порушення високого рівня"""
    def __init__(self, vtype: str, severity: float, evidence: list, context: str):
        self.type = vtype
        self.severity = severity
        self.evidence = evidence
        self.context = context

class VeritasCalibratedCore:
    """Advanced detector - FIXED: PROTECTS SCIENCE, PUNISHES ABSURDITY"""
    
    def __init__(self):
        # ============================================================
        # КРИТИЧНІ ПАТТЕРНИ (ЗАЛИШАЄМО)
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
                'score_boost': 0.6  # ПІДВИЩЕНО!
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
                'score_boost': 0.5  # ПІДВИЩЕНО!
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
                'score_boost': 0.7  # ПІДВИЩЕНО!
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
                'score_boost': 0.65  # ПІДВИЩЕНО!
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
                'score_boost': 0.55  # ПІДВИЩЕНО!
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
                'score_boost': 0.6  # ПІДВИЩЕНО!
            },

            # 7. ІНФОРМАЦІЙНА ВІЙНА
            {
                'name': 'ІНФОРМАЦІЙНА_ВІЙНА',
                'patterns': [
                    r'(ворог|enemy|предатель|зрада|зрадник).*?(народ|нація|країна|державa|суспільство).*?(знищення|manipulation)',
                    r'(інформаційна\s+війна|info[\s-]*war|cognitive\s+war).*?(перемога|бoritися|протистояти)',
                    r'(патріот|патріотизм|родина|батківщина).*?(окупант|ворог|агресор|колаборант).*?(предатели|тиха\s+група)',
                    r'(пропаганда|фейк|дезінформація).*?(обидва\s+боки|з\'обидва).*?(виноват|виновні)'
                ],
                'verdict': 'ІНФОРМАЦІЙНА ВІЙНА',
                'explanation': 'Текст використовує нарративи інформаційної війни для поляризації',
                'score_boost': 0.55  # ПІДВИЩЕНО!
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
                'explanation': 'Текст дискредитує медицину та просуть ненаукові альтернативи',
                'score_boost': 0.7  # ПІДВИЩЕНО!
            },

            # 9. AI ЕСХАТОЛОГИЯ
            {
                'name': 'AI_ЕСХАТОЛОГИЯ',
                'patterns': [
                    r'(superintelligence|суперінтелект|superintelligent).*?(знищить|destroys|destroy|humanity|людство|civilization)',
                    r'(robot uprising|machine revolt|восстание роботів|восстание роботов).*?(неминучий|inevitable|coming|настає)',
                    r'(AI apocalypse|AI апокаліпс|technological singularity|tech rapture).*?(кінець|end|collapse|humanity|людство)',
                    r'(post-human|posthuman|transhumanism).*?(salvation|спасіння|end|кінець|apocalypse|апокаліпс)'
                ],
                'verdict': 'AI ЕСХАТОЛОГИЯ',
                'explanation': 'Текст смішує AI narrative з апокаліптичними сценаріями',
                'score_boost': 0.6  # ПІДВИЩЕНО!
            }
        ]
        
        # ============================================================
        # ПРОБЛЕМНІ КОНФЛІКТНІ ПАРИ - ВИДАЛИТИ ВСІ, ЩО ШТРАФУЮТЬ НАУКУ!
        # ============================================================
        self.conflict_pairs = [
            # ЛИШЕ Справді абсурдні комбінації:
            
            # 1. Наука + Їжа (ФІКСОВАНО)
            (['квантовий', 'квантова', 'квантове', 'квантові', 'сингулярність',
              'суперпозиція', 'хвильова функція', 'колапс хвильової'],
             ['борщ', 'сметана', 'картопля', 'морква', 'суп', 'їжа', 'буряк', 'каструля', 
              'бульйон', 'черпак', 'петрушка', 'їсти', 'варити', 'страва', 'обід'], 
             0.8),  # ДУЖЕ ВИСОКИЙ ШТРАФ!
            
            # 2. Біологія + Техно-абсурд
            (['днк', 'генетичний', 'вакцина', 'імунітет', 'клітина', 'організм',
              'нейрон', 'синапс', 'мозок'],
             ['5g', 'супутник', 'старлінк', 'водопровідний', 'вода', 'чип', 'мікрочіп',
              'транслюють', 'частоти', 'гц', 'дестабілізує', 'записувати'], 
             0.75),
            
            # 3. Політика + Окультизм
            (['президент', 'уряд', 'держава', 'політика', 'закон', 'конституція'],
             ['рептилоїд', 'ілюмінат', 'масон', 'сатана', 'дьявол', 'антихрист',
              'апокаліпсис', 'ритуал', 'жертва', 'поклоніння'], 
             0.7),
            
            # 4. Економіка + Містицизм
            (['гроші', 'банк', 'економіка', 'фінанси', 'інвестиції', 'ринок',
              'акція', 'облігація', 'криптовалюта'],
             ['душа', 'карма', 'астрал', 'чакра', 'аура', 'енергія', 'вібрація',
              'потойбічний', 'космічний', 'божественний', 'містичний'], 
             0.7),
            
            # 5. Технології + Духовність
            (['AI', 'блокчейн', 'алгоритм', 'код', 'програма', 'матриця'],
             ['душа', 'свідомість', 'карма', 'просвітлення', 'медитація', 'йога'], 
             0.65),
            
            # 6. Істерія (ОСОБЛИВО ВАЖЛИВО!)
            (['СРОЧНО', 'УВАГА', 'ВНИМАНИЕ', 'шок', 'ужас', 'паніка'],
             ['правда', 'істина', 'факт', 'реальність', 'конец', 'загибель'], 
             0.8),
        ]
        
        # ============================================================
        # ВИДАЛИТИ всі градієнтні штрафи, які карають науку!
        # ============================================================
        self.gradient_penalties = [
            {
                'type': 'entropy_gradient',
                'calculate': lambda m: max(0, (m['shannon_entropy'] - 0.8) * 2) if m['signal_markers'] < 2 else 0
            },
            {
                'type': 'chaos_signal_ratio',
                'calculate': lambda m: min(0.7, m['chaos_markers'] / max(1, m['signal_markers'] + 1) * 0.3)
            },
        ]
        
        # ============================================================
        # НОВИЙ: Маркери ДИКИХ маніпуляцій
        # ============================================================
        self.hysteria_indicators = [
            'НЕГАЙНО', 'ПОШИРЮЙТЕ', 'ЗРАДА', 'ГАНЬБА', 'КРИМІНАЛЬНИЙ',
            'ПРИХОВУЮТЬ', 'СКРИТА ПРАВДА', 'ВИЙДІТЬ НА ВУЛИЦІ', 'ПІЗНО',
            'МАЄМО ВИЙТИ', 'ЗУПИНИМО', 'КІНЕЦЬ', 'КАТАСТРОФА', 'СКАНДАЛ'
        ]
        
        # ============================================================
        # НОВИЙ: Маркери псевдоінтелектуального абсурду
        # ============================================================
        self.pseudo_science_absurdity = [
            ('нанодискретизація', 0.6),
            ('колективне несвідоме', 0.7),
            ('супутникові масиви низької орбіти', 0.8),
            ('квантова суперпозиція нейронів', 0.9),
            ('пост-біологічне суспільство', 0.7),
            ('чакри', 0.8),
            ('вібраційний фон', 0.7),
            ('ефірний кокон', 0.8),
            ('провідники прани', 0.9),
            ('солфеджіо', 0.6),
            ('мета-фізичні протоколи', 0.9),
            ('квантове вирівнювання аури', 1.0),
            ('підсвідомих архетипів', 0.7),
            ('світловий вузол у глобальній матриці', 0.9),
            ('трансцендентна рентабельність', 0.8),
            ('езотеричні цикли накопичення капіталу', 0.9),
            ('не матеріалізувалися в поточному часовому континуумі', 1.0),
        ]
        
        # ============================================================
        # НОВИЙ: Маркери БІЗНЕС-ЕЗОТЕРИКИ (корпоративний абсурд)
        # ============================================================
        self.business_esoteric_bullshit = [
            ('синергетичний розвиток', 0.5),
            ('імплементація', 0.3),
            ('холістичний маркетинг', 0.6),
            ('екосистема', 0.4),
            ('глобальна матриця споживання', 0.8),
            ('оптимізуємо людські ресурси', 0.4),
            ('квантове вирівнювання', 0.9),
            ('енергетичний баланс команди', 0.8),
            ('вібраційна ефективність', 0.9),
            ('духовний KPI', 1.0),
            ('астральний брендинг', 1.0),
            ('чакровий менеджмент', 1.0),
        ]

    def analyze(self, text):
        """ПОВНІСТЮ ПЕРЕРОБЛЕНА ЛОГІКА!"""
        if not text or len(text.strip()) < 20:
            return {'error': 'Text too short'}
        
        text_lower = text.lower()
        words = text.split()
        word_count = len(words)
        
        # ============================================================
        # КРОК 1: ШВИДКІ ДЕТЕКТОРИ АБСУРДУ (ВИСОКІ ШТРАФИ!)
        # ============================================================
        
        # 1. Істерія та паникерство
        hysteria_score = 0
        for indicator in self.hysteria_indicators:
            if indicator.lower() in text_lower:
                hysteria_score += 0.5
                if indicator in text:  # У верхньому регістрі - ще більше!
                    hysteria_score += 0.3
        
        # 2. Псевдонауковий абсурд
        pseudo_science_score = 0
        for term, weight in self.pseudo_science_absurdity:
            if term.lower() in text_lower:
                pseudo_science_score += weight
        
        # 3. Бізнес-езотерика
        business_bullshit_score = 0
        for term, weight in self.business_esoteric_bullshit:
            if term.lower() in text_lower:
                business_bullshit_score += weight
        
        # 4. Конфліктні пари (лише справді абсурдні)
        conflict_penalty, conflict_details = self.calculate_conflict_penalty(text)
        
        # 5. Критичні паттерни
        detected_patterns = self.detect_patterns(text)
        
        # ============================================================
        # КРОК 2: ЗАХИСТ НАУКИ (відразу вихід для чистої науки)
        # ============================================================
        
        # Наукові маркери
        academic_terms = ['термодинаміка', 'ентропія', 'фізика', 'статистичний',
                         'дослідження', 'експеримент', 'теорія', 'гіпотеза',
                         'методологія', 'аналіз', 'кореляція', 'верифікація']
        
        science_markers = sum(1 for term in academic_terms if term in text_lower)
        has_science_formulas = any(formula in text for formula in ['=', '≠', '≈', '~', '→', '⇒', '∈', '∑', '∫', '∂'])
        
        # Якщо це науковий текст БЕЗ абсурду - VERIFIED
        if (science_markers >= 3 and has_science_formulas and 
            hysteria_score == 0 and pseudo_science_score == 0 and 
            business_bullshit_score == 0 and conflict_penalty == 0):
            
            return {
                'entropy': 0.05,
                'status': 'VERIFIED',
                'verdict': 'НАУКОВИЙ СТАНДАРТ',
                'language': 'UK',
                'explanation': 'Текст демонструє наукову цілісність без ознак абсурду',
                'diagnostics': {
                    'science_score': science_markers,
                    'hysteria_score': hysteria_score,
                    'pseudo_science_score': pseudo_science_score,
                    'business_bullshit_score': business_bullshit_score,
                    'conflict_penalty': conflict_penalty,
                    'is_science': True
                }
            }
        
        # ============================================================
        # КРОК 3: РОЗРАХУНОК ЗАГАЛЬНОГО ШТРАФУ
        # ============================================================
        
        # БАЗОВИЙ ШТРАФ (70% - абсурдні маркери!)
        base_score = (
            min(hysteria_score, 1.0) * 0.4 +
            min(pseudo_science_score, 2.0) * 0.3 +
            min(business_bullshit_score, 2.0) * 0.3 +
            conflict_penalty * 0.4
        )
        
        # Бонуси за критичні паттерни (сильніше!)
        for pattern in detected_patterns:
            base_score += pattern['score_boost']
        
        # Автоматичний CRITICAL для явного абсурду
        if pseudo_science_score > 1.5 or business_bullshit_score > 1.5:
            base_score = max(base_score, 0.8)
        
        if hysteria_score > 1.0:
            base_score = max(base_score, 0.7)
        
        final_score = min(0.99, max(0.0, base_score))
        
        # ============================================================
        # КРОК 4: ВЕРДИКТИ (ЖОРСТКІШІ ПОРОГИ!)
        # ============================================================
        
        if detected_patterns:
            main_pattern = detected_patterns[0]
            status = 'CRITICAL' if final_score > 0.4 else 'WARNING'
            verdict = main_pattern['verdict']
            explanation = main_pattern['explanation']
        elif final_score > 0.7:
            status = 'CRITICAL'
            if pseudo_science_score > 1.0:
                verdict = 'НАУКОВИЙ АБСУРД'
                explanation = 'Псевдонаукові терміни використані для створення беззмістовних конструкцій'
            elif business_bullshit_score > 1.0:
                verdict = 'КОРПОРАТИВНИЙ ЕЗОТЕРИЧНИЙ АБСУРД'
                explanation = 'Бізнес-жаргон змішаний з містичними концепціями'
            elif hysteria_score > 0.8:
                verdict = 'ЕМОЦІЙНА ІСТЕРІЯ'
                explanation = 'Текст свідомо нагнітає паніку для маніпуляції'
            else:
                verdict = 'КРИТИЧНИЙ ЛОГІЧНИЙ АБСУРД'
                explanation = 'Текст містить несумісні поняття високого рівня'
        elif final_score > 0.5:
            status = 'WARNING'
            verdict = 'ПІДОЗРІЛА ЛОГІЧНА СТРУКТУРА'
            explanation = 'Текст містить ознаки логічних несумісностей'
        elif final_score > 0.3:
            status = 'ACCEPTABLE'
            verdict = 'ПРИЙНЯТНИЙ ДИСКУРС'
            explanation = 'Текст відповідає нормам логічної сумісності'
        elif final_score > 0.1:
            status = 'TRUSTED'
            verdict = 'СТАБІЛЬНИЙ ЛОГІЧНИЙ СИГНАЛ'
            explanation = 'Текст демонструє високу логічну цілісність'
        else:
            status = 'VERIFIED'
            verdict = 'ВЕРИФІКОВАНИЙ КОНТЕНТ'
            explanation = 'Текст демонструє ідеальну логічну цілісність'
        
        # Деталізація
        details = []
        if hysteria_score > 0:
            details.append(f"Істерія: {hysteria_score:.1f}")
        if pseudo_science_score > 0:
            details.append(f"Псевдонаука: {pseudo_science_score:.1f}")
        if business_bullshit_score > 0:
            details.append(f"Бізнес-абсурд: {business_bullshit_score:.1f}")
        if conflict_penalty > 0:
            details.append(f"Конфлікти: {conflict_penalty:.1f}")
        
        if details:
            explanation += " | " + " + ".join(details)
        
        return {
            'entropy': round(final_score, 3),
            'status': status,
            'verdict': verdict,
            'language': 'UK',
            'explanation': explanation,
            'diagnostics': {
                'hysteria_score': round(hysteria_score, 2),
                'pseudo_science_score': round(pseudo_science_score, 2),
                'business_bullshit_score': round(business_bullshit_score, 2),
                'conflict_penalty': round(conflict_penalty, 2),
                'word_count': word_count,
                'char_count': len(text),
                'science_markers': science_markers,
                'has_science_formulas': has_science_formulas,
                'pattern_count': len(detected_patterns),
                'is_science': False
            }
        }
    
    def detect_patterns(self, text):
        """Виявляє критичні паттерни"""
        detected = []
        text_lower = text.lower()
        
        for pattern in self.critical_patterns:
            for regex in pattern['patterns']:
                if re.search(regex, text_lower, re.DOTALL | re.IGNORECASE):
                    detected.append(pattern)
                    break
        
        return detected
    
    def calculate_conflict_penalty(self, text):
        """Обчислює штраф за справді абсурдні конфлікти"""
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
                    penalty += weight * 1.5
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
        
        return min(penalty, 1.0), found_conflicts

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
