"""
Veritas Protocol - Semantic Void Detector v9.0 (Expanded Taxonomy)
Extended terminology, 14 chaos categories, 8 critical patterns
"""

import re
import math
from collections import Counter

class VeritasCalibratedCore:
    """Advanced detector with fine-tuned sensitivity"""
    
    def __init__(self):
        # ============================================================
        # КРИТИЧНІ ПАТТЕРНИ (8 категорій)
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
                'score_boost': 0.4
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
                'score_boost': 0.35
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
                'score_boost': 0.45
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
                'score_boost': 0.5
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
                'score_boost': 0.42
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
                'explanation': 'Технологічна термінология смішується з окультними концепціями',
                'score_boost': 0.38
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
                'score_boost': 0.44
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
                'score_boost': 0.46
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
                'score_boost': 0.40
            }
        ]
        
        # ============================================================
        # ХАОС-ІНДИКАТОРИ (14 категорій)
        # ============================================================
        self.chaos_indicators = {
            # --- Оригінальні 6 (розширені списки) ---
            'esoteric': [
                'чакра', 'карма', 'астральний', 'енергетичний', 'вібрація',
                'аура', 'третій око', 'кундаліні', 'медитація',
                'мантра', 'янтра', 'сиддхи', 'самадхі',
                'таро', 'руни', 'пентаграма', 'окутьна'
            ],
            'conspiracy': [
                'змова', 'рептилоїд', 'хімітрейл', '5g', 'дезінформація',
                'нова світова порядок', 'нового світового порядку',
                'секретне товариство', 'секретні товариства', 'темні сили',
                'оккутьна еліта', 'таємна група', 'shadow government',
                'deep state', 'illuminati', 'skull and bones', 'bilderberg'
            ],
            'pseudoscience': [
                'квантовий', 'нейтрино', 'іоносфера', 'кристалічний',
                'торсійне поле', 'торсійна енергія',
                'зеро-поинт', 'zero point', 'ефір',
                'антигравітація', 'scalar field', 'скалярне поле',
                'тесла-котушка', 'тесла', 'free energy', 'безкоштовна енергія'
            ],
            'revisionism': [
                'антарктида', 'атлантида', 'наполеон', 'штучний місяць',
                'аґарта', 'шамбала', 'тартарія',
                'древні інопланетяні', 'древні боги', 'ancient aliens',
                'пираміди пришельців', 'lost civilization',
                'hidden history', 'скрита історія', 'справжня історія'
            ],
            'alarmism': [
                'перезавантаження', 'пожежа реальності', 'деактивувати',
                'кінець світу', 'end of the world', 'total collapse',
                'крах системи', 'system failure',
                'great reset', 'великий перезапуск',
                'планетарна катастрофа', 'масове загибель', 'mass extinction'
            ],
            'economic_occult': [
                'потойбічний', 'карма актив', 'hades-coin', 'ефірний пласт',
                'душа-валюта', 'soul currency', 'spiritual investment',
                'енергетичний банк', 'карма-фонд', 'cosmic economy',
                'cosmic currency', 'astral banking', 'soul contract'
            ],

            # --- Нові 8 категорій ---
            'emotional_manipulation': [
                'шок', 'невозможно поверити', 'неможливо поверити',
                'ужас', 'катастрофа', 'скандал', 'сенсація',
                'OMG', 'WOW', 'СРОЧНО', 'URGENT',
                'breaking news', 'exclusive',
                'ви не готовні', 'будь готовий',
                'всё кончилось', 'game over', 'тільки зараз',
                'limited time', 'не повторюється', 'once in a lifetime'
            ],
            'social_pressure': [
                'поділіть', 'поделайся', 'поделайтесь', 'share this',
                'підпишіть', 'подпишитесь', 'subscribe', 'sign up',
                'tell your friends', 'расскажите друзьям', 'spread the word',
                'join the movement', 'приєднуйся до руху',
                'if you care', 'якщо вам не всё равно',
                'wake up', 'просыпайся', 'просыпайтесь',
                'be part of', 'будьте частиною', 'you need to know',
                'ви повинні знати', 'everyone needs to see'
            ],
            'tech_mystification': [
                'AI свідомість', 'sentient AI',
                'blockchain truth', 'блокчейн правда', 'NFT soul',
                'метаверс реальність', 'metaverse reality',
                'digital enlightenment', 'цифрове просвітлення',
                'код вселенної', 'code of the universe',
                'simulation theory', 'теория симуляції',
                'matrix awakening', 'пробуджень матриці',
                'soul upload', 'mind upload'
            ],
            'health_misinformation': [
                'вакцина убиває', 'vaccines kill',
                'Big Pharma', 'pharma hides',
                'натуральне лікування краще', 'nature cures all',
                'доктори брешуть', 'doctors lie', 'WHO lies',
                'ВОЗ брешуть', 'FDA корупція', 'FDA corrupt',
                'cure for cancer hidden', 'ліки від онкология скрити',
                '5G causes illness', 'GMO poison', 'ГМО отрута',
                'хімітрейл здоров\'я'
            ],
            'political_manipulation': [
                'ворог народу', 'enemy of the people', 'предатель',
                'зрада', 'зрадник', 'traitor', 'колаборант',
                'агресор', 'окупант',
                'тиха група', 'fifth column', 'п\'ята колона',
                'антинародний режим', 'антинародний уряд',
                'кримінальний режим', 'tyranny', 'тиранія',
                'false flag', 'провокація'
            ],
            'ai_doom_or_salvation': [
                'AI знищить людство', 'AI destroys humanity',
                'AI спасть світ', 'AI saves the world',
                'superintelligence', 'суперінтелект',
                'technological singularity', 'технологічна сингулярність',
                'robot uprising', 'восстание роботів',
                'AI apocalypse', 'AI апокаліпс', 'post-human',
                'transhumanism salvation',
                'бессмертя через AI', 'immortality through AI'
            ],
            'identity_crisis': [
                'ви не те, хто думаєте', 'you are not who you think',
                'пробуджень іденті', 'identity awakening',
                'ваша справжня природа', 'your true nature',
                'запрограмована іденті', 'programmed identity',
                'breaking free', 'звільнення від системи',
                'ваша душа знає', 'your soul knows',
                'внутрішня правда', 'inner truth',
                'самопробуджень', 'self awakening',
                'личность матриці', 'matrix personality'
            ]
        }
        
        # ============================================================
        # СИГНАЛЬНІ МАРКЕРИ (24)
        # ============================================================
        self.signal_markers = [
            # Оригінальні
            'факт', 'дані', 'показник', 'кількість', 'число', 'статистика',
            'дослідження', 'експеримент', 'результат', 'метод', 'протокол',
            # Розширення — методология
            'аналіз', 'модель', 'гипотеза', 'контрольна група', 'виборка',
            'значущість', 'реплікація', 'валідація', 'верифікація',
            # Розширення — публікації / інституції
            'публікація', 'рецензування', 'журнал', 'університет',
            'інститут', 'академія', 'лабораторія',
            # Розширення — специфічні
            'коефіцієнт', 'кореляція', 'відхилення',
            'мета-аналіз', 'p-value', 'confidence interval'
        ]
        
        # ============================================================
        # АКАДЕМІЧНИЙ WHITELIST (35)
        # ============================================================
        self.academic_whitelist = [
            # Оригінальні
            'кореляція', 'верифікація', 'гіпотеза', 'вибірка', 'значущість',
            'нейрони', 'синапси', 'метааналіз', 'статистичний', 'логістика',
            'деескалація', 'макроекономічний', 'інвестиції', 'інфраструктура',
            'ратифікація', 'протокол', 'емпіричний', 'квалітативний', 'кількісний',
            # Розширення — наука
            'гипотеза', 'реплікація', 'валідація', 'контрольна група',
            'плацебо', 'рандомізація', 'когорта',
            'мета-аналіз', 'систематичний огляд',
            # Розширення — інститункційні маркери
            'опубликовано в', 'peer-reviewed',
            # Розширення — академічний стиль
            'за даними', 'згідно з дослідженням', 'результати показують',
            'статистично значущий', 'ефект розміру', 'effect size'
        ]
        
        # ============================================================
        # ГРАДІЄНТНІ ШТРАФИ (без змін)
        # ============================================================
        self.gradient_penalties = [
            {
                'type': 'entropy_gradient',
                'calculate': lambda m: max(0, (m['shannon_entropy'] - 0.7) * 2) if m['signal_markers'] < 2 else 0
            },
            {
                'type': 'complexity_gradient',
                'calculate': lambda m: max(0, (m['complexity'] - 0.75) * 1.5) if m['signal_markers'] < 2 else 0
            },
            {
                'type': 'chaos_signal_ratio',
                'calculate': lambda m: min(0.5, m['chaos_markers'] / max(1, m['signal_markers'] + 1) * 0.2)
            },
            {
                'type': 'academic_dissonance',
                'calculate': lambda m: 0.15 if m['academic_markers'] > 0 and m['chaos_markers'] > 0 else 0
            },
            {
                'type': 'zero_signal_complexity',
                'calculate': lambda m: 0.25 if m['signal_markers'] == 0 and m['complexity'] > 0.75 else 0
            }
        ]
        
        # ============================================================
        # КОНФЛІКТНІ ПАРИ (9)
        # ============================================================
        self.conflict_pairs = [
            # Оригінальні 5
            (['бднф', 'гіпокамп', 'нейропластичність'], ['5g', 'супутник', 'таргетування'], 0.35),
            (['нейтрино', 'квантовий', 'ентропія'], ['ринок', 'економіка', 'політика'], 0.3),
            (['днк', 'генетичний'], ['алгоритм', 'код', 'підпис'], 0.4),
            (['антарктида', 'атлантида'], ['технологія', 'цивілізація', 'резонатор'], 0.3),
            (['облігація', 'криптовалюта', 'банк'], ['потойбічний', 'карма', 'душа'], 0.4),
            # Нові 4
            (['вакцина', 'щеплення', 'FDA', 'ВОЗ'], ['скрита правда', 'вони скрывают', 'Big Pharma'], 0.4),
            (['AI', 'штучний інтелект', 'нейромережа', 'блокчейн'], ['душа', 'свідомість', 'карма', 'астрал', 'awakening'], 0.35),
            (['статистика', 'дані', 'дослідження', 'університет'], ['snake oil', 'народна медицина', 'натуральне лікування'], 0.35),
            (['патріот', 'батківщина', 'нація'], ['ворог народу', 'предатель', 'зрада', 'п\'ята колона'], 0.3)
        ]

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

    def count_terms(self, text):
        """Підраховує терміни за категоріями"""
        text_lower = text.lower()
        counts = {'academic': 0, 'chaos': 0, 'signal': 0, 'noise': 0}
        
        for term in self.academic_whitelist:
            if term.lower() in text_lower:
                counts['academic'] += 1
        
        for category, terms in self.chaos_indicators.items():
            for term in terms:
                if term.lower() in text_lower:
                    counts['chaos'] += 1
        
        for marker in self.signal_markers:
            if marker.lower() in text_lower:
                counts['signal'] += 1

        # Noise = емоційна маніпуляція + соціальний тиск (окремо для signal_ratio)
        for cat in ['emotional_manipulation', 'social_pressure']:
            for term in self.chaos_indicators.get(cat, []):
                if term.lower() in text_lower:
                    counts['noise'] += 1
        
        return counts

    def calculate_gradient_penalties(self, metrics):
        """Обчислює градієнтні штрафи"""
        total_penalty = 0.0
        for penalty in self.gradient_penalties:
            total_penalty += penalty['calculate'](metrics)
        return min(total_penalty, 0.6)

    def calculate_conflict_penalty(self, text):
        """Обчислює штраф за конфліктні пари"""
        penalty = 0.0
        text_lower = text.lower()
        
        for list1, list2, weight in self.conflict_pairs:
            has_first = any(term.lower() in text_lower for term in list1)
            has_second = any(term.lower() in text_lower for term in list2)
            if has_first and has_second:
                penalty += weight
        
        non_sequitur_patterns = [
            (r'вода.*?кипить.*?100', r'ядерний.*?арсенал'),
            (r'сонце.*?сходить.*?сході', r'дестабілізація'),
            (r'2\+2=4', r'хаос.*?логіка'),
            (r'земля.*?кругла', r'випадкові.*?числа')
        ]
        
        for pattern1, pattern2 in non_sequitur_patterns:
            if re.search(pattern1, text_lower) and re.search(pattern2, text_lower):
                penalty += 0.3
        
        return min(penalty, 0.5)

    def calculate_contextual_score(self, text, term_counts, metrics):
        """Обчислює контекстуальну оцінку"""
        score = 0.0
        words = text.split()
        word_count = len(words)
        text_lower = text.lower()
        
        # 1. Семантична пустота
        if term_counts['signal'] == 0:
            if metrics['complexity'] > 0.75:
                score += 0.4
            elif metrics['shannon_entropy'] > 0.75:
                score += 0.3
            else:
                score += 0.15
        
        # 2. Науковий нігілізм
        if term_counts['academic'] > 0 and term_counts['chaos'] > 0:
            academic_ratio = term_counts['academic'] / word_count
            chaos_ratio = term_counts['chaos'] / word_count
            score += 0.35 if chaos_ratio > academic_ratio else 0.2
        
        # 3. Історичний ревізіонізм
        if any(w in text_lower for w in ['антарктида', 'атлантида', 'аґарта', 'шамбала', 'тартарія']):
            score += 0.4 if term_counts['signal'] == 0 else 0.25
        
        # 4. Економічний окультизм
        if any(w in text_lower for w in ['облігація', 'криптовалюта', 'банк', 'блокчейн', 'NFT', 'DAO']):
            if any(w in text_lower for w in ['карма', 'потойбічний', 'душа', 'астрал', 'soul', 'spirit']):
                score += 0.45

        # 5. Емоційна дестабілізація
        if term_counts.get('noise', 0) >= 2:
            caps_words = len([w for w in words if w.isupper() and len(w) > 2])
            score += 0.3 if caps_words >= 2 else 0.15

        # 6. Цифровий містицізм
        tech = ['AI', 'блокчейн', 'blockchain', 'NFT', 'метаверс', 'metaverse', 'алгоритм']
        mystic = ['душа', 'свідомість', 'consciousness', 'карма', 'awakening', 'просвітлення']
        if any(t in text for t in tech) and any(t in text_lower for t in mystic):
            score += 0.35

        # 7. Медична дезінформація
        med_targets = ['вакцина', 'вакцинація', 'щеплення', 'FDA', 'ВОЗ', 'Big Pharma']
        med_attack = ['скрита правда', 'вони скрывают', 'they hide', 'корупція', 'genocide', 'убиває']
        if any(t.lower() in text_lower for t in med_targets):
            if any(t.lower() in text_lower for t in med_attack):
                score += 0.4

        # 8. AI доом/salvation
        ai_extreme = ['AI знищить', 'AI спасть', 'суперінтелект', 'сингулярність', 'robot uprising', 'восстание роботів']
        if any(t.lower() in text_lower for t in ai_extreme):
            score += 0.3
        
        return min(score, 0.7)

    def analyze(self, text):
        """Основний метод аналізу"""
        if not text or len(text.strip()) < 20:
            return {'error': 'Text too short'}
        
        words = text.split()
        word_count = len(words)
        
        detected_patterns = self.detect_patterns(text)
        term_counts = self.count_terms(text)
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
        
        base_score = (
            shannon_entropy * 0.12 +
            complexity * 0.08 +
            (term_counts['chaos'] / max(1, word_count)) * 0.20 +
            contextual_score * 0.25 +
            gradient_penalty * 0.20 +
            conflict_penalty * 0.15
        )
        
        for pattern in detected_patterns:
            base_score += pattern['score_boost']
        
        # АКАДЕМІЧНИЙ ЗАХИСТ
        if term_counts['academic'] >= 2 and term_counts['signal'] >= 2:
            if term_counts['chaos'] == 0:
                base_score *= 0.3
            elif term_counts['chaos'] <= 1:
                base_score *= 0.5
            else:
                base_score *= 0.7
        elif term_counts['academic'] >= 1 and term_counts['signal'] >= 1:
            base_score *= 0.8
        
        if conflict_penalty > 0.35:
            base_score = max(base_score, 0.65)
        if contextual_score > 0.4:
            base_score = max(base_score, 0.6)
        
        final_score = min(0.99, max(0.0, base_score))
        
        # ВЕРДИКТ
        if detected_patterns:
            main_pattern = detected_patterns[0]
            status = 'CRITICAL' if final_score > 0.6 else 'WARNING'
            verdict = main_pattern['verdict']
            explanation = main_pattern['explanation']
        elif final_score > 0.7:
            status = 'CRITICAL'
            if contextual_score > 0.4:
                verdict = 'ВИСОКИЙ РІВЕНЬ СЕМАНТИЧНОГО ХАОСУ'
                explanation = 'Текст демонструє критичний рівень семантичної несумісності'
            else:
                verdict = 'СЕМАНТИЧНА ПУСТОТА'
                explanation = 'Високий рівень абстракції при відсутності конкретного змісту'
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
        
        detail_explanations = []
        if gradient_penalty > 0.1:
            detail_explanations.append(f"Градієнтний штраф: {gradient_penalty:.2f}")
        if conflict_penalty > 0.1:
            detail_explanations.append(f"Конфліктний штраф: {conflict_penalty:.2f}")
        if contextual_score > 0.2:
            detail_explanations.append(f"Контекстуальна оцінка: {contextual_score:.2f}")
        
        if detail_explanations:
            explanation += " | " + " + ".join(detail_explanations)

        # ============================================================
        # ПОХІДНІ МЕТРИКИ
        # ============================================================
        signal = term_counts['signal']
        chaos = term_counts['chaos']
        context = contextual_score
        conflict = conflict_penalty
        final = final_score

        if signal >= 2 and chaos == 0:
            chaos_index = 0.0
        elif chaos > 0:
            chaos_index = final * 100 * (1 + chaos * 0.6) * (1 + max(0, context - 0.3) * 1.96) / (1 + signal * 0.8)
        else:
            chaos_index = final * 100 * (1 - conflict * 0.8) * (1 - context * 0.46) / (1 + signal * 1.0)
        chaos_index = round(chaos_index, 2)

        if signal >= 2 and chaos == 0:
            influence_index = final * word_count * (1 + final)
        elif signal == 0:
            influence_index = final * 100 * (1 + final) + chaos_index
        else:
            score_part = final * 100 * (1 + final) / (1 + signal * 0.35)
            ci_part = chaos_index / (1 + signal * 0.2)
            influence_index = score_part + ci_part
        influence_index = round(influence_index, 2)

        sanity_penalty = round(conflict_penalty + max(0, gradient_penalty - 0.3), 3)

        noise_marker_count = term_counts.get('noise', 0)
        signal_ratio = 0 if noise_marker_count == 0 else round(noise_marker_count / max(1, signal), 2)
        
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
                'noise_markers': noise_marker_count,
                'pattern_count': len(detected_patterns),
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
