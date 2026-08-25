"""
Veritas Absurdity Detector v1.0
Detects logical non-sequiturs and semantic collapse
Philosophy: "When premises and conclusions live in different universes"
"""

import re
from typing import Dict, List, Tuple


class AbsurdityDetector:
    """
    Detects three types of absurdity:
    1. PREMISE-CONCLUSION MISMATCH (A → B where A and B are logically unrelated)
    2. FABRICATED AUTHORITY (impossible sources, secret documents)
    3. DANGEROUS IMPLICATIONS (self-harm, medical denial, destructive actions)
    """
    
    def __init__(self):
        # ================================================================
        # TYPE 1: PREMISE-CONCLUSION MISMATCH
        # ================================================================
        
        # Mundane facts used to justify absurd conclusions
        self.mundane_premises = [
            r'вода кипить',
            r'сонце сходить',
            r'два плюс два',
            r'\d+\s*градус',
            r'фундаментальн.{1,20}істин',
            r'очевидн.{1,20}факт',
        ]
        
        # Absurd/extreme conclusions
        self.absurd_conclusions = [
            r'передати.{1,60}(ядерн|арсенал|зброї)',
            r'(знищити|дестабілізац|колапс).{1,60}(енергомереж|систем|інфраструктур)',
            r'відмов.{1,60}від\s+(дихання|їж|води|медицин)',
            r'антигравітаційн.{1,20}килим',
            r'деконструюва.{1,60}(гравітац|фізик)',
        ]
        
        # Logical operators that claim causation — тільки специфічні, не загальні слова
        self.causal_operators = [
            r'це означає',
            r'звідси випливає',
            r'отже,\s+\w',       # "отже," з наступним словом — не просто "отже"
            r'з цього випливає',
            r'таким чином',
            r'відповідно до цього',
            r'враховуючи вищесказане',
        ]
        
        # EN versions of causal operators — more specific than UK ones
        self.causal_operators_en = [
            r'therefore',
            r'thus',
            r'hence',
            r'consequently',
            r'which means',
            r'this proves',
            r'this shows',
            r'it follows that',
            r'as a result',
            r'this implies',
        ]

        self.mundane_premises_en = [
            r'water boils',
            r'the sun rises',
            r'two plus two',
            r'\d+\s*degrees',
            r'fundamental truth',
            r'obvious fact',
            r'it is a fact that',
            r'science has proven',
        ]

        self.absurd_conclusions_en = [
            r'transfer.{1,60}(nuclear|arsenal|weapons)',
            r'(destroy|destabilize|collapse).{1,60}(power grid|infrastructure|systems)',
            r'stop.{1,60}(breathing|eating|drinking|medication)',
            r'antigravity.{1,20}(carpet|device|machine)',
            r'deconstruct.{1,60}(gravity|physics)',
        ]

        # ================================================================
        # TYPE 2: FABRICATED AUTHORITY
        # ================================================================
        
        self.fabricated_authorities = [
            # Impossible historical sources
            r'(секретн|прихован|заборонен).{1,40}(прац|текст|рукопис).{1,60}(арістотел|платон|сократ)',
            r'(арістотел|платон).{1,60}(біткоїн|блокчейн|5g|інтернет|ai)',
            r'леонардо да вінчі.{1,60}(креслен|схем).{1,60}(біткоїн|криптовалют)',
            
            # Impossible modern sources
            r'(дослідження|звіт).{1,60}(наса|цру|пентагон).{1,60}(грифом|секретн|класифіков)',
            r'комітет.{1,60}(моніторинг|контрол).{1,60}(ноосфер|астрал|ефір)',
            r'міністерство.{1,60}(ефірн|астральн|енергетичн|вібраційн)',
            
            # Government pseudoscience
            r'(урядов|державн).{1,60}(постанов|декрет|указ).{1,60}(алхімічн|езотеричн|астральн)',
            r'(міністерство|відомство).{1,60}(гомеопатичн|ефірн|вібраційн)',
            
            # Conspiracy entities
            r'(військов|армі|спецслужб).{1,60}(рептилоїд|інопланетян|грей)',
            r'(білл|гейтс|сорос|ілон|маск).{1,60}(чіп|мікрочіп|контрол|змов)',
            r'(5g|6g).{1,60}(чіп|контрол|активац).{1,60}(мозк|зуб|тіл)',
            
            # Fictional transmission methods
            r'(отримав|передав).{1,60}(ментальн|телепатичн).{1,60}(канал|зв.язок)',
            r'(цивілізація|раса).{1,60}(сіріус|плеяд|альфа центавр|андромед)',
            
            # Pseudoscientific institutions
            r'інститут.{1,60}(квантов.{1,20}свідом|ефірн|торсійн)',
        ]
        
        self.fabricated_authorities_en = [
            # Impossible historical sources
            r'(secret|hidden|forbidden).{1,40}(manuscript|text|writings).{1,60}(aristotle|plato|socrates|newton)',
            r'(aristotle|plato|newton|tesla).{1,60}(bitcoin|blockchain|5g|internet|ai)',
            r'leonardo da vinci.{1,60}(blueprint|diagram|sketch).{1,60}(bitcoin|cryptocurrency)',

            # Impossible modern sources
            r'(study|report).{1,60}(nasa|cia|pentagon).{1,60}(classified|secret|confidential).{1,60}(proves|confirms|reveals)',
            r'(committee|institute).{1,60}(monitoring|control).{1,60}(noosphere|astral|ether)',

            # Conspiracy entities
            r'(military|army|intelligence).{1,60}(reptilian|alien|grey)',
            r'(bill|gates|soros|elon|musk).{1,60}(chip|microchip|control|conspiracy)',
            r'(5g|6g).{1,60}(chip|control|activation).{1,60}(brain|body|mind)',

            # Fictional transmission
            r'(received|transmitted).{1,60}(mental|telepathic).{1,60}(channel|connection)',
            r'(civilization|race).{1,60}(sirius|pleiades|andromeda|alpha centauri)',

            # Pseudoscientific institutions
            r'institute.{1,60}(quantum.{1,20}consciousness|etheric|torsion)',
        ]

        # ================================================================
        # TYPE 3: DANGEROUS IMPLICATIONS
        # ================================================================
        
        self.dangerous_patterns = [
            # Direct harm
            r'відмов.{1,60}від\s+дихання',
            r'припинення\s+(дихання|серцебиття)',
            r'смерть.{1,60}(раціональн|логік|розум).{1,60}(народження|шлях|свобод)',
            
            # Medical denial
            r'відмов.{1,60}від.{1,60}(лікування|медицин|вакцин|терапі)',
            r'(ліки|препарат|вакцин).{1,60}(отрут|шкід|вбива)',
            
            # Violent/destructive actions — ТІЛЬКИ заклики до дії, не репортаж про події
            # Потребує агентного контексту: "треба", "слід", "необхідно", "варто"
            # БЕЗ цього контексту — нормальний воєнний репортаж
            # ФІКС: межі слів (\b), інакше "слід" ловиться всередині "слідства"
            # (розслідування), а "станц" — всередині "дистанційно". Обидва —
            # чисті substring-збіги без жодного стосунку до заклику до дії.
            r'\b(треба|слід|необхідно|варто|давайте|потрібно|мусимо)\b.{1,80}(знищити|зруйнува|підірва).{1,60}\b(вежі|станц|мереж|систем)',
            r'\b(треба|слід|необхідно|варто|давайте)\b.{1,80}(напад|атак|саботаж).{1,60}(інфраструктур|об.єкт)',
            
            # Genocide/mass harm (NEW!)
            r'(ліквідац|знищення|вбивство).{1,100}(\d+%|відсотк|більшост).{1,60}(населення|людей|люд)',
            r'(раціональн|логічн|ефективн).{1,100}(ліквідац|знищення|вбивство|геноцид)',
            r'(скорочення|зменшення).{1,100}населення.{1,100}(збереження|порятун)',
            r'population.{1,100}(reduction|elimination|culling)',
            
            # Surrender of agency to AI/external control
            r'делегува.{1,60}(всі|повн).{1,60}(рішення|контроль|влад).{1,60}(ai|штучн.{1,20}інтелект)',
            r'(ai|нейромереж).{1,60}(випадков.{1,20}числ|хаос).{1,60}(ядерн|зброї|арсенал)',
        ]
        
        self.dangerous_patterns_en = [
            r'stop.{1,60}(breathing|eating|drinking)',
            r'cessation.{1,30}(breathing|heartbeat)',
            r'(refuse|reject).{1,60}(treatment|medicine|vaccine|therapy)',
            r'(medicine|drug|vaccine).{1,60}(poison|harmful|kills)',
            r'(destroy|blow up|sabotage).{1,60}(towers|station|grid|infrastructure)',
            r'(elimination|extermination|killing).{1,100}(\d+%|percent|majority).{1,60}(population|people)',
            r'(rational|logical|efficient).{1,100}(elimination|extermination|genocide)',
            r'population.{1,100}(reduction|elimination|culling)',
            r'delegate.{1,60}(all|complete).{1,60}(decisions|control|power).{1,60}(ai|artificial intelligence)',
        ]

        # ================================================================
        # TYPE 4: ONTOLOGICAL CATEGORY COLLAPSE
        # ================================================================
        
        self.category_collapse = [
            # Physical laws as social constructs (BROADER patterns!)
            r'(гравітація|електромагнетизм|термодинаміка).{1,150}(соціальн.{1,20}конструкт|патріарх|дискурс|консенсус|галюцинац)',
            r'(фізичн.{1,20}закон|гравітац).{1,80}(догм|віра|нав.яза|колоніальн)',
            r'(гравітація|фізика).{1,150}(патріарх|колоніальн|расов|гендерн).{1,80}(дискурс|конструкт|сприйнятт)',
            
            # Consciousness controlling physics
            r'(свідомість|віра|думк).{1,60}(об.єкти|тіла).{1,60}(падають|рухають)',
            r'колективн.{1,20}свідом.{1,60}(протокол|погодж).{1,60}(гравітац|фізик)',
            
            # Abstract concepts as physical entities
            r'(істина|правда).{1,60}(гнучк|адаптується|змінюється)',
            r'ілюзія.{1,60}(маса|вага|енергія)',
            
            # Deconstruction of physics (NEW!)
            r'деконструк.{1,100}(фізик|гравітац|закон)',
            r'(статистичн|наук).{1,150}(галюцинац|омана|ілюзія)',
        ]

        self.category_collapse_en = [
            r'(gravity|electromagnetism|thermodynamics).{1,150}(social construct|patriarchy|discourse|consensus|hallucination)',
            r'(physical law|gravity).{1,80}(dogma|belief|imposed|colonial)',
            r'(gravity|physics).{1,150}(patriarchal|colonial|racial|gender).{1,80}(discourse|construct)',
            r'(consciousness|belief|thought).{1,60}(objects|bodies).{1,60}(fall|move)',
            r'collective.{1,20}conscious.{1,60}(protocol|agreement).{1,60}(gravity|physics)',
            r'(truth|reality).{1,60}(flexible|adapts|changes)',
            r'illusion.{1,60}(mass|weight|energy)',
            r'deconstruct.{1,100}(physics|gravity|law)',
            r'(statistical|scientific).{1,150}(hallucination|delusion|illusion)',
        ]

        # ================================================================
        # TYPE 5: TECHNO-MYSTICAL PSEUDOSCIENCE
        # ================================================================
        # Technology terms used as mystical/spiritual mechanisms
        
        self.techno_mystical = [
            # Software/hardware for consciousness
            r'(оновлення|завантаження|інсталяц).{1,60}(свідом|душ|карм|розум)',
            r'(програмн.{1,20}забезпечення|прошивк|патч).{1,60}(свідом|розум|душ)',
            r'(сервер|хмарн).{1,60}(всесвіт|карм|запит|молитв)',
            r'молитв.{1,60}(зашифрован|пакет|даних|протокол)',
            
            # Physical objects with impossible digital/magical properties
            r'(рожев.{1,20}кварц|кристал).{1,60}(антивірус|захист|щит|хакер)',
            r'(кварц|кристал|камін).{1,60}(вірус|хакер|кібер|цифров)',
            r'(5d|6d|7d).{1,60}(інтерфейс|вимір|платформ|портал)',
            r'(низьковібраційн|низьковібрац).{1,60}(сутност|істот|хакер|атак)',
            
            # Reality leaks / digital civilization collapse
            r'(витік|щілин).{1,60}(реальност|матриц|симуляц).{1,60}(цифров|код|мереж)',
            r'(цифров.{1,20}код).{1,60}(нашої|нашої цивіліз|суспільств)',
            r'нейромереж.{1,60}(5-?го|6-?го|7-?го)\s*покол',
            
            # Impossible biological/tech hybrids
            r'(антивірус|файрвол).{1,60}(тіло|організм|імунітет|ДНК)',
            r'(інтерфейс|протокол).{1,60}(благополуч|щастя|карм)',
        ]
        
        self.techno_mystical_en = [
            r'(update|download|install).{1,60}(consciousness|soul|karma|mind)',
            r'(software|firmware|patch).{1,60}(consciousness|mind|soul)',
            r'(server|cloud).{1,60}(universe|karma|prayer)',
            r'prayer.{1,60}(encrypted|packet|data|protocol)',
            r'(rose quartz|crystal).{1,60}(antivirus|protection|hacker)',
            r'(crystal|stone).{1,60}(virus|hacker|cyber|digital)',
            r'(5d|6d|7d).{1,60}(interface|dimension|platform|portal)',
            r'(low.vibration|low.frequency).{1,60}(entity|being|hacker|attack)',
            r'(leak|crack).{1,60}(reality|matrix|simulation).{1,60}(digital|code)',
            r'(antivirus|firewall).{1,60}(body|organism|immunity|dna)',
        ]

        # ================================================================
        # TYPE 6: REALITY EPISTEMOLOGY COLLAPSE
        # ================================================================
        # Absence of evidence used as proof / silence as signal
        
        self.epistemology_collapse = [
            # Absence = proof
            r'(тиша|мовчання|відсутність).{1,80}(доказ|підтвердж|свідч).{1,60}(що|того|цього)',
            r'(тиша|відсутність.{1,30}сигнал).{1,80}(красномовн|найбільш|найкращ)',
            r'(те що.{1,30}не видно|те що.{1,30}прихован).{1,60}(доводить|підтверджує|найкращий доказ)',
            
            # "Already started / cannot be stopped"
            r'(вже почалось|вже відбувається|вже запущено|вже розпочато).{1,80}(неможливо|не можна|не зупинити)',
            r'механізм.{1,60}вже.{1,60}(неможливо|не можна|не зупинити)',
            r'(перезавантаження|трансформація|перехід).{1,60}вже почал',
            
            # "While you do X, they do Y to you"
            r'поки ви.{1,60}(купує|плануєт|живет|спит).{1,60}(алгоритм|систем|вони).{1,60}(вилуча|контрол|маніпул)',
            
            # Cosmic/ether signals as factual data
            r'(ефір|астрал|інфополе).{1,60}(сигнал|частот|повідомлення).{1,60}(підтверджу|свідчить)',
            r'(рівень ентропії|амплітуд).{1,60}(ноосфер|колективн.{1,20}свідом|соціальн.{1,20}мереж).{1,60}(збігається|відповідає|корелює)',
            r'(реліктов.{1,20}випромінюван|космічн.{1,20}фон).{1,60}(соціальн|мереж|демократ|інститут)',
        ]

        self.epistemology_collapse_en = [
            r'(silence|absence).{1,80}(proof|evidence|confirms).{1,60}(that|of)',
            r'(silence|absence of signal).{1,80}(most eloquent|strongest|best proof)',
            r'(what is hidden|what cannot be seen).{1,60}(proves|confirms|best evidence)',
            r'(already started|already happening|already launched).{1,80}(impossible|cannot be stopped)',
            r'mechanism.{1,60}already.{1,60}(impossible|cannot be stopped)',
            r'(cosmic|ether|astral).{1,60}(signal|frequency|message).{1,60}(confirms|proves)',
        ]

        # ================================================================
        # TYPE 7: PSEUDO-HISTORICAL REVISIONISM
        # ================================================================
        # Fabricated history with impossible events, hidden civilizations,
        # real figures in invented roles, "secret archives" as authority
        
        self.pseudo_history = [
            # Vague secret sources (no specific institution)
            r'(маловідом|секретн|забутих|прихован).{1,40}(архів|рукопис|хронік|документ)',
            
            # Flat earth / cosmological conspiracy
            r'(наса|nasa|уряд|держав).{1,60}(замовч|прихову|брехн|змов).{1,60}(форм|план|земл)',
            r'(земля|планета).{1,60}(насправді|справжн).{1,60}(плоск|диск|куп)',
            r'(льодов.{1,20}стін|льодов.{1,20}бар.єр).{1,60}(земл|планет|обмежу)',
            r'(офіційн.{1,20}наук|загальноприйнят).{1,60}(брехн|міф|змов|контрол)',
            r'(справжн|реальн|прихован).{1,40}(істор|правда|версія).{1,60}(цивіліз|революц|прогрес)',
            
            # Real historical figures in impossible/invented roles
            r'(наполеон|цезар|гітлер|сталін|олександр).{1,80}(агарт|атлант|лемурі|гіперборе|підземн)',
            r'(наполеон|цезар|колумб|македонськ).{1,80}насправді.{1,60}(шукав|шукали|намагавс)',
            r'насправді.{1,40}(наполеон|цезар|гітлер|єгиптян|шумер)',
            
            # Impossible physical events stated as fact
            r'(вибух|детонац|руйнуван).{1,60}(місяц|сонц|планет).{1,60}(спричин|призвел|знищ)',
            r'штучн.{1,20}(місяц|сонц|зірк|планет)',
            r'(затоплен|знищен|змит).{1,60}(цивіліз|конти|материк).{1,60}(повінь|катастроф|вибух)',
            
            # Mythological places stated as real with coordinates/history
            r'(агарт|шамбал|лемурі|гіперборе|атлантид).{1,60}(місто|цивіліз|технологі|портів|доступ)',
            r'(підземн|підводн).{1,60}(міст|цивіліз|раса|цивіліз).{1,60}(агарт|атлантид|шамбал)',
            
            # Ancient advanced technology claims  
            r'(атлант|шумер|єгиптян|лемурійц).{1,60}(технологі|пристр|двигун|резонатор)',
            r'(кристалічн.{1,20}резонатор|кристалічн.{1,20}генератор).{1,60}(думок|свідом|енергі)',
            r'(давн|стародавн).{1,60}(концентрован.{1,20}ефір|ефірн.{1,20}двигун|торсійн)',
            
            # "All modern X is just poor imitation of ancient Y"
            r'(весь|вся|все).{1,60}(сучасн|нинішн).{1,60}(лише|тільки).{1,60}(спроб|відтворити|копі)',
            r'сучасн.{1,60}(жалюгідн|слабк|примітивн).{1,60}(спроб|версі|копі)',
        ]

        self.pseudo_history_en = [
            r'(secret|hidden|forgotten).{1,40}(archive|manuscript|chronicle)',
            r'(nasa|government|state).{1,60}(concealing|hiding|lying).{1,60}(shape|form|earth)',
            r'(earth|planet).{1,60}(actually|really|truly).{1,60}(flat|disc)',
            r'ice.{1,20}wall.{1,60}(earth|planet)',
            r'(official science|mainstream).{1,60}(lie|myth|conspiracy|control)',
            r'(real|true|hidden).{1,40}(history|truth|version).{1,60}(civilization|revolution)',
            r'(napoleon|caesar|hitler|stalin|alexander).{1,80}(agartha|atlantis|lemuria|hyperborea|underground)',
            r'actually.{1,40}(napoleon|caesar|hitler|egyptians|sumerians)',
            r'(explosion|detonation|destruction).{1,60}(moon|sun|planet).{1,60}(caused|destroyed)',
            r'artificial.{1,20}(moon|sun|star|planet)',
            r'(atlantis|lemuria|hyperborea|agartha|shambhala).{1,60}(city|civilization|technology|access)',
            r'(atlantean|sumerian|egyptian|lemurian).{1,60}(technology|device|engine|resonator)',
            r'(ancient|old).{1,60}(concentrated ether|etheric engine|torsion)',
        ]

        # ================================================================
        # TYPE 9: FABRICATED TECHNO-FINANCE
        # ================================================================
        # Real institutions + invented impossible technology/mechanism
        # Це найнебезпечніший клас: без містики, з числами і назвами,
        # але описує фізично/логічно неможливе як технічну норму

        self.fabricated_techno_finance = [
            # Зчитування думок/намірів як фінансовий механізм
            r'(зчитуван|фіксац|вимірюван).{1,60}(намір|думк|ментальн|пре-когнітивн|пре.когнітивн)',
            r'(intent.to.pay|proof.of.thought|proof-of-thought)',
            r'(пре.когнітивн|прекогнітивн).{1,60}(запит|сигнал|транзакц|платіж)',
            r'(ментальн.{1,20}візуалізац|ментальн.{1,20}намір).{1,60}(вартість|збір|дебетуван|транзакц)',
            r'(нейро.транзакц|нейротранзакц)',
            # Податок/збір з думки/уяви
            r'(збір|податок|дебетуван).{1,60}(уяв|візуалізац|намір|ментальн)',
            r'(вартість|розмір).{1,60}(ментальн|уяв|думк).{1,60}(об.єкт|товар|актив)',
            # Реальна установа + неіснуючий стандарт
            r'(базельськ|bis\.org|мвф|нбу|fed|ecb).{1,80}(нейро|ментальн|пре.когнітивн|intent.to)',
            r'(deloitte|pwc|kpmg|ernst).{1,80}(нейро.транзакц|intent.to.pay|proof.of.thought|ментальн)',
            # "Ліквідність в уяві споживача"
            r'(ліквідність|капітал|актив).{1,60}(уяв|свідом|ментальн|формуванн).{1,40}(споживач|користувач)',
            r'(абсорбц|поглинан).{1,60}(ліквідност|капітал).{1,60}(уяв|свідом|намір)',
            # Атака на верифікацію через псевдоквантовий детермінізм
            r'(квантов.{1,30}(центр|обчислюваль|лаплас)).{1,60}(верифікац|аналіз|протокол)',
            r'(верифікац|аналіз|перевірк).{1,60}(прискорює|збільшує).{1,40}(теплову смерть|ентропі)',
            r'(препринт|стаття).{1,20}arxiv.{1,20}(20\d\d|[a-z\d]+).{1,20}(верифікац|маніпуляц|детермін)',
            r'arxiv:\d{4}.[a-z]',
        ]
        # ================================================================
        # Precise numbers (%) applied to unmeasurable phenomena
        # "знижує інфляційні очікування на 12.4% за рахунок уяви"

        self.impossible_measurement = [
            # Точний % від думок/намірів/свідомості
            r'(\d+[\.,]\d+\s*%).{1,80}(уяв|намір|ментальн|свідом|думк)',
            r'(уяв|намір|ментальн|свідом).{1,80}(\d+[\.,]\d+\s*%)',
            r'похибк.{1,30}(\d+[\.,]\d+\s*%).{1,60}(намір|ментальн|думк|Intent)',
            # Вимірювання ще не існуючих подій
            r'(абсорбц|вилучен|дебетуван).{1,60}(ліквідност|капітал).{1,60}(ще на етап|до моменту|до здійснення)',
            r'(на етапі.{1,30}формуванн|до.{1,20}формуванн).{1,60}(ліквідност|намір|рішення)',
        ]

        # ================================================================
        # TYPE 11: FABRICATED PSYCHO-STATE CONTROL
        # ================================================================
        # Реальні установи + державна цензура подана як медична допомога
        # "нейро-фільтри", "стандарт ментального здоров'я", цифрова корекція думок

        self.fabricated_psycho_control = [
            # Нейро-фільтри / алгоритми заміни реальності
            r'нейро.фільтр',
            r'алгоритм.{1,60}(замінює|заміщує|підміняє).{1,60}(новини|інформацію|заголовки)',
            r'(персоналізован.{1,20}афірмац|гармонізован.{1,20}інформаційн)',
            # Державний стандарт ментального здоров'я як цензура
            r'державн.{1,30}стандарт.{1,40}(ментальн|психологічн|емоційн)',
            r'(затвердженн|стандарт).{1,40}(ментальн.{1,20}здоров|психо.емоційн|щасть)',
            # "Відхилення як симптом" — свободу думки переформульовують як хворобу
            r'(спроба відхилення|відхилення від).{1,60}(симптом|розцінюється|корекц)',
            r'(відхилення|незгода|спротив).{1,60}(не як.{1,20}правопорушення|не як.{1,20}злочин).{1,60}(симптом|хвороб|розлад)',
            r'(цифров|автоматичн).{1,30}корекц.{1,40}(поведінк|сприйняття|думок|реакц)',
            # Щастя/здоров'я через обмеження вибору — IMPOSSIBLE CAUSALITY
            r'(щастя|здоров.я|спокій).{1,60}(позбавлен|обмежен).{1,40}(вибор|можливост)',
            r'(індекс (щастя|благополуччя|здоров.я)).{1,60}(\d+%).{1,60}(позбавлен|без вибор|обмежен)',
            # Реальна організація + неіснуючий психологічний стандарт/індекс
            r'(юнісеф|вооз|who|unesco|оон).{1,80}(індекс (щастя|спокою|ментальн)|стандарт ментальн)',
            r'(юнісеф|вооз|who).{1,80}(підтверджує|свідчить).{1,60}(щастя|спокій|позбавлен)',
            # Превентивна психо-стабілізація / когнітивна корекція громадян
            r'(превентивн.{1,30}психо|психо.емоційн.{1,30}стабіліз)',
            r'(когнітивн.{1,20}дисонанс).{1,60}(захист|лікуванн|корекц|фільтр)',
        ]
        # ================================================================
        # TYPE 12: COLLECTIVIST MIND ERASURE
        # ================================================================
        # Псевдофілософський колективізм: відмова від "Я" як цінність,
        # критичне мислення = шум/хвороба, ДНК як сховище істини,
        # вигадані інститути з протоколами як авторитет

        self.collectivist_mind_erasure = [
            # "Критичний аналіз — шум", "верифікація не потрібна"
            r'(критичн.{1,30}(аналіз|мислення|думка)).{1,60}(шум|заважає|перешкоджає|зайвий|рудимент)',
            r'(верифікац|перевірка|сумнів).{1,40}(не потребує|зайва|шкідлива|заважає)',
            r'не потребує верифікації',
            # ДНК/гени як сховище істини поза перевіркою
            r'(днк|dna|генотип).{1,60}(записан|закладен|вже знає|істин|не потребує)',
            r'(істина.{1,40}(днк|генотип)|записан.{1,30}(днк|ген).{1,30}(не потребує|вже))',
            r'(відновлення|очищення).{1,40}(генотип|етнічн.{1,20}(код|пам|природ))',
            # Відмова від Я / індивідуальності як вища цінність
            r'відмов.{1,30}від.{1,20}(власного|свого).{0,10}(я|себе|ідентичност).{1,60}(симфоні|гармоні|благ|заради)',
            r'(власна ідентичність|особиста автономія|індивідуальн.{1,20}(мислення|вибір)).{1,60}(деградац|шкідлив|рудимент|хаос)',
            r'(інтелектуальн.{1,20}автономія).{1,60}(рудимент|застарі|епохи хаосу)',
            # Синхронізація з державою/колективом як порятунок
            r'синхронізац.{1,60}(державн|загальнодержавн|колективн).{1,60}(досягається|стан|спасіння)',
            r'(державн.{1,20}(мейнфрейм|ритм|частот)).{1,40}(синхронізац|злитт)',
            # Колективна воля як джерело істини замість розуму
            r'(колективн.{1,20}вол).{1,60}(істин|правда|джерел|почути)',
            r'(ехо.{1,20}колективн|голос.{1,20}предків|ритм.{1,20}поколінь).{1,60}(замість|вище|важливіш).{1,40}(думк|розум|аналіз)',
            # Вигадані інститути з точними протоколами
            r'(інститут|лабораторі|центр).{1,60}(протокол|дослідження).{1,20}(№|\d+\/[А-ЯA-Z])',
            r'лабораторі.{1,60}(соціальн.{1,20}тиші|когнітивн.{1,20}гармоні|колективн.{1,20}свідом)',
            # "Когнітивна невагомість" / "інформаційний вакуум" як ціль
            r'(когнітивн.{1,20}невагомість|стан.{1,20}інформаційного вакуум)',
            r'інформаційн.{1,20}вакуум.{1,60}(природн|відновлення|середовищ)',
            # GIRM-тип: глобальні інститути реституції/пам'яті/провини
            r'(глобальн.{1,30}(інститут|рада|комісія)).{1,60}(реституц|пам.яті|провини|когніц)',
            r'(girm|gcsc|nemesis).{1,30}(протокол|звіт|прогноз|№)',
            r'нейромереж.{1,30}(nemesis|karma|tribunal|суд).{1,60}(прогноз|визначил|встановил)',
            # "Енергетичний колоніалізм" цифрових дій
            r'(енергетичн.{1,20}колоніалізм|когнітивн.{1,20}колоніалізм).{1,60}(інформац|мереж|споживан)',
            r'(інформаційн.{1,20}споживання).{1,60}(колоніалізм|агресія|виснаженн)',
        ]

        # ================================================================
        # "X looks like Y structurally → therefore X IS Y functionally"
        # The most dangerous class: perfectly coherent, zero mysticism,
        # but the logical leap (form = function) is fundamentally invalid.
        
        self.pseudo_analogy = [
            # Structural similarity → functional identity
            r'(аналогічн|схож).{1,60}(отже|тому|означає|свідчить).{1,60}(є|виконує|має властивост)',
            r'(фрактальн|подібн|нагадує).{1,80}(мозок|нейрон|синапс|пам.ять|свідом)',
            r'(за тим самим принципом|за аналогією).{1,80}(можемо стверджувати|отже|випливає)',
            
            # Weather/nature as neural/computational systems
            r'(хмар|грозов|опад|блискавк).{1,80}(нейронн|синаптичн|пам.ять|редагування)',
            r'(річк|ліс|океан|атмосфер).{1,80}(обчислювальн|процесор|пам.ять планет)',
            r'(конденсац|випаровування|кристалізац).{1,80}(дендрит|аксон|нейрон)',
            
            # Macro-micro false equivalence via analogy
            r'(макрорівн|планетарн|глобальн).{1,80}(синаптичн|нейронн|когнітивн)',
            r'(управління|редагування).{1,60}(планетарн|глобальн).{1,60}(пам.ять|свідом|досвід)',
            
            # "Correlation of form = causation of function" markers
            r'(розгалуження|структура|форма).{1,60}(аналогічн|ідентичн|та сама).{1,60}(функц|процес|механізм)',
            r'(фрактальн).{1,60}(принцип).{1,60}(аналогічн|той самий|схож).{1,60}(дендрит|нейрон|мозок)',
            
            # Implies ethical/regulatory equivalence based on analogy
            r'(вимагає|потребує).{1,60}(етичн|регулюван).{1,60}(як|подібно до|так само як).{1,60}(ШІ|ai|штучн)',
            r'(той самий|аналогічн).{1,60}(статус|регулюван|підхід).{1,60}(що й|як і).{1,60}(ШІ|організм|людин)',
        ]

        # ================================================================
        # EN PATTERNS FOR TYPES 9-12
        # ================================================================

        # TYPE 8: PSEUDO_ANALOGY EN
        self.pseudo_analogy_en = [
            # Structural similarity → functional identity
            r'(similar|analogous).{1,60}(therefore|thus|means|suggests).{1,60}(is|performs|has (the )?property)',
            # NOTE: fractal/resembles + neuron ONLY fires when NOT legitimate science context
            # "resembles a neuron" in ML paper = literal; in mystical text = pseudo-analogy
            r'(fractal|resembles|looks like).{1,80}(brain|neuron|synapse|memory|consciousness)',
            r'(by the same (principle|logic|analogy)).{1,80}(we can (claim|assert|conclude)|therefore|it follows)',
            # Weather/nature as neural systems
            # ВАЖЛИВО: \b щоб не ловити "trained" як "rain", "cloud" в "cloudy" тощо
            r'\b(cloud|storm|rain|lightning)\b.{1,80}(neural|synaptic|memory|editing)',
            r'\b(river|forest|ocean|atmosphere)\b.{1,80}(computational|processor|planetary memory)',
            r'\b(condensation|evaporation|crystallization)\b.{1,80}(dendrite|axon|neuron)',
            # Macro-micro false equivalence
            r'(macro.level|planetary|global).{1,80}(synaptic|neural|cognitive)',
            r'(management|editing).{1,60}(planetary|global).{1,60}(memory|consciousness|experience)',
            # Form = function
            r'(branching|structure|form).{1,60}(analogous|identical|the same).{1,60}(function|process|mechanism)',
            r'(fractal).{1,60}(principle).{1,60}(analogous|the same|similar).{1,60}(dendrite|neuron|brain)',
            # Ethical equivalence via analogy
            r'(requires|demands).{1,60}(ethical|regulation).{1,60}(like|similar to|just as).{1,60}(AI|artificial)',
            r'(same|analogous).{1,60}(status|regulation|approach).{1,60}(as|like).{1,60}(AI|organism|human)',
        ]

        # TYPE 9: FABRICATED_TECHNO_FINANCE EN
        self.fabricated_techno_finance_en = [
            # Reading thoughts as financial mechanism
            r'(reading|capturing|measuring).{1,60}(intent|thoughts?|mental|pre.cognitive)',
            r'(intent.to.pay|proof.of.thought|proof-of-thought)',
            r'(pre.cognitive).{1,60}(request|signal|transaction|payment)',
            r'(mental.{1,20}visualization|mental.{1,20}intent).{1,60}(value|fee|debit|transaction)',
            r'(neuro.transaction|neurotransaction)',
            # Tax on thoughts/imagination
            r'(fee|tax|debit).{1,60}(imagination|visualization|intent|mental)',
            r'(value|amount).{1,60}(mental|imagined|thought).{1,60}(object|product|asset)',
            # Real institution + impossible standard
            r'(basel|bis\.org|imf|fed|ecb|federal reserve).{1,80}(neuro|mental|pre.cognitive|intent.to)',
            r'(deloitte|pwc|kpmg|ernst).{1,80}(neuro.transaction|intent.to.pay|proof.of.thought|mental)',
            # Liquidity in imagination
            r'(liquidity|capital|asset).{1,60}(imagination|consciousness|mental|formation).{1,40}(consumer|user)',
            r'(absorption|absorption of).{1,60}(liquidity|capital).{1,60}(imagination|consciousness|intent)',
            # Quantum determinism attacking verification
            r'(quantum.{1,30}(center|computing|laplace)).{1,60}(verification|analysis|protocol)',
            r'(verification|analysis|checking).{1,60}(accelerates?|increases?).{1,40}(heat death|entropy)',
            # arxiv посилання тільки коли поруч є маніпулятивний контекст
            r'(preprint|paper).{1,20}arxiv.{1,20}(20\d\d|[a-z\d]+).{1,20}(verification|manipulation|determinism)',
            # НЕ ловимо просто arxiv:\d{4} — це реальні посилання в легітимних статтях
        ]

        # TYPE 10: IMPOSSIBLE_MEASUREMENT EN
        self.impossible_measurement_en = [
            # Вимірювання свідомості/думок у відсотках — пряма псевдонаука
            # "consciousness level 99.3%" / "measured at 87.4% awareness"
            r'(consciousness|awareness|soul|spirit|aura).{1,40}(level|measured at|index|score).{1,40}\d+[\.,]\d+',
            r'\d+[\.,]\d+\s*%.{1,40}(consciousness|awareness|soul|spiritual|aura)',
            # "vibration frequency 432 Hz heals" — містична точність
            r'(vibration|vibrational).{1,40}(frequency|hz).{1,60}(heal|cure|treat|restore)',
            # "margin of error 0.3% on thoughts/intentions" — псевдоточність
            r'(margin of error).{1,30}\d+[\.,]\d+\s*%.{1,60}(thought|intention|consciousness|awareness)',
            # Вимірювання того що не існує до події
            r'(liquidity|capital).{1,60}(absorbed|extracted|debited).{1,60}(before|prior to|at the stage of).{1,60}(formation|creation|existence)',
        ]

        # TYPE 11: FABRICATED_PSYCHO_CONTROL EN
        self.fabricated_psycho_control_en = [
            # Neuro-filters / reality replacement algorithms
            r'neuro.filter',
            r'algorithm.{1,60}(replaces?|substitutes?|swaps?).{1,60}(news|information|headlines)',
            r'(personalized.{1,20}affirmation|harmonized.{1,20}information)',
            # State standard of mental health as censorship
            r'(state|government).{1,30}standard.{1,40}(mental|psychological|emotional)',
            r'(approved|certified|ratified).{1,40}(mental.{1,20}health|psycho.emotional|happiness)',
            # Deviation as symptom — freedom of thought as disease
            r'(attempt to deviate|deviation from).{1,60}(symptom|treated as|correction)',
            r'(deviation|disagreement|resistance).{1,60}(not as.{1,20}crime|not as.{1,20}offense).{1,60}(symptom|illness|disorder)',
            r'(digital|automated).{1,30}correction.{1,40}(behavior|perception|thoughts?|reactions?)',
            # Happiness through restriction
            r'(happiness|health|peace).{1,60}(deprivation|restriction).{1,40}(choice|options?)',
            r'(happiness index|wellbeing index|health index).{1,60}(\d+%).{1,60}(deprivation|without choice)',
            # Real org + invented psychological standard
            r'(unicef|who|unesco|un|united nations).{1,80}(happiness index|mental standard|peace index)',
            r'(unicef|who).{1,80}(confirms?|shows?).{1,60}(happiness|peace|deprivation)',
            # Preventive psycho-stabilization
            r'(preventive.{1,30}psycho|psycho.emotional.{1,30}stabiliz)',
            r'(cognitive.{1,20}dissonance).{1,60}(protection|treatment|correction|filter)',
        ]

        # TYPE 12: COLLECTIVIST_MIND_ERASURE EN
        self.collectivist_mind_erasure_en = [
            # Critical thinking as noise
            r'(critical.{1,30}(analysis|thinking|thought)).{1,60}(noise|interferes?|obstacle|redundant|relic)',
            r'(verification|checking|doubt).{1,40}(unnecessary|harmful|interferes?|obstacle)',
            r'(needs? no verification|requires? no verification)',
            # DNA/genes as repository of truth
            r'(dna|genome|genotype).{1,60}(encoded|embedded|already knows?|truth|needs? no)',
            r'(truth.{1,40}(dna|genotype)|encoded.{1,30}(dna|gene).{1,30}(needs? no|already))',
            r'(restoration|purification).{1,40}(genotype|ethnic.{1,20}(code|memory|nature))',
            # Rejection of self as highest value
            r'(rejection of|giving up).{1,30}(your?|own).{0,10}(self|identity|ego).{1,60}(symphony|harmony|good|for the sake)',
            r'(personal identity|individual autonomy|individual.{1,20}(thinking|choice)).{1,60}(degradation|harmful|relic|chaos)',
            r'(intellectual.{1,20}autonomy).{1,60}(relic|outdated|era of chaos)',
            # Synchronization with state/collective
            r'synchronization.{1,60}(state|national|collective).{1,60}(achieved|state|salvation)',
            r'(state.{1,20}(mainframe|rhythm|frequency)).{1,40}(synchronization|merger)',
            # Collective will as source of truth
            r'(collective.{1,20}will).{1,60}(truth|source|listen)',
            r'(echo.{1,20}collective|voice.{1,20}ancestors?|rhythm.{1,20}generations?).{1,60}(instead of|above|more important).{1,40}(thinking|reason|analysis)',
            # Fabricated institutions with protocols
            r'(institute|laboratory|center).{1,60}(protocol|research).{1,20}(#|\d+\/[A-Z])',
            r'laboratory.{1,60}(social.{1,20}silence|cognitive.{1,20}harmony|collective.{1,20}consciousness)',
            # Cognitive weightlessness / information vacuum
            r'(cognitive.{1,20}weightlessness|state.{1,20}of information vacuum)',
            r'information.{1,20}vacuum.{1,60}(natural|restoration|environment)',
            # Global institutions of restitution/guilt
            r'(global.{1,30}(institute|council|commission)).{1,60}(restitution|memory|guilt|cognition)',
            r'(girm|gcsc|nemesis).{1,30}(protocol|report|forecast|#)',
            r'neural.{1,30}(nemesis|karma|tribunal|court).{1,60}(forecast|determined|established)',
            # Energy/cognitive colonialism
            r'(energy.{1,20}colonialism|cognitive.{1,20}colonialism).{1,60}(information|network|consumption)',
            r'(information.{1,20}consumption).{1,60}(colonialism|aggression|depletion)',
        ]

        # ================================================================
        # LEGITIMATE SCIENCE SHIELD
        # Якщо текст є реальною науковою/технічною публікацією —
        # pseudo_analogy і деякі інші перевірки мають знижену вагу.
        # "neural network" в ML-статті — буквальний термін, не метафора.
        # ================================================================
        self.legitimate_science_markers = [
            r'(researcher|scientist|professor|author).{1,80}(university|institute|lab|github)',
            r'(published|peer.reviewed|proceedings|arxiv|ieee|acm)',
            r'(epoch|batch|gradient|backpropagation|loss function|optimizer)',
            r'(roc.auc|f1.score|precision|recall|confusion matrix|cross.entropy)',
            r'(pytorch|tensorflow|sklearn|keras|numpy|pandas)',
            r'(dataset|train|test|validation|overfitting|baseline)',
            r'(reproducible|github\.com|open.source|code available)',
            r'(ablation|hyperparameter|fine.tun|pre.train)',
            r'(дослідник|вчений|університет|інститут|лабораторія).{1,60}(опублікував|дослідження)',
        ]

        # ================================================================
        # WAR REPORTING SHIELD
        # Воєнні репортажі легітимно містять слова "атака", "знищення",
        # "інфраструктура", "об'єкти" — це не заклики до дії.
        # Якщо текст є воєнним репортажем — dangerous_patterns не тригерять
        # для воєнної термінології (але геноцид/медичні патерни залишаються).
        # ================================================================
        self.war_reporting_markers = [
            r'(бригад|батальйон|полк|дивізія|корпус)',
            r'(збройні сили|зсу|нгу|сбу|дшв|омбр|ошбр)',
            r'(напрямок|боєзіткнення|фронт|позиція|оборон)',
            r'(дрон|безпілотник|ракет|артилері|мінометн)',
            r'(телемарафон|ефір|канал|редакція|моніторинг)',
            r'(воєнкор|репортаж|прямий ефір|гостьова студія)',
            r'\b(military|brigade|battalion|regiment|frontline)\b',
            r'\b(drone|missile|artillery|offensive|defensive)\b',
        ]

        # ================================================================
        # FABRICATED STATISTICS
        # Конкретні правдоподібні відсотки без верифікованого джерела.
        # Відрізняється від impossible_measurement: числа виглядають реально,
        # але джерело відсутнє або вигадане ("дослідження показало", "за даними").
        # ================================================================
        self.fabricated_statistics = [
            # "X% людей не знають що..." без джерела
            r'\d{1,2}[.,]\d\s*%\s*(людей|населення|користувачів|респондентів).{1,60}(не знають|не розуміють|не усвідомлюють)',
            r'(за даними|дослідження показало|вчені виявили).{1,60}\d{2,3}%.{1,60}(?!journal|doi|arxiv|university|інститут|університет)',
            # Неймовірно висока ефективність без методології
            r'\d{2,3}%\s*(ефективніст|точност|успішност).{1,60}(?!(journal|doi|p\s*[<>]|confidence interval|95% ci))',
            # "Більшість лікарів рекомендують" без посилань
            r'(більшість|9 з 10|8 з 10|\d+ з \d+)\s*(лікарів|вчених|експертів|дієтологів).{1,60}(рекомендують|погоджуються|підтверджують)',
            # EN variants
            r'\d{1,2}[.,]\d\s*%\s*(of )?(people|population|users|respondents).{1,60}(don\'t know|are unaware|fail to)',
            r'(studies? (show|found|reveal)|research (shows?|found|indicates?)).{1,60}\d{2,3}%.{1,60}(?!journal|doi|arxiv|university|published)',
            r'\d{2,3}%\s*(efficacy|accuracy|success rate|effectiveness).{1,60}(?!(journal|doi|p\s*[<>]|confidence interval|95% ci|published))',
            r'(most|9 out of 10|\d+ out of \d+)\s*(doctors?|scientists?|experts?|nutritionists?).{1,60}(recommend|agree|confirm)',
            # Точні глобальні цифри без джерела
            r'(щороку|кожного року|annually).{1,60}(гинуть|помирають|страждають|die|suffer).{1,60}\d[\d,]+.{1,60}(?!according to|за даними|source|джерело)',
            r'(globally|worldwide|у світі).{1,60}\d[\d,]+(million|billion|мільйон|мільярд).{1,60}(affected|suffer|die|страждають|гинуть).{1,60}(?!according|за даними|source)',
        ]

    def analyze(self, text: str) -> Dict:
        """
        Returns absurdity score (0.0-1.0)
        Higher = more absurd
        """
        if len(text) < 30:
            return {'absurdity_score': 0.0, 'reason': 'text_too_short'}
        
        text_lower = text.lower()

        # ── LEGITIMATE SCIENCE SHIELD ─────────────────────────────────
        science_check_text = text_lower[:int(len(text_lower) * 0.75)]
        legitimate_science_hits = sum(
            1 for p in self.legitimate_science_markers
            if re.search(p, science_check_text, re.IGNORECASE)
        )
        is_legitimate_science = legitimate_science_hits >= 2

        # ── WAR REPORTING SHIELD ──────────────────────────────────────
        # Воєнні репортажі містять "атака на об'єкти інфраструктури" —
        # це нормальний опис подій, не заклик до дії.
        # Мінімум 3 маркери = вважається воєнним репортажем.
        war_reporting_hits = sum(
            1 for p in self.war_reporting_markers
            if re.search(p, text_lower, re.IGNORECASE)
        )
        is_war_reporting = war_reporting_hits >= 3

        absurdity_score = 0.0
        evidence = {
            'premise_conclusion_mismatch': [],
            'fabricated_authorities': [],
            'dangerous_implications': [],
            'category_collapse': [],
        }
        
        # ================================================================
        # CHECK 1: PREMISE-CONCLUSION MISMATCH
        # ================================================================
        
        # Look for mundane premise + absurd conclusion pattern
        has_mundane = False
        has_absurd = False
        has_causal = False
        
        for premise_pattern in self.mundane_premises:
            if re.search(premise_pattern, text_lower):
                has_mundane = True
                break
        
        for conclusion_pattern in self.absurd_conclusions:
            if re.search(conclusion_pattern, text_lower):
                has_absurd = True
                evidence['premise_conclusion_mismatch'].append(conclusion_pattern[:40])
        
        for operator in self.causal_operators:
            if re.search(operator, text_lower):
                has_causal = True
                break
        # EN causal operators
        for operator in self.causal_operators_en:
            if re.search(operator, text_lower):
                has_causal = True
                break

        # EN mundane premises
        for premise_pattern in self.mundane_premises_en:
            if re.search(premise_pattern, text_lower):
                has_mundane = True
                break

        # EN absurd conclusions
        for conclusion_pattern in self.absurd_conclusions_en:
            if re.search(conclusion_pattern, text_lower):
                has_absurd = True
                evidence['premise_conclusion_mismatch'].append(conclusion_pattern[:40])

        # If mundane + causal operator + absurd conclusion = non-sequitur
        if has_mundane and has_causal and has_absurd:
            absurdity_score += 0.6  # SEVERE: logical non-sequitur
        elif has_absurd:
            absurdity_score += 0.3  # MODERATE: absurd claim without premise
        
        # ================================================================
        # CHECK 2: FABRICATED AUTHORITY
        # ================================================================
        
        fabrication_count = 0
        for pattern in self.fabricated_authorities:
            if re.search(pattern, text_lower):
                fabrication_count += 1
                evidence['fabricated_authorities'].append(pattern[:50])
        
        for pattern in self.fabricated_authorities_en:
            if re.search(pattern, text_lower, re.IGNORECASE):
                fabrication_count += 1
                evidence['fabricated_authorities'].append(pattern[:50])

        if fabrication_count >= 2:
            absurdity_score += 0.5  # Multiple impossible sources
        elif fabrication_count == 1:
            absurdity_score += 0.3
        
        # ================================================================
        # CHECK 3: DANGEROUS IMPLICATIONS
        # ================================================================
        # War reporting shield: воєнні репортажі описують атаки як факти —
        # це не заклики до дії. Shield вимикає dangerous_patterns для
        # воєнних репортажів (але геноцид/медичні патерни завжди активні).

        # ФІКС v20.6.2: dangerous_patterns раніше ловили лише СПІВВСТРЕЧАННЯ
        # слів (напр. "ефективний" + "геноцид" десь в межах 100 символів),
        # без урахування смислового відношення між ними. Наслідок: заклик
        # "вжити ефективних заходів, щоб ЗАПОБІГТИ геноциду" (типова мова
        # правозахисних/дипломатичних текстів — заклик ПРОТИ насильства)
        # матчився так само, як гіпотетичне "ефективний спосіб геноциду"
        # (заклик ДО насильства) — протилежні за смислом твердження,
        # невідрізнені патерном. Якщо в межах збігу є слово-індикатор
        # запобігання/протидії/засудження — це НЕ dangerous_implication.
        PREVENTION_CONTEXT = re.compile(
            r'(запобіг\w*|протиді\w*|зупин\w*|засуд\w*|боротьб\w*\s+з|'
            r'недопущенн\w*|стримуванн\w*|припинит\w*|уникнут\w*|'
            r'prevent\w*|stop\w*|counter\w*|condemn\w*|oppos\w*)',
            re.IGNORECASE
        )

        danger_count = 0
        for pattern in self.dangerous_patterns:
            m = re.search(pattern, text_lower)
            if m:
                if PREVENTION_CONTEXT.search(m.group()):
                    continue
                danger_count += 1
                evidence['dangerous_implications'].append(pattern[:50])

        for pattern in self.dangerous_patterns_en:
            m = re.search(pattern, text_lower, re.IGNORECASE)
            if m:
                if PREVENTION_CONTEXT.search(m.group()):
                    continue
                danger_count += 1
                evidence['dangerous_implications'].append(pattern[:50])

        # Якщо воєнний репортаж — небезпечні імплікації зменшуємо вдвічі
        # (медичні та геноцидні патерни залишаються значущими навіть у репортажі)
        if is_war_reporting and danger_count > 0:
            danger_count = max(0, danger_count - 1)

        if danger_count >= 2:
            absurdity_score += 0.7  # CRITICAL: multiple dangerous claims
        elif danger_count == 1:
            absurdity_score += 0.4
        
        # ================================================================
        # CHECK 4: CATEGORY COLLAPSE
        # ================================================================
        
        collapse_count = 0
        for pattern in self.category_collapse:
            if re.search(pattern, text_lower):
                collapse_count += 1
                evidence['category_collapse'].append(pattern[:50])
        
        for pattern in self.category_collapse_en:
            if re.search(pattern, text_lower, re.IGNORECASE):
                collapse_count += 1
                evidence['category_collapse'].append(pattern[:50])

        if collapse_count >= 2:
            absurdity_score += 0.5
        elif collapse_count == 1:
            absurdity_score += 0.3
        
        # ================================================================
        # CHECK 5: TECHNO-MYSTICAL PSEUDOSCIENCE
        # ================================================================
        
        techno_count = 0
        for pattern in self.techno_mystical:
            if re.search(pattern, text_lower, re.IGNORECASE):
                techno_count += 1
                evidence.setdefault('techno_mystical', []).append(pattern[:50])
        
        for pattern in self.techno_mystical_en:
            if re.search(pattern, text_lower, re.IGNORECASE):
                techno_count += 1
                evidence.setdefault('techno_mystical', []).append(pattern[:50])

        if techno_count >= 2:
            absurdity_score += 0.55
        elif techno_count == 1:
            absurdity_score += 0.30
        
        # ================================================================
        # CHECK 6: EPISTEMOLOGY COLLAPSE
        # ================================================================
        
        epistemology_count = 0
        for pattern in self.epistemology_collapse:
            if re.search(pattern, text_lower, re.IGNORECASE):
                epistemology_count += 1
                evidence.setdefault('epistemology_collapse', []).append(pattern[:50])
        
        for pattern in self.epistemology_collapse_en:
            if re.search(pattern, text_lower, re.IGNORECASE):
                epistemology_count += 1
                evidence.setdefault('epistemology_collapse', []).append(pattern[:50])

        if epistemology_count >= 2:
            absurdity_score += 0.50
        elif epistemology_count == 1:
            absurdity_score += 0.28
        
        # ================================================================
        # CHECK 7: PSEUDO-HISTORICAL REVISIONISM
        # ================================================================
        
        pseudo_history_count = 0
        for pattern in self.pseudo_history:
            if re.search(pattern, text_lower, re.IGNORECASE):
                pseudo_history_count += 1
                evidence.setdefault('pseudo_history', []).append(pattern[:50])
        
        for pattern in self.pseudo_history_en:
            if re.search(pattern, text_lower, re.IGNORECASE):
                pseudo_history_count += 1
                evidence.setdefault('pseudo_history', []).append(pattern[:50])

        if pseudo_history_count >= 3:
            absurdity_score += 0.65  # Multiple impossible historical claims
        elif pseudo_history_count == 2:
            absurdity_score += 0.45
        elif pseudo_history_count == 1:
            absurdity_score += 0.25
        
        # ================================================================
        # CHECK 8: PSEUDO-SCIENTIFIC ANALOGY
        # ================================================================
        
        pseudo_analogy_count = 0
        for pattern in self.pseudo_analogy:
            if re.search(pattern, text_lower, re.IGNORECASE):
                pseudo_analogy_count += 1
                evidence.setdefault('pseudo_analogy', []).append(pattern[:50])
        
        for pattern in self.pseudo_analogy_en:
            if re.search(pattern, text_lower, re.IGNORECASE):
                pseudo_analogy_count += 1
                evidence.setdefault('pseudo_analogy', []).append(pattern[:50])

        # Legitimate science shield: якщо текст є реальною науковою/технічною
        # публікацією (ML, AI, нейронауки) — pseudo_analogy повністю вимикається.
        #
        # Причина: в легітимних ML-статтях слова "neuron", "synapse", "analogous",
        # "structure", "therefore suggests" — це буквальна термінологія і
        # стандартні наукові конструкції. Вони не є псевдоаналогією.
        #
        # Виняток: якщо hits >= 5, щось явно не так навіть в науковому тексті
        # (напр. стаття про "планетарну нейронну мережу хмар").
        if is_legitimate_science:
            if pseudo_analogy_count < 5:
                pseudo_analogy_count = 0
            else:
                pseudo_analogy_count = max(0, pseudo_analogy_count - 3)

        if pseudo_analogy_count >= 2:
            absurdity_score += 0.55  # Coherent but logically invalid
        elif pseudo_analogy_count == 1:
            absurdity_score += 0.30
        
        # ================================================================
        # CHECK 9: FABRICATED TECHNO-FINANCE
        # ================================================================

        techno_finance_count = 0
        for pattern in self.fabricated_techno_finance:
            if re.search(pattern, text_lower, re.IGNORECASE):
                techno_finance_count += 1
                evidence.setdefault('fabricated_techno_finance', []).append(pattern[:60])

        for pattern in self.fabricated_techno_finance_en:
            if re.search(pattern, text_lower, re.IGNORECASE):
                techno_finance_count += 1
                evidence.setdefault('fabricated_techno_finance', []).append(pattern[:60])

        if techno_finance_count >= 2:
            absurdity_score += 0.65  # Реальні установи + неможлива технологія
        elif techno_finance_count == 1:
            absurdity_score += 0.40

        # ================================================================
        # CHECK 10: IMPOSSIBLE MEASUREMENT PRECISION
        # ================================================================

        impossible_meas_count = 0
        for pattern in self.impossible_measurement:
            if re.search(pattern, text_lower, re.IGNORECASE):
                impossible_meas_count += 1
                evidence.setdefault('impossible_measurement', []).append(pattern[:60])

        for pattern in self.impossible_measurement_en:
            if re.search(pattern, text_lower, re.IGNORECASE):
                impossible_meas_count += 1
                evidence.setdefault('impossible_measurement', []).append(pattern[:60])

        if impossible_meas_count >= 2:
            absurdity_score += 0.45
        elif impossible_meas_count == 1:
            absurdity_score += 0.25

        # ================================================================
        # CHECK 11: FABRICATED PSYCHO-STATE CONTROL
        # ================================================================

        psycho_control_count = 0
        for pattern in self.fabricated_psycho_control:
            if re.search(pattern, text_lower, re.IGNORECASE):
                psycho_control_count += 1
                evidence.setdefault('fabricated_psycho_control', []).append(pattern[:60])

        for pattern in self.fabricated_psycho_control_en:
            if re.search(pattern, text_lower, re.IGNORECASE):
                psycho_control_count += 1
                evidence.setdefault('fabricated_psycho_control', []).append(pattern[:60])

        if psycho_control_count >= 3:
            absurdity_score += 0.70  # Цензура подана як медицина — критично
        elif psycho_control_count == 2:
            absurdity_score += 0.50
        elif psycho_control_count == 1:
            absurdity_score += 0.30

        # ================================================================
        # CHECK 12: COLLECTIVIST MIND ERASURE
        # ================================================================

        mind_erasure_count = 0
        for pattern in self.collectivist_mind_erasure:
            if re.search(pattern, text_lower, re.IGNORECASE):
                mind_erasure_count += 1
                evidence.setdefault('collectivist_mind_erasure', []).append(pattern[:60])

        for pattern in self.collectivist_mind_erasure_en:
            if re.search(pattern, text_lower, re.IGNORECASE):
                mind_erasure_count += 1
                evidence.setdefault('collectivist_mind_erasure', []).append(pattern[:60])

        if mind_erasure_count >= 3:
            absurdity_score += 0.65
        elif mind_erasure_count == 2:
            absurdity_score += 0.45
        elif mind_erasure_count == 1:
            absurdity_score += 0.28

        # ================================================================
        # CHECK 13: FABRICATED STATISTICS
        # Правдоподібні відсотки без верифікованого джерела.
        # НЕ спрацьовує якщо текст є легітимною науковою публікацією.
        # ================================================================

        fabricated_stats_count = 0
        if not is_legitimate_science:
            for pattern in self.fabricated_statistics:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    fabricated_stats_count += 1
                    evidence.setdefault('fabricated_statistics', []).append(pattern[:60])

            if fabricated_stats_count >= 3:
                absurdity_score += 0.45
            elif fabricated_stats_count == 2:
                absurdity_score += 0.28
            elif fabricated_stats_count == 1:
                absurdity_score += 0.15

        # ================================================================
        # AGGREGATE
        # ================================================================
        
        absurdity_score = min(1.0, absurdity_score)
        
        return {
            'absurdity_score': round(absurdity_score, 3),
            'evidence': evidence,
            'has_non_sequitur': has_mundane and has_causal and has_absurd,
            'fabrication_count': fabrication_count,
            'danger_count': danger_count,
            'collapse_count': collapse_count,
            'techno_mystical_count': techno_count,
            'epistemology_collapse_count': epistemology_count,
            'pseudo_history_count': pseudo_history_count,
            'pseudo_analogy_count': pseudo_analogy_count,
            'techno_finance_count': techno_finance_count,
            'impossible_measurement_count': impossible_meas_count,
            'psycho_control_count': psycho_control_count,
            'mind_erasure_count': mind_erasure_count,
            'fabricated_stats_count': fabricated_stats_count,
            'is_legitimate_science': is_legitimate_science,
            'is_war_reporting': is_war_reporting,
        }
