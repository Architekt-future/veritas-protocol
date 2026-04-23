"""
Veritas Alarmism Detector v1.0
================================
Патерн: текст створює тривогу без інформування.
Комерційний алармізм, медіа-монетизація через страх,
корпоративні звіти з зацікавленим джерелом.

Класичні форми:
  - CyberSec firm: "unprecedented threat" → buy our product
  - Pharma: "millions at risk" → one unnamed study
  - Tech media: "impossible to protect" → ads for antivirus
  - Health scare: "doctors warn" → no doctors named

Відрізняється від маніпуляції тим що фактаж може бути реальним —
але архітектура тексту веде до тривоги і покупки, а не до розуміння.

SIGNALS:
  1. ALARM_WITHOUT_ACTION — загроза без конкретного виходу
  2. SINGLE_INTERESTED_SOURCE — єдине джерело є зацікавленою стороною
  3. FEAR_TO_PRODUCT — загроза → реклама/CTA → загроза
  4. SUPERLATIVE_THREAT — "never-before-seen", "unprecedented" без верифікації
  5. VAGUE_SCALE — великі числа без методології
"""

import re
from dataclasses import dataclass, field
from typing import List


@dataclass
class AlarmismResult:
    score: float = 0.0
    verdict: str = 'CLEAN'
    signals: List[str] = field(default_factory=list)
    explanation: str = ''
    is_flagged: bool = False


class AlarmismDetector:

    # ================================================================
    # SIGNAL 1: ALARM WITHOUT ACTION
    # Загроза описана але виходу немає — мета тривога, не інформування
    # ================================================================

    ALARM_WITHOUT_ACTION_UK = [
        r'(неможливо|не можна).{1,60}(захистити|зупинити|запобігти|протидіяти)',
        r'(захиститися|протидіяти).{1,60}(практично|фактично|майже).{1,60}(неможливо|нереально)',
        r'(загроза|ризик|небезпека).{1,60}(яку (не можна|неможливо)|без (захисту|виходу))',
        r'(жертви|постраждалі|під загрозою).{1,60}(не (знають|підозрюють)|нічого не (знають|підозрюють))',
        r'(атака|загроза|вірус).{1,60}(непомітн|невидим|не (виявляється|детектується))',
        r'(ніхто не|неможливо).{1,60}(зупинити|нейтралізувати|протидіяти)',
    ]

    ALARM_WITHOUT_ACTION_EN = [
        r'(impossible|nearly impossible|almost impossible).{1,60}(to protect|to defend|to stop|to prevent)',
        r'(protect|defend).{1,60}(against).{1,60}(impossible|incredibly difficult|near impossible)',
        r'(threat|risk|danger).{1,60}(cannot be (stopped|detected|prevented))',
        r'(victims|infected|affected).{1,60}(unaware|wouldn\'t know|no way to tell)',
        r'(attack|malware|threat).{1,60}(undetectable|invisible|goes unnoticed)',
        r'(no (way|means|method)).{1,60}(to (stop|detect|prevent|protect))',
        r'(resilient|resistant).{1,60}(attempts to (shut down|dismantle|stop))',
        r'makes.{1,40}(impossible|incredibly hard|nearly impossible).{1,40}(to (defend|protect|detect))',
    ]

    # ================================================================
    # SIGNAL 2: SINGLE INTERESTED SOURCE
    # Єдине джерело = компанія що продає рішення від цієї ж загрози
    # ================================================================

    INTERESTED_SOURCE_MARKERS_UK = [
        r'(компанія|фірма|дослідники).{1,60}(з кібербезпеки|безпеки|захисту).{1,60}(виявил|повідомил|попередил)',
        r'(звіт|дослідження).{1,60}(компанії|фірми).{1,60}(безпеки|кібербезпеки|захисту)',
        r'(виробник|розробник).{1,60}(антивірус|захист|безпека).{1,60}(попередж|виявил|звіт)',
        r'(фармацевтичн|медичн).{1,60}(компанія|корпорація).{1,60}(дослідження|звіт|виявил)',
        r'(дослідження|звіт).{1,60}(фінансован|замовлен|проведен).{1,60}(компанією|корпорацією)',
    ]

    INTERESTED_SOURCE_MARKERS_EN = [
        r'(cybersecurity|security).{1,40}(firm|company|researcher).{1,60}(found|discovered|warned|revealed)',
        r'(report|study).{1,60}(by|from).{1,60}(cybersecurity|security|antivirus).{1,40}(firm|company)',
        r'(antivirus|security software).{1,60}(company|maker|vendor).{1,60}(warns|reports|discovered)',
        r'(pharmaceutical|drug).{1,60}(company|maker).{1,60}(study|research|trial)',
        r'(study|research).{1,60}(funded|commissioned|conducted).{1,60}(by).{1,60}(company|corporation|manufacturer)',
        r'(lumen|crowdstrike|kaspersky|symantec|mcafee|norton|avast|eset).{1,60}(report|study|research|warns)',
    ]

    # ================================================================
    # SIGNAL 3: FEAR TO PRODUCT
    # Архітектурний патерн: загроза → CTA/реклама → загроза
    # ================================================================

    FEAR_TO_PRODUCT_UK = [
        r'(захистіть|убезпечте|захисти).{1,60}(себе|свій|свої).{1,60}(зараз|сьогодні|негайно)',
        r'(отримай|завантаж|купи|спробуй).{1,60}(захист|антивірус|безпека|програм)',
        r'(повний захист|комплексний захист|надійний захист).{1,60}(цифров|онлайн|пристро)',
        r'(реклама|advertisement|sponsored).{0,20}(захист|безпека|antivirus|security)',
        r'(дізнайтесь більше|learn more|детальніше).{1,60}(захист|безпека|security)',
    ]

    FEAR_TO_PRODUCT_EN = [
        r'(protect yourself|stay protected|get protected).{1,60}(now|today|immediately)',
        r'(download|get|buy|try).{1,60}(protection|antivirus|security|software)',
        r'(all.in.one|complete|total|award.winning).{1,60}(protection|security|defense)',
        r'advertisement.{0,200}(protection|security|antivirus|software)',
        r'(learn more|get started|try free).{1,60}(protection|security|digital)',
        r'(sponsored|advertisement|ad).{0,30}(security|protect|antivirus)',
    ]

    # ================================================================
    # SIGNAL 4: SUPERLATIVE THREAT
    # "never-before-seen", "unprecedented" без верифікації
    # Перебільшення масштабу загрози
    # ================================================================

    SUPERLATIVE_THREAT_UK = [
        r'(небачен|безпрецедентн|унікальн).{1,60}(загроза|атака|вірус|зброя|метод)',
        r'(вперше в (історії|світі|практиці)).{1,60}(виявлен|зафіксован|створен)',
        r'(найнебезпечніш|найскладніш|найпотужніш).{1,60}(загроза|вірус|атака|зброя)',
        r'(принципово нов|революційно нов).{1,60}(метод|спосіб|підхід|вірус|атака)',
        r'(ніколи раніше|вперше).{1,60}(не (бачили|фіксували|стикалися))',
    ]

    SUPERLATIVE_THREAT_EN = [
        r'(never.before.seen|never seen before|first of its kind)',
        r'(unprecedented|unparalleled|unlike anything).{1,60}(threat|attack|malware|weapon|method)',
        r'(most (dangerous|sophisticated|advanced|powerful)).{1,60}(ever|in history|to date)',
        r'(brand new|entirely new|completely new).{1,60}(type of|kind of|form of).{1,60}(threat|attack|malware)',
        r'(researchers have never|experts have never).{1,60}(seen|encountered|documented)',
        r'(cyber.?weapon|cyberweapon).{1,60}(new|novel|unprecedented)',
        r'(new (class|breed|generation) of).{1,40}(threat|attack|malware|weapon)',
        r'(unlike (anything|any (threat|malware|attack)) (we\'ve|we have|researchers have) (seen|encountered))',
        r'(redefin(es?|ing) (the|what).{1,30}(threat|attack|danger|risk))',
        r'(raises? the (bar|stakes) (on|for).{1,40}(security|cybersecurity|defense))',
    ]

    # ================================================================
    # SIGNAL 5: VAGUE SCALE
    # Великі числа без методології — "thousands", "millions at risk"
    # ================================================================

    VAGUE_SCALE_UK = [
        r'(тисяч|мільйон|мільярд).{1,60}(пристро|користувач|людей|жертв).{1,60}(під загрозою|постраждал|інфікован)',
        r'(мільйони|мільярди).{1,60}(ризикують|під ризиком|у небезпеці)',
        r'(величезн|масштабн|колосальн).{1,60}(загроза|ризик|масштаб|збитки)',
        r'(по всьому світу|у всьому світі|глобально).{1,60}(загроза|атака|поширен)',
        r'\d+\s*(тисяч|мільйон).{1,60}(пристро|жертв|інфікован|уражен)',
    ]

    VAGUE_SCALE_EN = [
        r'(thousands|millions|billions).{1,60}(devices|users|people|victims).{1,60}(at risk|affected|infected|compromised)',
        r'(millions|billions).{1,60}(at risk|in danger|could be affected)',
        r'(massive|enormous|unprecedented).{1,60}(scale|threat|risk|impact)',
        r'(worldwide|globally|across the globe).{1,60}(threat|attack|spread|impact)',
        r'\d{1,3}[,.]?\d{3}\+?.{1,60}(devices|systems|users|victims).{1,60}(hijacked|infected|compromised)',
        r'(every|any).{1,20}(device|router|system).{1,60}(could be|is potentially|at risk)',
        r'(vast (majority|number) of).{1,60}(users|devices|people|organizations)',
        r'(potentially (affect(ing)?|impact(ing)?)).{1,60}(millions|billions|everyone|all)',
        r'(no (organization|company|individual|device) is.{1,20}(safe|immune|protected))',
    ]

    # ================================================================
    # SIGNAL 6: TEMPORAL COMPRESSION (геополітичний)
    # "може статися через рік" але текст створює відчуття що вже зараз
    # Патерн: умовний горизонт на початку + перехід до вже існуючих інцидентів
    # ================================================================

    TEMPORAL_COMPRESSION_UK = [
        r'(може|здатна|готова).{1,80}(протягом|через|впродовж).{1,30}(рок|місяц|тижн)',
        r'(за (найсприятливіших|певних|відповідних) умов).{1,80}(може|здатна|готова)',
        r'(сценарі[їй]|варіант).{1,60}(рок|місяц).{1,60}(після|від)',
        r'(прогноз|оцінк).{1,60}(рок|місяц).{1,60}(конфлікт|напад|удар|загроз)',
    ]

    TEMPORAL_COMPRESSION_EN = [
        r'(could|may|might).{1,80}(within|in).{1,30}(year|month|weeks?)',
        r'(under (favorable|certain|the right) conditions).{1,80}(could|may|might)',
        r'(scenario|timeline).{1,60}(year|month).{1,60}(after|from|following)',
        r'(forecast|assessment|estimate).{1,60}(year|month).{1,60}(conflict|attack|strike|threat)',
    ]

    # ================================================================
    # SIGNAL 7: THREAT ACCUMULATION (геополітичний)
    # Текст починається з однієї теми але акумулює різні загрози
    # без логічного зв'язку між ними
    # ================================================================

    THREAT_ACCUMULATION_MARKERS_UK = [
        r'(шпигун|розвідник|агент).{1,60}(заарештован|затриман|викрит|звільнен|звільнили|затримали)',
        r'(кібератак|кіберудар|кіберзагроз).{1,60}(інфраструктур|держав|критичн)',
        r'(ядерн).{1,60}(загроз|зброя|шантаж)',
        r'(диверсі[їя]).{1,60}(інфраструктур|обєкт|мережі)',
        r'(гібридн).{1,60}(атак|загроз|операці)',
    ]

    THREAT_ACCUMULATION_MARKERS_EN = [
        r'(spy|agent|intelligence officer).{1,60}(arrested|detained|caught|fired|dismissed)',
        r'(cyberattack|cyber strike|cyber threat).{1,60}(infrastructure|state|critical)',
        r'(nuclear).{1,60}(threat|weapon|blackmail|escalation)',
        r'(sabotage|subversion).{1,60}(infrastructure|facility|network)',
        r'(hybrid).{1,60}(attack|threat|operation|warfare)',
    ]

    # ================================================================
    # SIGNAL 8: OFFICIAL INTERESTED SOURCE (геополітичний)
    # Офіційне держджерело як єдине підтвердження власних тверджень
    # Розвідка у власному звіті, міністерство в пресрелізі
    # ================================================================

    OFFICIAL_INTERESTED_SOURCE_UK = [
        r'(розвідк|спецслужб).{1,120}(річний|власний|свій).{1,120}(звіт|доповідь|оцінка)',
        r'(річний|власний).{1,60}(звіт|доповідь).{1,60}(розвідк|спецслужб|mivd|cia|фсб)',
        r'(міністерств|відомств).{1,60}(повідомляє|заявляє|попереджає).{1,60}(без)',
        r'(за (даними|оцінками|словами)).{1,60}(розвідк|спецслужб|командуванн)',
        r'(єдин|лише|тільки).{1,60}(джерело|підтвердження).{1,60}(розвідк|офіційн)',
    ]

    OFFICIAL_INTERESTED_SOURCE_EN = [
        r'(intelligence|spy agency).{1,60}(its own|annual|own).{1,60}(report|assessment|estimate)',
        r'(ministry|department|agency).{1,60}(says|warns|claims).{1,60}(without|no independent)',
        r'(according to|per).{1,60}(intelligence|military intelligence|defense ministry)',
        r'(only|sole|single).{1,60}(source|confirmation).{1,60}(intelligence|official)',
    ]



    def analyze(self, text: str) -> AlarmismResult:
        result = AlarmismResult()
        if not text or len(text) < 50:
            return result

        text_lower = text.lower()
        signals = []
        score = 0.0

        # ── SIGNAL 1: ALARM WITHOUT ACTION ───────────────────────────
        alarm_patterns = self.ALARM_WITHOUT_ACTION_UK + self.ALARM_WITHOUT_ACTION_EN
        alarm_hits = []
        for p in alarm_patterns:
            m = re.search(p, text_lower, re.IGNORECASE)
            if m:
                alarm_hits.append(m.group(0)[:60])

        if alarm_hits:
            # Перевіряємо чи є конкретні поради/дії в тексті
            action_markers = [
                r'(оновіть|встановіть|перевірте|змініть|налаштуйте)',
                r'(update|patch|install|check|configure|change|enable|disable)',
                r'(конкретн.{1,20}(крок|порада|дія|захід))',
                r'(specific(ally)?|concretely).{1,40}(step|action|measure)',
                r'(ось що (робити|зробити)|what to do)',
            ]
            has_action = any(re.search(p, text_lower, re.IGNORECASE) for p in action_markers)

            if not has_action:
                signals.append(f'Загроза без конкретного виходу: «{alarm_hits[0][:50]}»')
                score += 0.25
            elif len(alarm_hits) >= 2:
                signals.append(f'Переважає алармізм над порадами ({len(alarm_hits)} тривожних патернів)')
                score += 0.12

        # ── SIGNAL 2: SINGLE INTERESTED SOURCE ───────────────────────
        interested_patterns = (self.INTERESTED_SOURCE_MARKERS_UK +
                               self.INTERESTED_SOURCE_MARKERS_EN)
        interested_hits = []
        for p in interested_patterns:
            m = re.search(p, text_lower, re.IGNORECASE)
            if m:
                interested_hits.append(m.group(0)[:60])

        if interested_hits:
            # Перевіряємо чи є незалежні джерела
            independent_markers = [
                r'(незалежн.{1,20}(експерт|дослідник|організація|джерело))',
                r'(independent (expert|researcher|organization|source|analyst))',
                r'(за даними (ООН|НАТО|Europol|Interpol|FBI|CISA|CERT))',
                r'(according to (UN|NATO|Europol|Interpol|FBI|CISA|CERT|government))',
                r'(кілька (джерел|компаній|дослідників)|multiple (sources|firms|researchers))',
            ]
            has_independent = any(re.search(p, text_lower, re.IGNORECASE)
                                  for p in independent_markers)

            if not has_independent:
                signals.append(f'Єдине джерело — зацікавлена сторона: «{interested_hits[0][:50]}»')
                score += 0.20
            else:
                signals.append('Зацікавлене джерело є, але є й незалежні')
                score += 0.08

        # ── SIGNAL 3: FEAR TO PRODUCT ────────────────────────────────
        fear_product_patterns = self.FEAR_TO_PRODUCT_UK + self.FEAR_TO_PRODUCT_EN
        fp_hits = []
        for p in fear_product_patterns:
            m = re.search(p, text_lower, re.IGNORECASE)
            if m:
                fp_hits.append(m.group(0)[:60])

        if len(fp_hits) >= 2:
            signals.append(f'Комерційний алармізм: загроза → продукт ({len(fp_hits)} патернів)')
            score += 0.25
        elif len(fp_hits) == 1:
            signals.append(f'Можливий комерційний контекст: «{fp_hits[0][:50]}»')
            score += 0.10

        # ── SIGNAL 4: SUPERLATIVE THREAT ─────────────────────────────
        superlative_patterns = self.SUPERLATIVE_THREAT_UK + self.SUPERLATIVE_THREAT_EN
        sup_hits = []
        for p in superlative_patterns:
            m = re.search(p, text_lower, re.IGNORECASE)
            if m:
                sup_hits.append(m.group(0)[:60])

        if sup_hits:
            signals.append(f'Суперлатив загрози без верифікації: «{sup_hits[0][:50]}»')
            score += 0.15

        # ── SIGNAL 5: VAGUE SCALE ─────────────────────────────────────
        scale_patterns = self.VAGUE_SCALE_UK + self.VAGUE_SCALE_EN
        scale_hits = []
        for p in scale_patterns:
            m = re.search(p, text_lower, re.IGNORECASE)
            if m:
                scale_hits.append(m.group(0)[:60])

        if len(scale_hits) >= 2:
            signals.append(f'Масштаб загрози без методології ({len(scale_hits)} патернів)')
            score += 0.15
        elif len(scale_hits) == 1:
            signals.append(f'Розмитий масштаб: «{scale_hits[0][:50]}»')
            score += 0.07

        # ── SIGNAL 6: TEMPORAL COMPRESSION ───────────────────────────
        # "може статися через рік" але накопичення деталей створює відчуття "вже зараз"
        temporal_patterns = self.TEMPORAL_COMPRESSION_UK + self.TEMPORAL_COMPRESSION_EN
        temporal_hits = []
        for p in temporal_patterns:
            m = re.search(p, text_lower, re.IGNORECASE)
            if m:
                temporal_hits.append(m.group(0)[:60])

        if temporal_hits:
            # Перевіряємо чи є в тому ж тексті вже існуючі інциденти
            # (що створює ефект стиснення часу)
            existing_incident_markers = [
                r'(вже|наразі|зараз|тепер).{1,120}(спостеріг|фіксу|виявлен|відбувається|перебуває)',
                r'(already|currently|now|at present).{1,120}(observ|detect|found|occurring|state)',
                r'(також|крім того|водночас|додамо).{1,60}(шпигун|кібер|диверс|співпрац|скандал)',
                r'(наразі).{1,120}(стан|загроз|ризик|перебуває)',
            ]
            has_existing = any(
                re.search(p, text_lower, re.IGNORECASE)
                for p in existing_incident_markers
            )
            if has_existing:
                signals.append(f'Стиснення часу: умовний горизонт + вже існуючі інциденти')
                score += 0.06

        # ── SIGNAL 7: THREAT ACCUMULATION ────────────────────────────
        # Текст акумулює тематично різні загрози без логічного зв'язку
        threat_acc_patterns = (
            self.THREAT_ACCUMULATION_MARKERS_UK +
            self.THREAT_ACCUMULATION_MARKERS_EN
        )
        threat_acc_hits = []
        for p in threat_acc_patterns:
            m = re.search(p, text_lower, re.IGNORECASE)
            if m:
                threat_acc_hits.append(m.group(0)[:60])

        if len(threat_acc_hits) >= 3:
            signals.append(
                f'Картечниця загроз: {len(threat_acc_hits)} різних загроз без зв\'язку'
            )
            score += 0.05

        # ── SIGNAL 8: OFFICIAL INTERESTED SOURCE ─────────────────────
        # Офіційне держджерело як єдине підтвердження власних тверджень
        official_patterns = (
            self.OFFICIAL_INTERESTED_SOURCE_UK +
            self.OFFICIAL_INTERESTED_SOURCE_EN
        )
        official_hits = []
        for p in official_patterns:
            m = re.search(p, text_lower, re.IGNORECASE)
            if m:
                official_hits.append(m.group(0)[:60])

        if official_hits:
            # Перевіряємо чи є незалежні джерела в тексті
            independent_markers = [
                r'(незалежн).{1,60}(експерт|аналітик|дослідник)',
                r'(independent|separate).{1,60}(expert|analyst|researcher|assessment)',
                r'(також|підтвердж).{1,60}(інш|окрем|додатков).{1,60}(джерел|експерт)',
            ]
            has_independent = any(
                re.search(p, text_lower, re.IGNORECASE)
                for p in independent_markers
            )
            if not has_independent:
                signals.append(
                    f'Офіційне зацікавлене джерело без незалежного підтвердження'
                )
                score += 0.08

        # ── ПІДСУМОК ──────────────────────────────────────────────────
        score = min(score, 0.80)

        if score >= 0.45:
            verdict = 'COMMERCIAL_ALARMISM'
            explanation = (
                'Текст використовує страх як комерційний або риторичний інструмент. '
                'Загроза описана без конкретного виходу, джерело зацікавлене, '
                'масштаб перебільшений. Архітектура веде до тривоги або покупки.'
            )
            result.is_flagged = True
        elif score >= 0.25:
            verdict = 'ALARMIST_FRAMING'
            explanation = (
                'Текст має алармістські ознаки: перебільшення загрози, '
                'відсутність конкретних дій або зацікавлене джерело. '
                'Фактаж може бути реальним, але подача створює надмірну тривогу.'
            )
            result.is_flagged = True
        else:
            verdict = 'CLEAN'
            explanation = ''

        result.score = round(score, 3)
        result.verdict = verdict
        result.signals = signals
        result.explanation = explanation
        return result


# ── Smoke tests ──────────────────────────────────────────────────────

if __name__ == '__main__':
    det = AlarmismDetector()

    tests = {
        'Independent KadNap': (
            "Criminals hijack thousands of devices to create never-before-seen cyber weapon. "
            "Criminals have secretly hijacked more than 14,000 devices worldwide in order to carry out "
            "attacks that are almost impossible to protect against, security researchers have warned. "
            "Details of the KadNap botnet were shared by the cybersecurity firm Lumen in a new report. "
            "Its decentralised design means there is no central server that could be easily shut down, "
            "making the KadNap botnet incredibly resilient to attempts to dismantle it. "
            "Award-winning security software you can trust. Always. Get All-in-One Protection. LEARN MORE "
            "ADVERTISEMENT Award-winning security software you can trust. LEARN MORE ADVERTISEMENT "
            "Every IP address associated with this botnet represents a significant, persistent risk."
        ),
        'Чистий Reuters кібер': (
            "A new malware strain has been identified by multiple independent security researchers. "
            "According to CISA and Europol, the botnet affects approximately 14,000 routers globally. "
            "Users can protect themselves by updating router firmware — Asus has released patch 3.0.0.4.388. "
            "The FBI recommends rebooting affected devices and enabling automatic updates. "
            "Several cybersecurity firms including Lumen and CrowdStrike confirmed the findings independently."
        ),
        'Фармацевтичний алармізм': (
            "Мільйони людей під загрозою невідомої хвороби. "
            "Дослідження компанії PharmaCorp виявило безпрецедентну загрозу здоров'ю. "
            "Захиститися від цього практично неможливо без спеціальних препаратів. "
            "Отримайте повний захист вашого організму вже сьогодні. Дізнайтесь більше."
        ),
        'Нейтральна стаття': (
            "Дослідники Київської політехніки опублікували аналіз вразливостей роутерів Asus. "
            "За даними незалежних експертів, проблема стосується близько 14 тисяч пристроїв. "
            "Для захисту достатньо оновити прошивку через офіційний сайт виробника. "
            "Asus вже випустив відповідне оновлення безпеки версії 3.0.0.4.388."
        ),
    }

    print(f'{"Тест":<30} {"Verdict":<24} {"Score":>6}')
    print('─' * 65)
    for name, text in tests.items():
        r = det.analyze(text)
        sigs = ' | '.join(r.signals[:2])[:45] if r.signals else '-'
        print(f'{name:<30} {r.verdict:<24} {r.score:>6.3f}  {sigs}')

