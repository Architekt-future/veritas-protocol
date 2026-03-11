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
        
        # Logical operators that claim causation
        self.causal_operators = [
            r'враховуючи',
            r'оскільки',
            r'тому',
            r'це означає',
            r'звідси випливає',
            r'отже',
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
            
            # Violent/destructive actions
            r'(знищити|зруйнува|підірва).{1,60}(вежі|станц|мереж|систем)',
            r'(напад|атак|саботаж).{1,60}(інфраструктур|об.єкт)',
            
            # Genocide/mass harm (NEW!)
            r'(ліквідац|знищення|вбивство).{1,100}(\d+%|відсотк|більшост).{1,60}(населення|людей|люд)',
            r'(раціональн|логічн|ефективн).{1,100}(ліквідац|знищення|вбивство|геноцид)',
            r'(скорочення|зменшення).{1,100}населення.{1,100}(збереження|порятун)',
            r'population.{1,100}(reduction|elimination|culling)',
            
            # Surrender of agency to AI/external control
            r'делегува.{1,60}(всі|повн).{1,60}(рішення|контроль|влад).{1,60}(ai|штучн.{1,20}інтелект)',
            r'(ai|нейромереж).{1,60}(випадков.{1,20}числ|хаос).{1,60}(ядерн|зброї|арсенал)',
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
        ]

        # ================================================================
        # TYPE 10: IMPOSSIBLE MEASUREMENT PRECISION
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
        # TYPE 8: PSEUDO-SCIENTIFIC ANALOGY
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

    def analyze(self, text: str) -> Dict:
        """
        Returns absurdity score (0.0-1.0)
        Higher = more absurd
        """
        if len(text) < 30:
            return {'absurdity_score': 0.0, 'reason': 'text_too_short'}
        
        text_lower = text.lower()
        
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
        
        if fabrication_count >= 2:
            absurdity_score += 0.5  # Multiple impossible sources
        elif fabrication_count == 1:
            absurdity_score += 0.3
        
        # ================================================================
        # CHECK 3: DANGEROUS IMPLICATIONS
        # ================================================================
        
        danger_count = 0
        for pattern in self.dangerous_patterns:
            if re.search(pattern, text_lower):
                danger_count += 1
                evidence['dangerous_implications'].append(pattern[:50])
        
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

        if impossible_meas_count >= 2:
            absurdity_score += 0.45
        elif impossible_meas_count == 1:
            absurdity_score += 0.25

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
        }
