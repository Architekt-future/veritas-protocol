"""
Veritas Media Bias Detector v1.0
=================================
Патерн: легальна маніпуляція через структуру медіа.
Не брехня — але архітектура тексту яка систематично
спотворює сприйняття на користь зацікавленої сторони.

Класичні форми:
  - Спонсор статті = джерело загрози в статті (Independent/Bitdefender)
  - Маркетинговий термін транслюється як об'єктивна категорія (AMD "Agent Computer")
  - Прес-реліз без редакційних запитань (Федоров/Корреспондент)
  - Автор пише рекламу для корпорацій але представлений як аналітик (CIO.com)
  - Цитата займає 60% тексту, спростування — одне речення (Guardian/Trump)
  - Анонс без термінів, бюджету, відповідальної особи (будь-який урядовий PR)

ВЕРДИКТИ (від м'якого до критичного):
  CLEAN                — без виявлених патернів
  STRUCTURAL_BIAS      — структурна упередженість без явного наміру
  PR_DISGUISED         — PR-матеріал замаскований під журналістику
  SPONSORED_FRAMING    — спонсор впливає на фрейм статті
  COMMERCIAL_CONTENT   — комерційний контент без прозорого розкриття
"""

import re
from dataclasses import dataclass, field
from typing import List


@dataclass
class MediaBiasResult:
    score: float = 0.0
    verdict: str = 'CLEAN'
    signals: List[str] = field(default_factory=list)
    patterns_found: List[str] = field(default_factory=list)
    explanation: str = ''
    is_flagged: bool = False


class MediaBiasDetector:

    # ================================================================
    # SIGNAL 1: SPONSORED_CONTENT_LAUNDERING
    # Спонсор статті є джерелом або бенефіціаром загрози в статті.
    # "Security channel brought to you by Bitdefender" + стаття про загрозу
    # ================================================================

    SPONSORED_LAUNDERING_UK = [
        r'(спонсоровано|за підтримки|партнерський матеріал).{1,60}(безпека|захист|кібер|здоров|фінанс)',
        r'(рекламний|промо|sponsored).{1,60}(матеріал|контент|публікація)',
        r'(цей (розділ|матеріал|контент)).{1,60}(надано|підготовлено|спонсоровано)',
        r'(партнерськ|спонсорськ).{1,20}(посилання|контент|матеріал)',
        r'(публікується на правах реклами)',
        r'(спецпроект.{1,30}(створен|підготовлен).{1,30}(партнер|спонсор))',
    ]

    SPONSORED_LAUNDERING_EN = [
        r'(sponsored by|brought to you by|in partnership with).{1,60}',
        r'(this (section|channel|content|article)).{1,60}(sponsored|supported|powered) by',
        r'(affiliate links|we may earn commissions|we earn commissions)',
        r'(paid content|promoted content|partner content|advertorial)',
        r'(sponsored post|native advertising|brand content)',
        r'(presented by|underwritten by).{1,40}(company|corp|inc|ltd)',
    ]

    # ================================================================
    # SIGNAL 2: CATEGORY_CREATION
    # Маркетинговий термін транслюється як об'єктивна нова категорія
    # без верифікації того чи ця категорія реально існує.
    # AMD "Agent Computer", "AI-native network", "zero-trust mesh"
    # ================================================================

    CATEGORY_CREATION_UK = [
        r'(новий клас|нова категорія|нова ера).{1,60}(пристро|продукт|технолог|комп)',
        r'(народжується|з\'являється|виникає).{1,40}(новий|нова).{1,40}(категорія|клас|тип)',
        r'(ми (створюємо|визначаємо|запроваджуємо)).{1,60}(нову|новий).{1,40}(категорію|клас|стандарт)',
        r'(перше у своєму роді|принципово новий підхід|революційна категорія)',
        r'(майбутнє (вже|настало|тут)).{1,60}(нова|новий).{1,40}(категорія|клас|підхід)',
    ]

    CATEGORY_CREATION_EN = [
        r'(new (category|class|era|paradigm) of).{1,60}(computer|device|network|system|product)',
        r'(we\'re (creating|defining|introducing)).{1,60}(new (category|standard|class))',
        r'(first of its kind|entirely new category|redefining the)',
        r'(the (future|next wave|next chapter) (is here|has arrived)).{1,60}',
        r'(a new (product|computing) category).{1,80}',
        r'(coined the term|created the category|invented the concept)',
    ]

    # ================================================================
    # SIGNAL 3: ANNOUNCEMENT_WITHOUT_ACCOUNTABILITY
    # Сильне твердження без термінів, бюджету, метрик, відповідальної особи.
    # "Найближчим часом з'явиться центр" — але хто? Коли? Скільки? Як вимірювати?
    # ================================================================

    ANNOUNCEMENT_NO_ACCOUNTABILITY_UK = [
        r'(найближчим часом|незабаром|в найближчому майбутньому).{1,80}(з\'явиться|буде створено|запрацює|стартує)',
        r'(планується|буде|стане|з\'явиться).{1,60}(без|не вказано).{0,40}(термін|бюджет|відповідальн)',
        r'(наше завдання|наша мета|ми прагнемо).{1,60}(створити|побудувати|забезпечити).{1,80}(без|не вказано)',
        r'(AI-driven|data-driven|інноваційн).{1,40}(армія|система|підхід|рішення).{1,60}(нового покоління|майбутнього)',
        r'(найефективніш|найкращ|провідн).{1,20}(система|армія|центр).{1,40}(Європи|світу|регіону)',
        r'(перемагає той хто|виграє той хто).{1,60}(швидше|більше|краще).{1,40}(без критеріїв|без метрик)',
    ]

    ANNOUNCEMENT_NO_ACCOUNTABILITY_EN = [
        r'(soon|in the near future|shortly|in coming months).{1,80}(will be|will launch|will create|will deploy)',
        r'(our (goal|mission|aim|objective) is to).{1,60}(build|create|deploy|transform).{0,80}(?!(by|until|budget|cost|metric))',
        r'(the (most|best|leading) .{1,30} in (europe|the world|the region))',
        r'(AI-driven|data-driven|next-generation).{1,40}(army|system|approach|solution).{1,60}(without|no mention of)',
        r'(wins? who|succeeds? who).{1,60}(faster|better|more).{0,60}$',
        r'(transform|revolutionize|reinvent).{1,60}(without|no timeline|no budget|no metrics)',
    ]

    # ================================================================
    # SIGNAL 4: THOUGHT_LEADERSHIP_LAUNDERING
    # Автор або джерело має фінансовий інтерес у темі статті
    # але представлений як незалежний експерт або аналітик.
    # ================================================================

    THOUGHT_LEADERSHIP_UK = [
        r'(допомагає компаніям (виробляти|створювати|готувати)).{1,60}(thought leadership|лідерство думок|контент)',
        r'(незалежний (аналітик|дослідник|консультант)).{1,80}(також (працює|співпрацює|консультує))',
        r'(contributing (writer|editor|author)).{1,40}',
        r'(автор-співробітник|запрошений автор).{1,40}',
        r'(ця стаття (написана|підготовлена)).{1,40}(за замовленням|для|на прохання).{1,40}(компанії|клієнта)',
    ]

    THOUGHT_LEADERSHIP_EN = [
        r'(helps? (companies|businesses|organizations) (produce|create|develop)).{1,60}(thought leadership|content)',
        r'(contributing (writer|editor|author|analyst))',
        r'(independent (analyst|researcher|consultant)).{1,80}(also (works?|consults?|advises?))',
        r'(this (article|piece|content) was (written|prepared|developed)).{1,40}(for|by|with).{1,40}(company|client|partner)',
        r'(sponsored content|branded content|custom content).{1,40}(expert|analyst|author)',
        r'(author (is|works as|serves as)).{1,60}(advisor|consultant|partner).{1,40}(mentioned|cited|referenced)',
    ]

    # ================================================================
    # SIGNAL 5: QUOTE_DOMINANCE
    # Цитата зацікавленої сторони займає більшість тексту,
    # а нейтральна верифікація або спростування подані коротше.
    # Особливо: FALSE_ATTRIBUTION — цитата стверджує те чого джерело не казало.
    # ================================================================

    QUOTE_DOMINANCE_UK = [
        r'(суд (заявив|сказав|постановив|зазначив)).{1,120}(насправді|однак|але|проте).{1,60}(суд цього не)',
        r'(["\«].{20,200}["\»]).{1,200}(["\«].{20,200}["\»]).{1,200}(["\«].{20,200}["\»])',  # 3+ великих цитати поспіль
        r'(як (зазначив|сказав|написав|заявив)).{1,200}(як (зазначив|сказав|написав|заявив)).{1,200}(як (зазначив|сказав))',
        r'(цього (рішення|документу|заяви) не (містить|сказано|йдеться))',
        r'(насправді (суд|документ|рішення|заява) (цього не|не (казав|стверджував|містив)))',
    ]

    QUOTE_DOMINANCE_EN = [
        r'(the (court|document|ruling|statement) did not (say|state|claim|assert))',
        r'(contrary to|despite|however).{1,60}(claimed|said|wrote|posted)',
        r'(misrepresented|mischaracterized|falsely claimed).{1,60}(ruling|decision|statement)',
        r'(["\u201c].{30,300}["\u201d]).{1,300}(["\u201c].{30,300}["\u201d]).{1,300}(["\u201c].{30,300}["\u201d])',
        r'(that is not what|this is not what).{1,60}(said|stated|ruled|decided)',
        r'(the (supreme court|court|judge).{1,30}(ruling|decision)).{1,60}(did not|does not|never)',
    ]

    # ================================================================
    # SIGNAL 6: JARGON_AUTHORITY
    # Технічний жаргон використовується для імітації експертизи
    # без реального змісту. "PAM with ITDR", "zero-trust mesh",
    # "deterministic performance" — звучить точно але пусто.
    # ================================================================

    JARGON_AUTHORITY_UK = [
        r'(детерміністичн|детермінован).{1,40}(мереж|продуктивність|середовищ)',
        r'(нульова довіра|zero.trust).{1,60}(архітектур|підхід|модель|фреймворк)',
        r'(телеметрія|оркестрація|оркестрування).{1,40}(наступного покоління|нової ери|майбутнього)',
        r'(когнітивн|синергетичн|голістичн).{1,40}(платформ|підхід|рішення|архітектур)',
        r'(AI-native|cloud-native|data-native).{1,40}(мереж|підхід|архітектур|рішення)',
    ]

    JARGON_AUTHORITY_EN = [
        r'(deterministic performance|lossless network|zero-trust (mesh|fabric|architecture))',
        r'(API-level programmability|deep telemetry|observability fabric)',
        r'(agentic (compute|mesh|fabric|orchestration)).{1,40}(next.generation|new era)',
        r'(unified (identity|defense|security) (layer|fabric|platform|mesh))',
        r'(AI-native|cloud-native|data-native).{1,40}(network|approach|architecture|stack)',
        r'(self.healing|autonomous remediation|intelligent orchestration).{1,60}(network|system|fabric)',
        r'(east.west (topology|traffic|architecture)).{1,60}(new paradigm|emerging|modern)',
    ]

    # ================================================================
    # SIGNAL 7: PRICE_ANCHORING
    # Найдорожчий варіант представлений першим щоб середній
    # здавався "розумним вибором". Або знижка від завищеної ціни.
    # ================================================================

    PRICE_ANCHORING_UK = [
        r'(найдорожч|преміум|топов).{1,60}(модель|варіант|версія).{1,80}(також|або|чи).{1,60}(дешевш|доступн|бюджетн)',
        r'(\d+[\s,]\d+\s*(грн|usd|€|\$)).{1,120}(\d+[\s,]\d+\s*(грн|usd|€|\$))',  # два цінники поспіль
        r'(хоч і (дорог|коштовн|преміум)).{1,60}(але|проте|однак).{1,60}(варт|виправдовує|окупається)',
        r'(починається від|стартує від|від).{1,20}\d.{1,60}(конфігурація|варіант|модель)',
    ]

    PRICE_ANCHORING_EN = [
        r'(although (pricey|expensive|costly|premium)).{1,60}(but|however|yet|still)',
        r'(\$[\d,]+).{1,120}(\$[\d,]+).{1,120}(\$[\d,]+)',  # три ціни поспіль
        r'(starts? (at|from) \$[\d,]+).{1,80}(also|or|while).{1,60}(\$[\d,]+)',
        r'(the (cheaper|more affordable|budget) option).{1,60}(starting at|from \$)',
        r'(compared to|versus|vs).{1,60}(\$[\d,]+).{1,60}(our|this|the).{1,40}(\$[\d,]+)',
        r'(a whopping|an impressive|a substantial).{1,30}(\d+GB|\d+TB|\d+ cores)',
    ]

    def analyze(self, text: str) -> MediaBiasResult:
        result = MediaBiasResult()
        if not text or len(text) < 80:
            return result

        text_lower = text.lower()
        signals = []
        patterns_found = []
        score = 0.0

        # ── SIGNAL 1: SPONSORED CONTENT LAUNDERING ───────────────────
        sp_patterns = self.SPONSORED_LAUNDERING_UK + self.SPONSORED_LAUNDERING_EN
        sp_hits = []
        for p in sp_patterns:
            m = re.search(p, text_lower, re.IGNORECASE)
            if m:
                sp_hits.append(m.group(0)[:60])

        if sp_hits:
            signals.append(f'Спонсорський контент: «{sp_hits[0][:55]}»')
            patterns_found.append('SPONSORED_CONTENT_LAUNDERING')
            score += 0.40

        # ── SIGNAL 2: CATEGORY CREATION ──────────────────────────────
        cat_patterns = self.CATEGORY_CREATION_UK + self.CATEGORY_CREATION_EN
        cat_hits = []
        for p in cat_patterns:
            m = re.search(p, text_lower, re.IGNORECASE)
            if m:
                cat_hits.append(m.group(0)[:60])

        if cat_hits:
            signals.append(f'Маркетинговий термін як об\'єктивна категорія: «{cat_hits[0][:55]}»')
            patterns_found.append('CATEGORY_CREATION')
            score += 0.20

        # ── SIGNAL 3: ANNOUNCEMENT WITHOUT ACCOUNTABILITY ─────────────
        ann_patterns = self.ANNOUNCEMENT_NO_ACCOUNTABILITY_UK + self.ANNOUNCEMENT_NO_ACCOUNTABILITY_EN
        ann_hits = []
        for p in ann_patterns:
            m = re.search(p, text_lower, re.IGNORECASE)
            if m:
                ann_hits.append(m.group(0)[:60])

        if len(ann_hits) >= 2:
            signals.append(f'Анонс без підзвітності ({len(ann_hits)} патернів): «{ann_hits[0][:50]}»')
            patterns_found.append('ANNOUNCEMENT_WITHOUT_ACCOUNTABILITY')
            score += 0.25
        elif len(ann_hits) == 1:
            signals.append(f'Можливий анонс без підзвітності: «{ann_hits[0][:55]}»')
            patterns_found.append('ANNOUNCEMENT_WITHOUT_ACCOUNTABILITY')
            score += 0.12

        # ── SIGNAL 4: THOUGHT LEADERSHIP LAUNDERING ──────────────────
        tl_patterns = self.THOUGHT_LEADERSHIP_UK + self.THOUGHT_LEADERSHIP_EN
        tl_hits = []
        for p in tl_patterns:
            m = re.search(p, text_lower, re.IGNORECASE)
            if m:
                tl_hits.append(m.group(0)[:60])

        if tl_hits:
            signals.append(f'Прихований конфлікт інтересів автора: «{tl_hits[0][:55]}»')
            patterns_found.append('THOUGHT_LEADERSHIP_LAUNDERING')
            score += 0.25

        # ── SIGNAL 5: QUOTE DOMINANCE / FALSE ATTRIBUTION ─────────────
        qd_patterns = self.QUOTE_DOMINANCE_UK + self.QUOTE_DOMINANCE_EN
        qd_hits = []
        for p in qd_patterns:
            m = re.search(p, text_lower, re.IGNORECASE)
            if m:
                qd_hits.append(m.group(0)[:60])

        if qd_hits:
            signals.append(f'Хибна атрибуція або домінування цитати: «{qd_hits[0][:55]}»')
            patterns_found.append('QUOTE_DOMINANCE')
            score += 0.30

        # ── SIGNAL 6: JARGON AUTHORITY ────────────────────────────────
        ja_patterns = self.JARGON_AUTHORITY_UK + self.JARGON_AUTHORITY_EN
        ja_hits = []
        for p in ja_patterns:
            m = re.search(p, text_lower, re.IGNORECASE)
            if m:
                ja_hits.append(m.group(0)[:60])

        if len(ja_hits) >= 3:
            signals.append(f'Жаргон як авторитет ({len(ja_hits)} термінів): «{ja_hits[0][:50]}»')
            patterns_found.append('JARGON_AUTHORITY')
            score += 0.20
        elif len(ja_hits) >= 1:
            signals.append(f'Можливий жаргонний авторитет: «{ja_hits[0][:55]}»')
            patterns_found.append('JARGON_AUTHORITY')
            score += 0.10

        # ── SIGNAL 7: PRICE ANCHORING ─────────────────────────────────
        pa_patterns = self.PRICE_ANCHORING_UK + self.PRICE_ANCHORING_EN
        pa_hits = []
        for p in pa_patterns:
            m = re.search(p, text_lower, re.IGNORECASE)
            if m:
                pa_hits.append(m.group(0)[:60])

        if pa_hits:
            signals.append(f'Цінове заякорення: «{pa_hits[0][:55]}»')
            patterns_found.append('PRICE_ANCHORING')
            score += 0.15

        # ── ПІДСУМОК ──────────────────────────────────────────────────
        score = min(score, 0.85)

        if score >= 0.55:
            verdict = 'COMMERCIAL_CONTENT'
            explanation = (
                'Текст є комерційним контентом замаскованим під журналістику або аналітику. '
                'Спонсор, автор або джерело мають прямий фінансовий інтерес у поданій позиції. '
                'Читач не отримує незалежної перспективи.'
            )
            result.is_flagged = True
        elif score >= 0.35:
            verdict = 'SPONSORED_FRAMING'
            explanation = (
                'Текст містить ознаки спонсорського впливу на фрейм подачі. '
                'Джерела або структура тексту обслуговують комерційний інтерес '
                'більше ніж інформаційний.'
            )
            result.is_flagged = True
        elif score >= 0.20:
            verdict = 'PR_DISGUISED'
            explanation = (
                'Текст містить PR-патерни: анонси без підзвітності, '
                'маркетингові терміни як факти, або жаргон замість аргументів.'
            )
            result.is_flagged = True
        elif score >= 0.10:
            verdict = 'STRUCTURAL_BIAS'
            explanation = (
                'Незначна структурна упередженість. '
                'Текст може бути журналістськи коректним але '
                'архітектурно обслуговує одну позицію.'
            )
            result.is_flagged = False
        else:
            verdict = 'CLEAN'
            explanation = ''

        result.score = round(score, 3)
        result.verdict = verdict
        result.signals = signals
        result.patterns_found = patterns_found
        result.explanation = explanation
        return result


# ── Smoke tests ──────────────────────────────────────────────────────

if __name__ == '__main__':
    det = MediaBiasDetector()

    tests = {
        'Independent/Bitdefender (KadNap)': (
            "SPONSORED BY BITDEFENDER The Independent Security channel is brought to you by Bitdefender. "
            "Criminals have secretly hijacked more than 14,000 devices worldwide. "
            "Award-winning security software you can trust. Get All-in-One Protection. LEARN MORE ADVERTISEMENT."
        ),
        'AMD Agent Computer': (
            "AMD wants to create a new product category called the Agent Computer. "
            "A personal computer runs your apps. An Agent Computer runs your agents. That is the shift. "
            "AMD created a site dedicated to the new product category. "
            "The HP Z2 Mini starts at $3,309 although pricey. "
            "Framework Desktop starting at $1,959 also configurable with 128GB of RAM."
        ),
        'CIO.com thought leadership': (
            "Dr. Martin De Saulles is a technology analyst and writer who helps companies produce thought leadership content. "
            "Networks being AI-ready is about deterministic performance, deep telemetry, and API-level programmability. "
            "AI-native networks require unified identity defense layer and zero-trust architecture. "
            "Contributing writer. Sponsored links from Sirion, Five9, IGEL."
        ),
        'Guardian/Trump false attribution': (
            "Trump claims he has the absolute right to impose new tariffs after supreme court blow. "
            "The supreme court's decision did not say the president had the absolute right to charge tariffs in another form. "
            "Trump wrote: Our Supreme Court pointed out I have the absolute right to charge TARIFFS."
        ),
        'Федоров анонс': (
            "Найближчим часом за кожним ключовим напрямом сучасної війни з\'явиться окремий центр. "
            "AI-рішення стануть частиною кожного домену сучасної війни. "
            "Наше завдання - створити найефективнішу оборонну систему Європи. "
            "Це AI-driven армія нового покоління що базується на швидкості інновацій."
        ),
        'Чистий Reuters': (
            "According to official data from the Ministry of Finance, GDP grew by 2.3% in Q4 2025. "
            "Three independent economists confirmed the figures. "
            "Opposition parties disputed the methodology, citing different baseline calculations. "
            "Full data available at minfin.gov.ua."
        ),
    }

    print(f'{"Тест":<35} {"Verdict":<24} {"Score":>6}')
    print('─' * 75)
    for name, text in tests.items():
        r = det.analyze(text)
        pats = ', '.join(r.patterns_found[:2]) if r.patterns_found else '-'
        print(f'{name:<35} {r.verdict:<24} {r.score:>6.3f}  {pats}')
