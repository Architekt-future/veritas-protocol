"""
Veritas Protocol - Semantic Void Detector v10.5 (ORIGINAL RESTORED + Fixes)
Повернення оригінальної системи з усіма маркерами та категоріями
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
                'explanation': 'Технологічна термінологія смішується з окультними концепціями',
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
        # ХАОС-ІНДИКАТОРИ (14 категорій) - ОРИГІНАЛ
        # ============================================================
        self.chaos_indicators = {
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
                'ви не готові', 'будь готовий',
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
        # СИГНАЛЬНІ МАРКЕРИ (24) - ОРИГІНАЛ
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
        # АКАДЕМІЧНИЙ WHITELIST (35) - ОРИГІНАЛ
        # ============================================================
        self.academic_whitelist = [
            # Оригінальні
            'кореляція', 'верифікація', 'гіпотеза', 'выбірка', 'значущість',
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
        # КОНФЛІКТНІ ПАРИ (9) - ОРИГІНАЛ + УНІВЕРСАЛЬНІ
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
            (['патріот', 'батківщина', 'нація'], ['ворог народу', 'предатель', 'зрада', 'п\'ята колона'], 0.3),
            
            # ============================================================
            # УНІВЕРСАЛЬНІ КОНФЛІКТНІ ПАРИ ДЛЯ АБСУРДУ (ДОДАЄМО!)
            # ============================================================
            
            # 1. Наукові терміни + їжа
            (['квантовий', 'квантова', 'квантове', 'квантові', 'ентропія', 'флуктуація', 'тунельний', 'сингулярність', 
              'суперпозиція', 'планк', 'гейзенберг', 'хвильова функція', 'колапс хвильової', 'мультивсесвіт', 
              'кристалізація', 'термодинаміка', 'термодинаміці', 'термодинаміку', 'фізика', 'математика'],
             ['борщ', 'сметана', 'картопля', 'морква', 'суп', 'їжа', 'кулінарний', 'буряк', 'каструля', 'бульйон', 
              'черпак', 'петрушка', 'кроп', 'морква', 'їсти', 'варити', 'страва', 'обід'], 
             0.45),
            
            # 2. Медицина/біологія + технологічний абсурд
            (['пінеальний', 'шишкоподібний', 'імунний', 'імунної', 'нанобот', 'наноботів', 'днк', 'генетичний',
              'вакцина', 'вакцинований', 'імунітет', 'клітина', 'організм', 'біологічний', 'медичний'],
             ['5g', 'супутник', 'старлінк', 'блокчейн', 'гейтса', 'водопровідний', 'вода', 'чип', 'мікрочіп',
              'транслюють', 'частоти', 'гц', 'дестабілізує', 'записувати', 'протокол', 'матриця'], 
             0.5),
            
            # 3. Історія/археологія + фантастика
            (['антарктида', 'атлантида', 'тартарія', 'древній', 'інопланетянин', 'бог', 'пираміда', 'цивілізація',
              'історія', 'археологія', 'наполеон', 'цезар', 'клеопатра', 'македонський', 'римський', 'грецький'],
             ['портал', 'вимір', 'тесла', 'голограма', 'резонатор', 'деактивувати', 'код', 'шифр', 'технологія',
              'іншопланетний', 'прибулець', 'нло', 'летюча тарілка', 'паралельний', 'часовий', 'просторовий'], 
             0.4),
            
            # 4. Політика/суспільство + окультизм
            (['президент', 'прем\'єр', 'уряд', 'держава', 'політика', 'суспільство', 'народ', 'країна',
              'міністр', 'парламент', 'вибори', 'демократія', 'республіка', 'монархія'],
             ['рептилоїд', 'ілюмінат', 'масон', 'таємний', 'оккультний', 'ритуал', 'жертва', 'поклоніння',
              'демон', 'сатана', 'дьявол', 'темний', 'світ', 'паралельний', 'вимір', 'потойбічний'], 
             0.42),
            
            # 5. Економіка/фінанси + містицизм
            (['гроші', 'валюта', 'банк', 'економіка', 'фінанси', 'інвестиції', 'ринок', 'бізнес',
              'акція', 'облігація', 'криптовалюта', 'біткоїн', 'етhereum', 'блокчейн', 'nft'],
             ['душа', 'карма', 'астрал', 'енергія', 'вібрація', 'чакра', 'аура', 'рекорнація',
              'потойбічний', 'космічний', 'божественний', 'духовний', 'містичний', 'езотеричний', 'оккультний'], 
             0.38),
            
            # 6. Психологія/неврологія + конспірологія
            (['психологія', 'психічний', 'неврологія', 'мозок', 'свідомість', 'підсвідомість', 'когнітивний',
              'емоційний', 'ментальний', 'розум', 'інтелект', 'пам\'ять', 'сприйняття'],
             ['контроль', 'зомбування', 'програмування', 'маніпуляція', 'вплив', 'втручання', 'втручатися',
              'чип', 'імплант', 'мікрохвильовий', 'радіохвиля', 'частота', 'сигнал', 'трансляція'], 
             0.43),
            
            # 7. Фізика/хімія + езотерика
            (['фізика', 'хімія', 'біологія', 'атом', 'молекула', 'електрон', 'протон', 'нейтрон',
              'енергія', 'матерія', 'поле', 'хвиля', 'частинка', 'кварк', 'бозон', 'ферміон'],
             ['чакра', 'аура', 'біополе', 'енергетичний', 'вібраційний', 'духовний', 'космічний',
              'божественний', 'містичний', 'таємний', 'прихований', 'непізнаний', 'заборонений'], 
             0.35),
            
            # 8. Астрономія/космос + конспірологія
            (['космос', 'всесвіт', 'галактика', 'зірка', 'планета', 'сатурн', 'юпітер', 'марс',
              'астрономія', 'астрофізика', 'космологія', 'чорна діра', 'нейтронна зірка', 'квазар'],
             ['змова', 'приховують', 'нібито', 'насправді', 'правда', 'секрет', 'таємниця', 'прихований',
              'непізнаний', 'іншопланетний', 'прибулець', 'нло', 'контакт', 'послання', 'сигнал'], 
             0.4),
            
            # 9. Технології + містицизм
            (['технологія', 'інтернет', 'комп\'ютер', 'смартфон', 'програма', 'софт', 'апарат',
              'пристрій', 'гаджет', 'девайс', 'інновація', 'цифровий', 'віртуальний'],
             ['душа', 'свідомість', 'дух', 'енергія', 'вібрація', 'карма', 'астрал', 'потойбічний',
              'космічний', 'божественний', 'містичний', 'таємний', 'прихований'], 
             0.36),
            
            # 10. УНІВЕРСАЛЬНА патерн: будь-яка наука + будь-який абсурд
            (['наука', 'науковий', 'дослідження', 'експеримент', 'теорія', 'гіпотеза', 'метод',
              'факт', 'доказ', 'результат', 'висновок', 'публікація', 'журнал', 'університет'],
             ['абсурд', 'нісенітниця', 'бред', 'дурниця', 'вигадка', 'фантазія', 'вигаданий',
              'вигадувати', 'вигадати', 'придуманий', 'неіснуючий', 'вигадати', 'вигаданий'], 
             0.3)
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
        """Підраховує терміни за категоріями - ФІКСОВАНО: використовує всі категорії"""
        text_lower = text.lower()
        counts = {'academic': 0, 'chaos': 0, 'signal': 0, 'noise': 0}
        
        # 1. Академічні маркери
        for term in self.academic_whitelist:
            if term.lower() in text_lower:
                counts['academic'] += 1
        
        # 2. Хаос-маркери з ВСІХ 14 категорій
        for category, terms in self.chaos_indicators.items():
            for term in terms:
                if term.lower() in text_lower:
                    counts['chaos'] += 1
        
        # 3. Сигнальні маркери
        for marker in self.signal_markers:
            if marker.lower() in text_lower:
                counts['signal'] += 1

        # 4. Noise = емоційна маніпуляція + соціальний тиск
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
        """Обчислює штраф за конфліктні пари - ПОКРАЩЕНО"""
        penalty = 0.0
        text_lower = text.lower()
        found_conflicts = []
        
        for list1, list2, weight in self.conflict_pairs:
            found_in_first = []
            found_in_second = []
            
            # Шукаємо терміни з першого списку
            for term in list1:
                if term.lower() in text_lower:
                    found_in_first.append(term)
            
            # Шукаємо терміни з другого списку
            for term in list2:
                if term.lower() in text_lower:
                    found_in_second.append(term)
            
            # Якщо знайшли в обох списках
            if found_in_first and found_in_second:
                # ДОДАТКОВА ПЕРЕВІРКА: чи в одному реченні?
                sentences = re.split(r'[.!?]+', text)
                same_sentence = False
                
                for sentence in sentences:
                    sentence_lower = sentence.lower()
                    has_first_in_sentence = any(term.lower() in sentence_lower for term in found_in_first)
                    has_second_in_sentence = any(term.lower() in sentence_lower for term in found_in_second)
                    
                    if has_first_in_sentence and has_second_in_sentence:
                        same_sentence = True
                        break
                
                # Більший штраф за терміни в одному реченні
                if same_sentence:
                    penalty += weight * 1.2  # +20% за те саме речення
                    found_conflicts.append({
                        'first': found_in_first[:2],  # Перші 2 знайдені
                        'second': found_in_second[:2],
                        'weight': weight * 1.2,
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
        
        # ДОДАТКОВИЙ ШТРАФ за кілька конфліктів
        if len(found_conflicts) >= 3:
            penalty += 0.15
        if len(found_conflicts) >= 5:
            penalty += 0.25
        
        return min(penalty, 0.7), found_conflicts  # Збільшили максимум до 0.7

    def calculate_contextual_score(self, text, term_counts, metrics):
        """Обчислює контекстуальну оцінку - ФІКСОВАНО: більше категорій"""
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

        # 6. Цифровий містицизм
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
        
        # 9. Конспірологія
        if any(t.lower() in text_lower for t in ['рептилоїд', 'ілюмінат', 'більдерберг', 'хімітрейл', '5g']):
            score += 0.25
        
        # 10. Псевдонаука
        if any(t.lower() in text_lower for t in ['квантовий', 'торсійний', 'ефір', 'нейтрино']):
            if any(t.lower() in text_lower for t in ['чакра', 'аура', 'вібрація']):
                score += 0.3
        
        return min(score, 0.7)

    def analyze(self, text):
        """Основний метод аналізу - ФІКСОВАНО: використовує всі маркери"""
        if not text or len(text.strip()) < 20:
            return {'error': 'Text too short'}
        
        words = text.split()
        word_count = len(words)
        
        # 1. Детекція паттернів
        detected_patterns = self.detect_patterns(text)
        
        # 2. Підрахунок термінів (з усіма категоріями!)
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
        
        # 4. Розрахунок штрафів
        gradient_penalty = self.calculate_gradient_penalties(base_metrics)
        
        # Отримуємо не тільки штраф, а й список конфліктів
        conflict_penalty, conflict_details = self.calculate_conflict_penalty(text)
        
        # Додаємо штраф за кількість конфліктних категорій
        if conflict_details:
            conflict_categories = set()
            for conflict in conflict_details:
                # Визначаємо категорію конфлікту
                if any(term in ['борщ', 'сметана', 'картопля'] for term in conflict['first'] + conflict['second']):
                    conflict_categories.add('food_absurdity')
                if any(term in ['рептилоїд', 'ілюмінат'] for term in conflict['first'] + conflict['second']):
                    conflict_categories.add('conspiracy')
                if any(term in ['5g', 'супутник'] for term in conflict['first'] + conflict['second']):
                    conflict_categories.add('tech_conspiracy')
            
            # Штраф за різноманітність конфліктів
            if len(conflict_categories) >= 2:
                conflict_penalty = min(0.7, conflict_penalty + 0.1)
            if len(conflict_categories) >= 3:
                conflict_penalty = min(0.7, conflict_penalty + 0.15)
        
        contextual_score = self.calculate_contextual_score(text, term_counts, base_metrics)
        
        # 5. Базова оцінка
        base_score = (
            shannon_entropy * 0.12 +
            complexity * 0.08 +
            (term_counts['chaos'] / max(1, word_count)) * 0.20 +
            contextual_score * 0.25 +
            gradient_penalty * 0.20 +
            conflict_penalty * 0.15
        )
        
        # 6. Бонуси за паттерни
        for pattern in detected_patterns:
            base_score += pattern['score_boost']
        
        # 7. Академічний захист
        if term_counts['academic'] >= 2 and term_counts['signal'] >= 2:
            if term_counts['chaos'] == 0:
                base_score *= 0.3
            elif term_counts['chaos'] <= 1:
                base_score *= 0.5
            else:
                base_score *= 0.7
        elif term_counts['academic'] >= 1 and term_counts['signal'] >= 1:
            base_score *= 0.8
        
        # 8. Критичні підвищення
        if conflict_penalty > 0.35:
            base_score = max(base_score, 0.65)
        if contextual_score > 0.4:
            base_score = max(base_score, 0.6)
        
        final_score = min(0.99, max(0.0, base_score))
        
        # 9. Розрахунок індексів
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
        
        # 10. Вердикт
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
        
        # 11. Деталі
        detail_explanations = []
        if gradient_penalty > 0.1:
            detail_explanations.append(f"Градієнтний штраф: {gradient_penalty:.2f}")
        if conflict_penalty > 0.1:
            detail_explanations.append(f"Конфліктний штраф: {conflict_penalty:.2f}")
        if contextual_score > 0.2:
            detail_explanations.append(f"Контекстуальна оцінка: {contextual_score:.2f}")
        
        if detail_explanations:
            explanation += " | " + " + ".join(detail_explanations)

        # 12. Категорії хаосу
        chaos_categories = []
        text_lower = text.lower()
        for category, terms in self.chaos_indicators.items():
            for term in terms:
                if term.lower() in text_lower:
                    if category not in chaos_categories:
                        chaos_categories.append(category)
        
        if chaos_categories:
            explanation += f" | Категорії: {', '.join(chaos_categories[:3])}"
        
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
                'sanity_penalty': sanity_penalty,
                'chaos_categories': chaos_categories,
                'conflict_details': conflict_details[:5]  # Перші 5 конфліктів для аналізу
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
