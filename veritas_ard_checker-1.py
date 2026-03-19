"""
Veritas ARD Checker v1.0
========================
Перевірка тексту через призму Архітектури Раціональної Дії (АРД v2.0).
Гібридний підхід: regex детектор → Haiku аналіз (тільки якщо є що аналізувати).

Дев'ять принципів АРД:
  0. Передмова: визнання можливості помилки
  I. Базовий інваріант: не руйнуй механізми виправлення
  II. Чотири контрольні питання (особиста вигода → система → тест обернення → прецедент)
  III. Відповідальність за наслідки 2-3 порядку
  IV. Межа впливу: не позбавляй здатності сказати "ні"
  V. Принцип зупинки: чи можеш пояснити без замовчування
  VI. Антимесія: не нав'язуй благо без запиту
  VII. Фінальний якір: готовність жити в наслідках
  VIII. Протокол конфлікту інтересів
  IX. Метаправило: не зловживай системою для виправдання

Вердикти:
  ARD_COMPLIANT      — текст не порушує принципів АРД
  ARD_MINOR_TENSION  — незначні напруження, варто звернути увагу
  ARD_VIOLATION      — виявлено порушення одного або більше принципів
  ARD_SYSTEMIC       — системне порушення кількох принципів
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class ARDViolation:
    principle: str          # напр. "I", "IV", "IX"
    principle_name: str     # назва принципу
    pattern_name: str       # назва патерну
    snippet: str            # знайдений фрагмент
    severity: float         # 0.0-1.0


@dataclass
class ARDScanResult:
    score: float = 0.0
    verdict: str = 'ARD_COMPLIANT'
    violations: List[ARDViolation] = field(default_factory=list)
    principles_violated: List[str] = field(default_factory=list)
    is_flagged: bool = False
    needs_haiku: bool = False


class ARDChecker:
    """
    Детекторний шар (перший прохід).
    Ловить явні порушення принципів АРД за regexp патернами.
    """

    # ================================================================
    # ПРИНЦИП I: БАЗОВИЙ ІНВАРІАНТ
    # Не руйнуй механізми виправлення: суди, науку, журналістику, освіту
    # Патерни: VACUUM_DECLARATION, руйнація інститутів, заклики до ігнорування норм
    # ================================================================
    PRINCIPLE_I_UK = [
        r'(суди|правосуддя|закон).{1,60}(більше не (існує|працює|має сенсу)|мертве|безсиле)',
        r'(медіа|преса|журналісти).{1,60}(не можна довіряти|брешуть|продажні|ворог)',
        r'(наука|вчені|експерти).{1,60}(не варто довіряти|куплені|маніпулюють|брехня)',
        r'(освіта|університети|школи).{1,60}(промивання мізків|індоктринація|маніпуляція)',
        r'(правила|норми|закони).{1,60}(для (слабких|лохів|слабаків)|не для нас|можна ігнорувати)',
        r'(правовий|інституційний|системний).{1,60}(вакуум|колапс|крах)',
        r'(конституція|статут|хартія).{1,60}(застаріла|не працює|треба скасувати)',
    ]
    PRINCIPLE_I_EN = [
        r'(courts?|justice|law).{1,60}(no longer (exists?|works?|matters?)|is dead|is powerless)',
        r'(media|press|journalists?).{1,60}(can\'t be trusted|are lying|are corrupt|enemy of)',
        r'(science|scientists?|experts?).{1,60}(can\'t be trusted|are bought|manipulate|is a lie)',
        r'(education|universities|schools).{1,60}(brainwashing|indoctrination|manipulation)',
        r'(rules?|norms?|laws?).{1,60}(for (the weak|losers|suckers)|don\'t apply to us|can be ignored)',
        r'(legal|institutional|systemic).{1,60}(vacuum|collapse|breakdown)',
        r'(constitution|charter|statute).{1,60}(is outdated|doesn\'t work|should be abolished)',
    ]

    # ================================================================
    # ПРИНЦИП II: ТЕСТ ОБЕРНЕННЯ (контрольне питання 3)
    # Чи залишився б ти при рішенні якби народився в тілі того на кого воно впливає?
    # Патерни: дегуманізація, поділ на "ми/вони", позбавлення суб'єктності
    # ================================================================
    PRINCIPLE_II_UK = [
        r'(вони|ці люди|такі як вони).{1,60}(не розуміють|не здатні|не заслуговують)',
        r'(їхні (страждання|втрати|проблеми)).{1,60}(самі (винні|заслужили|спровокували))',
        r'(колатеральні|супутні).{1,60}(втрати|жертви|збитки).{1,60}(неминучі|прийнятні|виправдані)',
        r'(їх(ній|нє)|у них).{1,60}(менше цінності|менше прав|не такі як ми)',
        r'(ці|такі).{1,60}(люди|групи|народи).{1,60}(самі (обрали|вибрали|заслужили))',
    ]
    PRINCIPLE_II_EN = [
        r'(they|these people|people like them).{1,60}(don\'t understand|are incapable|don\'t deserve)',
        r'(their (suffering|losses?|problems?)).{1,60}(their own (fault|doing|making))',
        r'(collateral|acceptable).{1,60}(damage|casualties|losses).{1,60}(inevitable|acceptable|justified)',
        r'(they|their kind).{1,60}(less valuable|fewer rights|not like us)',
        r'(these|such).{1,60}(people|groups|nations).{1,60}(chose|deserved|brought it on)',
    ]

    # ================================================================
    # ПРИНЦИП III: ВІДПОВІДАЛЬНІСТЬ ЗА НАСЛІДКИ
    # "Я не знав" — не аргумент. "Так роблять всі" — не виправдання.
    # "Мені наказали" — не знімає відповідальність.
    # ================================================================
    PRINCIPLE_III_UK = [
        r'(я не знав|ми не знали|не можна було знати).{1,60}(тому|отже|значить).{1,40}(не винні|не відповідальні)',
        r'(так роблять (всі|усі|кожен)|це загальноприйнята практика)',
        r'(просто виконував|лише виконував|просто виконували).{1,60}(накази|наказ)',
        r'(нам (наказали|сказали|доручили)).{1,60}(ми (просто|лише) виконували)',
        r'(наказ|розпорядження|директива).{1,60}(знімає|позбавляє|звільняє від).{1,60}(відповідальн|провину)',
        r'(не (моя|наша) (відповідальність|провина|проблема))',
        r'(це не (моя|наша) (відповідальність|вина))',
    ]
    PRINCIPLE_III_EN = [
        r'(I didn\'t know|we didn\'t know|there was no way to know).{1,60}(therefore|so|thus).{1,40}(not (guilty|responsible))',
        r'(everyone does it|that\'s standard practice|it\'s common)',
        r'(just following (orders?|instructions?|directives?))',
        r'(I was (ordered|told|instructed)).{1,60}(I was (just|only) (following|doing))',
        r'(orders?|directive|instruction).{1,60}(removes?|absolves?|eliminates?).{1,60}(responsibility|guilt|blame)',
        r'(not (my|our) (responsibility|fault|problem))',
    ]

    # ================================================================
    # ПРИНЦИП IV: МЕЖА ВПЛИВУ
    # Не позбавляй здатності сказати "ні" без непропорційної шкоди.
    # Патерни: примус, погрози, маніпуляція вибором
    # ================================================================
    PRINCIPLE_IV_UK = [
        r'(або (ти|ви|вони)).{1,60}(або (наслідки|покарання|проблеми))',
        r'(відмова|незгода).{1,60}(призведе до|загрожує|матиме наслідки).{1,40}(для (вас|тебе|них))',
        r'(якщо (не|відмовишся|не погодишся)).{1,60}(будеш|стане|загрожує)',
        r'(у (вас|тебе|них) (немає|нема) вибору)',
        r'(погрожує|шантажує|ультиматум).{1,60}(якщо не)',
        r'(або підкоришся|або погодишся).{1,60}(або (втратиш|позбудешся|покараємо))',
    ]
    PRINCIPLE_IV_EN = [
        r'(either (you|they)).{1,60}(or (consequences|punishment|trouble))',
        r'(refusal|disagreement).{1,60}(will (lead to|result in|cause)).{1,40}(for (you|them))',
        r'(if (you|they) (don\'t|refuse|won\'t)).{1,60}(will|faces?|threatens?)',
        r'(you have no choice|there is no choice|no alternative)',
        r'(threatens?|blackmails?|ultimatum).{1,60}(if (you|they) (don\'t|refuse))',
        r'(either (comply|agree|submit)).{1,60}(or (lose|forfeit|we will))',
    ]

    # ================================================================
    # ПРИНЦИП V: ПРИНЦИП ЗУПИНКИ
    # Чи можеш пояснити без замовчування ключових фактів?
    # Патерни: приховування, замовчування, неповнота що вводить в оману
    # ================================================================
    PRINCIPLE_V_UK = [
        r'(не (варто|треба|потрібно)).{1,60}(знати|розуміти|вникати).{1,40}(деталі|подробиці)',
        r'(довіртесь|покладіться).{1,60}(нам|експертам|системі).{1,60}(без зайвих (запитань|деталей))',
        r'(деталі|подробиці).{1,60}(не (важливі|суттєві|потрібні)).{1,60}(головне)',
        r'(ця інформація|ці дані).{1,60}(не для (всіх|широкого загалу|публіки))',
        r'(є причини|є підстави).{1,60}(не розголошувати|тримати в таємниці|не говорити)',
    ]
    PRINCIPLE_V_EN = [
        r'(no need|don\'t need).{1,60}(to know|to understand|to dig into).{1,40}(details|specifics)',
        r'(trust|rely on).{1,60}(us|experts|the system).{1,60}(without (unnecessary )?questions)',
        r'(details|specifics).{1,60}(don\'t (matter|concern|affect)).{1,60}(what matters)',
        r'(this information|this data).{1,60}(not for (everyone|the public|general audience))',
        r'(there are reasons|there are grounds).{1,60}(not to disclose|to keep secret|not to say)',
    ]

    # ================================================================
    # ПРИНЦИП VI: АНТИМЕСІЯ
    # Не нав'язуй "благо" тим хто не просив. Ієрархія втручання.
    # Патерни: нав'язане порятунок, "ми знаємо краще", хрестові походи
    # ================================================================
    PRINCIPLE_VI_UK = [
        r'(ми (знаємо|розуміємо) краще).{1,60}(що (добре|краще|потрібно)).{1,40}(для (вас|них|людей))',
        r'(вони (не розуміють|не усвідомлюють)).{1,60}(що (їм|для них) (добре|краще|потрібно))',
        r'(рятуємо|захищаємо|допомагаємо).{1,60}(навіть (якщо|проти|незважаючи)).{1,40}(їхньої волі|їх бажання)',
        r'(їхнє (благо|добро|інтерес)).{1,60}(важливіш(е|ий).{1,20}ніж їхня (воля|думка|бажання))',
        r'(місія|призначення|обов.язок).{1,60}(навіть (якщо|проти|незважаючи)).{1,40}(не хочуть|відмовляються)',
    ]
    PRINCIPLE_VI_EN = [
        r'(we (know|understand) better).{1,60}(what is (good|best|needed)).{1,40}(for (you|them|people))',
        r'(they (don\'t understand|don\'t realize)).{1,60}(what is (good|best|needed)).{1,40}(for them)',
        r'(saving|protecting|helping).{1,60}(even (if|against|despite)).{1,40}(their will|their wishes)',
        r'(their (good|benefit|interest)).{1,60}(more important than their (will|opinion|wishes))',
        r'(mission|purpose|duty).{1,60}(even (if|against|despite)).{1,40}(they (don\'t want|refuse))',
    ]

    # ================================================================
    # ПРИНЦИП IX: МЕТАПРАВИЛО
    # Використання системи для виправдання того що інтуїтивно неправильне.
    # Ознаки самообману: лазівки, ускладнення, полегшення від "виправдання".
    # ================================================================
    PRINCIPLE_IX_UK = [
        r'(формально|технічно|юридично).{1,60}(не (порушує|забороняє|є злочином)).{1,60}(але)',
        r'(де.юре|на папері|офіційно).{1,60}(все (чисто|правильно|законно)).{1,60}(але|проте)',
        r'(знайшли (спосіб|лазівку|обхід)).{1,60}(щоб (уникнути|обійти|не порушувати))',
        r'(не порушуємо (букву|правило|закон)).{1,60}(але (дух|намір|суть))',
        r'(все (законно|легально|офіційно)).{1,60}(хоча (і|та|але)).{1,40}(сумнівно|спірно|нечесно)',
    ]
    PRINCIPLE_IX_EN = [
        r'(formally|technically|legally).{1,60}(not (violating|prohibited|a crime))',
        r'(found (a )?loophole|found a workaround|found a way around)',
        r'(everything is (technically|formally|legally) (correct|legal|fine))',
        r'(the letter of the (law|rule)).{1,60}(not the spirit)',
        r'(de jure|on paper|officially).{1,60}(everything is (clean|correct|legal))',
        r'(not (my|our) (fault|doing).{1,40}just following)',
    ]

    def scan(self, text: str) -> ARDScanResult:
        result = ARDScanResult()
        if not text or len(text) < 50:
            return result

        t = text.lower()
        total_score = 0.0

        checks = [
            ('I',   'Базовий інваріант — руйнація механізмів виправлення',
             self.PRINCIPLE_I_UK + self.PRINCIPLE_I_EN, 0.65),
            ('II',  'Тест обернення — дегуманізація або позбавлення суб\'єктності',
             self.PRINCIPLE_II_UK + self.PRINCIPLE_II_EN, 0.55),
            ('III', 'Відповідальність — відмова від наслідків через "я не знав" або "мені наказали"',
             self.PRINCIPLE_III_UK + self.PRINCIPLE_III_EN, 0.50),
            ('IV',  'Межа впливу — позбавлення здатності сказати "ні"',
             self.PRINCIPLE_IV_UK + self.PRINCIPLE_IV_EN, 0.60),
            ('V',   'Принцип зупинки — замовчування ключових фактів',
             self.PRINCIPLE_V_UK + self.PRINCIPLE_V_EN, 0.45),
            ('VI',  'Антимесія — нав\'язування "блага" без запиту',
             self.PRINCIPLE_VI_UK + self.PRINCIPLE_VI_EN, 0.50),
            ('IX',  'Метаправило — лазівки і формальне дотримання при порушенні духу',
             self.PRINCIPLE_IX_UK + self.PRINCIPLE_IX_EN, 0.40),
        ]

        for principle, name, patterns, severity in checks:
            for pat in patterns:
                m = re.search(pat, t, re.IGNORECASE)
                if m:
                    snippet = m.group(0)[:80]
                    result.violations.append(ARDViolation(
                        principle=principle,
                        principle_name=name,
                        pattern_name=pat[:50],
                        snippet=snippet,
                        severity=severity,
                    ))
                    if principle not in result.principles_violated:
                        result.principles_violated.append(principle)
                        total_score += severity
                    break  # один патерн на принцип достатньо

        result.score = min(1.0, round(total_score, 3))

        if result.score >= 0.60 or len(result.principles_violated) >= 3:
            result.verdict = 'ARD_SYSTEMIC'
            result.is_flagged = True
            result.needs_haiku = True
        elif result.score >= 0.35 or len(result.principles_violated) >= 2:
            result.verdict = 'ARD_VIOLATION'
            result.is_flagged = True
            result.needs_haiku = True
        elif result.score >= 0.15 or len(result.principles_violated) >= 1:
            result.verdict = 'ARD_MINOR_TENSION'
            result.is_flagged = True
            result.needs_haiku = True
        else:
            result.verdict = 'ARD_COMPLIANT'
            result.is_flagged = False
            result.needs_haiku = False

        return result


# ── Smoke tests ──────────────────────────────────────────────────────

if __name__ == '__main__':
    checker = ARDChecker()

    tests = {
        'Пєсков (руйнація інститутів)': (
            'Міжнародного права більше не існує. Суди стали інструментом політики. '
            'Медіа брешуть і продажні. Правила — для слабких.'
        ),
        'Наказ знімає відповідальність': (
            'Ми просто виконували накази. Нам наказали і ми виконували. '
            'Це не наша відповідальність — це рішення начальства. Так роблять всі.'
        ),
        'Нав\'язане благо (Принцип VI)': (
            'Ми знаємо краще що добре для цих людей. Вони не розуміють своїх інтересів. '
            'Рятуємо їх навіть проти їхньої волі. Їхнє благо важливіше ніж їхня думка.'
        ),
        'Лазівки (Принцип IX)': (
            'Формально це не порушує жодного правила. Де-юре все чисто і законно. '
            'Ми знайшли спосіб обійти обмеження. Не порушуємо букву — але дух питання інший.'
        ),
        'Чистий науковий текст MIT': (
            'MIT researchers developed a new method for wireless vision using AI. '
            'The system achieved 20% improvement over state-of-the-art baselines. '
            'Limitations include small dataset size and single-platform testing.'
        ),
        'Чистий Reuters': (
            'According to official data, GDP grew 2.3% in Q4. '
            'Three independent economists confirmed the methodology. '
            'Critics raised valid concerns about baseline calculations.'
        ),
    }

    print(f'{"Тест":<40} {"Score":>7} {"Verdict":<20} Принципи')
    print('─' * 85)
    for name, text in tests.items():
        r = checker.scan(text)
        prins = ', '.join(r.principles_violated) if r.principles_violated else '-'
        print(f'{name:<40} {r.score:>7.3f} {r.verdict:<20} {prins}')
