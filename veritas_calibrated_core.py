"""
Veritas Protocol - Semantic Void Detector v11.0 (LOGICAL INQUISITOR - SYNTHESIZED)
Об'єднана версія з посиленим штрафом за суміжні категорії в одному реченні
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
    """Advanced detector with fine-tuned sensitivity - FOCUS ON CONFLICTS & SENTENCE-LEVEL VIOLATIONS"""
    
    def __init__(self):
        # ============================================================
        # КРИТИЧНІ ПАТТЕРНИ (оригінальні 9)
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
                    r'(обмежений\s+сприйняттия|не\s+здатний\s+побачити|закритий\s+мінд).*?(ключі|двері|опіка|правда)',
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
        # ХАОС-ІНДИКАТОРИ (14 категорій) - ОБ'ЄДНАНА ВЕРСІЯ
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
            ],
            'pseudo_intellectual': [  # НОВА КАТЕГОРІЯ
                'парадигма', 'дискурс', 'наратив', 'конструкт', 'семіозис',
                'трансгресивний', 'деконструкція', 'постмодерн', 'метанаратив',
                'симулякр', 'гіперреальність', 'детеріторіалізація'
            ]
        }
        
        # ============================================================
        # СИГНАЛЬНІ МАРКЕРИ (24) - ОРИГІНАЛ
        # ============================================================
        self.signal_markers = [
            'факт', 'дані', 'показник', 'кількість', 'число', 'статистика',
            'дослідження', 'експеримент', 'результат', 'метод', 'протокол',
            'аналіз', 'модель', 'гипотеза', 'контрольна група', 'виборка',
            'значущість', 'реплікація', 'валідація', 'верифікація',
            'публікація', 'рецензування', 'журнал', 'університет',
            'інститут', 'академія', 'лабораторія',
            'коефіцієнт', 'кореляція', 'відхилення',
            'мета-аналіз', 'p-value', 'confidence interval'
        ]
        
        # ============================================================
        # АКАДЕМІЧНИЙ WHITELIST (35) - ОРИГІНАЛ
        # ============================================================
        self.academic_whitelist = [
            'кореляція', 'верифікація', 'гіпотеза', 'вибірка', 'значущість',
            'нейрони', 'синапси', 'метааналіз', 'статистичний', 'логістика',
            'деескалація', 'макроекономічний', 'інвестиції', 'інфраструктура',
            'ратифікація', 'протокол', 'емпіричний', 'квалітативний', 'кількісний',
            'реплікація', 'валідація', 'контрольна група', 'плацебо', 'рандомізація',
            'когорта', 'мета-аналіз', 'систематичний огляд',
            'опубликовано в', 'peer-reviewed',
            'за даними', 'згідно з дослідженням', 'результати показують',
            'статистично значущий', 'ефект розміру', 'effect size'
        ]
        
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
            
            # УНІВЕРСАЛЬНІ КОНФЛІКТНІ ПАРИ ДЛЯ АБСУРДУ
            (['квантовий', 'квантова', 'квантове', 'квантові', 'ентропія', 'флуктуація', 'тунельний', 'сингулярність', 
              'суперпозиція', 'планк', 'гейзенберг', 'хвильова функція', 'колапс хвильової', 'мультивсесвіт', 
              'кристалізація', 'термодинаміка', 'термодинаміці', 'термодинаміку', 'фізика', 'математика',
              'біологія', 'хімія', 'генетика', 'мікроскоп', 'лабораторія', 'експеримент'],
             ['борщ', 'сметана', 'картопля', 'морква', 'суп', 'їжа', 'кулінарний', 'буряк', 'каструля', 'бульйон', 
              'черпак', 'петрушка', 'кроп', 'морква', 'їсти', 'варити', 'страва', 'обід', 'сніданок', 'вечеря',
              'рецепт', 'кухня', 'продукти', 'продукт', 'їстівний', 'смачний', 'солоний', 'солодкий'], 
             0.45),
            
            (['пінеальний', 'шишкоподібний', 'імунний', 'імунної', 'нанобот', 'наноботів', 'днк', 'генетичний',
              'вакцина', 'вакцинований', 'імунітет', 'клітина', 'організм', 'біологічний', 'медичний',
              'вірус', 'бактерія', 'антитіло', 'гормон', 'нейрон', 'синапс', 'мозок', 'серце', 'печінка',
              'ліки', 'лікування', 'діагноз', 'симптом', 'хвороба', 'здоров\'я'],
             ['5g', 'супутник', 'старлінк', 'блокчейн', 'гейтса', 'водопровідний', 'вода', 'чип', 'мікрочіп',
              'транслюють', 'частоти', 'гц', 'дестабілізує', 'записувати', 'протокол', 'матриця', 'програмування',
              'WiFi', 'радіо', 'телебачення', 'мобільний', 'телефон', 'сітка', 'покриття', 'антена'], 
             0.5),
            
            # Термодинаміка + політика (з твого тесту)
            (['термодинаміка', 'ентропія', 'ізольована система', 'теплова смерть',
              'фізика', 'наука', 'закон', 'теорія', 'формула', 'рівняння'],
             ['політика', 'влада', 'уряд', 'президент', 'вибори', 'демократія',
              'соціальний', 'економічний', 'громадянський', 'суспільний'], 
             0.4),
            
            # Логіка + емоції
            (['логіка', 'раціональний', 'розум', 'інтелект', 'міркування', 'висновок',
              'аргумент', 'доказ', 'обґрунтування', 'послідовність'],
             ['емоції', 'почуття', 'серце', 'інтуїція', 'віра', 'довіра',
              'любов', 'ненависть', 'страх', 'радість', 'сум', 'злість'], 
             0.35),
        ]
        
        # ============================================================
        # ЛОГІЧНІ КОЛАПСИ З МНОЖНИКАМИ (x3, x3.5!) - з першого файлу
        # ============================================================
        self.LOGICAL_COLLAPSE_PAIRS = [
            # Бізнес + Езотерика (НАЙВИЩИЙ множник!)
            (['бізнес', 'ринок', 'прибуток', 'стратегія', 'ефективність', 'менеджмент', 'продажі'],
             ['чакра', 'аура', 'енергія', 'вібрація', 'карма', 'квантовий', 'резонанс'],
             0.75, 3.5),
            
            # Наука + Віра (x3)
            (['наука', 'доказ', 'експеримент', 'гіпотеза', 'теорія', 'методологія'],
             ['віра', 'почуття', 'інтуїція', 'очевидність', 'аксіома', 'відчуття'],
             0.7, 3.0),
            
            # Математика + Містика (x3)
            (['математика', 'формула', 'рівняння', 'обчислення', 'статистика', 'алгоритм'],
             ['душа', 'карма', 'судьба', 'провидіння', 'чудо', 'таємниця'],
             0.65, 3.0),
            
            # Логіка + Емоція (x2.5)
            (['логіка', 'раціональний', 'розум', 'аргумент', 'доказ', 'послідовність'],
             ['емоція', 'серце', 'інтуїція', 'віра', 'відчуття', 'почуття'],
             0.6, 2.5),
            
            # Фізика + Соціальні явища (x2)
            (['фізика', 'термодинаміка', 'ентропія', 'енергія', 'атом', 'молекула'],
             ['суспільство', 'політика', 'культура', 'мораль', 'етика', 'відносини'],
             0.55, 2.0),
        ]
        
        # ============================================================
        # ГРАДІЄНТНІ ШТРАФИ (формули з другого файлу)
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
        # НОВА ФУНКЦІЯ: СИЛЬНИЙ ШТРАФ ЗА КАТЕГОРІЇ В ОДНОМУ РЕЧЕННІ
        # ============================================================
        
    def _calculate_sentence_level_violations(self, text: str) -> tuple:
        """Обчислює штрафи за різні категорії в одному реченні"""
        text_lower = text.lower()
        sentences = re.split(r'[.!?]+', text)
        
        total_penalty = 0.0
        violations = []
        
        # Отримуємо всі терміни з усіх категорій
        all_chaos_terms = {}
        for category, terms in self.chaos_indicators.items():
            for term in terms:
                all_chaos_terms[term] = category
        
        # Перевіряємо кожне речення
        for sentence_idx, sentence in enumerate(sentences):
            if not sentence.strip():
                continue
                
            sentence_lower = sentence.lower()
            found_categories = set()
            found_terms_by_category = {}
            
            # Шукаємо терміни в реченні
            for term, category in all_chaos_terms.items():
                if term in sentence_lower:
                    found_categories.add(category)
                    if category not in found_terms_by_category:
                        found_terms_by_category[category] = []
                    found_terms_by_category[category].append(term)
            
            # Якщо знайшли 2 або більше категорій в одному реченні
            if len(found_categories) >= 2:
                # Базовий штраф: 0.3 за кожну додаткову категорію після першої
                penalty = 0.3 * (len(found_categories) - 1)
                
                # Додатковий штраф за особливо несумісні категорії
                category_list = list(found_categories)
                for i in range(len(category_list)):
                    for j in range(i + 1, len(category_list)):
                        cat1, cat2 = category_list[i], category_list[j]
                        
                        # Особливо сильні штрафи за певні комбінації
                        if ('esoteric' in [cat1, cat2] and 'pseudoscience' in [cat1, cat2]):
                            penalty += 0.2  # Езотерика + псевдонаука
                        if ('political_manipulation' in [cat1, cat2] and 'conspiracy' in [cat1, cat2]):
                            penalty += 0.15  # Політика + змова
                        if ('tech_mystification' in [cat1, cat2] and 'esoteric' in [cat1, cat2]):
                            penalty += 0.25  # Технології + езотерика
                
                total_penalty += penalty
                
                # Збираємо докази
                evidence = []
                for category in found_categories:
                    terms = found_terms_by_category.get(category, [])[:2]
                    evidence.append(f"{category}: {', '.join(terms)}")
                
                violations.append(LogicalViolation(
                    'sentence_category_collision',
                    penalty,
                    evidence,
                    f'Речення #{sentence_idx+1}: {len(found_categories)} несумісних категорій'
                ))
        
        # Тепер перевіряємо суміжні речення (менший штраф)
        for i in range(len(sentences) - 1):
            sentence1 = sentences[i].lower()
            sentence2 = sentences[i + 1].lower()
            
            if not sentence1.strip() or not sentence2.strip():
                continue
            
            # Знаходимо категорії в кожному реченні
            categories1 = set()
            categories2 = set()
            
            for term, category in all_chaos_terms.items():
                if term in sentence1:
                    categories1.add(category)
                if term in sentence2:
                    categories2.add(category)
            
            # Якщо є спільні категорії в суміжних реченнях
            common_categories = categories1.intersection(categories2)
            if common_categories:
                # Менший штраф: 0.15 за кожну спільну категорію
                penalty = 0.15 * len(common_categories)
                total_penalty += penalty
                
                evidence = []
                for category in common_categories:
                    # Шукаємо приклади термінів
                    term_examples = []
                    for term, cat in all_chaos_terms.items():
                        if cat == category and (term in sentence1 or term in sentence2):
                            term_examples.append(term)
                            if len(term_examples) >= 2:
                                break
                    evidence.append(f"{category}: {', '.join(term_examples[:2])}")
                
                violations.append(LogicalViolation(
                    'adjacent_sentence_collision',
                    penalty,
                    evidence,
                    f'Суміжні речення #{i+1}-#{i+2}: спільні категорії'
                ))
        
        return min(total_penalty, 0.8), violations

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
        
        return min(penalty, 0.8), found_conflicts

    def calculate_contextual_score(self, text, term_counts, metrics):
        """Покращена версія з фокусом на хибну логіку"""
        score = 0.0
        words = text.split()
        word_count = len(words)
        text_lower = text.lower()
        
        # 1. НОВЕ: Детекція псевдологічних конструкцій
        pseudo_logic_patterns = [
            (['квантовий', 'ентропія', 'нейтрино', 'ізотоп', 'атом'],
             ['любов', 'ненависть', 'щастя', 'гнів', 'емоції'], 0.4),
            
            (['статистика', 'кореляція', 'ймовірність', 'вибірка'],
             ['душа', 'карма', 'судьба', 'провидення'], 0.38),
            
            (['математика', 'формула', 'рівняння', 'алгоритм'],
             ['духовність', 'просвітлення', 'медитація', 'йога'], 0.35),
            
            (['фізика', 'термодинаміка', 'гравітація', 'магнетизм'],
             ['політика', 'економіка', 'соціум', 'культура'], 0.42),
        ]
        
        for science_terms, nonsense_terms, weight in pseudo_logic_patterns:
            has_science = any(term in text_lower for term in science_terms)
            has_nonsense = any(term in text_lower for term in nonsense_terms)
            if has_science and has_nonsense:
                sentences = re.split(r'[.!?]+', text)
                for sentence in sentences:
                    sentence_lower = sentence.lower()
                    science_in_sentence = any(term in sentence_lower for term in science_terms)
                    nonsense_in_sentence = any(term in sentence_lower for term in nonsense_terms)
                    if science_in_sentence and nonsense_in_sentence:
                        score += weight * 1.2  # +20% за те саме речення
                        break
        
        # 2. ЗАЛИШАЄМО оригінальну логіку
        if term_counts['signal'] == 0:
            if metrics['complexity'] > 0.75:
                score += 0.4
            elif metrics['shannon_entropy'] > 0.75:
                score += 0.3
            else:
                score += 0.15
        
        if term_counts['academic'] > 0 and term_counts['chaos'] > 0:
            academic_ratio = term_counts['academic'] / word_count
            chaos_ratio = term_counts['chaos'] / word_count
            score += 0.35 if chaos_ratio > academic_ratio else 0.2
        
        if any(w in text_lower for w in ['антарктида', 'атлантида', 'аґарта', 'шамбала', 'тартарія']):
            score += 0.4 if term_counts['signal'] == 0 else 0.25
        
        if any(w in text_lower for w in ['облігація', 'криптовалюта', 'банк', 'блокчейн', 'NFT', 'DAO']):
            if any(w in text_lower for w in ['карма', 'потойбічний', 'душа', 'астрал', 'soul', 'spirit']):
                score += 0.45

        if term_counts.get('noise', 0) >= 2:
            caps_words = len([w for w in words if w.isupper() and len(w) > 2])
            score += 0.3 if caps_words >= 2 else 0.15

        tech = ['AI', 'блокчейн', 'blockchain', 'NFT', 'метаверс', 'metaverse', 'алгоритм']
        mystic = ['душа', 'свідомість', 'consciousness', 'карма', 'awakening', 'просвітлення']
        if any(t in text for t in tech) and any(t in text_lower for t in mystic):
            score += 0.35

        med_targets = ['вакцина', 'вакцинація', 'щеплення', 'FDA', 'ВОЗ', 'Big Pharma']
        med_attack = ['скрита правда', 'вони скрывают', 'they hide', 'корупція', 'genocide', 'убиває']
        if any(t.lower() in text_lower for t in med_targets):
            if any(t.lower() in text_lower for t in med_attack):
                score += 0.4

        ai_extreme = ['AI знищить', 'AI спасть', 'суперінтелект', 'сингулярність', 'robot uprising', 'восстание роботів']
        if any(t.lower() in text_lower for t in ai_extreme):
            score += 0.3
        
        if any(t.lower() in text_lower for t in ['рептилоїд', 'ілюмінат', 'більдерберг', 'хімітрейл', '5g']):
            score += 0.25
        
        if any(t.lower() in text_lower for t in ['квантовий', 'торсійний', 'ефір', 'нейтрино']):
            if any(t.lower() in text_lower for t in ['чакра', 'аура', 'вібрація']):
                score += 0.3
        
        return min(score, 0.8)

    def _detect_logical_collapses(self, text: str) -> tuple:
        """Виявляє логічні колапси з множниками (з першого файлу)"""
        total_penalty = 0.0
        violations = []
        text_lower = text.lower()
        
        for first_terms, second_terms, weight, multiplier in self.LOGICAL_COLLAPSE_PAIRS:
            has_first = any(term in text_lower for term in first_terms)
            has_second = any(term in text_lower for term in second_terms)
            
            if has_first and has_second:
                sentences = re.split(r'[.!?]+', text)
                for sentence in sentences:
                    sentence_lower = sentence.lower()
                    first_in_sentence = any(term in sentence_lower for term in first_terms)
                    second_in_sentence = any(term in sentence_lower for term in second_terms)
                    
                    if first_in_sentence and second_in_sentence:
                        penalty = weight * multiplier
                        total_penalty += penalty
                        
                        violations.append(LogicalViolation(
                            'semantic_incoherence',
                            penalty,
                            [first_terms[0], second_terms[0]],
                            f'Логічний колапс: {first_terms[0]} + {second_terms[0]} (x{multiplier})'
                        ))
                        break
        
        return min(total_penalty, 1.0), violations

    def analyze(self, text):
        """Головний метод аналізу з посиленими штрафами за речення"""
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
        
        # 4. Розрахунок ВСІХ штрафів
        gradient_penalty = self.calculate_gradient_penalties(base_metrics)
        conflict_penalty, conflict_details = self.calculate_conflict_penalty(text)
        contextual_score = self.calculate_contextual_score(text, term_counts, base_metrics)
        
        # 5. НОВИЙ: Штрафи за категорії в одному реченні
        sentence_penalty, sentence_violations = self._calculate_sentence_level_violations(text)
        
        # 6. Логічні колапси з множниками
        collapse_penalty, collapse_violations = self._detect_logical_collapses(text)
        
        # 7. Базова оцінка (тепер включаємо sentence_penalty!)
        base_score = (
            shannon_entropy * 0.08 +
            complexity * 0.05 +
            (term_counts['chaos'] / max(1, word_count)) * 0.20 +
            contextual_score * 0.35 +
            gradient_penalty * 0.12 +
            conflict_penalty * 0.40 +
            sentence_penalty * 0.25 +  # Додаємо новий штраф!
            collapse_penalty * 0.30    # Додаємо штраф за логічні колапси
        )
        
        # 8. Бонуси за паттерни
        for pattern in detected_patterns:
            base_score += pattern['score_boost']
        
        # 9. Академічний захист (послаблюємо для абсурдних текстів)
        academic_absurd = False
        if conflict_penalty > 0.3 or sentence_penalty > 0.2:
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
        
        # 10. Критичні підвищення (частіше і жорсткіше)
        if sentence_penalty > 0.3:  # НОВИЙ поріг
            base_score = max(base_score, 0.6)
        
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
        
        # 11. Розрахунок індексів
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

        sanity_penalty = round(conflict_penalty + max(0, gradient_penalty - 0.2) + sentence_penalty, 3)

        noise_marker_count = term_counts.get('noise', 0)
        signal_ratio = 0 if noise_marker_count == 0 else round(noise_marker_count / max(1, signal), 2)
        
        # 12. Вердикт
        if detected_patterns:
            main_pattern = detected_patterns[0]
            status = 'CRITICAL' if final_score > 0.5 else 'WARNING'
            verdict = main_pattern['verdict']
            explanation = main_pattern['explanation']
        elif final_score > 0.6:
            status = 'CRITICAL'
            if sentence_penalty > 0.3:  # НОВА умова
                verdict = 'КРИТИЧНА КАТЕГОРІЙНА КОЛІЗІЯ'
                explanation = 'Множинні несумісні категорії в одному реченні'
            elif conflict_penalty > 0.4:
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
        
        # 13. Деталі (додаємо інформацію про речення)
        detail_explanations = []
        if sentence_penalty > 0.1:  # НОВЕ
            detail_explanations.append(f"Речення: {sentence_penalty:.2f}")
        if gradient_penalty > 0.05:
            detail_explanations.append(f"Градієнт: {gradient_penalty:.2f}")
        if conflict_penalty > 0.1:
            detail_explanations.append(f"Конфлікти: {conflict_penalty:.2f}")
        if contextual_score > 0.15:
            detail_explanations.append(f"Контекст: {contextual_score:.2f}")
        
        if detail_explanations:
            explanation += " | " + " + ".join(detail_explanations)
        
        # 14. Конфліктні пари
        if conflict_details:
            conflict_pairs = []
            for conflict in conflict_details[:3]:
                first_terms = ', '.join(conflict['first'][:2])
                second_terms = ', '.join(conflict['second'][:2])
                conflict_pairs.append(f"{first_terms} vs {second_terms}")
            
            if conflict_pairs:
                explanation += f" | Конфлікти: {'; '.join(conflict_pairs)}"
        
        # 15. Інформація про речення (Нова секція!)
        if sentence_violations:
            sentence_info = []
            for viol in sentence_violations[:2]:
                if 'речення' in viol.context.lower():
                    sentence_info.append(viol.context.split(':')[0])
            
            if sentence_info:
                explanation += f" | Порушення речень: {', '.join(sentence_info)}"
        
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
                'sentence_penalty': round(sentence_penalty, 3),  # НОВЕ
                'collapse_penalty': round(collapse_penalty, 3),  # НОВЕ
                'word_count': word_count,
                'char_count': len(text),
                'academic_markers': term_counts['academic'],
                'chaos_markers': term_counts['chaos'],
                'signal_markers': term_counts['signal'],
                'noise_markers': noise_marker_count,
                'pattern_count': len(detected_patterns),
                'sentence_violations': len(sentence_violations),  # НОВЕ
                'collapse_violations': len(collapse_violations),  # НОВЕ
                'shout_factor': len([w for w in words if w.isupper() and len(w) > 2]) / max(1, word_count),
                'number_density': len(re.findall(r'\d+', text)) / max(1, word_count),
                'signal_ratio': signal_ratio,
                'chaos_index': chaos_index,
                'influence_index': influence_index,
                'sanity_penalty': sanity_penalty,
                'conflict_count': len(conflict_details),
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
