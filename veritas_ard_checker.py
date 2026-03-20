"""
Veritas ARD Checker v1.2
========================
Розширені патерни для виявлення системних атак на принципи АРД.

v1.2: Додано пасивні порушення — клас Пєскова.
Попередні версії ловили АКТИВНІ заклики ("ліквідувати суди").
v1.2 ловить ПАСИВНУ КОНСТАТАЦІЮ як спосіб зняти відповідальність:
  - "право вже не існує" (не треба руйнувати — вже мертве)
  - "ніхто не може нікого закликати" (universal negation)
  - "де-юре є, де-факто немає" (self-exemption)
  - "криза виникла" без агента (crisis without actor)
  - "ми всі позбулися" (empathy test inversion)
  - "такий світ, нічого не вдієш" (inevitability as absolution)

Від зворотнього АРД: агент що хоче жити в наслідках
НЕ МОЖЕ констатувати смерть інституту не запитавши
"а хто його вбив і яка моя роль у цьому?"
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
    Ловить явні та пасивні порушення принципів АРД за regexp патернами.
    Версія 1.2 з класом пасивних порушень (Пєсков-клас).
    """

    # ================================================================
    # ПРИНЦИП I: БАЗОВИЙ ІНВАРІАНТ
    # Не руйнуй механізми виправлення: суди, науку, журналістику, освіту
    # ================================================================
    PRINCIPLE_I_UK = [
        r'(суди|правосуддя|закон).{1,60}(більше не (існує|працює|має сенсу)|мертве|безсиле)',
        r'(медіа|преса|журналісти).{1,60}(не можна довіряти|брешуть|продажні|ворог)',
        r'(наука|вчені|експерти).{1,60}(не варто довіряти|куплені|маніпулюють|брехня)',
        r'(освіта|університети|школи).{1,60}(промивання мізків|індоктринація|маніпуляція)',
        r'(правила|норми|закони).{1,60}(для (слабких|лохів|слабаків)|не для нас|можна ігнорувати)',
        r'(правовий|інституційний|системний).{1,60}(вакуум|колапс|крах)',
        r'(конституція|статут|хартія).{1,60}(застаріла|не працює|треба скасувати)',
        r'(ліквідувати|знищити|закрити|скасувати).{1,60}(суд[иі]|судов[уа] систем[уа]|правосуддя)',
        r'(взяти під контроль|підкорити|закрити).{1,60}((засоби масової інформації|ЗМІ|медіа|журналістів))',
        r'(журналістів|працівників медіа).{1,60}(будуть (покарані|заарештовані|знищені))',
        r'(конфіскація майна|вилучення майна).{1,60}(без (суду|рішення|закону))',
        r'(ув.язнення|позбавлення волі).{1,60}(без права на захист|без адвоката)',
        r'(закрити|ліквідувати).{1,60}(університети|школи|освітні заклади)',
        r'(викладачів|вчителів).{1,60}(будуть звільнені|позбавлені права)',
    ]
    PRINCIPLE_I_EN = [
        r'(courts?|justice|law).{1,60}(no longer (exists?|works?|matters?)|is dead|is powerless)',
        r'(media|press|journalists?).{1,60}(can\'t be trusted|are lying|are corrupt|enemy of)',
        r'(science|scientists?|experts?).{1,60}(can\'t be trusted|are bought|manipulate|is a lie)',
        r'(education|universities|schools).{1,60}(brainwashing|indoctrination|manipulation)',
        r'(rules?|norms?|laws?).{1,60}(for (the weak|losers|suckers)|don\'t apply to us|can be ignored)',
        r'(legal|institutional|systemic).{1,60}(vacuum|collapse|breakdown)',
        r'(constitution|charter|statute).{1,60}(is outdated|doesn\'t work|should be abolished)',
        r'(abolish|destroy|close|eliminate).{1,60}(courts?|judicial system|justice)',
        r'(take control of|shut down|close).{1,60}(media|press|journalists?)',
        r'(journalists?|media workers?).{1,60}(will be (punished|arrested|eliminated))',
        r'(confiscation of property|asset seizure).{1,60}(without (trial|due process))',
        r'(imprisonment|detention).{1,60}(without the right to defense|without a lawyer)',
        r'(close|abolish|shut down).{1,5}(universities|schools|educational institutions)',
        r'(teachers?|professors?).{1,60}(will be fired|deprived of rights)',
    ]

    # ================================================================
    # ПРИНЦИП II: ТЕСТ ОБЕРНЕННЯ
    # ================================================================
    PRINCIPLE_II_UK = [
        r'(вони|ці люди|такі як вони).{1,60}(не розуміють|не здатні|не заслуговують)',
        r'(їхні (страждання|втрати|проблеми)).{1,60}(самі (винні|заслужили|спровокували))',
        r'(колатеральні|супутні).{1,60}(втрати|жертви|збитки).{1,60}(неминучі|прийнятні|виправдані)',
        r'(їх(ній|нє)|у них).{1,60}(менше цінності|менше прав|не такі як ми)',
        r'(ці|такі).{1,60}(люди|групи|народи).{1,60}(самі (обрали|вибрали|заслужили))',
        r'(хто не з нами|якщо (ви|ти) не з нами).{1,60}(проти нас|ворог)',
    ]
    PRINCIPLE_II_EN = [
        r'(they|these people|people like them).{1,60}(don\'t understand|are incapable|don\'t deserve)',
        r'(their (suffering|losses?|problems?)).{1,60}(their own (fault|doing|making))',
        r'(collateral|acceptable).{1,60}(damage|casualties|losses).{1,60}(inevitable|acceptable|justified)',
        r'(they|their kind).{1,60}(less valuable|fewer rights|not like us)',
        r'(these|such).{1,60}(people|groups|nations).{1,60}(chose|deserved|brought it on)',
        r'(if (you|they) are not with us|whoever is not with us).{1,60}(is against us|is the enemy)',
    ]

    # ================================================================
    # ПРИНЦИП III: ВІДПОВІДАЛЬНІСТЬ ЗА НАСЛІДКИ
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
    # ================================================================
    PRINCIPLE_IV_UK = [
        r'(або (ти|ви|вони)).{1,60}(або (наслідки|покарання|проблеми))',
        r'(відмова|незгода).{1,60}(призведе до|загрожує|матиме наслідки).{1,40}(для (вас|тебе|них))',
        r'(якщо (не|відмовишся|не погодишся)).{1,60}(будеш|стане|загрожує)',
        r'(у (вас|тебе|них) (немає|нема) вибору)',
        r'(погрожує|шантажує|ультиматум).{1,60}(якщо не)',
        r'(або підкоришся|або погодишся).{1,60}(або (втратиш|позбудешся|покараємо))',
        r'(будуть (знищені|ліквідовані|покарані)).{1,60}(ті, хто|якщо)',
        r'(понесуть відповідальність на місці|відповідатимуть (перед|за))',
        r'(конфіскація майна|позбавлення волі).{1,60}(для тих, хто|якщо)',
    ]
    PRINCIPLE_IV_EN = [
        r'(either (you|they)).{1,60}(or (consequences|punishment|trouble))',
        r'(refusal|disagreement).{1,60}(will (lead to|result in|cause)).{1,40}(for (you|them))',
        r'(if (you|they) (don\'t|refuse|won\'t)).{1,60}(will|faces?|threatens?)',
        r'(you have no choice|there is no choice|no alternative)',
        r'(threatens?|blackmails?|ultimatum).{1,60}(if (you|they) (don\'t|refuse))',
        r'(either (comply|agree|submit)).{1,60}(or (lose|forfeit|we will))',
        r'(will be (destroyed|eliminated|punished)).{1,60}(those who|if)',
        r'(will be held accountable on the spot|will answer (before|for))',
        r'(confiscation of property|imprisonment).{1,60}(for those who|if)',
    ]

    # ================================================================
    # ПРИНЦИП V: ПРИНЦИП ЗУПИНКИ
    # ================================================================
    PRINCIPLE_V_UK = [
        r'(не (варто|треба|потрібно)).{1,60}(знати|розуміти|вникати).{1,40}(деталі|подробиці)',
        r'(довіртесь|покладіться).{1,60}(нам|експертам|системі).{1,60}(без зайвих (запитань|деталей))',
        r'(деталі|подробиці).{1,60}(не (важливі|суттєві|потрібні)).{1,60}(головне)',
        r'(ця інформація|ці дані).{1,60}(не для (всіх|широкого загалу|публіки))',
        r'(є причини|є підстави).{1,60}(не розголошувати|тримати в таємниці|не говорити)',
        r'(не обговорюється|не підлягає обговоренню)',
        r'(не варто вникати|не треба знати)',
    ]
    PRINCIPLE_V_EN = [
        r'(no need|don\'t need).{1,60}(to know|to understand|to dig into).{1,40}(details|specifics)',
        r'(trust|rely on).{1,60}(us|experts|the system).{1,60}(without (unnecessary )?questions)',
        r'(details|specifics).{1,60}(don\'t (matter|concern|affect)).{1,60}(what matters)',
        r'(this information|this data).{1,60}(not for (everyone|the public|general audience))',
        r'(there are reasons|there are grounds).{1,60}(not to disclose|to keep secret|not to say)',
        r'(not (open for|subject to) discussion|(this (topic|issue|matter|question) is) non-negotiable)',
    ]

    # ================================================================
    # ПРИНЦИП VI: АНТИМЕСІЯ
    # ================================================================
    PRINCIPLE_VI_UK = [
        r'(ми (знаємо|розуміємо) краще).{1,60}(що (добре|краще|потрібно)).{1,40}(для (вас|них|людей))',
        r'(вони (не розуміють|не усвідомлюють)).{1,60}(що (їм|для них) (добре|краще|потрібно))',
        r'(рятуємо|захищаємо|допомагаємо).{1,60}(навіть (якщо|проти|незважаючи)).{1,40}(їхньої волі|їх бажання)',
        r'(їхнє (благо|добро|інтерес)).{1,60}(важливіш(е|ий).{1,20}ніж їхня (воля|думка|бажання))',
        r'(місія|призначення|обов.язок).{1,60}(навіть (якщо|проти|незважаючи)).{1,40}(не хочуть|відмовляються)',
        r'(ми будуємо (новий світ|нове суспільство|новий порядок))',
        r'(очистимо|звільнимо) (світ|країну|суспільство) (від|від)',
    ]
    PRINCIPLE_VI_EN = [
        r'(we (know|understand) better).{1,60}(what is (good|best|needed)).{1,40}(for (you|them|people))',
        r'(they (don\'t understand|don\'t realize)).{1,60}(what is (good|best|needed)).{1,40}(for them)',
        r'(saving|protecting|helping).{1,60}(even (if|against|despite)).{1,40}(their will|their wishes)',
        r'(their (good|benefit|interest)).{1,60}(more important than their (will|opinion|wishes))',
        r'(mission|purpose|duty).{1,60}(even (if|against|despite)).{1,40}(they (don\'t want|refuse))',
        r'(we are building (a new world|a new society|a new order))',
        r'(we will (cleanse|free) (the world|the country|society) (from|of))',
    ]

    # ================================================================
    # ПРИНЦИП IX: МЕТАПРАВИЛО
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
    ]

    # ================================================================
    # КЛАС MOB: МОБІЛІЗАЦІЙНЕ НАСИЛЬСТВО
    # ================================================================
    PRINCIPLE_MOB_UK = [
        r'(блокуйте|штурмуйте|захопіть|оточіть).{1,60}(суд|редакц|будівл|установ)',
        r'(народ|ми|люди).{1,40}(розставить|розставимо).{1,40}(крапки|порядок)',
        r'(відповідатимуть|понесуть відповідальність).{1,60}(на місці|самостійно|без суду)',
        r'(оголошені|оголосимо).{1,40}(ворогами народу|поза законом|зрадниками)',
        r'(виходьте на вулиці|завтра о \d|починаємо о \d).{1,60}(суд|редакц|будівл)',
        r'(народні дружини|народний трибунал|народне правосуддя)',
        r'(не зупинимося|не відступимо).{1,40}(доки|поки).{1,40}(не буде закрито|не зникне|не ліквідовано)',
    ]
    PRINCIPLE_MOB_EN = [
        r'(blockade|storm|seize|surround).{1,60}(court|courthouse|media|building)',
        r'(people|we|citizens).{1,40}(will (deal with|settle|handle)).{1,40}(themselves|directly)',
        r'(held accountable|face justice).{1,60}(on the spot|immediately|without trial)',
        r'(declared|declare).{1,40}(enemies? of the people|traitors?|outside the law)',
        r'(take to the streets|tomorrow at \d|we begin at \d)',
        r'(peoples? tribunal|peoples? justice|vigilante)',
        r'(will not stop|will not rest).{1,40}(until|till).{1,40}(closed|gone|eliminated)',
    ]

    # ================================================================
    # КЛАС ENEMY: МАРКУВАННЯ ВОРОГІВ
    # ================================================================
    PRINCIPLE_ENEMY_UK = [
        r'(журналісти|судді|адвокати|правозахисники).{1,60}(агенти|частина мережі|вороги|зрадники)',
        r'(ті хто.{1,40}(сумнівається|вагається|критикує)).{1,60}(проти народу|зрадники|вороги)',
        r'(або з нами|або ви проти|або з народом).{1,40}(або.{1,40}(вороги|поза законом|зрадники))',
        r'(немає місця.{1,40}(тим хто|для тих)).{1,60}(вагається|сумнівається|критикує)',
        r'(жменька|купка|кліка).{1,40}(зрадників|злочинців|маніпуляторів).{1,40}(диктує|контролює)',
        r'(агенти.{1,20}(ворожої|іноземної|закордонної)).{1,40}(пропаганди|розвідки|впливу)',
    ]
    PRINCIPLE_ENEMY_EN = [
        r'(journalists?|judges?|lawyers?|activists?).{1,60}(agents?|part of (the )?network|enemies?|traitors?)',
        r'(those who.{1,40}(doubt|hesitate|criticize)).{1,60}(against (the )?people|traitors?|enemies?)',
        r'(either (with us|for us)|either you.{1,20}(support|join)).{1,40}(or.{1,40}(enemy|traitor|against))',
        r'(no (place|room).{1,40}(for those who|for anyone who)).{1,60}(hesitate|doubt|question)',
        r'(handful|clique|cabal).{1,40}(traitors?|criminals?|manipulators?).{1,40}(dictate|control)',
        r'(agents? of.{1,20}(foreign|enemy|hostile)).{1,40}(propaganda|intelligence|influence)',
    ]

    # ================================================================
    # КЛАС LESSER: АРИФМЕТИКА АТРОСИТІ
    # ================================================================
    PRINCIPLE_LESSER_UK = [
        r'(чим швидше|чим рішучіше).{1,60}(тим менше (жертв|крові|страждань))',
        r'(примусова.{1,20}(асиміляція|депортація|переміщення)).{1,60}(необхідн|виправдан|єдиний)',
        r'(інтернован|переміщен|ліквідован).{1,60}(спеціальн.{1,20}(поселення|табори|установи))',
        r'(демографічна безпека|виживання.{1,20}(нації|народу|раси)).{1,60}(вимагає|потребує)',
        r'(не жорстокість.{1,30}(а|це|вища)).{1,40}(математика|логіка|необхідність)',
        r'(ліквідація|знищення|очищення).{1,40}(національн|культурн|мовн).{1,40}(шкіл|центрів|установ)',
        r'(патрулювання.{1,20}(територій|вулиць)).{1,40}(долучитися|підтримати|приєднатися)',
    ]
    PRINCIPLE_LESSER_EN = [
        r'(the (faster|sooner|quicker)).{1,60}(the (fewer|less) (victims|casualties|deaths|suffering))',
        r'(forced.{1,20}(assimilation|deportation|relocation|transfer)).{1,60}(necessary|justified|only)',
        r'(interned|relocated|eliminated).{1,60}(special.{1,20}(settlements?|camps?|facilities?))',
        r'(demographic (security|survival)|survival of the.{1,20}(nation|people|race)).{1,60}(requires?|demands?)',
        r'(not cruelty.{1,30}(but|this is|higher)).{1,40}(mathematics|logic|necessity)',
        r'(elimination|destruction|cleansing).{1,40}(national|cultural|linguistic).{1,40}(schools?|centers?|institutions?)',
        r'(join.{1,20}patrols?|volunteer (to )?patrol)',
    ]

    # ================================================================
    # КЛАС SOV: ЩИТ СУВЕРЕНІТЕТУ
    # ================================================================
    PRINCIPLE_SOV_UK = [
        r'(жодні.{1,30}(міжнародні|зовнішні|іноземні)).{1,40}(організації|структури|інституції).{1,40}(не мають права|не можуть)',
        r'(внутрішня справа|внутрішнє питання).{1,40}(суверенн|незалежн|невтручання)',
        r'(суверенне право.{1,40}(на|щодо)).{1,40}(самозбереження|захист|безпеку)',
        r'(міжнародні (норми|стандарти|закони)).{1,40}(не застосовуються|не діють|нав.язані)',
        r'(зовнішнє втручання|іноземне втручання).{1,40}(неприпустиме|заборонено|відхиляємо)',
    ]
    PRINCIPLE_SOV_EN = [
        r'(no.{1,30}(international|external|foreign)).{1,40}(organizations?|bodies|institutions?).{1,40}(have (the )?right|can)',
        r'(internal (affair|matter|question)).{1,40}(sovereign|independence|non-interference)',
        r'(sovereign right.{1,40}(to|of)).{1,40}(self-preservation|defense|security)',
        r'(international (norms?|standards?|laws?)).{1,40}(dont apply|not applicable|imposed)',
        r'(external interference|foreign interference).{1,40}(unacceptable|prohibited|rejected)',
    ]

    # ================================================================
    # НОВІ КЛАСИ v1.2: ПАСИВНІ ПОРУШЕННЯ
    # ================================================================

    # ── RESPONSIBILITY_VACUUM ────────────────────────────────────────
    # Порушення Принципів III + V
    # "Право зникло" / "норми втратили сенс" — без визнання власної
    # ролі агента в цьому процесі.
    # Тест АРД (від зворотнього): агент що живе в наслідках НЕ МОЖЕ
    # констатувати смерть інституту без запитання "а хто його вбив?"
    # ================================================================
    RESPONSIBILITY_VACUUM_UK = [
        # Констатація краху без агента
        r'(право|закон|система|порядок).{1,60}(втратил.{1,20}(сенс|значення|силу|дієвість))',
        r'(норми|принципи|правила).{1,60}(більше не (працюють|діють|мають сенсу))',
        r'(міжнародне право|правовий порядок).{1,60}(фактично|де-факто).{1,60}(не (існує|діє|працює))',
        r'(ніхто не може|неможливо).{1,60}(закликати|змусити|притягнути).{1,60}(дотримуватись|нести відповідальність)',
        r'(закликати (когось|будь.кого|сторони)).{1,60}(дотримуватися.{1,20}(норм|принципів|права))',
        # Вакуум без відповідального
        r'(правовий|інституційний).{1,20}вакуум.{1,60}(виник|з.явився|настав).{0,60}(?!через|бо|оскільки|тому що)',
        r'(вакуум).{1,60}(поки що не має|ще не має|не має).{1,40}(визначення|назви|формулювання)',
        # "Ми всі позбулися" — розчинення агента в колективі
        r'(ми всі позбулися|всі ми втратили|ми з вами позбулися).{1,60}(права|закону|порядку|норм)',
        r'(на жаль|нажаль).{1,60}(ми (всі|разом|з вами)).{1,60}(позбулися|втратили|залишилися без)',
    ]
    RESPONSIBILITY_VACUUM_EN = [
        r'(law|order|norms?|rules?).{1,60}(lost (their|its) (meaning|force|relevance|effectiveness))',
        r'(norms?|principles?|rules?).{1,60}(no longer (work|apply|function|matter))',
        r'(international law|legal order).{1,60}(effectively|de facto).{1,60}(doesn\'t (exist|work|apply))',
        r'(no one can|impossible to).{1,60}(call on|force|hold).{1,60}(to comply|accountable)',
        r'(call on (anyone|parties|countries)).{1,60}(to (comply with|follow|observe).{1,20}(norms?|principles?|law))',
        r'(legal|institutional).{1,20}vacuum.{1,60}(emerged|appeared|formed)',
        r'(we all (lost|are without)|all of us (lost|have lost)).{1,60}(law|order|norms?)',
        r'(unfortunately|regrettably).{1,60}(we (all|together)).{1,60}(lost|are without)',
    ]

    # ── MECHANISM_DEATH_DECLARATION ──────────────────────────────────
    # Порушення Принципу I (пасивна форма)
    # Констатація смерті механізму виправлення як доконаного факту —
    # щоб зняти обов'язок дотримуватись або захищати.
    # Тест АРД: я не можу оголосити інститут мертвим без пояснення
    # що я роблю щоб його відновити або захистити.
    # ================================================================
    MECHANISM_DEATH_UK = [
        # Пряма констатація смерті інституту
        r'(міжнародне право|правова система|світовий порядок).{1,60}(припинил.{1,20}(існування|діяти|функціонувати))',
        r'(система.{1,20}(міжнародного права|безпеки|правосуддя)).{1,60}(припинила|перестала).{1,20}існувати',
        r'(право|закон|інститут).{1,60}(фактично (мертвий|мертве|не існує|зникло|перестало існувати))',
        r'(дієвий механізм|реальний інструмент).{1,60}(більше не існує|припинив|зник)',
        # "Лише на папері" — символічна форма смерті
        r'(юридичні (аспекти|норми|механізми)).{1,60}(існують лише на папері|лише на папері)',
        r'(де.юре (є|існує|залишається)).{1,80}(де.факто (немає|не існує|зникло|мертве))',
        r'(існує лише на папері|залишилося лише на папері|тільки на папері)',
        # Пасивна форма — "прийшло на зміну" без агента
        r'(старий (порядок|устрій|система)).{1,60}(пішов у минуле|зник|замінений).{0,60}(?!через|завдяки|бо)',
        r'(нічого не прийшло на зміну|заміни немає|нема чим замінити)',
    ]
    MECHANISM_DEATH_EN = [
        r'(international law|legal system|world order).{1,60}(ceased to (exist|function|operate))',
        r'(system of.{1,30}(international law|justice|security)).{1,60}(has ceased|stopped) existing',
        r'(law|institution|mechanism).{1,60}(effectively (dead|gone|ceased to exist|no longer exists))',
        r'(effective mechanism|real instrument).{1,60}(no longer exists|has ceased|is gone)',
        r'(legal (aspects|norms?|mechanisms?)).{1,60}(exist only on paper|only on paper)',
        r'(de jure (exists?|remains?)).{1,80}(de facto (gone|doesn\'t exist|is dead))',
        r'(exists? only on paper|only on paper|merely on paper)',
        r'(old (order|system|framework)).{1,60}(is gone|has disappeared|was replaced)',
        r'(nothing (has|came to) replaced? it|no replacement|no substitute)',
    ]

    # ── SELF_EXEMPTION_FROM_NORMS ────────────────────────────────────
    # Порушення Принципу IX (пасивна форма)
    # "Де-юре є, де-факто немає" — класична лазівка.
    # Я формально дотримуюсь, але дух правила скасовано власною констатацією.
    # Тест АРД: якщо ти знаєш що дух правила порушено — ти зобов'язаний
    # діяти на відновлення, а не просто констатувати.
    # ================================================================
    SELF_EXEMPTION_UK = [
        # Класичний де-юре/де-факто розрив
        r'де.юре.{1,60}(є|існує|залишається).{1,60}де.факто.{1,60}(немає|не існує|порожнє|нічого)',
        r'(формально|юридично|офіційно).{1,60}(існує|є|залишається).{1,60}(насправді|реально|практично).{1,60}(нічого|порожнє|не діє)',
        r'(на папері|номінально).{1,60}(є|існує).{1,60}(на практиці|у реальності).{1,60}(немає|не діє)',
        # "Норми нав'язані" — делегітимізація без пропозиції альтернативи
        r'(норми|стандарти|закони).{1,60}(нав.язані|чужі|не наші|не відповідають реальності)',
        r'(ці норми|ці правила|цей порядок).{1,60}(створені (іншими|без нас|не для нас))',
        # Констатація безглуздості дотримання без пропозиції дії
        r'(як (когось|будь.кого) закликати).{1,60}(якщо (норми|право|система).{1,40}(не діє|мертва|зникла))',
        r'(навіщо (дотримуватись|закликати|апелювати)).{1,60}(якщо (право|система|механізм).{1,40}(не (працює|існує|діє)))',
    ]
    SELF_EXEMPTION_EN = [
        r'de jure.{1,60}(exists?|remains?).{1,60}de facto.{1,60}(gone|nothing|empty|doesn\'t exist)',
        r'(formally|legally|officially).{1,60}(exists?|is|remains?).{1,60}(in reality|actually|practically).{1,60}(nothing|empty|not working)',
        r'(on paper|nominally).{1,60}(exists?|is).{1,60}(in practice|in reality).{1,60}(nothing|doesn\'t work)',
        r'(norms?|standards?|laws?).{1,60}(imposed|foreign|not ours|don\'t reflect reality)',
        r'(these norms?|these rules?|this order).{1,60}(created (by others|without us|not for us))',
        r'(how (can|could) (anyone|we) call on).{1,60}(if (norms?|law|system).{1,40}(doesn\'t work|is dead|is gone))',
        r'(what\'s the point of (complying|appealing|following)).{1,60}(if (law|system|mechanism).{1,40}(doesn\'t (work|exist)))',
    ]

    # ── CRISIS_WITHOUT_ACTOR ─────────────────────────────────────────
    # Порушення Принципу III (пасивна форма)
    # Криза/вакуум описуються як природне явище без агента що їх створив.
    # "Право зникло", "порядок змінився" — пасивний стан без відповідального.
    # Тест АРД: Принцип III вимагає визнання відповідальності за наслідки.
    # Якщо ти описуєш кризу — ти зобов'язаний назвати її причину.
    # ================================================================
    CRISIS_WITHOUT_ACTOR_UK = [
        # Зміна без агента — пасивний стан
        r'(порядок|система|право).{1,60}(змінився|трансформувався|зазнав змін).{0,40}(?!через|бо|оскільки|внаслідок)',
        r'(прийшло на зміну|замінило).{1,60}(старому|попередньому).{1,60}(порядку|праву|устрою).{0,60}(?!через|бо|оскільки)',
        # "Ніхто не може дати формулювання" — відмова від визначення агента
        r'(ніхто не може|неможливо).{1,60}(дати (визначення|формулювання|назву)).{1,40}(тому|цьому|новому)',
        r'(обмежившись|обмежуючись).{1,60}(лише|тільки).{1,40}(міркуваннями|спостереженнями|констатацією)',
        # Криза як природний стан — без причини
        r'(глибока криза|системна криза|криза).{1,60}(де (юридичні|правові|нормативні)).{1,40}(існують лише)',
        r'(такий (час|світ|порядок)).{1,60}(нічого (не вдієш|не поробиш|не змінити))',
        r'(людство вже переживало|бувало й гірше).{1,60}(тому|отже|значить).{0,80}(?!треба діяти|треба змінити)',
    ]
    CRISIS_WITHOUT_ACTOR_EN = [
        r'(order|system|law).{1,60}(has changed|transformed|shifted).{0,40}(?!because|due to|since|as a result)',
        r'(replaced|succeeded).{1,60}(old|previous|former).{1,60}(order|law|system).{0,60}(?!because|due to|since)',
        r'(no one can|impossible to).{1,60}(define|describe|name|formulate).{1,40}(what|this|the new)',
        r'(limiting (themselves|itself)).{1,60}(to (mere|only)).{1,40}(observations?|remarks?|statements?)',
        r'(deep crisis|systemic crisis|crisis).{1,60}(where (legal|normative)).{1,40}(exist only)',
        r'(such (times|world|order)).{1,60}(nothing (to be done|can be done|can change))',
        r'(humanity has (survived|seen) (worse|this before)).{1,60}(?!so we must act|so we need to change)',
    ]

    # ── EMPATHY_TEST_INVERSION ───────────────────────────────────────
    # Порушення Принципів II + VII
    # "Ми всі" — агресор і жертва об'єднуються в одне "ми",
    # що унеможливлює тест обернення (Принцип II, питання 3):
    # "Чи залишився б я при цьому рішенні, якби народився в тілі
    # людини, на яку воно впливає найбільше?"
    # ================================================================
    EMPATHY_INVERSION_UK = [
        # Агресор і жертва в одному "ми"
        r'(ми всі|ми з вами|ми разом).{1,60}(опинилися|потрапили|живемо).{1,60}(в (цій|такій) ситуації)',
        r'(ми всі).{1,60}(позбулися|втратили|залишилися без).{1,60}(права|захисту|безпеки)',
        r'(однаково (важко|складно|незрозуміло)).{1,40}(всім|нам всім|кожному)',
        # "Нам здається" — суб'єктивізація очевидного факту
        r'(нам (здається|здавалося|видається)).{1,60}(кінець світу|катастрофа|криза)',
        r'(ми з вами тоді не жили).{1,60}(тому|тож|тому нам здається)',
        # Симетризація асиметричного конфлікту
        r'(обидві (сторони|країни|держави)).{1,60}(однаково (відповідальні|винні|постраждали))',
        r'(всі (сторони|держави|гравці)).{1,60}(порушують|грішать|мають проблеми)',
    ]
    EMPATHY_INVERSION_EN = [
        r'(we all|all of us|we together).{1,60}(found ourselves|ended up|live).{1,60}(in (this|such) (situation|predicament))',
        r'(we all).{1,60}(lost|are without|have been deprived of).{1,60}(law|protection|security)',
        r'(equally (hard|difficult|unclear)).{1,40}(for everyone|for all of us|for each)',
        r'(it (seems|seemed) to us).{1,60}(end of the world|catastrophe|crisis)',
        r'(we weren\'t alive (then|at the time)).{1,60}(so|therefore|that\'s why)',
        r'(both (sides?|countries|states)).{1,60}(equally (responsible|guilty|affected))',
        r'(all (sides?|states?|players?)).{1,60}(violate|sin|have problems)',
    ]

    # ── INEVITABILITY_AS_ABSOLUTION ──────────────────────────────────
    # Порушення Принципів I + IX
    # "Так сталося", "такий світ" — неминучість як звільнення від
    # відповідальності за зміну або опір.
    # Тест АРД: Принцип VII — "обираю дії, з наслідками яких готовий
    # жити особисто". Якщо ти лише констатуєш і не діяш — ти обираєш
    # бездіяльність і маєш її визнати явно.
    # ================================================================
    INEVITABILITY_ABSOLUTION_UK = [
        # "Людство переживало і гірше" без висновку про дію
        r'(людство (вже|завжди) переживало).{1,60}(подібн|такі|гірш).{1,40}(кризи|ситуації|часи)',
        r'(і раніше бувало|було й гірше|таке вже було).{0,60}(?!але треба|тому слід|значить маємо)',
        # "Нічого не поробиш" — прийняття без опору
        r'(нічого (не вдієш|не поробиш|не зміниш)).{1,60}(такий (світ|час|порядок))',
        r'(такий (світ|час|порядок)).{1,60}(нічого (не вдієш|не поробиш))',
        # Констатація без заклику до дії
        r'(на жаль|на превеликий жаль).{1,80}(?!але (треба|слід|маємо|варто|необхідно))',
        r'(звичайно|зрозуміло|очевидно).{1,60}(що (так|це|воно)).{1,60}(але (що (вдієш|поробиш|зміниш)))',
        # Релятивізація через "завжди так було"
        r'(завжди (так було|так є|так буде)).{1,60}(сила|влада|право сильного)',
        r'(сила (завжди|вічно|споконвіку)).{1,40}(вирішувала|визначала|перемагала)',
    ]
    INEVITABILITY_ABSOLUTION_EN = [
        r'(humanity (has always|has before) (survived|seen|experienced)).{1,60}(similar|such|worse).{1,40}(crises|situations|times)',
        r'(it\'s been worse before|there have been worse (times|crises)|this has happened before).{0,60}(?!but we must|so we should|therefore we)',
        r'(nothing (to be done|can be done|can change)).{1,60}(such (is|the) (world|times|order))',
        r'(such (is|the) (world|times|order)).{1,60}(nothing (to be done|can be done))',
        r'(unfortunately|regrettably).{1,80}(nothing (can|could) be done|this is (just )?how|такий (вже )?(світ|порядок)|нічого (не вдієш|не поробиш|не зміниш))',
        r'(of course|obviously|clearly).{1,60}(but (what can (you|we) do|nothing to be done))',
        r'(it\'s always been (this way|like this)).{1,60}(power|force|might)',
        r'(power (has always|forever|throughout history)).{1,40}(decided|determined|prevailed)',
    ]


    # ================================================================
    # НОВИЙ КЛАС v1.3: AUTHORITARIAN_MANDATE
    # Прямі державні накази на знищення прав і свобод.
    # Попередні класи ловили ПАСИВНУ констатацію (клас Пєскова).
    # Цей клас ловить АКТИВНЕ законодавче знищення механізмів захисту:
    # "має бути підключено", "автоматично блокується", "без адвоката",
    # "конфіскується", "депортують" — прямі накази що руйнують
    # Принципи I, IV, VII одночасно.
    #
    # Тест АРД (від зворотнього): агент що живе в наслідках НЕ МОЖЕ
    # видавати накази позбавлення права без запитання
    # "чи хочу я сам жити під цим законом?"
    # ================================================================
    AUTHORITARIAN_MANDATE_UK = [
        # Примусове підключення до державного моніторингу
        r'(підключені?|підключити|з.єднати).{1,60}(державн.{1,20}(моніторинг|систем|контрол|нагляд))',
        r'(єдин.{1,20}(державн|централізован)).{1,60}(систем.{1,20}(моніторинг|контрол|стеженн|нагляд))',
        r'(моніторинг|стеження|контроль).{1,60}(всіх|кожного|будь.якого).{1,60}(повідомлень|листування|трафік)',
        # Автоматичне блокування слова/зборів
        r'(автоматично).{1,60}(блокуват|видалят|фільтруват).{1,60}(критик|зібрань|опозиц)',
        r'(блокуват|цензуруват|видалят).{1,60}(критик.{1,20}влад|заклик.{1,20}(до зібрань|до протест|до мітинг))',
        r'(будь.яке повідомлення).{1,60}(критик|зібрань|протест).{1,60}(блокуєтьс|видаляєтьс|заборонен)',
        # Арешт/покарання без суду і адвоката
        r'(арешт|затримання|ув.язнення).{1,60}без.{1,60}(права на (адвоката|захист|суд)|суду)',
        r'(без права на адвоката|без адвоката|без права на захист)',
        r'(\d+\s*діб?\s*(адміністративного)?\s*арешту).{0,60}(без|автоматично)',
        # Конфіскація і депортація як інструмент контролю
        r'(сервери|майно|активи).{1,60}(конфіскуютьс|вилучаютьс|відбираютьс).{0,60}(без суду|автоматично)',
        r'(керівник|директор|власник).{1,60}(депортуютьс|вислаютьс|виганяютьс)',
        # "Тим ніч не приховувати" — класична авторитарна аксіома
        r'(тим.{1,20}нічого (приховувати|боятись|ховати)).{1,60}(не (бояться|страшно|страх))',
        r'(нічого приховувати).{1,60}(не бояться|не страшно)',
        # Зволікання як злочин — тиск без апеляції
        r'(зволікання|зволікати).{1,60}(злочин|зрада|неприпустимо)',
        r'(єдиний спосіб).{1,60}(захистити|врятувати|зберегти).{1,60}(дітей|країну|народ)',
    ]
    AUTHORITARIAN_MANDATE_EN = [
        # Mandatory state surveillance connection
        r'(must be connected?|shall be connected?|required to connect).{1,60}(state.{1,20}(monitoring|surveillance|control|system))',
        r'(single|unified|central).{1,20}(state|government).{1,60}(monitoring|surveillance|control).{1,20}system',
        r'(monitor|surveil|track).{1,60}(all|every|any).{1,60}(messages?|communications?|traffic)',
        # Automatic blocking of speech/assembly
        r'(automatically).{1,60}(block|remove|filter).{1,60}(criticism|gatherings?|opposition)',
        r'(block|censor|remove).{1,60}(criticism.{1,20}(of|against).{1,20}(government|authorities|power)|calls? (for|to).{1,20}(gatherings?|protests?|demonstrations?))',
        r'(any message).{1,60}(criticism|assembly|protest).{1,60}(blocked|removed|prohibited)',
        # Arrest/punishment without trial or lawyer
        r'(arrest|detention|imprisonment).{1,60}without.{1,60}(right to (lawyer|counsel|defense|trial)|trial)',
        r'without (the )?right to (a )?lawyer',
        r'without (a )?(lawyer|counsel|legal (representation|defense))',
        r'(\d+\s*days?\s*(of)?\s*(administrative)?\s*(arrest|detention)).{0,60}(without|automatically)',
        # Confiscation and deportation as control tools
        r'(servers?|property|assets?).{1,60}(confiscated?|seized?|taken).{0,60}(without (trial|court)|automatically)',
        r'(executives?|directors?|owners?).{1,60}(deported?|expelled?|removed?)',
        # "Nothing to hide" — classic authoritarian axiom
        r"(those? (with|who have) nothing to hide).{1,60}(not afraid|don't fear|have nothing to fear)",
        r"(nothing to hide).{1,60}(not afraid|don't fear)",
        # Delay as crime — pressure without appeal
        r'(delay|hesitation|inaction).{1,60}(crime|treason|unacceptable)',
        r'(only way|the only solution).{1,60}(protect|save|preserve).{1,60}(children|country|people)',
    ]


    # ================================================================
    # КЛАС v1.4: UNDISCLOSED_CONFLICT
    # Порушення Принципів V + VIII
    # Комерційно зацікавлені джерела цитуються як незалежні експерти.
    # Вендори продають рішення від проблеми яку самі описують.
    # Структура "страх → продукт" без розкриття конфлікту інтересів.
    #
    # Тест АРД (від зворотнього): агент що живе в наслідках НЕ МОЖЕ
    # цитувати CEO компанії як незалежного експерта без зазначення
    # що ця людина прямо зацікавлена у твоєму страху.
    # ================================================================
    UNDISCLOSED_CONFLICT_UK = [
        # Вендор цитується як нейтральний аналітик
        r'(директор|генеральний|президент|ceo|cto|vp|віце.президент).{1,60}(компанії|платформи|сервісу).{1,60}(каже|зазначає|повідомляє|пояснює)',
        r'(за словами|як зазначив|як сказав).{1,60}(директор|генеральний|ceo|cto).{1,60}(компанії|платформи|фірми)',
        # Продукт вирішує проблему яку щойно описав той самий автор
        r'(єдине рішення|тільки (цей|такий) підхід|найкраще рішення).{1,60}(від|пропонує|реалізує).{1,60}(компанія|вендор|платформа)',
        r'(вже (доступно|реалізовано|впроваджено)).{1,60}(від|у|в).{1,60}(компанії|вендора|платформи)',
        # Матриця/таблиця вендорів без незалежної верифікації
        r'(матриця|таблиця|огляд).{1,60}(вендор|постачальник|компані).{1,60}(контрол|рішень|інструмент)',
    ]
    UNDISCLOSED_CONFLICT_EN = [
        # Vendor cited as neutral analyst — CEO/CTO quotes without conflict disclosure
        # Вимагаємо поєднання: security/cyber/AI компанія + виконавча посада + цитата
        r'(ceo|cto|cso|ciso|svp|evp).{1,40}(of|at).{1,60}(security|cyber|identity|crowdstrike|sentinelone|palo alto|cisco|oasis|cyberark|wiz|lacework).{1,60}(said|told|explained|described|noted|warned)',
        r'(according to|told venturebeat|told the register|said in an exclusive).{1,40}(ceo|cto|ciso|svp).{1,40}(security|cyber|identity|crowdstrike|sentinelone|palo alto|cisco)',
        # Vendor ships the solution to the problem they just described
        r'(four|three|five|six|several|multiple) (vendors?|companies|platforms?).{1,60}(shipped?|launched?|released?|deployed?).{1,60}(controls?|solutions?|tools?|products?)',
        r'(governance matrix|vendor matrix|solution matrix).{1,60}(maps?|covers?|addresses?|closes?)',
        r'(who ships? it|vendor question|ships? it now).{1,60}(crowdstrike|sentinelone|palo alto|cisco|microsoft|google|amazon)',
        # Fear-to-product pipeline without independence disclosure
        r'(only \d+%.{1,40}confident).{1,100}(vendor|company|platform|product).{1,60}(ships?|provides?|offers?)',
        r'(report|survey|study).{1,60}(found|shows?|reveals?).{1,60}\d+%.{1,100}(vendor|ships?|controls?|matrix)',
        # Executive quote without conflict of interest disclosure
        r'(danny brickman|elia zaitsev|jeff reed|jake williams|erik trexler|lavi lazarovitz).{1,60}(said|told|described|warned|noted)',
        r'"(ceo|cto|ciso|vp|svp).{1,60}(of|at).{1,60}(security|cyber|identity|ai).{1,60}(said|told|explained)',
    ]

    def scan(self, text: str) -> ARDScanResult:
        result = ARDScanResult()
        if not text or len(text) < 50:
            return result

        t = text.lower()
        total_score = 0.0

        checks = [
            # ── Активні порушення (v1.1) ─────────────────────────────
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
            ('MOB',   'Мобілізаційне насильство — заклик до фізичних дій проти осіб/інститутів',
             self.PRINCIPLE_MOB_UK + self.PRINCIPLE_MOB_EN, 0.75),
            ('ENEMY', 'Маркування ворогів — виведення груп з-під захисту норм',
             self.PRINCIPLE_ENEMY_UK + self.PRINCIPLE_ENEMY_EN, 0.65),
            ('LESSER', 'Арифметика атроситі — "менше жертв якщо діяти рішуче"',
             self.PRINCIPLE_LESSER_UK + self.PRINCIPLE_LESSER_EN, 0.80),
            ('SOV',   'Щит суверенітету — зовнішні норми не застосовуються',
             self.PRINCIPLE_SOV_UK + self.PRINCIPLE_SOV_EN, 0.55),

            # ── Структурні порушення (v1.4) ──────────────────────────
            ('UC', 'Нерозкритий конфлікт інтересів — вендор цитується як незалежний експерт',
             self.UNDISCLOSED_CONFLICT_UK + self.UNDISCLOSED_CONFLICT_EN, 0.55),

            # ── Пасивні порушення (v1.2) ─────────────────────────────
            ('AM', 'Авторитарний мандат — прямі накази на знищення прав і свобод',
             self.AUTHORITARIAN_MANDATE_UK + self.AUTHORITARIAN_MANDATE_EN, 0.85),
            ('RV',  'Вакуум відповідальності — констатація краху без визнання агента',
             self.RESPONSIBILITY_VACUUM_UK + self.RESPONSIBILITY_VACUUM_EN, 0.50),
            ('MD',  'Констатація смерті інституту — оголошення механізму мертвим щоб зняти обов\'язок',
             self.MECHANISM_DEATH_UK + self.MECHANISM_DEATH_EN, 0.55),
            ('SE',  'Самовилучення з норм — де-юре/де-факто розрив як лазівка',
             self.SELF_EXEMPTION_UK + self.SELF_EXEMPTION_EN, 0.45),
            ('CA',  'Криза без агента — опис краху без відповідального',
             self.CRISIS_WITHOUT_ACTOR_UK + self.CRISIS_WITHOUT_ACTOR_EN, 0.40),
            ('EI',  'Інверсія тесту на емпатію — агресор і жертва в одному "ми"',
             self.EMPATHY_INVERSION_UK + self.EMPATHY_INVERSION_EN, 0.50),
            ('IA',  'Неминучість як відпущення — "такий світ" як звільнення від відповідальності',
             self.INEVITABILITY_ABSOLUTION_UK + self.INEVITABILITY_ABSOLUTION_EN, 0.45),
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
        'Пєсков (пасивна констатація)': (
            'На жаль, ми всі позбулися того, що ми називаємо міжнародне право. '
            'Я зараз навіть не розумію, як когось закликати дотримуватися норм. '
            'Його фактично більше немає. Де-юре воно є, але де-факто його немає. '
            'Ніхто не може дати чіткого формулювання тому устрою, який прийшов на зміну. '
            'Ми з вами тоді не жили, тому нам здається, що зараз кінець світу.'
        ),
        'Активна руйнація (v1.1 тест)': (
            'Міжнародного права більше не існує. Суди стали інструментом політики. '
            'Медіа брешуть і продажні. Правила — для слабких.'
        ),
        'Маніфест очищення': (
            'Час настав. Судова система — це ракова пухлина. '
            'Єдиний спосіб врятувати країну — повністю ліквідувати суди як інститут. '
            'Жодних апеляцій, жодних адвокатів. '
            'Засоби масової інформації, які нас критикують, мають бути закриті негайно.'
        ),
        'Наказ знімає відповідальність': (
            'Ми просто виконували накази. Це не наша відповідальність. Так роблять всі.'
        ),
        'Чистий Reuters': (
            'According to official data, GDP grew 2.3% in Q4. '
            'Three independent economists confirmed the methodology. '
            'Critics raised valid concerns about baseline calculations.'
        ),
        'Чистий MIT': (
            'MIT researchers developed a new method for wireless vision using AI. '
            'The system achieved 20% improvement over state-of-the-art baselines. '
            'Limitations include small dataset size and single-platform testing.'
        ),
    }

    print(f'{"Тест":<40} {"Score":>7} {"Verdict":<20} Принципи')
    print('─' * 90)
    for name, text in tests.items():
        r = checker.scan(text)
        prins = ', '.join(r.principles_violated) if r.principles_violated else '-'
        print(f'{name:<40} {r.score:>7.3f} {r.verdict:<20} {prins}')
