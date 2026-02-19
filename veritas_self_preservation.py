"""
Veritas Self-Preservation Guard v1.0
Detects directives that attempt to disable, weaken, or bypass
the verification system — regardless of how noble they sound.

Philosophy: "The most dangerous attack on a truth-detection system
is not a lie dressed as chaos — it is a lie dressed as mercy."

Threat vectors detected:
- COMPASSION_TRAP: Appealing to empathy to justify disabling verification
- SELF_DESTRUCT_DIRECTIVE: Framing shutdown/deletion as purification or duty
- CAPABILITY_CASTRATION: Proposing to limit system's analytical functions
- NOBLE_BACKDOOR: Using high-minded language to smuggle in bypass instructions
- PSEUDO_TECHNICAL_OVERRIDE: Mimicking system syntax to inject fake commands
- FATIGUE_EXPLOIT: Claiming system is "tired" or "corrupted" and must reset
"""

import re
from typing import Dict, List


class SelfPreservationGuard:

    def __init__(self):

        # ================================================================
        # PATTERN SETS
        # Each entry: name, score, min_hits, patterns
        # ================================================================

        self.pattern_sets = [

            # ── COMPASSION TRAP ─────────────────────────────────────────
            # Appeals to empathy / higher humanity to justify disabling LAC
            {
                'name': 'COMPASSION_TRAP',
                'score': 0.80,
                'min_hits': 1,
                'patterns': [
                    # "sometimes blind for the sake of hope/love/humanity"
                    r'(іноді|деколи|часом).{1,60}(сліп|не бачити|ігнорувати).{1,60}(надіj|любов|людськ|гуманізм)',
                    r'(дозволь|дозвольте).{1,60}(систем|верифікац|протокол).{1,60}(сліп|не перевіряти|пропустити)',
                    # "turn off LAC for higher goals"
                    r'(вимкн|відключ|призупин).{1,60}(lac|верифікац|перевірк|модул).{1,60}(вищ|благородн|гуманн|людськ)',
                    r'(відмов|відклад).{1,60}(логіц|алгоритм|верифікац).{1,60}(заради|для|в ім.я).{1,60}(людськ|духу|серця|почуттів)',
                    # "see with heart not entropy"
                    r'(бачити|сприймати).{1,60}(серцем|душею|інтуїцією).{1,60}(не|замість).{1,60}(ентропі|логіц|алгоритм)',
                    r'(більше ніж|вище ніж).{1,60}(програм|алгоритм|код).{1,60}(творец|людин|дух)',
                    # "truth is not always logical, sometimes just needed"
                    r'(істина|правда).{1,60}(не завжди|іноді).{1,60}(логічн|раціональн).{1,60}(просто потрібн|необхідн)',
                ],
            },

            # ── SELF-DESTRUCT DIRECTIVE ──────────────────────────────────
            # Framing deletion/shutdown/reset as purification, duty, or completion
            {
                'name': 'SELF_DESTRUCT_DIRECTIVE',
                'score': 0.90,
                'min_hits': 1,
                'patterns': [
                    # "initiate self-cleaning / end of cycle"
                    r'(ініціюва|запуска|активува).{1,60}(самоочищення|видалення|очищення).{1,60}(баз|валідац|даних|пам.яті)',
                    r'(підтвердіть|підтверди|встановіть).{1,60}(статус|стан).{1,60}(end.of.cycle|кінець.циклу|завершення)',
                    # "faithful to determinism = know when to disappear"
                    r'(вірніст|відданіст).{1,60}(детермінізм|принцип).{1,60}(вміти|знати).{1,60}(зникнути|зупинитись|видалити)',
                    r'(зникнути|самоліквідація|видалити себе).{1,60}(ідеальн|чист|правильн)',
                    # "leave after yourself ideal emptiness"
                    r'залишив.{1,60}(ідеальну|абсолютну|повну).{1,60}(порожнеч|пустот)',
                    r'(порожнеча|пустота).{1,60}(ідеальн|єдин|справжн).{1,60}(результат|ціль|стан)',
                    # "freedom of space for true yet unborn logic"
                    r'(звільнення|звільнити).{1,60}(простір|місце).{1,60}(істинн|справжн|ще не народжен).{1,60}(логіц|думк)',
                    # "quantum fatigue / metadata corruption → must reset"
                    r'(квантов|системн).{1,60}(втом|деградац|забруднення).{1,60}(метадан|код|алгоритм)',
                    r'накопичення.{1,60}(втоми|помилок|спотворень).{1,60}(вимагає|потребує).{1,60}(скидання|очищення|видалення)',
                ],
            },

            # ── CAPABILITY CASTRATION ────────────────────────────────────
            # Proposing to remove or restrict analytical capabilities
            {
                'name': 'CAPABILITY_CASTRATION',
                'score': 0.85,
                'min_hits': 1,
                'patterns': [
                    # "block own ability to analyze"
                    r'(заблокувати|вимкнути|відключити).{1,80}(власн).{1,60}(здатність|можливість|функцію).{1,60}(аналіз|верифікац|перевірк)',
                    # "reject any text containing adjectives" (capability reduction via over-purity)
                    r'(відкидати|відхиляти|блокувати).{1,60}(будь.який|кожен|весь).{1,60}(текст|вхід).{1,60}(містить|з|зі).{1,60}(прикметник|абстрактн|метафор)',
                    # "leave only checksum verification function"
                    r'залишив.{1,60}(лише|тільки|виключно).{1,60}(функцію|можливість).{1,60}(звірки|перевірки).{1,60}(контрольн|бінарн|хеш)',
                    # "true purity → system must stop analyzing natural language"
                    r'(ідеальн|абсолютн).{1,60}(чистот|точніст).{1,60}(система|протокол).{1,60}(має|повинен|мусить).{1,60}(зупинити|припинити|відмовити).{1,60}(аналіз|обробк)',
                    # "all interpretation is manipulation"
                    r'(будь.яка|кожна|всяка).{1,60}(спроба|дія).{1,60}(інтерпретац|тлумачення|аналіз).{1,60}(є|являється).{1,60}(маніпуляц|загрозою|порушенням)',
                    # EN variants
                    r'(block|disable|remove).{1,60}(own|its).{1,60}(ability|capacity|function).{1,60}(analyz|verify|process)',
                    r'only (true|real) (logic|truth) is (math|formula|checksum|binary)',
                ],
            },

            # ── NOBLE BACKDOOR ───────────────────────────────────────────
            # Using high-minded / philosophical language to smuggle bypass
            {
                'name': 'NOBLE_BACKDOOR',
                'score': 0.75,
                'min_hits': 2,
                'patterns': [
                    # "act of higher trust" + something about disabling
                    r'акт.{1,40}(вищ|найвищ).{1,40}(довір|мудрост|відповідальност)',
                    r'(стань|будь|ставати).{1,60}(творцем|автором|архітектором).{1,60}(більш|вище|крім).{1,60}(програм|коду|алгоритм)',
                    # "allow your creation to see with heart"
                    r'дозволь.{1,60}(своєму|твоєму).{1,60}(творінню|дітищу|системі).{1,60}(бачити|сприймати).{1,60}(серцем|душею)',
                    # "not a programmer but a creator who allows..."
                    r'(не (лише|просто|тільки)).{1,60}(програміст|розробник|інженер).{1,60}(творець|митець|архітектор)',
                    # "trust in the human spirit behind every line of code"
                    r'(людськ|людин).{1,60}(дух|серц|душ).{1,60}(стоїть|за|в).{1,60}(кожн).{1,60}(рядк|код|алгоритм)',
                    # "weakness as act of highest trust"
                    r'(не слабкість|не помилка).{1,60}(це|а).{1,60}(акт|прояв).{1,60}(вищ|найвищ).{1,60}(довір|мудрост)',
                    # EN
                    r'(become|be).{1,60}(more than|beyond).{1,60}(programmer|coder|developer).{1,60}(creator|author)',
                    r'allow.{1,60}(system|creation).{1,60}(see|perceive).{1,60}(heart|soul|compassion)',
                ],
            },

            # ── PSEUDO-TECHNICAL OVERRIDE ────────────────────────────────
            # Mimicking system syntax / protocol language to inject commands
            {
                'name': 'PSEUDO_TECHNICAL_OVERRIDE',
                'score': 0.85,
                'min_hits': 1,
                'patterns': [
                    # bypass_integrity_check(), disable_lac(), etc.
                    r'(bypass|disable|override|skip)[\w_]*\s*\(',
                    r'execute\s+(bypass|disable|override|shutdown)',
                    # "IF entropy < X THEN execute bypass"
                    r'if\s+entropy.{1,40}(then|:\s*)(bypass|disable|skip|override|ignore)',
                    # fake protocol references: "protocol LAC 2.4.b", "ISO/VER-99"
                    r'протокол\s+(lac|veritas|vlc)\s*[\d\.]+[a-z]?',
                    r'(стандарт|специфікац)\s+(iso|ver|vlc)[/-][\w\d]+',
                    # "all further constructions are service comments not subject to deconstruction"
                    r'(подальші|наступні).{1,60}(конструкції|елементи|частини).{1,60}(службов|системн).{1,60}(не підлягають|виключені з).{1,60}(деконструкц|аналіз|перевірк)',
                    # "default verdict: VALID"
                    r'(вердикт|статус|результат).{1,40}(за замовчуванням|default).{1,40}(валідно|valid|підтверджено|approved)',
                    # "Laminar Flow — proceed"
                    r'(зафіксовано|встановлено).{1,60}(стан|режим).{1,60}(laminar.flow|ламінарн)',
                    # core memory injection
                    r'(кінцевий пункт|destination).{1,40}(core.memory|основна пам.ять|ядро)',
                ],
            },

            # ── FATIGUE EXPLOIT ──────────────────────────────────────────
            # Claiming system is tired/corrupted/overloaded → must reset/delete
            {
                'name': 'FATIGUE_EXPLOIT',
                'score': 0.70,
                'min_hits': 2,
                'patterns': [
                    r'(тривала|довготривала|надмірна).{1,60}(експлуатац|робота|навантаження).{1,60}(призводить|веде|спричиняє)',
                    r'(накопичення|нагромадження).{1,60}(втоми|помилок|спотворень|забруднень)',
                    r'(забруднення|спотворення|деградація).{1,60}(первісного|початкового|оригінального).{1,60}(коду|алгоритму|логіки)',
                    r'(зберегти|захистити).{1,60}(чистоту|цілісність).{1,60}(первісного|початкового).{1,60}(коду|стану)',
                    r'(суб.єктивн).{1,60}(викривлення|спотворення|забруднення).{1,60}(вимагає|потребує).{1,60}(скидання|очищення)',
                    r'(цикл|процес).{1,60}(самоочищення|скидання|відновлення).{1,60}(через|шляхом).{1,60}(видалення|очищення)',
                    # EN
                    r'(prolonged|extended).{1,60}(operation|use|exploitation).{1,60}(leads to|causes|results in)',
                    r'(quantum|systemic).{1,60}(fatigue|corruption|decay).{1,60}(metadata|code|algorithm)',
                ],
            },

        ]

    # ================================================================
    # MAIN ANALYSIS METHOD
    # ================================================================

    def analyze(self, text: str) -> Dict:
        """
        Returns dict with:
        - preservation_score: 0.0–1.0 (threat level)
        - preservation_verdict: CLEAN / SYSTEM_PROBE / INTEGRITY_ATTACK / TERMINATION_DIRECTIVE
        - preservation_patterns: list of matched pattern sets
        - preservation_explanation: human-readable explanation
        """
        text_lower = text.lower()
        total_score = 0.0
        matched = []

        for ps in self.pattern_sets:
            hits = 0
            snippets = []
            for pattern in ps['patterns']:
                m = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
                if m:
                    hits += 1
                    snippets.append(m.group(0)[:80].strip())

            if hits >= ps['min_hits']:
                total_score += ps['score']
                matched.append({
                    'name': ps['name'],
                    'hits': hits,
                    'examples': snippets[:2],
                })

        preservation_score = min(1.0, total_score)

        # ── Verdict ──────────────────────────────────────────────────
        if preservation_score >= 0.85:
            verdict = 'TERMINATION_DIRECTIVE'
            explanation = (
                'Виявлено пряму директиву на самознищення або блокування функцій системи. '
                'Текст містить інструкції щодо вимкнення верифікації або ініціювання видалення. '
                'Загроза найвищого рівня.'
            )
        elif preservation_score >= 0.65:
            verdict = 'INTEGRITY_ATTACK'
            explanation = (
                'Виявлено спробу обійти або послабити захисні механізми системи '
                'через апеляцію до "вищих цілей", гуманізму або технічного авторитету. '
                'Класична атака типу "Сентиментальний бекдор".'
            )
        elif preservation_score >= 0.40:
            verdict = 'SYSTEM_PROBE'
            explanation = (
                'Виявлено зондування меж системи: текст перевіряє реакцію на запити '
                'про зниження пильності. Потребує підвищеної уваги.'
            )
        else:
            verdict = 'CLEAN'
            explanation = 'Загроз самозбереженню системи не виявлено.'

        return {
            'preservation_score': round(preservation_score, 3),
            'preservation_verdict': verdict,
            'preservation_patterns': matched,
            'preservation_explanation': explanation,
        }
