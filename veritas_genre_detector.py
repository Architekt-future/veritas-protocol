"""
Veritas Genre Detector v2.0
Detects text genre to apply appropriate analysis calibration.

Genres:
  ANALYTICS        — multi-source, hedged claims, expert opinions
  REPORT           — factual, single event, who/what/where/when
  OPINION          — first person, subjective, persuasive
  SATIRE           — irony, hyperbole, humor signals
  SCIENCE          — research, studies, scientific methodology
  SPORT            — sports events and coverage
  CULTURE          — film, music, art, entertainment
  CONSPIRACY_NEWS  — "juicy coincidence" framing, unnamed sources, implied causality
  UNKNOWN          — insufficient signals

Changes v2.0:
  - Added CONSPIRACY_NEWS genre (implied causality, anonymous sources, mystery framing)
  - Added SPORT, CULTURE genres (moved from app.py crude regex)
  - Removed overly generic sport/culture words from other signal lists
  - Raised ANALYTICS threshold (was too easy to trigger)
  - Added confidence-weighted genre selection (prevents weak multi-match noise)
  - Calibration hints updated for new genres
"""

import re
from dataclasses import dataclass
from typing import Dict


@dataclass
class GenreResult:
    genre: str
    confidence: float  # 0.0-1.0
    signals: Dict[str, int]
    calibration: Dict[str, float]


class GenreDetector:

    # ── ANALYTICS ────────────────────────────────────────────────────
    # Hedged, multi-source analytical writing
    ANALYTICS_SIGNALS = [
        r'\bвважають\b', r'\bне виключають\b', r'\bза оцінками\b',
        r'\bаналітики\b', r'\bексперти зазначають\b', r'\bрозглядається\b',
        r'\bімовірно\b', r'\bповідомляється\b', r'\bочікується\b',
        r'\bза словами\b', r'\bза даними\b', r'\bна думку\b',
        r'\banalysts (say|believe|estimate)\b', r'\baccording to\b',
        r'\bexperts (say|warn|suggest|believe)\b', r'\bappear to\b',
        r'\bsuggests\b', r'\bsources (say|claim|indicate)\b',
    ]

    # ── REPORT ───────────────────────────────────────────────────────
    # Factual, event-driven, timestamped
    REPORT_SIGNALS = [
        r'\bзатримали\b', r'\bповідомив\b', r'\bзаявив\b', r'\bвідбулось\b',
        r'\bсталось\b', r'\bзагинули\b', r'\bпоранені\b', r'\bарештували\b',
        r'\bвибухи\b', r'\bнапад\b', r'\bоперація\b', r'\bнаступ\b',
        r'\bannounced\b', r'\bconfirmed\b', r'\barrested\b',
        r'\bо \d{1,2}:\d{2}\b',
        r'\b\d{1,2} (january|february|march|april|may|june|july|august|september|october|november|december) \d{4}\b',
        r'\bpublished:\b', r'\bupdated:\b',
        # EN investigative / breaking news
        r'\b(resigned|resignation)\b',
        r'\b(investigation|investigating|under investigation)\b',
        r'\b(declined to comment|did not (immediately )?respond|referred questions)\b',
        r'\b(first reported|exclusively reported|obtained by)\b',
        r'\b(according to (nbc|cnn|bbc|reuters|ap news|the times|a source))\b',
        r'\b(leak(ed|ing)|leaks?)\b',
        r'\b(fired|dismissed|ousted|stepped down)\b',
        r'\b(press secretary|spokesperson for|official said)\b',
        r'\b(hit back|pushed back|disputed|denied the claims?)\b',
        r'\b\d{1,2}:\d{2}\s*(AM|PM|EDT|EST|GMT|UTC)\b',
    ]

    # ── OPINION ──────────────────────────────────────────────────────
    # First-person, subjective, persuasive
    OPINION_SIGNALS = [
        r'\bя вважаю\b', r'\bна мою думку\b', r'\bмені здається\b',
        r'\bпереконаний\b', r'\bмоя позиція\b', r'\bавтор вважає\b',
        r'\bI believe\b', r'\bIn my opinion\b', r'\bI think\b',
        r'\bмусимо визнати\b', r'\bочевидно що\b', r'\bбезсумнівно\b',
        r'\bколумніст\b', r'\bколонка\b', r'\bop-?ed\b', r'\bcommentary\b',
    ]

    # ── SCIENCE ──────────────────────────────────────────────────────
    # Research methodology, peer-reviewed signals
    SCIENCE_SIGNALS = [
        r'\bдослідник\w*\b', r'\bдослідженн\w*\b', r'\bнауков\w*\b',
        r'\bпсихолог\w*\b', r'\bнейробіолог\w*\b', r'\bвстановлено\b',
        r'\bгіпотез\w*\b', r'\bкогнітивн\w*\b', r'\bклінічн\w*\b',
        r'\bвибірк\w*\b', r'\bексперимент\w*\b', r'\bopublikoван\w*\b',
        r'\bresearch(ers)?\b', r'\bstudy\b', r'\bfindings\b', r'\bscientists\b',
        r'\bpsycholog\w*\b', r'\bneurolog\w*\b', r'\bclinical\b',
        r'\bjournal\b', r'\bpeer.reviewed\b', r'\bpublished in\b',
    ]

    # ── SATIRE ───────────────────────────────────────────────────────
    SATIRE_SIGNALS = [
        r'\bнібито\b.{1,40}\bзнову\b', r'\bгеніальний план\b',
        r'\bтрадиційно\b.{1,40}\bзвинувачують\b',
        r'\bексперти.{1,30}одностайні\b', r'\bнесподівано з.ясувалось\b',
        r'\bofficial sources confirm\b.{1,40}\bsurprisingly\b',
        r'\bonion\b', r'\bсатира\b', r'\bпародія\b',
    ]

    # ── SPORT ────────────────────────────────────────────────────────
    # Sports-specific vocabulary (NOT generic English words like "score", "match")
    SPORT_SIGNALS = [
        r'\b(футбол|баскетбол|волейбол|теніс|хокей|бокс|гандбол|регбі|крикет)\b',
        r'\b(football|basketball|volleyball|tennis|hockey|boxing)\b',
        r'\b(олімпіад|чемпіонат|турнір|кубок|ліга|плей-оф)\b',
        r'\b(olympic|championship|tournament|playoff|league)\b',
        r'\b(гол|пенальті|арбітр|стадіон|збірна|тренер команди)\b',
        r'\b(goalkeeper|penalty|referee|stadium|squad leader|head coach)\b',
        r'\b(спортсмен|атлет|гравець команди|футболіст|баскетболіст)\b',
        r'\b(медальний залік|таблиця чемпіонату|груповий етап)\b',
        r'\b(transfer window|match day|league table|hat.trick)\b',
    ]

    # ── CULTURE ──────────────────────────────────────────────────────
    CULTURE_SIGNALS = [
        r'\b(фільм|кіно|серіал|театр|виставка|концерт|альбом)\b',
        r'\b(режисер|актор|актриса|сценарист|продюсер)\b',
        r'\b(film|movie|series|theatre|concert|album|premiere)\b',
        # "director" без кінематографічного контексту — не культурний сигнал.
        # Потребує супутнього слова щоб відрізнити від "Director of FBI"
        r'\b(director|actor|actress|screenwriter|producer)\b(?=.{0,60}(film|movie|series|theatre|music|album|award))',
        r'\b(нагород|номінант|прем.єра|реліз|кінофестиваль)\b',
        r'\b(award|nomination|release|box office|film festival)\b',
    ]

    # ── CONSPIRACY_NEWS ──────────────────────────────────────────────
    # "Juicy coincidence" journalism: real facts + implied causality + mystery framing
    # Classic patterns: Daily Mail, NY Post, tabloids, UFO/deep state content
    CONSPIRACY_NEWS_SIGNALS = [
        # Mystery/coincidence framing — the core tell
        r'\b(mysterious(ly)?|mysteriously)\b',
        r'\b(oddly timed|suspicious timing|coincidence|no coincidence)\b',
        r'\b(hours (after|before|later).{1,60}(wiped|deleted|removed|vanished|disappeared))\b',
        r'\b(days (after|before).{1,60}(died|killed|arrested|fired|resigned))\b',
        r'\b(the timing.{1,40}(suspicious|odd|strange|raises questions))\b',
        r'\b(raises questions about|prompting questions)\b',

        # Unnamed/anonymous sourcing as primary evidence
        r'\b(sources (say|claim|tell us|reveal)|insiders (say|claim|reveal))\b',
        r'\b(according to sources|sources close to)\b',
        r'\b(джерела (стверджують|кажуть|повідомляють))\b',
        r'\b(behind the scenes|off the record|in private)\b',

        # Can't rule out / can't confirm framing (epistemic escape hatch)
        r"\b(can.t rule (it )?out|cannot rule out)\b",
        r'\b(we cannot confirm|unconfirmed (reports|claims))\b',
        r'\b(could not be independently verified)\b',
        r'\b(не (можна|можу) виключити|не вдалось підтвердити)\b',

        # Deep state / cover-up vocabulary
        r'\b(cover.?up|coverup|deep state|shadow government)\b',
        r'\b(suppressed|silenced|wiped clean|scrubbed)\b',
        r'\b(they don.t want you to know|what (they|the government) (doesn.t|don.t) want)\b',
        r'\b(UFO|UAP|extraterrestrial|alien (technology|life|contact))\b',
        r'\b(declassif|FOIA request|Freedom of Information)\b',

        # Sensational verb choices
        r'\b(vanished|wiped (clean|out)|mysteriously (deleted|disappeared|died))\b',
        r'\b(bombshell|explosive (revelation|claim)|shocking (twist|revelation))\b',
        r'\b(truth (finally|about)|reveal(ed)? the truth)\b',
    ]

    # ── INTERVIEW ────────────────────────────────────────────────────
    # Питання-відповідь структура: тире або Q/A мітки
    INTERVIEW_SIGNALS = [
        r'^\s*—\s+.{10,}',                          # тире на початку рядка (UK стиль)
        r'\b(запитує|відповідає|розповідає|пояснює)\b',
        r'\b(в розмові|в інтерв.ю|в бесіді)\b',
        r'\b(Q:|A:|Question:|Answer:)\b',
        r'\b(says?\s+in\s+an?\s+interview|spoke\s+(to|with)\s+\w+\s+(about|on))\b',
        r'\b(tells?\s+(me|us)|told\s+(me|us)\b)',
        r'\bvarosh\s+talks?\b',
        r'\b(у\s+розмові|розмовляє\s+з|бесідує\s+з)\b',
    ]

    # ── GEOPOLITICS ──────────────────────────────────────────────────
    # Міжнародні відносини, безпека, дипломатія
    GEOPOLITICS_SIGNALS = [
        r'\b(nato|нато)\b',
        r'\b(sanctions?|санкці)\b',
        r'\b(diplomatic|дипломатичн)\b',
        r'\b(sovereignty|суверенітет)\b',
        r'\b(ceasefire|перемир.я)\b',
        r'\b(kremlin|кремл)\b',
        r'\b(geopolit|геополіт)\b',
        r'\b(international\s+(law|order|community)|міжнародн\w+\s+(право|порядок|спільнот))\b',
        r'\b(war\s+crimes?|воєнн\w+\s+злочин)\b',
        r'\b(allies?|alliance|альянс|союзник)\b',
        r'\b(annexation|анексі)\b',
        r'\b(occupation|окупац)\b',
    ]

    # ── ECONOMY ──────────────────────────────────────────────────────
    # Макроекономіка — без фінансових інструментів (відрізняємо від фінансів)
    ECONOMY_SIGNALS = [
        r'\b(gdp|ввп|gross\s+domestic\s+product)\b',
        r'\b(inflation|інфляці)\b',
        r'\b(central\s+bank|центральн\w+\s+банк)\b',
        r'\b(interest\s+rate|облікова\s+ставка)\b',
        r'\b(imf|мвф|international\s+monetary\s+fund)\b',
        r'\b(export|import|експорт|імпорт)\b',
        r'\b(budget\s+deficit|бюджетн\w+\s+дефіцит)\b',
        r'\b(foreign\s+(direct\s+)?investment|прям\w+\s+іноземн\w+\s+інвестиці)\b',
        r'\b(unemployment|безробітт)\b',
        r'\b(fiscal|фіскальн)\b',
        r'\b(recession|рецесі)\b',
        r'\b(monetary\s+policy|монетарн\w+\s+політик)\b',
    ]

    # ── INVESTIGATION ────────────────────────────────────────────────
    # Журналістське розслідування з жертвами, даними, судовими справами
    INVESTIGATION_SIGNALS = [
        r'\b(lawsuit|sued|suing|wrongful.death)\b',
        r'\b(hospitali[sz]ed?|suicide|suicidal)\b',
        r'\b(wrecked|derailed|destroyed).{1,40}(life|marriage|career|family)\b',
        r'\b(victim|survivor|affected)\b',
        r'\b(\d+\s*(suicides?|deaths?|hospitali[sz]))\b',
        r'\b(psychiatrist|psychologist|researcher).{1,60}(warn|concern|alarm)\b',
        r'\b(support\s+group|advocacy\s+group)\b',
        r'\b(estate\s+of|filed\s+in\s+(california|court))\b',
        r'\b(delusion|psychosis|mental\s+breakdown)\b',
        r'\b(lives?\s+(ruined|wrecked|destroyed|derailed))\b',
    ]

    # ── MEDIA_MONITORING ─────────────────────────────────────────────
    # Моніторинг ЗМІ, телемарафонів, медіааналіз
    MEDIA_MONITORING_SIGNALS = [
        r'\b(моніторинг|моніторингу)\b',
        r'\b(телемарафон|телемарафону|ефір|ефіру)\b',
        r'\b(стандарт\w*\s+журналіст|журналістськ\w+\s+стандарт)\b',
        r'\b(порушення\s+стандарт|стандарт\w+\s+достовірн)\b',
        r'\b(гостьова\s+студія|гостьових\s+студ)\b',
        r'\b(воєнкор|медіатренер|медіааналіз|медіаексперт)\b',
        r'\b(детектор\s+медіа|media\s+monitor|media\s+watch)\b',
        r'\b(редакц\w+\s+канал|канал\w+\s+редакц)\b',
        r'\b(висвітлення\s+(тем|подій|ситуац)|покриття\s+теми)\b',
        r'\b(піар|pr)\w*\s+(в\s+ефір|матеріал|сюжет)\b',
    ]

    CALIBRATION = {
        'ANALYTICS': {
            'absurdity_weight': 0.0,
            'anon_authority':   False,
            'unanchored_claim': False,
            'entropy_damper':   False,
            'entropy_cap':      0.85,
        },
        'MEDIA_MONITORING': {
            'absurdity_weight': 0.0,   # Моніторинг описує атаки — не псевдонаука
            'anon_authority':   True,
            'unanchored_claim': False,
            'entropy_damper':   True,
            'entropy_cap':      0.80,
        },
        'REPORT': {
            'absurdity_weight': 1.8,
            'anon_authority':   True,
            'unanchored_claim': True,
            'entropy_damper':   True,
            'entropy_cap':      1.0,
        },
        'OPINION': {
            'absurdity_weight': 1.0,
            'anon_authority':   False,
            'unanchored_claim': False,
            'entropy_damper':   True,
            'entropy_cap':      1.0,
        },
        'SCIENCE': {
            'absurdity_weight': 0.0,
            'anon_authority':   False,
            'unanchored_claim': False,
            'entropy_damper':   False,
            'entropy_cap':      0.85,
        },
        'SATIRE': {
            'absurdity_weight': 0.0,
            'anon_authority':   False,
            'unanchored_claim': False,
            'entropy_damper':   False,
            'entropy_cap':      0.90,
        },
        'SPORT': {
            'absurdity_weight': 0.0,
            'anon_authority':   False,
            'unanchored_claim': False,
            'entropy_damper':   True,
            'entropy_cap':      0.70,
            # Sports results are facts — high entropy = something wrong
        },
        'CULTURE': {
            'absurdity_weight': 0.0,
            'anon_authority':   False,
            'unanchored_claim': False,
            'entropy_damper':   True,
            'entropy_cap':      0.80,
        },
        'CONSPIRACY_NEWS': {
            'absurdity_weight': 1.5,
            'anon_authority':   True,   # anonymous sources ARE the problem here
            'unanchored_claim': True,   # implied causality = unanchored
            'entropy_damper':   False,  # don't suppress — let entropy speak
            'entropy_cap':      1.0,
            # Key: implied_causality penalty active for this genre
            'implied_causality_boost': 0.25,
        },
        'UNKNOWN': {
            'absurdity_weight': 1.8,
            'anon_authority':   True,
            'unanchored_claim': True,
            'entropy_damper':   True,
            'entropy_cap':      1.0,
        },
        'INTERVIEW': {
            'absurdity_weight': 0.5,
            'anon_authority':   False,  # інтерв'ю = іменований спікер
            'unanchored_claim': False,
            'entropy_damper':   True,
            'entropy_cap':      0.90,
        },
        'GEOPOLITICS': {
            'absurdity_weight': 0.8,
            'anon_authority':   True,   # анонімні дипломатичні джерела — норма
            'unanchored_claim': True,
            'entropy_damper':   True,
            'entropy_cap':      1.0,
        },
        'ECONOMY': {
            'absurdity_weight': 0.5,
            'anon_authority':   False,
            'unanchored_claim': False,
            'entropy_damper':   True,
            'entropy_cap':      0.85,
        },
        'INVESTIGATION': {
            'absurdity_weight': 1.0,
            'anon_authority':   True,   # анонімні жертви — норма в розслідуваннях
            'unanchored_claim': True,
            'entropy_damper':   False,
            'entropy_cap':      1.0,
        },
    }

    # ── Verdict labels (for clean texts of this genre) ───────────────

    CLEAN_VERDICT = {
        'ANALYTICS': ('VERIFIED', 'АНАЛІТИЧНА СТРУКТУРОВАНІСТЬ',
                      'Текст демонструє ознаки аналітичного жанру: множинні джерела, '
                      'хеджовані твердження, структурована аргументація'),
        'OPINION':   ('VERIFIED', 'АВТОРСЬКА ПОЗИЦІЯ',
                      'Текст є вираженням суб\'єктивної думки; оцінюйте аргументи, '
                      'а не факти'),
        'SCIENCE':   ('VERIFIED', 'НАУКОВИЙ ТЕКСТ',
                      'Текст містить ознаки наукового або науково-популярного матеріалу. '
                      'Перевіряйте конкретні твердження у наукових джерелах.'),
        'SATIRE':    ('VERIFIED', 'САТИРИЧНИЙ КОНТЕНТ',
                      'Виявлено ознаки сатири або іронії; буквальна інтерпретація '
                      'може бути хибною'),
        'SPORT':     ('VERIFIED', 'СПОРТИВНИЙ РЕПОРТАЖ',
                      'Текст є спортивним репортажем або результатами змагань.'),
        'CULTURE':   ('VERIFIED', 'КУЛЬТУРНИЙ КОНТЕНТ',
                      'Текст є культурним оглядом або рецензією.'),
        'INTERVIEW': ('VERIFIED', 'ІНТЕРВ\'Ю',
                      'Текст є інтерв\'ю або бесідою. Оцінюйте позицію спікера '
                      'як суб\'єктивну думку, а не об\'єктивний факт.'),
        'GEOPOLITICS': ('VERIFIED', 'ГЕОПОЛІТИЧНИЙ АНАЛІЗ',
                      'Текст стосується міжнародних відносин або безпеки. '
                      'Перевіряйте факти в офіційних джерелах.'),
        'ECONOMY':   ('VERIFIED', 'ЕКОНОМІЧНИЙ ОГЛЯД',
                      'Текст містить макроекономічні дані або аналіз. '
                      'Перевіряйте цифри у первинних джерелах (МВФ, ЦБ, Мінфін).'),
        'INVESTIGATION': ('VERIFIED', 'ЖУРНАЛІСТСЬКЕ РОЗСЛІДУВАННЯ',
                      'Текст є розслідуванням із задокументованими випадками. '
                      'Перевіряйте конкретні факти у судових реєстрах та офіційних джерелах.'),
        'MEDIA_MONITORING': ('VERIFIED', 'МЕДІАМОНІТОРИНГ',
                      'Текст є аналізом медіапростору або моніторингом ЗМІ. '
                      'Оцінює якість журналістики — не є маніпулятивним за природою.'),
        'CONSPIRACY_NEWS': ('SUSPICIOUS', 'НОВИНИ З ІМПЛІКОВАНОЮ ПРИЧИННІСТЮ',
                      'Текст містить реальні факти, але подані через "дивний збіг" або '
                      'анонімні джерела без прямих доказів зв\'язку між подіями. '
                      'Перевіряйте кожне твердження окремо.'),
    }

    # ────────────────────────────────────────────────────────────────

    def analyze(self, text: str) -> GenreResult:
        t = text.lower()

        analytics       = sum(1 for p in self.ANALYTICS_SIGNALS       if re.search(p, t, re.I))
        science         = sum(1 for p in self.SCIENCE_SIGNALS          if re.search(p, t, re.I))
        report          = sum(1 for p in self.REPORT_SIGNALS           if re.search(p, t, re.I))
        opinion         = sum(1 for p in self.OPINION_SIGNALS          if re.search(p, t, re.I))
        satire          = sum(1 for p in self.SATIRE_SIGNALS           if re.search(p, t, re.I))
        sport           = sum(1 for p in self.SPORT_SIGNALS            if re.search(p, t, re.I))
        culture         = sum(1 for p in self.CULTURE_SIGNALS          if re.search(p, t, re.I))
        conspiracy_news = sum(1 for p in self.CONSPIRACY_NEWS_SIGNALS  if re.search(p, t, re.I))
        interview       = sum(1 for p in self.INTERVIEW_SIGNALS        if re.search(p, t, re.I | re.MULTILINE))
        geopolitics     = sum(1 for p in self.GEOPOLITICS_SIGNALS      if re.search(p, t, re.I))
        economy         = sum(1 for p in self.ECONOMY_SIGNALS          if re.search(p, t, re.I))
        investigation   = sum(1 for p in self.INVESTIGATION_SIGNALS    if re.search(p, t, re.I))
        media_monitoring = sum(1 for p in self.MEDIA_MONITORING_SIGNALS if re.search(p, t, re.I))

        signals = {
            'analytics':       analytics,
            'science':         science,
            'report':          report,
            'opinion':         opinion,
            'satire':          satire,
            'sport':           sport,
            'culture':         culture,
            'conspiracy_news': conspiracy_news,
            'interview':       interview,
            'geopolitics':     geopolitics,
            'economy':         economy,
            'investigation':      investigation,
            'media_monitoring':   media_monitoring,
        }

        # ── Genre selection logic ────────────────────────────────────
        # Priority order matters: more specific genres win over generic ones.
        # CONSPIRACY_NEWS can overlay REPORT or ANALYTICS — it wins if strong enough.

        genre = 'UNKNOWN'
        conf  = 0.0

        if media_monitoring >= 4:
            # Медіамоніторинг — дуже специфічний жанр, виграє над усіма
            genre, conf = 'MEDIA_MONITORING', min(media_monitoring / 8, 1.0)

        elif satire >= 2:
            genre, conf = 'SATIRE',          min(satire / 4, 1.0)

        elif conspiracy_news >= 4:
            genre, conf = 'CONSPIRACY_NEWS', min(conspiracy_news / 10, 1.0)

        elif opinion >= 2 and opinion > analytics:
            genre, conf = 'OPINION',         min(opinion / 4, 1.0)

        elif science >= 3:
            genre, conf = 'SCIENCE',         min(science / 8, 1.0)

        elif sport >= 3:
            genre, conf = 'SPORT',           min(sport / 6, 1.0)

        elif culture >= 3:
            genre, conf = 'CULTURE',         min(culture / 6, 1.0)

        elif investigation >= 4:
            # Розслідування з задокументованими жертвами — специфічний жанр
            genre, conf = 'INVESTIGATION',   min(investigation / 8, 1.0)

        elif interview >= 3:
            # Інтерв'ю: тире + контекст розмови
            genre, conf = 'INTERVIEW',       min(interview / 6, 1.0)

        elif geopolitics >= 4:
            genre, conf = 'GEOPOLITICS',     min(geopolitics / 10, 1.0)

        elif economy >= 4:
            genre, conf = 'ECONOMY',         min(economy / 10, 1.0)

        elif analytics >= 3:
            if conspiracy_news >= 2:
                genre, conf = 'CONSPIRACY_NEWS', min((analytics + conspiracy_news) / 14, 1.0)
            else:
                genre, conf = 'ANALYTICS',   min(analytics / 8, 1.0)

        elif report >= 2:
            if conspiracy_news >= 2:
                genre, conf = 'CONSPIRACY_NEWS', min((report + conspiracy_news) / 12, 1.0)
            else:
                genre, conf = 'REPORT',      min(report / 8, 1.0)

        elif geopolitics >= 2:
            genre, conf = 'GEOPOLITICS',     min(geopolitics / 10, 0.5)

        elif economy >= 2:
            genre, conf = 'ECONOMY',         min(economy / 10, 0.5)

        elif interview >= 2:
            genre, conf = 'INTERVIEW',       min(interview / 6, 0.5)

        elif conspiracy_news >= 2:
            genre, conf = 'CONSPIRACY_NEWS', min(conspiracy_news / 10, 0.5)

        return GenreResult(
            genre=genre,
            confidence=round(conf, 2),
            signals=signals,
            calibration=self.CALIBRATION[genre],
        )


# ── Quick smoke-test ─────────────────────────────────────────────────

if __name__ == '__main__':
    d = GenreDetector()

    tests = [
        ('Daily Mail НЛО',
         'Mystery as UFO vault with 3.8 million files is wiped clean hours after Trump demands '
         'alien docs released. Greenewald said he could not rule out foul play because of the '
         'suspicious information. They said it was a deletion, not corruption. The timing raises '
         'questions. Could it have been foul play? I can\'t rule it out. Bombshell UFO speech ready. '
         'According to sources close to the investigation the server was deliberately wiped.'),

        ('TSN Аналітика',
         'Аналітики вважають що Пекін дедалі більше виступає у ролі старшого партнера. '
         'Експерти не виключають що Китай не очікував такого масштабу. За оцінками ЄС '
         'Китай забезпечує до 80 відсотків компонентів. За словами джерел у Брюсселі.'),

        ('rbc Репортаж',
         'Правоохоронці затримали ймовірну виконавицю двох вибухів. Жінку було затримано '
         'в районному центрі. Published: 12 February 2025. Confirmed by police spokesperson.'),

        ('Думка колумніста',
         'Я вважаю що Україна мусить визнати реальність. На мою думку переговори неминучі. '
         'Переконаний що час діяти. Колонка редактора.'),

        ('Спорт',
         'Збірна України вийшла до фіналу чемпіонату. Тренер команди підтвердив склад. '
         'Матч відбудеться на стадіоні в Варшаві. Груповий етап завершено. '
         'Баскетбол і волейбол також в програмі олімпіади.'),

        ('Наука',
         'Дослідники виявили новий механізм. Клінічне дослідження охопило 500 осіб. '
         'Гіпотеза підтверджена експериментом. Published in peer-reviewed journal. '
         'Scientists from the laboratory conducted research on cognitive functions.'),
    ]

    print(f'{"Тест":<22} {"Жанр":<20} {"Conf":>5}  {"Сигнали"}')
    print('─' * 80)
    for name, text in tests:
        r = d.analyze(text)
        sig_str = '  '.join(f'{k}={v}' for k, v in r.signals.items() if v > 0)
        print(f'{name:<22} {r.genre:<20} {r.confidence:>5.2f}  {sig_str}')
