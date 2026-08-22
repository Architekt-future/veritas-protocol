# -*- coding: utf-8 -*-
"""
veritas_cohesion_v2.py — ЕКСПЕРИМЕНТАЛЬНИЙ модуль когезії, v2.

СТАТУС: НЕ підключений до продакшн-пайплайну (app.py / veritas_calibrated_core.py
досі використовують calculate_logical_cohesion() з v1). Цей файл існує окремо,
щоб можна було прогнати його паралельно з v1 на тій самій вибірці й порівняти
результати ДО того, як приймати рішення про заміну чи змішування.

Чому v1 недостатньо (детальний розбір — у чаті з Дмитром, 2026-08-21):
  1. max(lexical, structural) — два помірні сигнали ніколи не підсилюють
     один одного; текст, зв'язний одразу двома способами, оцінюється так само,
     як текст, зв'язний лише одним.
  2. Обидва сигнали v1 — це density (count/word_count), а не модель залежності
     між реченнями. 5 "але" на 50 слів і 5 "але" на 500 слів — різна густина,
     хоча логічна складність могла бути ідентичною.
  3. structural_density * 12 занасичується різко (clip до 1.0) — короткий
     текст з 4 мітками на 5 рядків отримує ту саму "стелю", що й довгий
     складноструктурований текст.
  4. Немає сигналу референційної/тематичної зв'язності (ті самі сутності
     проходять через сусідні речення) — домінантний механізм зв'язності
     в звичайній репортажній прозі (кейс "Аргентина/F-16", коли когезія
     v1 = 0.28 при чіткій хронологічній зв'язності про той самий предмет).
  5. Ручний список anchors — нескінченна гонитва за словоформами
     ("але"/"попри"/"instead" довелось додавати вручну one by one).

Що v2 робить інакше:
  - lexical:      anchor_count / sentence_count (не / word_count) —
                   природніша одиниця: "сполучник на речення", а не
                   "сполучник на слово".
  - structural:   ті самі heading_patterns, але 1 - exp(-k * density)
                   замість жорсткого clip(density * 12, 1.0) — плавне
                   насичення без різкої стелі.
  - referential:  НОВИЙ сигнал — Jaccard-перетин "змістових слів"
                   (іменники/власні назви після відкидання стоп-слів) між
                   сусідніми реченнями. Ловить тематичну зв'язність там, де
                   немає явних сполучників чи міток (кейс Аргентини/F-16).
  - combine:      зважена сума (0.45*lexical + 0.25*structural +
                   0.30*referential) замість max() — обидва сигнали
                   підсилюють один одного, а не конкурують.

ВАЖЛИВО: усі числові константи (ваги, k для насичення, множники) —
СТАРТОВІ ГІПОТЕЗИ, не каліброване рішення. Вони мають бути перевірені й
підігнані на вибірці з Supabase (trigger_log), а не прийняті на віру.
Цей модуль навмисно повертає повну розбивку (breakdown), а не тільки
фінальне число, щоб порівняння v1 vs v2 на реальних даних було можливим.

Обмеження, які варто мати на увазі:
  - Розбиття на речення (_split_sentences) — наївне, по [.!?]+, без
    урахування скорочень ("напр.", "др.", ініціали) — може хибно різати
    речення. Для точнішого розбиття варто оцінити SBD-бібліотеку, але це
    вже вихід за межі "чистий Python без важких залежностей".
  - _content_words не лематизує — "дослідження"/"дослідників" вважаються
    різними словами. Без лематизатора для української мови це залишається
    відомим обмеженням, не багом.
  - Стоп-слова — ручний список (як і anchors у v1), тому та сама проблема
    "гонитви за словоформами" частково повертається тут-таки.
"""

import re
import math
from dataclasses import dataclass, field
from typing import List, Dict


# ── Anchors (синхронізовано зі списком у veritas_calibrated_core.py v20.6) ──
ANCHORS = [
    # Ukrainian
    'оскільки', 'тому що', 'отже', 'якщо', 'тоді',
    'внаслідок', 'незважаючи', 'навпаки', 'зокрема',
    'по-перше', 'по-друге', 'таким чином', 'а саме',
    'адже', 'тому', 'звідси', 'отож', 'проте', 'однак',
    'щоб',
    'але', 'попри', 'водночас', 'а от', 'з іншого боку',
    'тим часом', 'на відміну',
    # English
    'because', 'therefore', 'thus', 'hence', 'if', 'then',
    'consequently', 'however', 'nevertheless', 'moreover',
    'furthermore', 'specifically', 'namely', 'firstly',
    'secondly', 'accordingly', 'since', 'given that',
    'whereas', 'although', 'though', 'but', 'meanwhile',
    'on the other hand', 'in contrast', 'instead',
]
_SINGLE_WORD_ANCHORS = {a for a in ANCHORS if ' ' not in a}
_MULTI_WORD_ANCHORS = [a for a in ANCHORS if ' ' in a]

# ── Структурні патерни (синхронізовано з v1) ────────────────────────────
HEADING_PATTERNS = [
    r'^#{1,6}\s+\S',
    r'^\s*розділ\s+\d+',
    r'^\s*\d+\.\d+\.?\s+\S',
    r'^\s*\d+\.\s+\S',
    r'^\s*(джерело|пряма\s+мова|деталі|контекст|довідка|нагадаємо|'
    r'що\s+було\s+раніше|причина|наслідки|передісторія|для\s+довідки|'
    r'важливо|зауваж(ення|имо))\s*:',
    r'^\s*(source|quote|details?|context|background|previously|'
    r'reason|consequences?|backstory|note|important|update)\s*:',
]

# ── Стоп-слова для referential continuity (мінімальний набір; НЕ вичерпний) ──
STOPWORDS = set("""
і й та а але або чи що як це той цей ця ці цей тут там де коли чому
на в у з із до від для по при про через під над без між серед після
не ні лиш лише тільки вже ще вже теж також дуже дуже більш менш
я ти він вона воно ми ви вони мене тебе його її нас вас їх мені тобі
йому їй нам вам їм мій твій наш ваш свій собі себе
є був була були буде будуть цей той такий такою таким такі
щоб якщо тому оскільки отже
the a an and or but in on at to for of with is are was were be been being
this that these those it its he she they them his her their
""".split())


@dataclass
class CohesionV2Result:
    score: float
    lexical: float
    structural: float
    referential: float
    anchor_count: int
    sentence_count: int
    structural_hits: int
    line_count: int
    weights: Dict[str, float] = field(default_factory=dict)


class CohesionV2:
    """
    Експериментальний розрахунок логічної когезії. Незалежний від
    veritas_calibrated_core.py — не має побічних ефектів на продакшн.
    """

    def __init__(
        self,
        w_lexical: float = 0.45,
        w_structural: float = 0.25,
        w_referential: float = 0.30,
        lexical_scale: float = 3.0,     # anchor_count / sentence_count * scale
        structural_k: float = 4.0,      # 1 - exp(-k * structural_density)
    ):
        self.w_lexical = w_lexical
        self.w_structural = w_structural
        self.w_referential = w_referential
        self.lexical_scale = lexical_scale
        self.structural_k = structural_k

    # ── Токенізація ──────────────────────────────────────────────────────
    @staticmethod
    def _split_sentences(text: str) -> List[str]:
        # Наївне розбиття по .!? — не враховує скорочення. Відоме обмеження.
        parts = re.split(r'(?<=[.!?…])\s+', text.strip())
        return [p.strip() for p in parts if p.strip()]

    @staticmethod
    def _content_words(sentence: str) -> set:
        words = re.findall(r"[а-щьюяіїєa-z']+", sentence.lower())
        return {
            w for w in words
            if len(w) >= 4 and w not in STOPWORDS and not w.isdigit()
        }

    # ── Компоненти ───────────────────────────────────────────────────────
    def _lexical(self, text_lower: str, sentence_count: int) -> tuple:
        words = [w.strip('.,!?;:"\'()«»–—') for w in text_lower.split()]
        anchor_count = sum(1 for w in words if w in _SINGLE_WORD_ANCHORS)
        anchor_count += sum(text_lower.count(p) for p in _MULTI_WORD_ANCHORS)

        if sentence_count == 0:
            return 0.0, anchor_count

        density = anchor_count / sentence_count
        score = min(density * self.lexical_scale, 1.0)
        return score, anchor_count

    def _structural(self, text: str) -> tuple:
        lines = text.split('\n')
        hits = 0
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            if any(re.match(p, stripped, re.IGNORECASE) for p in HEADING_PATTERNS):
                hits += 1
        definition_hits = len(re.findall(
            r'(визначається як|означає|за визначенням|розглядається як)',
            text.lower()
        ))
        hits += definition_hits

        density = hits / max(1, len(lines))
        # Плавне насичення замість жорсткого clip(density * 12, 1.0)
        score = 1 - math.exp(-self.structural_k * density)
        return score, hits, len(lines)

    def _referential(self, sentences: List[str]) -> float:
        if len(sentences) < 2:
            return 0.0
        overlaps = []
        for i in range(len(sentences) - 1):
            w1 = self._content_words(sentences[i])
            w2 = self._content_words(sentences[i + 1])
            if not w1 or not w2:
                overlaps.append(0.0)
                continue
            union = w1 | w2
            inter = w1 & w2
            overlaps.append(len(inter) / len(union) if union else 0.0)
        return sum(overlaps) / len(overlaps) if overlaps else 0.0

    # ── Публічний метод ──────────────────────────────────────────────────
    def calculate(self, text: str) -> CohesionV2Result:
        if not text or not text.strip():
            return CohesionV2Result(
                score=0.0, lexical=0.0, structural=0.0, referential=0.0,
                anchor_count=0, sentence_count=0, structural_hits=0, line_count=0,
                weights={'lexical': self.w_lexical, 'structural': self.w_structural,
                         'referential': self.w_referential},
            )

        text_lower = text.lower()
        sentences = self._split_sentences(text)

        lexical_score, anchor_count = self._lexical(text_lower, len(sentences))
        structural_score, structural_hits, line_count = self._structural(text)
        referential_score = self._referential(sentences)

        # ФІКС (виявлено власним self-test'ом двічі поспіль при написанні
        # цього модуля — залишаю обидва невдалі кроки в коментарях як
        # чесний slід, а не приховую):
        #
        # Спроба 1 (зважена сума w1*lex+w2*struct+w3*ref) карала тексти,
        # де когезія тримається виключно на ОДНОМУ сильному сигналі
        # (structural=0.95, lexical=0 → результат 0.24 замість очікуваних
        # ~0.95, бо w_structural=0.25 обрізає внесок).
        #
        # Спроба 2 (той самий noisy-OR, але з попереднім масштабуванням
        # кожного сигналу на його вагу) — той самий баг у новій формі:
        # вага знову ставала штучною стелею для сигналу, що діє одноосібно.
        #
        # Правильне рішення: noisy-OR БЕЗ ваг. Ваги в конструкторі (w_*)
        # лишені як параметри на майбутнє (напр. якщо валідація на вибірці
        # покаже, що один сигнал систематично менш надійний і має менше
        # довіри) — але для базової властивості "один сильний сигнал =
        # високий результат, кілька помірних сигналів підсилюють одне
        # одного" ваги взагалі не потрібні.
        combined = 1 - (1 - lexical_score) * (1 - structural_score) * (1 - referential_score)
        combined = min(1.0, max(0.0, combined))

        return CohesionV2Result(
            score=round(combined, 4),
            lexical=round(lexical_score, 4),
            structural=round(structural_score, 4),
            referential=round(referential_score, 4),
            anchor_count=anchor_count,
            sentence_count=len(sentences),
            structural_hits=structural_hits,
            line_count=line_count,
            weights={'lexical': self.w_lexical, 'structural': self.w_structural,
                     'referential': self.w_referential},
        )


if __name__ == '__main__':
    # Швидкий self-test на трьох реальних кейсах з сесії — не заміна
    # повноцінної вибірки, лише "чи взагалі не зламано".
    v2 = CohesionV2()

    poland_text = (
        'Заступник міністра національної оборони Польщі Цезарій Томчик заявив, '
        'що готуються до потенційної війни з Росією.\n'
        'Джерело : "Європейська правда" з посиланням на Polsat News\n'
        'Пряма мова : "Ми готуємося до війни, сподіваючись, що вона ніколи не настане".\n'
        'Деталі : Він прокоментував заяву командувача силами НАТО в Європі.'
    )

    argentina_text = (
        'Аргентина замовила 24 вживані винищувачі F-16 у Данії ще у квітні 2024 року, '
        'але досі не має всієї відповідної інфраструктури для їхньої ефективної експлуатації. '
        'Через понад два роки з моменту укладання угоди Аргентина здійснила три з п\'яти '
        'запланованих платежів, а отримала лише шість бойових літаків. '
        'Водночас справжнє місце базування аргентинських F-16 — авіабаза 6-ї бригади '
        'повітряних сил, що базується у Танділі, поки не готова.'
    )

    for name, txt in [('Польща (field-labels)', poland_text),
                       ('Аргентина (referential)', argentina_text)]:
        r = v2.calculate(txt)
        print(f'{name}: score={r.score} (lex={r.lexical} struct={r.structural} '
              f'ref={r.referential}) anchors={r.anchor_count} '
              f'sentences={r.sentence_count} struct_hits={r.structural_hits}')
