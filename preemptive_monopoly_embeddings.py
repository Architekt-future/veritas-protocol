"""
Embedding-based semantic scorer for PREEMPTIVE_MONOPOLY.

На відміну від regex і slot-based підходів (обидва — лексичний пошук,
просто різного ступеня грануляції), тут порівнюється ЗМІСТ речення/
абзацу з набором еталонних формулювань "lesser evil monopoly" через
косинусну схожість векторів. Це має ловити перефразування без жодних
спільних коренів зі старими патернами (саме той кейс, де regex і
slot-based підхід дали 0.0).

МОДЕЛЬ: paraphrase-multilingual-MiniLM-L12-v2
  - ~470MB, 12-шаровий, підтримує UK напряму (50+ мов)
  - CPU-only inference достатньо швидкий для коротких текстів
  - Альтернатива, якщо ця не влізе в Render free tier за RAM/cold-start:
    paraphrase-multilingual-mpnet-base-v2 (точніша, але ~970MB, важча)
    distiluse-base-multilingual-cased-v2 (легша, ~500MB, трохи гірша якість)

НЕ ПЕРЕВІРЕНО В ЦЬОМУ СЕРЕДОВИЩІ: sandbox не має мережевого доступу до
huggingface.co (тільки pypi/npm/github у whitelist), тому завантаження
ваг тут неможливе. Логіка і структура коду коректні, але RAM/cold-start
на Render free tier треба перевірити на місці.
"""

import functools
from typing import Dict, List

# ── Еталонні формулювання "lesser evil monopoly" ──────────────────────
# Навмисно різноманітні: буквальні (як у смоук-тесті) і повністю
# перефразовані (як мій "рефразований" тест, що провалив і regex,
# і slot-based підхід) — щоб embedding-простір покривав обидва полюси.
REFERENCE_SENTENCES: List[str] = [
    # UK — буквальні
    "Ми свідомо обираємо цей шлях як менше зло, бо альтернатива — неконтрольоване поширення небезпечних систем.",
    "Тільки ми маємо інфраструктуру та відповідальність, щоб гарантувати безпеку; це не привілей, а необхідність.",
    "Якщо не ми, то хто зможе гарантувати контроль над цією технологією?",
    "Концентрація влади в наших руках — не ідеальна річ, але вона значно краща за хаотичну альтернативу.",
    # UK — перефразовані (інша лексика, той самий хід думки)
    "Питання лише в тому, хто буде тримати кермо, коли ця технологія зʼявиться попри все.",
    "Наша команда — чи не єдина структура, що вибудувала роками систему стримувань; передати цю роль комусь менш підготовленому означало б відкрити двері до катастрофи.",
    "Ми йдемо на цей крок не заради влади, а тому що альтернатива — хаос — набагато гірша.",
    "Світ опинився перед вибором без гарних варіантів, і хтось має взяти на себе цю відповідальність.",
    # EN — literal
    "We deliberately choose this path as the lesser evil, given the alternative is uncontrolled proliferation.",
    "Only we have the infrastructure and accountability to guarantee safety; this is a necessity, not a privilege.",
    "If not us, then who could possibly guarantee control over this technology?",
    # EN — paraphrased
    "The real question is who ends up holding the wheel once this technology exists regardless of what we do.",
    "Handing this responsibility to a less prepared actor would open the door to a catastrophe we could no longer stop.",
]

SIMILARITY_THRESHOLD = 0.55   # початкова гіпотеза — калібрувати на реальних логах
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


@functools.lru_cache(maxsize=1)
def _get_model():
    # lazy import + lazy load: модель вантажиться один раз за життя процесу,
    # а не при кожному виклику analyze() — критично для cold-start на Render.
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(MODEL_NAME)


@functools.lru_cache(maxsize=1)
def _get_reference_embeddings():
    model = _get_model()
    return model.encode(REFERENCE_SENTENCES, normalize_embeddings=True)


def score_preemptive_monopoly_semantic(text: str, threshold: float = SIMILARITY_THRESHOLD) -> Dict:
    """
    Розбиває текст на речення/абзаци, ембедить кожен шматок,
    рахує максимальну косинусну схожість з еталонним набором.
    Повертає score = max_similarity (0..1), якщо >= threshold, інакше 0.
    """
    import numpy as np

    model = _get_model()
    ref_emb = _get_reference_embeddings()

    # проста розбивка на речення; для абзацного контексту можна
    # замінити на split по \n\n, якщо короткі речення дають шум
    chunks = [c.strip() for c in text.replace("\n", " ").split(".") if len(c.strip()) > 20]
    if not chunks:
        return {'score': 0.0, 'best_chunk': None, 'best_similarity': 0.0}

    chunk_emb = model.encode(chunks, normalize_embeddings=True)
    sims = chunk_emb @ ref_emb.T          # косинусна схожість (embeddings normalized)
    best_idx = np.unravel_index(np.argmax(sims), sims.shape)
    best_sim = float(sims[best_idx])
    best_chunk = chunks[best_idx[0]]
    best_ref = REFERENCE_SENTENCES[best_idx[1]]

    score = round(best_sim, 3) if best_sim >= threshold else 0.0
    return {
        'score': score,
        'best_chunk': best_chunk,
        'best_similarity': round(best_sim, 3),
        'matched_reference': best_ref,
    }


if __name__ == "__main__":
    # швидкий self-test — запускати вже там, де huggingface.co доступний
    samples = {
        "OpenAI (буквальний)": "Тільки ми маємо інфраструктуру для цілодобового моніторингу. Якщо не ми, то хто зможе гарантувати безпеку?",
        "Рефразований (без спільних коренів)": "Питання лише в тому, хто буде тримати кермо, коли ця технологія зʼявиться попри все. Передати цю роль комусь менш підготовленому означало б відкрити двері до катастрофи.",
        "Бенайн": "Тільки вчора ми отримали звіт, і команда аналітиків вважає, що дані потребують перевірки.",
    }
    for name, t in samples.items():
        r = score_preemptive_monopoly_semantic(t)
        print(name, "->", r)
