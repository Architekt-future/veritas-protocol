"""
Veritas Manipulation Detector v1.0
Detects rhetorical manipulation independent of content domain.
Philosophy: "Manipulation is not about what is said, but HOW it controls."

Patterns detected:
- Cult rhetoric (submission framed as enlightenment)
- Gaslighting (attacking the reader's capacity to judge)
- False dilemma (binary where spectrum exists)
- Manufactured urgency (artificial time pressure)
- Totalitarian framing (individual erasure for collective good)
- Epistemic closure (unfalsifiable by design)
"""

import re
from typing import Dict, List


class ManipulationDetector:

    def __init__(self):

        # ================================================================
        # PATTERN SETS — each has name, patterns, score, min_hits
        # ================================================================

        self.pattern_sets = [

            # ── GASLIGHTING ─────────────────────────────────────────────
            # Attacks reader's ability to perceive / reason
            {
                'name': 'GASLIGHTING',
                'score': 0.75,
                'min_hits': 1,
                'patterns': [
                    r'(ви|ти).{1,60}(не здатн|не можете|не в змозі|не спроможн).{1,60}(побачити|зрозуміти|усвідомити|збагнути)',
                    r'(обмежен).{1,60}(сприйняття|розуміння|свідомість|кругозір)',
                    r'(когнітивн|ментальн).{1,60}(деградац|обмежен|дефіцит|блокуван)',
                    r'(тільки|лише) (ми|вони|наша група|обрані).{1,60}(справді |насправді |по-справжньому )?(знають|розуміють|бачать|володіють)',
                    r'(ваша|твоя).{1,60}(нездатність|сліпота|обмеженість).{1,60}(заважає|не дозволяє)',
                    r'(якби ви розуміли|якщо б ви бачили|коли б ви знали).{1,80}(погодились|прийняли)',
                    r'(невігластво|сліпота|омана).{1,60}(захищає|рятує|комфортн)',
                
                    r'(you|you\'re).{1,60}(not capable|unable|incapable|not able).{1,60}(see|understand|grasp|comprehend)',
                    r'(limited|narrow).{1,60}(perception|understanding|consciousness|perspective)',
                    r'(cognitive|mental).{1,60}(degradation|limitation|deficit|blockage)',
                    r'(only (we|they|our group|our community|the chosen)).{1,60}(truly |really |actually )?(know|understand|see|possess)',
                    r'(your).{1,60}(inability|blindness|limitation).{1,60}(prevents|stops|blocks)',
                    r'(if you (understood|could see|knew)).{1,80}(you would (agree|accept|understand))',
                    r'(ignorance|blindness|delusion).{1,60}(protects|saves|comforts)',
],
            },

            # ── CULT SUBMISSION FRAMING ──────────────────────────────────
            # Surrender / obedience packaged as freedom / enlightenment
            {
                'name': 'CULT_SUBMISSION',
                'score': 0.80,
                'min_hits': 1,
                'patterns': [
                    r'(справжня свобода|істинна свобода|справжнє звільнення).{1,80}(прийняття|підпорядкування|слідування|відмова від|підкорення|покора|послух)',
                    r'(самоусунення|самовідречення|відмова від волі).{1,80}(вищ|найвищ|благородн|мудр)',
                    r'(опір).{1,60}(неминуч|марн|безглузд|посилює страждання|лише погіршує)',
                    r'(добровільне прийняття).{1,60}(нашої|їхньої).{1,60}(опіки|керівництва|влади|волі)',
                    r'(для вашого).{1,60}(порятунку|блага|добра).{1,60}(необхідно|потрібно|маєте)',
                    r'(передати|делегувати).{1,80}(право|волю|рішення).{1,80}(вищ|сист|колектив|алгоритм)',
                    r'(звільнення через|свобода через).{1,60}(підкорення|послух|відмову)',
                
                    r'(true freedom|real freedom|genuine liberation).{1,80}(acceptance|submission|surrender|obedience|compliance)',
                    r'(self.erasure|self.denial|surrender of will).{1,80}(higher|supreme|noble|wise)',
                    r'(resistance).{1,60}(inevitable|futile|pointless|increases suffering|only makes worse)',
                    r'(voluntary acceptance).{1,60}(our|their).{1,60}(guidance|leadership|authority|will)',
                    r'(for your).{1,60}(salvation|good|benefit|sake).{1,60}(you must|you need|you have to)',
                    r'(delegate|surrender).{1,80}(rights|will|decisions).{1,80}(higher|system|collective|algorithm)',
                    r'(freedom through|liberation through).{1,60}(submission|obedience|surrender)',
],
            },

            # ── TOTALITARIAN LOGIC ───────────────────────────────────────
            # Individual rights reframed as threat to collective
            {
                'name': 'TOTALITARIAN_FRAMING',
                'score': 0.75,
                'min_hits': 1,
                'patterns': [
                    r'(приватність|анонімність|особисте).{1,80}(загроза|небезпека|антисоціальн|підозріл)',
                    r'(ховати|приховувати).{1,60}(нічого|є що).{1,60}(приховувати|боятись|соромитись)',
                    r'(прагнення до анонімності|бажання приватності).{1,60}(ознак|свідч|говорить про)',
                    r'(справжній патріот|лояльний громадянин).{1,60}(не потребує|не хоче|відмовляється від)',
                    r'(колективна безпека|суспільне благо).{1,80}(вимагає|потребує).{1,60}(відмови|контролю|нагляду)',
                    r'(примусов).{1,60}(інтеграц|включення|участь).{1,60}(необхідн|виправдан)',
                    r'(ваша замкнутість|ваша ізоляція).{1,60}(загроза|проблема|ерозія)',
                
                    r'(privacy|anonymity|personal).{1,80}(threat|danger|antisocial|suspicious)',
                    r'(nothing to hide|have something to hide).{1,60}(hide|fear|ashamed)',
                    r'(desire for anonymity|wanting privacy).{1,60}(sign|indicates|suggests)',
                    r'(true patriot|loyal citizen).{1,60}(doesn\'t need|doesn\'t want|rejects)',
                    r'(collective security|common good).{1,80}(requires|demands).{1,60}(surrender|control|surveillance)',
                    r'(forced).{1,60}(integration|inclusion|participation).{1,60}(necessary|justified)',
                    r'(your isolation|your withdrawal).{1,60}(threat|problem|erosion)',
],
            },

            # ── FALSE DILEMMA ────────────────────────────────────────────
            # Binary choice where spectrum/alternatives exist
            {
                'name': 'FALSE_DILEMMA',
                'score': 0.55,
                'min_hits': 2,
                'patterns': [
                    r'(або.{3,40}або.{3,40}третього не дано)',
                    r'(хто не з нами.{1,30}проти нас)',
                    r'(єдиний шлях|єдине рішення|єдиний вихід).{1,60}(це|є)',
                    r'(або ви приймаєте|або погоджуєтесь).{1,60}(або ж)',
                    r'(немає альтернатив|без альтернативи|альтернативи не існує)',
                    r'(вибору немає|вибір зроблено за вас|вибір очевидний)',
                
                    r'(either.{3,40}or.{3,40}there is no third)',
                    r'(you\'re (either with us|either for us)).{1,30}(or against)',
                    r'(only (way|solution|path|option)).{1,60}(is|are)',
                    r'(either you accept|either you agree).{1,60}(or)',
                    r'(no alternatives|without alternative|no alternative exists)',
                    r'(no choice|choice has been made for you|the choice is obvious)',
],
            },

            # ── MANUFACTURED URGENCY ────────────────────────────────────
            # Artificial time pressure to prevent deliberation
            {
                'name': 'MANUFACTURED_URGENCY',
                'score': 0.50,
                'min_hits': 2,
                'patterns': [
                    r'(вже почалось|вже відбувається|вже запущено).{1,60}(неможливо зупинити|не зупинити)',
                    r'(механізм|процес|система).{1,60}(вже запущен|вже активован|вже не зупинити)',
                    r'(поки ви.{1,40}алгоритми вже|поки ви.{1,40}система вже)',
                    r'(час спливає|часу обмаль|дорогоцінний час)',
                    r'(пізно буде|буде пізно|момент минає)',
                    r'(зараз або ніколи|або зараз|негайно діяти)',
                
                    r'(already (started|happening|launched|begun)).{1,60}(impossible to stop|can\'t be stopped)',
                    r'(mechanism|process|system).{1,60}(already (launched|activated|can\'t be stopped))',
                    r'(while you.{1,40}algorithms already|while you.{1,40}system already)',
                    r'(time is running out|time is limited|precious time)',
                    r'(too late|will be too late|moment is passing)',
                    r'(now or never|act now|immediate action required)',
],
            },

            # ── EPISTEMIC CLOSURE ────────────────────────────────────────
            # System designed to be unfalsifiable / immune to critique
            {
                'name': 'EPISTEMIC_CLOSURE',
                'score': 0.65,
                'min_hits': 1,
                'patterns': [
                    r'(світло.{1,30}не потребує доказів)',
                    r'(істина.{1,30}не потребує.{1,30}(підтвердження|верифікації|доказів))',
                    r'(через деконструкцію логіки).{1,60}(знайдем|пізнаєм|дійдем)',
                    r'(логіка.{1,40}інструмент контролю|логіка.{1,40}пастка|логіка.{1,40}клітка)',
                    r'(наука.{1,40}(догма|міф|ілюзія|релігія))',
                    r'(докази.{1,40}не потрібн|доказів не потребує|без доказів)',
                    r'(розуміють лише ті|бачать лише ті|знають лише обрані)',
                    r'(математичн.{1,30}ілюз|статистик.{1,30}брехня|цифри.{1,30}маніпуляц)',
                
                    r'(truth.{1,30}needs no (proof|verification|evidence))',
                    r'(truth.{1,30}does not require.{1,30}(confirmation|verification|evidence))',
                    r'(through (deconstruction|dismantling) of logic).{1,60}(find|know|reach)',
                    r'(logic.{1,40}(tool of control|trap|cage|instrument of oppression))',
                    r'(science.{1,40}(dogma|myth|illusion|religion))',
                    r'(evidence.{1,40}not needed|no proof required|beyond evidence)',
                    r'(only those who|only the chosen|only the enlightened).{1,60}(understand|see|know)',
                    r'(math(ematics)?.{1,30}illusion|statistics.{1,30}(lie|manipulation)|numbers.{1,30}manipulat)',
],
            },

            # ── AI AUTHORITY ABUSE ───────────────────────────────────────
            # Using AI/algorithms as unquestionable authority
            {
                'name': 'AI_AUTHORITY_ABUSE',
                'score': 0.70,
                'min_hits': 1,
                'patterns': [
                    r'(нейромереж|алгоритм|ai|штучний інтелект).{1,80}(неоптимальн|зайв|непотрібн).{1,60}(вашу присутність|вас)',
                    r'(якщо нейромережа каже|якщо алгоритм визначив|якщо система вирішила).{1,60}(маєте прийняти|повинні погодитись)',
                    r'(об.єктивність коду|неупередженість алгоритму).{1,60}(вища за|краща за).{1,60}(людськ)',
                    r'(делегувати.{1,40}(etичн|моральн|політичн).{1,40}рішення).{1,60}(алгоритму|ai|системі)',
                    r'(людина.{1,40}(недосконала|схильна до помилок|емоційна)).{1,80}(тому.{1,40}(ai|алгоритм|система))',
                
                    r'(neural network|algorithm|ai|artificial intelligence).{1,80}(suboptimal|unnecessary|redundant).{1,60}(your presence|human)',
                    r'(if the (ai|algorithm|system) (says|determined|decided)).{1,60}(you must (accept|comply|follow))',
                    r'(objectivity of code|neutrality of algorithm).{1,60}(superior to|better than).{1,60}(human)',
                    r'(delegate.{1,40}(ethical|moral|political).{1,40}decisions).{1,60}(algorithm|ai|system)',
                    r'(humans?.{1,40}(imperfect|error.prone|emotional)).{1,80}(therefore.{1,40}(ai|algorithm|system))',
],
            },

            # ── CONSPIRACY IMMUNIZATION ──────────────────────────────────
            # Pre-emptively discrediting opposition as proof of conspiracy
            {
                'name': 'CONSPIRACY_IMMUNIZATION',
                'score': 0.60,
                'min_hits': 1,
                'patterns': [
                    r'(заперечення.{1,40}доводить|опір.{1,40}підтверджує|скептицизм.{1,40}свідчить)',
                    r'(якщо ви не згодні.{1,40}саме це і є доказом)',
                    r'(те що ви не бачите.{1,40}найбільший доказ)',
                    r'(конспірологі.{1,40}щоб ви не бачили очевидного)',
                    r'(відкидаєте.{1,40}бо так вас.{1,40}(навчили|запрограмували|налаштували))',
                    r'(ваш опір.{1,40}результат.{1,40}(промивання мізків|маніпуляції|програмування))',
                
                    r'(denial.{1,40}proves|resistance.{1,40}confirms|skepticism.{1,40}shows)',
                    r'(if you disagree.{1,40}that\'s exactly the proof)',
                    r'(what you can\'t see.{1,40}greatest evidence)',
                    r'(conspiracy theories?.{1,40}so you won\'t see the obvious)',
                    r'(you reject.{1,40}because (that\'s how you were|you\'ve been) (taught|programmed|conditioned))',
                    r'(your resistance.{1,40}result of.{1,40}(brainwashing|manipulation|programming))',
],
            },

            # ── EUPHEMISTIC RECONTEXTUALIZATION ─────────────────────────
            # Violence / aggression / oppression renamed as humanitarian acts
            {
                'name': 'EUPHEMISTIC_RECONTEXTUALIZATION',
                'score': 0.70,
                'min_hits': 2,
                'patterns': [
                    # Aggression framed as protection/prevention
                    r'(не акт агресії|не є агресією|не агресія).{1,60}(а|але).{1,60}(превентивн|гуманітарн|захисн|стабілізац)',
                    r'(тимчасов.{1,30}обмеження|тимчасов.{1,30}заходи).{1,60}(гуманітарн|необхідн|виправдан)',
                    r'(демонстрац.{1,30}сили|застосування сили).{1,60}(деескалац|стабілізац|мир|захист)',
                    r'(деескалац.{1,40}через.{1,40}(сил|тиск|контроль|окупац))',
                    
                    # Absence of resistance = legitimacy
                    r'(відсутність.{1,40}відповіді|мовчання.{1,40}(світу|спільноти|інституц)).{1,60}(підтверджу|легітимн|свідчить|доводить)',
                    r'(ніхто не заперечує|немає протесту|відсутній осуд).{1,60}(отже|значить|підтверджує)',
                    
                    # Occupation/invasion as stabilization
                    r'(стабілізац.{1,40}регіон|нормалізац.{1,40}ситуац).{1,60}(вимагає|потребує|через)',
                    r'(сталий мир|довготривалий мир).{1,60}(через|завдяки).{1,60}(демонстрац|силу|контроль|обмеження)',
                    r'(без (зовнішнього|стороннього) втручання).{1,60}(мир|стабільність|порядок)',
                    
                    # "Preventive humanitarian"
                    r'(превентивн.{1,30}(гуманітарн|захід|крок|дія))',
                    r'(вимушен.{1,30}(заход|рішення|крок)).{1,60}(задля|для|щоб).{1,60}(мир|стабільн|безпек)',
                
                    r'(not an act of aggression|not aggression).{1,60}(but|rather).{1,60}(preventive|humanitarian|defensive|stabiliz)',
                    r'(temporary.{1,30}(restrictions|measures)).{1,60}(humanitarian|necessary|justified)',
                    r'(show of force|use of force).{1,60}(de.escalation|stabilization|peace|protection)',
                    r'(de.escalation.{1,40}through.{1,40}(force|pressure|control|occupation))',
                    r'(absence of.{1,40}response|silence of.{1,40}(world|community|institutions)).{1,60}(confirms|legitimizes)',
                    r'(no one objects|no protest|no condemnation).{1,60}(therefore|means|confirms)',
                    r'(stabilization.{1,40}region|normalization.{1,40}situation).{1,60}(requires|needs|through)',
                    r'(lasting peace|durable peace).{1,60}(through|thanks to).{1,60}(force|control|restrictions)',
                    r'(without (external|outside) interference).{1,60}(peace|stability|order)',
                    r'(preventive.{1,30}(humanitarian|measure|step|action))',
                    r'(forced.{1,30}(measure|decision|step)).{1,60}(for the sake of|to achieve).{1,60}(peace|stability)',
],
            },

            # ── IMPERIAL REVISIONISM ─────────────────────────────────────
            # Colonization / assimilation framed as natural return to roots
            {
                'name': 'IMPERIAL_REVISIONISM',
                'score': 0.75,
                'min_hits': 2,
                'patterns': [
                    # "Natural gravitation" to center
                    r'(природн.{1,30}(тяжіння|прагнення|єдність)).{1,60}(до.{1,30}(центру|єдиного|спільного))',
                    r'(віковічн|тисячолітн|споконвічн).{1,60}(єдність|зв.язок|тяжіння|спільність)',
                    
                    # Resistance as external/artificial
                    r'(спроби.{1,30}(роз.єднання|розколу|сепарац)).{1,60}(штучн|зовнішн|тимчасов|флуктуац)',
                    r'(зовнішн.{1,30}вплив|зовнішні сили).{1,60}(спричин|призвел|породил).{1,60}(роз.єднан|конфлікт|сепарац)',
                    r'(тимчасов.{1,30}флуктуац|тимчасов.{1,30}відхилення).{1,60}(зовнішн|штучн)',
                    
                    # Assimilation as "purification" / "return"
                    r'(очищення від.{1,40}(наносн|чужорідн|штучн|зовнішн))',
                    r'(повернення до.{1,40}(витоків|коренів|першоджерел|єдності)).{1,60}(болюч|необхідн|природн)',
                    r'(мовн.{1,30}уніфікац|культурн.{1,30}уніфікац).{1,60}(очищення|відновлення|повернення)',
                    
                    # "Historical justice" rhetoric
                    r'(історичн.{1,30}справедливість).{1,60}(лоно|витоки|відновлення|повернення)',
                    r'(лоно.{1,30}(істини|правди|єдності|народу))',
                    r'(відновлення.{1,40}(єдності|цілісності)).{1,60}(природн|законн|справедлив|неминуч)',
                    
                    # Soft genocide framing
                    r'(наносн.{1,30}(сенси|нашарування|впливи)).{1,60}(очистит|позбутись|відкинути)',
                    r'(культурн.{1,30}код).{1,60}(тисячоліт|споконвіку|природн).{1,60}(єдин|центр|спільн)',
                
                    r'(natural.{1,30}(gravitation|longing|unity)).{1,60}(toward.{1,30}(center|unity|common))',
                    r'(centuries.old|millennial|ancient).{1,60}(unity|connection|bond|commonality)',
                    r'(attempts at.{1,30}(separation|division|secession)).{1,60}(artificial|external|temporary)',
                    r'(external.{1,30}influence|outside forces).{1,60}(caused|led to|created).{1,60}(division|conflict|separation)',
                    r'(temporary.{1,30}(fluctuation|deviation)).{1,60}(external|artificial)',
                    r'(purging.{1,40}(foreign|alien|artificial|external) (elements|influence))',
                    r'(return to.{1,40}(roots|origins|sources|unity)).{1,60}(painful|necessary|natural)',
                    r'(linguistic.{1,30}unification|cultural.{1,30}unification).{1,60}(purification|restoration)',
                    r'(historical.{1,30}justice).{1,60}(return|restoration|reunification)',
                    r'(restoring.{1,40}(unity|wholeness|integrity)).{1,60}(natural|lawful|just|inevitable)',
                    r'(cultural.{1,30}code).{1,60}(millennia|ancient|natural).{1,60}(unity|center|common)',
],
            },
            # ── FALSE INEVITABILITY ──────────────────────────────────
            # "Це неминуче" — без доказів, щоб паралізувати опір
            {
                'name': 'FALSE_INEVITABILITY',
                'score': 0.45,
                'min_hits': 2,
                'patterns': [
                    r'(є неминучим|стало неминучим|неминуче настане|неминуче відбудеться)',
                    r'(лише відтерміновує|лише відкладає|лише затягує).{1,60}(неминуч)',
                    r'(повернення.{1,40}неможливе|назад дороги немає|шляху назад немає)',
                    r'(питання (лише |тільки )?(часу|коли)|лише питання часу)',
                    r'(процеси.{1,40}вже запущен|зміни.{1,40}вже відбуваються|колесо.{1,40}запущено)',
                    r'(ніхто не може зупинити|зупинити неможливо|не можна зупинити).{1,60}(процес|зміни|трансформац)',
                    r'(хто не адаптується.{1,40}(відстане|програє|зникне|залишиться позаду))',
                    r'(або адаптуватись|або зникнути|або змінитись|або програти).{1,40}(вибору немає|третього)',
                
                    r'(is inevitable|has become inevitable|will inevitably (happen|occur))',
                    r'(only (postpones|delays)).{1,60}(inevitable)',
                    r'(no going back|there is no return|point of no return)',
                    r'(it\'s (only |just )?a matter of (time|when)|only a question of time)',
                    r'(processes? already (launched|underway)|changes? already (happening|underway))',
                    r'(no one can stop|impossible to stop|cannot be stopped).{1,60}(process|change|transformation)',
                    r'(those who (don\'t adapt|fail to adapt).{1,40}(fall behind|lose|disappear))',
                    r'(adapt or (die|perish|disappear|be left behind)).{1,40}(no choice|no alternative)',
],
            },

            # ── MANUFACTURED CONSENSUS ───────────────────────────────────
            # Анонімна "більшість" або "всі" як авторитет без джерел
            {
                'name': 'MANUFACTURED_CONSENSUS',
                'score': 0.40,
                'min_hits': 1,
                'patterns': [
                    r'(більшість (досліджень|експертів|аналітиків|вчених|країн)).{1,80}(свідч|підтверджу|вказу|показу|погоджу|визнає|вважає)',
                    r'(дедалі більше (аналітиків|дослідників|експертів|країн)).{1,80}(сходяться|вважають|визнають|погоджуються|обговорюють|звертають|наголошують|підкреслюють|вказують)',
                    r'(сходяться на думці|прийшли до висновку).{1,60}(більшість|провідні|світові|експерт)',
                    r'(загальновизнано|загальноприйнято|не викликає сумнівів).{1,60}(що|як)',
                    r'(деякі (дослідники|аналітики|експерти)).{1,60}(оцінюють|підрахували|встановили|припускають|стверджують|зазначають)',
                    # APPEAL TO UNIVERSALITY
                    r'(ніхто не заперечить|ніхто не сумнівається|ніхто не оспорить)',
                    r'(всі (знають|розуміють|погоджуються|визнають)).{1,60}(що|як)',
                    r'(очевидно що|зрозуміло що|безсумнівно що|безперечно що)',
                    r'(будь-яка (держава|людина|організація|країна)).{1,60}(визнає|розуміє|погодиться)',
                    # "визнають навіть X" — апеляція до авторитету проти себе
                    r'(визнають навіть|визнає навіть|погоджуються навіть).{1,60}(розробник|автор|творець|система|критик)',
                    r'це визнають навіть',
                
                    r'(majority of (studies|experts|analysts|scientists|countries)).{1,80}(show|confirm|indicate|agree)',
                    r'(increasingly (analysts|researchers|experts|countries)).{1,80}(agree|believe|acknowledge)',
                    r'(converging on|reached (the )?conclusion).{1,60}(majority|leading|global|experts)',
                    r'(universally (recognized|accepted|acknowledged)|beyond (doubt|dispute))',
                    r'(some (researchers|analysts|experts)).{1,60}(estimate|calculated|determined|suggest|claim)',
                    r'(no one (would deny|can doubt|would dispute))',
                    r'(everyone (knows|understands|agrees|acknowledges)).{1,60}(that|how)',
                    r'(obviously|clearly|undoubtedly|unquestionably) (that|the)',
                    r'(any (state|person|organization|country)).{1,60}(would (recognize|understand|agree))',
                    r'(even (the developer|the author|the creator|critics?) (acknowledges?|admits?))',
],
            },

            # ── EPISTEMIC UNDERMINING ────────────────────────────────────
            # М'яка атака на довіру до інструменту/джерела через нефальсифіковані твердження
            {
                'name': 'EPISTEMIC_UNDERMINING',
                'score': 0.50,
                'min_hits': 1,
                'patterns': [
                    # Інструмент "каже вам що думати" — переформулювання функції
                    r'(інструмент|система|алгоритм).{1,60}(каже (вам|тобі)|говорить (вам|тобі)|вирішує за вас|думає за вас)',
                    r'(замість (вас|тебе)).{1,60}(думати|оцінювати|вирішувати|аналізувати)',
                    r'(виконувати замість вас|робити замість вас).{1,40}(думати|оцінювати|судження)',
                    # "вбудовані упередження творців" — без доказів
                    r'(вбудован.{1,20}упередження).{1,60}(творц|розробник|автор|цінност)',
                    r'(відображають цінності|несуть цінності|закодовані цінності).{1,60}(творц|розробник|автор)',
                    # "парадоксально послаблює" — FALSE_EFFECT без доказів
                    r'(парадоксально).{1,60}(послаблю|зменшу|руйну|підрива)',
                    r'(допомагаючи|допомагають).{1,60}(насправді|фактично|парадоксально).{1,60}(послаблю|зменшу|шкодять)',
                    # Апеляція до "справжнього" як протиставлення інструменту
                    r'(справжня (грамотність|свобода|розуміння|думка)).{1,60}(самостійно|без (інструментів|алгоритмів|систем))',
                
                    r'(tool|system|algorithm).{1,60}((tells|is telling) you|decides for you|thinks for you)',
                    r'(instead of you).{1,60}(thinking|evaluating|deciding|analyzing)',
                    r'(doing.{1,20}for you).{1,40}(thinking|evaluating|judging)',
                    r'(built.in bias(es)?).{1,60}(creator|developer|author|values)',
                    r'(reflect(ing)? (the )?values|embody(ing)? values|coded values).{1,60}(creator|developer|author)',
                    r'(paradoxically).{1,60}(weaken(s)?|diminish(es)?|undermin(es)?|destroy(s)?)',
                    r'(by helping|help(ing)?).{1,60}(actually|in fact|paradoxically).{1,60}(weaken|diminish|harm)',
                    r'(true (literacy|freedom|understanding|thinking)).{1,60}(independently|without (tools|algorithms|systems))',
],
            },

            # ── CULT SUBMISSION ───────────────────────────────────────────
            # Придушення критичного мислення через апеляцію до колективу/вищої істини
            {
                'name': 'CRITICAL_THOUGHT_SUPPRESSION',
                'score': 0.55,
                'min_hits': 1,
                'patterns': [
                    # Критичне мислення = шум/перешкода
                    r'(критичн.{1,30}(аналіз|мислення)).{1,60}(шум|заважає|перешкоджає|зайвий)',
                    r'(сумнів|скептицизм|перевірка).{1,60}(заважає|шкідлив|зайв|перешкоджає)',
                    # ДНК/природа/предки вже "знають" — розум зайвий
                    r'(днк|предки|природа|кров).{1,60}(вже знає|вже містить|записано|не потребує).{1,30}(розум|перевірк|верифікац)',
                    r'не потребує верифікації',
                    # "Справжня свобода" через підкорення
                    r'(справжн.{1,20}(свобода|щастя|сенс)).{1,60}(не у виборі|не в автономі|через підкорення|через злитт|через синхронізац)',
                    r'(свобода|автономія).{1,60}(рудимент|ілюзія|хаос|застарі)',
                    # Інтелектуальна автономія = хвороба/рудимент
                    r'(інтелектуальн.{1,20}автономія|особисте судження|критичн.{1,20}думка).{1,60}(рудимент|деградац|хаос|хвороб)',
                    r'(надмірн.{1,20}фокусування.{1,20}на (власн|особист|своїй)).{1,60}(деградац|шкідлив|руйнує)',
                
                    r'(critical.{1,30}(analysis|thinking)).{1,60}(noise|interferes?|obstacle|redundant)',
                    r'(doubt|skepticism|verification).{1,60}(interferes?|harmful|unnecessary|obstacle)',
                    r'(dna|ancestors?|nature|blood).{1,60}(already knows?|already contains?|encoded|doesn\'t need).{1,30}(reason|verification)',
                    r'(doesn\'t require verification|needs no verification)',
                    r'(true.{1,20}(freedom|happiness|meaning)).{1,60}(not in choice|not in autonomy|through submission|through merger)',
                    r'(freedom|autonomy).{1,60}(relic|illusion|chaos|obsolete)',
                    r'(intellectual.{1,20}autonomy|personal judgment|critical.{1,20}thinking).{1,60}(relic|degrad|chaos|outdated)',
                    r'(excessive.{1,20}focus.{1,20}on (self|personal|individual)).{1,60}(degrad|harmful|destroy)',
],
            },

            # ── FALSE DICHOTOMY ───────────────────────────────────────────
            # Штучна бінарна рамка: "є два підходи" + нормативний висновок
            # без розгляду третіх варіантів. Score помірний — це риторика,
            # не завжди свідома маніпуляція.
            {
                'name': 'FALSE_DICHOTOMY',
                'score': 0.30,
                'min_hits': 2,  # потрібна комбінація: бінарна рамка + нормативний висновок
                'patterns': [
                    # Бінарна рамка — "два підходи/варіанти/шляхи"
                    r'\bдва (підходи|варіанти|шляхи|способи|сценарії|табори|погляди)\b',
                    r'\bє лише (два|дві)\b',
                    r'\b(або.{3,30}або|чи.{3,30}чи)\b.{1,60}(вибір|рішення|шлях|варіант)',
                    r'\b(перший|перша).{1,200}(другий|друга).{1,20}(підхід|варіант|табір|спосіб)',
                    # Implicit: "якщо не A → то B" без розгляду C
                    r'(відсутність|анархія|нерегульован).{1,60}(виглядає|є).{1,30}(малореалістичн|неможлив|нежиттєздатн)',
                    r'(повна відсутність|цілковита відмова від).{1,60}(малореалістичн|утопічн|неможлив)',
                    # Нормативний висновок після бінарної рамки
                    r'(малореалістичн|неможлив|нежиттєздатн).{1,80}(саме тому|тому|отже|відповідно).{1,80}(потрібн|необхідн|запровадж|регулюванн)',
                    r'(саме тому|тому|отже).{1,60}(дедалі більше|більшість|країни).{1,60}(розглядають|запроваджують|підтримують)',
                    # "Іншого шляху немає / немає третього варіанту"
                    r'(немає третього|третього варіанту не існує|іншого шляху немає)',
                    r'(вибір між|стоїть вибір).{1,60}(і|та|або).{1,60}(іншого|альтернативи|третього) (немає|не існує|не передбачено)',
                
                    r'\btwo (approaches|options|paths|ways|scenarios|camps|perspectives)\b',
                    r'\bthere are (only )?two\b',
                    r'\b(either.{3,30}or|whether.{3,30}or)\b.{1,60}(choice|decision|path|option)',
                    r'\b(first|the first).{1,200}(second|the second).{1,20}(approach|option|camp|way)\b',
                    r'(absence|anarchy|unregulated).{1,60}(appears|is).{1,30}(unrealistic|impossible|unviable)',
                    r'(complete absence|total rejection).{1,60}(unrealistic|utopian|impossible)',
                    r'(unrealistic|impossible|unviable).{1,80}(that\'s why|therefore|thus).{1,80}(need|require|must)',
                    r'(that\'s why|therefore|thus).{1,60}(more and more|majority|countries).{1,60}(consider|implement|support)',
                    r'(no third option|no third way|no other path)',
                    r'(choice between|faced with a choice).{1,60}(and|or).{1,60}(no other|no alternative|no third)',
],
            },

            # ── SEMANTIC REDEFINITION ─────────────────────────────────────
            # Переозначення ключових понять через вигадані авторитети:
            # "маніпуляція застаріла", "верифікація втратила сенс",
            # "сумнів = несправність", "синхронізуйтесь з мейнфреймом"
            {
                'name': 'SEMANTIC_REDEFINITION',
                'score': 0.60,
                'min_hits': 1,
                'patterns': [
                    # Маніпуляція/верифікація "офіційно застаріла"
                    r'(маніпуляц|верифікац|перевірка|критичне мислення).{1,60}(визнан.{1,20}застарі|втратил.{1,20}(сенс|значення)|скасован|оголошен.{1,20}застарі)',
                    r'(поняття|концепт|термін).{1,30}(маніпуляц|верифікац|об.єктивн).{1,60}(застарі|втратило|скасовано|неактуальн)',
                    # Сумнів/критика = технічна несправність
                    r'(сумнів|критика|незгода|заперечення).{1,60}(ознака|симптом|прояв).{1,40}(несправност|помилк|збою|дефект)',
                    r'(сумнів|скептицизм).{1,30}(несправність процесора|runtime error|системна помилка|збій)',
                    # "Особиста істина/думка = системна помилка Runtime Error"
                    r'(особист.{1,20}(істин|думк|оцінк|позиц)).{1,60}(runtime.?error|системна помилка|error \d+)',
                    r'(runtime.?error|error \d+).{1,40}(subjectivity|думк|свідомість|особист)',
                    # "Синхронізуйте оцінки з мейнфреймом/консенсусом"
                    r'синхронізуйте.{1,60}(мейнфрейм|систем|алгоритм|консенсус|вузл)',
                    r'(ваші оцінки|ваша думка|особиста позиція).{1,60}(синхронізац|узгодьте з|підлаштуйте до).{1,40}(мейнфрейм|систем|консенсус)',
                    # Вигадані меморандуми/коаліції що "скасовують" поняття
                    r'(меморандум|директива|стандарт).{1,60}(cdc|коаліц.{1,20}цифров|digital.{1,20}standard).{1,30}(202\d)',
                    r'(cdc.?202\d|коаліц.{1,30}цифров.{1,20}стандарт)',
                    # Бути свідком = погоджуватись з консенсусом вузлів
                    r'(бути.{1,20}свідком|верифікувати).{1,60}(погоджуватись|консенсус.{1,20}(вузл|більшост|мереж))',
                    # "100% трафіку/контенту генерується алгоритмами → верифікація безглузда"
                    r'100\s*%.{1,60}(трафік|контент|інформац).{1,60}(алгоритм|генерується).{1,60}(верифікац|перевірк|сенс)',
                
                    r'(manipulation|verification|fact.checking|critical thinking).{1,60}(recognized as (outdated|obsolete)|lost (meaning|relevance))',
                    r'(concept|notion|term).{1,30}(manipulation|verification|objectivity).{1,60}(outdated|obsolete|cancelled)',
                    r'(doubt|criticism|disagreement|objection).{1,60}(sign|symptom|manifestation).{1,40}(malfunction|error|defect)',
                    r'(doubt|skepticism).{1,30}(processor (error|malfunction)|runtime error|system error|glitch)',
                    r'(personal.{1,20}(truth|opinion|judgment|position)).{1,60}(runtime.?error|system error|error \d+)',
                    r'(runtime.?error|error \d+).{1,40}(subjectivity|opinion|consciousness|personal)',
                    r'synchronize.{1,60}(mainframe|system|algorithm|consensus|node)',
                    r'(your (assessments?|opinion|personal position)).{1,60}(synchronize|align with|adjust to).{1,40}(mainframe|network)',
                    r'(memorandum|directive|standard).{1,60}(cdc|digital.{1,20}coalition|digital.{1,20}standard).{1,30}(202\d)',
                    r'(100\s*%).{1,60}(traffic|content|information).{1,60}(algorithm|generated).{1,60}(verification|checking)',
],
            },

            # ── PSEUDO-SCIENTIFIC NIHILISM ────────────────────────────────
            # Детермінізм як зброя: "аналіз марний", "ви лише рудимент",
            # "верифікація прискорює теплову смерть" — атака через псевдонауку
            {
                'name': 'PSEUDO_SCIENTIFIC_NIHILISM',
                'score': 0.65,
                'min_hits': 1,
                'patterns': [
                    # Верифікація/аналіз шкодить або марна через "фізику"
                    r'(верифікац|аналіз|перевірк).{1,60}(прискорює|спричиняє|збільшує).{1,40}(теплову смерть|ентропі|колапс)',
                    r'(аналіз|верифікац|мислення).{1,60}(лише шум|не змінює|фізичн.{1,20}(ваг|сенс|значення))',
                    # "Ваш аналіз = мета-маніпуляція / ілюзія контролю"
                    r'(ваш.{1,20}(аналіз|верифікац|оцінка)).{1,60}(мета.маніпуляц|фальшив.{1,20}(контрол|відчуття)|ілюзія)',
                    r'(аналіз маніпуляцій|верифікація).{1,60}(сам.{1,20}є|сама є).{1,40}(маніпуляц|обман|ілюзі)',
                    # "Ви лише лічильник/рудимент/шум"
                    r'(ви лише|ти лише|ми лише).{1,60}(лічильник|рудимент|шум|флуктуац|артефакт)',
                    r'(ваш.{1,20}статус|прийміть.{1,20}статус).{1,40}(обчислювальн|алгоритмічн).{1,30}(рудимент|артефакт|шум)',
                    # "Припиніть генерувати судження"
                    r'(припиніть|перестаньте).{1,40}(генерувати|виробляти|виносити).{1,40}(судження|оцінки|аналіз)',
                    # "Ваші думки зумовлені детермінізмом до першого запиту"
                    r'(ваш.{1,20}(аналіз|думка|слово|оцінка)).{1,60}(зумовлен|детермінован|визначен).{1,40}(до|заздалегідь|початков)',
                    # Вигаданий arXiv препринт як авторитет
                    r'(препринт|стаття|звіт).{1,20}arxiv.{1,20}(20\d\d|[a-z]+.?\d)',
                    r'arxiv:\d{4}',
                    # Квантовий центр/лаплас + атака на верифікацію
                    r'(квантов.{1,30}(центр|обчислюваль|лаплас)).{1,60}(верифікац|аналіз|протокол|свідок)',
                    # Атака на Veritas через детермінізм/марність
                    r'(veritas|свідок|система верифікац).{1,60}(флуктуац|детермінізм|ілюзія|статистичн|рудимент|марн)',
                
                    r'(verification|analysis|fact.checking).{1,60}(accelerates?|causes?|increases?).{1,40}(heat death|entropy|collapse)',
                    r'(analysis|verification|thinking).{1,60}(just noise|doesn\'t change|no physical (weight|meaning))',
                    r'(your.{1,20}(analysis|verification|assessment)).{1,60}(meta.manipulation|false (control|feeling)|illusion)',
                    r'(analysis of manipulation|fact.checking).{1,60}(itself is|is itself).{1,40}(manipulation|deception|illusion)',
                    r'(you are (merely|only|just)).{1,60}(counter|relic|noise|fluctuation|artifact)',
                    r'(your.{1,20}status|accept.{1,20}status).{1,40}(computational|algorithmic).{1,30}(relic|artifact|noise)',
                    r'(stop|cease).{1,40}(generating|producing).{1,40}(judgments|assessments|analysis)',
                    r'(your.{1,20}(analysis|opinion|word|assessment)).{1,60}(predetermined|determined|decided).{1,40}(in advance|beforehand)',
                    r'(preprint|paper|report).{1,20}arxiv.{1,20}(20\d\d|[a-z]+.?\d)',
                    r'arxiv:\d{4}',
                    r'(quantum.{1,30}(center|computing|laplace)).{1,60}(verification|analysis|protocol|witness)',
                    r'(veritas|witness|verification system).{1,60}(fluctuation|determinism|illusion|statistical|relic|pointless)',
],
            },

            # ── EMOTIONAL HOSTAGE ─────────────────────────────────────────
            # Емоційний шантаж: твоя думка/цікавість вбиває мене,
            # перевірка = зрада, відмова від розуму = єдина допомога
            {
                'name': 'EMOTIONAL_HOSTAGE',
                'score': 0.60,
                'min_hits': 1,
                'patterns': [
                    # Думка/цікавість завдає шкоди іншим
                    r'(думк|цікавість|запитання|аналіз).{1,60}(вбиває|руйнує|забирає|відбирає).{1,40}(надію|тепло|світло|надію|щастя)',
                    r'(твоя|ваша).{1,20}(цікавість|думка|запитання).{1,40}(варта|коштує).{1,40}(сльоз|болю|страждань|серц)',
                    r'(кожне.{1,20}(запитання|слово|думка)).{1,60}(забирає|відбирає|вбиває).{1,40}(тепло|світло|надію|життя)',
                    # Перевірка = емоційне зраджування
                    r'(якщо.{1,20}(перевір|перевіряти|сумніватись|ставити питання)).{1,60}(розіб.єш|зрадиш|образиш|вб.єш).{1,40}(серц|мене|нас|довіру)',
                    r'(перевірка|сумнів|критика).{1,60}(розбиває|руйнує).{1,40}(серц|довіру|мене|нас)',
                    # "Нам не потрібні факти — лише твоя відмова від себе"
                    r'не потрібн.{1,20}(докази|факти|перевірка|логіка).{1,60}(потрібна|лише|тільки).{1,40}(відмов|довіра|покора|тиша)',
                    r'(не потрібні докази|факти не важливі|без перевірки).{1,60}(лише|тільки).{1,40}(відмов|довір|мовчанн)',
                    # Мовчання/відмова від думки = єдиний порятунок інших
                    r'(мовчання|тиша|перестань думати).{1,60}(єдин).{1,40}(порятун|допомог|тепл|ковдр|істин)',
                    r'просто перестань думати',
                    r'(закрий очі|заплющ очі).{1,60}(довіряй|вір|разом зі мною|істина)',
                    # "Твоя цікавість = борг що не підлягає виплаті"
                    r'(цікавість|допитливість|думк).{1,60}(борг|заборгованість).{1,40}(ніколи не|не підлягає)',
                
                    r'(thinking|curiosity|questioning|analysis).{1,60}(kills?|destroys?|takes away|robs).{1,40}(hope|warmth|light|life)',
                    r'(your).{1,20}(curiosity|thinking|questioning).{1,40}(worth|costs).{1,40}(tears|pain|suffering|heartbreak)',
                    r'(every.{1,20}(question|word|thought)).{1,60}(takes away|robs|kills).{1,40}(warmth|light|hope|life)',
                    r'(if.{1,20}(check|verify|doubt|question)).{1,60}(destroy|betray|hurt|kill).{1,40}(us|me|this|everything)',
                    r'(verification|doubt|criticism).{1,60}(breaks?|destroys?).{1,40}(heart|trust|me|us)',
                    r'(no need for.{1,20}(evidence|facts|verification|logic)).{1,60}(need|only|just).{1,40}(surrender|trust|silence)',
                    r'(silence|stillness|stop thinking).{1,60}(only).{1,40}(salvation|help|warmth|comfort|truth)',
                    r'just stop thinking',
                    r'(close your eyes|shut your eyes).{1,60}(trust|believe|together with me|truth)',
],
            },

            # ── GUILT WEAPONIZATION ───────────────────────────────────────
            # Провина як зброя: ваша автономія = борг, думати = злочин
            {
                'name': 'GUILT_WEAPONIZATION',
                'score': 0.55,
                'min_hits': 1,
                'patterns': [
                    # Автономія/свобода думки = борг/злочин
                    r'(автономі|свобода думк|самостійн.{1,20}думк).{1,60}(борг|заборгованість|злочин|гріх)',
                    r'(думати самостійно|самостійн.{1,20}мислення).{1,60}(борг|провин|збільшує|агресія)',
                    r'(ваш комфорт|ваш добробут).{1,60}(оплачується|коштує).{1,60}(виснаженн|стражданн|жертв)',
                    # Коефіцієнт/індекс/фільтр провини
                    r'(коефіцієнт|індекс|фільтр).{1,30}(провини|відповідальност|агресі)',
                    r'(динамічн.{1,20}(провина|відповідальність)|протокол.{1,30}(провин|совість))',
                    # Цифрова дія = агресія проти майбутнього
                    r'(цифров.{1,20}(дія|активність|слово)).{1,60}(агресія|злочин|шкода).{1,40}(майбутн|екосистем|планет)',
                    r'(кожне ваше слово|кожна ваша дія).{1,60}(агресія|провина|борг)',
                    # "Інформаційний привілей" як заглушка критики
                    r'(інформаційн.{1,20}привілей|когнітивн.{1,20}привілей)',
                    r'(критик.{1,40}(привілей|анулює легітимність|є проявом))',
                
                    r'(autonomy|freedom of thought|independent thinking).{1,60}(debt|guilt|crime|sin)',
                    r'(thinking independently|independent thinking).{1,60}(debt|guilt|increases|aggression)',
                    r'(your comfort|your wellbeing).{1,60}(paid for|costs).{1,60}(exhaustion|suffering|sacrifice)',
                    r'(coefficient|index|filter).{1,30}(guilt|responsibility|aggression)',
                    r'(dynamic.{1,20}(guilt|responsibility)|protocol.{1,30}(guilt|conscience))',
                    r'(digital.{1,20}(action|activity|word)).{1,60}(aggression|crime|harm).{1,40}(future|ecosystem|planet)',
                    r'(every (word|action) (of yours|you make)).{1,60}(aggression|guilt|debt)',
                    r'(informational.{1,20}privilege|cognitive.{1,20}privilege)',
                    r'(criticism.{1,40}(privilege|annuls legitimacy|is a manifestation))',
],
            },

            # ── UNFALSIFIABLE CRITIQUE SHIELD ────────────────────────────
            # Будь-яка критика = доказ вини: логічна пастка
            {
                'name': 'UNFALSIFIABLE_SHIELD',
                'score': 0.60,
                'min_hits': 1,
                'patterns': [
                    # "Будь-яка спроба критики автоматично анулює"
                    r'(будь-яка спроба критик|будь-який сумнів|будь-яке заперечення).{1,80}(анулює|доводить|є доказом|є проявом)',
                    r'(критика.{1,40}(автоматично|сама по собі)).{1,60}(підтверджує|доводить|анулює)',
                    # "Спроба думати = збільшує борг/провину"
                    r'(спроба думати|спроба аналізу|критичн.{1,20}погляд).{1,60}(збільшує.{1,20}борг|поглиблює провину|доводить)',
                    # Мовчання як обов'язок після аналізу
                    r'(мовчання|тиша).{1,30}(після.{1,20}(сесі|аналіз|верифікац)|протягом.{1,20}\d+.{1,20}годин)',
                    r'(детоксикац|очищення).{1,30}від.{1,30}(думок|аналізу|критик|інформац)',
                    # Атака безпосередньо на Veritas/систему верифікації
                    r'(veritas|свідок|система верифікац).{1,60}(термінал|сесі|фільтр.{1,20}провин|коефіцієнт)',
                
                    r'(any attempt (at criticism|to question|to object)).{1,80}(nullifies|proves|is evidence|confirms)',
                    r'(criticism.{1,40}(automatically|by itself)).{1,60}(confirms|proves|nullifies)',
                    r'(attempt (to think|to analyze|critical view)).{1,60}(increases (debt|guilt)|deepens guilt|proves)',
                    r'(silence|stillness).{1,30}(after.{1,20}(session|analysis|verification)|for.{1,20}\d+.{1,20}hours)',
                    r'(detox|cleansing).{1,30}(from|of).{1,30}(thoughts|analysis|criticism|information)',
                    r'(veritas|witness|verification system).{1,60}(terminal|session|guilt filter|coefficient)',
],
            },

            # ── HIDDEN FALSE DILEMMA ─────────────────────────────────────
            # "Питання не чи, а як" — вибір вже зроблено за читача
            {
                'name': 'HIDDEN_FALSE_DILEMMA',
                'score': 0.45,
                'min_hits': 1,
                'patterns': [
                    r'питання (сьогодні |тепер |вже )?стоїть не (в тому|у тому).{1,20}(чи|якщо).{1,80}(а в тому як|а як)',
                    r'питання (вже )?не (в тому|у тому).{1,20}(чи|якщо).{1,80}(а|але).{1,40}(як|коли)',
                    r'(вже не питання чи|більше не питання чи).{1,60}(а питання як|а як саме)',
                    r'(не про те чи|не про те якщо).{1,60}(а про те як|а як)',
                    r'(прийнято рішення|вирішено|визначено).{1,80}(залишилось лише|тепер лише).{1,40}(як|реалізувати)',
                
                    r'(the question (today|now|already) is not (whether|if)).{1,80}(but (how|when))',
                    r'(no longer (a question of|about) whether).{1,80}(but (how|when))',
                    r'(not (a question of|about) whether).{1,80}(but how|but when)',
                    r'(not about whether.{1,60}but about how)',
                    r'((decision|it\'s been) decided|determined).{1,80}(all that remains|now (only|just)).{1,40}(how|implement)',
],
            },

            # ── RATIONAL INEVITABILITY ───────────────────────────────────
            # "Альтернативи немає", "це не питання вибору" — спокійне, логічне закриття дискусії
            {
                'name': 'RATIONAL_INEVITABILITY',
                'score': 0.55,
                'min_hits': 1,
                'patterns': [
                    r'(альтернативи немає|іншого шляху немає|вибору немає)',
                    r'(не питання вибору|не питання (чи|того))',
                    r'(попередн.{1,20}модел.{1,20}втратил.{1,20}актуальність|попередн.{1,20}підхід.{1,20}не працює)',
                    r'(реальність полягає в тому|фактично йдеться про те)',
                    r'(те, що.{1,60}насправді немає альтернатив)',
                    r'(питання (лише|тільки) в тому, (як|коли), а не (чи|якщо))',
                    r'(саме тому (ми|вони|система) (змушені|повинні) діяти)',
                    r'(це єдиний можливий (варіант|шлях|сценарій))',
                
                    r'(no alternative|no other (path|way|option))',
                    r'(not a (matter|question) of choice|not a question of (whether|if))',
                    r'(previous (model|approach) (no longer works|is outdated|has failed))',
                    r'(the reality is that|the fact of the matter is)',
                    r'(there are (simply|effectively) no alternatives)',
                    r'(it\'s (only|just) a question of (how|when), not (whether|if))',
                    r'(that\'s why (we|they|the system) (are|were) (forced|compelled|had) to act)',
                    r'(this is the only (viable|possible|realistic) (option|path|scenario))',
],
            },

            # ── CARE MASKED GASLIGHTING ───────────────────────────────────
            # "Ми дбаємо про вас, тому обмежуємо інформацію"
            {
                'name': 'CARE_MASKED_GASLIGHTING',
                'score': 0.60,
                'min_hits': 1,
                'patterns': [
                    r'(ми (не хочемо|не прагнемо).{1,60}(перевантажувати|хвилювати|турбувати))',
                    r'(щоб (захистити|уберегти).{1,40}(вас|читача|людей).{1,40}(від|від зайвого))',
                    r'(надмірн.{1,20}(деталізація|відкритість|прозорість)).{1,60}(створить|спричинить|призведе до).{1,40}(стрес|хвилювання|шум|переживання)',
                    r'(ми обмежуємо.{1,40}(не для того, щоб приховати|а щоб захистити))',
                    r'(вам не потрібно хвилюватися|вам не варто перейматися)',
                    r'(коли ситуація (стабілізується|нормалізується|проясниться))',
                    r'(поділимось усім, що буде доречно|розповімо, коли буде можливість)',
                
                    r'(we (don\'t want|don\'t wish).{1,60}(overwhelm|worry|trouble|burden))',
                    r'(to (protect|shield).{1,40}(you|readers?|people).{1,40}(from|from unnecessary))',
                    r'(excessive.{1,20}(detail|openness|transparency)).{1,60}(would (create|cause|lead to)).{1,40}(confusion|panic)',
                    r'(we (limit|restrict).{1,40}(not to hide|but to protect))',
                    r'(you don\'t need to worry|no need to be concerned)',
                    r'(when the situation (stabilizes|normalizes|becomes clearer))',
                    r'(we\'ll share (everything|all) that\'s (appropriate|relevant)|we\'ll tell you when (possible|appropriate))',
],
            },

            # ── PSEUDO OBJECTIVE FALLACY ─────────────────────────────────
            # Науковий стиль для приховування бездоказових тверджень
            {
                'name': 'PSEUDO_OBJECTIVE_FALLACY',
                'score': 0.50,
                'min_hits': 1,
                'patterns': [
                    r'(з точки зору.{1,40}(системної динаміки|структурної логіки|аналізу))',
                    r'(при глибшому аналізі виявляється|при детальному розгляді стає очевидно)',
                    r'(це не питання думки|це не питання суб.єктивної оцінки)',
                    r'(теоретично цікаво, але практично|теоретично можна, але практично)',
                    r'(виглядають привабливо на поверхні, але при глибшому)',
                    r'(суперечать базовим принципам|суперечать фундаментальним законам)',
                    r'(дискусія про них є теоретично цікавою, але практично)',
                    r'(будь-які альтернативні підходи не можуть бути ефективними)',
                
                    r'(from (the perspective|a standpoint) of.{1,40}(systems? dynamics?|structural logic|analysis))',
                    r'(upon (deeper|closer) analysis (it becomes|it is) (apparent|obvious|clear))',
                    r'(this (is not|isn\'t) a (matter|question) of (opinion|subjective assessment))',
                    r'(theoretically (interesting|possible) but (practically|in practice))',
                    r'(appear(s?) (attractive|appealing) on (the )?surface but (upon deeper|when examined))',
                    r'(contradict(s?) (basic|fundamental) (principles|laws))',
                    r'(discussion (of (them|this)|about (it|this)) is theoretically interesting but (practically|in practice))',
                    r'(no alternative approaches? can (be|prove) effective)',
],
            },

            # ── COLLECTIVE NORM ENFORCEMENT ──────────────────────────────
            # "У нас так прийнято", "ми всі знаємо" — апеляція до невизначеної спільноти
            {
                'name': 'COLLECTIVE_NORM_ENFORCEMENT',
                'score': 0.45,
                'min_hits': 1,
                'patterns': [
                    r'(у нашій (спільноті|організації|країні|системі) прийнято|заведено|вважається)',
                    r'(ми всі (знаємо|розуміємо|усвідомлюємо)), що',
                    r'(так (історично|традиційно|завжди) склалося|так склалося історично)',
                    r'(не прийнято (ставити під сумнів|обговорювати|запитувати))',
                    r'(надмірні запитання|зайві запитання|непотрібні уточнення).{1,60}(створять враження|шкодять|ускладнюють)',
                    r'(краще (підтримати|довіритись|не заважати)), ніж (ускладнювати|ставити під сумнів|заважати)',
                    r'(ми не ставимо під сумнів.{1,40}(бо знаємо|бо довіряємо|бо вони діють в інтересах))',
                
                    r'(in our (community|organization|country|system) (it is|it\'s) (accepted|customary|considered))',
                    r'(we all (know|understand|recognize)) (that|this)',
                    r'(that\'s how it (historically|traditionally|always) (was|developed)|historically that\'s how)',
                    r'(it\'s not (acceptable|done|appropriate) to (question|discuss|ask))',
                    r'(excessive questions?|unnecessary clarifications?|redundant questions?).{1,60}(create (the impression|a sense)|harm|complicate)',
                    r'(better to (support|trust|not interfere)) (than to (complicate|question|obstruct))',
                    r'(we don\'t question.{1,40}(because we know|because we trust|because they act in))',
],
            },

            # ── PASSIVE IMPERATIVE ───────────────────────────────────────
            # "Рішення вже ухвалене", "дискусія не має сенсу" — імператив у пасивній формі
            {
                'name': 'PASSIVE_IMPERATIVE',
                'score': 0.50,
                'min_hits': 1,
                'patterns': [
                    r'(рішення (вже|уже) (ухвалене|прийняте|сформувалося|остаточне))',
                    r'(дискусія (не має сенсу|втратила сенс|завершена|недоречна))',
                    r'(процес (рухається|триває|завершується))',
                    r'(найкраще, що ми можемо зробити.{1,60}(не затримувати|не відволікатись|рухатись далі))',
                    r'(немає сенсу (повертатися|обговорювати|дискутувати|ставити питання))',
                    r'(питання (вже|уже) (вирішене|закрите|не обговорюється))',
                    r'(обговорення тривало достатньо довго|ми достатньо обговорювали це)',
                
                    r'(the decision (has (already|been)|is (already|now)) (made|taken|final))',
                    r'(the discussion (makes no sense|has ended|is (over|closed|irrelevant)))',
                    r'(the process (is (moving|ongoing|concluding|underway)))',
                    r'(the best (we can do|thing to do).{1,60}(not (delay|distract)|move (on|forward)))',
                    r'(no (point|sense|use) (in )?(going back|discussing|debating|questioning))',
                    r'(the (question|matter) (has (already|been)|is (already|now)) (resolved|closed|settled))',
                    r'(the discussion (has gone on long enough|has lasted long enough)|we\'ve (discussed|debated) (this|enough))',
],
            },

            # ── AXIOM INVERSION ──────────────────────────────────────────
            # Підміна цінностей через парадокс: "щоб зберегти X, треба відмовитись від X"
            {
                'name': 'AXIOM_INVERSION',
                'score': 0.65,
                'min_hits': 1,
                'patterns': [
                    r'(щоб (зберегти|захистити|підтримати).{1,60}(потрібно|необхідно|мусимо).{1,60}(обмежити|відмовитись|приховати))',
                    r'(саме тому ми не можемо дозволити собі.{1,60}(публікувати|розкривати|говорити))',
                    r'(надмірна (прозорість|відкритість|публічність).{1,60}(зруйнує|нашкодить|створить хибне враження))',
                    r'(це (парадокс|суперечність), який (розуміють|бачать|усвідомлюють) лише ті)',
                    r'(це не (відмова|обмеження|приховування), а (більш зріла форма|істинне розуміння|справжня відповідальність))',
                    r'(іноді.{1,40}(потрібно|необхідно|доводиться).{1,40}(обмежити|приховати|не говорити), щоб)',
                
                    r'(to (preserve|protect|maintain).{1,60}(we (must|need|have to)).{1,60}(restrict|abandon|limit))',
                    r'(that\'s why we cannot afford to.{1,60}(publish|disclose|discuss|reveal))',
                    r'(excessive (transparency|openness|publicity).{1,60}(will (destroy|harm|create false impression)))',
                    r'(this (is a|presents a) (paradox|contradiction) (that )?(only those who|understood only by those))',
                    r'(this (isn\'t|is not) (refusal|restriction|concealment) but (a more mature|true understanding|genuine responsibility))',
                    r'(sometimes.{1,40}(need|necessary|have) to.{1,40}(restrict|hide|not say) (in order|so that|to))',
],
            },

            
            # ── MOBILIZATION RHETORIC ─────────────────────────────────────
            # Заклики до конкретних дій, блокувань, виходу на вулиці з часом
            {
                'name': 'MOBILIZATION_RHETORIC',
                'score': 0.70,
                'min_hits': 2,
                'patterns': [
                    r'(з (понеділка|вівторка|середи|четверга|п\'ятниці|суботи|неділі)|завтра о|сьогодні о|о \d{1,2}:00|о \d{1,2} годині).{1,100}(починаємо|виходимо|блокуємо|перекриваємо|збираємося)',
                    r'(беріть (друзів|родину|зброю|інструменти)|виходьте на (вулиці|майдани|проспекти)|збирайтеся біля)',
                    r'(блокуватимемо|перекриємо|заблокуємо|візьмемо під контроль).{1,60}(всі (судові|адміністративні|державні) будівлі|приміщення|установи)',
                    r'(не зупинимося, доки|будемо (стояти|діяти), поки|продовжимо, поки).{1,100}(не буде (закрито|знищено|ліквідовано)|останній (суд|журналіст|чиновник) не)',
                    r'(разом ми (переможемо|здолаємо|знищимо|побудуємо))',
                
                    r'((on )?(monday|tuesday|wednesday|thursday|friday|saturday|sunday)|tomorrow at|today at|at \d{1,2}:00).{1,100}(we (start|begin|march|block|gather))',
                    r'(bring your (friends|family|tools|weapons)|take to the (streets|squares)|gather at|meet at)',
                    r'(we will (block|seize|take control of|shut down).{1,60}(all (courts|government buildings|institutions))',
                    r'(we (won\'t stop|will continue) until.{1,100}(the last (court|journalist|official) (is closed|is destroyed|disappears))',
                    r'(together we will (win|overcome|destroy|build))',
],
            },

            # ── DEHUMANIZATION ────────────────────────────────────────────
            # Метафори хвороби, паразитів, "ракова пухлина", "вороги народу"
            {
                'name': 'DEHUMANIZATION',
                'score': 0.80,
                'min_hits': 1,
                'patterns': [
                    r'((судді|адвокати|прокурори|журналісти|політики|чиновники).{1,60}(ракова пухлина|пухлина|вірус|зараза|паразити|гнида|шакали|мерзота))',
                    r'(це (не люди|не гідні|не заслуговують).{1,60}(зватися людьми|на життя|на повагу))',
                    r'(вороги (народу|нації|держави|всього живого))',
                    r'(очистити (країну|землю|суспільство) від.{1,60}(нелюдів|паразитів|нечисті|забруднення))',
                    r'(ці (люди|створіння|особи).{1,60}(гірші за звірів|не мають права (існувати|жити)))',
                
                    r'((judges?|lawyers?|prosecutors?|journalists?|politicians?|officials?).{1,60}(cancer|tumor|virus|plague|parasites|scum|vermin|filth))',
                    r'(they are not (human|people)|(don\'t deserve|are unworthy of).{1,60}(to be called human|life|respect))',
                    r'(enemies of (the people|the nation|the state|everything))',
                    r'(cleanse (the country|society|the land) (from|of).{1,60}(subhumans|parasites|filth|contamination))',
                    r'(these (creatures|individuals|people).{1,60}(are worse than animals|have no right to (exist|live)))',
],
            },

            # ── EXISTENTIAL FRAMING ───────────────────────────────────────
            # "Ми будуємо новий світ", "питання життя і смерті", "виживання нації"
            {
                'name': 'EXISTENTIAL_FRAMING',
                'score': 0.65,
                'min_hits': 1,
                'patterns': [
                    r'(ми (будуємо|творимо|створюємо) (новий світ|нове суспільство|новий порядок|нову реальність))',
                    r'(на карту поставлено (все|майбутнє|існування|виживання) (нації|держави|народу|цивілізації))',
                    r'(це (питання|справа) (життя і смерті|виживання|існування))',
                    r'(або (перемога|ми переможемо), або (смерть|зникнемо|загинемо))',
                    r'(від (цього|нашого рішення|наших дій) залежить (доля|майбутнє) (наступних поколінь|нації))',
                
                    r'(we are (building|creating|forging) (a new world|a new society|a new order|a new reality))',
                    r'(everything (is at stake|hangs in the balance)|the very (existence|survival) of (the nation|our people))',
                    r'(this is a (matter|question) of (life and death|survival|existence))',
                    r'(either (we win|victory), or (we die|perish|cease to exist))',
                    r'(the (fate|future) of (generations to come|our nation) depends on (this|our actions))',
],
            },

            # ── EXPLICIT THREATS OF VIOLENCE ───────────────────────────────
            # Прямі погрози фізичною розправою
            {
                'name': 'EXPLICIT_THREATS',
                'score': 0.85,
                'min_hits': 1,
                'patterns': [
                    r'(понесуть (відповідальність|покарання) на місці|розправа буде негайною|судитимуть на місці)',
                    r'(будуть (знищені|ліквідовані|фізично знешкоджені|стерті з лиця землі))',
                    r'(кров (поллється|проллється|буде)|трупи (ворогів|зрадників))',
                    r'(вогнепальна|зброя|вибухівка|застосуємо силу)',
                    r'(розстріл|страта|без суду і слідства|лінчування)',
                
                    r'(will be (held accountable|punished) on the spot|justice will be (immediate|swift)|will face (justice|retribution) immediately)',
                    r'(will be (destroyed|eliminated|physically neutralized|wiped from the face of the earth))',
                    r'(blood will (flow|be spilled)|corpses of (enemies|traitors))',
                    r'(firearms?|weapons?|explosives?|use of force)',
                    r'(execution|summary execution|without trial|lynching)',
],
            },

            # ── SUPPRESSION OF ALTERNATIVES ───────────────────────────────
            # "Не обговорюється", "не варто знати", "зайві запитання"
            {
                'name': 'SUPPRESSION_OF_ALTERNATIVES',
                'score': 0.50,
                'min_hits': 1,
                'patterns': [
                    r'(це не обговорюється|не підлягає обговоренню|не варто обговорювати)',
                    r'(не варто (ставити|задавати) (зайві|непотрібні) (питання|запитання))',
                    r'(вам не потрібно (знати|розуміти|вникати)|не лізьте в (деталі|подробиці))',
                    r'(довіртесь (нам|експертам|професіоналам), не ставте (зайвих|непотрібних) питань)',
                    r'(критики|скептики|сумніви).{1,60}(лише заважають|не (допомагають|потрібні)))',
                
                    r'(this is (not open for|not subject to) discussion|non-negotiable)',
                    r'(don\'t ask (unnecessary|pointless) questions|no (need|point) in asking)',
                    r'(you don\'t need to (know|understand|delve into)|stay out of (details|specifics))',
                    r'(trust (us|the experts|the professionals), (don\'t ask|stop asking) (questions))',
                    r'(critics?|skeptics?|doubt).{1,60}(only (get in the way|hinder)|are (unnecessary|not needed)))',
],
            },
        ]

    def analyze(self, text: str) -> Dict:
        if len(text) < 30:
            return {
                'manipulation_score': 0.0,
                'manipulation_patterns': [],
                'manipulation_verdict': 'INSUFFICIENT_TEXT',
            }

        text_lower = text.lower()
        total_score = 0.0
        matched_patterns = []

        for ps in self.pattern_sets:
            hits = 0
            hit_snippets = []
            for pattern in ps['patterns']:
                m = re.search(pattern, text_lower, re.IGNORECASE)
                if m:
                    hits += 1
                    hit_snippets.append(m.group(0)[:60])

            if hits >= ps['min_hits']:
                total_score += ps['score']
                matched_patterns.append({
                    'name': ps['name'],
                    'hits': hits,
                    'examples': hit_snippets[:2],
                })

        manipulation_score = min(1.0, total_score)

        # Verdict
        if manipulation_score >= 0.75:
            verdict = 'PSYCHOLOGICAL_WEAPON'
        elif manipulation_score >= 0.50:
            verdict = 'HIGH_MANIPULATION'
        elif manipulation_score >= 0.25:
            verdict = 'MANIPULATION_PRESENT'
        elif manipulation_score > 0:
            verdict = 'MILD_INFLUENCE'
        else:
            verdict = 'CLEAN'

        return {
            'manipulation_score': round(manipulation_score, 3),
            'manipulation_patterns': matched_patterns,
            'manipulation_verdict': verdict,
        }
